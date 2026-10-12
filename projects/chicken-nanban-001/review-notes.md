# chicken-nanban-001: production review notes (Claude Code → ChatGPT)

Claude Code has not changed any creative file. These are observations for the creative lead. Each one is either recorded as a decision already, or waiting on one.

## Recorded discrepancy
- **s26 (page 2, cut 26):** the storyboard image shows end time 0:22. `storyboard.json` has 25–26 s. Per user instruction (2026-10-12), the JSON timing 0:25–0:26 is used. The original image is still uncorrected, and the conflict stays recorded in `production-status.json → discrepancies`. A corrected page-02 image is requested.

## Blockers
- `storyboard-pages/page-01.png` … `page-05.png` are not in the repo. The image/JSON cross-check (framing, subject, cut order) is on hold until they are uploaded.

## Questions for the creative lead (no change made)
1. **s70 garnish:** the prompt mentions "tomatoes", but no tomato appears in the ingredients (s04) or the plating (s48–s54). Is this intended?
2. **Time of day:** s01 says "morning sunlight", while s56/s66 frame the meal as "dinner" and the global prompt says "warm daylight". Which lighting should continuity follow?
3. **Boiled eggs:** s35 places peeled hard-boiled eggs with no boiling step on screen. Is it OK that they appear pre-made?
4. **Camera / motion fields:**
   - `camera` has only three generic values: "match exact framing of storyboard panel", "close-up or macro matching panel", and "wide or establishing, as storyboard".
   - `motion` is the same sentence for all 70 cuts.
   - The real direction therefore depends entirely on the storyboard images. Please confirm that is intended, or add per-cut camera and motion.
5. **Cost of 1-second cuts:** Seedance renders at least 4 s, so every cut is generated at 4 s and trimmed. One full pass is 280 generated seconds: about 840 / 1960 / 3360 credits at 480p / 720p / 1080p (balance on 2026-10-12: 890.73). Should consecutive cuts be grouped into multi-shot generations? That changes prompt composition, so it is your call.
6. **Audio:** the storyboard has no audio direction (generated audio, separate ASMR or BGM, or silent).
