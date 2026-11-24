# Recipe 36 — AI-world explainer (style 27): a long YouTube video made entirely with AI

Approved: «عالم الـ AI كله في فيديو واحد» rough cut v11 (2026-11-24, 27:24, 16:9), after 11 versions and ~200 review notes
(sheets `projects/2026-11-20 avatar aiFullVideoCost/review_rough_v2..v10_notes.md`). Aly: «دي تكون النسخة الاخيرة» -> approved, «save knowledge and the new style».
Style card: `styles/27 ai-world-explainer/` (sample.mp4, cover.jpg, اقرأني.txt). Scripts archived in `tools/recipes/aiworld/`.
Related: docs/33 (avatar mode, HeyGen / ElevenLabs / Higgsfield rules), docs/34 (hybrid AI reel), docs/22 (enta kit used for the boards).

## 1. What it looks like (the approved look)
- Aly is NOT on camera: picture + voice = his HeyGen digital twin (look S4g «Nefertari stars + Cairo mashrabiya» studio, Avatar 6 Turbo,
  motion «less», reference twin look). Full-frame twin clips at the start / key moments; a TALKING CIRCLE (top-left, x250 y270 r110, face
  centred with MediaPipe) during long explanations. His face is shown in ONE place at a time.
- Families -> sub-parts. Every sub-part opens with a SEPARATOR: the whole video's tree (TreeMap), done parts ✓ dimmed, the next one lit with
  an arrow; KIDS shout its name (6 different ElevenLabs takes mixed with a small random spread + a cheer after — never pitch/delay copies).
- Top breadcrumb «family › sub» always. Background: one star field on video time (navy + gold asterisks).
- Boards (enta kit `Item` + V-series nodes/edges): ONE clear explaining visual per SENTENCE, each item entering on its WORD:
  logo of each tool named, REAL picture / clip (with «المصدر» tag for web clips), diagrams with arrows (step boards, before/after, «one
  original on top + variants under it» (the v2v layout he loved), loops), counters, typed code / prompts, browser pages that scroll.
- Examples: EXPLAIN first (idea -> steps: folder, prompt, code, libraries, output files) -> «تعالوا نسمع/نشوف النتيجة» -> the RESULT alone
  in its own hold, labelled, with its waveform / picture. A result out of nowhere looks like a mistake (v10 note 3).
- Concepts before names (library names change by year/language; show Transcript / OCR / TTS with tiny visuals).
- Captions = the script on word times (not over the song). English-only lines are drawn LTR; mixed lines start with Arabic;
  never a lone «و» between two English words (it reads «g») -> «،».
