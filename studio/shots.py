"""Split a multi-shot generation into storyboard cuts and pick each cut's best 1-second window."""
import subprocess

import numpy as np

from .render import probe

CUT_SCORE = 0.3      # ffmpeg scene score that counts as a hard cut
EDGE_MARGIN = 0.08   # seconds kept away from each cut (blend/transition frames)
MIN_STRETCH_SHOT = 0.75  # shorter shots (>= this) are slowed to fill the cut instead of regenerated


def _frames(path, width=160):
    info = probe(path)["video"]
    num, den = info["r_frame_rate"].split("/")
    fps = float(num) / float(den)
    h = round(info["height"] * width / info["width"] / 2) * 2
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"scale={width}:{h}",
                          "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, width).astype(np.float32), fps


FALLBACK_SCORE = 0.06  # lowest score accepted when a cut between similar-coloured shots is missed


def scene_scores(path):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf",
                          "select='gte(scene,0)',metadata=print:key=lavfi.scene_score:file=-", "-f", "null", "-"],
                         capture_output=True, text=True, check=True).stdout
    return [float(line.split("=")[1]) for line in out.splitlines() if "scene_score" in line]


def detect_cuts(path, expected_shots=None, fps=24.0):
    """Frame indices where a new shot starts. If fewer than expected are found at the normal
    threshold, take the strongest remaining peaks (>= FALLBACK_SCORE, >= 0.5 s apart)."""
    scores = scene_scores(path)
    cuts = [i for i, s in enumerate(scores) if s > CUT_SCORE]
    if expected_shots and len(cuts) < expected_shots - 1:
        gap = round(0.5 * fps)
        for i in sorted(range(len(scores)), key=lambda k: -scores[k]):
            if len(cuts) >= expected_shots - 1 or scores[i] < FALLBACK_SCORE:
                break
            if i > gap and all(abs(i - c) >= gap for c in cuts):
                cuts.append(i)
        cuts.sort()
    return cuts


def split(path, cut_ids, use_seconds=1.0):
    """Map shots to cut ids in order and choose the steadiest window inside each shot."""
    frames, fps = _frames(path)
    n = len(frames)
    starts = [0] + detect_cuts(path, len(cut_ids), fps)
    bounds = list(zip(starts, starts[1:] + [n]))
    result = {"path": str(path), "fps": fps, "shots_found": len(bounds), "shots_expected": len(cut_ids), "cuts": {}}
    if len(bounds) != len(cut_ids):
        result["problem"] = f"found {len(bounds)} shots, expected {len(cut_ids)}"
        return result
    motion = np.concatenate([[0.0], np.abs(np.diff(frames, axis=0)).mean(axis=(1, 2))])
    win = round(use_seconds * fps)
    margin = round(EDGE_MARGIN * fps)
    for cid, (a, b) in zip(cut_ids, bounds):
        lo, hi = a + margin, b - margin - win
        entry = {"shot_seconds": [round(a / fps, 3), round(b / fps, 3)]}
        if hi < lo and b - a >= win:
            # shot only just long enough: use it without the edge margin
            lo, hi = a + max(0, (b - a - win) // 2), a + max(0, (b - a - win) // 2)
            entry["tight"] = True
        if hi < lo and b - a >= round(MIN_STRETCH_SHOT * fps):
            # slightly short shot: use all of it, slowed down to fill the cut (edit only, no new content)
            entry.update(trim_in_seconds=round(a / fps, 3), frames=[a, b - 1], stretch_factor=round(win / (b - a), 4),
                         mean_motion=round(float(motion[a + 1:b].mean()), 3))
            result["cuts"][cid] = entry
            continue
        if hi < lo:
            entry["problem"] = f"shot is {(b - a) / fps:.2f}s, shorter than {MIN_STRETCH_SHOT}s"
        else:
            best = min(range(lo, hi + 1), key=lambda s: motion[s + 1:s + win].mean())
            entry.update(trim_in_seconds=round(best / fps, 3), frames=[best, best + win - 1],
                         mean_motion=round(float(motion[best + 1:best + win].mean()), 3))
        result["cuts"][cid] = entry
    return result
