"""Project discovery and read-only loading of project files."""
import json
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROJECTS_DIR = REPO_ROOT / "projects"

# Overall statuses that mean "a new project waiting for production work".
ACTIONABLE_STATUSES = ("not_started", "ready_for_generation")


def resolve_asset(path):
    """Asset paths in status/manifest files are absolute or relative to the repo root."""
    path = Path(path)
    return path if path.is_absolute() else REPO_ROOT / path


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


@dataclass
class Project:
    root: Path
    storyboard: dict
    status: dict
    prompts: dict = None
    pages: dict = None
    manifest: dict = None
    load_errors: list = field(default_factory=list)

    @property
    def id(self):
        return self.storyboard.get("project_id") or self.root.name

    @property
    def scenes(self):
        return self.storyboard.get("scenes") or []

    def prompt_for(self, scene_id):
        """Prompt entry for a scene: prompts.json if present, else the storyboard scene itself."""
        if self.prompts:
            for entry in self.prompts.get("scenes", []):
                if entry.get("id") == scene_id:
                    return entry
            return None
        for scene in self.scenes:
            if scene.get("id") == scene_id:
                return {"id": scene_id, "higgsfield_prompt": scene.get("prompt")}
        return None

    @property
    def status_path(self):
        return self.root / "production-status.json"


def _optional(path, errors):
    if not path.is_file():
        return None
    try:
        return load_json(path)
    except json.JSONDecodeError as exc:
        errors.append(f"{path.name}: invalid JSON ({exc})")
        return None


def load_project(root):
    root = Path(root)
    errors = []
    for name in ("storyboard.json", "production-status.json"):
        if not (root / name).is_file():
            errors.append(f"{name}: missing")
    storyboard = _optional(root / "storyboard.json", errors)
    status = _optional(root / "production-status.json", errors)
    return Project(
        root=root,
        storyboard=storyboard or {},
        status=status or {},
        prompts=_optional(root / "prompts.json", errors),
        pages=_optional(root / "pages.json", errors),
        manifest=_optional(root / "manifest.json", errors),
        load_errors=errors,
    )


def discover_projects(projects_dir=PROJECTS_DIR, statuses=None):
    """Return projects under projects_dir, optionally filtered by overall_status."""
    found = []
    for root in sorted(Path(projects_dir).iterdir()):
        if not (root / "storyboard.json").is_file():
            continue
        project = load_project(root)
        if statuses is None or project.status.get("overall_status") in statuses:
            found.append(project)
    return found
