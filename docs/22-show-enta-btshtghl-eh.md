# Show: "انت بتشتغل ايه" (What do you do for a living?) — show bible (2026-10-10, before episode 1)

Interview show: Aly + one guest per episode, three departments: **حاسبات (cs)**, **فنون (fnon)** and **رواد الأعمال (biz)** (added 2026-10-27).
Aly hands his EDITED episode → Claude adds motion graphics + captions + sfx + internet pictures/clips that explain
the guest's job, terms and examples. Goal (Aly): fun, visualized, explain every term with an example.

## Files
- Episodes: `projects/انت بتشتغل ايه/<date> epNN <cs|fnon|biz> <guest>/` made by `new-episode.bat` (in that folder; 3 = biz; epNN counts per department).
  notes.txt ends with `dept:` and `intro_in_video: yes|no`.
- Brand copies (sources are READ-ONLY on E:/root/output/Youtube/Aly Shorosh New/انت بتشتغل ايه):
  `brand/enta/intro_cs.mp4`, `intro_fnon.mp4` (17.1 s, 1280x720 25 fps — upscale to the episode size),
  `logo_cs.png` / `logo_fnon.png` (cartoon Aly at desk, speech bubble "حاسبات/فنون — انت بتشتغل ايه", ON AIR, "يقدمه علي معتز شُرُش"),
  `styles_sheet.png` (his element sheet), `thumb_example_*.png`. Contact sheets: `references/style-sheets/enta_*.jpg`.
- Studio = OBS two-camera layout (Aly LEFT, guest RIGHT; also single-focus scenes). Raw ep1 (fnon, Ahmed Moataz) exists on E:.
- Guest questions per department: `اسئلة الضيوف - حاسبات/فنون/بزنس.docx` in the show folder (read for terms).
  biz has 2 question sets: `اسئلة الضيوف - بزنس.docx` (one project: idea -> first client -> his tasks vs hired -> first profit -> hardest
  surprise -> where it is now -> advice) and `اسئلة الضيف - صاحب مشروعين.docx` (two projects: why each started / first client / why
  it stopped). Episode chapters follow these sections (البداية / المشروع / الختام).

## Intro / outro
- `intro_in_video: no` → prepend `brand/enta/intro_<dept>.mp4`. Episode also ENDS with the intro/its logo end
  (Aly: "تبدأ بانترو و تنتهي بانترو") — confirm on the first episode whether the end = same intro or only its logo tail.
- No motion / captions on the intro parts (`plan.quiet`).

## Visual language (from the intros + styles.png + thumbnails)
- Intro = old Egyptian B&W film clips (fez, Islamic-Cairo balcony, woman at the window asking "انت بتشتغل ايه؟"),
  film/movie meme cutaways per department, orange hand-drawn "?!", then a blurred B&W still with the cartoon logo.
- Texture: film grain + dust + vertical scratches, VHS/RGB glitch bars (red/blue), scanlines, warm light leaks
  (orange/red), lens flares, bokeh, burnt-paper edges.
- Stickers (styles.png): flat hand-drawn, white sticker outline, muted palette **orange #E0642E-ish, blue #5C8BC0-ish,
  olive #8E9A5B-ish, mustard #E8B54A-ish** on dark: ?!, burst lines, arrows, masking tape, paint splats,
  `{ }`, 0/1, floppy, bug (cs); film reel, theatre masks, brush, music notes (fnon); ON AIR sign, stars.
- Thumbnails: mixed-media collage, sepia cut-out photos with white border, blue paper speech bubble.
- Department flavour: cs → code, circuits, floppy, bug, 0101; fnon → curtain, film reel, masks, paint drips, notes;
  biz → idea bulb, coins, rising chart, briefcase, rocket (startup), shop; boards = timeline of the project (idea → first client
  → profit → now), team split (his tasks vs hired), numbers only when the guest says them.
- biz intro = `brand/enta/intro_biz.mp4` (copy of Aly's `C:/_working pc/upsampling.mp4`, 2026-10-27; 17.12 s, 1920x1080 25 fps,
  same length as the cs/fnon intros). No separate `logo_biz.png` yet — take the logo end from the intro's tail when needed.

