# Higgsfield integration design

## Principles
- No paid call happens without a human approval file that names the scenes, the resolution and a credit ceiling.
- One scene at a time. Each submission is re-quoted (`get_cost`) first, and Claude Code stops if the quote differs from the plan.
- No API keys in this repository. Claude Code submits through the Higgsfield MCP connector in the agent session, which authenticates with the user's account. A human can also generate in the Higgsfield web app instead.
- Only real outcomes are recorded: job ids, credits charged, and probed clip files.

## Model
`config/generation.json` targets `seedance_2_5`. The model accepts 4–30 s, 9:16, 480p/720p/1080p, `start_image` / `end_image` / `image_references` and optional audio. Observed prices on 2026-10-12 from `get_cost` preflight were 3 / 7 / 12 credits per second at 480p / 720p / 1080p. Audio did not change the price at 1080p.

The model renders at least 4 s, so a 1-second storyboard cut is generated at 4 s and trimmed in the edit. For chicken-nanban-001 (70 × 1 s cuts) that means 280 generated seconds per full pass: about 840 / 1960 / 3360 credits at 480p / 720p / 1080p, before any retakes.

Grouping several consecutive cuts into one longer generation would lower cost, but it changes how prompts are composed. That is a creative decision for ChatGPT, not something this tool does.

## Flow
```
validate → (images uploaded + cross-check recorded) → status ready_for_generation
→ human writes generation-approval.json
→ studio.py plan P --resolution R --scenes ...      # writes generation-queue.json only if approved
→ per scene: MCP get_cost → MCP generate_video(mcp_params) → studio.py record-job P sNN JOB --credits C --resolution R
→ download result → studio.py register-clip P sNN media/P/sNN.mp4
→ human review (hands, food physics, raw vs cooked, continuity) → studio.py scene P sNN approved|rejected
```

`generation-approval.json` example:
```json
{
  "approved_by": "shuichik331",
  "approved_at": "2026-10-12",
  "max_credits": 120,
  "resolution": "480p",
  "scene_ids": ["s01", "s02", "s03", "s04", "s05", "s06", "s07", "s08", "s09", "s10"]
}
```
`check_approval` rejects a plan in any of these cases:
- the project is not `ready_for_generation` (or later),
- a requested scene or resolution is not in the approval,
- credits already spent plus planned credits exceed `max_credits`.

## Storyboard reference images
Each request records its `reference_page` and `reference_panel`. Once the page images are in the repo, two steps remain:
1. Crop each panel. The panel layout per page has to be confirmed from the real images.
2. Upload each crop with MCP `media_upload`. The returned media id goes into `medias` as `start_image` or `image_references`; the role is still to be decided.

This step is not implemented yet because the images are not available.

## Not implemented (by design or pending)
- A Python HTTP client for Higgsfield. MCP covers submission, and a direct API would need key management.
- Automatic retries. A retry spends credits again and needs a human decision.
- Publishing to TikTok or YouTube. That requires human signoff and is out of scope.
