#!/usr/bin/env python3
"""Download project storyboard PNGs from private Drive using an OAuth bearer token.

Requires GOOGLE_DRIVE_ACCESS_TOKEN, with Drive read permission, on the machine
running Claude Code. Do not expose that token to the repository or logs.
"""
import argparse, hashlib, json, os, sys, urllib.request
from pathlib import Path

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--project",required=True)
    args=parser.parse_args()
    token=os.environ.get("GOOGLE_DRIVE_ACCESS_TOKEN")
    if not token:
        sys.exit("Missing GOOGLE_DRIVE_ACCESS_TOKEN (OAuth token with Drive read access). No files downloaded.")
    repo=Path(__file__).resolve().parent.parent
    mapping=json.loads((repo/"config/google-drive-assets.json").read_text(encoding="utf8"))
    item=mapping.get("projects",{}).get(args.project)
    if not item:
        sys.exit("Unknown project: "+args.project)
    project_dir=repo/"projects"/args.project
    pages=json.loads((project_dir/"pages.json").read_text(encoding="utf8"))
    allowed={Path(x["file"]).name for x in pages["pages"]}
    output=project_dir/"storyboard-pages"
    output.mkdir(exist_ok=True)
    uploaded=item.get("files",[])
    if set(x["name"] for x in uploaded)!=allowed:
        sys.exit("Drive file list does not match pages.json")
    for item in uploaded:
        name=item["name"]
        if not name.startswith("page-") or not name.endswith(".png"):
            sys.exit("Invalid image name")
        file_id=item["file_id"]
        if "/" in file_id or "?" in file_id:
            sys.exit("Invalid Drive file ID")
        url=f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
        request=urllib.request.Request(url,headers={"Authorization":"Bearer "+token})
        with urllib.request.urlopen(request,timeout=45) as response:
            data=response.read(12*1024*1024+1)
        if len(data)>12*1024*1024 or not data.startswith(bytes([137,80,78,71,13,10,26,10])):
            sys.exit("Invalid or oversized PNG: "+name)
        (output/name).write_bytes(data)
        print(name, len(data), hashlib.sha256(data).hexdigest()[:16])
    print(f"Downloaded {len(uploaded)} images; review visual consistency before changing project status.")

if __name__=="__main__":
    main()