## Motion recipe = mix of all approved styles
- Pacing from the reference (Peace Cake "مرتبة الشرف", 5YLfxDi4tIs): ~70 shot changes in 2 min (one every ~1.7 s):
  wide two-shot → punch-in on the speaker → other person → board graphic. Use virtual camera on his edit:
  punch-in/out on each speaker turn, reframe to the single speaker, quick push on a joke. Never > ~5 s without a change.
- Every term → explainer card (sticker style) + example; every tool/place/person → picture/logo from the internet
  (Wikimedia / official logos), photos as sepia/colour cut-outs with white border (thumbnail look).
- Old film meme cutaways (like the intro) for reactions — only short, from free/archival sources.
- Captions always on (LTR groups for English terms).
- SFX on every pop/whoosh/glitch (`tools/make_sfx.py`, `public/sfx`), his voice untouched.
- Graphics on the side opposite to whoever talks; full-screen idea scenes for big explanations (style 01 / 04 kits).
- When approved → new style number in `styles/` (e.g. 09 enta-show).

## Episode 1 recipe (2026-10-10, fnon, Ahmed Moataz — BIM Architect, Technical Design dept) — review_01 reviewed by Aly (notes below, nothing changed yet)
- Input = his edited episode (17:44, 1080p60, ONE wide camera on a couch: Aly LEFT x~0.2, guest RIGHT x~0.76), intro_in_video yes:
  intro 0-17.0 AND the same intro again at the end (1046.7-end) -> both in `plan.quiet` (found by matching tiny frames vs intro_fnon.mp4).
- Who talks: `tools/recipes/enta_ep01/voices.py` (pitch + MFCC, 2-cluster GMM; mono mix, lav mics not separate) ->
  `speakers.py` (word labels A/G, turns). Mouth-motion from frames was unreliable (Aly in profile) — don't use.
- Virtual camera = zoom style `cut` (Edit.tsx): close 1.6 / medium 1.3 / wide on the speaker, origin x 0 (Aly) / 1 (guest);
  long turns split every 2.2-3.4 s; short turns = wide; while a card is up the shot is LOCKED (1.45) on the speaker and the
  card sits on the opposite side (wide -> centre). Boards force wide.
- Kit `motion-library/src/enta/`: stickers = real crops of his styles sheet (`public/enta/*.png`, fx_*.jpg),
  templates enta_term (paper card: term + EN + meaning + "مثال"), enta_photos (white-border taped photos/logos),
  enta_stickers, enta_bubble, enta_name, enta_glitch, enta_leak; full-screen boards enta_pipeline, enta_clash,
  enta_deadend (Board.tsx), enta_render, enta_merge (Board2.tsx). New cue `sfx` {name, volume} plays public/sfx.
- Pictures: Wikimedia via `work/scripts/commons.py` (polite: retries on 429), logos simple-icons (jsdelivr) recoloured.
  The old woman from his intro (intro_fnon 9.0 s crop) used when Aly says "زي الست اللي بتسأل".
- Captions: Whisper was very rough on this audio -> every sentence fixed in `work/fix.json` (English terms: BIM, Facade,
  Curtain Wall, Coordination, Shaft, Ducts, Revit, Clash Report, Render, Prompt...). Aly to check spelling.
- Scripts archived in `tools/recipes/enta_ep01/` (make_plan.py = the full cue list; copy + change anchors per episode).

### Aly's review of ep01 review_01 (2026-10-10) — he said: change NOTHING now (waits for viewers); edits later = review_02
- Liked: motion graphics very good, pictures very good. Keep the SAME amount — do not add more motion (Aly: "متكترش موشن اكتر"). Face reactions are good — keep them.
- Too much zoom in (start was over). Never repeat the same slow zoom-in on a person right after cutting back. Most zooms OK.
- 0:23 enta_leak has a hard edge. 1:30 board backdrop (fast pixelated dust/scratches) too noisy → clean or still.
- 7:40 meaningless arrow sticker (stick() at S093 'بيبدأ').
- Leak hard edge again at 17:15 (thanks). End 'أول حلقة' card = white empty photo with the logo tiny in a corner → show the logo ALONE (trimmed, no card).

### review_02 (2026-10-13, Aly + guest Ahmed's notes) — `work/scripts/make_plan_v2.py` -> plan_v2.json, `output/review_02.mp4`
- CUT 273.72-294.85 (guest's "design changes when it reaches technical / a good designer..." remark — Ahmed: not tasteful
  toward the design team). Cut on audio dips; `plan.keep` + quiet in TIMELINE seconds; different framing each side + glitch.
