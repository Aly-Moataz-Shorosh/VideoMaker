# Recipe: faceless tutorial shorts, POP STUDIO look (ffmpeg, 2026-10-14) — NOT approved yet

Job: `projects/2026-10-14 shorts ffmpeg` — his 2021 FFmpeg lecture clip (6:12, YouTube 71aYvUDbqk8, dark screen recording, no face).
notes.txt: style "جديد" + 5 Behance links (Dtmg.tv showreel 2025, Graphic Design Portfolio 2026, Disney DNA, Multer Knows, ShakeUp).
Evidence sheets: `references/style-sheets/behance_*.jpg`.
Output: 3 shorts (`output/short_1..3.mp4` + txt, `sfx_only/`, `voice/`). Waiting for Aly's review.
1 = condensed whole tutorial (6 MB → 90 KB hook, google → site → bin → what it does → CMD → `ffmpeg -i "x.mov" "y.mp4"` → Enter → result).
2 = why ffmpeg.exe opens and closes (console program waiting for an input → -i = input).
3 = 3 ways to open CMD (address bar / Windows search / Win+R).

## Look 'pop' (src/pop/kit.tsx, composition film-short prop look 'pop')
- Electric violet `#4B1FE0` + neon lime `#B8FF3C`, pink / teal / yellow accents, lavender HUD `#E4E2FB` with blue mono text.
- 90 px moving grid + crosshairs + grain (PopBg); design-tool frame on top: corner brackets, `● FFMPEG.EXE 00:12:05`, `1080×1920` (PopFx).
- Scenes enter/leave with a PIXEL DISSOLVE (PScene). Figma selection boxes with 8 handles + name tag (SelBox), glossy smiley ball (Ball),
  big arrow cursor with lime click ring (Cursor), stretched italic echo type (Echo, Latin only), Arabic headline with lime/pink pills (Head),
  black ticker tape (Ticker), file cards (FileCard), cmd window + typing (Term/Typed), 3D keys (Key), polaroid of HIS real frame with
  handwritten note (Polaroid, font Aref Ruqaa), neon orbit ring (Orbit), simple-icons logos via CSS mask (Logo: ffmpeg, google, github, vlc, linux, apple).
- His dark 720p screen recording is NOT shown big (unreadable + upscale) — UI is rebuilt as clean vector, his real frame only as a small polaroid proof.
- Arabic text with Latin inside a Head/Note gets re-ordered by bidi ("Win + R" came out "R + Win") → put Latin-only text in Echo/Pill dir ltr.

## Pipeline = docs/19 (scripts copied to tools/recipes/ffmpeg/)
- transcript S001 was a Whisper hallucination (long "آآآ") → re-transcribed 14–40 s with a hint prompt and split into S001a..h.
- `make_shorts.py`: SPANS tuples can carry a forced start / end (`(a, b, a_force, b_force)`) measured on `edges.profile` when Whisper's
  start sits on the tail of the previous word. Two spans must never overlap (hook 321–330 + end 330 → the end scene covered the whole short).
- `partial` text is now used for full sentences too (spelling fix per sentence).
- CTA = `brand/clips/cta_comment_youtube_9x16.mp4` 7.0–11.95 (keyword يوتيوب), comment card at +0.6 s.
- Facts on screen come from his own screen: 5.95 MB (6,239,826 bytes) → ~90 KB, log shows libx264 → "codec H.264".

## Aly's review of v1 (2026-10-14) → v2
- Animation: "حلوين كا animation اوي". But the 3 split shorts each had INCOMPLETE info → he wants ONE short with the whole tutorial.
- New rules: always ASK "one short or several?" first; one = whole goal of the video; several = suggestions, he picks.
  No short ever reaches 3:00 (v2 first try was 3:01 → cut the spoken command recap to its last 4 s, dropped "خلص بسرعة").
- v2 = `output/v2/short_full.mp4` (2:43, 24 scenes, key 4 in make_shorts.py): hook → google → site (not source code) → GitHub → zip →
  folder → bin → what it does → why it opens & closes → CMD (+ the other 2 ways as pills) → drag ffmpeg.exe in → give it an input →
  `-i` → drag the video → command piece by piece → rename output → .mp4 trick → small vs 100 MB files → Enter → new file → result + CTA.
- New scenes `src/pop/f4.tsx`. `stills_cli.sh` now montages with PIL (ffmpeg tile dropped the first frames of big sheets).
