# Recipe: several shorts from a TALKING video = style 15 glass-face-talk (graphictablet, 2026-10-21) — APPROVED "الفيديوهات ممتازة"

Job: `projects/2026-10-21 shorts graphictablet` — his 2022 video "أهمية الجرافيك تابلت" (12:20, YouTube Uc47QvWaocs). notes.txt:
style 10, CTA = "مش فيديو بوشي، اعملها بالطريقة اللي عملناها في ستايل 11" (read as: no face CTA clip, QR of the full video at the end),
face yes. Asked first (rule 00) → he picked 5 of my 8 ideas: **6 choose, 3 types, 5 math, 2 study, 7 unboxing**.

## His source (what to look for in a talking video)
- Talking head, he sits right of centre (face x ≈ 1030 of 1920). Camera modes `tfull` / `tlow` / `tlowr` / `wbig` / `tbig` (kit.tsx).
- **Picture-in-picture inserts** he put top-left (box x66 y314 806×452) — the frame slides so he moves right (`tlowr`). Found with
  `pip.py` (straight edge at the box's right side; short runs = noise, trust only long ones). Shown BIG on the stage with `tb_clip`
  (a crop of the same cam mp4) — real material, not a stand-in.
- **Full-frame footage** (his whiteboard photos, Word equation screen, unboxing, his brother drawing): camera `wbig` / `tbig`.
  Where the footage shows someone else (delivery 481.9–486.9) → `hide` + big cards so the screen is never empty.
- Unboxing part = music under him → Whisper missed words: re-transcribe that range with a prompt (`retr.py`, decode with ffmpeg;
  `vad_filter` on). Unsure words (button count "14"?) are hidden in captions (`--`) and not put on a card; official specs only with a link.

## Build (scripts in tools/recipes/graphictablet/)
`shorts_data.py` = pieces + scenes per short (source seconds) + caption fixes per sentence (same word count = word by word).
`make_shorts.py N…` → `short_N.json`, `voice_N.wav` (gain only, raw music pieces -8 dB), `cam_N.mp4`:
- camera = ONE decode, `split` → `trim=start_frame:end_frame` per piece → concat **in the short's order** (a `select=between(n…)`
  chain re-orders pieces back to source order and drops repeated frames — the hook came out in the wrong place).
- piece starts rounded to the frame the camera is cut at (voice uses the same start).
- scenes map source → timeline in order (a hook may repeat a later range: search from the previous scene's start).
`qc_cam.py` = picture gate (cam frames vs source frames). Note: `-ss` seeking shows a constant 1-frame "offset" — exact check by
frame number gave 0; the gate aligns to the frame grid. `render.sh` → `output/_raw/`, `finalize.py` → -16 LUFS limiter + CRF 23.

## Scenes (src/glass/tablet.tsx, all on the top stage y 0..~700, his camera below)
`tb_free` (declarative items: type / pill / card / logo / emoji / mark / word / tablet / monitor / pen), `tb_clip` (his insert big),
`tb_check` (9 tiles light up on his words, then ✓ on an example set + "مثال"), `tb_types` (Pen Display vs Pen Tablet),
`tb_map` (pen on the tablet → same stroke + cursor on the monitor), `tb_math` (LaTeX typed ✕ vs written formula ✓),
`tb_board` (his red-framed whiteboard: scribbles, then the story map with pins), `tb_rewind` (after a hook), `tb_end` (QR, middle).
Hooks: 5 math = the Word equation converting; 2 study = "summary in big handwriting" over the board photo; 7 = his brother's finished drawing.

## Review (2026-10-21)
All 5 "ممتازة". One rule: a QR of a YouTube video ALWAYS with that video's thumbnail → `tb_end` shows the thumbnail (glass card, 920 wide)
with the QR under it. v2 in `output/v2/` (v1 kept): only the end frames re-rendered (`--frames`) and spliced onto the v1 render with the
v1 audio (`v2_end.sh`), then `finalize.py --v2`. Frame counts equal, QR decodes.
