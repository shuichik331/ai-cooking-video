# s01 Seedance 2.5 test 01 — result: rejected

| item | value |
|---|---|
| date | 2026-10-12 |
| approval | user, chat: "正面のコマを加えて、なおかつ 480p で5秒間で作ってほしいです。" (`generation-approval.json`, max 15 credits) |
| job | `6c4335a4-b957-41ed-bbda-de7dbd7aefb1` (Higgsfield) |
| request | seedance_2_5, omni_reference, 5 s, 480p, 9:16, no audio, prompt = prompts.json s01 verbatim |
| references | `image_references`: s01 panel picture area (4x upscale), s03 face/shoulders only (4x upscale) |
| quote / charged | 15 / 15 credits (balance 890.73 → 875.73) |
| output | 480×854, 24 fps, 121 frames, 5.04 s, no audio. Kept local at `media/chicken-nanban-001/clips/s01_test_480p.mp4` (not in Git) |

## What was generated
Scene detection (ffmpeg, threshold 0.3) finds 4 shots:

| time | content |
|---|---|
| 0.00–0.33 s | hand dipping raw chicken into beaten egg |
| 0.33–1.92 s | chicken frying in a shallow pan; the meat is still pink under a thin crust |
| 1.92–3.38 s | sliced cutlet on a white plate with brown sauce poured from a spoon and a piped tartar rosette |
| 3.38–5.04 s | protagonist close-up eating with chopsticks, then smiling |

## Against the test objectives
| objective | result |
|---|---|
| Protagonist appearance | **Good.** Face, tousled black hair and white T-shirt clearly follow the s03 reference. |
| Kitchen background | **Not tested.** No wide kitchen shot was produced, and the s01 kitchen reference was effectively ignored. |
| Illustration style | **Good.** Hand-drawn anime look, ink outlines and warm palette close to the storyboard. |
| Fit for s01 | **Fail.** The clip is not s01 (wide establishing shot). No 1-second window shows the kitchen. |
| Food accuracy | **Fail.** Undercooked-looking frying, tonkatsu-style slicing and spoon-poured sauce: steps that are not in the storyboard. |

## Likely cause (production finding, prompt not changed)
Every `higgsfield_prompt` in prompts.json ends with the shared `global_prompt`, which contains the sentence:
> "Chicken nanban cooked from raw chicken thigh through egg batter frying, sweet-sour nanban sauce, egg-onion tartar sauce, plating and tasting."

Seedance 2.5 read this as a story to tell and generated a multi-shot recipe montage inside one 5-second clip. That sentence is in all 70 prompts, so every cut is likely to drift the same way. This is a creative-file issue for ChatGPT. Claude Code has not edited the prompt.

## Options for the next test (each needs approval; ~15 credits at 480p)
1. **ChatGPT supplies a generation-ready s01 prompt** (recommended). It would keep the global style and character description, drop the whole-recipe sentence, and state "single continuous shot, no cuts".
2. **Production-side only, prompt unchanged:** pass the s01 panel as `start_image` instead of a reference, so the first frame is anchored to the storyboard framing. The panel is landscape, so it would be letterboxed or outpainted to 9:16. Montage drift is still likely while the recipe sentence remains.
3. Combine 1 and 2.
