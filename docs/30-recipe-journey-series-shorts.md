# Recipe: "رحلة إلى مركز الجرافيكس" → series of shorts (2026-10-22, pilot 8 / 33 / 44 — waiting for Aly's review)

Job: `projects/2026-10-22 shorts Journey to the center of computer graphics` — his whole playlist (37 videos, fetched with yt-dlp):
01 intro (9:19), 02–31 "هو ايه" (30 terms, ~1 min each), 32–36 "المجالات و ساحر مدينة أوز" (5 chapters), 37 "البرامج" (12:30).
Plan for 48 shorts: `خطة_الشورتس.md` in the project (Aly said "تمام" and picked the pilot: 8 vectors, 33 scarecrow, 44 3D programs).

## Aly's rules for this series (2026-10-22)
- Every short complete on its own, but it must make people want the series: it ends on the NEXT term / next station.
- Series identity on every short: top bar = "رحلة إلى مركز الجرافيكس" + route with 3 stations (his three logos) + label
  ("هو ايه · مصطلح 7 من 30"); bottom = HIS channel logo + name (`pp 2.png` split into face + name).
- End card: playlist thumbnail (= video 01's 1280 thumbnail; the playlist jpg is only 336 px) + name + QR of the PLAYLIST,
  under it the original video's thumbnail WITHOUT QR. No CTA clip.
- Oz chapters: everything DRAWN (Dorothy, scarecrow, road, emerald city) — never the film footage (copyright).
- Calm backgrounds ("مريحة اكتر للعين"): soft flat gradients, no grain, no busy lines.
- Logos = HIS EXACT files ("استخدم اللوجو نفسه مش زيه"), copied (read-only) from
  `F:\_root\output\Youtube\Aly Shorosh NEW\` → project `assets/his/`:
  هو ايه = `هو ايه\LOGO\هو ايه2.png` (356 px: never shown bigger), المجالات badge = `البرامج\logo for video.png`,
  البرامج = `البرامج\البرامج\logo ae.ai` rendered with pymupdf WITHOUT its background layer ("Layer 1") at 400 dpi,
  program logos = `البرامج\البرامج\png logos\` (his tree). Missing there: 3ds Max (cut from his video frame 37@229 s, 128 px,
  shown ≤ 120 px) and Illustrator (Commons CC icon, same family as his Xd/Id icons).
- Stronger drawings + three.js where it helps (`src/journey/three.tsx`): pixel heart = glossy voxels, vector heart = extruded
  bevelled 3D heart, packaging boxes, towers + room (3ds Max), bouncing ball (Maya), cloner wave (Cinema 4D), principles knot.

## His CLEAN voice (no music / no film audio under it)
- هو ايه: `F:\...\Aly Shorosh NEW\هو ايه_\<n>-<term> FIXED.mp3` — one constant offset (vectors: voice_t = video_t − 4.15).
- المجالات: `F:\...\المجالات\_Assets\audio\eN orginal v1.mp3` — the raw take; his edit cut it, so the map is PIECEWISE
  (ep 33: 7 pieces, found with 3 s envelope cross-correlation windows, cut points on the quietest 10 ms near each jump).
- البرامج (37): no clean file found → the video's own audio.
- Map lives in `work/scripts/jy_audio.py` (`VOICE`); `take()` builds the voice of any kept range. QC: 2 s windows of the short's
  voice vs the video audio, all within 30 ms (only the vectors outro window is unsure because his outro music covers it).

## Build (scripts in the project `work/scripts/`, copy in tools/recipes/journey/)
`shorts_data.py` (pieces, scenes with beats in source seconds, caption word fixes `WFIX`) → `make_shorts.py N…` (edges on the
waveform, voice gain only, scenes chained, sfx, props) → `render.sh N…` (one bundle, TEMP inside out/, deleted after) →
`finalize.py N…` (−16 LUFS + limiter, CRF 23, `output/NN_slug.mp4` + `.txt`).
Composition `film-short`, `look: 'journey'`, prop `series {sec, label}`; scenes `src/journey/` (kit, vectors, oz, prog, three, end).
Stage is scaled ×1.1 and moved down 70 px for every journey scene (fills the space between the bar and the captions); captions 0.115.

## Review of the pilot (Aly 2026-10-22) -> v2 (`output/v2/`, v1 kept in `output/v1/`)
Liked: the opening and the end ("البداية و النهاية"), the colours. Notes (all fixed in v2):
- Motion alone is not descriptive enough ("مش مفهوم كفاية"): REAL example pictures on top of the motion, in circles / cards
  on the word (`jy_real` overlay, `src/journey/real.tsx`, data `REAL` in shorts_data.py). Source order he set:
  1) HIS work (F:\_root\output\_portfolio, F:\_root\output\Designs — copies in assets/his/work), 2) crops of HIS video where the
  example is visible around him (`real_images.py` FRAMES), 3) free Commons pictures (`commons.py`, credits -> .txt).
  Never a crop that cuts a face; no alcohol products (dropped a soju box). Real pixels = nearest-neighbour zoom of his photo.
- His work on screen -> "Bē be.net/shorosh" tag under it + "شغلي على Behance: be.net/shorosh" in the description.
- Oz chapters: HE tells the story from a circle (`FaceCircle`): his face matted from the published chapter (crop 720x720 at
  x600 y300 -> tools/matte.py, 6 fps), same timeline as the voice, keeps the drawn characters; circle moves to the free corner per
  scene (`face_pos`). Field drawings shrink to make room for the real card on top.
- Nothing may be cut by a canvas edge ("الكورة كانت بتتقص… الفيديو اكنه وحدة واحدة"): three.js objects stay inside their canvas
  (ball range + height limited, canvas = full stage width). The stage scale ×1.1 widens canvases by 54 px per side — keep margins.

## Review of v2 (Aly 2026-10-22) -> v3 (`output/v3/`)
- هو ايه: HIS OWN episode motion is better ("بيعبر اكتر") -> `jy_clip` = his episode playing in sync, cropped to where his animation
  is (`content_boxes.py`: diff vs the episode's own grey background, 0.25 s steps), scaled ≤ ×1.6 and ≤ 860 px wide (stage ×1.1 ->
  never wider than the screen). My scenes only where they explain more (pixels added/removed, billboard + t-shirt, file size).
- Pixels: show the REAL photo first, then ZOOM into it until the squares show (`jy_zoom`, nearest-neighbour + pixel grid) — not separate
  crops. A drawn landscape is NOT a raster photo; a manipulation is NOT a photograph.
- Behance: a small QR (be.net/shorosh) only next to his strongest works, never a text chip under every picture.
- Nothing may leave the frame (labels of side circles were cut).
- Oz: NO roto — his ORIGINAL frame inside the circle, centred on his face (center 960,690 r 230 of the 1920 frame). Examples = his WHOLE
  chapter frame while he scrolls (not zoomed crops); the field's own motion sits right under that frame, above the captions, never covered.
- Programs: fewer examples, no overlaps (Big Buck Bunny replaces the Blender ball inside the scene).
