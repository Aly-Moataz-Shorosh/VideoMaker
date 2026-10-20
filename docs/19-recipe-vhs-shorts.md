# Recipe: faceless-first shorts, VHS look (vhstodigital, 2026-10-09) — style 06

Job: `projects/2026-10-09 shorts vhstodigital` — his 2023 YouTube video "VHS لـ Digital" (16 min, fetched with yt-dlp)
→ I proposed 8 short ideas, he picked 4 (1 his way + EasyCap summary, 2 price 30→300, 4 EasyCap vs his way, 8 nostalgia).
Aly approved v2: "زي الفل". Same engine as style 04 (docs/18): composition `film-short`, prop `look: 'vhs'`.
Scripts: `tools/recipes/vhstodigital/` (copy to `<project>/work/scripts/`, change SRC / SPANS / SHORTS).

## Pipeline
1. `tools/fetch.py <url> projects/<p>` (now with `--js-runtimes node -N 4`; without a JS runtime YouTube throttles to ~100 KB/s).
2. `tools/transcribe.py input/<id>.mp4 work --prompt "VHS, EasyCap, OBS Studio, HDMI, USB, AV, Hi8, Capture Card"`.
   `work/scripts/words.py S001-S010` prints words with start times (to pick spans).
3. Real footage: 2 contact sheets of the whole video (`fps=1/8, tile=8x8` — NOTE the drawtext label there is frame×64,
   real second = label/8), then crop the useful parts into small clips in `public/projects/<p>/` (ffmpeg crop+scale 720p).
   Check each crop with a 1/3 s tile strip (layouts move inside screen recordings).
4. `faces.py` → his cut-outs (desk shots only; square crop round the haar face, `tools/matte.py`). If haar misses
   (`faceW 0`), try `haarcascade_frontalface_alt2` and write face/faceW into faces.json by hand — alpha_pos is fooled by hands/mic.
5. `make_shorts.py` → `short_<n>.json`: SPANS = (first word start, last word start) per piece; `edges.py` fits every edge on
   the WAVEFORM; captions = exactly the words of the spans (`KEEP`); `fix.json` spelling; `partial` for cut sentences;
   `level_voice.py` writes `voice_<n>.wav` (pieces + CTA, per-sentence gain, -15 LUFS) → props `segs` = one piece, `ctaVol` 0.
   Tiny holes between scenes (< 0.6 s) are closed automatically.
6. `check.sh <n>` (2 stills per scene) → `render.sh 1 2 4 8` → verify duration, -15 LUFS, LRA ≤ 2.5, CTA frame.
7. Deliverables: `write_meta.py` (txt beside each short), `export_sfx.py` (sfx stems), `output/voice/` (= voice_<n>.wav).
   NO Word script unless he asks.

## Aly's review of v1 (all fixed in v2)
- Words clipped at piece ends ("لديجيتال", "لتلتمية", "USB", "خالص"): Whisper ends are off by ~0.3 s and a stop consonant
  inside a word looks like a dip → `edges.py` (walk to 150 ms of real quiet + 80 ms, never into the next word; tight jump
  cut → deepest dip before the next word). Print every edge with its dB.
- Short 8 started on the tail of the cold open: speech starts at 0.95 s, Whisper said 1.54.
- Voice level jumped between pieces ("كل مشهد تحسه متسجل في يوم") → `level_voice.py` (gain only).
- He does NOT want voice cleanup unless he asks (I had run the podcast chain by default — wrong).
- Short 1: don't stack two hook sentences; when he summarizes BOTH ways at the end, use the summary.
- Short 2: show WHY it is costly (tapes pop one by one, "300" each, total 10 × 300 = 3,000).
- Short 8: wrong caption on his sketch (it is "مش قلتلك هيقعوا؟ لو وقعوا وراحوا مالهمش نسخ تانية") — re-transcribe unclear
  lines with a hint prompt; real footage of him talking = big 16:9 card, not a small TV.

## Code
- `src/vhs/kit.tsx`: palette V (CRT black-blue, VCR blue #1F33E8, RCA red/white/yellow, magenta/cyan fringe), VhsBg (glow +
  retro grid), VhsFx (scanlines, rolling tracking band, glitch, PLAY + timecode OSD), Rgb text, BluePanel, Crt, Footage,
  Cassette, SmallTape (Hi8), Vcr, RcaPlug, Cable (draws + signal flow), Box (converter / capture card), Laptop, Chip.
- `src/vhs/v1|v2|v4|v8.tsx` scenes, `scenes.ts` registry (merged into film-short's scene map). Generic: `vt` (title behind
  him + stamp), `v1_chain` (whole signal chain built on beats), `v8_save` (tape → .MP4), `v1_end` (3 icon cards).
- film kit `Title`: `*word*…` now works (ellipsis after a marker).
