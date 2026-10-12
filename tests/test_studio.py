import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from studio import higgsfield, panels, prompt_audit, render, scene_sheet, status, test_plan  # noqa: E402
from studio.project import discover_projects, load_project, write_json  # noqa: E402
from studio.validate import validate_project  # noqa: E402

HAS_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))
GLOBAL = "Shared style."


def make_project(base, pid="demo-001", n=3, overall="not_started", images=False):
    root = Path(base) / pid
    (root / "storyboard-pages").mkdir(parents=True)
    ids = [f"s{i:02d}" for i in range(1, n + 1)]
    write_json(root / "storyboard.json", {
        "project_id": pid, "title": "Demo", "aspect_ratio": "9:16", "duration_seconds": n,
        "scenes": [{"id": sid, "start_seconds": i, "end_seconds": i + 1, "duration_seconds": 1,
                    "shot": f"shot {sid}", "page": 1, "frame_number": i + 1} for i, sid in enumerate(ids)],
    })
    write_json(root / "prompts.json", {
        "project_id": pid, "global_prompt": GLOBAL,
        "scenes": [{"id": sid, "camera": "close", "motion": "slow", "continuity": "same pan",
                    "higgsfield_prompt": f"Scene {sid}. {GLOBAL}",
                    "reference_page": "storyboard-pages/page-01.png", "reference_panel": sid} for sid in ids],
    })
    write_json(root / "pages.json", {
        "project_id": pid,
        "pages": [{"file": "storyboard-pages/page-01.png", "first_scene": ids[0], "last_scene": ids[-1], "scene_ids": ids}],
    })
    write_json(root / "production-status.json", {
        "project_id": pid, "overall_status": overall, "last_verified_at": None,
        "scenes": {sid: {"status": "pending", "asset_path": None, "approved": False} for sid in ids},
        "publication": {"approved": False, "tiktok_url": None, "youtube_url": None},
    })
    if images:
        (root / "storyboard-pages" / "page-01.png").write_bytes(b"\x89PNG")
    return root


def edit_json(path, fn):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    fn(data)
    write_json(path, data)


def messages(report, severity):
    return " | ".join(i.message for i in report.by(severity))


class TempDirTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)


class DiscoveryTest(TempDirTest):
    def test_filters_by_status(self):
        make_project(self.tmp, "a-001", overall="not_started")
        make_project(self.tmp, "b-001", overall="ready_for_generation")
        make_project(self.tmp, "c-001", overall="published")
        (Path(self.tmp) / "notes").mkdir()
        found = [p.id for p in discover_projects(self.tmp, ("not_started", "ready_for_generation"))]
        self.assertEqual(found, ["a-001", "b-001"])
        self.assertEqual(len(discover_projects(self.tmp)), 3)


class ValidationTest(TempDirTest):
    def test_missing_images_block_but_do_not_error(self):
        report = validate_project(load_project(make_project(self.tmp)))
        self.assertTrue(report.ok)
        self.assertFalse(report.ready)
        self.assertIn("not in repo", messages(report, "blocker"))

    def test_images_need_recorded_verification(self):
        root = make_project(self.tmp, images=True)
        self.assertIn("not yet recorded as verified", messages(validate_project(load_project(root)), "blocker"))
        edit_json(root / "production-status.json", lambda d: d.update(image_verification={"status": "verified"}))
        self.assertTrue(validate_project(load_project(root)).ready)

    def test_timeline_gap_is_error(self):
        root = make_project(self.tmp)
        edit_json(root / "storyboard.json", lambda d: d["scenes"][1].update(start_seconds=2, end_seconds=3))
        self.assertIn("timeline gap", messages(validate_project(load_project(root)), "error"))

    def test_duration_field_mismatch_is_error(self):
        root = make_project(self.tmp)
        edit_json(root / "storyboard.json", lambda d: d["scenes"][0].update(duration_seconds=2))
        self.assertIn("duration_seconds 2", messages(validate_project(load_project(root)), "error"))

    def test_prompt_ids_must_match(self):
        root = make_project(self.tmp)
        edit_json(root / "prompts.json", lambda d: d["scenes"].pop())
        self.assertIn("missing ['s03']", messages(validate_project(load_project(root)), "error"))

    def test_reference_page_must_match_pages_json(self):
        root = make_project(self.tmp)
        edit_json(root / "prompts.json", lambda d: d["scenes"][0].update(reference_page="storyboard-pages/page-09.png"))
        self.assertIn("reference_page", messages(validate_project(load_project(root)), "error"))

    def test_storyboard_page_must_match_pages_json(self):
        root = make_project(self.tmp)
        edit_json(root / "storyboard.json", lambda d: d["scenes"][0].update(page=2))
        self.assertIn("pages.json puts it on page 1", messages(validate_project(load_project(root)), "error"))

    def test_known_issue_blocks_until_resolution_recorded(self):
        root = make_project(self.tmp)
        edit_json(root / "pages.json", lambda d: d.update(known_reference_issues=[{"page": 1, "scene": "s02", "issue": "bad time"}]))
        self.assertIn("bad time", messages(validate_project(load_project(root)), "blocker"))
        project = load_project(root)
        status.record_discrepancy(project, "s02", "pages.json", "bad time", "use JSON", "user")
        write_json(project.status_path, project.status)
        report = validate_project(load_project(root))
        self.assertNotIn("bad time", messages(report, "blocker"))
        self.assertIn("bad time", messages(report, "warning"))

    def test_unknown_status_is_error(self):
        root = make_project(self.tmp, overall="done")
        self.assertIn("unknown overall_status", messages(validate_project(load_project(root)), "error"))

    def test_legacy_storyboard_without_prompts_json(self):
        root = make_project(self.tmp)
        (root / "prompts.json").unlink()
        (root / "pages.json").unlink()
        edit_json(root / "storyboard.json", lambda d: [s.update(prompt="p") for s in d["scenes"]])
        report = validate_project(load_project(root))
        self.assertTrue(report.ok)
        self.assertIn("no pages.json", messages(report, "blocker"))


