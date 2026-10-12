# AI Cooking Video Studio

ChatGPT → GitHub → Claude Code → Higgsfield → FFmpeg → TikTok / YouTube.

## Roles
- **ChatGPT** owns the cooking idea, storyboard and exact scene prompts.
- **Claude Code** validates and executes the approved storyboard; it may not silently rewrite creative decisions.
- **Higgsfield** generates scene clips (manual import for MVP; API integration later).
- **FFmpeg** assembles approved footage; publication requires human approval.

## Start
```bash
python3 scripts/studio.py list                       # projects waiting for production
python3 scripts/studio.py validate                   # all projects (errors / blockers / warnings)
python3 scripts/studio.py sheet chicken-nanban-001   # Seedance generation sheet (verbatim)
python3 -m unittest discover -s tests                # tests (FFmpeg tests skip if not installed)
```
Rendering needs FFmpeg and approved scene clips stored outside Git. See `docs/production-pipeline.md` for statuses, files and commands, and `docs/higgsfield-integration.md` for the generation and spend-approval flow.

## Workflow
1. ChatGPT commits a storyboard JSON under `projects/<id>/`.
2. Claude Code pulls latest main, validates storyboard, and reads `CLAUDE.md`.
3. Generate/upload clips in storyboard order, add local paths to `manifest.json`.
4. Review clips; render with FFmpeg, obtain human approval, then publish.
5. Record real platform metrics and export feedback for ChatGPT.

## Security
No API keys, source clips, generated exports, personal data or account tokens in Git. Use a private repo if future content must stay confidential. AI disclosures and each platform's monetization rules must be checked before posting.
