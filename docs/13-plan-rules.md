# Plan rules (the ONE Claude pass per video/short → plan JSON)

Input: `work/sentences.txt` ([?] = low-confidence text) + `motion-library/catalog.json` + project
`notes.txt`. Output: plan JSON (schema in `tools/build_edit.py` docstring). Modes: `docs/14-production-modes.md`.

## Cutting
- Default `"cut": false` — Aly edits himself; keep his video whole. Only cut when asked (or dry runs).
- When cutting: keep the full idea; drop false starts/repeated takes (keep last clean one); `cut_words` for
  stumbles; check terms complete at cut edges; drop known Whisper hallucinations ("ترجمة نانسي قنقر").
- Shorts: `"range"` + `cut_words` so the short STARTS ON THE HOOK (strongest line), ends on a closed idea.

## Captions
- Automatic from all words. ALWAYS fix spelling in `fix` (sentence id → corrected text of the kept words):
  technical terms in English (DaVinci Resolve, Threshold…), Egyptian spelling as spoken, numbers as digits.

## Motion density (hard rule — Aly 2026-10-06)
- Max gap between visual events ≤ 5 s (shorts ≤ 4 s). Count `zoom` cues as events.
- Mix: BIG every 20–40 s (portal_world, bar_chart full, section_transition, steps_list), MEDIUM every
  5–10 s (side_picture, keyword_pop, counter, steps), SMALL fills gaps (zoom punch/push/out, icon_pop).
- Number said → counter. Comparison → bar_chart. Process/menu path → steps_list. Place → map (todo).
  Big topic entry → portal_world (Aly cut out, can slide with `alyX`). Emotion/joke → icon_pop + zoom punch.
- Never stack two medium graphics on the same side at once; alternate sides (Aly is centered).
- 9:16 zones: face top (0.12–0.40), graphics 0.40–0.66, captions ~0.66–0.75, platform UI below.
- Each cue explains what is said at that moment; text max ~5 words, one *highlight*.
- Long video (> 5 min) only: section_transition between parts + outro asset; none in reels/shorts.
- End: subscribe_press (youtube) or platform instagram for reels CTA when notes ask.

## Condensed shorts / CTA (Aly review 2026-10-06, RippleCutToll)
- `keep` edges only in real pauses between complete phrases — keep a phrase whole or drop it whole. Whisper gaps
  (missing English terms) are speech: never put a cut edge inside one.
- CTA clip: the LAST complete clean take as ONE range. Never splice two takes.
- Check numbers/signs against the UI (threshold = -20 dB, negative).
- Explain concepts with diagrams, not only labels. TODO templates: `threshold_wave` (waveform + dB line, below = silence
  removed, above = kept), `trim_handles` (clip with N frames kept before/after speech), `audio_crossfade` (two clips,
  audio overlaps and blends).
