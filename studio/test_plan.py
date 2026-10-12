"""Single 5-second Seedance proof: request draft, references and gates. Never submits anything."""
from .higgsfield import APPROVAL_FILE
from .panels import CROP_DIR, LAYOUT_FILE
from .scene_sheet import build_sheet, load_generation_config
from .status import now_iso
from .validate import validate_project

PLAN_FILE = "seedance-test-plan.json"

REVIEW_CHECKLIST = [
    "framing, subject and action match the storyboard panel",
    "hand anatomy (finger count, grip, no merging with utensils)",
    "food state matches the step (raw vs cooked, batter, sauce)",
    "protagonist, kitchen, cookware and lighting match the global prompt",
    "no captions, watermarks or invented cooking steps",
    "usable 1-second window for the edit (cut stays inside the scene's action)",
]


def build_test_plan(project, scene_id, config=None, selected_by=None, objectives=None):
    config = config or load_generation_config()
    test = config["test_generation"]
    report = validate_project(project)
    sheet = build_sheet(project, report, config)
    scene = next((s for s in sheet["scenes"] if s["scene_id"] == scene_id), None)
    if scene is None:
        raise ValueError(f"unknown scene {scene_id}")
    crop = CROP_DIR / project.id / "panels" / f"{scene_id}.png"
    upscaled = crop.with_name(f"{scene_id}@4x.png")
    rate = config["observed_credits_per_second"][test["resolution"]]

    def relevant(issue):
        # Discrepancies about other scenes do not block a single-scene proof.
        return not issue.where.startswith("discrepancy ") or issue.where == f"discrepancy {scene_id}"

    blockers = [f"{i.where}: {i.message}" for i in report.errors + report.blockers if relevant(i)]
    if not (project.root / LAYOUT_FILE).is_file():
        blockers.append(f"{LAYOUT_FILE} missing: panel grid not confirmed from the real pages")
    if not crop.is_file():
        blockers.append(f"reference crop {crop.relative_to(CROP_DIR.parent)} missing (run studio.py crop-panels)")
    blockers.append("reference crop not yet uploaded to Higgsfield (media_upload -> media_id)")
    blockers.append("live quote with the actual reference not yet taken (get_cost)")
    if not (project.root / APPROVAL_FILE).is_file():
        blockers.append(f"no {APPROVAL_FILE}: user approval of the test cost required")

    return {
        "project_id": project.id,
        "created_at": now_iso(),
        "status": "blocked" if blockers else "ready_for_approval",
        "purpose": "One paid 5-second proof before any batch generation.",
        "scene_selection": selected_by or "proposal; the user/ChatGPT confirm which scene is tested",
        "objectives": objectives or [],
        "scene": {k: scene[k] for k in ("scene_id", "start_seconds", "end_seconds", "duration_seconds", "shot",
                                        "visual_description", "camera", "motion", "continuity", "discrepancies")},
        "reference": {
            "page_file": scene["reference"]["page_file"],
            "panel": scene["reference"]["panel"],
            "crop_path": str(crop.relative_to(CROP_DIR.parent)),
            "crop_exists": crop.is_file(),
            "upload_candidate": str(upscaled.relative_to(CROP_DIR.parent)),
            "upload_candidate_exists": upscaled.is_file(),
            "upscale": "4x Lanczos (local, free) because storyboard panels are ~250 px wide",
            "higgsfield_media_id": None,
            "role": test["reference_role"],
        },
        "request": {
            "tool": "generate_video",
            "params": {
                "model": config["model"],
                "mode": test["mode"],
                "prompt": scene["higgsfield_prompt"],
                "duration": test["duration_seconds"],
                "resolution": test["resolution"],
                "aspect_ratio": scene["generation"]["aspect_ratio"],
                "generate_audio": test["generate_audio"],
                "medias": [{"role": test["reference_role"], "value": "<media_id of the uploaded crop>"}],
            },
        },
        "cost": {
            "estimated_credits": rate * test["duration_seconds"],
            "basis": test["quote_note"],
            "must_requote": True,
        },
        "edit_use": {
            "use_seconds": scene["duration_seconds"],
            "trim": "window chosen at review (trim_in_seconds); default start of clip",
        },
        "blockers": blockers,
        "review_checklist": REVIEW_CHECKLIST,
    }
