# Video Maker — Aly Shorosh (read me first)

Goal: help Aly produce MANY high-quality YouTube videos (+ Shorts/Reels) with the least time, zero money,
and the fewest tokens. First deliverable: a reusable **Motion Graphics Library**.

## Who you work with
Aly Shorosh — Egyptian content creator (Cairo), CS graduate, software QC engineer, strong professional
background in graphics, media and video production. Topics: geography, history, religion, sports,
self-development, relationships, philosophy, general knowledge, explainers. New long video every Friday.
Full context: `docs/01-about-aly.md`.

## How to talk to Aly (important)
- Reply in **simple Egyptian Arabic**. Avoid mixing many English words into Arabic sentences — it confuses
  him. Use an English term only when it is a tool/button name, once, and explain it in Arabic.
- Short, practical, step by step. One question at a time at most.
- Code: clean and simple, no over-engineering. UIs: calm and descriptive.
- Free tools only. No paid services, no subscriptions beyond what he already has.

## Read order (load only what the task needs — saves tokens)
0. Skill `.claude/skills/aly-video-motion/SKILL.md` — what Aly loved (repeat) + his review mistakes (never repeat).
   Load it for every video job.
1. `docs/03-decisions.md` — what was decided and why (don't re-argue settled points).
2. `docs/05-motion-library-spec.md` — the library to build.
3. `docs/07-learn-from-codex.md` — review his earlier Codex attempt FIRST (incl. its Excel project catalog).
4. `docs/06-brand-and-setup.md` — DISCOVER brand/setup from his folders. Aly does NOT fill forms;
   ask him only what you truly can't find, in one short message.
5. Tutorial/UI shorts: `docs/16-recipe-tutorial-short.md` (proven recipe + review lessons).
6. Only if needed: `docs/02-current-workflow.md`, `docs/04-pipeline-plan.md`, `docs/08-token-rules.md`,
   `docs/09-chat-history.md`.

## Hard rules
- Never edit, move or delete anything in the Codex folder or in Aly's other automations
  (reels-publisher, instagram-comment-dm). Read only.
- Never open/read video files as frames to "look" at them (exception: ONE frame when 06 says so). Work from text (transcripts, JSON, code).
  To check a motion visually, render ONE still frame (PNG), not a video.
- Never put money-costing services in the flow.
- NEVER delete a video file (full videos, render chunks, reviews, mixes) without asking Aly first (2026-10-25). If only the opening/ending changed, render those and splice the old middle.
- When a job is DONE, delete all TEMP files yourself (Aly 2026-10-28): render chunks/parts, PNG frame sequences, Blender frames already
  encoded, bundles, temp mixes, still checks. Keep final videos + .txt, review videos, public/ clips, inputs. Next smart redo = the delivered video as base.
- Keep `motion-library/catalog.json` as the single source of truth for templates (see spec).
- Git: repo https://github.com/Aly-Moataz-Shorosh/VideoMaker, branch `main` only. After EVERY code/docs change: commit + push right away (no asking). Never commit `projects/` (new jobs) or videos/audio — .gitignore handles it.

## Current state (update this section after each work session)
**Start every job with `docs/14-production-modes.md` (job types, density rule) + `docs/13-plan-rules.md`
+ `docs/15-style-library.md` (what Aly's work looks like; pick a color pack per video).**
Aly-facing guide: `ابدأ هنا.md`; new project = `new-project.bat` → `projects/<date> <type> <name>/`
(input/, assets/, notes.txt). Tests live in `projects/_tests/` (00-calibration input is a HARD LINK — never write).

Done (2026-10-06):
- Codex review `docs/10`; identity `docs/11` (Aly-approved colors/text; name = logo images, text "Aly Shorosh";
  Arabic spelling شرش); `brand/theme.json` v1; brand files in `brand/` (logo, sfx, logos-tools).
- Remotion lib (registry in `motion-library/src/registry.ts`): keyword_pop, side_picture, captions (always on,
  LTR groups for English), subscribe_press (youtube/instagram), portal_world (matte, wave world, alyX move),
  counter, bar_chart, steps_list, icon_pop, section_transition; `edit`/`edit-v` compositions with smart zoom
  cues (punch/push/out). 9:16 = centered crop; graphics zone 0.40–0.66, captions below.
- Tools: transcribe.py (large-v3-turbo + 2nd pass for weak parts), matte.py (RVM mobilenet r0.4, despill
  edges; resnet50 tested — not better), build_edit.py (plan → edit json, Premiere XML, SRT, review mp4,
  overlays; --plan/--name/--vertical; cut=false default), fetch.py (yt-dlp).
- Dry run: full auto-edit 440→198 s (Aly: "very nice", wants MORE motion; cutting is his job now).
  Test short `_tests/00-calibration/output/short_01.mp4` (16 cues / 39 s).
- Aly wants (not built yet): intro + transitions + outro for > 5 min videos (outro asset
  `_branding/outro_1.mov`; R01 originals on drive F:), faceless videos (full-screen scenes), maps,
  better roto (ask what looked bad), more infographic types.
- 2026-10-06 style study of ALL his folders (F: Youtube/180 Daraga/Work + archives) → `docs/15-style-library.md`,
  `brand/packs.json` (10 packs, `plan.pack`), evidence `references/style-sheets/` (3 MB). Identity = logo/
  signature + subscribe + intro/outro + Aly; colors free per video. New: `cta_endcard` (his reel end card + QR).
  Tools: `style_sheet.py` (local), `stream_sheet.py` (YouTube frames, no download).
- F: drive and all external folders are READ-ONLY. Copy small things only. Genjutsu clips copied to `brand/clips/` (cue brand_clip).
- 2026-10-06 first real job `projects/2026-10-06 shorts RippleCutToll` → ONE condensed 9:16 short (~75 s) +
  his CTA clip. New: templates `screen_ui` (crop of a real screen recording + highlight marks) and `comment_cta`;
  build_edit plan keys `video` (alt footage), `keep` (exact ranges), `append` (CTA clip, anchors "A1:S001"),
  cue `"src": <sec>`; `motion-library/stills.mjs` (N still frames → 1 sheet). His edit had overlays baked in →
  `work/mkclean.py` rebuilt clean V1 from his .prproj. (transcribe.py print crash on Windows fixed.)
- RippleCutToll DONE: Aly approved `output/short_02.mp4` (v2 after review). Full recipe + lessons: `docs/16-recipe-tutorial-short.md`.
- NEXT (Aly 2026-10-06): After Effects versions of `comment_cta` (YouTube/comment popups), `screen_ui` (video card)
  and `side_picture` (picture sliding in) — editable colors (Essential Graphics / controls) so he reuses them himself in AE.
- 2026-10-08 `projects/2026-10-07 youtube figmaMake` (his final 8:18 edit, motion only, nothing cut, his intro/outro
  untouched via `plan.quiet`) → `output/review_01.mp4`. Recipe + gotchas: `docs/17-recipe-youtube-motion-only.md`.
  New templates: egypt_crowd, judge_scene, logo_flow, same_word, credits_drain, green_clip (+ world map data).
  Aly reviewed v1 (scenes "ممتاز جدا"; 6 mistakes → checklist in docs/17 + memory) → `output/review_02.mp4`
  fixes all 6 (badge greeting, picture on the word, face pan via tools/face_pos.py, green clip native side,
  click marks in every tutorial recording, Claude Code/Codex/Copilot/Cursor logos). Aly approved v2 ("كدا احسن بكتير"). Lessons saved in skill `aly-video-motion`.
- 2026-10-08 figmaMake → 6 VERTICAL reels `output/reel_1..6.mp4` (ROTO MODE: he is cut out at the bottom over a
  grainy two-blue motion background, recordings big on top, his CTA clip + comment_cta at the end). Plans:
  `work/scripts/make_reels.py`; mattes `public/projects/<code>/roto_*.webm`; textures `tools/make_grain_bg.py`.
  Aly approved the reels ("زي الفل"). Project folders may be archived off-PC: reusable scripts in `tools/recipes/`,
  green-screen clips `public/brand/greenscreen/`, CTA clip `brand/clips/cta_comment_youtube_9x16.mp4`. Layout rules in skill `aly-video-motion`.
- 2026-10-08 `projects/2026-10-08 shorts theodesy` (17:18 "حكاية الفيلم") → 10 FACELESS-FIRST vertical shorts: full
  motion graphics (new composition `film-short`, kit `src/film/`, pack `darkroom`), his cut-out only start/middle/end
  (raw HDR clips, auto-graded car shots), CTA clip at the end. Recipe: `docs/18-recipe-faceless-film-shorts.md`.
  Old projects' public assets parked in `motion-library/_parked_public/` (move back if an old project is re-rendered).
  Aly: animation "ممتاز ممتاز ممتاز" (technique = default for coming projects). Audio was his only complaint → versions:
  v2 podcast-processed voice + 39 synthesized sfx (`tools/make_sfx.py`, sfx liked), v3 AI voice (Edge TTS + OpenVoice
  timbre, short re-timed to the voice), v4 (short 2 only) his cut-out the whole short + ORIGINAL voice + sfx. He closed the
  job after v4 ("كدا شكرا"). Exports: `output/sfx_only/` (sfx stems), `output/voice_original/`, Word script, and a
  `<video>.txt` (titles + description + pinned comment) beside EVERY video in all projects. Scripts archived in
  `tools/recipes/theodesy/`. Next time: suggest Adobe Podcast "Enhance Speech" (free tier) for his voice — none of my
  local voice cleanups satisfied him.
- 2026-10-09 `projects/2026-10-09 shorts vhstodigital` (his 2023 video "VHS لـ Digital", fetched from YouTube) → 4 shorts he
  picked from my list (1 his own way, 2 price 30→300, 4 EasyCap vs his way, 8 nostalgia) = `output/short_{1,2,4,8}.mp4`.
  New look `vhs` for `film-short` (prop `look`, kit `src/vhs/`: CRT, VCR, cassettes, RCA cables, OSD, scanlines, chain diagram);
  real footage = cropped clips of his screen captures (B&W EasyCap vs colour). Scripts `tools/recipes/vhstodigital/`.
  **Aly rule (2026-10-09): never clean/process his voice unless he asks — original audio + sfx only.**
  yt-dlp needs `--js-runtimes node` (else ~100 KB/s). v1 review → v2 (waveform edges `edges.py`, even voice level
  `level_voice.py`, short 1 = both ways from his summary). Aly approved v2 ("زي الفل"). Recipe: `docs/19-recipe-vhs-shorts.md`.
- 2026-10-09 **STYLES CATALOG** `styles/` (Aly: "لما اجي اعمل فيديو جديد احط بس انهي ستايل"): numbered folders 01–06, each
  `sample.mp4` + `cover.jpg` + `اقرأني.txt`; index `styles/الستايلات.md` (Aly) + `styles/styles.json` (Claude: recipe/scripts
  per number). `projects/_template/notes.txt` has a line `الستايل: ..` → read it first and build that style. Add a new
  numbered folder whenever a new look gets approved.
- 2026-10-09 `projects/2026-10-09 shorts cairohistory` (his "خريطة القاهرة", Google Earth) → 4 MAP shorts (1 summary build, 3 Port Said
  street was a canal, 2 Zamalek, 9 seat of power ×7). Map = HIS KMZ (`E:/root/output/GoogleEarth/*.kmz`) + OSM Nile → `src/cairo/` engine
  (3D tilted map, houses rise inside his polygons, years, countryball cities, crown hops). Recipe `docs/20-recipe-map-history-shorts.md`.
  Then all 9 shorts (4–8 too). APPROVED = v2 of 4/5/6 → **style 07 map-history** (big cut-out in the opening, small round webcam after,
  no roto). Outputs: `output/` (v1), `output/v2/`. Scripts `tools/recipes/cairohistory/`. Aly: "ممتاز… عاش اوي" (2026-10-10).
- 2026-10-10 `projects/2026-10-10 shorts historyOfGraphics` (his "تاريخ الجرافيكس", 12:25) → 9 ideas, best 5 first (3 death→writing,
  4 pyramids/dead sciences, 5 stone→paper→print, 7 main skill per era, 9 whole history), then the rest (1 weak human, 2 three criteria,
  6 picture = 1000 words, 8 82% video + teach kids) = `output/short_1..9.mp4` (first 5/7/9 kept in output/v1; v1 press was frozen + a Nazi poster
  in his propaganda insert — never use that clip). NEW look 'hist'
  (`src/hist/`): ONE continuous timeline world, old LEFT → new RIGHT, camera walks/stops/zooms per era, photo/clip circles, HUD era+year,
  3 criteria meters; his face = BIG circle opening that shrinks into a small circle to the end (NOT a cut-out). Music from Pixabay
  (only tracks WITHOUT Content ID), pictures Wikimedia Commons. Recipe `docs/21-recipe-timeline-history-shorts.md`, scripts
  `tools/recipes/historyOfGraphics/`. APPROVED ("الجودة حلوة اوي اوي اوي ممتاز") → **style 08 timeline-history**; job closed.
  Only note: short 1's music (curious_mind) too busy → calm music only from now on (don't re-edit the delivered ones). Cairohistory/vhstodigital public parked.
- 2026-10-10 NEW SHOW "انت بتشتغل ايه" (interview, guest per episode, depts حاسبات cs / فنون fnon): show bible
  `docs/22-show-enta-btshtghl-eh.md` (look = his intros + styles.png stickers + film grain/glitch; pacing ~1 change / 2 s).
  Episodes via `projects/انت بتشتغل ايه/new-episode.bat` → `<date> epNN <dept> <guest>/`; brand copies in `brand/enta/`.
  Nothing rendered yet — waiting for his first edited episode.
  2026-10-27: 3rd department رواد الأعمال (`biz`): new-episode.bat option 3 (epNN per dept), vector stickers bulb/coin/chart_up/
  briefcase/rocket/shop, his question sets بزنس + صاحب مشروعين (docs/22). Intro = `brand/enta/intro_biz.mp4` (1080p); no separate logo png.
- 2026-10-10 EP01 `projects/انت بتشتغل ايه/2026-10-10 ep01 fnon Ahmed Moataz Shorosh` (guest = BIM architect, Technical Design dept;
  ONE wide couch camera, Aly LEFT) → `output/review_01.mp4` (+ .xml/.srt/.txt). Virtual camera on the speaker (voice clustering),
  enta kit (`src/enta/`: stickers from his sheet, term cards, taped photos, 5 full-screen boards), sfx cue. Recipe in docs/22
  ("Episode 1 recipe"), scripts `tools/recipes/enta_ep01/`. Waiting for Aly's review.
- 2026-10-14 `projects/2026-10-14 shorts ffmpeg` (his 2021 FFmpeg lecture clip, no face, style "جديد" + 5 Behance links) → NEW look 'pop'
  (`src/pop/`: violet + neon lime, grid, pixel dissolves, Figma selection boxes, glossy smiley ball, cursor clicks, echo type, tickers,
  polaroids, lavender HUD) → 3 faceless shorts `output/short_1..3.mp4` (1 condensed tutorial, 2 why it opens & closes, 3 three ways to open CMD).
  Aly: animation liked a lot, but split shorts = incomplete info → v2 ONE full short `output/v2/short_full.mp4` (2:43). RULES: ask one or
  several shorts first; never ≥ 3:00. Recipe `docs/23-recipe-pop-studio-shorts.md`, scripts `tools/recipes/ffmpeg/`. v2 APPROVED ("تمام") → **style 09 pop-studio**.
- 2026-10-14 `projects/2026-10-14 shorts lighting` (his "lighting your setup", 12:41, style "new" + Behance ref S.r. Seth Portfolio 2026) →
  asked first → ONE full short `output/short_1.mp4` (2:49). NEW look 'glass' (`src/glass/`: frosted glass cards on charcoal-navy glows in HIS
  channel colours, typing words + gold pill, Light Studio toggles clicked on the moment each light turns on, sphere 2D→3D, vector bust lit
  from an angle, spill/foil/grid, phone Manual Focus) + `Cam` = his camera ALWAYS on screen (cam.mp4 of the kept pieces, modes full/low/
  wide/mini/hide; wide on every light reveal). Recipe `docs/24-recipe-glass-face-shorts.md`, scripts `tools/recipes/lighting/`.
  APPROVED ("الستايل حلو", 2026-10-15) → **style 10 glass-face**. Parked public: ep01 + historyOfGraphics → `_parked_public/` (move back to re-render).
- 2026-10-15 `projects/2026-10-15 shorts adobeaudition` (his Audition voice-fix video, style 10) → asked first → ONE full short
  `output/short_1.mp4` (2:02). Glass look + his face always on (talking head, then the webcam CORNER of his screen recording: Cam modes
  `corner`/`cmini`), his real Audition recording big in a glass card with gold boxes on every click (`Screen`), real voice bars before/after
  (`Sound`), scenes `src/glass/audition.tsx`. NEW TRIAL: QR of the full-video link in the CTA (`CommentCta` qr/qrAt; at the top, never on
  his face) + in the last scene. Scripts `tools/recipes/adobeaudition/`. Aly v1 review: needs a HOOK → `output/v2/short_1.mp4` (1:32): before→after hook, steps at once with zoom on every click, small round webcam, voice enhanced (not the demo). v2 review: hook must be the REAL demo he played (1:53 before / 1:59 after) → v3; Aly: use his OPENING demo (0:00 Before label / 0:10.8 After) → `output/v4/short_1.mp4` (1:31, his real clip big in the middle). APPROVED v4 ("تمام") → **style 11 tutorial-hook-glass**, recipe `docs/25-recipe-tutorial-hook-glass.md`.
- 2026-10-16 show intro video `projects/انت بتشتغل ايه/فيديو تعريفي` (Aly alone, 4:23, nothing cut, no intro/outro) → `output/review_01.mp4`:
  enta look, files screenshot 2023, muted intro teasers on the side, new boards enta_flavours + enta_drawer. Code `enta00`, recipe in docs/22. APPROVED v1 ("حلو جدا الفيديو").
- 2026-10-16 `projects/2026-10-15 shorts aftereffects to code` (his AE → Lottie/Bodymovin tutorial, style "2 and 6 and 10") → asked first → ONE
  full short `output/short_1.mp4` (2:51): NEW mixed look 'lottie' (`src/glass/lottie.tsx`: grainy two-blue bg + glass + light VHS OSD, his
  water-circle animation rebuilt in vector, code typed in a vector editor, real AE/browser screen with gold click boxes, round webcam).
  Aly: v1 "طويل على الفاضي" → v2 `output/v2/short_1.mp4` (1:01, his 8-part outline, one sentence each).
  Recipe `docs/26-recipe-lottie-mixed-short.md`, scripts `tools/recipes/aftereffects2code/`. v2 "احسن بكتير" + 4 notes → v3 `output/v3/short_1.mp4` (1:23). APPROVED v3 ("ده ممتاز حلو اوي") → **style 12 lottie-mix**.
- 2026-10-16/17 `projects/2026-10-16 youtube premiere pro course` (his 2018 Premiere course, 3 YouTube parts 2:55 h → ONE course video 2:58,
  nothing cut, no intro/outro): NEW composition `course` (25 fps, `src/course/`: screen ALWAYS visible full/side + click zooms, Kw pills,
  Def/Fig cards, keycaps, DaVinci names, ⚡ 2026 cards with best video + QR, concept animations, 47 chapter separators with music, opening =
  2018 proof + 3 coverage rings 100/81/71 + timestamps, last chapter = what to learn next). Ch1 review approved after 2 notes (music in the
  opening, no "الحلقة N"). Recipe `docs/27-recipe-course-video.md`, scripts `tools/recipes/premierecourse/`, sources `research/` (44 verified
  screenshots), Excel `output/تغطية_كورس_بريمير.xlsx`, description `output/premiere_course_full.txt`. Full render → `output/premiere_course_full.mp4`.
- 2026-10-18 premiere course → 44 SHORTS series (`output/shorts/NN_name.mp4` + `.txt`, posting order = file number, most impressive
  first). Composition `course-short` (series frame + band: title, REEL NN/44, chapter + minute; captions; QR + his whole CTA clip).
  Aly's review notes (whole words, whole sentences, show the changing panel, anim + real screen, correct drawings, self-contained,
  compress like `ffmpeg -i in out`) → docs/27 "Shorts series" + skill. All 44 rendered; 2nd review fixed 1/25/30/31/34 (click marks in
  dual cards + manual `clicks`, timeline on screen, fast start, his own rose+Save example drawn = anim `RoseKey`). Job DONE (Aly: "thank you").
  `_raw` deleted; `output/full` course chunks (1.5 GB) still kept — ask before deleting.
