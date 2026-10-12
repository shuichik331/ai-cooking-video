#!/usr/bin/env python3
"""Import storyboard pages from local ZIP or HTTPS ZIP into a project.

Never run this with an untrusted ZIP or source URL. This command does not upload
anything on its own: GitHub Actions may commit the resulting files, or Claude
Code can commit them after approval.
"""
import argparse
import hashlib
import io
import json
import urllib.request
import zipfile
from pathlib import Path
from urllib.parse import urlparse

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project",required=True)
    source=ap.add_mutually_exclusive_group(required=True)
    source.add_argument("--zip",dest="zip_path")
    source.add_argument("--url")
    args=ap.parse_args()
    root=Path("projects")/args.project
    if not root.is_dir() or not (root/"pages.json").is_file():
        ap.error("Existing project with pages.json required")
    mapping=json.loads((root/"pages.json").read_text(encoding="utf-8"))
    expected=[x["file"] for x in mapping["pages"]]
    if any(not x.startswith("storyboard-pages/") or Path(x).name not in {f"page-{i:02d}.png" for i in range(1,100)} for x in expected):
        ap.error("Unsafe or unexpected page filenames")
    if args.url:
        parsed=urlparse(args.url)
        if parsed.scheme!="https" or not parsed.netloc:
            ap.error("Only absolute HTTPS URLs are allowed")
        request=urllib.request.Request(args.url,headers={"User-Agent":"ai-cooking-video-importer/1.0"})
        with urllib.request.urlopen(request,timeout=35) as response:
            payload=response.read(40*1024*1024+1)
        if len(payload)>40*1024*1024: ap.error("ZIP exceeds 40 MB")
    else:
        payload=Path(args.zip_path).read_bytes()
    out=root/"storyboard-pages"
    out.mkdir(exist_ok=True)
    digests={}
    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        files=[f for f in zf.infolist() if not f.is_dir()]
        if len(files)!=len(expected): ap.error(f"Expected {len(expected)} files; found {len(files)}")
        seen=set()
        for item in files:
            name=Path(item.filename).name
            matches=[x for x in expected if Path(x).name==name]
            if len(matches)!=1 or name in seen or item.file_size>12*1024*1024:
                ap.error(f"Invalid or duplicate ZIP member: {item.filename}")
            # Zip entries may carry parent dir, but not traversal or absolute names.
            member=Path(item.filename)
            if member.is_absolute() or ".." in member.parts: ap.error("Unsafe ZIP member")
            b=zf.read(item)
            if not b.startswith(b"\\x89PNG\\r\\n\\x1a\\n".decode("unicode_escape").encode("latin1")):
                ap.error(f"Not a PNG: {name}")
            (out/name).write_bytes(b)
            digests[name]=hashlib.sha256(b).hexdigest()
            seen.add(name)
    print(json.dumps({"project":args.project,"uploaded_to_repository":False,"pages":digests},indent=2))
if __name__=="__main__":
    main()
