"""Seedance generation sheet: a per-scene, verbatim view of the approved creative files.

Nothing here is authored by Claude Code: every creative field is copied unchanged from
storyboard.json / prompts.json / pages.json. Fields the creative files do not provide are
left null and listed as "unspecified" rather than filled in.
"""
from .project import REPO_ROOT, load_json

GENERATION_CONFIG = REPO_ROOT / "config" / "generation.json"


def load_generation_config(path=GENERATION_CONFIG):
    return load_json(path)


def _scene_description(prompt, global_prompt):
    """Scene-specific part of a prompt that ends with the shared global prompt (verbatim slice)."""
    if prompt and global_prompt and prompt.endswith(global_prompt):
        return prompt[: -len(global_prompt)].strip()
    return prompt


def build_sheet(project, report=None, config=None):
    config = config or load_generation_config()
    constraints = config["model_constraints"]
    global_prompt = (project.prompts or {}).get("global_prompt")
    page_files = {}
    for page in (project.pages or {}).get("pages", []):
        for sid in page.get("scene_ids", []):
            page_files[sid] = page.get("file")
    discrepancies = {}
    for issue in (project.pages or {}).get("known_reference_issues", []):
        discrepancies.setdefault(issue.get("scene"), []).append({"source": "pages.json", "issue": issue.get("issue")})
    for d in project.status.get("discrepancies", []):
        discrepancies.setdefault(d.get("scene"), []).append(d)

    scenes = []
    for scene in project.scenes:
        sid = scene["id"]
        entry = project.prompt_for(sid) or {}
        prompt = entry.get("higgsfield_prompt")
        duration = scene["end_seconds"] - scene["start_seconds"]
        ref_file = entry.get("reference_page") or page_files.get(sid)
        unspecified = [f for f in ("camera", "motion", "continuity") if not entry.get(f)]
        scenes.append({
            "scene_id": sid,
            "start_seconds": scene["start_seconds"],
            "end_seconds": scene["end_seconds"],
            "duration_seconds": duration,
            "shot": scene.get("shot"),
            "visual_description": _scene_description(prompt, global_prompt),
            "camera": entry.get("camera"),
            "motion": entry.get("motion"),
            "continuity": entry.get("continuity"),
            "unspecified": unspecified,
            "higgsfield_prompt": prompt,
            "reference": {
                "page_file": ref_file,
                "panel": entry.get("reference_panel") or (sid if ref_file else None),
                "image_in_repo": bool(ref_file) and (project.root / ref_file).is_file(),
            },
            "generation": {
                "model": config["model"],
                "aspect_ratio": project.storyboard.get("aspect_ratio"),
                # Seedance cannot render shorter than its minimum; the clip is trimmed in the edit.
                "generate_seconds": max(duration, constraints["min_duration_seconds"]),
                "use_seconds": duration,
            },
            "discrepancies": discrepancies.get(sid, []),
        })
    return {
        "project_id": project.id,
        "title": project.storyboard.get("title"),
        "derived_from": [n for n in ("storyboard.json", "prompts.json", "pages.json", "production-status.json")
                         if (project.root / n).is_file()],
        "note": "Derived file. Do not edit; regenerate with `python3 scripts/studio.py sheet <project>`.",
        "style": project.storyboard.get("style"),
        "global_prompt": global_prompt,
        "validation": report.summary() if report else None,
        "scene_count": len(scenes),
        "total_generate_seconds": sum(s["generation"]["generate_seconds"] for s in scenes),
        "scenes": scenes,
    }


def estimate_credits(sheet, config=None):
    """Local estimate per resolution from observed prices; confirm with a live quote before spending."""
    config = config or load_generation_config()
    rates = {k: v for k, v in config["observed_credits_per_second"].items() if not k.startswith("_")}
    seconds = sheet["total_generate_seconds"]
    return {res: rate * seconds for res, rate in rates.items()}


def _cell(value):
    return (value or "—").replace("|", "\\|").replace("\n", " ")


def render_markdown(sheet, config=None):
    costs = estimate_credits(sheet, config)
    lines = [
        f"# Generation sheet — {sheet['project_id']}",
        "",
        f"**{sheet['title']}** · {sheet['scene_count']} scenes · {sheet['note']}",
        "",
        f"- Validation: {sheet['validation']}",
        f"- Model: `{sheet['scenes'][0]['generation']['model']}` · total generated seconds: "
        f"{sheet['total_generate_seconds']} (each scene rendered at least the model minimum, then trimmed)",
        "- Estimated credits (observed prices, re-quote before spending): "
        + ", ".join(f"{res}: {credits}" for res, credits in costs.items()),
        "",
    ]
    if sheet.get("global_prompt"):
        lines += ["## Global prompt (appended to every scene prompt)", "", f"> {sheet['global_prompt']}", ""]
    lines += [
        "## Scenes",
        "",
        "| id | time | use/gen s | shot | visual description | camera | motion | ref | notes |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for s in sheet["scenes"]:
        ref = s["reference"]
        ref_txt = f"{ref['page_file'].rsplit('/', 1)[-1]}#{ref['panel']}" if ref["page_file"] else "—"
        if ref["page_file"] and not ref["image_in_repo"]:
            ref_txt += " (missing)"
        notes = []
        if s["unspecified"]:
            notes.append("unspecified: " + ", ".join(s["unspecified"]))
        for d in s["discrepancies"]:
            notes.append(f"⚠ {d.get('issue')}" + (f" → {d['resolution']}" if d.get("resolution") else ""))
        lines.append(
            f"| {s['scene_id']} | {s['start_seconds']}–{s['end_seconds']}s | "
            f"{s['duration_seconds']}/{s['generation']['generate_seconds']} | {_cell(s['shot'])} | "
            f"{_cell(s['visual_description'])} | {_cell(s['camera'])} | {_cell(s['motion'])} | {ref_txt} | "
            f"{_cell('; '.join(notes))} |"
        )
    continuity = {s["continuity"] for s in sheet["scenes"] if s["continuity"]}
    if continuity:
        lines += ["", "## Continuity notes", ""] + [f"- {c}" for c in sorted(continuity)]
    lines += ["", "Full verbatim `higgsfield_prompt` per scene: see `generation-sheet.json`.", ""]
    return "\n".join(lines)
