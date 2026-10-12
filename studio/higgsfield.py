"""Higgsfield generation interface: request building, spend approval and job/clip records.

Design (see docs/higgsfield-integration.md):
- This module never calls Higgsfield. It builds requests from the generation sheet,
  enforces a human spend approval, and records what actually happened.
- Submission happens through one of two backends:
    * manual  - a human generates in the Higgsfield web app and registers the downloaded
                file with `studio.py register-clip`.
    * mcp     - Claude Code submits the queued requests with the Higgsfield MCP tools
                (get_cost quote first, then generate_video) and records job ids with
                `studio.py record-job`. MCP tools are only callable from the agent session,
                so there is deliberately no Python HTTP client and no API key handling here.
"""
from dataclasses import asdict, dataclass, field

from .project import load_json, resolve_asset, write_json
from .render import probe
from .status import StatusError, now_iso, set_scene

APPROVAL_FILE = "generation-approval.json"
QUEUE_FILE = "generation-queue.json"


class ApprovalError(Exception):
    pass


@dataclass
class GenerationRequest:
    scene_id: str
    model: str
    prompt: str
    duration: int
    resolution: str
    aspect_ratio: str
    generate_audio: bool
    # Filled once storyboard panel crops are uploaded to Higgsfield (media_upload -> media_id).
    medias: list = field(default_factory=list)
    reference_page: str = None
    reference_panel: str = None
    idempotency_key: str = None
    estimated_credits: float = None

    def mcp_params(self):
        """Arguments for the Higgsfield MCP generate_video tool."""
        params = {
            "model": self.model,
            "prompt": self.prompt,
            "duration": self.duration,
            "resolution": self.resolution,
            "aspect_ratio": self.aspect_ratio,
            "generate_audio": self.generate_audio,
        }
        if self.medias:
            params["medias"] = self.medias
        return params


def build_requests(project, sheet, config, resolution, generate_audio, scene_ids=None):
    if resolution not in config["model_constraints"]["resolutions"]:
        raise ValueError(f"resolution {resolution!r} not in {config['model_constraints']['resolutions']}")
    rate = config["observed_credits_per_second"].get(resolution)
    requests = []
    for s in sheet["scenes"]:
        if scene_ids and s["scene_id"] not in scene_ids:
            continue
        attempt = len(project.status["scenes"][s["scene_id"]].get("jobs", [])) + 1
        seconds = s["generation"]["generate_seconds"]
        requests.append(GenerationRequest(
            scene_id=s["scene_id"],
            model=s["generation"]["model"],
            prompt=s["higgsfield_prompt"],
            duration=seconds,
            resolution=resolution,
            aspect_ratio=s["generation"]["aspect_ratio"],
            generate_audio=generate_audio,
            reference_page=s["reference"]["page_file"],
            reference_panel=s["reference"]["panel"],
            idempotency_key=f"{project.id}:{s['scene_id']}:{attempt}",
            estimated_credits=rate * seconds if rate is not None else None,
        ))
    return requests


def load_approval(project):
    path = project.root / APPROVAL_FILE
    return load_json(path) if path.is_file() else None


def spent_credits(project):
    return sum(job.get("credits") or 0 for s in project.status["scenes"].values() for job in s.get("jobs", []))


def check_approval(project, requests):
    """Raise ApprovalError unless a human approval covers these requests and their cost."""
    if project.status.get("overall_status") not in ("ready_for_generation", "generating", "in_review"):
        raise ApprovalError(f"project is {project.status.get('overall_status')}; must be ready_for_generation first")
    approval = load_approval(project)
    if not approval:
        raise ApprovalError(f"no {APPROVAL_FILE}; a human must approve scenes, resolution and max_credits")
    for key in ("approved_by", "approved_at", "max_credits", "resolution", "scene_ids"):
        if approval.get(key) in (None, "", []):
            raise ApprovalError(f"{APPROVAL_FILE}: missing {key}")
    problems = []
    for r in requests:
        if r.scene_id not in approval["scene_ids"]:
            problems.append(f"{r.scene_id} not in approved scene_ids")
        if r.resolution != approval["resolution"]:
            problems.append(f"{r.scene_id} resolution {r.resolution} != approved {approval['resolution']}")
    if problems:
        raise ApprovalError("; ".join(problems))
    planned = sum(r.estimated_credits or 0 for r in requests)
    already = spent_credits(project)
    if already + planned > approval["max_credits"]:
        raise ApprovalError(f"spent {already} + planned {planned} credits exceeds approved max {approval['max_credits']}")
    return approval


def write_queue(project, requests, approval):
    data = {
        "project_id": project.id,
        "created_at": now_iso(),
        "approval": {k: approval[k] for k in ("approved_by", "approved_at", "max_credits")},
        "note": "Submit one scene at a time. Re-quote each with get_cost and stop if the quote differs.",
        "requests": [{**asdict(r), "mcp_params": r.mcp_params()} for r in requests],
    }
    write_json(project.root / QUEUE_FILE, data)
    return data


def record_job(project, scene_id, job_id, credits, resolution, backend="mcp"):
    """Record a submitted job with its actual quoted/charged credits."""
    entry = project.status["scenes"].get(scene_id)
    if entry is None:
        raise StatusError(f"unknown scene {scene_id}")
    entry.setdefault("jobs", []).append({
        "job_id": job_id, "backend": backend, "credits": credits,
        "resolution": resolution, "submitted_at": now_iso(),
    })
    set_scene(project, scene_id, "generating")


def register_clip(project, scene_id, path, min_seconds=None):
    """Attach a downloaded/uploaded clip after probing it; marks the scene generated (not approved)."""
    resolved = resolve_asset(path)
    if not resolved.is_file():
        raise StatusError(f"{scene_id}: clip not found {resolved}")
    info = probe(resolved)
    if info["video"] is None:
        raise StatusError(f"{scene_id}: {resolved} has no video stream")
    scene = next(s for s in project.scenes if s["id"] == scene_id)
    needed = min_seconds or (scene["end_seconds"] - scene["start_seconds"])
    if info["duration"] + 1e-3 < needed:
        raise StatusError(f"{scene_id}: clip is {info['duration']:.2f}s, scene needs {needed}s")
    set_scene(project, scene_id, "generated", asset_path=str(path))
    project.status["scenes"][scene_id]["probe"] = {
        "duration_seconds": round(info["duration"], 3),
        "width": info["video"]["width"],
        "height": info["video"]["height"],
        "audio": bool(info["audio"]),
    }
