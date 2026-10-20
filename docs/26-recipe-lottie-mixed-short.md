# Recipe: tutorial short in a MIXED look (aftereffects to code, 2026-10-16). APPROVED v3 ("ده ممتاز حلو اوي") = style 12 

Job: `projects/2026-10-15 shorts aftereffects to code` = his 2021 video "After effects animation to a Code" (YouTube 5C4KNFiJFjA, 39:36,
720p screen recording + webcam in the bottom-right corner; big webcam only 0–26 s). Notes: style "2 and 6 and 10", CTA yes, face yes.
Asked first: ONE full short → `output/short_1.mp4` (2:51 incl. CTA).

## Look 'lottie' (`src/glass/lottie.tsx`, film-short `look: 'lottie'`)
- 02 → grainy two-blue background (`LottieBg` = the reels GrainBg textures, grain 0.5).
- 10 → glass cards, typed titles + gold pill, chips, cursor, his face always on (Cam modes `lbig` / `lmini` in glass/kit.tsx).
- 06 → light VHS: scanlines 0.1, faint tracking band, "▶ PLAY SP 0:00:12" OSD top-left with RGB fringe (`LottieFx`).
- Motif: HIS animation (circle filling with red water + red stripe) rebuilt as vector `Liquid`, used in hook / buttons / hover / end.
- Code is a clean vector editor (`Code`, typed on his words) — the 720p recording is unreadable when shrunk. Real screen only where it
  is readable: AE Bodymovin panel clicks, browser result, the smileys test.
## Structure (style 11 order): hook (Play/Pause demo) → what → tip (effects don't export) → plugin → install → export → player.js →
server (XAMPP) → code → run + loop → no pixelation → autoplay + buttons → hover → test (shape layer 4 KB) → end chain + QR → CTA.
## Gotchas
- 720p source → cam.mp4 is upscaled to 1920x1080 (lanczos) so Screen/Cam px stay 1080p.
- English pills inside RTL: use "→" not "⬅"; flex rows inside the vector Browser need `direction: ltr` (PLAY/PAUSE flipped).
- First cut was 3:20 → removed 7 pieces to 2:51 (rule: never ≥ 3:00).
Scripts: `tools/recipes/aftereffects2code/` (make_short.py, write_meta.py, export_sfx.py, render.sh).

## Review 1 (2026-10-16): v1 2:51 "طويل على الفاضي" → v2 1:01 (`output/v2/short_1.mp4`, make_short_v2.py)
Aly: simpler and faster, the CTA sends them to YouTube anyway. His outline = hook, after effects, download, convert to json, code,
result, vector and compare, summary → 11 pieces, one sentence each (tip, install, player.js, server, loop, buttons, hover dropped).
Scenes reused; new props `n` (chip number) and `stepKeys`; LtCode types all lines fast when it has only the load beat.

## Review 2: v2 "احسن بكتير… متوصل ببعضه و مفهوم" + 4 fixes → v3 1:23 (`output/v3/short_1.mp4`, make_short_v3.py)
Intro sentence kept to "Android Application أو ويب سايت"; new `lt_aelook` (his AE comp 27.6 s) before the export; new `lt_use` (his real
browser 1541.9–1546.5 with PLAY/PAUSE boxes, no zoom = NOZOOM, then 3 animations with their own buttons + "game"); `lt_eff inside` =
"Shape Layer = مرسوم جوه After Effects" + "أكتر حاجة بتوفّر مساحة". Gotchas: Pill color must be a hex (rgba + 'DD' = invisible);
Latin units inside an Arabic pill flip ("4 KB بس") → write "4 كيلو بايت".
