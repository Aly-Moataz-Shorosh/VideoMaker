# Recipe: faceless-first shorts from a long video (theodesy, 2026-10-08)

Job: `projects/2026-10-08 shorts theodesy` — his 17:18 YouTube video "حكاية الفيلم" → 10 self-contained vertical shorts.
Aly's brief: the whole short = creative motion graphics / animated infographics (learn from his reference shorts:
collage, cut-out B&W photos, paper + grain, red marker scribbles, maps with characters, light beams); real footage
only when showing how a real thing looks; his cut-out appears only at a few moments (start / middle / end); every
short ends with his comment-keyword CTA; no Claude colours; "wow", not basic moves. Plan + scripts: `work/shorts_plan.md`.

## Pipeline (all in work/scripts)
1. `transcribe.py final.mp4` → transcript; `snap_ranges.py` → `ranges.json` (edges on audio dips; manual overrides in make_shorts.py).
2. `clean_voice.py <car_end_sec>` → `voice.m4a`: noisereduce (stationary) on the CAR part only (engine noise), loudnorm.
   (DeepFilterNet needs Rust on py3.13 → not installable; ffmpeg afftdn too weak.)
3. `faces.py` → his face moments cut from the RAW clips (no overlays): audio cross-correlation finds the raw clip +
   offset; raw clips are HLG HDR → tonemap hable; CAR clips get an auto grade (black/white points, gamma, sat 1.35 —
   Aly: car shots looked washed out next to home shots); square crop → `tools/matte.py` → `aly_<n>_<k>.webm`.
4. `make_shorts.py` → `public/projects/<code>/short_<n>.json` for composition `film-short` (src/film/FilmShort.tsx):
   scenes per short = tuples (id, src start, src end, layer back|front, props, beats{name: src sec}); Aly windows;
   caption fixes `work/fix.json` + per-short `partial`; CTA clip + comment_cta; whoosh/pop sfx.
5. `check.sh <n>` → 2 stills per scene; `render.sh <n...>` → `output/short_<n>.mp4` (one bundle, temp on C: deleted per short).

## Audio (Aly's review: animation "ممتاز ممتاز ممتاز", audio "وحش اوي، مش بودكاست، واطي وبعيد، مفيش sound effects")
- `podcast_voice.py`: dns64 denoise (cached `voice_dns16.npy`) → 48 kHz with gated original highs → EQ + de-ess + 2
  compressors → loudnorm −12 LUFS. Result: car + home parts at the same level, final shorts −12.3 LUFS, LRA 2.4.
- `tools/make_sfx.py` → 39 synthesized effects in `motion-library/public/sfx`; `sfx_plan.py` per-scene specials;
  make_shorts adds whoosh/swish/pop/impact/CTA sounds; `sfxGain` 1.6 in the props. CTA audio → `cta_podcast.mp4`.

## v3 = AI voice (Aly: "خد الكلام بس وخلي الـ AI يقوله بصوت نضيف… قريب من صوتي"; may talk faster, "مش سريع اوي")
- `ai_voice.py`: phrases from his caption words → Edge TTS `ar-EG-ShakirNeural` (free, rate +0%) → OpenVoice V2
  tone-colour converter (MIT, local; checkpoint ~/ai-models/openvoice-v2; reference = 60 s of the raw home clip,
  `work/tts/aly_se.pth`) → polish −12 LUFS. Voiceprint similarity to Aly 0.84 (plain TTS 0.45, his own 0.92).
- The SHORT is re-timed to the voice (no stretching): piecewise-linear old→new map moves scenes, beats, captions, sfx;
  his cut-out windows get `rate` (playbackRate). Shorts got ×1.03–1.30 faster. Output `output/v3/`, props `short_<n>_v3.json`.
- OpenVoice's ToneColorConverter(enable_watermark=False) crashes → build via OpenVoiceBaseClass.__init__ (see script).
- New public files need a fresh bundle (`rm -rf out/bundle`) or the render fails with readFile.

## v4 = his cut-out the WHOLE short (Aly 2026-10-09, short 2 only, then he closed the job)
- `faces_full.py`: rebuilds his edit from the RAW clips: 0.5 s windows located by audio correlation (fast check at the
  predicted offset first), jump cuts refined to 20 ms, unmatched bits hold the previous piece; tonemap + ONE grade per
  car clip; fixed 1080 crop per clip; joined → matte (~5 min per 45 s). `make_v4.py`: layout 'v4' (front scenes shrink
  to a 0.72 screen card at the top, he stays below over everything, disc behind his head, captions on his chest),
  ORIGINAL untouched voice (`voice_original.m4a` = audio stream copy of final.mp4), original CTA clip at ctaVol 0.75,
  sfxGain 0.9 (raw voice ≈ −16.7 dB mean vs −12 processed).

## Deliverables at the end of a job (he asked for each of these)
- `export_sfx.py` → sfx-only WAV stems per short (same length/timing as the video), for v2 and v3 timings.
- original voice per short (`output/voice_original/`, his edit's audio as is + CTA) and the full video audio.
- the spoken script as Word (`script_to_word.js`, RTL Arabic, one page per short).
- `write_meta.py` → `<video>.txt` beside every video: 3 titles, description (+ keyword CTA), hashtags, pinned comment.
- All scripts of this job are archived in `tools/recipes/theodesy/`.

## Code
- `src/film/kit.tsx` darkroom collage kit (FilmBg, FilmFx grain/dust/flicker, Paper torn edges, Photo, Clip, Title with
  *yellow* / _red box_ highlights (multi-word OK), Tag, Stamp, Scribble, Beam, Strip, Count, Pop, Scene).
- `src/film/draw.tsx` engraved SVG drawings (Eye, Sun, Pyramid, Palm, Brain, Runner, Obscura, CrankCamera).
- `src/film/s01..s10.tsx` scenes per short, mapped in `src/film/scenes.ts`.
- Palette: ink #0E0D0C, paper #E4E2DC, safelight red #E5232B, Kodak yellow #FFC21A, cyan #3FC7DA (pack `darkroom`).

## Gotchas
- Haar misses him in the car (wide frame) → crop fallback x 0.46 there; head position from haar when found, else alpha.
- Energy normalisation with np.convolve over a 10-min clip took minutes and looked like a hang → cumulative sum.
- Whisper word times can sit inside a range edge (e.g. 'نكمل') → `partial: {id: ''}` drops it.
- Parked old projects out of `public/` (`motion-library/_parked_public/`) so every bundle copies ~400 MB, not 2 GB.
