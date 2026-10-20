# Learn from the earlier Codex attempt (do this FIRST)

Folder (READ ONLY — never edit, move, delete, never add files there; Aly wants it kept uncluttered):
`E:\root\output\Youtube\Aly Shorosh New\_Ai Video Maker`
This project stays separate in `automations\video-maker\`. Copy anything reusable here; never move.

## Known structure (from Aly's screenshot, 2026-10-06)
- `AGENTS.md`, `README.md`, `CLAUDE_HANDOFF_202*.md` ← read these first (a handoff to Claude already exists)
- `knowledge-base\`: `README.md`, `START_HERE.html`, `ARCHIVE_STATUS.md`, `EXTERNAL_SOURCES.md`,
  `External_Projects_Catalog*.xlsx` (catalog of projects), and folders `asset-library\`, `inbox\`
  (README + EXAMPLE_NOTES.md), `learned\`, `reference-archive\`, `reference-browser\`, `reference-projects\`
- `projects\`, `scripts\`, `skills\`, `tools\`, `.tools\`, `__pycache__\` (skip)
- Root scripts: `transcribe_reel_raw.py`, `build_reel_v02.py`, `reel_v03.py`, `reel_v03_analysis.py`,
  `reel_v03_handoff.py`, `reel_v03_windows.py`, `reel_v03_plan.json`, `reel_v04.py`, `reel_v04_handoff.py`
  → an earlier attempt at automatic reel building; v04 is probably the latest.

## Order (keep tokens low)
1. Tree with names + sizes only (skip `__pycache__`, `.tools`, media files).
2. Read: CLAUDE_HANDOFF → AGENTS.md → README.md → knowledge-base\README.md → ARCHIVE_STATUS.md →
   everything in `learned\` (these are lessons — most valuable).
3. Excel catalog: with python/openpyxl print sheet names, headers, row count, and first 5 rows only.
   Then query specific columns as needed. Never dump the whole sheet.
4. `reel_v04.py` + `reel_v03_plan.json` (plan format = useful for our edit-plan step). Skim v02/v03
   only if v04 references them.
5. `skills\`, `tools\`, `scripts\`: names first; open only what relates to motion, transcription,
   editing, assets.
6. `reference-*` and `asset-library\`: list + read their README/index files; don't open media.

## Output
Write `docs/10-codex-review.md` (short, English):
- What was tried, what worked, what failed and WHY.
- Reusable pieces (code, prompts, plan format, asset/reference index) → copied into this project.
- Conflicts with `03-decisions.md` → list them.
Then fill `06-brand-and-setup.md` using what you found.
Finally tell Aly in simple Egyptian Arabic (4–6 lines): what you learned, what you'll reuse, and ONE
question only if something important is still unknown.
