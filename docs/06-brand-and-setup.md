# Brand & setup — DISCOVER, don't ask

Aly does NOT want to fill forms. Find every item yourself from his folders, then show him ONE short
Arabic summary ("لقيت كذا وكذا — صح؟") and ask only about what you truly couldn't find.
Write the findings below (English) and build `brand/theme.json` from them.

## Where to look (read-only)
- Codex folder: `E:\root\output\Youtube\Aly Shorosh New\_Ai Video Maker` (see `07-learn-from-codex.md`),
  especially `knowledge-base\` and `knowledge-base\External_Projects_Catalog*.xlsx`.
- His YouTube/project root: `E:\root\output\Youtube\` (past projects, exports, assets).
- Installed fonts: `C:\Windows\Fonts` and `%LOCALAPPDATA%\Microsoft\Windows\Fonts` (match names found
  in projects).
- Public pages if needed: YouTube channel, Behance (http://be.net/shorosh).

## How to find each item cheaply
| Item | How |
|---|---|
| Colors | logo files / theme files / CSS or JSON in knowledge-base; else sample 1 thumbnail image |
| Fonts (AR + EN) | font names inside .prproj (gzipped XML: `gzip -dc` + grep font), .mogrt/.json, AE files (strings + grep), then confirm installed |
| Logo | search `*logo*` (png/svg/ai/psd) under E:\root\output |
| Resolution / FPS | `ffprobe` on 2–3 recent final exports (no frame reading) |
| Speaker position (left/right/center) | extract ONE frame of a recent video with ffmpeg and view it |
| Green screen or normal background | same single frame |
| Digits (١٢٣ vs 123) | from existing on-screen text in projects/thumbnails; default Western if unclear |
| Style references | `knowledge-base\reference-*`, `learned\`, EXTERNAL_SOURCES.md, the xlsx catalog |
| SFX library | search folders named sfx / sound / whoosh / audio |
| Premiere / AE versions | `C:\Program Files\Adobe\` folder names |
| Node.js / ffmpeg / python | `node -v`, `ffmpeg -version`, `python --version` |
| Most-used motion types | read past project names + catalog + learned notes; infer, then propose top 5 |

## Findings (2026-10-06)
- Colors: no approved palette (Codex confirmed). Evidence: R01 intro uses gold Arabic signature; room has
  gold-framed art + cyan/blue light. Proposal v0 in `brand/theme.json`: deep navy base, warm gold accent,
  cyan secondary, off-white text. Needs Aly's OK on one style frame.
- Fonts AR / EN: user-installed (= chosen by Aly): Cairo (variable), Montserrat (variable), Qahiri, Tasees,
  Far_ArtBold, Cinzel, TECHNO*. System: Amiri (+AmiriQuran), Noto Kufi/Naskh/Sans Arabic, Reem Kufi, Rubik.
  No font names recoverable from his AE/Premiere projects. Proposal: Cairo (AR UI), Montserrat (EN),
  Amiri (religious), Reem Kufi / Qahiri (display titles, optional).
- Logo path: no clean channel logo file found. Candidates: `E:\root\output\Youtube\Aly Shorosh New\_branding\`
  (`VIDEO BLOG.png`, `NewLogo Without Back to mo'men.psd`, character sheets, `pp 2.png`),
  `E:\root\output\Videos\the-incomplete-truth\shorosh vision logo.png`. Ask Aly.
- Resolution / FPS: long videos 1920×1080 @ 30 fps (`delete silencef.mp4`); some exports 29.97. Shorts
  1080×1920 @ 30. Use 30 fps.
- Speaker position: center-right, waist-up, talking to camera (frame from `delete silencef.mp4` @20 s).
  Free space mostly on the LEFT → default `side: left`.
- Background: real room (desk, monitors, gold-framed Islamic art), cyan/blue light right, warm left. No green
  screen.
- Digits: unknown → default Western (123), setting in theme.
- Style references: Codex `knowledge-base\learned\` (see docs/10). Prefer R01, R14, R11, R12, R19, R20.
- SFX folder: none of his own. 3 Mixkit SFX copied to `brand/sfx/` (license in manifest).
  Free source to add later: Mixkit (no attribution needed).
- Premiere / AE versions: CC 2020 (Premiere, AE, AME, Audition, Illustrator, Photoshop).
  ⚠ Verify Premiere 2020 imports ProRes 4444 alpha on Windows; fallback = QuickTime PNG (alpha) or
  PNG sequence.
- Node / ffmpeg / python: Node v24.12.0, ffmpeg 2024-09 build, Python 3.13.1. F: drive not connected now.
- Proposed top-5 motions: side_picture, keyword_pop, map_highlight, counter, captions_word
  (then history_timeline, versus, bullet_list).
- Still unknown (ask Aly in ONE message): which file is his logo/avatar to use.