- Dead End limit is NOT fixed: 6 / 9 / 12 m depending on use (residential / commercial / hotel...) and other factors
  (enta_deadend `varyAt/values/types/note`). Never present a code number as a fixed rule.
- Captions OFF in long videos (plan `captions: false`); reels/shorts keep them. Bottom = `enta_note` point strips.
- Camera calmer: crops 1.45 / 1.25, static (no drift), same person never gets the same zoom twice in a row, calm first
  2 min, no slow-push fillers. Leaks = CSS glow (no image edge). Board backdrop = calm (no moving dust/scratches).
- Softened card "قابل للتنفيذ؟" -> "من الديزاين للتنفيذ". Added cards where nothing explained the talk. End = logo alone (trimmed).

- Stickers per DEPARTMENT (Aly 2026-10-13, after ep01 v2 used `brace_l` `{` on a فنون card): never mix.
  فنون (fnon): reel, masks, brush, note_o/b/g, splat_o/b/g + shared. حاسبات (cs): brace_l/r, zero, one, floppy, bug + shared.
  رواد الأعمال (biz, 2026-10-27, vector in `vstick.tsx`): bulb, coin, chart_up, briefcase, rocket, shop + shared.
  Shared (both): qmark, burst, star_*, spark_*, star8_b, onair, tape_*, arrows (only when they point at something).
  ep01 v2 still has the `{` sticker (card "الإنشائي يحدد العواميد") — fix only when Aly asks.
- NO pixelated pictures (Aly 2026-10-13). The stickers are 3x upscales of ~100 px crops of his 1344x752 styles.png (the only
  copy, thumbnails/styles.png) -> soft/pixel edges. Next: redraw the sticker set as VECTOR (SVG, same look: flat muted fill,
  dark outline, white sticker border, grain) so they are sharp at any size. Pictures: source >= displayed size x 1.5; never
  upscale small crops (ep01: the woman from the 720p intro is soft too).
- Speech bubble tail must not show a seam/cut where it meets the bubble (Aly 2026-10-13). enta_bubble draws the tail as a
  separate SVG triangle over a CSS rounded box -> the outlines break at the joint. Next: bubble + tail = ONE SVG path with one
  outline (and one white sticker border). ep01: only when he asks.

## Show intro video "فيديو تعريفي" (2026-10-16) — `projects/انت بتشتغل ايه/فيديو تعريفي/` -> `output/review_01.mp4` — APPROVED as is (Aly: "حلو جدا الفيديو")
- Aly alone on the couch (4:23, 1080p60 HEVC, centre x~0.45), improvised talk about the show. Nothing cut, NO intro/outro added, no captions (notes).
- His asks: files screenshot (`Screenshot_45.png`, dates 3-7/2023) when he says he made the intro back then; when he names the
  CS ("graphics") and fnon intros -> the intros as MUTED taped clips on the side, a teaser (a few seconds), not the whole intro.
  Done at 80.8-92 s (both sides), 92 s (window woman → logo), 193 s, 226 s.
- Project code = `enta00` (public folder must be ASCII): `sh work/scripts/build.sh review_NN` (make_plan + build_edit + rename).
  Scripts copied to `tools/recipes/enta_intro/`.
- New boards `src/enta/Board3.tsx`: `enta_flavours` (3 guest types: cs / fnon / business, chips) and `enta_drawer` (desk drawer:
  logos inside 2023 → closes, years tick + dust → opens, logo jumps out onto the desk; 4 text phases).
- Pictures: his 2023 OBS designs (`_assets/OBS/scene2.png`, `_assets/OBS 2/Background.png`), Adobe icons from Wikimedia,
  Wikimedia workshop + camera photos, Claude logo when he says "في كلود دلوقتي" (Whisper heard "فيك لود").
- Camera: single person, static 'cut' crops 1.25 / 1.4, card on the right -> origin x 0.95 (pushes him left to ~0.33).

