---
name: aly-video-motion
description: How to add motion graphics to Aly Shorosh's videos the way he approved (figmaMake 2026-10-08) — workflow, what he loved (repeat and grow it) and his review mistakes (never repeat). Use for ANY job in this video-maker project — youtube / reel-h / shorts / faceless, a new projects/<date> <type> <name> folder, "اشتغل على", موشن جرافيك, زوم, سكرين ريكورد, لوجوهات, كروما, انترو/اوترو, or rendering/reviewing a video — even if he doesn't name the skill.
---

# Aly video motion — the approved way

Talk to Aly in simple Egyptian Arabic, short, few English words. Free tools only.
Deep docs (read only what the job needs): `docs/14` modes · `docs/13` plan rules · `docs/15` style packs ·
`docs/16` tutorial short · `docs/17` long-video motion-only recipe (commands + gotchas).

## 00. Shorts count — ASK first (Aly 2026-10-14)
Before any shorts job ask: one short or several? One = the WHOLE goal of the video (complete tutorial, no missing step).
Several = give him suggestions, he picks. NEVER build before he picks (cs ep01 2026-10-21: my pick rejected) — list each idea with length + % motion graphics, most motion first. HARD RULE: no short ever reaches 3:00 (CTA included).
TUTORIAL short = SIMPLE + FAST (~1 min, Aly 2026-10-16: 2:51 was "طويل على الفاضي"; the CTA sends them to the full video):
hook → tool → download → convert → code → result → compare → summary, ONE key sentence each. "Whole goal" = the goal in brief.
But (v2 review): keep the sentence that gives the hook its meaning (what it's FOR), show the tool's real look before its plugin, add his real
"trying it" clip + use cases after the result, and explain every term in plain words (Shape Layer = drawn inside After Effects = least space).

## 0. Style number first
`notes.txt` line `الستايل: NN` → `styles/styles.json` tells the recipe/scripts for that number (01 youtube-motion, 02 reels-roto,
03 tutorial-short, 04 film-faceless, 05 film-face, 06 vhs-faceless, 07 map-history, 08 timeline-history, 09 pop-studio, 10 glass-face, 11 tutorial-hook-glass, 12 lottie-mix, 13 lecture-stage, 14 online-interview, 15 glass-face-talk, 16 journey-series, 17 online-episode-3d, 18 meet-shorts; samples in `styles/`). No number → ask him ONE
question with the list. A newly approved look = a new numbered folder (sample.mp4 12 s, cover.jpg, اقرأني.txt) + styles.json entry.

## 1. Read the job first
- His finished edit = THE base: cut nothing, add no intro (he places intro/outro/music himself).
- Find his intro/outro by numbers (brightness / diff vs a room frame) → `plan.quiet` = no motion, no captions there.
- Where does he sit? (motion per column, or ONE frame) → all graphics on the OTHER side.
- His notes give scene ideas at approximate seconds — speech may start a bit before/after; anchor on the WORD.
- Messy room / weak light → more and bigger motion to cover it.

## 2. What he LOVED — repeat and grow it
- **Full-screen idea scenes built from his own notes** ("ممتاز جدا جدا"): Egypt map filling with people → laptops →
  jumping → one stands out → map closes like a book (`egypt_crowd`); world map, cat & dog, people in China/USA agree
  → fly to Egypt university → split screen two doctors, different marks (`judge_scene`). Build one for every
  idea he describes; make new templates when needed (map data in `src/data/world.json`, `blocks/geo.tsx`).
- **Big photo BEHIND him** (`portal_world`, his cut-out in front) — "فكرة حلوة اوي".
- Dense motion: never > 3 s without motion or zoom (`fill()` zoom fillers in make_plan).
- Real logos from the internet, his packs (charcoal etc.), not Claude's default colors.

- Show intro video (enta, 2026-10-16) APPROVED first time ("حلو جدا"): his proof screenshot (file dates) on the words, his intros as
  MUTED few-second teasers on the side, idea boards from his talk (3 guest types, the drawer 2023 → today), his old designs, tool logos.

## 3. Mistakes from his review — NEVER again (check all before rendering)
1. Greeting "علي شو": no gold calligraphy signature picture → `brand/video-blog-badge.png` or channel logo, or nothing.
2. A topic picture appears ON its word, not before.
3. Never crop faces: `python tools/face_pos.py <img>`; tall photo in a wide card → side_picture `panFrom:100 → panTo:<face%>`
   (bottom→top, ends on the faces, quickly).
4. His green-screen clips (`_branding/on video/*`, keyed to alpha webm, cue `green_clip`) stay on their NATIVE side —
   the character enters from that edge. Never shift/mirror; pick a clip whose corner is free.
5. Tutorials: show WHERE he clicks — the real screen recording with a highlight box on EVERY button
   (`screen_ui` marks, frames from cue start). Find clicks with a dense contact sheet + full-res crops.
   A result-only card is not enough.
6. Every tool/program he names gets its logo. Whisper drops English names (silent gaps) → re-transcribe the gap
   with a prompt of likely names, confirm with a second different prompt.

7. (found by me, reels 2026-10-08) A whole-sentence caption fix on a sentence a reel CUTS puts wrong words on
   screen (reel 1 showed the video's opening words). Give the kept part only; build_edit now warns.
8. Colors: he prefers his ORIGINAL colors — no color correction unless he asks (stills first if he does).
9. (vhstodigital 2026-10-09) Clipped words at cut edges ("ديجيتال", "تلتمية", "USB") — Whisper word ends are ~0.3 s off and
   a stop consonant inside a word looks like a dip. Fit every edge on the waveform (`tools/recipes/vhstodigital/edges.py`:
   walk to 150 ms of real quiet, never into the next word) and print the edge dB. Never start on the tail of an earlier word.
10. Uneven voice level between pieces ("كل مشهد تحسه متسجل في يوم") → per-sentence GAIN to one target for every short
   (`level_voice.py`, gain only, no cleanup), then -15 LUFS. Voice processing itself only on request.
   One loud peak must not leave one short quieter (cs ep01 roadmap -19 vs -16): reach the target with a light peak limiter, check all LUFS equal.
11. Shorts from a tutorial: when he summarizes BOTH ways at the end, use the summary (both ways), not one way only.
   Hook = straight into the idea; don't stack two intro sentences. Real footage of him talking = big (16:9 card), not a small TV.
   Explain WHY visually when he says something costs more (count it up: 10 × 300 = 3000).

12. (enta ep01 review 2026-10-10 — NOT fixed yet, Aly waits for viewers' opinions; any change = review_02, never overwrite)
   - Zoom in was too much, especially at the start. Never ease-in on a person, cut back, then do the SAME zoom on him again
     (looks like a mistake). Most zoom in/out was good — just less, and calmer at the start.
   - Light leak (`enta_leak` fx_leak_warm) showed a hard visible edge (23 s) — never a leak with a visible crop edge.
   - Board backdrop (dust + scratches moving fast, pixelated) = noisy/ugly → clean, calm, or a still background.
   - A sticker arrow with no meaning (7:40) — every sticker must point at / mean something.
   - The light-leak edge happened TWICE (0:23 and 17:15): never use enta_leak / fx_leak_* crops as they are.
   - End "أول حلقة": logo_fnon.png inside a white photo card = big empty white card with a tiny logo in the corner.
     A logo goes ALONE (trimmed to its content, transparent, no white card) — never an empty/white picture.
   - Liked: motion graphics "حلو جدا" and pictures "حلوة اوي". Amount is RIGHT — do NOT add more motion (Aly: "متكترش موشن اكتر").
     Face reactions (camera on a face reacting + reaction stickers/punch) = "حلوة" — keep them.

13. (enta ep01 v2, 2026-10-13) Long videos: NO captions (too many Whisper mistakes) — captions only in reels/shorts.
   Fill the bottom with point notes (enta_note) instead. Facts from the guest are checked with him: never show a code
   value as fixed when it varies (Dead End 6/9/12 m by building use). Remarks that can offend a team (e.g. "the design
   changes when it reaches us") → cut cleanly on audio dips or soften; ask Aly.

14. Show "انت بتشتغل ايه": stickers belong to the episode's department — فنون: reel, masks, brush, notes, splats;
   حاسبات: { }, 0/1, floppy, bug; رواد الأعمال (biz): bulb, coin, chart_up, briefcase, rocket, shop; shared: ?!, burst, stars, sparkles, ON AIR, tape. Never a code sticker in a فنون episode
   (ep01 v2 had `{` — left as is until Aly says).

15. Never pixelated graphics/pictures (Aly 2026-10-13: the upscaled sheet stickers looked pixelated). Stickers/icons = vector
   (SVG); photos only when the source is bigger than shown; no upscaled crops of small frames.

16. Speech bubbles: body + tail are ONE shape with one continuous outline — no visible seam at the tail (Aly 2026-10-13).

17. (enta cs ep01 review 2026-10-20) "مثال" label on term cards was wrong almost every time: write "مثال" ONLY when the line is MY
   simplification of a scientific term; when it is what he/the guest said, no label (EntaTerm `exLabel`, default empty).
   EVERY term that is said (UI/UX, Postman, Agile, Refund, Soft Skills…) gets a short plain definition on screen.
   Bubble tail again looked glued on (#16) -> EntaBubble is now ONE SVG path. Text must fit its sticker (ON AIR was cut).
   Explanation boards > ~5 s: the person talking in a circle in a corner (MeetPip, cue `pip`) — skip only when the board
   itself is full of motion. Liked: the cadre switching ("حركة التنقل حلوة جدا جدا") and the calm dark background.

18. (biz ep01 full review 2026-10-28, docs/22) Arabic text with English/numbers/arrows flipped 5x -> RTL everywhere, Arabic arrows ←,
   still-check every mixed text. Card lines on their own words. Each sentence on its own side. Generic things = icons. Same colour =
   same quantity. His name = "علي شُرُش". Re-render only the changed parts (redo_parts.py + render_redo.sh + 'fix' overlay layer).

19. (biz ep01 shorts 2026-10-31) A short's HOOK is never the sentence the short starts with after the rewind (heard twice) — take it from later.

## ONLINE interview (style 14, enta cs ep01 2026-10-20, docs/22 'حاسبات ep01') — cadre switching + background "حلوة جدا جدا"
- Google Meet/Zoom screen recording: hide the meeting UI, tiles on a calm dark bg, NO decorative frame ("دوشة"), switch cadres
  (two / one big / person + card) instead of zoom; zoom only inside a tile, ≤ 1.08. Sides by gaze (usually Aly left, guest right).
- Every term = card with a plain definition; boards > 5 s get the speaker circle (not a tight face crop) unless the board is busy.
- Render: 30 fps proxy + PNG grain (full-frame SVG noise = 14 h render), 5-min muted chunks + ffmpeg audio.
- LONG videos: never compress without asking him (shorts: always compress).
- SFX on camera moves (cs ep01 shorts 2026-10-21): a whoosh on EVERY zoom in/out = "over". Whoosh only when the cadre itself moves
  (layout / other person), never on a zoom inside the same cadre.
- Shorts from an online episode (cs ep01 2026-10-21, docs/22): ONLY the 3–5 strongest (Aly: 17 = too many). Composition `meet-short` — tiles stacked (Aly top), speaker big,
  the approved long edit's boards on top; hook + rewind + captions; END = episode thumbnail + QR only (no CTA clip).
  NO post number ("06/6") in انت بتشتغل ايه shorts (Aly 2026-10-31: he picks which to post) -> band pill = "من الدقيقة m:ss في الحلقة"
  (MeetShort prop `at`) in the PUBLISHED YouTube episode — his upload may cut parts (biz ep01: 231.2-269.2 removed = -38 s, make_short YT_CUT).
  Other series (courses, playlists) keep the REEL NN/total number.

## Vertical reels from a long video (figmaMake reels 2026-10-08)
- Ranges = closed ideas; his edit has almost no pauses → put every edge on a measured audio dip (50 ms dB profile),
  never on Whisper word times (they are ~0.3 s off). No clean dip → keep the piece whole.
- 9:16 framing: plan `cropX` = his x in the 16:9 frame (0.40 here), `vShift` 0.15 lifts the face to the top;
  graphics on his chest 0.38–0.655, captions under. Cards: height ≤ 0.27 of the screen.
- CTA = his vertical phone clip (`brand/clips/cta_comment_youtube_9x16.mp4`, already leveled; original `input/calltoaction.mp4`, keyword يوتيوب, keep 7.06–12.01) re-encoded +8.5 dB,
  appended with `fit: cover`; comment_cta `top: 0.02`.
- Screen recordings in 9:16 must be BIG (Aly: "اكبر بكتير و صغرني"): `split: true` on screen_ui / phone_tour →
  card owns the top half (0.085–0.485), he shrinks into the lower half, captions lift between them. Click steps
  (marks) are always big; other recording groups alternate big/small for variety ("شوية كبيرة وشوية صغيرة").
  Small cards in the chest zone only for short non-tutorial moments.
- Never a hard-edged video box: footage melts into the background with gradient masks (Edit `splitStyle`), or
  (his other option, not built yet) his head pops out of the frame via matte. Background = two blues mixed
  (main + darker) with STRONG risograph grain: stippled/dithered shading, shapes with dotted edges, clear film
  grain that boils (`tools/make_grain_bg.py` → `public/bg/*.png`, Edit `GrainBg`). Faint noise = not enough; grain overlay opacity 0.65 approved ("ممكن يقل حاجة بسيطة" from 0.9).
- **Preferred 9:16 layout = ROTO MODE** (Aly reviewing reel_1, 2026-10-08): no black/empty strip ever. He is cut out
  for the whole reel (`tools/matte.py ... --fps 30` per kept range → plan `roto`), smaller at the bottom
  (`rotoScale` 0.62), motion-graphics background (GrainBg) everywhere, every recording BIG in the top area,
  other graphics lifted (`gShift` 0.3), captions on his chest (`capBottom` 0.17). No portal with a phone
  screenshot behind him (phone got hidden + huge) → a real phone card instead. Roto ≈ 2.6 fps → start it first.
- Never start a reel ON a word: begin in the quiet tail before it (+ 3-frame audio fade) — "مثلا" got cut.
- Show the WHOLE app when he says "the result": `phone_tour` (one phone, every page slides in, splash first).
- Reuse the long plan's cues (same source seconds) via a make_reels script (example: `tools/recipes/figmaMake/make_reels.py`); set `plan.video` explicitly
  (build_edit picks the first file in input/ — calltoaction.mp4 sorted first).

## VHS look (style 06, vhstodigital 2026-10-09) — Aly: "زي الفل"
- Same engine as the film shorts (`film-short`, prop `look: 'vhs'`, kit `src/vhs/`): CRT TVs with his REAL footage inside,
  VCR, spinning cassettes, RCA cables that draw themselves, the whole signal chain built on his words, OSD PLAY/timecode,
  scanlines. Recipe docs/19. Pick a look per topic (old tech → VHS, film/history → darkroom); new topic look = new kit.

## Faceless-first shorts from a long video (theodesy 2026-10-08, docs/18) — Aly: "الانيميشن ممتاز ممتاز ممتاز"
**Use this technique in every coming project** (his words: "احفظ التيكنيك ده").
- VOICE = HIS ORIGINAL AUDIO, UNTOUCHED (Aly 2026-10-09: "تنضيف الصوت متعملوش الا لو انا طلبته"). Only GAIN: every
  sentence to one level, every short -15 LUFS (`level_voice.py`, docs/19), CTA clip matched. Cleanup (`podcast_voice.py`),
  Adobe Podcast or AI voice (theodesy v3) ONLY when he asks.
  Every short gets sound effects from `public/sfx` (`tools/make_sfx.py`): whoosh per scene, pop per label, and a
  matching sound per action (scissors, stamp, cash, clock, projector, tape, glitch...) — plan in `sfx_plan.py`.
- Deliver as standard: sfx-only stems, voice stems, a title + description `.txt` next to every video. Word script ONLY
  on request. His face the WHOLE short = style 05 (v4 layout, `faces_full.py`).
- Whole short = creative motion graphics / animated infographics from HIS explanation (his reference shorts: collage,
  cut-out B&W photos, paper + grain, red marker scribbles, maps with little characters, light beams). Real footage only
  when the point is how a real thing looks. His cut-out only at start / middle / end (+ a red halftone disc behind him).
- Composition `film-short` + kit `src/film/` (pack `darkroom`, never Claude colours). Scenes placed on his words (beats).
- Raw phone clips are HLG HDR → tonemap; car shots need the auto grade (Aly asked). Voice: denoise the car part.

## History MAP shorts (style 07, cairohistory 2026-10-10, docs/20) — Aly: motion "ممتاز جدا جدا جدا جدا"
- Maps = HIS Google Earth KMZ (search E:/root/output/GoogleEarth, myplaces.kml) — never draw by eye ("زي ما انا راسمها بالظبط");
  today's Nile/roads OSM, region Natural Earth. Engine `src/cairo/map.tsx` (scene 'cmap'): tilted 3D camera, houses rise inside his
  polygons era by era, big year + era tag, countryball cities, walls/aqueduct build, canals + boats, crown hopping seats, his old maps
  on taped paper (cpaper, flip for upside-down maps), ✓/✗ chips.
- His face: BIG cut-out in the opening only, then a small round webcam bubble (no roto, his screen behind him) to the END, continuous.
  A big cut-out the whole time hides the map; a few bubbles only is too little.
- Never show him PIL-drawn Arabic (unshaped letters) — he thought the video was broken. Stills from Remotion only.
- Redo of delivered videos → `output/v2/`, never overwrite.

## TIMELINE one-shot shorts (style 08, historyOfGraphics 2026-10-10, docs/21) — Aly: "الجودة حلوة اوي اوي اوي ممتاز"
- Whole short = ONE continuous drawn world (`look: 'hist'`, scene `hworld`, `src/hist/`): old LEFT → new RIGHT with a year ruler;
  the camera walks left → right on his words, stops / zooms on an era, the era's drawing acts (hands, hieroglyphs, press, fire…),
  then walks on. Never walk backwards: a list that runs back in time = circles around the current era; "these 4 scripts" = pan at z 0.6.
- Flat geometric drawing, warm ochre / plum / terracotta, paper grain, blurred foreground columns ONLY while moving (wipe).
- HUD: era card + year, 3 criteria meters when he measures things. Real photos / his inserts = small circles next to the drawing.
- His face: BIG CIRCLE in the opening (not a cut-out!) that shrinks into a small circle bottom-left, visible to the very end.
- Music: calm only, low. Short 1's `curious_mind` was "صاخبة شوية" → never busy/beat tracks; Pixabay tracks WITHOUT Content ID.
- Check every insert clip of his before reuse: one (his "propaganda" montage) shows a Nazi poster — never use it.
- Ideas count = what the video holds (never a fixed 9); build the best first, then the rest.

## POP STUDIO look (ffmpeg 2026-10-14, docs/23) — animation "حلوين كا animation اوي"; v1 = 3 split shorts rejected (incomplete info) → v2 one full short APPROVED ("تمام") = style 09
- Faceless tutorial shorts: violet + neon lime design-tool world (`look: 'pop'`, `src/pop/`), UI rebuilt as vector (his dark 720p
  recording only as a small polaroid proof), pixel dissolves, selection boxes, cursor clicks, echo type, tickers, lavender HUD.
- When he gives reference links: study images + video frames (Vimeo: playerConfig HLS url → ffmpeg tile), save sheets in references/style-sheets.

## GLASS look + face always on (lighting 2026-10-14, docs/24) — APPROVED "الستايل حلو" (2026-10-15) = style 10
- When his topic needs his real picture (light, camera, setup), keep HIS CAMERA on screen the whole short (`cam` prop, modes
  full/low/wide/mini/hide) and put the graphics on the top stage; switch to 'wide' on every moment the room changes.
- Build cam.mp4 with an EXACT frame count per piece (trim=end_frame) — -ss/-t + fps drifted 0.5 s over 42 pieces.
- Hide his camera where his source shows someone else's photo (gym pictures, a stranger lit from the front).

## TUTORIAL + HOOK (style 11, adobeaudition 2026-10-15, docs/25): v4 APPROVED ("تمام")
- A short is not a normal video: open with a HOOK = the result (before → after), then go straight to the steps. Cut the long video's intro talk.
- The before/after = the REAL demo he already shows (look at the FIRST seconds first: burned-in Before/After labels). Never two takes I pick myself (v2), and not a later demo (v3).
- His real screen recording big in a glass card that ZOOMS onto every click (gold box, cursor ripple, label); his face = small round webcam. More motion, less face.
- CTA: QR of the full-video link at the top (never on his face) + a QR card in the last scene, ALWAYS with the video's thumbnail. Check the QR scans from the rendered mp4.

## 4. Workflow (commands in docs/17)
transcribe (`--prompt` English terms) → fill skipped speech (`work/scripts/fill_gaps.py` (copy from `tools/recipes/figmaMake/`)) → contact sheet per
screen recording + crops for click rects → `work/scripts/make_plan.py` + `work/fix.json` (examples in `tools/recipes/`) (caption spelling) →
`tools/build_edit.py --name review_NN` → still checks with `sh motion-library/stills_cli.sh` → render →
verify duration / audio level / intro-outro identical to his edit.

## 5. Disk safety (C: and E: filled up during figmaMake)
Every Remotion bundle copies `public/` (~2 GB). Bundle ONCE to `motion-library/out/bundle`; set TEMP/TMP to
`motion-library/out/tmp` for renders and delete that folder after EACH render (13 GB from one render; every still
check adds ~650 MB). Check `df -h` before and after.

## 6. After every review
Add what he liked to section 2 and every mistake to section 3 (with the fix), plus the memory file
`aly-review-*-lessons`. Keep this skill short; details go to docs/17.

## LOTTIE MIX (style 12, aftereffects-to-code 2026-10-16, docs/26): v3 APPROVED ("ده ممتاز حلو اوي")
- He can write several style numbers ("2 and 6 and 10") → blend them into ONE look (bg from one, cards from another, touches from the third).
- Simple + fast tutorial short (~1:20): one sentence per step, his "trying it" clip + use cases after the result, explain every term.

## COURSE video (premiere pro course 2026-10-16/17, docs/27) — ch1 review approved after 2 notes; full 2:58 delivered, waiting for his review
- Old lessons merged into ONE video: nothing cut, his screen recording ALWAYS visible (full, or side when a card is up), zoom on his
  clicks (cursor still then screen changes, only where there is content), English-word pills, keycaps for spoken shortcuts, definition
  cards, concept animations, DaVinci names bottom-left, ⚡ "easier in 2026" cards (official source + best video thumbnail + QR + "Claude
  recommends, not Aly"), chapter separators with music, ×4 for silent waits, last chapter = what to learn next.
- Merged video: never "الحلقة 1/2/3"; music under the whole opening; Claude's text segments = typed text, NEVER AI voice-over.
- Coverage analysis: vs TODAY's program, explained tool = covered, exclude non-editing parts (say how big), 3 sourced yardsticks + Excel.
- Every outside fact: verbatim quote + highlighted screenshot (`tools/evidence.py`, `tools/pdf_evidence.py`); bot check = other source.
- Long render: muted 20-min chunks + audio built with ffmpeg (`mix_audio.py`) — Remotion's audio pass of 3 h filled the disk.

## Shorts from a course / tutorial (Premiere course series, 2026-10-18)
- Never: a clipped last word; a piece that starts/ends on half a neighbouring sentence; extra words at the edges.
- Every action he talks about must be visible: setting + result together; the panel that changes (timeline tracks) — not a ruler.
- An animation alone doesn't explain: animation on top + his real screen under it.
- Drawings must be technically right (Linear = straight, Bezier = S, Hold = step; Adobe definitions for Ease In/Out).
- Each short stands alone: result first, then why, steps, result. Shaky 2018 explanations → build from the clear parts + sourced card.
- Final pass compresses like his `ffmpeg -i in out` (x264 CRF 23 + AAC). Recipe: docs/27 "Shorts series".
- Mark EVERY click (also inside setting/result cards); add missed clicks by hand. Work on the timeline → timeline on screen.
- Start fast (the idea/animation first). When he gives his own example (rose + Save), draw HIS example.

## Lecture → many shorts (newstage19, 2026-10-19, docs/28) — APPROVED = style 13 lecture-stage (styles/13)
- He FILLS the whole 9:16 frame for the whole short (his recorded talk); never a small card, never removed for motion.
  Motion goes around him: zoom in/out, a tray of scenes over the empty part of the frame, slide/projector inserts.
- No roto/matte on a far 720p camera ("سيئ جدا جدا جدا"). Cut the camera from the RAW file (best quality), not his re-encode.
- Drawings: Microsoft Fluent 3D emoji actors (brand/fluent3d), not flat geometric SVG ("بدائي اوي و هندسي اوي").
- NO automatic blur (he blurs others himself). Hook sentence first, then a rewind to the start of the idea.
- (v3 review) Every icon must BE the thing he says: a snorkel mask is not swim fins (foot fins), a ring buoy is not a life
  jacket (vest) — when Fluent has no exact emoji, draw it (SwimFins in src/stage/emo.tsx). Check every slide number against
  the slide he is talking about at that second (short 3 got the wireframe slide 39 instead of the reading-order slides 37/38).
- When he names a missing sentence ("زود الجزئية اللي قولت فيها…"), add the whole passage, not one line.
- Real brands = their REAL logos as they are (Apple, Pixar, Facebook, TikTok, Blender, Arduino…; Aly 2026-10-19), never an emoji
  stand-in (an apple fruit for Apple). `logo:<name>` actors in src/stage/emo.tsx (white app-icon tile, public/logos).
- (v3 review 2026-10-19, "حلو اوي اوي ممتاز" + notes on 18/30) Show the REAL thing he talks about (his slide videos/photos, his own
  YouTube videos + QR, web clips) and explaining motion for concepts (pixel vs vector, rotating 3D, drag a material, one moving map).
  Whole words at every edge, finished sentences at the end, captions = his exact words, bleep insults, NO automatic blur (he blurs
  others himself — my auto blur was "وحش"), and keep the crop on him. Old versions → output/v3/archive/.
- LIP SYNC: concat video and audio SEPARATELY (a joint concat drifted the voice up to 0.28 s); check every short with qc_sync.py
  (constant offset = OK) and qc_cam.py (he stays in frame) BEFORE delivering — Aly: "متغلطش غلطات دي تاني".
- PICTURE SYNC (cs ep01 shorts 2026-10-21, Aly: "الصوت مش ماشي مع الصورة… متحصلش تاني"): the rewind clip after the hook had ZERO
  frames (fps=27/span → fps=30 chain) → every picture after it 0.93 s early; voice QC and file length both looked fine. Build every
  piece frame-exact (select/settb/setpts=N, trim=end_frame, pieces rounded to whole frames) and run `qc_av.py` = frames of the short
  vs the SOURCE frames (≤ 0.025 s) as a gate before any render. Never trust length or voice-only checks.
- CAMERA LENGTH: never reuse a cached camera/footage render unless it was built from the SAME timeline (short 28: an old
  camera was reused → he froze while the voice went on). Check every short: camera length = short length.
- More shorts from one source: list the parts no short used yet (gaps) and propose them; use his slides (proj_sheet.py) for motion.

## Shorts from a TALKING video = style 15 glass-face-talk (graphictablet 2026-10-21, docs/29) — APPROVED "الفيديوهات ممتازة"
- His own picture-in-picture inserts (product clips, his screen) = real material: show them BIG on the stage (`tb_clip`), camera `tlowr`.
- Full-frame footage → camera `wbig`/`tbig`; footage of someone else → `hide` + big cards (never an empty screen).
- "CTA مش فيديو بوشي زي ستايل 11" = no face CTA clip; end card = the full video's THUMBNAIL + its QR.
- RULE (Aly 2026-10-21): NEVER a QR of a YouTube video without that video's thumbnail next to it (i.ytimg.com/vi/<id>/maxresdefault.jpg).
- Redo of delivered videos = new folder (output/v2), keep the old; if only the end changes, render the end frames only and splice (v2_end.sh).
- Camera mp4: split + trim per piece + concat in the short's order (select=between reorders a hook to source order).

## The .txt beside every video (Aly 2026-10-21) — his posting script reads the word "العناوين:"
Usual layout: `العناوين:` (exact header, first line) + 1) 2) 3) titles / `الوصف:` free length / #tags / `الكومنت المثبت:`.
NO YouTube link in the txt, NO "ترتيب النشر" line (he tried a strict template and took it back). UTF-8 without BOM, LF line ends.
HASHTAGS (Aly 2026-10-30 "ليه مش حاتط هاشتاجز"): ONE line of real #hashtags INSIDE الوصف (every word starts with #, multi-word
joined with _), 6-8 tags, the short's own 2-3 FIRST (Instagram/TikTok take only 5). His reels-publisher (bulk.notes_for) reads only
the headings العناوين / الوصف / الكومنت / ترتيب النشر: a 'الوسوم:' part or 'كومنت مثبت:' (without ال) is NOT a heading and lands inside
the description -> pinned heading = `الكومنت المثبت:`. Check: run reels-publisher app.bulk.notes_for on the mp4 (read only).
Credit a played third-party clip by name + channel (on screen FilmTag + in الوصف), never its YouTube link.
Writer: tools/recipes/graphictablet/write_meta.py.

## Series shorts from a whole playlist = style 16 journey-series (Journey 2026-10-22/23, docs/30) — v4 APPROVED "حلو اوي انت كدا فهمت زوقي"
- Order = the PLAYLIST order (file number = playlist position). Series bar with his 3 EXACT stage logos + section label (never
  outside the frame, under its own station); his channel logo + name (character skin colour) at the bottom; calm backgrounds.
- His OWN episode motion is better than mine (jy_clip, his clip big + key-word chips on his words); my motion only where it explains
  more (lists, before/after, formats + program logos) or to replace a THIRD-PARTY clip inside his episode (short 10 photo-edit scene).
- Motion alone is not enough: REAL examples (his work -> his video -> Commons, credited). His strong works only: small Behance QR.
  When he names a real search ("What is graphic design"), show a REAL screenshot of that page (headless Edge), credit it in the txt.
- Use his EXACT logo files from F: (copy only), never redraw a logo.
- Story chapters: drawn characters + HIM in a circle with his original background (no roto), centred on his face (clean the face
  track: a hand/background jump = wrong). Ch5: bigger 4:3 RECTANGLE that shows his room; move the characters left to make room.
- NOTHING overlaps, nothing outside the frame: check every scene type with stills (face circle vs characters/pills/screenshots).
  Long English words: size from the longest word. Latin "?" after English, "؟" only in RTL text. Emoji only up to Emoji 12.
- Voice: clean take only where it really matches (check every voice_N.wav for long silences; fill gaps from the video); when he
  says the clean voice sounds bad -> his published sound WITH music, ONE gain per piece (per-sentence gain pumps the music).
- Whole sentences at every edge — print the words around each edge; no edge on a dangling "بس"; force an edge into a real silence.
- Merging two parts under 3:00: drop only repeats/asides/jokes, keep the story and every field.
- REVIEW RULE (2026-10-23): redo ONLY the videos he names (a code fix may help all, but render only the named ones); move each
  original to output/series/archive/ first (never overwrite an archived copy — use "v2/v3" names). Rebuild the bundle when public
  or src changed (stale bundle = old voice / old code). After every render: voice sync vs voice_N.wav = 0.


## Course shorts series — audio course review 1 (2026-10-26, style course-short, look 'sound')
- ORDER: a course series is numbered in COURSE order (chapter order), not "most impressive first" (that stays for talks/lectures).
- 3D = BLENDER (he compared three.js vs Blender: "4b احسن بكتير"), rendered at the WHOLE phone size 1080x1920, under the band and
  captions (BlenderClip full=True) — never a small box. Stone in water falls from far above; mic and speaker = complete models.
- Never a still icon card while he talks: idea scenes of his words (Fluent pictures + motion, src/course/shortScenes.tsx BoomScene).
- Emoji newer than Emoji 12 render as an empty box (🪚) → use the Fluent PNG (public/fluent/<name>.png, Label img).
- Click box = the size of the clicked word (marks w/h in source px); through menus the zoom follows the mouse with a mark on every
  click (menu bar → submenu → item → dialog button).
- Hook strong and fast: real "before" sound → what it is → real "after" → "بكليكة واحدة" (~17 s), then the steps.
- A sound demo that plays BEFORE his words must stay (fit() cut one: "مش باين الصوت") → raw piece edges, demo at its own level.
- Channel logo + name small at the very bottom of every short (his ch_face / ch_name).
- Review 2 (same day): sessions with students → only HIS voice in a short (cut their questions/answers); the hook of a demo short =
  just the demo he played; consecutive screen pieces = ONE continuous card (cin/cout) so it reads as one video; drags = the view follows
  the mouse to the drop point with a box on grab and drop. On a talk without screen: picture rows (IdeaRows, RTL) instead of an icon card.
- Series band title: at most ~27 Arabic characters (longer titles end in "..." in the band) — check one band still before rendering a batch.
- REVIEW 2026-10-27 (overrides the IdeaRows lines above): "ال icons مش بتبقى كافية خالص للشرح نهائي" + "جيب انا بشرح بايه في الفيديو".
  Icon/picture rows are NEVER the explanation. For every piece look at what HE showed at that moment (frame_sheet.py on start/mid/end)
  and show THAT (slide, film scene, photo, demo video); if he scrolled to an unrelated slide mid-sentence, pin the right picture with `src`
  and zoom on the part he names. A film scene he explains with = shown AND heard (raw piece) + FilmTag (03/04/16). Nothing on screen ->
  a real explaining animation (course anim, Blender full screen with cinematic sfx like 02's street), never icons.
- A short with no useful takeaway (05: general talk only) should not exist; theory shorts (Hz, sample rate) need an animation that
  SHOWS the concept step by step, else "ممل". Keep every example of a set (01: drawing + camera + sound).
- Text never leaves the frame: Label / Tag font shrinks with the text length (Short.tsx, shortScenes.tsx, sound3d.tsx).
- REVIEW 2026-10-29 (rest "حلوة اوي"): a piece never ends mid-thought ("يعتبر تقريبا" without "50% / نص الفيديو") and never starts
  after his bridge words ("المهم الأوديو بقى") — read the words around both edges. The hook = his strongest one-liner (01: "الصمت مهم زي
  أهمية الصوت"). Every example he PLAYS in that part is in the short (19 missed the العار clip), and a played video runs long enough
  to be felt — never 10 s of it; it is always heard as it was (gain 1). Tags/labels never on the caption line (Blender tags y 1190).

## 3D opening for an episode (رواد الأعمال ep01, 2026-10-27/28) — Aly: "عايز المقدمة استثنائية… مش اي حد يعرف يعمل زيه"
- Blender = realistic, not childish: lathe objects (chess pieces, coins, mics), measured PBR, kelvin practicals, real props; use the
  blender-skills repo scripts (apply_stack bevels, qa_check) — he checks that I really use it.
- Every 3D clip plays from its own start (Sequence per layer). Transitions must tell a story (studio inside a building -> out the
  window -> the city). Replicate the reference he names (RWA podcast set) closely, wide normal-lens framing, enough light.
- Nothing overlaps; his camera crop centred on his face; the guest never flashes; rings/highlights fitted to the real text box.

