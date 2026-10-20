# Token-saving rules for Claude Code in this project

- Keep CLAUDE.md short; load other docs only when the task needs them.
- Never read binary/media files. Use `ls`, ffprobe, or file names.
- Check visuals with ONE still PNG at the key frame; render full previews only when Aly asks.
- Reuse shared building blocks; a new template should be mostly props + layout.
- Edit files with small targeted edits, not full rewrites.
- `catalog.json` descriptions ≤ 15 words each (the edit-plan step reads them every video).
- Transcripts for AI: numbered sentences, no timestamps in the prompt (map IDs back to times in code).
- Ask for JSON outputs that list only what changes (e.g. sentence IDs to drop), not full copies.
- Write docs/code in English (fewer tokens than Arabic); talk to Aly in Arabic.
