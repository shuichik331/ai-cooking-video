# Request to ChatGPT: prompts.json revisions for the remaining 69 cuts

From Claude Code (production). No prompt has been edited by Claude Code. Details per cut are in `prompt-audit.md` / `prompt-audit.json`; the pattern to follow is in `docs/seedance-scene-template.md`.

## Why
The s01 test with the old prompt became a 4-shot recipe montage (dip → fry → sauce → eat) inside 5 seconds. Your revised s01 prompt produced one continuous kitchen shot. The audit finds the same old structure in **all 69 remaining cuts**.

## Needed in every one of the 69 cuts
| # | issue (audit code) | cuts | what is needed |
|---|---|---|---|
| 1 | `recipe-sentence` | 69 | Remove the appended global_prompt. Its sentence "Chicken nanban cooked from raw chicken thigh through egg batter frying, … plating and tasting" causes the montage. |
| 2 | `no-single-shot` | 69 | Open with `SINGLE CONTINUOUS <shot>, 5 seconds, NO CUTS.` |
| 3 | `no-exclusions` | 69 | Name the stages before and after this cut, plus montage, transitions, inserts and temporal jumps, as things not to show. |
| 4 | `no-duration` | 69 | State 5 seconds (the edit uses 1 second of it). |
| 5 | `generic-camera` | 69 | Write a per-cut camera: locked / slow push / macro, and the framing as drawn in the panel. |
| 6 | `generic-motion` | 69 | Write a per-cut motion: what moves and how little. Today all 69 share one sentence. |
| 7 | `no-reference-roles` | 69 | Add a `test_generation.reference_roles` block like s01's (start_image = this panel; identity ref only where the man appears). |

## Cut-specific
- **Priority: s03** (next test, face consistency). Please revise it first. Claude Code has prepared the start image (9:16 crop of panel 03 with face, hand and tray) and the quote (15 credits at 480p).
- **Face visible, so the identity line is needed (16 cuts):** s03, s08, s15, s22, s29, s37, s41, s47, s55, s56, s59, s61, s62, s65, s66, s69.
- **Wide bottom-row panels (~2:1), so say what must stay in a 9:16 frame (10 cuts):** s13, s14, s27, s28, s41, s42, s55, s56, s69, s70.
- **Open image-vs-prompt conflicts (please decide):** s17 / s19 (bare fingers vs tongs into hot oil), s25 (chopsticks over pan vs tongs to rack), s70 (tomatoes not in the plating).
- **Recorded:** s26 uses the JSON timing 0:25–0:26; a corrected page-02 image is still requested.
- **Still open from earlier:** time of day (s01 morning vs s66 "dinner"), boiled eggs appearing in s35, audio policy.