- 2026-10-18/19 `projects/2026-10-18 shorts newstage19shorts` (his 52-min New Stage 19 lecture "Digital Art") → 30 viral shorts
  (hook first + rewind, headline, 3D-emoji tray, side badge + QR, no CTA). v1 small card + v2 roto rejected → v3: he fills the
  9:16 frame cut from the RAW HLG file (`cam.py`), faces of others blurred, Fluent 3D emoji. Recipe `docs/28-recipe-lecture-stage-shorts.md`,
  scripts `work/scripts/` (build.sh N…). Output `output/v3/NN_slug.mp4` + .txt. Review 2026-10-19 ("حلو اوي اوي ممتاز") → 18 shorts redone (real material,
  three.js scenes, NO blur — he blurs himself; old in `output/v3/archive/`), then 28 v2 (lip-sync fix: separate audio/video concat;
  qc_sync.py + qc_cam.py). APPROVED → **style 13 lecture-stage**, scripts `tools/recipes/newstage19/`. Shorts built before the sync fix
  (all but 28) drift up to 0.28 s — rebuild only if Aly asks. 28 v3 fixes a stale reused camera (build.sh now checks camera timeline + length). Then 4 more shorts 31–34 from the
  unused lecture parts (`new_1019.py`, TOTAL 34). Job closed (Aly: "thank you").
