#!/usr/bin/env python3
"""Validate the project that owns a storyboard.json. Exits 1 on contract errors only;
blockers (e.g. storyboard images not uploaded yet) are reported but do not fail CI."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from studio.project import load_project  # noqa: E402
from studio.validate import validate_project  # noqa: E402


def main(path):
    project = load_project(Path(path).resolve().parent)
    report = validate_project(project)
    for issue in report.errors + report.blockers:
        print(f"  {issue}")
    if report.ok:
        print(f"VALID: {project.id} | {len(project.scenes)} scenes | "
              f"{project.storyboard.get('duration_seconds')}s | {report.summary()}")
    else:
        print(f"INVALID: {report.summary()}")
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "projects/karaage-001/storyboard.json"))
