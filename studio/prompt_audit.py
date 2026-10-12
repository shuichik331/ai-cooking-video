"""Read-only audit of prompts.json against the s01 success pattern.

It never edits prompts; it lists what the creative lead (ChatGPT) should revise so a
1-second cut does not turn into a whole-recipe montage. Rules come from the s01 tests:
test-01 (old prompt + global recipe sentence) produced a 4-shot montage, test-02 (revised
single-shot prompt + 9:16 start image + identity reference) held one composition.
"""
import re

SINGLE_SHOT = re.compile(r"single continuous|no cuts?\b|one continuous", re.I)
DURATION = re.compile(r"\b\d+\s*(?:-|\s)?seconds?\b", re.I)
EXCLUSION = re.compile(r"\b(no|absolutely no|do not)\b[^.]*\b(montage|transitions?|cuts?|inserts?)\b", re.I)
GENERIC_CAMERA = {
    "match exact framing of storyboard panel",
    "close-up or macro matching panel",
    "wide or establishing, as storyboard",
}
RECIPE_SENTENCE = re.compile(r"cooked from raw chicken thigh through", re.I)

# From the visual review of the five pages (storyboard-crosscheck.md).
FACE_VISIBLE = {"s03", "s08", "s15", "s22", "s29", "s37", "s41", "s47", "s55", "s56",
                "s59", "s61", "s62", "s65", "s66", "s69"}
WIDE_PANELS = {"s13", "s14", "s27", "s28", "s41", "s42", "s55", "s56", "s69", "s70"}

SEVERITY = {"high": 0, "medium": 1, "low": 2}


def audit(project):
    gp = (project.prompts or {}).get("global_prompt") or ""
    discrepancies = {d["scene"]: d for d in project.status.get("discrepancies", [])}
    motion_count = {}
    for e in (project.prompts or {}).get("scenes", []):
        motion_count[e.get("motion")] = motion_count.get(e.get("motion"), 0) + 1
    rows = []
    for entry in (project.prompts or {}).get("scenes", []):
        sid, prompt = entry["id"], entry.get("higgsfield_prompt") or ""
        findings = []

        def add(sev, code, text):
            findings.append({"severity": sev, "code": code, "text": text})

        if RECIPE_SENTENCE.search(prompt):
            add("high", "recipe-sentence", "contains the whole-recipe sentence from global_prompt (caused the 4-shot montage in s01 test-01)")
        elif gp and prompt.endswith(gp):
            add("high", "global-appended", "global_prompt appended verbatim")
        if not SINGLE_SHOT.search(prompt):
            add("high", "no-single-shot", "no 'single continuous shot / no cuts' instruction")
        if not EXCLUSION.search(prompt):
            add("medium", "no-exclusions", "no explicit exclusion of other recipe stages, montage, transitions or inserts")
        if not DURATION.search(prompt):
            add("medium", "no-duration", "generation length not stated (s01 pattern: '5 seconds')")
        if (entry.get("camera") or "").strip() in GENERIC_CAMERA:
            add("medium", "generic-camera", f"camera field is generic: '{entry.get('camera')}'")
        if motion_count.get(entry.get("motion"), 0) > 1:
            add("medium", "generic-motion", f"motion field is shared word-for-word with {motion_count[entry.get('motion')] - 1} other cut(s)")
        if "test_generation" not in entry:
            add("medium", "no-reference-roles", "no test_generation block (start_image / identity reference roles not defined)")
        if sid in FACE_VISIBLE:
            add("low", "face-visible", "protagonist's face is visible in the panel: needs the identity reference (s03_face)")
        if sid in WIDE_PANELS:
            add("low", "wide-panel", "wide bottom-row panel (~2:1): a 9:16 start image keeps under half the width; confirm which part to keep")
        if sid in discrepancies and not discrepancies[sid].get("resolution"):
            add("high", "open-discrepancy", discrepancies[sid]["issue"])
        elif sid in discrepancies:
            add("low", "recorded-discrepancy", discrepancies[sid]["resolution"])
        findings.sort(key=lambda f: SEVERITY[f["severity"]])
        rows.append({"scene_id": sid, "findings": findings})
    return rows


def summary(rows):
    counts = {}
    for r in rows:
        for f in r["findings"]:
            counts[f["code"]] = counts.get(f["code"], 0) + 1
    return counts


def render_markdown(project, rows, exclude=()):
    shots = {s["id"]: s["shot"] for s in project.scenes}
    target = [r for r in rows if r["scene_id"] not in exclude]
    counts = summary(target)
    lines = [
        f"# Prompt audit — {project.id}",
        "",
        "Read-only check of `prompts.json` against the s01 success pattern (`docs/seedance-scene-template.md`). "
        "Claude Code has not edited any prompt; ChatGPT does the final edit.",
        "",
        f"Scenes audited: {len(target)} (excluded: {', '.join(exclude) or 'none'})",
        "",
        "| finding | scenes | severity |",
        "|---|---|---|",
    ]
    sev = {f["code"]: f["severity"] for r in target for f in r["findings"]}
    for code, n in sorted(counts.items(), key=lambda kv: (SEVERITY[sev[kv[0]]], -kv[1])):
        lines.append(f"| `{code}` | {n} | {sev[code]} |")
    lines += ["", "## Per scene", "", "| id | shot | high | medium/low |", "|---|---|---|---|"]
    for r in target:
        high = "; ".join(f["code"] if f["code"] != "open-discrepancy" else "open-discrepancy: " + f["text"]
                         for f in r["findings"] if f["severity"] == "high")
        rest = ", ".join(f["code"] for f in r["findings"] if f["severity"] != "high")
        lines.append(f"| {r['scene_id']} | {shots.get(r['scene_id'], '')} | {high.replace('|', '/')} | {rest} |")
    lines.append("")
    return "\n".join(lines)
