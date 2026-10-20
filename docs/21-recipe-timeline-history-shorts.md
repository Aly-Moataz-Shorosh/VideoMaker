# Recipe: TIMELINE history shorts (historyOfGraphics, 2026-10-10) — look 'hist'

Job: `projects/2026-10-10 shorts historyOfGraphics` — his video "تاريخ الجرافيكس" (cdkvUAgSoKc, 12:25, him talking in front of a teal
cloth, small picture/video inserts top-right at crop 508x284 @ (1335,116)). I proposed 9 ideas (the count = what the video holds, never
a fixed number — Aly asked), built the best 5 first, then the rest (1, 2, 6, 8). APPROVED as style 08
("الجودة حلوة اوي اوي اوي ممتاز"). His only note: short 1's music (`curious_mind`) was too busy → calm tracks only.
First 5: 3 fear of death invented writing, 4 dead sciences / pyramids, 5 stone → paper →
printing, 7 the main skill of every era, 9 the whole history in one minute.

## Aly's brief
- ONE-SHOT motion graphics for the whole short along a TIMELINE: old on the LEFT, new on the RIGHT; the camera walks left → right
  while he explains, slows / stops on an era for effects, zooms in / out, then walks on.
- His face the whole short in a SMALL CIRCLE; only the opening is a BIG CIRCLE (not a cut-out!). Never cover the motion.
- Real pictures / his video inserts (temples, printing…) + more from the internet = very small circles next to the drawing.
- Nice music + sound effects. Drawing style = his references (studied as frame sheets in `references/style-sheets/graphics/`):
  Ancient Egyptian Kit + Egyptian Stories opener (flat geometric, ochre/plum/terracotta, paper grain, side-scrolling camera with a
  blurred foreground passing), Mazepa (painted landscape pan), Tamim/AJ+ (continuous travelling floor), Russia infographic (round photo
  circles). Behance pages: pictures via JS `img` list, VIDEOS via the Vimeo player page (`window.playerConfig.request.files.progressive`)
  → `vsheet` frames with ffmpeg seeking (no download). He asked me to watch the videos, not only the pictures.

## Engine `motion-library/src/hist/`
- `pal.ts` palette `H`, sky colours along x (dawn caves → bright Egypt → dusk Baghdad → blue modern), stations `ST` (world x + year):
  speech 600, village 1450, cave 2350, sumer 3450, egypt 4550, pyramids 5650, china 6750, rome 7800, paper 8900, baghdad 10050,
  press 11250, computer 12400, now 13600.
- `stations.tsx` one flat drawing per era with actions on events (`{s, k, at}`): speech chain/lost/talk, village talk/fade, cave
  paint/hands, sumer cune, egypt hiero/carve, pyramids q/ramp1/ramp2/x1/x2/crane, china bamboo, rome latin, paper book/sheets/pigeon/ship,
  baghdad lib/burn/ink, press press/copies, computer type/web, now video/icons/world (drawn flags — emoji flags don't render).
- `people.tsx` flat people (acts idle/talk/paint/chisel/read/write/point/pull/type/cheer, hats egypt/turban/roman/cap/fur), fire, bubbles.
- `world.tsx` scene `hworld` (back layer, whole short): cam `{t,x,z}` keyframes (eased, tiny drift = never frozen; zoomed out → world
  lifted), far layer (dunes, far pyramids, far city, parallax .35), ground + RULER with years + soil strata with buried things,
  foreground columns/palms ONLY half-way between eras and only while the camera moves (= wipe), air (dust, triangles, birds),
  `pics` (screen-sized circles anchored to world points, his clips loop / photos Ken-Burns, label), `words` (big kinetic words, y .25),
  `era` (HUD card + year), `meters` (3 criteria bars: سرعة الانتشار / الجهد / البقاء, ▲▼), `bursts` (rays + ring), grain + vignette.
- FilmShort: `look: 'hist'`, his face modes `bubble-big` (560 px, centre, opening; shrinks into the small one in its last 14 frames)
  and `bubble-s` (290 px bottom-left at 0.83 H, under the captions), `music` prop (vol, lower under the CTA). Captions `capBottom .175`
  (between the ruler and his circle).

## Pipeline (`work/scripts/`, archived in `tools/recipes/historyOfGraphics/`)
fetch → transcribe → contact sheet + insert crops (`clips/*.mp4` from his inserts) → Commons pictures (API search, 900 px thumbs,
credits in `assets/pics_credits.txt`, slow down on HTTP 429) → Pixabay music WITHOUT "Content ID Registered" (fetch the track pages,
skip registered ones) → `make_shorts.py` (SPANS / BIG / MUSIC / PLAN per short in SOURCE seconds; webcam = plain crop 600 @ (610,100)
per kept range) → stills (`stills_cli.sh`, frames every ~4 s) → `render.sh` → `write_meta.py`, `export_sfx.py`.

## Gotchas
- Two kept pieces whose source ranges touch (hook 283.6–289.1 then 289.0–319): an event at 289.04 maps into the FIRST piece →
  the camera jumped. Put events of a piece inside its own range (+0.2 s).
- Far overviews (z < 0.35) made the eras tiny under an empty sky → use z ≥ 0.36 + lift, and for "these 4 scripts" pan
  left → right at z 0.6 instead of one far overview. A list that runs backwards in time (hard disk → print → wall → rock) = circles
  around the current era, don't walk the camera backwards.
- A clip whose insert window starts on a transition shows an empty teal frame → trim 0.5 s inside.
