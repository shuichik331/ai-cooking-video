#!/usr/bin/env python3
"""Single-cut retake request (4 s, one continuous shot) built from the original cut text.

usage: retake_request.py PROJECT CUT START_MEDIA_ID [--face] [--no-person]
Keeps the cut text verbatim (plus creative overrides) and the global style/kitchen sentences;
with --no-person the protagonist sentence is left out and 'no person in frame' is added,
because the storyboard panel shows no person (logged in generation-overrides.json).
"""
import argparse, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from studio.production_plan import RECIPE_SENTENCE, _sentences, apply_override, scene_text  # noqa: E402
from studio.project import load_json  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("project"); ap.add_argument("cut"); ap.add_argument("start_media")
ap.add_argument("--face", action="store_true"); ap.add_argument("--no-person", action="store_true")
a = ap.parse_args()
root = Path(__file__).resolve().parent.parent / "projects" / a.project
pr = load_json(root / "prompts.json"); gp = pr["global_prompt"]
entry = next(e for e in pr["scenes"] if e["id"] == a.cut)
ov = load_json(root / "generation-overrides.json")["cut_text"]
text = apply_override(a.cut, scene_text(entry, gp), ov)
kept = [s for s in _sentences(gp) if not RECIPE_SENTENCE.search(s)]
if a.no_person:
    kept = [s for s in kept if "young Japanese man" not in s]
    kept.insert(1, "The same cozy compact apartment kitchen with wooden countertops, warm daylight and consistent utensils.")
parts = ["SINGLE CONTINUOUS SHOT, 4 seconds, NO CUTS.",
         "Use the supplied storyboard panel as the start frame and keep its framing for the whole shot.", text] + kept
if a.no_person:
    parts.append("No person in frame; show only what the storyboard panel shows.")
if a.face:
    parts.append("Keep the young man's face and hairstyle consistent with the separate face-and-shoulders identity reference; do not copy that image's tray or hands.")
parts += ["Natural cooking sounds only, no music, no speech.",
          "Absolutely no other cooking stages, scene transitions, montage, inserts, temporal jumps, extra people, overlay text, logos or watermarks."]
medias = [{"role": "start_image", "value": a.start_media}]
if a.face:
    medias.append({"role": "image_references", "value": "0e722b28-105b-483a-bc45-1024d3c90329"})
print(json.dumps({"model": "seedance_2_5", "mode": "omni_reference", "prompt": " ".join(parts), "duration": 4, "resolution": "480p",
                  "aspect_ratio": "9:16", "generate_audio": True, "count": 1, "medias": medias}, ensure_ascii=False))