## حاسبات ep01 (2026-10-20, guest Aiman Ismail — Senior Software QA Engineer) — ONLINE episode (Google Meet screen recording)
- Input `input/main video.mp4` (30:23, 1080p60): Meet tiles guest LEFT [36,290,910,470], Aly RIGHT [985,290,910,470] (source px,
  name labels/corners cropped), his intro 0-17.13 and again 1806.5-end (found by the dark Meet bar under the tiles).
- Aly: his OBS frames were "دوشة" -> SIMPLE: no frame, hide the Meet UI (browser bar, call buttons) completely, calm dark bg.
  Instead of zoom: switch "كادرات" (both / one person big / one person left + card right), soft slide 14 frames. Zoom ONLY
  inside the tile and only a little (1.08) — "it's a screen recording, not a camera".
- Code: `src/enta/Meet.tsx` (Edit prop `meet`, cue `shot` {m: two|G|A|GP|AP|full, z, zx, zy}; 'full' = his intro as is).
  Boards `src/enta/BoardQA.tsx` (13: qa_what, qa_req, qa_eyes (SVG cube that turns), qa_types, qa_login (manual cases ->
  automation code -> ×N -> report), qa_api, qa_perf, qa_road, qa_joker, qa_istqb (real ISTQB badges from istqb.org),
  qa_ai, qa_prod, qa_demand (labelled as Aly's opinion, not a statistic)). Real objects = Fluent 3D emoji + real logos.
- Stickers are VECTOR now (`src/enta/vstick.tsx`, used by Sticker() first) — no more pixelated PNG crops.
- Board text: wrap in `direction: rtl` (mixed "*Postman*: جرّب" was reversed in LTR). Cards capped at 9 s, bubbles 5 s.
- Speakers: voices.py + speakers.py (same as ep01) worked on the Meet mix (remote voice vs local mic). Aly's camera dropped
  ~1129-1131 -> guest-only shot there.
- Render: `work/scripts/render.sh review_NN` = 5-min MUTED chunks + `mix_audio.py` (his audio untouched + sfx) + join.
  stills_cli.sh now empties TEMP after every still (each still copied the 2 GB source: 11 stills filled E:).
- Scripts archived in `tools/recipes/enta_cs01/`.
- Aly's notes on review_01 (chunks 0-3): one-path bubble, ON AIR text fits, NO 'مثال' unless I simplify a term myself, a short
  definition for EVERY term said, QA/QC card = "QA مجال وQC مجال تاني… إحنا هنا بنتكلم عن الـQC" (don't correct the words said),
  links note "في الوصف", speaker circle on boards > 5 s (MeetPip, `pip` cues; not on qa_login — busy enough), circle not zoomed
  on the face, sides by GAZE (looks left -> placed right; here Aly left / guest right, meet.left = 'A' — usual, not a law), person+card on his side. Liked: cadre switching + background.
- review_02 APPROVED (Aly 2026-10-20: "حلو جدا") -> **style 14 online-interview** (styles/14). Long videos: ask before compressing (shorts: always).

## حاسبات ep01 -> vertical SHORTS (2026-10-21; 17 ideas, Aly picked: only the 5 strongest) — `output/shorts/NN_slug.mp4` + `.txt`, composition `meet-short`
- Aly: "حولي الفيديو ده ل shorts" + full episode link (https://youtu.be/5xqomlWcKzE) + his thumbnail `input/e2.png`; END of every short =
  the episode itself + QR (like newstage19), NO CTA clip of his.
- Ideas = every self-contained Q&A of the episode (17), posting order = strongest first (tester vs developer eyes, AI replace, boring?...).
  Data `work/scripts/shorts_data.py` (hook + pieces in source sec), captions hand-corrected per piece in `caps.py` (Whisper on the Meet
  mix is weak: re-transcribe per piece with `cap_words.py`, then write their exact words; English terms in English).
- Look (`src/enta/MeetShort.tsx`): style 14 turned 9:16 — calm Meet bg, headline + series tag "انت بتشتغل ايه · حاسبات NN/17", captions
  (enta palette: paper box / mustard / orange via stage kit `pal`), hook sentence first + VCR rewind. Cadres: `two` = Aly top / guest
  bottom stacked · `one` = speaker big (zoom inside tile ≤ 1.08) · `board`/`card` = the APPROVED long edit (review_02, 1080x608) on top
  where it shows a board or person+card, with the speaker (board) / listener (card) under it. Notes of the long plan = taped strips on
  the seam. Small episode badge top-left, then a 3.2 s END CARD: "شوف الحلقة كاملة", big thumbnail, QR + "امسح الكود · أو اللينك في الوصف".
- Pipeline: `bash work/scripts/build_shorts.sh N…` = make_short (edges.fit on the waveform, Meet strip + review strip cut with audio/video
  concatenated SEPARATELY) -> one bundle, media copied into out/bundle/public -> render -> `level.py` (-16 LUFS, CRF 23 = compressed).
  QC `qc_sync.py N…` (piece offsets 0, length = timeline); QR decoded from the rendered end frame with cv2. ~5 min render per short.
- Edges: Meet audio has digital silence (-80 dB) between speakers -> easy cuts; but within one speaker check with `edges.py` profile
  (fit() walked into "اللي بعده" / "طبعا" / "معينة" -> exact `(a, b, 'x')` edges by hand).
- ⚠ v1 (shorts 1-3) had the PICTURE 0.93 s ahead of the voice after the hook: the rewind clip produced 0 frames, tpad hid it.
  Fixed (frame-exact select/settb, whole-frame pieces) + gate `qc_av.py strip N` in build_shorts.sh (0.5 s of frames slid over the
  source at 60 fps, ≤ 0.025 s) and `qc_sync.py` after leveling (voice). Aly: "17 too many" -> `PICK = [1, 2, 5, 3, 4]` in shorts_data
  (posting order; best 3 first): tester vs developer eyes, AI replace, no CS degree, boring?, production/refund. Others stay in IDEAS.
- v2 (Aly on short 2): sfx on every zoom = over -> whoosh only when the cadre moves (two/one/board/card or other person), zoom-only changes silent. v1 in output/shorts/archive_v1/.
- v3: my 5 rejected ("more motion graphics… give me the choice") -> table of 17 ideas with % motion/board -> Aly picked 14 API, 10 roadmap, 11 manual/automation, 4 production (PICK in shorts_data).

## رواد الأعمال ep01 (2026-10-27, guest Karim Tamer — Courzerve -> Kiko's Snacks -> FPL Champ) — ONLINE (Meet), code `entabiz01`
- Input = his Premiere export (45:03, 1080p60) of an OBS Meet recording; biz intro 0-17.12 and again 2686.0-end (from the .prproj ticks:
  254016000000 / s). The Meet LAYOUT CHANGES at his own cut 187.53: before = Karim big (169,151 1582x800) + Aly's tiny self-view
  (1658,808 139x104) inside Karim's tile corner; after = side by side (Karim 18,288 / Aly 966,288, 936x526). `meet.phases` in the plan.
- Aly's asks: 0:17-2:03 = his intro with a tiny camera -> "enlarge only enough + a lot of motion + Blender": ONE full-screen board
  `biz_open` (src/enta/BizOpen.tsx): his self-view pre-cut + lanczos 3.2x (`work/scripts/aly_open.sh`, Meet label cut off) in an ON-AIR
  TV frame the WHOLE opening (hero -> left -> hero), Karim behind a red curtain ("ضيف الحلقة؟") that opens on "كريم" (karim_open.mp4 =
  his FULL tile, no crop), headlines/chips/stickers on his words, an Egypt -> Cairo (OSM Nile) -> GUC pin map (Wikidata Q691097
  29.988N 31.442E) + the real New Cairo road sign "GUC" (Commons), and 4 Blender clips (tools/blender/biz_scenes.py, cinematic v2: DOF
  on the subject, motion blur via frame handler, handheld drift, swoop/crane/dolly-zoom, teal-orange light): tower (big success),
  road (starter / reached a level / closed / something new), crowd (dolly zoom on the golden 0.25%), three (the 3 projects timed to
  "المشروع… التاني… التالت"). Render: `bash tools/blender/render_biz_clips.sh "b_tower tower 270" ...` (~2 s/frame on the 1050 Ti).
- Aly: NO crop of the tiles the whole video (zoom ≤ 1.08 only for moments) -> Meet UI inside tiles is COVERED: our paper name tags
  over the Meet labels, a soft blur over his crop button, and (phase 1) our framed picture of Aly over Meet's self-view (`self`, `masks`).
- Aly LEFT / Karim RIGHT in the two-shot (he looks right) = meet.left 'A'. Then style 14 cadres + calm zoom.
- Boards = ONE declarative `biz_free` (src/enta/BoardBiz.tsx): emo/pic(video)/logo/text/chip/mark/sticker/arrow/path/walker/bar/num/
  panel/strike/poly/wave. 27 boards (Breadfast, Courzerve pivots, skills ✓✗, real Behance campaign videos, The Dip walker, McDonald's
  example, a 4-panel comic of the 4-month system story, cinema snacks world, 4 h vs 14 h, price 90 -> 200, FPL, 5 pillars + AI, iceberg,
  how each project reached customers, AI wave surfer...). Pictures: Behance (Courzerve: 3 campaign videos via the CCV HLS 720p),
  Instagram (kikos.snacks, fpl.champ posts, 640 px), Breadfast site, Open Library cover (The Dip), Commons (GUC).
- Scripts: project work/scripts (make_plan.py, build.sh, render.sh, mix_audio.py, voices.py + speakers.py, aly_open.sh).

### biz ep01 — Aly's opening reviews (2026-10-27/28) — what he wants from a "wow" 3D opening
- Blender clips inside a board MUST each sit in their own `<Sequence from={layer.at}>` (v1 bug: they played from the board start ->
  only their last frame showed: "كل الحاجات ال 3d كانت صور"). Same for video items in picture layers.
- "Less childish, more professional/realistic": no capsule pawns / candy colours. v3 = lathe-turned chess pieces (marble/onyx pawns,
  a GOLD QUEEN for the rare/famous one — he preferred the queen to the king), night glass towers with per-window random lights
  (brick node Bias, mortar size is in brick space), measured PBR, kelvin practicals, satin metal that catches light on dark sets.
- Use the blender-skills repo (tools/external/blender-skills = EL4CTEO/blender-skills 1.1.0) for real, not only its tables:
  `apply_stack` (Bevel arc miter + Weighted Normal) on furniture/props, `qa_check` on every build (it caught mics INSIDE the
  characters), time-of-day light temperatures + moon. Helpers in biz_scenes.py: hs_stack(), qa(), kelvin(), moon().
- Transitions must make sense: the podcast studio is an apartment INSIDE a building of the city -> the camera backs out through the
  window into the city -> the gold tower (one continuous shot, scene 'podcity'). A push into a crown was "مش مفهوم".
- Podcast set = a REPLICA of RWA "حوارات مع عباس" (refs references/style-sheets/rwa_podcast.jpg): black pleated curtain, big screen
  with OUR show logo, studio monitors, bookshelf with books/trophies, posters, long PLAIN table (no wood grain), typewriter, props,
  Edison bulb, office chairs, boom mics that stop 6-7 cm off the face; wide front-on two-shot (deep room, ~23-30 mm, no 14 mm
  distortion), enough light. A real store needs details (lit shelves, OPEN/CLOSED neon, awning, sign, shutter).
- Chess board flicker = z-fighting (board and frame top at the same height) -> lift the board 4 mm. Card numbers bright.
- Overlays: no overlap ever (stickers vs his frame, heads vs the guest corner); department name rings drawn INSIDE the logo picture
  (measured name box per logo); logos from the intros at a non-wink frame (11.0 s); his self-view crop centred on his FACE (the
  Meet self-view is wider than it looks: 1658-1887); no inner-shadow ring on tiles (radius 28 only); the self-view inside the
  guest tile = blur ONLY the visible part, no badge; speaker circle follows a FACE TRACK (karim_track.py) through layout changes;
  no fade-in on the opening board (the guest tile flashed); "Full Time… وبيزنس خاص" = two parallel lanes, the 1-year stop = a 1/8 gap.
- Blender renders: run ONE chain at a time; stopping the outer bash leaves child loops alive -> kill them (they wrote old-version
  frames into the new folders). render_resume.sh resumes after EEVEE crashes.


### biz ep01 — Aly's review of the FULL episode (2026-10-28, 31 notes, `work/review1_notes.md`) -> review_02
- **Re-render only what changed** ("متعيدش الفيديو كله… عيد بس الموشن للحتت دي و بعدين جمع الفيديو"): `work/scripts/redo_parts.py <old json>
  <new json>` diffs the cues (a changed shot counts until the next shot; mixed-direction board titles; captioned collages) ->
  `redo_parts.json`; `render_redo.sh review_02 <old chunks>` renders those parts muted, renders the Edit layer **'fix'** (transparent:
  only masks marked fix/patch, nothing while a full-screen board is on) as PNGs, and `compose_redo.py` lays overlay + parts over the old
  chunks in ONE ffmpeg pass; sound re-mixed whole (voice untouched). Global changes (a renamed name tag) go in the 'fix' overlay;
  the new tag keeps the old text's width (`keep`) so it covers the old one completely.
- Meet's "speaking" dots on the guest tile (77 % of the call) = masks with `patch` = clean crops of that spot from frames without dots
  (`work/indicator_scan.npz`, nearest earlier crop), drawn inside the picture with a soft round edge. Scan the source for Meet UI first.
- **Text direction** (5 notes!): board titles were LTR (biz_free is not inside Base) -> "4 شهور", "هرم AI", "موجة الـAI" flipped.
  Title is RTL now; arrows inside Arabic text point LEFT (←). Write his titles exactly ("الـAI بيتغلغل واحدة واحدة", no dots).
- Every card line on ITS word: term `defAt` / `exAt` (absolute s); a line whose word is far later becomes a note on that word,
  never early inside the card. English name = the term itself -> Arabic name under it (Accountability -> المساءلة).
- Each sentence on its own side / pillar (Breadfast vs Early Breakfast = two halves, no joining arrow; the 5 pillars). Generic
  players = icons (3000 restaurants), real brands only when named. Same colour = same quantity in comparisons (time / money).
- Recurring ideas get a recurring motif: "العالم بتاعك" = planets (`planet` item: players on the rim, grow, shake, ceiling) + the guest
  as a character with his REAL face (`char`: face circles cut from his camera, poses walk/push/jump/cheer/sad) like the Oz shorts.
- Examples Aly explains get their own animation (cake: small cake/big share vs big cake/small share, `cake`); jokes too
  ("عزة النفس بتلعب كوتشينة" = `card` items on a table). Both people stay visible while one explains (`board(..., both=True)` = one
  circle per side).
- Sources: a number from the internet gets its source ON screen (picture + who said it: Karpathy's napkin math via 36Kr), our own
  episodes get thumbnail + exact title + QR. His accounts: YouTube @AlyShorosh · Instagram @alyshorosh · Facebook aly.shorosh · TikTok @alyshorosh.
- His name on screen: "علي شُرُش" (or "علي معتز شُرُش"), never "علي معتز".

### biz ep01 -> 5 vertical SHORTS (2026-10-28) — `output/shorts/NN_slug.mp4` + `.txt`, composition `meet-short`
- Aly picked from 3 idea lists (rejected most): 01 AI took two pillars, 02 The Dip, 03 first customers, 04 food business, 05 worlds (last).
  Pipeline = cs ep01 shorts recipe (scripts `tools/recipes/enta_biz01_shorts/`): strip y 282..820 (side-by-side tiles), boards from review_02,
  MeetShort `masks` (our name tags علي شُرُش / كريم تامر over Meet labels, blur on the crop button, clean patch over Karim's speaking dots).
  End card = his thumbnail `input/e3.png` + QR of https://youtu.be/HCDZvW9lJtk (checked from every rendered end frame). All picture/voice
  QC ok, -16 LUFS. Titles in the .txt all Arabic. Assets afterwards in `<project>/motion_public/entabiz01s`.
- 06 Courzerve (2026-10-31, Aly: "شورت ليها علاقة ب courzerve يكون باين فيها امثلة من شغل courzerve"): the story (idea -> name -> pivot ->
  corona -> closed) + the lesson (engineers polished the website, weak in marketing/sales, marketing = experiments). NEW MeetShort
  `work` items = the guest's REAL work on top while he names it (cadre 'work': card + speaker under): `clip` = cut of their Behance
  campaign videos (website, calendar, form/SMS, Zoom session, instructors in the studio), `pic`, `posts` (fanned designs); label chip
  (`pos: top` when a clip has a lower third), small brand logo badge. Data = `work` list in shorts_data (source seconds), make_short cuts the
  clips into `entabiz01s/cz/`. Captions: consecutive English words now one LTR group (stage Caps; "Engineering Software" bug).
