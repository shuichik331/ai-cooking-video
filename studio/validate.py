"""Read-only validation of a project's ChatGPT-authored files.

Severity levels:
  error   - the files contradict each other or the input contract; ask ChatGPT for a revision.
  blocker - files are consistent but production cannot start yet (e.g. storyboard images missing).
  warning - recorded for human review; does not block.
"""
from dataclasses import dataclass, field

from .status import OVERALL_STATUSES, SCENE_STATUSES

STORYBOARD_FIELDS = ("project_id", "title", "aspect_ratio", "duration_seconds", "scenes")
SCENE_FIELDS = ("id", "start_seconds", "end_seconds", "shot")
PROMPT_DIRECTION_FIELDS = ("camera", "motion", "continuity")


@dataclass
class Issue:
    severity: str
    where: str
    message: str

    def __str__(self):
        return f"[{self.severity.upper()}] {self.where}: {self.message}"


@dataclass
class Report:
    project_id: str
    issues: list = field(default_factory=list)

    def add(self, severity, where, message):
        self.issues.append(Issue(severity, where, message))

    def by(self, severity):
        return [i for i in self.issues if i.severity == severity]

    @property
    def errors(self):
        return self.by("error")

    @property
    def blockers(self):
        return self.by("blocker")

    @property
    def warnings(self):
        return self.by("warning")

    @property
    def ok(self):
        """No contract errors (blockers may remain)."""
        return not self.errors

    @property
    def ready(self):
        """Nothing stands between this project and generation."""
        return not self.errors and not self.blockers

    def summary(self):
        return (f"{self.project_id}: {len(self.errors)} error(s), "
                f"{len(self.blockers)} blocker(s), {len(self.warnings)} warning(s)")


def validate_project(project):
    report = Report(project.id)
    for message in project.load_errors:
        report.add("error", "files", message)
    if not project.storyboard:
        return report
    _check_storyboard(project, report)
    _check_prompts(project, report)
    _check_pages(project, report)
    _check_status(project, report)
    _check_manifest(project, report)
    return report


def _scene_ids(project):
    return [s.get("id") for s in project.scenes]


def _check_storyboard(project, report):
    sb = project.storyboard
    for name in STORYBOARD_FIELDS:
        if sb.get(name) in (None, "", []):
            report.add("error", "storyboard.json", f"missing {name}")
    if sb.get("aspect_ratio") not in (None, "9:16"):
        report.add("error", "storyboard.json", f"aspect_ratio is {sb['aspect_ratio']}, expected 9:16")
    if project.root.name != sb.get("project_id"):
        report.add("error", "storyboard.json", f"project_id {sb.get('project_id')!r} != folder {project.root.name!r}")

    cursor, seen = 0, set()
    for scene in project.scenes:
        sid = scene.get("id", "?")
        where = f"storyboard.json {sid}"
        missing = [f for f in SCENE_FIELDS if scene.get(f) in (None, "")]
        if missing:
            report.add("error", where, f"missing {', '.join(missing)}")
            continue
        if sid in seen:
            report.add("error", where, "duplicate scene id")
        seen.add(sid)
        start, end = scene["start_seconds"], scene["end_seconds"]
        if start != cursor:
            report.add("error", where, f"timeline gap/overlap: starts at {start}s, previous scene ended at {cursor}s")
        if end <= start:
            report.add("error", where, f"end {end}s is not after start {start}s")
        if "duration_seconds" in scene and scene["duration_seconds"] != end - start:
            report.add("error", where, f"duration_seconds {scene['duration_seconds']} != end-start {end - start}")
        cursor = end
    if project.scenes and sb.get("duration_seconds") is not None and cursor != sb["duration_seconds"]:
        report.add("error", "storyboard.json", f"scenes end at {cursor}s but duration_seconds is {sb['duration_seconds']}")


