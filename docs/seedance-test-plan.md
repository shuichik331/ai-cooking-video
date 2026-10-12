# Chicken nanban Seedance 2.5 — test plan

## Confirmed information
- Google Drive folder `chicken-nanban-001` has five uploaded storyboard pages.
- File IDs are in `config/google-drive-assets.json`.
- `storyboard.json`, `prompts.json` and `pages.json` cover 70 one-second cuts.
- A read-only Higgsfield preflight for `seedance_2_5`, 5s, 9:16, 720p, omni_reference, generate_audio:false returned **35 credits** on 2026-10-12. This is an estimate, not a validated job with uploaded references.
- Do **not** submit a paid Higgsfield request until explicit user approval of that cost and of the prepared references.

## Image retrieval on Claude Code machine
1. Clone/pull the repository.
2. Obtain an OAuth token with Drive read access under the user's authorized account. Store it only in local environment variable `GOOGLE_DRIVE_ACCESS_TOKEN`. Never commit it or print it. Token provisioning is not automatic and may expire.
3. Run `python3 scripts/fetch_drive_storyboards.py --project chicken-nanban-001`.
4. Compare all five images with `pages.json`, `storyboard.json`, `prompts.json`. Note: page 2's shot s26 has a timecode inconsistency; hold and request ChatGPT correction rather than reinterpreting it.
5. Crop each panel into a standalone reference; exclude caption bars, labels and grid edges. Review crops against storyboard manually before generation. Keep a consistent character/style reference.
6. Design an approved 5-second proof with scene mapping, correct visuals, smooth motion and no fabricated cooking steps. Do not presume a montage can be created directly from an entire 14-panel sheet.
7. Quote final price with actual references, request user approval, then generate at most one 5-second trial.
8. Review anatomy, kitchen continuity, food state, audio and timing before proceeding.

## Boundaries
- The GitHub repository currently does not contain binary storyboard images: Google Drive stores them privately.
- GitHub Actions cannot fetch these Drive files without authorized Drive OAuth credentials or another access mechanism.
- Claude Code must not say the auto-download is working until OAuth credentials are configured and downloads are tested.
- Keep project `not_started` until the image/JSON mismatch is resolved and the pipeline verified.
