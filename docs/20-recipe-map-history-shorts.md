# Recipe: history MAP shorts (cairohistory, 2026-10-09) — look 'cairo'

Job: `projects/2026-10-09 shorts cairohistory` — his video "خريطة القاهرة" (Vd0NUtDsUfk, 24 min, Google Earth screen recording,
him keyed small in the bottom-right corner; green-screen intro 0–62 s) → I proposed 9 short ideas, built 1 (summary: the city
builds era by era), 3 (Port Said street was a canal), 2 (Zamalek didn't exist), 9 (seat of power moved 7 times), then ALL the rest
(4 first 3 capitals as characters, 5 Fatimid walled city + gates, 6 Saladin wall/citadel/aqueduct, 7 Piri Reis upside-down map, 8 Baibars
mosque outside the walls). APPROVED = v2 of 4/5/6 (style 07): motion "ممتاز جدا جدا جدا جدا", layout "ممتاز".
Aly's brief: maps EXACTLY as he drew them ("زي ما انا راسمها بالظبط"), creative motion, his face sometimes yes sometimes no.
Refs he sent (sheets in `references/style-sheets/cairo/`, made with `tools/ref_sheet.py <out.jpg> <url> [sec ...]`, no download):
Paris 3D timelapse (city growth + big year), countryballs (cities as characters), Crash Course (flat warm drawings),
Yom-Kippur 3D table map, Constantinople short (old maps on paper), mapcontentstudio reel (pins + photo cards).

## His map = his KMZ files (never draw by eye)
`E:/root/output/GoogleEarth/مصر الاسلامية2.kmz` (+ ALL.kmz for Abdeen/Baibars/Sultan Hassan/Azhar). Copied to `assets/kmz/`.
`work/scripts/build_map.py` → `motion-library/src/cairo/data.json`: his layers (metres around 31.245E 30.05N), today's Nile from OSM
bank lines (Overpass `maps.mail.ru` mirror worked; rasterize banks → components touching top/bottom = water, Dahab island
excluded by hand), main roads (OSM), Egypt region (Natural Earth 10m land/rivers/lakes + approximate ancient canals), and
generated houses INSIDE his polygons per era, Mamluk suburbs, modern blocks, fields, palms.
His "Untitled Polygon" = العسكر. His "شط النيل قديما" is the east-bank strip; for "Zamalek didn't exist" the islands (except
Roda) are also flooded in the old-Nile layer.

## Engine: `src/cairo/map.tsx` (scene 'cmap', ONE back scene for the whole short)
Props (seconds): `cam` keyframes {t, x,y | at:place, s px/m, tilt, rot} (zoom is geometric → region ↔ city fly-ins),
`ev` layer events {l, at, out?, d?} (oldnile, fields, khalij, fustat/askar/qatai/fatimid/mamluk (houses rise from the
centre), fwall, swall, citadel, aqueduct, modern (grows outward + built-up ground), roads, focus_<city>, focus_oldnile,
canal_sesostris/roman/amr, boat_*, ismailia), `labels` (HTML pins, red = historical), `icons` (mosque/spiral/fort/gate/palace/
citadel), `years` (big counter + era tag), `balls` (countryball cities, mood squeeze/angry), `seats` (crown hopping, numbered).
Overlays `src/cairo/scenes.tsx`: ct (title), cpaper (his old map crop on taped paper + red circle), cchip (✓/✗ chip).
His face: 'big' cut-out from the green intro (matte), 'bubble'/'bubble-r' = round webcam clip (`make_cams.py`).

## Pipeline
fetch → transcribe (prompt = place names) → contact sheets → `build_map.py` → `make_cams.py` → old-map crops (`work/maps`) →
`make_shorts.py` (SPANS + MAP + FRONT + ALY, all in SOURCE seconds) → still sheet every ~4 s → `render.sh` (temp on E:) →
`write_meta.py`, `export_sfx.py`, voice stems. Scripts archived in `tools/recipes/cairohistory/`.

## Gotchas
- PIL draws Arabic unshaped (Aly saw a debug png and thought the video's Arabic was broken) — never show him PIL Arabic.
- cam keyframes use key `at` for a place name → only convert `t` for cam.
- Overpass main servers 504/406 — mail.ru mirror; Natural Earth from GitHub raw.

## His face (review 2026-10-09/10) — the approved layout
- v1 (round webcam at a few moments) → "عايز اكون في الفيديو اكتر". v2 big roto cut-out the whole short → "متحطنيش كبير اوي كدا طول
  الفيديو". APPROVED: big cut-out ('anchor', roto) in the OPENING piece only, then the small round webcam bubble (plain crop
  `camr_<start>.mp4` from `cam_ranges.py`, his screen visible behind him — "حلوة للخرايط") for EVERY following piece, windows touching
  edge to edge (ain/aout false = no pop between pieces); map `cx 0.6, cy 0.5` so the action stays away from the bubble (bottom-left).
- His corner in the screen recording is fixed from 80 s to the end: crop 450 @ (1381, 630) for the bubble, 470 @ (1385, 612) for roto
  (`roto_all.py`, RVM ≈ 30 min for 9.5 min of pieces). Roto: `clipL 0.3` hides the mouse hand; face from alpha (`alpha_pos`).
- Run: `python work/scripts/make_shorts.py 4 5 6 7 8` (roto all) or `V=v2 python … 4 5 6` (approved bubble layout) →
  `V=v2 sh work/scripts/render.sh 4 5 6` → output/v2/. New public files need `rm -rf out/bundle`.

## More gotchas
- Old wide Nile ('oldnile') only up to the Ayyubids (he says it shrank then) — never in Mamluk/Ottoman scenes (`base(..., nile=False)`).
- Windows for his face must be the fitted piece (segs), not word times — word times leave 0.2–0.6 s holes (he vanished in short 9).
- Labels with explicit positions: place '@x,y' (metres). Keep east/west labels inside ±2500 m of the camera x.
