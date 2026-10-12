#!/usr/bin/env python3
"""Record split cuts of a group attempt into production-status.json after visual review.

usage: record_cuts.py PROJECT GROUP_ATTEMPT_TAG JOB_ID [--reject CUT:reason ...] [--note CUT:text ...]
Accepted cuts become status 'generated' with asset_path = group clip and trim_in_seconds.
Rejected or unsplittable cuts are recorded as 'rejected' with the reason (kept for retry).
"""
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from studio import status  # noqa: E402
from studio.project import load_project, write_json  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("project"); ap.add_argument("tag"); ap.add_argument("job_id")
ap.add_argument("--reject", nargs="*", default=[]); ap.add_argument("--note", nargs="*", default=[])
a = ap.parse_args()
root = Path(__file__).resolve().parent.parent
p = load_project(root / "projects" / a.project)
res = json.loads((p.root / "group-results" / f"{a.tag}.json").read_text(encoding="utf-8"))
rejects = dict(r.split(":", 1) for r in a.reject)
notes = dict(n.split(":", 1) for n in a.note)
clip = str((root / res["path"]).resolve().relative_to(root)) if not Path(res["path"]).is_absolute() else str(Path(res["path"]).relative_to(root))
for cid, c in res["cuts"].items():
    e = p.status["scenes"][cid]
    e.setdefault("jobs", []).append({"job_id": a.job_id, "group_attempt": a.tag, "shot_seconds": c.get("shot_seconds")})
    reason = rejects.get(cid) or c.get("problem")
    if reason:
        status.set_scene(p, cid, "rejected", note=f"{a.tag}: {reason}")
        print(cid, "REJECTED", reason)
        continue
    status.set_scene(p, cid, "generated", asset_path=clip, note=f"{a.tag}: {notes.get(cid, 'visual check passed')}")
    e["trim_in_seconds"] = c["trim_in_seconds"]
    e["selected_cut"] = {"source": clip, "frames": c["frames"], "tight": bool(c.get("tight")), "mean_motion": c["mean_motion"]}
    print(cid, "ok trim", c["trim_in_seconds"])
write_json(p.status_path, p.status)
