# Style library — learned from ALL of Aly's work (2026-10-06)

Sources studied (read-only, nothing modified): `F:\_root\output\Youtube` (2018–2026 channel projects),
`F:\_root\_archive\_working pc` (218 final exports) + `C:\_working pc\Archive reels` (published reels),
`F:\_root\output\180 Daraga` (events, sessions, Start Course, غطاء, elections, after-grad),
`Work\_Dolus` (AE course trailer + AE tutorial reels), `Work\...\Digital Glances` (portfolio),
`Work\...\Alaa Ramadan` (flat ad), `Work\...\Magdy Mansour` (voice-over only, no visuals),
inspiration excerpts (Statistics, PeaceCake, Fireship, Muqaddimah, CrashCourse, Kings&Generals, NDL,
MrBeast) + 3 Vox videos (frames streamed, not downloaded).
Evidence kept small: `references/style-sheets/*.jpg` (contact sheets, 6–8 frames per video) and
`references/style-sheets/palettes.json` (measured dominant colors per video). Lists in `.../lists/`.

## 1. The REAL identity (Aly, explicit): NOT colors
Channel identity = **logo/signature + subscribe keycap + intro/outro + Aly himself (+ mascot)**.
Colors change per video ("a red video, a green video, a blue video, a yellow video, an infographic video,
a Vox-like video, a Statistics-like video…"). Pick a **style pack** per video (section 3).
Constants in every video: gold calligraphy signature (`brand/logo/signature-calligraphy.png`),
subscribe_press keycap, captions always on, Aly present (cutout/zoom/move), mascot for jokes/CTA,
Genjutsu intro/transitions/outro only for > 5 min.

## 2. What his own work shows (by family)
| Family | Seen in | Look | Techniques to reuse |
|---|---|---|---|
| Channel talk 2025–26 | Genjutsu, AI comparison, Odyssey, delete silence | real room, cool blue/teal light vs warm, speaker center | pictures/thumbnails float around him, screen-record PiP, AI clips full-screen, cinematic interludes |
| AI film / AI reels 2026 | Higgsfield "The Incomplete Truth", Hercules, child video, Salah Jahin, the movie, r1–r11 | cinematic warm/dark, Disney-sunset magenta/orange/purple, film credits, gold festival laurel | letterbox, film titles centered serif caps, subtitles small white, "Original vs AI" split compare |
| Reel end card (standard!) | r3, r5, r7, r11, 0926 | black bg; top: white Arabic + red highlight ("عايز تعرف الفيديو ده اتعمل ازاي…"); center: long-video thumbnail; left: socials list; bottom: YouTube logo + "شاهد الفيديو كاملاً على YouTube" + avatar; right: QR | template `cta_endcard` |
| Vertical reel layout | 0926 | video top; 3-line Arabic caption block in black pills (white + yellow); bottom: YouTube + QR + thumbnail + his face cam | shorts with reference to long video |
| هو ايه (concepts) | R12 episodes | light grey vignette bg, magenta→orange gradient frame around examples, red YouTube source tag, keyed Aly vs patterned wall | gradient frame on screen content, source tag, subscribe keycap end |
| المجالات | R13 | Aly cut out (soft edge) in front of film/collage/UI worlds, warm grade, gold calligraphy chapter cards on black | portal_world |
| Old vblogs | v3, v5, v12, V14 | green-screen Aly over B-roll screens, stage footage with timecode, picture-in-picture | keyed background swap |
| Maps | V15, غطاء (180), Reel map (Dolus), v2 Manial | satellite map, red pin with calligraphy place name, green route line drawn, 3D tilted photo cards with shadow over map, colored district polygons | map_route / map_pin (todo), photo cards in 3D |
| Event / org (180 Daraga) | Start Course, New Stage, elections | deep purple-navy gradient + yellow condensed caps; unit charts (200 people icons, groups); teal bg + red Arabic "انا مين؟" | unit_chart (todo), number reveal titles |
| Corporate (Digital Glances) | portfolio | mint white `#E7F3EE`, green, navy pills, line pattern bg, 3D extruded bars on country map, big numbers | mint pack, map bars |
| Flat illustration ads | Alaa Ramadan, children (Behance) | pastel blue `#D1E6F9`, flat characters, product center, top headline | flat pack |
| Comparison videos | quick combination (cameras) | black, footage top, colored label + product photo + date bottom, socials footer | versus / product card |
| Tutorials | AE reels, AE trailer | screen recording full, zoom to UI, mint accent `#AAEBDD` | UI zoom + highlight box |

## 3. Style packs (choose ONE per video in plan: `"pack": "<name>"`; numbers in `brand/packs.json`)
| Pack | When | bg / panel | accents | text | Font (AR display) |
|---|---|---|---|---|---|
| `charcoal` (default) | tech, AI, tools | `#14181F` / `#1F2530` | gold `#F5B83D`, sky `#3BA9F5` | white | Cairo 900 |
| `cinema` | stories, history drama, AI film, intros | `#07080B` / `#16130F` | gold `#D9B165`, ember `#B5542E` | cream `#F2E9D8` | Reem Kufi / Amiri |
| `concept` (هو ايه) | definitions, "what is X" | `#B9B9B9→#8E8E8E` vignette / `#FFFFFF` | magenta `#E8175D`, orange `#F7931E` | `#1E1E24` | Cairo 900 |
| `map` (Vox × غطاء) | geography, history, places | satellite / paper `#EEE7D6` | red `#D7263D`, route green `#39B54A`, white dashed | white caps + black outline | Cairo 900 + calligraphy names |
| `mint` (corporate) | business, numbers, clean infographic | `#E7F3EE` / `#FFFFFF` | green `#1E8E3E`, navy `#1F3B57` | navy | Cairo 800 |
| `night` (180 events) | events, achievements, motivation | `#10002E→#33425C` gradient | yellow `#F9C80E`, violet `#7B2CBF` | white | condensed caps / Cairo 900 |
| `stats` (Statistics Easy) | teaching a concept step by step | blue `#0E5FA8` / grey `#A5A5A5` | green `#8BAF89`, white | white caps | Cairo 800 |
| `sunset` (AI Disney reels) | warm storytelling, emotion | `#160920` / `#41232D` | orange `#E2583E`, peach `#F6A04D`, gold `#D9B165` | cream | Reem Kufi |
| `flat` (illustration) | kids, simple explainers, ads | `#D1E6F9` / `#FFFFFF` | coral `#F26D5B`, mustard `#F2C14E` | `#24303A` | Cairo 800 |
| `peace` (PeaceCake-like) | comedy, reactions, talk | warm room | sticky yellow `#F4C430`, red tag `#E53935` | black on yellow | handwritten-ish / Cairo 900 |

## 4. Technique library (from his projects + Behance)
- Speaker as center of story; graphics around/behind him; rotoscope into worlds (R13, V14, after-grad cards).
- 3D tilted photo cards with shadow over a map; camera push from wide map to detail (غطاء, Vox, K&G).
- Unit charts (many person icons → groups → highlights) (Start Course R19).
- Growing hierarchy/tree (R11 file tree; Element 3D org chart).
- Gradient frame around screen recordings + small source tag (هو ايه).
- "Original vs AI" side-by-side with labels (r5, r7).
- Letterbox squeeze + dark stage + gold badges (Genjutsu outro/transitions).
- Mascot with mouth shapes / poses (2026 sheet) — pointing, holding Subscribe, reactions.
- Calligraphy titles for chapters and place names (FS_Diwany, Boutros, Hesham, AF_Diwani in his font library).
- Film grain, VHS look, 8-bit look (Genjutsu "8 bit" export), colorization before/after.
- Vox grammar: dashed borders, condensed caps labels with leader lines, highlighted region in red/orange,
  icon circles, B&W archive, big numbers in colored tags, yellow highlighter on documents.
- Statistics grammar: concept title → examples around one icon → branch lines into categories.
- PeaceCake grammar: yellow sticky card with handwritten Arabic, red/yellow comment stickers on a person,
  quick split screens of reactions.

## 5. Fonts
Installed & safe for renders: Cairo (var), Montserrat (var), Amiri, Reem Kufi, Noto Kufi/Naskh/Sans Arabic,
Rubik, Qahiri, Tasees Bold, Alef, Far_ArtBold, Cinzel. Seen in his AE projects: GE SS Text Bold, Myriad Arabic,
Montserrat, Alef, Reem Kufi, Noto Sans Arabic UI. His display-font library (calligraphy/decorative, ~350 files)
is in `F:\_root\output\180 Daraga\_Assets` — copy a specific font into `motion-library/public/fonts/` only
when a video needs it (license unknown → his own videos only).
