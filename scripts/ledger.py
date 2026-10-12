#!/usr/bin/env python3
"""Append a Higgsfield job to the chicken-nanban production ledger and enforce the approved cap.

usage: ledger.py PROJECT GROUP JOB_ID CREDITS [--note TEXT]   (records a submitted job)
       ledger.py PROJECT --check NEXT_CREDITS                   (exit 1 if the cap would be exceeded)
"""
import argparse, json, sys
from datetime import datetime, timezone
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("project"); ap.add_argument("group", nargs="?"); ap.add_argument("job_id", nargs="?")
ap.add_argument("credits", nargs="?", type=float); ap.add_argument("--note", default="")
ap.add_argument("--check", type=float)
a = ap.parse_args()
path = Path(__file__).resolve().parent.parent / "projects" / a.project / "production-plan.json"
plan = json.loads(path.read_text(encoding="utf-8"))
cap = plan["approval"]["hard_cap_credits"]
spent = sum(e["credits"] for e in plan["ledger"])
if a.check is not None:
    ok = spent + a.check <= cap
    print(f"spent {spent} + next {a.check} = {spent + a.check} / cap {cap}: {'OK' if ok else 'EXCEEDS CAP'}")
    sys.exit(0 if ok else 1)
plan["ledger"].append({"group": a.group, "job_id": a.job_id, "credits": a.credits, "note": a.note,
                       "submitted_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat()})
path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"recorded {a.group} {a.job_id} {a.credits}; total spent {spent + a.credits} / {cap}")
