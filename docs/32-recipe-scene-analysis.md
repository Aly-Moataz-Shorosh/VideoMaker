# Recipe 32 — Film scene analysis (16:9), "from the script to the screen"

First job: `projects/2026-11-06 youtube sceneAnalysis ibrahimLabyad` (Ibrahim El Abyad 2009, sc 55/56, OBS recording 4:02).
Composition `scene-analysis` (`motion-library/src/scene/`), scripts `tools/recipes/ibrahimLabyad/`.

## Aly's rules for this format (PROMPT.md + reviews)
- The scene plays WHOLE, untouched (picture and sound). Sound = the input's AAC muxed with `-c:a copy` after a muted render.
- Priority: Editing > Sound Design > Camera. Lighting / Acting = one NOTE line only.
- ALL terms in English. Every abbreviation gets its full name under it (LS = Long Shot, OTS = Over-the-Shoulder; Aly 2026-11-06:
  "حد تاني ميعرفش"). ASL / SFX / V.O. spelled out in the card title.
- Every term in the shot label gets a DRAWING (SizeGlyph = framed person per size, MoveGlyph = looping mini animation per move).
- ONE place per thing, nothing repeated: film RIGHT (Arabic eye starts right), script LEFT (SOUND window + PICTURE window on the real
  PDF pages), card strip under the film (3 kinds only), colour legend under the script, Premiere timeline at the bottom.
- J-Cut / Sound Bridge / Fade must be visible in sound AND picture: A-clip starts before the V-cut, dashed lines + "3.7 s" label.
- Script sync on the WORD: re-transcribe windows with the script text as prompt (A) and without (B), compare; refine starts on the audio level.
  Show every film ≠ script difference (chip FILM ≠ SCRIPT). Not in script = grey.
- Camera facts: only sure things (film stock, DoP). Gear "من شكل الصورة". Definitions = StudioBinder.
- Unsure items → ONE question with the whole list; 4–5 stills before the full render.

## Steps
1. `cuts.py` (frame diff + histogram) → every candidate cut not in the old list, `strip.py` frames around each → `shots_v4.json`.
   The old 88-shot list missed 10 cuts (whip-pan shots, jump cuts in a top shot). 30 fps from a 25 fps film = every 6th diff is 0.
2. `contact.py` sheets (5 frames per shot) + `motion_v4.py` optical flow → label size / move / angle per shot BY EYE.
3. `retr.py` per-window transcription, `make_props.py` (shots, lines with PDF rects in pt, pictures, cards, marks, markers, audio clips).
4. Page images at 216 dpi (3 px / pt) in public/projects/<code>/ ; `make_sss.py` = Shot → Scene → Sequence board (HTML + PNG via Playwright).
5. Stills → Aly → render muted (`--concurrency=6`, TEMP in out/tmp) → mux original audio → check length / loudness.

## Gotchas
- Mixed Arabic + English in one line flips brackets: put the English part in the TITLE, keep the Arabic line Arabic; in HTML use <bdi>.
- Markers closer than ~1 s overlap on the timeline → merge them ("Hidden Cut → Cross-Cutting").
