# Production pipeline

ChatGPT authors the creative files. Claude Code validates them, tracks status and assembles footage with the tools below. None of these commands calls a paid API.

## Project files (`projects/<project-id>/`)

| File | Owner | Purpose |
|---|---|---|
| `storyboard.json` | ChatGPT | Single source of truth for scene order and timing (`id`, `start_seconds`, `end_seconds`, `shot`, optional `duration_seconds`, `page`, `frame_number`, legacy `prompt`). |
| `prompts.json` | ChatGPT | Per-scene `higgsfield_prompt`, `camera`, `motion`, `continuity`, `reference_page`, `reference_panel`; optional `global_prompt`. |
| `pages.json` | ChatGPT | Storyboard image pages → scene ids; `known_reference_issues` for image/JSON conflicts. |
| `storyboard-pages/*.png` | ChatGPT | Storyboard images: the primary visual reference for framing, subject and flow. |
| `production-status.json` | Claude Code | Verified status only: overall status, per-scene status/asset/approval/jobs, validation, discrepancies, render result, publication. |
| `generation-sheet.json` / `.md` | derived | Verbatim per-scene generation sheet. Regenerate; never edit by hand. |
| `generation-approval.json` | human | Spend approval: `approved_by`, `approved_at`, `max_credits`, `resolution`, `scene_ids`. |
| `generation-queue.json` | derived | Requests approved for submission, with the exact MCP parameters. |

Older projects (karaage-001) keep `prompt` inside `storyboard.json` and have no `prompts.json` / `pages.json`. They still validate, but are blocked until storyboard images exist.

## Validation severities

- **error**: the files contradict each other or the contract. Production stops and ChatGPT revises the files.
- **blocker**: the files are consistent but something is missing, such as images not uploaded, the image cross-check not done, or an unresolved `known_reference_issues` entry.
- **warning**: recorded for review. A reference conflict whose decision is recorded in `production-status.json → discrepancies` becomes a warning, so the original conflict stays visible.

## Statuses

Overall flow: `not_started → ready_for_generation → generating → in_review → ready_for_render → rendered → approved_for_publish → published`. Rollbacks to earlier review stages are allowed.

| Transition to | Requires |
|---|---|
| `ready_for_generation` | No errors or blockers. All storyboard images are present, and `image_verification.status` is `verified`. |
| `ready_for_render` | Every scene is `approved`, and its asset file exists. |
| `rendered` | A verified render is recorded (`render --record`). |
| `approved_for_publish` | `publication.approved` is true. This is human signoff. |
| `published` | A real platform URL is recorded. |

Scene statuses: `pending → generating → generated → provisional → approved | rejected`. `provisional` means production review passed and the user accepted the clip tentatively; it is not approved and is never rendered as final. `generated` and `approved` require an existing, probed clip.

## Commands

```bash
python3 scripts/studio.py list                      # projects in not_started / ready_for_generation
python3 scripts/studio.py validate --record         # all projects; records result in production-status.json
python3 scripts/studio.py sheet chicken-nanban-001  # generation-sheet.json / .md
python3 scripts/studio.py discrepancy P s26 --source pages.json --issue ... --resolution ... --decided-by ...
python3 scripts/studio.py status P --set ready_for_generation
python3 scripts/studio.py plan P --resolution 480p --scenes s01 s02   # queue only if approval covers it
python3 scripts/studio.py register-clip P s01 media/P/s01.mp4         # clip is probed, not approved
python3 scripts/studio.py scene P s01 approved                         # after human review
python3 scripts/studio.py render P --output output/P.mp4 --record      # approved clips only
python3 scripts/studio.py verify output/P.mp4 --project P --audio yes
python3 -m unittest discover -s tests
```

Clip paths are absolute or relative to the repo root. Keep media in `media/` or `output/`; both are gitignored.

## Rendering

- Clips are used in storyboard order. Each is trimmed to its scene duration: start of the clip by default, or `--trim-anchor center`, or `trim_in_seconds` per scene in the status file.
- Video is cut to an exact frame count per scene, scaled to 1080×1920 (`--fit pad` letterbox or `--fit crop`), at 30 fps, H.264, yuv420p.
- Audio is kept when a clip has it, and silence is inserted when it doesn't. It is concatenated as PCM and encoded to AAC once, so cut points stay in sync. Use `--no-audio` for a silent master.
- The output is probed with ffprobe and checked for size, fps, codecs, pixel format, audio presence and duration (±0.15 s) before success is reported.
