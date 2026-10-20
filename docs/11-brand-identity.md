# Channel identity v1 (built by Claude from Aly's own work, 2026-10-06)

Built from primary evidence, not from Codex conclusions: Aly's `_branding` folder (newest files Sept 2026),
the live YouTube channel page (banner, avatar, 4 latest thumbnails), Behance profile, contact sheets of
R01/R11/R12/R14/R19/R20/R02, one frame of `delete silencef.mp4`. Status: **proposal until Aly approves the
style frame**. `brand/theme.json` holds the numbers.

## What the evidence says
| Source | What it shows |
|---|---|
| Channel banner + avatar | Royal blue banner, 2026 cartoon mascot center, gold Arabic calligraphy badges "VIDEO BLOG / علي شو / ALY SHOW" and "TUTORIALS / دروس". Avatar = old cartoon face + "Aly Shorosh". |
| Latest thumbnails (Remove silence, Genjutsu, AI contest, Digital Art) | Aly's face with expression; **huge heavy white Arabic text with dark outline**; ONE highlight in **yellow-gold**; dark rounded pill tags with icon; teal/cyan + warm cinematic grading; real tool logos. |
| `_branding` Sept 2026 designs (magnific_*) | Charcoal background `#1A1E23`, white heavy Arabic headline, **one word in sky blue**, thin blue diagonal accent lines, mascot pointing at a content box. Reels frames: near-black + neon blue/red glow, YouTube red CTA, round avatar + "Aly Shorosh". |
| `character cartoon.png` (2026) | Full mascot sheet: turnaround, eyes, mouth shapes (A/E/I/O/U/F/L/M), hands, pointing, holding Subscribe. Palette skin `#E0B884`, hair `#1A1A1A`, tee `#000000`, jeans `#1F4E79`. Animation-ready. |
| `title 3.png` | **Main signature logo**: Arabic calligraphy "علي معتز شرش" (spelling: شرش) + "ALY MOATAZ SHOROSH". Shown in gold bottom-left in R01. Aly never types his name; he uses the logo images. If text is needed: "Aly Shorosh". |
| R01 (latest long video) | Pictures/thumbnails float around him with no boxes; cinematic dark interludes with gold signature; mascot avatar for jokes/CTA. |
| R14, R11 | Collage of images around the speaker; R11 yellow folder tree grows in front of him over teal room light. |
| Room / footage | Real room, gold-framed art, cyan light right, warm left. **Aly is usually CENTERED** (confirmed by him). |
| Behance (techniques only, not colors) | Shape layers + Animation Composer; 3D camera with photo cards over real satellite maps (R20); **rotoscoping the person and compositing him into a scene**; chroma key + parenting; templates with swappable assets; 3D extruded data bars on a country map (R22); Element 3D org hierarchy. |
| R12 "هو ايه" subscribe | 3D keycap button (face + thick darker edge), pops in tilted under the logo, gets PRESSED (sinks into edge) → grey "SUBSCRIBED"; bell keycap pops beside it, turns red-orange gradient and rings; signature rises below. → template `subscribe-press`. |
| R13 "المجالات و ساحر مدينة أوز" | Aly cut out (soft edges), centered, in front of a full-frame changing world (film, images, collage, UI). → template `portal-world`. |

## The identity (rules for every template)
1. **Base:** charcoal-navy dark (`bg #14181F`), never flat black boxes over him — dark only for full-screen
   pieces, with soft vignette / subtle grain.
2. **Accents (max two per shot):** gold `#F5B83D` = emphasis, signature, numbers. Sky blue `#3BA9F5` = lines,
   highlight word, map routes, UI. Red `#E53935` only for YouTube/CTA/"wrong". Green `#35D07F` only for
   "right/success".
3. **Text:** Arabic heavy (Cairo 800–900), white, with a dark soft outline/shadow so it reads over footage —
   same grammar as his thumbnails. ONE highlighted word per line in gold or blue. English: Montserrat 800.
   Quran/hadith: Amiri, calm, no pop.
4. **Shapes:** rounded pills (radius full) for tags/labels with an icon; cards radius 22; thin 3–4 px
   accent lines (diagonal slashes as decoration, like his 2026 designs).
5. **Media around him:** he is usually centered → photos float on either side (alternate), narrower (~34% width) with soft shadow, slight tilt (−4°…4°),
   thin white/gold border optional — never a fixed box layout; they enter from his side and leave.
6. **Mascot:** use for jokes, CTA (pointing / holding Subscribe), "coming up" — not in every shot.
7. **Signature:** gold calligraphy logo for chapter cards, end screen, watermark (small, bottom-left).
8. **Motion feel:** fast-in / soft-out (overshoot 5–8%), 8–12 frames in, 6–8 out; staggered reveals for
   lists/groups (like R19); camera push/scale for maps (like R20 / Kings and Generals).
9. **Sound:** one cue per visual event, under the voice.
10. **Captions ALWAYS ON** (Aly's rule): everything he says is written, word-by-word highlight (template
    `captions`), 16:9 bottom, 9:16 lower third. Corrected transcript, Egyptian spelling as spoken.
11. **Portal technique:** cut Aly out (`tools/matte.py`, RVM on CPU ≈ 4 fps at 1080p) and wipe the room
    into a motion-graphics world behind him with a diagonal slash (brand lines); he stays in front.

## Still to confirm with Aly
- Exact thumbnail font (looks heavy rounded Arabic; Cairo Black used as closest installed).
- Whether gold or blue is the primary accent (proposal: gold = emphasis, blue = structure).
