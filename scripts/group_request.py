#!/usr/bin/env python3
"""Print the exact generate_video params for a plan group (all reference media must be uploaded)."""
import json, sys
from pathlib import Path
plan = json.loads((Path(__file__).resolve().parent.parent / "projects" / sys.argv[1] / "production-plan.json").read_text())
g = next(x for x in plan["groups"] if x["group"] == sys.argv[2])
missing = [r["for"] for r in g["references"] if "media_id" not in r]
if missing:
    sys.exit(f"missing media ids: {missing}")
print(json.dumps({"model": "seedance_2_5", "mode": "omni_reference", "prompt": g["draft_prompt"], "duration": g["generate_seconds"],
                  "resolution": "480p", "aspect_ratio": "9:16", "generate_audio": True, "count": 1,
                  "medias": [{"role": r["role"], "value": r["media_id"]} for r in g["references"]]}, ensure_ascii=False))
