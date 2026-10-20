# Two editing experiments (Aly asked 2026-10-06)

Same video for both, so results compare. Folder per video: `projects/<code>/input|work|output`.

## Shared pipeline (free, local)
1. `input/` raw clip(s) (after DaVinci silence removal or raw — both OK).
2. Transcribe: faster-whisper (CPU int8, word timestamps) → `work/transcript.json` + numbered sentences
   `work/sentences.txt`. Warn on ASR gaps (Codex v01 lost 115 s to gaps — check coverage vs duration).
3. ONE Claude call → `work/plan.json`: keep/drop sentence IDs (repeats, mistakes, best take),
   chapters, motion cues `{template, props, atSentence}`, B-roll needs (text only).
4. Render each motion cue → `output/overlays/<code>_<order>_<template>_<startTC>.mov` (ProRes 4444 alpha).
5. Build Premiere-importable FCP7 XML: V1 kept speech cuts, V2 overlays at their times, A1 speech
   (short audio crossfades). + `output/review.mp4` quick preview via ffmpeg.

## A — Full edit by Claude
Steps 1–5 automatic. Aly imports the XML in Premiere, watches, notes changes in Arabic → only affected
pieces re-render.

## B — Aly edits, Claude prepares
Steps 1–4, then `output/edit-guide.html` in Arabic: list per timecode — "احذف من … لـ …" (with reason),
"حط الموشن ده هنا" (file name), "دور على صورة لـ …". Aly does the cut himself; overlays are ready to drag.

## Success check
Aly's verdict + time he spent, per mode. Not technical checks.
