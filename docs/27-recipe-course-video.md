# Recipe: long COURSE video from old screen-recorded lessons (premiere pro course, 2026-10-16/17)

Job: `projects/2026-10-16 youtube premiere pro course` — his 2018 Premiere course (YouTube playlist, 3 parts, 2:55 h, 720p 25 fps,
screen only, no face) → ONE course video (2:58). Notes asked: nothing cut, no intro/outro, screen recording ALWAYS visible, English word
explainers, shortcuts on screen, callbacks, definitions, chapters with title separators + music, timestamps with icons at the start,
⚡ "easier in Premiere 2026" + best video + QR + "Claude recommends, not Aly", names in other programs bottom-left, final chapter
"what's missing", a 2018 disclaimer with a proof screenshot, Claude's coverage analysis as a chart, no AI voice-over.

## Review lessons (Aly)
- Coverage %: compare with TODAY's program; an explained tool counts fully; exclude non-editing parts and say how big they are;
  show 3 sourced yardsticks + what's missing + why they differ (100 / 81 / 71). Also as Excel (`work/scripts/make_coverage_xlsx.py`).
- Music under the WHOLE opening (not only the timestamps). Never "الحلقة 1/2/3" in a merged video — only "الفصل N من 47".
- Opening text = typed text, no AI voice (viewers would think the video is AI).

## Pipeline (`work/scripts/`, archived in `tools/recipes/premierecourse/`)
1. `tools/fetch.py`-style yt-dlp of the playlist → `input/ep1..3.mp4`; `tools/transcribe.py` per episode (mkdir work/epN first!).
2. `analyze.py 1 2 3` → per episode: his yellow cursor highlight (x,y @4 fps; ~(138,130,5) over black), screen diff, audio dB/0.1 s.
3. Research: `tools/evidence.py` (headful Chrome: `EV_HEADFUL=1` — helpx blocks headless; never bypass bot checks: loc.gov → NGA)
   rows in `research/evidence.json` (fetch → find → check → shoot). Official PDFs: `tools/pdf_evidence.py` (pypdfium2, highlighted page).
   Videos: yt-dlp `ytsearch8:` → prefer Adobe official, short, current; thumbnails `i.ytimg.com/vi/<id>/hqdefault.jpg`, QR via `qrcode`.
