"""Status vocabulary, allowed transitions and guarded writes to production-status.json.

Only verified outcomes are written. Moving to ready_for_generation requires a clean
validation (no errors, no blockers); later transitions require their evidence
(e.g. every scene approved before ready_for_render).
"""
from datetime import datetime, timezone
from .project import resolve_asset

OVERALL_STATUSES = (
    "not_started",
    "ready_for_generation",
    "generating",
    "in_review",
    "ready_for_render",
    "rendered",
    "approved_for_publish",
    "published",
)

# Forward path plus explicit rollbacks to earlier review stages.
TRANSITIONS = {
    "not_started": {"ready_for_generation"},
    "ready_for_generation": {"generating", "not_started"},
    "generating": {"in_review", "ready_for_generation"},
    "in_review": {"ready_for_render", "generating"},
    "ready_for_render": {"rendered", "in_review"},
    "rendered": {"approved_for_publish", "in_review"},
    "approved_for_publish": {"published", "rendered"},
    "published": set(),
}

SCENE_STATUSES = ("pending", "generating", "generated", "approved", "rejected")


class StatusError(Exception):
    pass


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def check_transition(project, new_status, report=None):
    """Raise StatusError unless project may move to new_status."""
    current = project.status.get("overall_status")
    if new_status not in OVERALL_STATUSES:
        raise StatusError(f"unknown status {new_status!r}")
    if new_status not in TRANSITIONS.get(current, set()):
        raise StatusError(f"{current} -> {new_status} is not an allowed transition")
    if new_status == "ready_for_generation":
        if report is None or not report.ready:
            detail = report.summary() if report else "no validation report"
            raise StatusError(f"cannot mark ready_for_generation: {detail}")
    if new_status == "ready_for_render":
        unapproved = [sid for sid, s in project.status["scenes"].items()
                      if not (s.get("approved") and s.get("asset_path") and resolve_asset(s["asset_path"]).is_file())]
        if unapproved:
            raise StatusError(f"cannot mark ready_for_render: scenes not approved or file missing: {unapproved}")
    if new_status == "rendered" and not (project.status.get("render") or {}).get("verified"):
        raise StatusError("cannot mark rendered: no verified render recorded")
    if new_status == "approved_for_publish" and not project.status.get("publication", {}).get("approved"):
        raise StatusError("cannot mark approved_for_publish: publication.approved is false (human signoff required)")
    if new_status == "published":
        pub = project.status.get("publication", {})
        if not (pub.get("tiktok_url") or pub.get("youtube_url")):
            raise StatusError("cannot mark published: no published URL recorded")


def set_overall(project, new_status, report=None):
    check_transition(project, new_status, report)
    project.status["overall_status"] = new_status
    project.status.setdefault("history", []).append({"status": new_status, "at": now_iso()})


def record_validation(project, report):
    """Store the latest validation result and the blockers it found."""
    project.status["validation"] = {
        "checked_at": now_iso(),
        "result": "ready" if report.ready else ("blocked" if report.ok else "invalid"),
        "errors": [str(i) for i in report.errors],
        "blockers": [str(i) for i in report.blockers],
        "warnings": len(report.warnings),
    }
    blockers = [f"{i.where}: {i.message}" for i in report.errors + report.blockers]
    if not (project.root / "generation-approval.json").is_file():
        blockers.append("generation: no generation-approval.json (paid Higgsfield generation not approved)")
    project.status["blockers"] = blockers
    project.status["last_verified_at"] = project.status["validation"]["checked_at"]


def record_discrepancy(project, scene, source, issue, resolution, decided_by):
    """Record a reference/JSON conflict and how it was decided; the original issue text is kept."""
    entries = project.status.setdefault("discrepancies", [])
    entries[:] = [d for d in entries if (d.get("scene"), d.get("source")) != (scene, source)]
    entries.append({
        "scene": scene,
        "source": source,
        "issue": issue,
        "resolution": resolution,
        "decided_by": decided_by,
        "recorded_at": now_iso(),
    })


def set_scene(project, scene_id, status, asset_path=None, approved=None, note=None):
    scenes = project.status["scenes"]
    if scene_id not in scenes:
        raise StatusError(f"unknown scene {scene_id}")
    if status not in SCENE_STATUSES:
        raise StatusError(f"unknown scene status {status!r}")
    entry = scenes[scene_id]
    if status in ("generated", "approved"):
        path = asset_path or entry.get("asset_path")
        if not path or not resolve_asset(path).is_file():
            raise StatusError(f"{scene_id}: {status} requires an existing asset file, got {path!r}")
        entry["asset_path"] = str(path)
    if status == "approved":
        approved = True
    if status in ("pending", "generating", "rejected"):
        approved = False
    entry["status"] = status
    if approved is not None:
        entry["approved"] = approved
    if note:
        entry["note"] = note
    entry["updated_at"] = now_iso()