- Ending: the song (Suno, one generated shot per line, static faint logo watermarks in 5 places, centre one .012), summary map with his
  talking face, «الـ AI مش ساحر» (5 days, skills trained before, Ali's knowledge, >10 versions), CTA with his REAL photo «ده أنا».
- The bill board: numbers read from the accounts (HeyGen / Higgsfield / ElevenLabs / Suno), plan prices from the pricing pages, Arabic-first
  lines, logo beside its line, a 3 s silent hold to read it.

## 2. Hard rules learned (each one cost a version)
1. OVERLAP LAW: nothing overlaps anything on screen at the same moment, all inside the safe area (x 96–1824, y 110–925). The checker's boxes
   must be MEASURED on a rendered still (text pill height = 1.55*size + 22 px) — an unmeasured model printed «0» on a stack of cards.
   Grids move as ONE block. Fillers / picture walls are random by design -> never.
2. REVIEW NOTES LAW: every note into `review_rough_vN_notes.md` as he says it; no new version until all ✓; ✓ only with INDEPENDENT proof
   (a still at its exact time, real-audio Whisper word times) — never the data file that produced it.
3. «On its word» = the REAL audio: Whisper word timestamps on the voice stem (`whisper_words_v11.py` + `words_real_v11.py`; the script order
   can differ from what was said). Word lists must be TIME-sorted (an unsorted list made items fall back to the board start).
4. Lip sync: avatar clips line up by their OWN SOUND (cross-correlate the clip's audio with the voice), not a mouth-vs-voice measure
   (it said +400 ms on a clip that was perfect). Generated copies without audio: compare their mouth with the original's mouth.
   Batch circles: place parts by SENTENCE IDS and add each line's trimmed leading silence (file piece `a`) to the skip.
   Never ask a clip past its last frame (frozen picture).
5. No blank stretch: a hold needs a board that lasts through it; empty/near-empty scenes are filled by the neighbour board.
6. What enters inside a group's time leaves WITH the group. Separators find their part by NAME; no board covers a separator.
7. PDF / screenshot pictures: dedupe by image content (perceptual hash) — the same thumbnail sits on several pages.
8. Paid generation: say the credit cost first, shortest test first, never auto-regenerate; log every job id (`assets/ai/heygen/v9/jobs_v9.md`).

## 3. Pipeline (v11 scripts, run from the project folder; archived in tools/recipes/aiworld/)
1. `make_timeline_v11.py`: pieces (v2 source voice pieces / re-voiced or new twin lines as file pieces / kids separators / holds) ->
   `work/timeline_v11.json`, `output/audio_stems_v11/voice_full_timeline.wav`, voice envelope. HOLD_AFTER = silent holds after lines that
   need reading time (examples, bill, results).
2. `words_v11_files.py` -> script words on times; `whisper_words_v11.py` + `words_real_v11.py` -> `work/words_v11_real.json` (REAL times)
   and `name_time()` for logos.
3. `v11_new.py` = all older specs (v5…v10, moved through the SOURCE seconds — `v10_new.py` with AIW_TIMELINE / AIW_WORDS env) + this
   version's boards (`spec11`, `drop_range` keeps items outside the new range) + general passes (group exit, logo snap).
4. `make_props_v11.py` -> `work/props_v11.json`: items, faces (two HeyGen batches by sentence ids), one-face rule, lip fix by clip sound,
   blank fill, `v11_resolve.resolve_all` (measured boxes, grids as blocks), Arabic/English text rules, bill wave env.
   Gates: `check_overlap_v11.py work/props_v11.json` must print «0 issues»; «words NOT found» must be [].
5. `make_sfx_v11.py` -> sfx stem + `mix_rough_v11.wav` (kids -3 dB, cash on prices, whoosh on separators, audiobook result).
6. Still checks BEFORE render: `stills_v11*.sh` (one Remotion still per note time, sheets of 12) — look at every one.
7. `redo_v11.py` (reuse old frames ONLY where the seconds are identical: the star background runs on video time) -> `render_v11.sh`
   (pieces ≤ 9000 frames, frame-count check, decode + concat FILTER, handles, mix). Bundle with TEMP on D: (never C:).
8. QA on the FINAL file: `qa_v11.py` (black / freeze — freezes only on separators/holds — and lip windows), circle audio vs voice
   (all ≤ 20 ms), full-frame clips vs their originals, `qa_audio_v11.py` (Whisper hear-check of kids, new lines, results, CTA),
   PSNR of final vs pieces at ±1 frame (alignment).
9. Deliverables: ONE video (no clean / Premiere copy unless asked), `<video>.txt` (العناوين / الوصف with chapters from the separator times +
   sources + one hashtag line / الكومنت المثبت), thumbnail (`make_thumbnail_v11.py`: his REAL twin frame cut out with tools/matte.py --png,
   HTML -> headless Chrome screenshot, big Arabic text high, tool logos on an oval, no overlap) = the LAYOUT DRAFT; Aly prefers the final from
   Higgsfield (gpt_image_2_6, 16:9, 2k, high, 4 credits / 2 images) with the draft + his real cut-out face as references and «keep the man exactly
   as in reference 2»; compare face crops with the reference before sending (output/thumbnail_v11_hf_1/2.jpg).

## 4. Generation notes (avatar mode)
- New twin lines: ONE HeyGen TTS request for all lines (voice 68fd7b29…, `withTimestamps`), split by the character timestamps, Whisper-check
  each line; then ONE avatar video for all lines joined with 0.4 s gaps (S4g look f1f77fad…, reference twin c7e371d6…, Avatar 6 Turbo,
  motion less, 1080p) + a parts map (sids, avatar_in, dur). v11: 15 lines, 113 s = 39 credits.
- Kids separators: 3 ElevenLabs kid voices × 2 takes of all names in one text, split by silence (`kids_split_v10.py`), grouped
  (`kids_group_v10.py`); let Aly hear ONE name before making all.
- Real material first (his PDF, recordings, screenshots, official pages); generated pictures only where nothing real exists.
