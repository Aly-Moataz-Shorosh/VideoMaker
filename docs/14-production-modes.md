# Production modes & standing rules (Aly, 2026-10-06) — READ before any video job

## What Aly will ask for (one project folder each, see `ابدأ هنا.md`)
| Mode | Input | Output | Intro/outro? |
|---|---|---|---|
| `reel-h` horizontal reel | his EDITED video (< 5 min) | 16:9 video full of motion + Premiere XML | NO intro, NO outro. CTA at end if he asks |
| `youtube` video (ANY length) | his EDITED video | 16:9 + XML | ONLY if the video is > 5 min: intro + section transitions + outro (Genjutsu R01). ≤ 5 min: none |
| `shorts` | a long video (local file or YouTube link → yt-dlp) | step 1: list of N proposed shorts with scripts (start/end, hook, title) → Aly says "نفذ" → step 2: N vertical 9:16 shorts, heavy graphics | NO intro. CTA/reference to long video at end |
| `shorts-raw` | RAW footage (not edited) | same as shorts, but each short is also cut: `"cut": true` (silences, false starts, repeated takes — rules in docs/13) | NO intro |
| `faceless` | voice-only video / audio | every second covered by full-screen motion/infographics (no talking head) | per length rule |

- **Aly now edits himself** (cuts, takes, silences). Default = NO cutting (`"cut": false`): keep his edit, only add motion.
  Exception: folder type `shorts-raw` → `"cut": true` per short. Type is the 2nd word of the project folder name.
  (Our auto-cut dry run worked but cutting is not the focus.) Cut only if he asks.
- **Do not re-make a delivered video** unless asked.

## Motion density (hard rule)
- **Never more than ~5 s without something that wows**: graphic, infographic, chart, keyword, picture,
  smart zoom, portal, moving Aly. Plan check: max gap between visual events ≤ 5 s.
- Mix levels: big moments (portal / full-screen infographic / chart) every 20–40 s; medium (picture,
  keyword, counter) every 5–10 s; small (smart zoom punch / push) fills the rest.
- Graphs/infographics wanted whenever a number, comparison, list, process, place or time is said.
- Smart zoom: punch-in on emphasis/jokes, slow push on serious lines, zoom-out on reveal. When Aly is
  cut out (matte), he can MOVE (slide aside, shrink) to make room for graphics.

## Long-video identity (Genjutsu R01) — decided by ACTUAL duration > 5 min, not by folder type
- Intro: hook first (few lines) → cinematic identity sting → content.
- Section transitions: letterbox squeeze (cinema bars) → dark "old movie" stage with dancing mascot,
  gold "VIDEO BLOG / علي شو / ALY SHOW" badge + gold signature → back to Aly. Template `section_transition`.
- Outro: letterbox squeeze → dark stage, mascot dances, subscribe keycap pressed + bell, gold badges.
- REAL clips (copied from Genjutsu final into `brand/clips/`, cue `brand_clip`): `genjutsu_intro_sting` 4.4 s,
  `genjutsu_transition_a` / `_b` ~1.7 s (use dur 1.6 — last frames return to the room), `genjutsu_outro` 25.8 s
  (starts with letterbox squeeze over room). AE source: `F:\_root\output\Youtube\Aly Shorosh - From 2026\
  4- harry potter before and after\the old movie.aep`; alt outro render `_branding\outro_1.mov`.
  Remotion fallback: `section_transition`. brand_clip covers his footage → put it at section breaks; in his
  own edits prefer placing it via the Premiere XML (V2) so his timing is untouched.
- Reel CTA end card (his standard): template `cta_endcard` (question + promise, long-video thumbnail,
  socials, YouTube line + avatar, QR from `props.qrUrl`).

## CTA
- **From now on (Aly 2026-10-06): the reel CTA will be a VIDEO of Aly saying "write <word> in a comment"**
  (ties to his instagram-comment-dm automation). Details pending from Aly — ask for them before building.
  Until then: don't invent CTA wording; cta_endcard / subscribe_press only if he asks.
- Reels he shoots himself: CTA at the end (follow / subscribe / watch full video). Templates:
  `subscribe_press` (YouTube) — follow variant for Instagram. His older green-screen CTA clips:
  `_branding\on video\youtube 1-3.mp4, instagram 1-3.mp4` (key once with FFmpeg if reused).

## Rotoscope
- First RVM mobilenet result "not good enough" → use better model/settings + edge refine; verify on a
  zoomed crop before using.
