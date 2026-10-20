# Recipe: a recorded lecture → many viral shorts (New Stage 19, 2026-10-18/19) — look 'stage'

Job: `projects/2026-10-18 shorts newstage19shorts` = his 52-min talk "Digital Art" at New Stage 19 (ITI, 180 درجة), one static hall
camera. Inputs: `Main new.mp4` (his edit: 2-min home intro + lecture, 720p 1.4 Mb/s, face blur on others) and the RAW phone file
`20260908_103633.mp4` (720p HEVC 10-bit HLG, 8.6 Mb/s, no intro, no blur; raw = edit − 88.01 s, constant) + his PowerPoint.
Aly: "shorts viral", podcast-clip trick (hook sentence first, then back to the start), no CTA, only a side badge + QR + lecture picture.

## What he decided (reviews 2026-10-19)
- v1 (his hall camera in a small card, full-screen drawn scenes): rejected → **he fills the whole 9:16 screen the whole short**
  ("من تحت لفوق"), motion must work around him (zoom in/out, show part of the screen, mask part him / part motion).
- v2 roto pop-out (square card, his body stepping out): "سيئ جدا جدا جدا" — no matte on a far 720p camera.
- Quality: never upscale in the browser from his re-encoded edit; cut the camera from the RAW file (one Lanczos resample).
- Flat SVG drawings were "بدائي اوي و هندسي اوي" → Microsoft Fluent 3D emoji (MIT) as actors (`brand/fluent3d`, public/fluent).
- Faces of anyone but him must be blurred (his edit had it; the raw doesn't).
- Ideas: split the talk into every self-contained idea (44 → 30 shorts), no sentence used in two shorts (checked in shorts_data).

## Pipeline (`work/scripts/`, archived in `tools/recipes/newstage19/`)
1. `transcribe.py` (long pass) → `words.py a b` to read word times; `shorts_data.py` = per short: slug, head (headline, *box*),
   hook, pieces, cues (src_sec, kind, props, beats{src_sec}); `cap_words.py N` re-transcribes each piece → `caps.py` = corrected
   captions per piece (`@L ` = use long-pass timings when the piece pass is garbage).
2. `sync.py` (edit ↔ raw offset), `track_raw.py` (OpenCV HOG person detector, 4/s; keep only boxes with feet on the stage
   bottom ≥ 380 and height ≥ 200 — a roll-up banner was a "person"), slides → PNG via PowerPoint COM, slide media extracted.
3. `make_short.py N`: edges on the waveform with neighbour words (`edges.py` + prev/next word → never "اللي بعده"), the short's
   voice mp4 (hook | 0.9 s reversed "rewind" | pieces | 1.6 s tail), captions, cues → props, `tl_NN.json` (timeline + zoom keys).
4. `cam.py N`: RAW → zscale/hable tonemap → per-frame crop window that follows him (median + mean smoothing) with zoom keys,
   warpAffine Lanczos straight to 1080×1920, light unsharp, Haar faces blurred only in the audience rows (y > 1000), CRF 14.
5. `build.sh N…` = make_short → cam → bundle (only this short's cam in public) → render `stage-short` (crf 16) → `level.py`
   (−16 LUFS, peak ≤ −1, x264 CRF 18 slow) → `output/v3/NN_slug.mp4`; `make_txt.py` = titles/description/pinned comment.

## Look (`src/stage/`: kit.tsx, emo.tsx, emo2.tsx, StageShort.tsx)
- Frame: progress bar, "NEW STAGE 19 · DIGITAL ART NN/30", the hook question as headline (yellow box word) the whole short.
- His camera full screen (head kept at y≈430 under the headline), dark gradient top/bottom; punch-in zoom on key words; every
  piece alternates framing (1.0 / 1.18) = jump-cut energy; hook pushes in, then a VCR rewind (◀◀ + timecode) to the start.
- Captions under his feet (y 1050), 2–4 words, current word in a yellow box, highlighted words yellow/red.
- Tray over the seats (y 1150–1700): scenes drawn for the 830-px stage box, scaled 0.66: Hero, Vs (✓/✗), Flow (numbered),
  List, Count, AtmStory, Steps (16 dialogs), TShape, Dots (Jobs), his slide crops (`slide`) and slide videos (`clip`).
- Badge: small on the left (lecture thumbnail + QR + "المحاضرة كاملة"), grows to the centre in the last 2.6 s.
- 3D emoji are 256 px → show ≤ 256 px on the final frame (no upscaling).

## Review 2026-10-19 ("حلو اوي اوي ممتاز" + notes on 18 shorts) -> new versions in output/v3, old ones in output/v3/archive/
- Show the REAL thing: his slide videos/pictures (find which slide was on the projector with `proj_sheet.py`, crops via
  `prep_media.py`), his own YouTube videos as thumbnails + QR (`thumbs`), web clips he links (yt-dlp; long videos: cut the
  seconds straight from the stream URL with ffmpeg -ss), CC clips from Wikimedia Commons (3D printer, VR, AR, WING IT!).
- Explaining motion: `three.tsx` (three.js via @remotion/three: Mat3D = drag a material onto a ball, Looks3D = one bear in
  ad / cartoon / film renders, Rot3D = object that turns on "تلفّها"), `extra.tsx` (MapTour one moving map, PixVec, Flipbook,
  Pic with zoom in/out, Pics, Thumbs). Scenes can play inside the hook (`'_hook': True`).
- Edges: `(a, b, 'x')` = exact edges by hand when speech runs on (fit() clipped الفن / بحثية); finish the sentence at the end.
- Bleep: `bleep=[(src_a, src_b)]` mutes + beep sfx; caption shows ▬▬▬.
- Privacy: blur the WHOLE BODY of anyone but him with a soft feather (like his own edit) — cam.py: RVM people matte; him =
  matte inside a band around his tracked x; faces (Haar) outside his head = someone else -> their body blurred even in front
  of him (Aly: OK if it covers him a little). Camera = nearest standing person ON the stage (never follows a passer-by).
  FINAL (Aly 2026-10-19): "ال blur وحش.. وقف اي blur" -> cam.py BLUR = False; deliver unblurred, he blurs by hand.
- Speed: build.sh reuses work/cam/cam_NN.mp4 when tl_NN.json did not change (motion-only edits); FORCE_CAM="N ..." redoes it.
  Render concurrency 10 (20 cores). ⚠ On Windows, stopping a background task does NOT kill its children (bash build.sh loop,
  python cam.py, ffmpeg, remotion node) -> 3 builds ran at once, fought over out/bundle and public/, renders failed
  ("cannot decode grain_0.png"). Before restarting, kill them by command line (Get-CimInstance Win32_Process ... build.sh/cam.py/remotion).
- Camera QC: `qc_cam.py N..` (RVM matte at 2 fps; prints stretches where he is near the edge or missing) runs in build.sh.
  cam.py v5 tracks with the RVM matte: blob with feet 360–540 px nearest his last x, jump to the tallest stage blob after 1 s
  lost, every piece starts on the tallest stage blob (short 13 camera "stuck in the middle" = lost track → fixed by v5).
- ⚠ LIP SYNC (found on short 28, 2026-10-19): one joint `concat=v=1:a=1` padded every audio piece a little → voice drifted up to
  0.28 s late by the end. make_short.py now concats video and audio SEPARATELY (each audio piece atrim + apad=whole_dur to the
  exact piece length). Check with `qc_sync.py N` (audio vs raw camera offset per piece: must be constant, ~-0.04). Shorts built
  before this fix (all but 28 of the first delivery) still have the drift — rebuild only if Aly asks.
- Short 28 v2: hook = picture of the plane INSIDE the 3D program (behance_2.jpg), his slide 109 in the piece, nicer plane shot.

## Style 13 lecture-stage (APPROVED 2026-10-19) → styles/13 lecture-stage, scripts archived in tools/recipes/newstage19/

## 2026-10-19 (late) — camera lag in 28 + 4 more shorts (31–34)
- ⚠ Short 28 v2: his stage camera lagged behind the voice and FROZE at the end — build.sh had REUSED an old cam_28.mp4
  (built from the old timeline, 4.5 s shorter). Fix: build.sh now saves the timeline a camera was built from in
  work/cam/tl_NN.json and reuses the camera only if it is identical; then it fails the short if cam length ≠ short length (±0.15 s).
  qc_sync.py checks the VOICE vs the source only — it cannot see a stale camera; the length check does.
- Shorts 31–34 = lecture parts no other short used (find them: union of all hooks/pieces vs the lecture → gaps ≥ 20 s, read
  sents_timed.txt in each gap): 31 CS jobs change vs engineering, 32 who I am (180 ten years ago + B&W colourist card),
  33 Digital Art / Graphics names, 34 Q&A OpenAI "معرفش صراحة". Data in work/scripts/new_1019.py, TOTAL = 34 (1–30 rendered with /30).
- Which slide was on the projector: `proj_sheet.py out.jpg t1 t2 …` (projector crops of the RAW) + a contact sheet of slides/
  (slide_timeline.json auto-match is unreliable). Crop one card of a slide with Slide sx/sy/sw.
- Captions: `'و *Word*'` with a space — 'و*Anthropic*' glued و onto the Latin word.
