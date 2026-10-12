# ChatGPT creative decisions — 2026-10-13

Status: creative guidance only. **No paid generation authorized.** Parent storyboard and scene timing remain authoritative. Claude Code should read this on main and merge or cherry-pick into its production branch before continuing.

## Resolve reference vs prompt conflicts

- **s17 / s19 (G05 / G06):** Follow storyboard depiction of carefully lowering chicken into oil **with hands kept safely away from hot oil**. To reconcile safety and staging, use **long cooking chopsticks or tongs** to lower the raw-coated chicken; never portray bare fingers entering or hovering immediately above hot oil. Preserve close camera composition and oil bubbling. A small, local visual adjustment for safety is approved; do not change timing or step.
- **s25 (G07):** Follow storyboard: **long cooking chopsticks** lifting fried chicken from the pan toward the rack. Replace any mention of metal tongs with chopsticks in the derived generation prompt. Do not replace the shot.
- **s70 (G20):** Remove unexpected cherry tomatoes from the image-generation prompt. Keep the finished dish consistent with s49–s54: chicken nanban, cabbage, egg tartar sauce and parsley. Do not introduce new ingredients at the end.

## Prompt construction rules

1. Preserve original per-scene action, shot order and timing in storyboard JSON.
2. Use only style/person/kitchen continuity clauses as reusable global context. **Never** append a summary of all cooking stages to a shot or a multi-cut generation request.
3. For each proposed 2–4-cut group, specify explicit temporal beats and shot IDs. Generation may ignore beat timing; split only if each required cut actually appears and lasts long enough for one stable second.
4. Use the storyboard crops as camera/composition references. Crop caption bars and grid lines; approve s55 manual recrop so face is not lost.
5. Generated audio must be evaluated per cut for synchronized and realistic ASMR. Never assume native audio is guaranteed or use copyrighted sounds without rights.
6. Don't quietly fill missing beats with unrelated generated actions. Log omissions and request creative decision if repair changes the scene.
7. G01 is a **feasibility gate**, not authorization to complete all groups automatically. Stop after inspecting results and report per-shot usable seconds and costs.

## Budget policy
- Claude Code proposal: 20 groups, estimated baseline 327 credits, possible ceiling 537 credits.
- These figures are estimates, not an authorization. **Maximum authorized additional spending is 0 credits** until the user explicitly approves a number.
- Request approval separately for G01 first (estimated 6s = 18 credits at 480p based on the reported 3 credits/s rate), verify exact reference-inclusive quote before running, and stop if exceeded.
- Don't proceed to G02–G20 or retries without a specific subsequent authorization.
