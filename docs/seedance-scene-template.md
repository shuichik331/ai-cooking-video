# Seedance 2.5 scene template (from the s01 success)

Source: chicken-nanban-001 s01. Test-01 (job 6c4335a4) was rejected: it came out as a 4-shot recipe montage. Test-02 (job 9027cd01) was accepted provisionally: a single continuous kitchen shot. Only the inputs below changed between the two tests.

## 1. Generation settings (Claude Code fills these; ChatGPT does not need to)
| field | value |
|---|---|
| model / mode | `seedance_2_5` / `omni_reference` |
| duration | 5 s (model minimum is 4 s; the edit uses 1 s) |
| resolution | 480p for tests and drafts; final resolution is still to be decided |
| aspect_ratio | `9:16` |
| generate_audio | `false` (audio policy still to be decided) |
| count | 1 |
| `start_image` | that scene's storyboard panel, picture area only (no number/time header, caption or frame), cropped to 9:16 by Claude Code around the panel's main subject, then upscaled 4× (Lanczos) |
| `image_references` | `s03_face`: the protagonist's face and shoulders, with no hands or ingredients. Used only for cuts where the protagonist appears. |
| cost | 15 credits at 480p / 5 s. Re-quote with the final media before every submission. |

Observed in test-02: `start_image` steers the composition, but frame 0 is **not** a pixel copy of it, and the model may widen the shot slightly.

## 2. Prompt structure (for ChatGPT, the prompt owner)
These are recommendations only. Claude Code does not edit prompts.

1. **Open with the shot contract:** `SINGLE CONTINUOUS <SHOT TYPE>, 5 seconds, NO CUTS.`
2. **Anchor to the start frame:** say the supplied panel is the start frame, and describe its layout in one sentence (subject, framing, light).
3. **Describe this cut's action only:** what moves, and how little. Use the cut's own `camera` and `motion` (locked / slow push / macro, etc.).
4. **Style and continuity:** the illustration style plus the props visible *in this panel*. Do not describe the whole recipe.
5. **Identity line, only when the protagonist appears:** keep the face and hair consistent with the separate s03 face-and-shoulders identity reference, and do not copy that shot's tray or hands.
6. **Exclusions:** list the recipe stages that come *before and after* this cut, plus `scene transitions, montage, inserts, temporal jumps, extra people, overlay text, logos, watermarks`.
7. **Close with:** `Remain on this one composition for all five seconds. Vertical 9:16.`

Never append the old `global_prompt`. Its sentence "Chicken nanban cooked from raw chicken thigh through egg batter frying, … plating and tasting" is what caused the montage.

Optional `test_generation` block per scene (as ChatGPT added for s01): `reference_roles` (`s01: start_image`, `s03_face: image`). Claude Code maps `image` → `image_references`, the role name the model accepts.

## 3. Acceptance checks (Claude Code, per clip)
- No cut anywhere in 5 s: ffmpeg scene score below 0.3 for every frame (s01 test-02 maximum was 0.0068).
- Composition held: frames 0, mid and last show the same framing.
- Only this cut's action: no earlier or later recipe stage.
- Food state, hands and protagonist checked visually; face against the identity reference **and** an independent panel.
- Pick the 1-second window with the lowest inter-frame change that contains the intended action, record `trim_in_seconds`, and cut exactly 24 frames.
- Status: `generated` → `provisional` (user's tentative OK) → `approved` (final sign-off). Rejected clips stay in `jobs` history.

## 4. Spend rules
One scene at a time. Each needs a written approval (`generation-approval.json`: scope, max credits, media) and is stopped if the live quote exceeds the cap. Approvals are marked `consumed` after use.
