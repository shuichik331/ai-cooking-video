"""Full-video production plan: grouping, references, draft generation prompts, cost.

Nothing here edits prompts.json. Draft generation prompts are built from the original
per-cut text (kept verbatim) plus the global_prompt sentences except the whole-recipe
sentence, wrapped in the multi-shot contract. They are written as a diff for ChatGPT to
confirm before any submission.
"""
import math
import re

from .project import REPO_ROOT, load_json

GROUPS_FILE = "production-groups.json"
RECIPE_SENTENCE = re.compile(r"cooked from raw chicken thigh through", re.I)
FACE_REF = {"file": "media/{pid}/panels/s03_face@4x.png", "media_id": "0e722b28-105b-483a-bc45-1024d3c90329"}
KITCHEN_REF = {"file": "media/{pid}/review/s01_accepted_frame.png",
               "note": "frame from the provisionally accepted s01 clip (test-02), environment reference"}
# generation length per group size: ~1.5 s per shot, because Seedance splits shots unevenly
# (s01 test-01 produced a 0.33 s shot); model minimum is 4 s.
SECONDS = {1: 4, 2: 4, 3: 5, 4: 6}


def _sentences(text):
    return [s.strip() for s in re.split(r"(?<=\.)\s+", text or "") if s.strip()]


def scene_text(entry, global_prompt):
    """The cut-specific part of an original prompt (verbatim)."""
    prompt = entry.get("higgsfield_prompt") or ""
    if global_prompt and prompt.endswith(global_prompt):
        return prompt[: -len(global_prompt)].strip()
    return prompt


def build_prompt(cuts, texts, durations, face, wide_env, global_prompt):
    n, total = len(cuts), sum(durations)
    kept = [s for s in _sentences(global_prompt) if not RECIPE_SENTENCE.search(s)]
    lines = [f"MULTI-SHOT SEQUENCE: exactly {n} shots in {total} seconds, hard cut between shots, no other shots."
             if n > 1 else f"SINGLE CONTINUOUS SHOT, {total} seconds, NO CUTS."]
    if n > 1:
        lines.append("Shot 1 starts from the supplied start frame; each later shot matches the next reference panel in order. "
                     "Each shot is one continuous take showing only its own action.")
    t = 0.0
    for i, (cid, txt, d) in enumerate(zip(cuts, texts, durations), 1):
        lines.append(f"Shot {i} ({t:.2f}-{t + d:.2f}s, storyboard {cid}): {txt}" if n > 1 else txt)
        t += d
    lines += kept
    if face:
        lines.append("Keep the young man's face and hairstyle consistent with the separate face-and-shoulders "
                     "identity reference; do not copy that image's tray or hands.")
    if wide_env:
        lines.append("Keep the room identical to the separate kitchen environment reference.")
    lines.append("Natural cooking sounds only, no music, no speech.")
    lines.append("Absolutely no cooking stages other than the shots listed, no extra shots, inserts, temporal jumps, "
                 "extra people, overlay text, logos or watermarks.")
    return " ".join(lines), kept


def apply_override(cid, text, overrides):
    rule = overrides.get(cid)
    if not rule:
        return text
    if "replace" in rule:
        old, new = rule["replace"]
        if old not in text:
            raise ValueError(f"{cid}: override text not found in the original prompt: {old!r}")
        text = text.replace(old, new)
    if "append" in rule:
        text = f"{text} {rule['append']}"
    return text


def build_plan(project, config, sheet):
    pid = project.id
    groups_spec = load_json(project.root / GROUPS_FILE)
    ov_path = project.root / "generation-overrides.json"
    overrides = load_json(ov_path)["cut_text"] if ov_path.is_file() else {}
    gp = project.prompts.get("global_prompt", "")
    entries = {e["id"]: e for e in project.prompts["scenes"]}
    face = set(groups_spec["face_visible"])
    wide_env = set(groups_spec["environment_shots"])
    blocked = {d["scene"]: d["issue"] for d in project.status.get("discrepancies", []) if not d.get("resolution")}
    rate = config["observed_credits_per_second"]["480p"]
    groups = []
    for g in groups_spec["groups"]:
        cuts = g["cuts"]
        seconds = SECONDS[len(cuts)]
        per = round(seconds / len(cuts), 2)
        durations = [per] * len(cuts)
        durations[-1] = round(seconds - per * (len(cuts) - 1), 2)
        originals = [scene_text(entries[c], gp) for c in cuts]
        texts = [apply_override(c, t, overrides) for c, t in zip(cuts, originals)]
        has_face = any(c in face for c in cuts)
        has_env = any(c in wide_env for c in cuts)
        prompt, kept = build_prompt(cuts, texts, durations, has_face, has_env, gp)
        refs = [{"role": "start_image", "file": f"media/{pid}/panels/{cuts[0]}_start_9x16.png", "for": cuts[0]}]
        refs += [{"role": "image_references", "file": f"media/{pid}/panels/{c}@4x.png", "for": c} for c in cuts[1:]]
        if has_face:
            refs.append({"role": "image_references", "file": FACE_REF["file"].format(pid=pid), "for": "identity",
                         "media_id": FACE_REF["media_id"]})
        if has_env:
            refs.append({"role": "image_references", "file": KITCHEN_REF["file"].format(pid=pid), "for": "environment"})
        groups.append({
            "group": g["id"], "stage": g["stage"], "cuts": cuts, "shot_seconds": durations,
            "generate_seconds": seconds, "estimated_credits": rate * seconds,
            "blocked_by": {c: blocked[c] for c in cuts if c in blocked},
            "references": refs,
            "draft_prompt": prompt,
            "prompt_diff": {
                "kept_verbatim_per_cut": dict(zip(cuts, originals)),
                "creative_overrides": {c: t for c, o, t in zip(cuts, originals, texts) if t != o},
                "kept_verbatim_from_global_prompt": kept,
                "removed": [s for s in _sentences(gp) if RECIPE_SENTENCE.search(s)],
                "added": "multi-shot / single-shot contract, shot timing labels, identity / environment lines, audio line, exclusions",
            },
        })
    base = sum(g["estimated_credits"] for g in groups)
    return {"project_id": pid, "groups": groups, "generations": len(groups),
            "generate_seconds": sum(g["generate_seconds"] for g in groups),
            "base_credits": base, "cuts": sum(len(g["cuts"]) for g in groups)}
