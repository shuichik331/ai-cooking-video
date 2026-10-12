#!/usr/bin/env python3
"""Download a finished group clip, split it into its cuts and build a review sheet.

usage: process_group.py PROJECT GROUP URL [--attempt N]
Writes media/<project>/clips/<group>_aN.mp4, media/<project>/review/<group>_aN.png and
projects/<project>/group-results/<group>_aN.json (shot boundaries, chosen 1 s windows).
"""
import argparse, json, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from PIL import Image, ImageDraw  # noqa: E402
from studio import shots  # noqa: E402
from studio.render import probe  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("project"); ap.add_argument("group"); ap.add_argument("url"); ap.add_argument("--attempt", type=int, default=1)
ap.add_argument("--cuts", nargs="*", help="override cut ids (for single-cut fixes)")
a = ap.parse_args()
root = Path(__file__).resolve().parent.parent
media = root / "media" / a.project
plan = json.loads((root / "projects" / a.project / "production-plan.json").read_text(encoding="utf-8"))
cuts = a.cuts or next(g["cuts"] for g in plan["groups"] if g["group"] == a.group)
tag = f"{a.group}_a{a.attempt}"
clip = media / "clips" / f"{tag}.mp4"
subprocess.run(["curl", "-sS", "-o", str(clip), a.url], check=True)
info = probe(clip)
res = shots.split(clip, cuts)
res.update(group=a.group, attempt=a.attempt, url=a.url, duration=round(info["duration"], 3),
           size=[info["video"]["width"], info["video"]["height"]], audio=bool(info["audio"]))
out = root / "projects" / a.project / "group-results"
out.mkdir(exist_ok=True)
(out / f"{tag}.json").write_text(json.dumps(res, indent=2) + "\n", encoding="utf-8")
# review sheet: for each detected shot, first / middle / last frame; storyboard panel on the left
starts = [0] + shots.detect_cuts(clip)
fps = res["fps"]; n = round(info["duration"] * fps)
bounds = list(zip(starts, starts[1:] + [n]))
rows = []
for k, (s, e) in enumerate(bounds):
    frames = []
    for f in (s + 1, (s + e) // 2, max(s, e - 2)):
        png = media / "review" / f"_tmp_{f}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(clip), "-vf", f"select=eq(n\\,{f})", "-frames:v", "1", str(png)], check=True)
        im = Image.open(png).convert("RGB"); im.thumbnail((160, 284)); frames.append(im); png.unlink()
    cid = cuts[k] if k < len(cuts) else "EXTRA"
    panel = media / "panels" / f"{cid}.png"
    ref = Image.open(panel).convert("RGB") if panel.is_file() else Image.new("RGB", (160, 120), "gray")
    ref.thumbnail((200, 284))
    row = Image.new("RGB", (210 + 3 * 165, 300), "white")
    row.paste(ref, (0, 16)); [row.paste(fr, (210 + i * 165, 16)) for i, fr in enumerate(frames)]
    ImageDraw.Draw(row).text((2, 2), f"{cid}  shot {k + 1}: {s / fps:.2f}-{e / fps:.2f}s", fill=(200, 0, 0))
    rows.append(row)
sheet = Image.new("RGB", (rows[0].width, 300 * len(rows)), "white")
for i, r in enumerate(rows):
    sheet.paste(r, (0, i * 300))
sheet.save(media / "review" / f"{tag}.png")
print(json.dumps({k: v for k, v in res.items() if k != "url"}, indent=1))
