# Storyboard image ingestion

## What is automated
Claude Code can run `python3 scripts/import_storyboard_images.py --project chicken-nanban-001 --zip /path/to/chicken-nanban-storyboard-pages.zip` from the repository root. It checks the project mapping, ensures exactly the required PNG pages, checks for unsafe ZIP paths and duplicate pages, and extracts directly to `projects/<id>/storyboard-pages/`. Claude Code may then commit and push the images.

Alternatively, on GitHub choose **Actions → Import storyboard image ZIP → Run workflow**, supplying a direct publicly accessible HTTPS ZIP URL. GitHub Actions downloads, validates and commits the PNG pages. Do not submit secrets/private presigned URLs to public workflow inputs.

## Current limitation
ChatGPT sandbox links are not public HTTPS download URLs. This workflow cannot fetch files from ChatGPT by itself. For fully unattended image handoff, connect a persistent asset store accessible to the GitHub runner, or arrange an authenticated agent with access to the image files and GitHub. Creating a storyboard inside ChatGPT does **not** automatically emit its PNG bytes to GitHub through this connector.

## Safety / review
The workflow commits images only. It does not invoke Higgsfield or incur paid model fees. Before creating video, confirm storyboard-image vs JSON agreement and explicit budget approval. Current `chicken-nanban-001` has a known s26 time-label discrepancy and remains `not_started`.
