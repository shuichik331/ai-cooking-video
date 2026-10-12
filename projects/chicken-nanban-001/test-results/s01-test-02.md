# s01 Seedance 2.5 test 02 — result: usable (awaiting human approval)

| item | value |
|---|---|
| date | 2026-10-12 |
| approval | user, chat (start image B, s03 face ref, 480p, 5 s, max 15 credits) |
| job | `9027cd01-bf6e-4671-a2ac-1c3bcc1a3e51` |
| request | seedance_2_5, omni_reference, 5 s, 480p, 9:16, no audio |
| prompt | prompts.json s01 `higgsfield_prompt` (commit 56ba4ac), verbatim; old global_prompt not appended |
| media | start_image = s01 panel cropped to 9:16 (`a8d063ab…`); image_references = s03 face/shoulders (`0e722b28…`) |
| quote / charged | 15 / 15 credits (balance 875.73 → 860.73) |
| output | 480×854, 24 fps, 121 frames, 5.04 s, no audio, `media/chicken-nanban-001/clips/s01_test02_480p.mp4` (not in Git) |

## Checks
| requirement | result |
|---|---|
| One continuous shot, no cuts | **Pass.** No cut above scene score 0.3; maximum score in the whole clip is 0.0068. |
| Kitchen-wide composition held for 5 s | **Pass.** Locked camera; frames 0 / 60 / 120 show the same framing. |
| No cooking steps or other cuts | **Pass.** He stands at the sink with only slight breathing and a small arm shift. |
| Matches storyboard s01 | **Pass.** Back view at the sink, pendant lamp, range hood, upper cabinets, table and chair in the foreground. |
| Illustration style | **Pass.** Hand-drawn anime look with ink outlines and a warm palette; cleaner and sharper than the low-res panel. |
| Protagonist | **Partly checked.** Black tousled hair, white T-shirt and dark trousers match. The face is not visible (back view, as in the storyboard), so the s03 face reference could not be checked in this shot. |
| Hands | No visible deformation at 480p; the hands are mostly hidden by the body. |

## Note on start_image
Frame 0 is **not** a pixel copy of start image B. The API echo listed both images under `reference_images`, and Seedance redrew the scene a little wider: the refrigerator (right) and window (left) from the original panel are back, and more floor shows. The composition still follows the storyboard. If an exact first frame is ever needed, it has to be confirmed how Higgsfield maps `start_image` in omni_reference mode.

## Selected 1 second
- **Window:** 1.50–2.50 s (frames 36–59, 24 frames).
- **File:** `media/chicken-nanban-001/clips/s01_cut_from_test02.mp4`. `trim_in_seconds: 1.5` is recorded on s01.
- **Reason:** the most stable 1-second window (mean inter-frame change 0.10/255, max 0.22). It avoids the arm movement around 3.4 s, and every window has the same panel similarity, since framing is identical throughout.

## Status
- s01 is `generated` and **not approved**: human review is required before it counts as an approved clip.
- Test-01 (job 6c4335a4, rejected) stays in `production-status.json → scenes.s01.jobs` and in `media/`.