class StatusTest(TempDirTest):
    def test_ready_requires_clean_report(self):
        project = load_project(make_project(self.tmp))
        with self.assertRaises(status.StatusError):
            status.set_overall(project, "ready_for_generation", validate_project(project))

    def test_ready_when_clean(self):
        root = make_project(self.tmp, images=True)
        edit_json(root / "production-status.json", lambda d: d.update(image_verification={"status": "verified"}))
        project = load_project(root)
        status.set_overall(project, "ready_for_generation", validate_project(project))
        self.assertEqual(project.status["overall_status"], "ready_for_generation")
        self.assertEqual(project.status["history"][-1]["status"], "ready_for_generation")

    def test_illegal_transition(self):
        project = load_project(make_project(self.tmp))
        with self.assertRaises(status.StatusError):
            status.set_overall(project, "published")

    def test_scene_generated_requires_file(self):
        project = load_project(make_project(self.tmp))
        with self.assertRaises(status.StatusError):
            status.set_scene(project, "s01", "generated", asset_path=str(Path(self.tmp) / "nope.mp4"))

    def test_record_validation_adds_spend_blocker(self):
        project = load_project(make_project(self.tmp))
        status.record_validation(project, validate_project(project))
        self.assertEqual(project.status["validation"]["result"], "blocked")
        self.assertTrue(any("not approved" in b for b in project.status["blockers"]))


class SheetTest(TempDirTest):
    def test_fields_are_verbatim(self):
        root = make_project(self.tmp)
        edit_json(root / "prompts.json", lambda d: d["scenes"][1].update(camera=""))
        project = load_project(root)
        sheet = scene_sheet.build_sheet(project, validate_project(project))
        prompts = {e["id"]: e for e in project.prompts["scenes"]}
        for s in sheet["scenes"]:
            self.assertEqual(s["higgsfield_prompt"], prompts[s["scene_id"]]["higgsfield_prompt"])
            self.assertEqual(s["generation"]["generate_seconds"], 4)
            self.assertEqual(s["generation"]["use_seconds"], 1)
        self.assertEqual(sheet["scenes"][0]["visual_description"], "Scene s01.")
        self.assertEqual(sheet["scenes"][1]["unspecified"], ["camera"])
        self.assertIn("| s02 |", scene_sheet.render_markdown(sheet))
        self.assertEqual(scene_sheet.estimate_credits(sheet)["480p"], 3 * 4 * 3)


