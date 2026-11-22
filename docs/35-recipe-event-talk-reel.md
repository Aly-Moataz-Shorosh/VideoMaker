# Recipe: reel from an event Aly attended (foreign guest, EN + AR) — style 26 event-talk-reel

Job: `projects/2026-11-22 reel-h garrett warren short video` = his 9:16 phone recording (HEVC 1080x1920 rotated, 60 fps, 2:58) of
Garrett Warren (stunt coordinator + 2nd unit director, Avatar 1-3) answering a question at UTH Festival 2026, Grand Egyptian Museum.
Output `output/v2/garrett_warren_uth.mp4` (2:05) + `.txt`. APPROVED v2 ("thanks save knowledge and style").

## What Aly asked (notes.txt + chat)
- Fast hook first, then the video from where the guest says "hit me" (= start of the question), under 3:00. No CTA.
- While he explains: visualise what he says + pictures from the film.
- Captions: English + Arabic translation under them. ElevenLabs for the captions "علشان الدقة".
- Explain the event (UTH, GEM, Friday + Saturday) and who the guest is.
- Title: make clear the question is about imagining it DURING FILMING; on screen = English title with the Arabic one under it.
- Footer: his channel face + handles, CENTRED, vertically centred on one line; only YouTube / TikTok / Instagram @alyshorosh +
  Facebook aly.shorosh (LinkedIn, Behance not important; no "Aly Shorosh" name image).
- .txt in ENGLISH, first description line: "I attended … and recorded this moment myself."

## Pipeline (scripts `tools/recipes/uthgarrett/`, project copies in work/scripts)
1. `transcribe_en.py` — local Whisper EN pass (tools/transcribe.py is Arabic-only) to find the structure quickly.
2. ElevenLabs Scribe (claude.ai ElevenLabs connector: creative_create_flow → creative_upload_flow_reference audio → Aly picks the
   mp3 in the picker → creative_transcribe_audio eleven_scribe_v1) → `work/el_words.json` (word times).
   ⚠ COST: estimate_only said 54 credits, the run charged 981 (3 min audio). Tell Aly the real risk before running.
3. Fix captions by ear + sources: "John Landis" → **Jon Landau** (Avatar producer, died 2024 — NPR), "the rook for where" → "the
   rookery where", unclear word dropped ("So sorry, Jon."). Arabic = Egyptian, one line per phrase (`plan.py` PHRASES).
4. Facts: `tools/evidence.py` rows (Egyptian Streets = UTH dates/place; MPA = guest role "on all three films", SAG; NPR = Landau).
   IMDb blocks the fetcher.
5. Pictures: the fan wiki CDN is bot-protected → do NOT force it. Official YouTube videos instead: `yt_sheet.py <id> <step>` (dense
   contact sheet from the stream, no download) → `yt_frames.py <id> <prefix> <dir> t…` (HD stills). Trailer frames are letterboxed
   (2.35:1 inside 16:9) → Photo zooms 1.34 on tr_*. The featurette is SD (640 px) → show ≤ 640 px wide. Portraits: Commons via
   `tools/recipes/enta_ep01/commons.py get` (thumb width 960; direct upload.wikimedia URLs refuse). Credits line under the tray.
6. Edges on the waveform (20 ms dB around each edge; crowd floor ~ -31 dB) → `plan.py` HOOK / MAIN.
7. `make_cam.py`: ONE ffmpeg run PER PIECE (hook | rewind = hook reversed every 7th frame, 27 f | main), frame count asserted, then
   concat. ⚠ a single graph with `split=3` + trim/reverse DROPPED 38 frames (picture 1.3 s short). Audio built separately (atrim +
   apad whole_dur, rewind = silence + tape sfx).
8. `make_props.py` → props (caps with ElevenLabs word times when counts match, else spread by length; cues; sfx; zoom 1.0/1.08).
9. Composition `uth-reel` (src/uth/UthReel.tsx): Header (tag + EN title + AR title), BiCaps, tray scenes pic / vs / event / who /
   person / term / count / emo / crown / versions / gear / logo / hire, Rewind from stage kit, Footer.
10. Bundle on D:/Temp/bundle_uth, TEMP on D:, `--concurrency=6`, then `volume=+1.6dB, alimiter` → -16 LUFS, x264 CRF 23 (shorts
    always compressed). Check: 3748 video frames = audio length; reels-publisher `app.bulk.notes_for` reads the txt.

## Gotchas
- "و" between two English words inside Arabic (bi() isolates) rendered like a Latin "g" → rephrase ("منتج أفلام Avatar",
  "James Cameron وعالم Pandora").
- Black logos (TikTok svg) vanish on the dark footer → small white tile.
- VS labels must sit under their own card (a shared centred label looked wrong).
- Redo after approval → `output/v2/`, old version kept.