def _check_prompts(project, report):
    ids = _scene_ids(project)
    if project.prompts is None:
        for scene in project.scenes:
            if not scene.get("prompt"):
                report.add("error", f"storyboard.json {scene.get('id')}", "no prompt and no prompts.json")
        report.add("warning", "prompts.json", "not provided; storyboard prompts used, camera/motion/continuity unspecified")
        return
    pr = project.prompts
    if pr.get("project_id") != project.id:
        report.add("error", "prompts.json", f"project_id {pr.get('project_id')!r} != {project.id!r}")
    entries = pr.get("scenes") or []
    pids = [e.get("id") for e in entries]
    if pids != ids:
        missing = [i for i in ids if i not in pids]
        extra = [i for i in pids if i not in ids]
        detail = f"missing {missing}, extra {extra}" if missing or extra else "same ids, different order"
        report.add("error", "prompts.json", f"scene ids do not match storyboard ({detail})")
    page_of = _page_index(project)
    for entry in entries:
        sid = entry.get("id")
        where = f"prompts.json {sid}"
        if not (entry.get("higgsfield_prompt") or "").strip():
            report.add("error", where, "empty higgsfield_prompt")
        absent = [f for f in PROMPT_DIRECTION_FIELDS if not (entry.get(f) or "").strip()]
        if absent:
            report.add("warning", where, f"no {', '.join(absent)}")
        ref = entry.get("reference_page")
        if page_of and ref and page_of.get(sid) and ref != page_of[sid]["file"]:
            report.add("error", where, f"reference_page {ref} but pages.json maps {sid} to {page_of[sid]['file']}")
        if entry.get("reference_panel") not in (None, sid):
            report.add("error", where, f"reference_panel {entry['reference_panel']!r} != scene id")


def _page_index(project):
    """scene id -> {"file", "number"} from pages.json."""
    index = {}
    for number, page in enumerate((project.pages or {}).get("pages", []), start=1):
        for sid in page.get("scene_ids", []):
            index.setdefault(sid, {"file": page.get("file"), "number": number, "dupes": 0})["dupes"] += 1
    return index


def _check_pages(project, report):
    if project.pages is None:
        report.add("blocker", "storyboard-pages", "no pages.json / storyboard images; image cross-check impossible")
        return
    pages = project.pages.get("pages", [])
    index = _page_index(project)
    for sid in _scene_ids(project):
        if sid not in index:
            report.add("error", "pages.json", f"{sid} is not on any page")
        elif index[sid]["dupes"] > 1:
            report.add("error", "pages.json", f"{sid} appears on more than one page")
    for sid in index:
        if sid not in _scene_ids(project):
            report.add("error", "pages.json", f"{sid} is not in storyboard")
    for page in pages:
        ids = page.get("scene_ids", [])
        if ids and (page.get("first_scene"), page.get("last_scene")) != (ids[0], ids[-1]):
            report.add("error", f"pages.json {page.get('file')}", "first_scene/last_scene do not match scene_ids")
    for scene in project.scenes:
        sid = scene.get("id")
        if "page" in scene and sid in index and scene["page"] != index[sid]["number"]:
            report.add("error", f"storyboard.json {sid}", f"page {scene['page']} but pages.json puts it on page {index[sid]['number']}")

    missing = [p.get("file") for p in pages if not (project.root / p.get("file", "")).is_file()]
    if missing:
        report.add("blocker", "storyboard-pages", f"{len(missing)} of {len(pages)} image(s) not in repo: {', '.join(missing)}")
    elif project.pages.get("images_uploaded") is False:
        report.add("warning", "pages.json", "images_uploaded is false but all image files exist")

    verification = project.status.get("image_verification", {}).get("status")
    if not missing and verification != "verified":
        report.add("blocker", "storyboard-pages", "images present but image/JSON cross-check not yet recorded as verified")

    resolved = {(d.get("scene"), d.get("source")) for d in project.status.get("discrepancies", []) if d.get("resolution")}
    for issue in project.pages.get("known_reference_issues", []):
        key = (issue.get("scene"), "pages.json")
        text = f"page {issue.get('page')}: {issue.get('issue')}"
        if key in resolved:
            report.add("warning", f"discrepancy {issue.get('scene')}", f"{text} (resolution recorded in production-status.json)")
        else:
            report.add("blocker", f"discrepancy {issue.get('scene')}", f"{text} (no recorded resolution)")


def _check_status(project, report):
    st = project.status
    if not st:
        return
    overall = st.get("overall_status")
    if overall not in OVERALL_STATUSES:
        report.add("error", "production-status.json", f"unknown overall_status {overall!r}")
    ids = _scene_ids(project)
    scenes = st.get("scenes") or {}
    if list(scenes) != ids:
        report.add("error", "production-status.json", "scene keys do not match storyboard ids/order")
    for sid, entry in scenes.items():
        if entry.get("status") not in SCENE_STATUSES:
            report.add("error", f"production-status.json {sid}", f"unknown scene status {entry.get('status')!r}")
        if entry.get("approved") and not entry.get("asset_path"):
            report.add("error", f"production-status.json {sid}", "approved without asset_path")


def _check_manifest(project, report):
    if project.manifest is None:
        return
    ids = _scene_ids(project)
    keys = list((project.manifest.get("scenes") or {}).keys())
    extra = [k for k in keys if k not in ids]
    if extra:
        report.add("error", "manifest.json", f"unknown scene ids {extra}")
