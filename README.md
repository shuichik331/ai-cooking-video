# AI Cooking Video Studio

ChatGPT → GitHub → Claude Code → Higgsfield → FFmpeg → TikTok / YouTube.

## Roles
- **ChatGPT** owns the cooking idea, storyboard and exact scene prompts.
- **Claude Code** validates and executes the approved storyboard; it may not silently rewrite creative decisions.
- **Higgsfield** generates scene clips (manual import for MVP; API integration later).
- **FFmpeg** assembles approved footage; publication requires human approval.

## Start
```bash
python3 scripts/validate_storyboard.py projects/karaage-001/storyboard.json
python3 scripts/render_video.py projects/karaage-001/manifest.json --output output/karaage-001.mp4
```
The renderer requires installed FFmpeg and existing scene assets. There are no generated video assets in the repo.

## Workflow
1. ChatGPT commits a storyboard JSON under `projects/<id>/`.
2. Claude Code pulls latest main, validates storyboard, and reads `CLAUDE.md`.
3. Generate/upload clips in storyboard order, add local paths to `manifest.json`.
4. Review clips; render with FFmpeg, obtain human approval, then publish.
5. Record real platform metrics and export feedback for ChatGPT.

## Security
No API keys, source clips, generated exports, personal data or account tokens in Git. Use a private repo if future content must stay confidential. AI disclosures and each platform's monetization rules must be checked before posting.
