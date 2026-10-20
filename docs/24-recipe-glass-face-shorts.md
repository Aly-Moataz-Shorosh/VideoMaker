# Recipe: ONE full short with his face ALWAYS on screen, GLASS look (lighting, 2026-10-14) — APPROVED ("الستايل حلو", 2026-10-15) = style 10

Job: `projects/2026-10-14 shorts lighting` — his video "lighting your setup" (12:41, YouTube o7QYL5qIY84, phone camera, room
goes dark → key → back → ambient cyan → manual focus). notes.txt: style "new style", "motion all the time but I'm visible the
whole video, it's about light so we must SEE the effect", CTA yes. Asked first (rule 00): ONE full short → `output/short_1.mp4` (2:49).
Style reference (his link): Behance S.r. Seth "Portfolio 2026" — SaaS animations (frosted glass cards on soft glowing gradients,
words typing grey → white with one word in a pill, cursor clicks, toggles, glowing dot on curves) + podcast shorts (speaker always
on screen, big caption with a highlighted word). Evidence: `references/style-sheets/behance_seth_*.jpg`.
Behance Vimeo embeds need the Behance referer: open the player URL in the browser pane and read `window.playerConfig` (HLS url) → ffmpeg tile.

## Look 'glass' (src/glass/kit.tsx + scenes.tsx, composition film-short prop look 'glass') — HIS channel colours, not the ref's
- Charcoal-navy bg with drifting sky-blue / royal glows + fine grain (GlassBg). Gold pill = highlighted word, sky blue = second accent.
  Light colours of the topic: key #FFF4E0, back #FFB23F, ambient cyan #35E0F2.
- Glass card, Type (`*word*` gold pill, `[word]` blue, `_` = space inside a pill), Chip (chapter "01 Key Light · الضوء الأساسي"),
  Toggle + Studio panel ("Light Studio": one row per light, flips ON with a cursor click on the moment the light turns on in his video),
  Cursor, Orb (glowing light dot), Sphere (2D disc → 3D by shading, hard/soft shadow), Bust (vector head lit from an angle, rim light),
  wall/side diagram, spill (bulb rays → foil cap → one beam, grid), LED strip, phone with Manual Focus slider, before/after wipe.
- `Cam` = HIS CAMERA ALWAYS ON SCREEN: one mp4 of the kept pieces (make_short.py builds `cam.mp4`, keyframe every 15) + layout keys:
  full (9:16 crop, opening), low (big in the lower part, graphics stage = top 0..~720), wide (whole 16:9 room in the middle — used on every
  "light turns on" moment so the room is visible), mini, hide (only where his source shows someone else's photo). Edges melt (mask), no hard box.
- Silent "light turns on" moments are kept as raw pieces (his music under them at a fixed -8 dB, 0.25 s fades, no levelling).

## Pipeline (scripts copied to tools/recipes/lighting/)
fetch → transcribe (prompt with the light terms) → contact sheets (1/12 s whole video + 1/3 s and dense strips around the reveals) →
`make_short.py` (PIECES with chapter tags, TXT caption text per sentence = same word count as the kept words, SCENES beats, CAM keys,
SFX) → `check.sh`-style stills (stills_cli.sh) → `render.sh 1` → `write_meta.py`, `export_sfx.py`, voice copy.
Length: first cut was 2:59.8 → trimmed to 2:49 (never ≥ 3:00).
