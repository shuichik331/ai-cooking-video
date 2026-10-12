#!/usr/bin/env python3
"""Re-run the splitter on an already downloaded group attempt (keeps download metadata)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from studio import shots  # noqa: E402
root = Path(__file__).resolve().parent.parent
project, tag = sys.argv[1], sys.argv[2]
p = root / "projects" / project / "group-results" / f"{tag}.json"
old = json.loads(p.read_text())
cuts = sys.argv[3:] or list(old["cuts"])
r = shots.split(root / "media" / project / "clips" / f"{tag}.mp4", cuts)
r.update({k: old[k] for k in ("group", "attempt", "url", "duration", "size", "audio") if k in old})
r["path"] = f"media/{project}/clips/{tag}.mp4"
p.write_text(json.dumps(r, indent=2) + "\n")
print(tag, r["shots_found"], {k: (v.get("trim_in_seconds"), v.get("stretch_factor"), v.get("problem")) for k, v in r["cuts"].items()})
