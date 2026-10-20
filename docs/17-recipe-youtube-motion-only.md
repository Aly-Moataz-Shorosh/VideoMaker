# Recipe: motion-only pass on Aly's finished long video (figmaMake, 2026-10-08)

Job: `projects/2026-10-07 youtube figmaMake` — his final edit (8:18, 60 fps) with HIS intro (114.45–116.0) and
outro+music (473.2–end) already placed, jump cuts done. Rules he gave: cut nothing, add no intro, NO motion and
no captions on his intro/outro, never > 3 s without motion/zoom, he is on the LEFT so graphics go RIGHT,
messy desk + weak light -> lots of impressive motion, screen recordings from `input/Screen Records` (numbered by
order, name = content), logos from the internet (never drawn), his style not Claude colors (pack `charcoal`).

## Steps
1. `python tools/transcribe.py <video> <proj>/work --prompt "Figma, Claude, ..."` (new `--prompt` = extra terms).
2. Whisper silently skipped 3 talking stretches (gap check did not catch them: words existed, hallucinated
   "هو هو هو"). Find them by long word gaps, then `work/scripts/fill_gaps.py <video> transcript.json a-b ...`
   splices new sentences G1.. in.
3. Intro/outro times by numbers (frame brightness / diff vs a room frame), not by watching.
4. Screen recordings: ONE contact sheet each (`work/sheets/rec*.jpg`) -> crop rects; hard-link them into
   `motion-library/public/projects/<code>/rec<N>.mp4` (`cp -l`, long names break python os.link).
5. Green-screen clips (`_branding/on video/youtube|instagram N.mp4`, read-only) keyed once:
   `chromakey=0x0AEE11:0.18:0.08,despill` -> VP9 alpha webm, cue `green_clip` (dx moves it to a free corner).
6. Plan = `work/scripts/make_plan.py` (helpers kw/zoom/screen/flow/portal/green; anchors = source seconds;
   `fill()` adds zoom fillers so no hole > 2.6 s; `plan.quiet` = intro/outro ranges, build_edit drops captions
   there and warns on cues). Caption spelling in `work/fix.json`.
7. `python tools/build_edit.py <proj> --name review_01` (mattes for portal_world ~3 min each), stills check,
   then `--render`.

## New templates (registry + catalog)
egypt_crowd, judge_scene (full-screen scenes from Aly's ideas), logo_flow, same_word, credits_drain, green_clip;
screen_ui got `hx/hw/htop/volume` for 16:9 side placement. Map data: `motion-library/src/data/world.json`
(Natural Earth 1:50m, public domain, equirectangular 3600x1800) + `blocks/geo.tsx` (MapPaths, fillPoints, Person).

## Gotchas
- Every Remotion bundle copies `public/` (now ~2 GB) into C:\Temp. 50 leftover bundles filled C: to 0 bytes.
  Use `sh stills_cli.sh` (one bundle in `motion-library/out/bundle`, `--timeout=240000` for the 60 fps source)
  and clean `C:\Users\alymo\AppData\Local\Temp\remotion-webpack-bundle-*` after renders.
- `stills.mjs` (renderStill in one browser) sometimes captures heavy SVG frames half-painted -> trust the CLI.

## Aly's review of review_01 (2026-10-08) — checklist before EVERY render
Liked (repeat): full-screen idea scenes from his notes (egypt_crowd, judge_scene); big photo BEHIND him (portal_world).
Fix (never again):
1. Greeting "علي شو": no calligraphy signature picture → `brand/video-blog-badge.png` or channel logo, or nothing.
2. Topic pictures start ON the word (portal on "تخرج", not before).
3. No cropped faces: `python tools/face_pos.py <img>` → side_picture `panFrom/panTo` (bottom→top ending on faces).
4. Green-screen clips stay on their native side (character enters from that edge). Never dx-shift/mirror them.
5. Tutorial steps = real screen recording + highlight box on EVERY click (screen_ui `marks`, frames from cue start).
   Find clicks: dense contact sheet of the recording, then full-res crops around the UI change.
6. Every tool he names gets its logo. Whisper drops English names → re-transcribe gaps with a names prompt
   (two different prompts must agree).

## Archived project (moved off this PC by Aly)
The figmaMake project folder may be gone. Reusable copies: `tools/recipes/figmaMake/` (make_plan.py, make_reels.py,
fill_gaps.py, fix.json — examples to copy into a new project's work/scripts), green-screen clips
`motion-library/public/brand/greenscreen/gs_*.webm`, his CTA clip `brand/clips/cta_comment_youtube_9x16.mp4`
(+ transcript; keep 7.06–12.01, keyword يوتيوب, already +8.5 dB). Paths inside the recipes point to the old project
folder — change PJ / paths when reusing.
