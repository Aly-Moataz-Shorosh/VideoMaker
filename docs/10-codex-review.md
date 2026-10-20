# Codex attempt — review (2026-10-06)

Source (read-only): `E:\root\output\Youtube\Aly Shorosh New\_Ai Video Maker`. Read: CLAUDE_HANDOFF, AGENTS,
READMEs, all key `learned\` files, Excel catalog (24 refs R01–R24), v03 plan, v04 structure, asset manifest.

## What was tried
1. Learning phase (Oct 1–2): indexed 24 reference projects from the Excel sheet, archived ~16 GB of
   selected evidence (hash-verified), wrote style notes (`learned\*.md`), sampled 8 inspiration channels.
2. Trial: auto-edit a vertical Short ("Ripple Delete Silence" in DaVinci) from raw footage. v01 → v04.
   Motion was drawn **frame by frame with Python/PIL** (`reel_v03.py`, `reel_v04.py`), audio mixed in numpy,
   XML exported for Premiere.

## Result and WHY it failed
| Version | Aly's verdict | Cause |
|---|---|---|
| v01 | Rejected | Arabic ASR dropped whole segments (38 s mid, 77 s at end) → missing content; silences/repeats left; static cards; CTA shrunk + green fringe. |
| v03 | Talk selection "much much better"; look rejected | Graphics/colors not his taste; layout = top title bar + face box + graphics box all the time ("sections"); procedural SFX loud and off-sync; Premiere logo redrawn; text cut ("Cross Fade ~~Audio~~"). |
| v04 | "Quality not suitable — don't try again now" | Same engine (PIL raster drawing) → low design ceiling; never checked in Premiere or by listening. |

Root causes: (a) raster drawing in Python can't reach motion-designer quality (no real easing, fonts, vectors,
layering); (b) one fixed boxed layout; (c) too much at once — a whole video per attempt instead of approving
pieces one by one; (d) technical checks treated as quality.

## Confirmed lessons (USER_CONFIRMED — follow them)
- Speaker and graphics move together in ONE frame; no permanent title bar / boxed sections. Split layout only
  for comparison or UI.
- Motion must explain meaning/relation/change (Statistics & Vox *function*, Aly's own feel), not label cards.
- Real logos only from official source, stored with URL + hash; never redraw.
- SFX: real, licensed, stored; one cue per visual event, under the voice. No default whoosh on every cut.
- No intro for Shorts/Reels or horizontal videos < ~5 min.
- No palette/font is "approved" yet; any look is a proposal shown as a style frame first.
- Don't copy inspiration channels' colors/characters. Don't take client (R22) colors as brand.
- Every on-screen term must be complete; check cut edges.
- Preferred refs: R01 Genjutsu + R14 AI comparison (current long style), R11 file-tree Short (best Short),
  R12 concept explainers, R19 shapes/numbers, R20 maps.

## Reused (copied, originals untouched)
- `brand/sfx/` 3 Mixkit SFX (woosh, pop, click) + `brand/logos-tools/` Premiere/DaVinci official logos;
  provenance in `brand/logos-tools/manifest-from-codex.json`.
- `references/from-codex/reel_v03_plan.json` — scene-plan JSON format (id, kind, title, clips[[in,out]],
  caption, note). Good base for our edit-plan.
- `references/from-codex/transcribe_media.py`, `transcribe_reel_raw.py` — faster-whisper scripts with ASR
  gap warnings. faster-whisper small/base models already downloaded in Codex `tools\models*`.
- Knowledge to keep pointing at (don't copy, too big): `learned\` notes, `reference-archive\`, Excel catalog,
  `START_HERE.html` portal.

## Conflicts with 03-decisions.md
1. **Engine.** Codex notes favor AE + MOGRT for motion. We chose Remotion. Resolution: Remotion fixes the real
   failure (PIL raster). Editability = each motion is a separate alpha overlay + its JSON props; change a prop →
   re-render that one piece. Heavy/special pieces stay in AE by Aly. Must show Aly that quality is high on the
   first stills before building more.
2. **Brand theme.** Codex: "no approved palette". We need a Theme → `brand/theme.json` is a *proposal v0*,
   approved via one style frame.
3. **Template spirit.** Spec lists cards (quote_card, chapter_title…). Per lessons, each template must sit in
   the speaker's frame (overlay on real footage), vary position/size, never become a fixed boxed layout.
4. Spec `side_picture` "frame next to speaker" is fine, but must move *with* the shot (enter from his side,
   respect his position), not a static box.

## Not reused
- `build_trial_project.py` (disabled by Codex after rejection), PIL motion code, procedural SFX.
