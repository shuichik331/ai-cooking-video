#!/usr/bin/env python3
"""Concatenate approved scene clips with ffmpeg (assets remain outside git)."""
import argparse, json, subprocess, tempfile
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument("manifest")
p.add_argument("--output",required=True)
args=p.parse_args()
data=json.loads(Path(args.manifest).read_text(encoding="utf-8"))
entries=data["scenes"]
if not entries or any(not v or not Path(v).is_file() for v in entries.values()):
    raise SystemExit("Missing one or more source clips. Set real clip paths in manifest.json.")
output=Path(args.output)
output.parent.mkdir(parents=True,exist_ok=True)
# Normalize codec, size, fps and audio for reliable concatenation.
with tempfile.TemporaryDirectory() as tmp:
    normalized=[]
    for idx,(scene,path) in enumerate(entries.items()):
        dst=str(Path(tmp)/f"{idx:03d}.mp4")
        subprocess.run(["ffmpeg","-y","-i",path,"-vf","scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30","-c:v","libx264","-pix_fmt","yuv420p","-an",dst],check=True)
        normalized.append(dst)
    listfile=Path(tmp)/"concat.txt"
    listfile.write_text("".join("file '"+str(Path(f).resolve()).replace("'","'\\''")+"'\n" for f in normalized))
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(listfile),"-c","copy",str(output)],check=True)
print(output)
