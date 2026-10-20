# Motion Graphics Library — spec

## Goal
One reusable library that covers almost everything Aly puts on screen: pictures/videos next to him,
text, numbers, maps, timelines, transitions, branding, Shorts captions. Aly can later ask for new ones
in Arabic ("عايز موشن يعمل كذا") and they get added the same way.

## Engine and structure
- Remotion project in `motion-library/` (Node.js + TypeScript). One folder per template.
- `motion-library/catalog.json` = single source of truth: id, Arabic name, category, props schema,
  default duration, formats, output type, priority, status. The edit-plan step (later) reads ONLY this
  file to choose templates — keep descriptions short.
- Shared building blocks (write once, reuse everywhere): `Theme` (colors, fonts, radius, shadows from
  `brand/`), `TextAR` (RTL, Arabic shaping, auto-fit size, Arabic or Western digits per setting),
  `Enter/Exit` animations (slide, scale-pop, fade, wipe, mask-reveal), `MediaFrame` (rounded frame,
  border, shadow, Ken Burns for stills), `SafeArea` (16:9 and 9:16), `SpeakerSide` (left/right).
- Every template: props in, render out. Props validated with zod. Defaults for everything so a template
  renders even with minimal data.
- Formats: 1920×1080 and 1080×1920 (4K only if Aly needs it). FPS from `06-brand-and-setup.md`.
- Output: overlays → ProRes 4444 with alpha (.mov) to drop above the speaker in Premiere.
  Full-screen pieces → H.264/ProRes normal.
- Optional SFX per template (whoosh/pop) from Aly's free SFX folder, exported as a separate WAV or
  embedded — ask Aly which he prefers.
- File naming of renders: `<videoCode>_<order>_<templateId>_<startTC>.mov` so Premiere placement is easy.

## How to add a new template (the loop — keep it cheap)
1. Aly describes it in Arabic (+ optional reference link/screenshot in `references/`).
2. Claude writes the component reusing building blocks, adds it to `catalog.json`.
3. Render ONE still PNG at the most important frame → Aly approves look.
4. Render a short preview video → Aly approves motion.
5. Mark status `ready` in the catalog. Note any learnings in `CLAUDE.md` "Current state".

## Catalog (P1 = build first)

### A. Media around the speaker
| id | Arabic name | Use | Main props | P |
|---|---|---|---|---|
| side_picture | صورة جنبي | picture next to Aly while he talks | src, side, caption?, enter, kenBurns | P1 |
| side_video | فيديو جنبي | video clip next to Aly | src, side, trimIn/out, caption? | P1 |
| fullscreen_picture | صورة ملء الشاشة | picture covers screen, Ken Burns | src, caption?, direction | P1 |
| picture_stack | صور ورا بعض | 2–5 photos stacking like polaroids | srcs[], captions[] | P2 |
| picture_grid | شبكة صور | 2–6 images grid reveal | srcs[], titles[] | P2 |
| before_after | قبل وبعد | split / slider compare | srcA, srcB, labels | P2 |
| media_with_source | صورة بمصدر | picture + small source credit | src, source | P2 |

### B. Text
| id | Arabic name | Use | Main props | P |
|---|---|---|---|---|
| keyword_pop | كلمة مهمة | one key word/phrase pops on screen | text, side, style | P1 |
| lower_third | تعريف شخص/مكان | name + title bar | title, subtitle | P1 |
| chapter_title | عنوان جزء | section/chapter card | number, title | P1 |
| bullet_list | نقط ورا بعض | points appear one by one | items[], timings[] | P1 |
| quote_card | اقتباس | quote/saying with author | text, author | P1 |
| religious_quote | آية/حديث | respectful calm style, source line | text, source, kind | P1 |
| question_card | سؤال | question to the audience | text | P2 |
| definition_card | تعريف مصطلح | term + short meaning | term, meaning | P2 |
| top_list_number | رقم الترتيب | "رقم 3" style for top-N videos | number, title | P2 |
| cta_subscribe | اشترك | subscribe / follow reminder | handle?, platform | P2 |

### C. Numbers & data
| id | Arabic name | Use | Main props | P |
|---|---|---|---|---|
| counter | رقم بيعد | number counts up | value, prefix, suffix, label | P1 |
| percent_ring | نسبة | circular percentage | value, label | P2 |
| bar_chart | أعمدة | compare 2–8 values | items[{label,value}] | P2 |
| versus | مقارنة | X vs Y two columns | left{title,points}, right{...} | P1 |
| history_timeline | خط زمني | events on a timeline | events[{year,label,img?}] | P1 |
| process_steps | خطوات | step 1 → 2 → 3 | steps[] | P2 |

### D. Geography (no paid APIs: Natural Earth public-domain shapes + d3-geo)
| id | Arabic name | Use | Main props | P |
|---|---|---|---|---|
| map_highlight | تحديد دولة | zoom map + highlight country/region | countries[], label | P1 |
| map_route | سهم بين مكانين | animated path between places | points[{name,lat,lon}] | P2 |
| map_pin | دبوس مكان | pin + name on a map | lat, lon, label | P2 |
| map_compare_size | مقارنة مساحات | overlay one country on another | a, b | P3 |
Needs an Arabic-names lookup for countries/cities (build once).

### E. Attention & transitions
| id | Arabic name | Use | Main props | P |
|---|---|---|---|---|
| arrow_point | سهم بيشاور | arrow pointing to a spot | x, y, label? | P2 |
| circle_highlight | دايرة تحديد | hand-drawn circle around something | x, y, w, h | P2 |
| icon_pop | أيقونة | emoji/icon pops near Aly | icon, side | P2 |
| section_transition | انتقال | full-screen transition between parts | style, title? | P2 |
| glitch_flash | فلاش | short accent hit | style | P3 |

### F. Branding
| id | Arabic name | Use | Main props | P |
|---|---|---|---|---|
| intro | مقدمة | channel intro | title? | P2 |
| end_screen | نهاية الفيديو | YouTube end-screen layout (safe zones) | nextTitle? | P2 |
| socials_bar | حساباتي | handles of all platforms | handles[] | P3 |
| watermark | لوجو صغير | corner logo | position | P3 |

### G. Shorts / Reels (9:16)
| id | Arabic name | Use | Main props | P |
|---|---|---|---|---|
| captions_word | كابشن كلمة بكلمة | animated Arabic captions from whisper word timestamps | words[{w,start,end}], style | P1 |
| short_hook_title | عنوان أول الريل | big hook text first 2 s | text | P2 |
All P1 templates in A–C must also render in 9:16.

### H. Tutorial / UI (built 2026-10-06, see docs/16)
| id | Arabic name | Use | Main props | P |
|---|---|---|---|---|
| screen_ui | تسجيل شاشة مقصوص | real software UI crop + highlight marks | src, start, crop, crop2, marks[] | P1 |
| threshold_wave | موجة وحد الصمت | explain a dB threshold | db, silenceAt, keepAt | P2 |
| trim_handles | قبل وبعد القطعة | explain pre/post handles | preAt, postAt | P2 |
| audio_crossfade | الصوت يدخل في بعض | explain an audio cross fade | overlapAt, doneAt | P2 |
| comment_cta | اكتب كلمة في كومنت | comment-keyword CTA (comment→DM automation) | keyword, dm | P1 |

## Not in Remotion
- Heavy particle/3D/realistic effects → After Effects by Aly (optionally nexrender later).
- AI-generated video → manual, marked `manual` in plans.
- Green-screen stock → keyed once with FFmpeg into the library (`assets/elements/`), not templates.
