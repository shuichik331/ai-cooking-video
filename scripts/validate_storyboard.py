#!/usr/bin/env python3
import json, sys
from pathlib import Path

def validate(path):
    data=json.loads(Path(path).read_text(encoding="utf-8"))
    assert data["aspect_ratio"]=="9:16", "expected 9:16"
    scenes=data["scenes"]
    assert scenes, "no scenes"
    cursor=0
    seen=set()
    for scene in scenes:
        for field in ("id","shot","prompt","start_seconds","end_seconds"):
            assert field in scene and scene[field] is not None, f"missing {field}"
        assert scene["id"] not in seen, "duplicate scene id"
        seen.add(scene["id"])
        assert scene["start_seconds"]==cursor, f"timeline gap/overlap at {scene['id']}"
        assert scene["end_seconds"]>cursor, "invalid time interval"
        cursor=scene["end_seconds"]
    assert cursor==data["duration_seconds"], "duration mismatch"
    print(f"VALID: {data['project_id']} | {len(scenes)} scenes | {cursor}s")

if __name__=="__main__":
    validate(sys.argv[1] if len(sys.argv)>1 else "projects/karaage-001/storyboard.json")