- 2026-10-20 show "انت بتشتغل ايه" حاسبات EP01 `projects/انت بتشتغل ايه/2026-10-20 ep01 cs quality control` (guest Aiman Ismail, Senior QA;
  ONLINE = Google Meet screen recording 30:23). Aly rejected his OBS frames ("دوشة") -> simple: Meet UI hidden, webcam tiles on a calm
  dark bg, cadre switches instead of zoom, zoom only inside a tile ≤1.08 (`src/enta/Meet.tsx`, cue `shot`). 13 QA boards
  `src/enta/BoardQA.tsx`, vector stickers `src/enta/vstick.tsx`. Render = 5-min muted chunks + ffmpeg audio (`work/scripts/render.sh`),
  30 fps proxy `source30.mp4` + PNG grain (SVG noise made it 14 h). Recipe docs/22 "حاسبات ep01", scripts `tools/recipes/enta_cs01/`.
  Aly reviewed the review_01 chunks -> `output/review_02.mp4` (full, with sound) — APPROVED ("حلو جدا") -> **style 14 online-interview**.
  Rule: compress shorts always, LONG videos only after asking him.
- 2026-10-21 cs ep01 -> 4 vertical SHORTS Aly PICKED from my 17-idea list with motion % (14 API, 10 roadmap, 11 manual/automation, 4 production) `output/shorts/NN_slug.mp4` (+ .txt titles/description/pinned, link youtu.be/5xqomlWcKzE):
  NEW composition `meet-short` (`src/enta/MeetShort.tsx`): stacked Meet tiles / speaker big / approved long-edit board on top, hook +
  rewind, captions, end card = episode thumbnail + QR (no CTA clip). Recipe docs/22 "17 vertical SHORTS", scripts `tools/recipes/enta_cs01_shorts/`.
  v1 picture was 0.93 s off (empty rewind clip) -> fixed + picture-sync gate qc_av.py; whoosh only on cadre moves; level.py limiter = same -16 LUFS. Waiting for review. Long-episode public (source30.mp4) parked in `_parked_public/2026-10-20 ep01 cs quality control/`.