class ApprovalTest(TempDirTest):
    def setUp(self):
        super().setUp()
        self.root = make_project(self.tmp, overall="ready_for_generation")
        self.project = load_project(self.root)
        self.config = scene_sheet.load_generation_config()
        self.sheet = scene_sheet.build_sheet(self.project, None, self.config)

    def requests(self, scenes=None):
        return higgsfield.build_requests(self.project, self.sheet, self.config, "480p", False, scenes)

    def approve(self, **kw):
        data = {"approved_by": "human", "approved_at": "2026-10-12", "max_credits": 100,
                "resolution": "480p", "scene_ids": ["s01", "s02"], **kw}
        write_json(self.root / higgsfield.APPROVAL_FILE, data)

    def test_no_approval_refuses(self):
        with self.assertRaises(higgsfield.ApprovalError):
            higgsfield.check_approval(self.project, self.requests())

    def test_not_ready_project_refuses(self):
        self.approve()
        self.project.status["overall_status"] = "not_started"
        with self.assertRaises(higgsfield.ApprovalError):
            higgsfield.check_approval(self.project, self.requests(["s01"]))

    def test_unapproved_scene_refuses(self):
        self.approve()
        with self.assertRaises(higgsfield.ApprovalError):
            higgsfield.check_approval(self.project, self.requests())

    def test_budget_includes_spent_credits(self):
        self.approve(max_credits=30)
        higgsfield.check_approval(self.project, self.requests(["s01", "s02"]))  # 24 credits
        self.project.status["scenes"]["s01"]["jobs"] = [{"credits": 12}]
        with self.assertRaises(higgsfield.ApprovalError):
            higgsfield.check_approval(self.project, self.requests(["s01", "s02"]))

    def test_queue_contains_mcp_params(self):
        self.approve()
        reqs = self.requests(["s01"])
        data = higgsfield.write_queue(self.project, reqs, higgsfield.check_approval(self.project, reqs))
        params = data["requests"][0]["mcp_params"]
        self.assertEqual(params["model"], "seedance_2_5")
        self.assertEqual(params["duration"], 4)
        self.assertEqual(params["prompt"], f"Scene s01. {GLOBAL}")
        self.assertEqual(data["requests"][0]["idempotency_key"], "demo-001:s01:1")


def make_clip(path, seconds, size="720x1280", audio=True):
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"testsrc2=size={size}:rate=24:duration={seconds}"]
    if audio:
        cmd += ["-f", "lavfi", "-i", f"sine=f=440:d={seconds}", "-c:a", "aac"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-shortest", str(path)]
    subprocess.run(cmd, check=True)


@unittest.skipUnless(HAS_FFMPEG, "ffmpeg not installed")
class RenderTest(TempDirTest):
    def setUp(self):
        super().setUp()
        self.root = make_project(self.tmp, n=3, overall="in_review")
        clips = Path(self.tmp) / "media"
        clips.mkdir()
        # portrait with audio, landscape with audio, portrait without audio
        for sid, size, audio in (("s01", "720x1280", True), ("s02", "1280x720", True), ("s03", "720x1280", False)):
            make_clip(clips / f"{sid}.mp4", 4, size, audio)
        self.project = load_project(self.root)
        for sid in ("s01", "s02", "s03"):
            higgsfield.register_clip(self.project, sid, str(clips / f"{sid}.mp4"))
        self.out = Path(self.tmp) / "out" / "final.mp4"

    def test_unapproved_clips_refused(self):
        with self.assertRaises(render.RenderError):
            render.render(self.project, self.out)

    def test_render_and_verify(self):
        for sid in ("s01", "s02", "s03"):
            status.set_scene(self.project, sid, "approved")
        status.set_overall(self.project, "ready_for_render")
        for fit in ("pad", "crop"):
            result = render.render(self.project, self.out, fit=fit, trim_anchor="center")
            self.assertTrue(result["verified"], result["problems"])
            self.assertEqual((result["width"], result["height"], result["fps"]), (1080, 1920, 30))
            self.assertTrue(result["audio"])
            self.assertAlmostEqual(result["duration_seconds"], 3, delta=0.05)

    def test_silent_render(self):
        result = render.render(self.project, self.out, audio=False, allow_unapproved=True)
        self.assertTrue(result["verified"], result["problems"])
        self.assertFalse(result["audio"])

    def test_clip_shorter_than_scene_refused(self):
        short = Path(self.tmp) / "short.mp4"
        make_clip(short, 0.5)
        with self.assertRaises(status.StatusError):
            higgsfield.register_clip(self.project, "s01", str(short))

    def test_verify_flags_wrong_spec(self):
        bad = Path(self.tmp) / "bad.mp4"
        make_clip(bad, 2, "1280x720")
        result = render.verify(bad, self.project, expect_audio=True)
        self.assertFalse(result["verified"])
        self.assertTrue(any("size" in p for p in result["problems"]))
        self.assertTrue(any("duration" in p for p in result["problems"]))


@unittest.skipUnless(HAS_FFMPEG, "ffmpeg not installed")
class PanelTest(TempDirTest):
    def setUp(self):
        super().setUp()
        self.root = make_project(self.tmp, n=4)
        # 2x2 page, each 200x300 cell a different solid colour
        page = self.root / "storyboard-pages" / "page-01.png"
        colors = ["red", "green", "blue", "yellow"]
        inputs = []
        for c in colors:
            inputs += ["-f", "lavfi", "-i", f"color=c={c}:s=200x300:d=1"]
        subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex",
                        "[0][1]hstack[t];[2][3]hstack[b];[t][b]vstack", "-frames:v", "1", str(page)], check=True)
        self.project = load_project(self.root)

    def test_missing_layout_refused(self):
        with self.assertRaises(panels.PanelError):
            panels.crop_panels(self.project, Path(self.tmp) / "crops")

    def test_grid_crop_maps_scenes_in_reading_order(self):
        write_json(self.root / panels.LAYOUT_FILE, {"pages": {"storyboard-pages/page-01.png": {
            "grid": {"rows": 2, "cols": 2}, "panel_inset": {"left": 0.1, "top": 0.1, "right": 0.1, "bottom": 0.2}}}})
        crops = panels.crop_panels(load_project(self.root), Path(self.tmp) / "crops")
        self.assertEqual(list(crops), ["s01", "s02", "s03", "s04"])
        expected = {"s01": (255, 0, 0), "s02": (0, 128, 0), "s03": (0, 0, 255), "s04": (255, 255, 0)}
        for sid, path in crops.items():
            info = render.probe(path)["video"]
            self.assertEqual((info["width"], info["height"]), (160, 210))
            rgb = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", "scale=1:1", "-f", "rawvideo",
                                  "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
            for got, want in zip(rgb, expected[sid]):
                self.assertAlmostEqual(got, want, delta=12)
        self.assertTrue(panels.contact_sheet(crops, Path(self.tmp) / "sheet.png").is_file())

    def test_grid_too_small(self):
        with self.assertRaises(panels.PanelError):
            panels.panel_boxes(400, 600, {"grid": {"rows": 1, "cols": 2}}, 4)


