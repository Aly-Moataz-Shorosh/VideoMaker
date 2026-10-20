# Recipe: condensed tutorial short from an edited video (first real job, RippleCutToll 2026-10-06)

Result Aly approved ("حلو اوي النتيجة دي"): `projects/2026-10-06 shorts RippleCutToll/output/short_02.mp4`
(9:16, 1:28, his DaVinci "Remove Silence" tutorial condensed from 2:41 + his CTA clip). v1 = short_01 (rejected
points listed in "Review lessons"). Reuse this recipe for any "make one short from my tutorial" job.

## Inputs
- His edited video (`input/`), his CTA clip (`input/`, filmed: "comment <word>"), notes.txt.
- His project folder on F: (read-only): screen recordings, `.prproj`, images. Copy small files only.

## Steps (commands from repo root unless noted)
1. **Transcribe**: `python tools/transcribe.py <video> <proj>/work` (CTA clip → `<proj>/work/cta`).
2. **Read his .prproj** (gzip XML) → where his screen recordings / overlays sit and the main-track clip in/out.
   Parser idea: ObjectID/ObjectRef map; `VideoClipTrackItem` Start/End (ticks / 254016000000 = s) → SubClip →
   Clip InPoint → Media `ActualMediaFilePath`. Gives rec_time = edit_time − offset (here 42.03).
3. **Clean footage** if his edit has baked-in full-screen recordings / green-screen clips (vertical crop would
   show the middle of a UI): `work/mkclean.py` rebuilds V1 from the raw file with his exact cuts, audio from his
   final export → `work/clean.mp4` (verified PSNR ≈ 36 dB vs his export). Plan key `"video": "work/clean.mp4"`.
4. **Find UI positions**: ONE contact sheet of the recording + one full-res crop (menu/dialog) → pixel rects.
   Find UI events (menu open, dialog close, timeline change) with frame-difference numbers, not by looking.
5. **Choose ranges** (`plan.keep`, source seconds of his edit, in play order): hook first, closed ideas only.
   Then `work/snap_edges.py <video> '<ranges>'` moves every edge to the quietest point ±0.25 s; if the level there
   is still loud (> −30 dB) the cut is inside speech → merge the neighbouring ranges instead.
6. **Captions**: `work/retranscribe_keep.py` (run from repo root) re-transcribes only kept ranges with an
   English-terms prompt → `work/fix_words.py`: full corrected sentence per range, timing aligned by difflib;
   missing English terms are interpolated into Whisper gaps. CTA text via `plan.fix["A1:S001"]` (same word count).
7. **Cues** (`work/make_plan_v2.py`): anchors by source second (`"src": 57.8`) or `"at": "A1:S001", "word": n`
   for the appended clip. Max gap ≤ 3 s between visual events (zooms, mark changes and diagram phases count).
8. **Check** with stills only: `cd motion-library && node stills.mjs edit-v <edit.json> <sheet.png> <frames...>`.
9. **Render**: `python tools/build_edit.py <proj> --name short_02 --vertical --render`. Level the CTA audio after
   (ffmpeg `volume=enable='gte(t,<cta_start>)'` + `alimiter`) — his phone clip is ~8 dB quieter.
10. Premiere (optional, Aly said not needed this time): `--overlays` → `<name>.xml` (V1 cuts with zoom pieces,
    V2 one alpha .mov per graphic, V3 captions .mov) via `motion-library/overlays.mjs` (bundles once).

## Templates made for this job (registry + catalog)
| id | what | key props |
|---|---|---|
| `screen_ui` | crop of a real screen recording as a card; camera move crop→crop2; glowing marks + labels | src, start, still, crop, crop2, moveAt, marks[{x,y,w,h,from,to,label}], title, width, top |
| `comment_cta` | comment box types the keyword → posts → DM with link arrives | keyword, dm, typeAt, sendAt, dmAt, title, top |
| `threshold_wave` | waveform + dB line: under = silence (red, removed), over = speech (green), gaps close | db, silenceAt, keepAt, collapseAt |
| `trim_handles` | speech clip; silence cut, pre/post handle frames stay, closes up | cutAt, preAt, postAt, closeAt |
| `audio_crossfade` | two clips: hard-cut "click" → overlap with X fade lines → smooth | overlapAt, doneAt |
build_edit plan keys added: `video`, `keep`, `append[{video, transcript, keep}]`, cue `src`.

## Layout numbers (9:16, 1080×1920)
Face 0.12–0.40 · cards top 0.36–0.42, width 0.8–0.9 · captions block ~0.66–0.73 · tall crops (dialog 430×250)
use width 0.8 so the card ends above the captions. CTA clip: card at top 0.02 (his face is low in that framing).

## Review lessons (v1 → v2)
- Never cut inside a phrase; Whisper gaps are lost words, not pauses (v1 ate "Threshold").
- CTA = last clean take, one piece (v1 spliced two takes → "يوتيوب" twice).
- Check numbers/signs against the UI and what he says ("negative 20" = −20 dB).
- Name labels are not enough: show the concept (threshold / pre-post / crossfade diagrams).

- (figmaMake 2026-10-08) Every button he clicks gets a highlight mark in the real recording; every tool he names gets its logo; faces never cropped (tools/face_pos.py). Full list: docs/17.

## Archived project
RippleCutToll folder may be gone. Helper scripts kept in `tools/recipes/RippleCutToll/` (snap_edges, mkclean,
retranscribe_keep, fix_words, make_plan_v2) — run from a new project's work/ after editing their paths.