4. `make_course.py ch1` = opening + chapter 1 (the hand-tuned review part). `course_data.py` = glossary (Arabic-letter spellings
   too!), spoken shortcuts, per-chapter cards anchored on WORDS (regex in the chapter's words), FF waits, ⚡ cards.
5. `make_full.py` → `props_full.json`: chapter edges snapped to 150 ms quiet, FF pieces ×4 (muted, low music, chip), auto Kw (again
   after 3 min), auto Keys, manual cards, side mode while a left-column card is up, slides chapters auto-cropped to the slide content,
   zoom on clicks (cursor still ~1 s then screen changes; ≥12 s apart; only where the crop has content).
6. Stills (`stills_cli.sh`) → `render_full.sh`: 20-min MUTED video chunks (9 × ~45 min; slower when the PC is busy).
   Paths to node/python from Git Bash must be `cygpath -m`.
7. Audio: NEVER Remotion's `--codec=wav` pass for a 3 h video (it visits every frame ~8 h and its temp filled E: at 98%).
   `mix_audio.py` builds the same mix with ffmpeg from props (voice pieces at rate 1, music with linear fades, sfx; amix normalize=0)
   in ~6 min, then concat (copy) + mux → `output/premiere_course_full.mp4`. Checked: sync < 1 ms, voice level ±0.3 dB vs source.

## Composition `course` (25 fps, `motion-library/src/course/`)
kit.tsx: Screen (full / side / sideR / wide + crop keys), CourseBg, Kw (bottom pill), Fig (Crash-Course "Fig N.N" card), Def,
Chip (back / later / weak / fix / tip / new / same / ff), Key (keycaps), Alt (DaVinci name, bottom-left), New26 (⚡ card + thumb +
QR), Hud, Ico (40 animated vector icons), Sep (chapter separator, thumb auto-cropped to the slide), `bi()` = isolate Latin runs inside
Arabic (else "4K" → "K4"). scenes.tsx: opening scenes (OProof, OName, OLine, OMeter, OWhy, OChanged, OVerdict, OStamps), ONext
(last chapter), chapter-1 animations. anims.tsx: concept animations for the left column. In `Type`, join English phrases with `_`.
Course.tsx renders only cues near the current frame (hundreds of cues).

## Shorts series from the course (2026-10-18) — 44 shorts, composition `course-short`
Scripts (project `work/scripts/`, archived in `tools/recipes/premierecourse/`):
- `shorts_data.py` = every short: `pieces` (a/b in the episode, `ep` per piece allowed), `show` (screen | anim name | `big:line|sub`),
  `crop` / `dual=(setting, result)` / `under=crop` (+`under_src`) = animation on top + his screen under it, `step`, `kw`, `key`,
  `labels`, `fix` (+source), `new` (⚡ 2026 card), `CAP` = hand-corrected captions per piece. Crops are in 1276×720 space for all eps.
  Useful crops: `PROG_PANE` (program, wide pane), `TL1` (ep1 timeline, single card), `TLD` (ep1 timeline TRACKS for wide/dual panes).
- `make_shorts.py N…` → `work/shorts/props_NN.json`; `caption_words.py N…` (re-transcribe each piece → words_NN.txt to write CAP);
  `fix_edges.py` (snap edges to whole sentences → `work/shorts/edge_fixes.json`, applied at the end of shorts_data);
  `render_shorts.sh "N NN_name" …` (one bundle, TEMP on E:, then `level_shorts.py`); `level_shorts.py` = body -16 LUFS, CTA 1.5 dB
  under, peak ≤ -1, and the video re-encoded like Aly's own `ffmpeg -i in out` (libx264 CRF 23 + AAC) to keep files small;
  `make_txt.py N…` = titles + description + pinned comment beside each video; `frame_sheet.py`, `chapter_text.py` for planning.
Lessons (Aly reviews 2026-10-18):
- Never cut his words: a piece's last word is always kept whole; and never let a piece start/end on half a neighbouring sentence —
  check `fix_edges.py` output (Whisper segments break mid-sentence).
- Every edit he talks about must be SEEN: dual card (setting on top, result below) with the panel that actually changes (timeline
  TRACKS, not the ruler). An animation alone is not enough — use `under=` to put his real screen under it.
- Motion drawings must be technically right (Linear = straight line; `InterpGraph` for interpolation, Adobe definitions).
- Each short must stand alone: hook (result) → why → steps → result. If his 2018 explanation is shaky, build from the clear parts.
- Latin phrases inside `big:` / Type text need `_` (else the words come out reversed); avoid Arabic "و" between two Latin words.
- Stills: `stills_cli.sh` now keeps Remotion's TEMP on E: (each still copied 0.24 GB into C:\Temp; 15 GB cleaned on 2026-10-18).
- Click marks: `clicks()` (yellow-cursor detector) misses clicks, esp. on ep3 (yellow track buttons confuse it). Add `clicks=[(abs_t, x, y)]`
  per piece (1276×720 space, read from `frame_sheet.py`). Dual cards now draw marks in whichever pane contains the point.
- Anims added for this series: `InterpGraph` (kind linear/hold/bezier/easeIn/easeOut/all), `RoseKey` (stage 1/2: his rose example +
  "💾 Save" keyframes + Play), `HideNote` context hides anim notes in shorts; `under=` puts the anim small on top + his screen below.
- Delivery: `_raw` = render only (delete after); `output/shorts` = leveled + compressed finals + .txt. Don't delete finals before the
  new version replaces them. Don't run a 2nd level pass over files he may be watching (a half-written mp4 = "broken" file).
