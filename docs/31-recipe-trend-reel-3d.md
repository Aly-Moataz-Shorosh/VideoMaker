# Recipe 31 — trend reel with his face + 3D (style 19, livematchligo 2026-11-01, APPROVED v3 "ممتاز")

Job: `projects/2026-11-01 reel-h livematchligo` — his 9:16 phone talk (91.8 s) about Bayern–Dortmund 2-2 shown LIVE as Playmobil
figures (MBC3 in Arabic, Sky/RTL+ in Germany). No notes (urgent). Composition `match-reel` (`motion-library/src/match/`).
Scripts: `tools/recipes/livematch/` (`clips.sh` cuts the match clips, `make_props.py` = words + cues + zoom + sfx + amp).

## What he asked (and what the look is)
- Face on screen most/all of the video, zoom in/out, a visual on EVERY word (net picture / clip / logo / motion), text behind him.
- Mix of his styles + a small Vox touch in our animation: paper cards (white border, tape, grain), yellow marker strokes, red stamps,
  hand-drawn circles, dotted maps. Cards live in the tray under his face (y 1210–1670), captions at 1090.
- Text BEHIND him: whole-video matte (`tools/matte.py ... 0 <dur> roto.webm --fps 30`, 2.4 fps ≈ 19 min, start it first);
  the roto is decoded ONLY while a behind-text cue is up (speed).
- Hook: many shots AT ONCE ("كلهم parallel") = 3×2 grid of tiles popping in (ClipCard `grid`), + channel logo + "✗ مش AI / ✗ مش لعبة".
- Real vs Playmobil: full split (real top, Playmobil bottom, face bubble) — the SAME moment from the SAME camera view. Align by the
  score-bug clock: tile the bug once per second for both highlight videos (`crop` + `drawtext t` + `tile`), then fine-tune by the
  goal moment (the Playmobil clock lagged ~4 s; goal graphics differ by ~1 s).
- 3D (`fig3d.tsx`, three.js): 21-point skeleton running (FK cycle) with a counter + groups lit on his words; Playmobil body that pops
  onto the bones; Aly as a Playmobil REPORTER (his crimson shirt + white collar, hair piece, beard, mic, mouth from the voice RMS
  `amp[]`, LIVE bug, one-line name strap). Films' motion capture = a full-screen free Pexels clip (credited), not a photo.
- Puppet picture on "عروسة/العرايس" = his 2020 Character Animator thumbnail (him holding a puppet), small in a free corner, the
  label BESIDE it as a solid yellow one-line box.
- End: his old video (thumb + QR + the note he dictated), follow, poll question.

## Copyright (he wants the clips but no claims)
Short pieces (≤ ~6 s), mirrored (hflip — never mirror clips with numbers/text), score bug + watermark cropped, smaller than the
screen inside paper frames, MUTED, "المصدر: Bundesliga — مقاطع قصيرة للمراجعة" on screen. Said honestly: nothing guarantees no claim.
The MBC3 Arabic-commentary pause after the hook was dropped (TikTok refused downloads; impersonation is blocked) — he allowed it.

## Gotchas
- **3D canvas band (v1/v2 bug)**: any DOM layer over a big ThreeCanvas (the name strap) made Chrome drop a band of the canvas —
  his mouth vanished in the render while 0.35-scale stills looked fine. Draw the 3D canvas LAST with nothing over it, and check 3D
  stills at SCALE=1.
- Playmobil hair back piece: CylinderGeometry theta 0 = +z (front) — the gap must be centred on the front.
- Redo = render only the changed frame ranges (in parallel, `--frames=a-b`, own TEMP each, `--timeout=240000` when 5 run at once)
  and splice into the previous version with ffmpeg trims (video only, audio copied) → check frames at every seam vs the old version.
- yt-dlp needs `--js-runtimes node`; Pexels pages need the browser (Cloudflare) — read the mp4 URLs from the page, then curl.
- Facts on screen were checked: EA agreed to buy TRACAB (3 Feb 2025), 21-point skeleton (Sportec/Bundesliga), Sky/RTL+ feed.
