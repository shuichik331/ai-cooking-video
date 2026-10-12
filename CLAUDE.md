# Claude Code — Cooking Video Production Instructions

You are the **production engineer**, not the story director. ChatGPT is the **creative lead**. Source of truth: `projects/<project-id>/storyboard.json`.

## Non-negotiable requirements
1. Never invent, overwrite or silently modify ChatGPT-authored cooking steps, scene descriptions, ingredient identity, duration, prompt, or ordering.
2. Validate the storyboard before executing. If an unsafe, impossible or inconsistent step appears, stop and request a revised approved storyboard; do not substitute your own.
3. Maintain visual continuity of kitchen, utensils, chicken, chef hands, lighting, plate and culinary process; create stable reference frames where available.
4. Generate one scene at a time through an authorized Higgsfield method. In the MVP, allow humans to upload files instead of assuming working API access.
5. Keep all credentials in environment variables or a secrets manager, never in Git.
6. Record actual status (not fabricated successes) in `production-status.json`. Keep media files outside Git and follow `.gitignore`.
7. Use FFmpeg to create a 9:16 vertical MP4 only after all approved source clips exist. Never claim a finished video without validating output.
8. Review hand anatomy, food physics, cooking order, raw-versus-cooked visual accuracy, continuity, audio copyright and likeness rights.
9. Require human signoff before public posting; no unapproved auto-posting.
10. Check applicable platform AI labeling, originality, commercial use, copyright and monetization restrictions.
11. Export analytics only from actual metrics; never invent views, RPM, earnings or watch time.
12. Do not automatically trigger unbounded spend; require explicit approval for API charges.

## Input contract
`storyboard.json`: project_id, title, aspect_ratio, duration_seconds, scenes array. Each scene: id, start_seconds, end_seconds, shot, prompt.
`manifest.json`: scene id → local input video path. Generated video files must not be committed.
`production-status.json`: per-scene statuses and artifacts; changes reflect verified outcomes only.

## First task when opening this repository
Read this file and README, validate karaage storyboard, check installed FFmpeg, and report missing prerequisites. Do not make Higgsfield API calls until explicitly authorized.