class TestPlanTest(TempDirTest):
    def test_plan_is_blocked_and_verbatim(self):
        project = load_project(make_project(self.tmp))
        plan = test_plan.build_test_plan(project, "s02")
        self.assertEqual(plan["status"], "blocked")
        params = plan["request"]["params"]
        self.assertEqual(params["prompt"], f"Scene s02. {GLOBAL}")
        self.assertEqual((params["duration"], params["resolution"], params["mode"]), (5, "720p", "omni_reference"))
        self.assertFalse(params["generate_audio"])
        self.assertEqual(plan["cost"]["estimated_credits"], 35)
        self.assertTrue(any("approval" in b for b in plan["blockers"]))


class PromptAuditTest(TempDirTest):
    def test_flags_old_structure_and_passes_single_shot(self):
        root = make_project(self.tmp)
        edit_json(root / "prompts.json", lambda d: (
            d["scenes"][0].update(higgsfield_prompt=f"Scene s01 cooked from raw chicken thigh through frying. {GLOBAL}"),
            d["scenes"][1].update(higgsfield_prompt="SINGLE CONTINUOUS SHOT, 5 seconds, NO CUTS. Absolutely no montage or transitions.",
                                  camera="locked macro on the bowl", motion="whisk turns twice", test_generation={}),
        ))
        rows = {r["scene_id"]: {f["code"] for f in r["findings"]} for r in prompt_audit.audit(load_project(root))}
        self.assertIn("recipe-sentence", rows["s01"])
        self.assertIn("no-single-shot", rows["s01"])
        self.assertEqual(rows["s02"], set())

    def test_audit_never_writes_prompts(self):
        root = make_project(self.tmp)
        before = (root / "prompts.json").read_bytes()
        prompt_audit.audit(load_project(root))
        self.assertEqual(before, (root / "prompts.json").read_bytes())


class ProvisionalStatusTest(TempDirTest):
    def test_provisional_requires_file_and_is_not_approved(self):
        project = load_project(make_project(self.tmp))
        with self.assertRaises(status.StatusError):
            status.set_scene(project, "s01", "provisional")
        clip = Path(self.tmp) / "c.mp4"
        clip.write_bytes(b"x")
        status.set_scene(project, "s01", "provisional", asset_path=str(clip))
        self.assertFalse(project.status["scenes"]["s01"]["approved"])


class RealProjectsTest(unittest.TestCase):
    """The committed projects must keep validating without contract errors."""

    def test_projects_have_no_errors(self):
        for project in discover_projects():
            report = validate_project(project)
            self.assertTrue(report.ok, f"{project.id}: {[str(i) for i in report.errors]}")

    def test_chicken_nanban_s26_timing(self):
        project = load_project(REPO / "projects" / "chicken-nanban-001")
        s26 = next(s for s in project.scenes if s["id"] == "s26")
        self.assertEqual((s26["start_seconds"], s26["end_seconds"]), (25, 26))
        self.assertTrue(any(d["scene"] == "s26" and d.get("resolution") for d in project.status.get("discrepancies", [])))


if __name__ == "__main__":
    unittest.main()
