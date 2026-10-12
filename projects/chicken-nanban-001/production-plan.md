# chicken-nanban-001: full 70-second production plan (480p)

Status: **awaiting cost approval and ChatGPT's confirmation of the draft prompts.** No paid generation has been run under this plan.

## Inputs checked
- 70/70 storyboard panels cross-checked against storyboard.json / pages.json (`storyboard-crosscheck.md`); s26 timing decision recorded.
- All 70 panels cropped (picture area only) and checked visually; 9:16 start images made for the first cut of each group. s55's crop loses the face (header tab), so it will be repositioned by hand before generation.
- s01: reuse the provisional clip (job 9027cd01, 1.5–2.5 s).

## Generation strategy
- **Group by cooking stage:** 69 cuts in 20 Seedance generations (`production-groups.json`), with 2–4 consecutive cuts each.
- **Shot length:** about 1.5 s per shot, because Seedance splits shots unevenly (test-01 had a 0.33 s shot).
- **References:**
  - `start_image`: 9:16 crop of the group's first panel.
  - `image_references`: the panels of the other cuts in the group, plus s03_face where the protagonist's face shows, plus the s01 kitchen frame for the room-wide shots.
- **Prompts:** drafts in `generation-prompts-for-review.md`. Each keeps the original cut text verbatim, removes the whole-recipe sentence and adds a multi-shot contract, audio line and exclusions. ChatGPT confirms them before use.
- **Audio:** Seedance native audio (`generate_audio: true`, no extra cost per quote), asking for natural cooking sounds, no music, no speech.
- **Check order:** G01 runs first as the check for the grouping method. If the shots don't follow the 4 panels, stop and choose between re-planning and single-cut generation.

| | generations | credits (480p) |
|---|---|---|
| base | 20 | 327 |
| expected (≈6 group retakes) | 26 | 417 |
| requested cap (+10 single-cut fixes) | up to 36 | **537** |
| fallback: every cut alone (4 s) | 69 | 828 (no margin) |

Balance on 2026-10-12: 860.73.

**Blocked until ChatGPT decides:** G05 (s17), G06 (s19), G07 (s25), G20 (s70).

## Edit and delivery (FFmpeg, no cost)
1. Split each group clip into its cuts (`studio/shots.py`): detect cuts, map shots to cuts in order, then take the steadiest 1 s inside each shot, at least 0.08 s away from the cut. A shot shorter than about 1.2 s is flagged for a single-cut fix.
2. Record each cut's source clip and `trim_in_seconds` in production-status.json; the user reviews each cut (`provisional` → `approved`).
3. Render 70 × 24 frames → **480×854 master** (`--size 480x854`) plus a 1080×1920 upscale for the platforms. Audio: per-cut native audio with 10 ms fades and loudness normalised to −14 LUFS.
4. Verify with ffprobe (70.0 s, 9:16, fps, codecs, audio), then write the 70-second quality report (per cut: match to panel, protagonist, kitchen, utensils, food state, hands, audio; overall: continuity, rhythm, loudness).

## Not covered by Seedance audio
Higgsfield's MCP has no general music/SFX model for this use. If native audio is weak, the alternative is licensed SFX that you provide (with source and licence recorded).
