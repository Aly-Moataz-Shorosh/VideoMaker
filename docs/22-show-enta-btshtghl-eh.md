# Show: "انت بتشتغل ايه" (What do you do for a living?) — show bible (2026-10-10, before episode 1)

Interview show: Aly + one guest per episode, two departments: **حاسبات (cs)** and **فنون (fnon)**.
Aly hands his EDITED episode → Claude adds motion graphics + captions + sfx + internet pictures/clips that explain
the guest's job, terms and examples. Goal (Aly): fun, visualized, explain every term with an example.

## Files
- Episodes: `projects/انت بتشتغل ايه/<date> epNN <cs|fnon> <guest>/` made by `new-episode.bat` (in that folder).
  notes.txt ends with `dept:` and `intro_in_video: yes|no`.
- Brand copies (sources are READ-ONLY on E:/root/output/Youtube/Aly Shorosh New/انت بتشتغل ايه):
  `brand/enta/intro_cs.mp4`, `intro_fnon.mp4` (17.1 s, 1280x720 25 fps — upscale to the episode size),
  `logo_cs.png` / `logo_fnon.png` (cartoon Aly at desk, speech bubble "حاسبات/فنون — انت بتشتغل ايه", ON AIR, "يقدمه علي معتز شُرُش"),
  `styles_sheet.png` (his element sheet), `thumb_example_*.png`. Contact sheets: `references/style-sheets/enta_*.jpg`.
- Studio = OBS two-camera layout (Aly LEFT, guest RIGHT; also single-focus scenes). Raw ep1 (fnon, Ahmed Moataz) exists on E:.
- Guest questions per department: `اسئلة الضيوف - حاسبات/فنون.docx` in the show folder (read for terms).

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
- Department flavour: cs → code, circuits, floppy, bug, 0101; fnon → curtain, film reel, masks, paint drips, notes.

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
