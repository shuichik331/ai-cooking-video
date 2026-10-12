#!/usr/bin/env python3
"""Legacy entry point: render a project from its manifest.json clip paths.
Prefer `scripts/studio.py render PROJECT`, which reads approved clips from production-status.json."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from studio import render  # noqa: E402
from studio.project import load_project  # noqa: E402

p = argparse.ArgumentParser()
p.add_argument("manifest")
p.add_argument("--output", required=True)
p.add_argument("--fit", choices=list(render.FIT_FILTERS), default="pad")
p.add_argument("--draft", action="store_true", help="allow clips not yet approved in production-status.json")
args = p.parse_args()
project = load_project(Path(args.manifest).resolve().parent)
try:
    result = render.render(project, args.output, fit=args.fit, use_manifest=True, allow_unapproved=args.draft)
except render.RenderError as exc:
    sys.exit(str(exc))
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(0 if result["verified"] else 1)
