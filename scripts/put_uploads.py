#!/usr/bin/env python3
"""PUT files to Higgsfield presigned URLs saved from a media_upload result, in order.

usage: put_uploads.py RESULT_JSON PROJECT CUT[=FILE] ...
Each CUT maps to the next upload entry; FILE defaults to the plan's reference file for that cut.
Prints media ids and records them on the plan's references.
"""
import json, subprocess, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
result = json.loads(Path(sys.argv[1]).read_text())
uploads = result["uploads"]
project = sys.argv[2]
plan_path = root / "projects" / project / "production-plan.json"
plan = json.loads(plan_path.read_text(encoding="utf-8"))
refs = {r["for"]: r for g in plan["groups"] for r in g["references"] if r["for"].startswith("s")}
specs = sys.argv[3:]
if specs and specs[0].startswith("--only="):
    # retry a subset: --only=INDEX,...  (indices into the saved upload list)
    idx = [int(i) for i in specs.pop(0).split("=", 1)[1].split(",")]
    uploads = [uploads[i] for i in idx]
assert len(specs) == len(uploads), f"{len(specs)} files for {len(uploads)} upload slots"
ok = []
for spec, up in zip(specs, uploads):
    cut, _, f = spec.partition("=")
    path = root / (f or refs[cut]["file"])
    for attempt in range(3):  # transient 5xx from the upload edge: retry the same URL
        code = subprocess.run(["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}", "-X", "PUT", "-H", "Content-Type: image/png",
                               "-H", "If-None-Match: *", "--data-binary", f"@{path}", up["upload_url"]],
                              capture_output=True, text=True).stdout
        if not code.startswith("5"):
            break
    print(cut, path.name, code, up["media_id"])
    if code == "200":
        if cut in refs and not f:
            refs[cut]["media_id"] = up["media_id"]
        ok.append(up["media_id"])
plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("CONFIRM", json.dumps(ok))