- 2026-10-21 `projects/2026-10-21 shorts graphictablet` (his 2022 "أهمية الجرافيك تابلت", style 10 + QR end like 11) → asked first, Aly picked
  6/3/5/2/7 of 8 ideas → `output/short_{6,3,5,2,7}.mp4` (0:52–1:38) + .txt, sfx_only, voice_original. Scenes `src/glass/tablet.tsx`
  (declarative `tb_free` items, his picture-in-picture inserts shown big `tb_clip`, checklist, tablet↔screen map, LaTeX vs pen, whiteboard
  story map, QR end). Camera = ONE decode + trim per piece + concat in order (select reorders!). Recipe `docs/29-recipe-glass-face-talk-shorts.md`,
  scripts `tools/recipes/graphictablet/`. APPROVED ("الفيديوهات ممتازة") → **style 15 glass-face-talk**. RULE: a YouTube QR NEVER without
  that video's thumbnail → v2 = thumbnail + QR end in `output/v2/` (v1 kept; only the end re-rendered + spliced, `v2_end.sh`). Job closed.
  Unsure: he says "14" buttons (Huion page: 12 hard + 16 soft) — hidden in captions.
- RULE 2026-10-21: the `<video>.txt` beside every video starts with the exact header `العناوين:` (his posting script reads it), then الوصف
  (free length), tags, كومنت مثبت. NO YouTube link, NO posting-order line. Skill aly-video-motion + memory aly-notepad-format.
