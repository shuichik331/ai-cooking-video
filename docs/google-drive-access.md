# Getting the storyboard pages from Google Drive

Status on 2026-10-12: **not retrievable from the cloud session.**

- `scripts/fetch_drive_storyboards.py` stops with "Missing GOOGLE_DRIVE_ACCESS_TOKEN". The environment has no such variable, and gcloud has no logged-in account.
- The Google Drive connector attached to Claude is signed in to a different Google account. That account gets "not found" for the project folder and all five file IDs in `config/google-drive-assets.json`, so they are not shared with it.

## Options (pick one)
1. **Upload the PNGs to GitHub (simplest).** In the GitHub web UI, go to `projects/chicken-nanban-001/storyboard-pages/` → *Add file → Upload files* → `page-01.png` … `page-05.png`. No credentials are involved. Keep the repository private if the storyboards are confidential.
2. **Share the Drive folder with the connector's account.** Give Viewer access on the `chicken-nanban-001` folder to the account the Claude Drive connector uses. Claude can then read the files through the connector. Large PNGs can be slow to move this way.
3. **Reconnect the Drive connector** with the account that owns the files, at <https://claude.ai/customize/connectors>, then start a new session.
4. **Token in the environment (for the script).** Add `GOOGLE_DRIVE_ACCESS_TOKEN` in the cloud environment settings (session title bar → environment → Edit → secrets / environment variables), never in Git and never pasted into chat. Plain OAuth access tokens expire after about an hour. For repeated use, the script would need a refresh-token or service-account flow, which is not implemented yet.

After the images arrive, run these commands:
```bash
python3 scripts/studio.py validate chicken-nanban-001      # images now present → cross-check blocker
# Claude Code views each page, writes panel-layout.json, records image_verification
python3 scripts/studio.py crop-panels chicken-nanban-001   # crops to media/ (gitignored) + contact sheet
python3 scripts/studio.py test-plan chicken-nanban-001 --scene <scene>
```