- ⚠ Remotion copies public/ (~2 GB) into Temp on EVERY bundle/still → C: hit 0 bytes twice. Use `stills_cli.sh`
  (one bundle in out/bundle), set TEMP/TMP to `motion-library/out/tmp` for renders and DELETE that folder after (one render left 13 GB).
- ⚠ C: fills during renders = Windows auto page file (19.4 GB) when RAM is full -> Remotion --concurrency=6 (not 10), temp never on C:, purge npm/pip caches after jobs (2026-10-29).
- ⚠ E: ~17 GB free. Premiere 2020 alpha format still untested by Aly (`_tests/premiere-test`).
- 2026-10-22 `projects/2026-10-22 shorts Journey to the center of computer graphics` (his whole playlist "رحلة إلى مركز الجرافيكس", 37 videos)
  → plan of 48 shorts (`خطة_الشورتس.md`), PILOT 3: `output/08_vectors.mp4`, `33_scarecrow.mp4`, `44_3d_programs.mp4` (+ .txt). New look 'journey'
  (`src/journey/`): series bar (3 stations = HIS logos), his channel logo + name at the bottom, end = playlist thumb + playlist QR + original
  video thumb (no QR), calm bg, Oz chapters DRAWN (no film), three.js scenes. HIS logo files + CLEAN voice files from
  `F:\_root\output\Youtube\Aly Shorosh NEW\` (copy only). Recipe `docs/30-recipe-journey-series-shorts.md`. v1 review (liked opening/end/colours) -> v2 `output/v2/` (v1 in output/v1): REAL
  example pictures (his work -> his video -> Commons) + be.net/shorosh tag, his matted face in a circle in Oz chapters, nothing clipped. v2 review -> v3 `output/v3/` (his own episode motion jy_clip, photo zoom to pixels, Behance QR, Oz face from his frame + whole-frame examples). v3 review -> v4 `output/v4/` (my motion back at 3 spots + word chips under his clips, pop-out scarecrow, bubble tails, clear 3D principles, name colour).
  v4 APPROVED ("حلو اوي انت كدا فهمت زوقي") -> WHOLE series in playlist order `output/series/NN_slug.mp4` + .txt
  (01 intro, 02–31 هو ايه, 32–40 Oz, 41–48 programs; 08/33/44 = v4 pilots). Data per section in project work/scripts (*_data.py, meta_all.py),
  archived `tools/recipes/journey/`; recipe docs/30 "The whole series". Aly's review 2026-10-23 (only named shorts redone, originals in
  `output/series/archive/`): outro text sizes, 10 = my photo-edit motion instead of a third-party clip, 11 = video audio, 31 = series-end
  text, 32 = opening sound + face track, 35 + 36 MERGED (2:54, no file 36), 37-40 = published audio with music + face 4:3 rectangle,
  37 = real LearnFree playlist screenshot. APPROVED as **style 16 journey-series** (styles/16). Job done ("thanks").
- 2026-10-24 `projects/2026-10-20 youtube audioproduction` (his 2021 ONLINE Zoom session "الصوت للفيديو", 2:03 h, students' voices) → ONE
  course video, composition `course` at 30 fps (`src/course/audio.tsx`: teaser "هتشوف في الكورس ده" from his own clips, 2021 proof from
  the taskbar date, Claude's opinion + counted stats (vector Claude spark), parts map + grouped timestamps, FilmTag). Aly rules: nothing
  cut / sped up, the session audio NEVER touched (mix_audio.py = pieces as-is, checked 0.01 dB / 0.7 ms), music only in opening/separators,
  31 chapters in 7 PARTS, motion only where it explains. Scripts `tools/recipes/audiocourse/`. `output/review1.mp4` = opening + part 1. Review 1 (2026-10-25): teaser smaller card + course minute, small proof frame (no zoom) + "still useful", 100% screen removed, Claude opinion = COVERAGE rings (`coverage.py` -> work/coverage.xlsx: fundamentals 71, mics 83, Premiere 55, Audition 53 = per TOOL; what was left out written on the card), opening ~48 s -> `output/review2.mp4`. Review 2: proof card smaller + zoom INTO the date, opening pages at 82 %, coverage rechecked vs transcript (same numbers), new 5 s screen ORecommend (Claude's reasons, each really in the session) -> `output/review3.mp4`. Review 3: Premiere course thumb + QR on the coverage card, card block centred. Review 4: teaser + films/terms/explosion demo, 'hide' screen key (no empty card behind opening pages), VCol centring, ONextVideos (4 of his videos, thumb + QR). FULL VIDEO `output/audio_course_full.mp4` (2:06:52, re-rendered 2026-10-25, 13 concept anims `src/course/audioAnims.tsx`, closing chapter ONextA; `render_full.sh` = 9000-frame chunks in output/_chunks, delete one to redo; audio QC 93 probes ≤0.05 dB / 0.7 ms) — sent, waiting for review. Not compressed (long video: ask first); _chunks kept until approval.
- 2026-10-26 audio course uploaded (youtu.be/2XVRSnTuZJQ, thumbnail in assets/) -> SHORTS series "أسرار الصوت": plan of 32 (`خطة_الشورتس.md`),
  composition `course-short` now generic (brand logo/name, src size, end card = thumbnail + QR, CTA word; look `sound` teal/violet). PILOT 4 in
  `output/shorts/`: 01 phone voice, 02 explosion, 03 noise removal, 04 sound = wave in REAL 3D (three.js `src/course/sound3d.tsx`) + 04b the same
  in BLENDER 5.2 (`tools/blender/sound_scenes.py` -> webm alpha clips `public/projects/audio/b3d/`, scene `BlenderClip`; Blender at
  `E:/root/_assets/programs/Blender Foundation/Blender 5.2`, GTX 1050 Ti, EEVEE ~1-3 s/frame). blender-skills repo in `tools/external/` (ignored).
  Scripts project work/scripts (archived `tools/recipes/audiocourse/shorts/`), level = -16 LUFS + peak limiter. Aly will record a NEW CTA for
  this course (Premiere CTA says "بريمير") -> add it to the end later. Review 1 (same day): Blender wins (04b), series numbered in
  COURSE order -> pilots are now 26 phone, 27 explosion (BoomScene idea scenes `src/course/shortScenes.tsx`), 29 noise (fast hook, word-size
  click boxes, mouse-follow zoom), 07 wave (= 04b, not remade); old pilots in output/shorts/archive/. Channel footer, Fluent label pictures.
  Next 3D: Blender at 1080x1920 full screen (sound_scenes.py default) — scenes must be RE-FRAMED for portrait (test: water edge, mic clipped),
  stone from far, complete mic/speaker.
  Reviews 2-4 (same day): only HIS voice (students cut), one continuous screen card (cin/cout), drag = view follows the mouse, NO two shorts
  with the same hook/content (check_overlap.py) -> 26+27 MERGED = `26_phone_explosion.mp4` (2:58, explosion heard), series = 31, noise = 28.
  07 v2 = full-screen Blender clips p_*.webm (sound_scenes.py portrait) + IdeaRows. Old versions in output/shorts/archive/. 
  2026-10-27 night (Aly 'كمل'): the rest of the series rendered = 29 shorts in output/shorts (all but 03/04 = film examples, held: Content ID)
  + .txt each. Data: project work/scripts series_data.py..series_data5.py + txt_series.py (archived tools/recipes/audiocourse/shorts/).
  Band title <= ~27 Arabic chars. No new 3D yet (theory = course anims + Fluent IdeaRows).
  2026-10-27 Aly: "اعمل 03 و 04 بمقاطع الأفلام زي الكورس" -> 03_film_music_comedy (1:44, Mickey + King of Comedy) and 04_sound_in_his_head
  (2:22, Wrestler hook + Raging Bull): films shown AND heard (raw pieces) + FilmTag cue (piece key `film`), series_data6.py.
  Review 2026-10-27 (big): "ال icons مش بتبقى كافية خالص" -> NO IdeaRows as explanation: series_data7.py replaces every icon-row piece with
  what he showed on screen (pinned `src` + zoom on what he names); 19-23 rebuilt in series_data8.py (sound examples HEARD as raw pieces,
  22 = his Single/Double drawing, 23 = camera vs mic + clap + SyncAnim); 12/13 pinned shotgun chart / event photo; 16 = Léon scene;
  27 frames him not the desk; 01 + camera example; labels/tags shrink to fit. 02 = Blender street scene (sound_scenes.py 'street',
  ~1600 frames, NOT rendered yet) + make_street_sfx.py. 07 v1 archived (07 = v2). OPEN: 05 (no useful info: drop?), 08/09 need real
  explaining animations. Almost every short must be RE-RENDERED (overnight, after his 'كمل'). Only 01 re-rendered (before the icon patch).
  08/09 = Blender explainers per sentence (series_data9.py, scenes hz_a-d / sr_a-d). Render started 12:05 after his 'كمل', STOPPED by Aly
  at 14:20 (PC off): done = p_street + hz_a-d + sr_a/b clips, raw 01 03 04 06 10-18 (not levelled). Old versions in output/shorts/archive/before_1027.
  On his next 'كمل': run project `work/scripts/resume_1027.sh` in the background (sr_c/sr_d, level, 19-31, 02/08/09, txt; log work/night_1027.log).
- 2026-10-27 show "انت بتشتغل ايه" رواد الأعمال EP01 `projects/انت بتشتغل ايه/2026-10-27 ep01 biz karim tamer` (guest Karim Tamer: Courzerve, Kiko's
  Snacks, FPL Champ; Meet recording 45:03, code `entabiz01`). Opening 0:17-2:04 (Aly's tiny self-view) = full board `biz_open` (Aly in an
  ON-AIR frame the whole time, Karim behind a curtain, Egypt->GUC map, 4 cinematic Blender clips `tools/blender/biz_scenes.py`, resume
  after EEVEE crashes with `render_resume.sh`); 28 `biz_free` boards + 117 cards; NO crop of tiles (Meet labels covered). Recipe docs/22.
  Opening reviewed 4x (2026-10-27/28; lessons in docs/22 "biz ep01 — Aly's opening reviews"): realistic v3 Blender (RWA studio
  replica inside a building -> city -> gold tower 'podcity', detailed store, chess board + gold queen, framed cards).
  2026-10-28 overnight: opening5 + stills of all 28 boards (4 overlap fixes) -> FULL `output/review_01.mp4` (45:03, 1.33 GB, not
  compressed) + `output/review_01.txt`; intro/outro frames + audio levels identical to the source. Waiting for Aly's review.
  E: was full (3 GB free): render chunks + mix in `D:/Temp/biz01_chunks` (render.sh CHUNKS/RTMP env) — ask before deleting.
  Aly's review of review_01 (31 notes, project work/review1_notes.md; lessons docs/22 "review of the FULL episode") -> `output/review_02.mp4`
  (+ .txt) made SMART: redo_parts.py diff -> only 20.2 of 45 min re-rendered + Edit layer 'fix' overlay (name tag "علي شُرُش", Meet
  speaking-dots patches) over the old chunks, compose_redo.py, sound re-mixed (levels = source). New items: planet / char (Karim
  Captain-Azouz style = his REAL head cut from the call with the headset on a cartoon body in black, approved after 6 tries) / cake / card;
  RTL titles; both speaker circles. Waiting for Aly's review. Temp: D:/Temp/biz01_chunks (review_01 chunks) + D:/Temp/biz_redo_review_02
  (parts, overlay PNGs) — ask before deleting. E: ~1.5 GB free. Audio-course public is parked again in `_parked_public/audio`
  (bundle was 3.5 GB with it) — move back before resume_1027.sh. No link for Karim's app (Aly: not needed).
- 2026-10-28 biz ep01 -> 5 meet-shorts `output/shorts/01..05` + .txt (Aly picked 3/5/7/18/1; end = input/e3.png + QR youtu.be/HCDZvW9lJtk;
  MeetShort masks = our name tags over Meet labels). Saved as **style 17 online-episode-3d** (the long episode) + **style 18 meet-shorts**.
  Episode .txt: chapters + titles 'ep3-entrepreneurs | <all-Arabic topic> | انت بتشتغل ايه؟'.
- 2026-10-28 ASSETS LIVE IN THEIR PROJECT (Aly moves finished projects to his external disk, "انقلها لفولدراتها"): every project's
  public assets (old motion-library/_parked_public/* and public/projects/entabiz01) are now in `<project>/motion_public/<name>/`
  (projects already moved off the PC got a folder of the same name holding only motion_public, to merge with his copy). To re-render
  a project: move `motion_public/<name>` back to `motion-library/public/projects/<name>`. Audio course = `projects/2026-10-20 youtube
  audioproduction/motion_public/audio` (back to public/projects/audio before resume_1027.sh); biz ep01 = its motion_public/entabiz01
  (back to public/projects/entabiz01 before any review_03). biz ep01 3D scenes saved as .blend (textures packed) in `<project>/blender/`
  (`biz_scenes.py --save`; the per-frame animation is code, the .blend opens on frame 1). Temp files deleted after each job.
