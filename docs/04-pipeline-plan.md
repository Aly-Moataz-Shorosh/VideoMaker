# Full pipeline plan (long-term)

Per video folder `V0001/` (numbered like reels-publisher).

1. Transcribe — faster-whisper (CPU, int8) → words with timestamps → numbered sentences file.
2. Clean cut — silences (keep Resolve step, or auto-editor which is free and exports Premiere XML)
   + mistakes/retakes: Claude reads numbered sentences, returns only IDs to drop. Aly confirms.
3. Edit plan — one Claude call: per sentence → visual type (broll / side_picture / side_video / motion /
   none), English search words, on-screen text, template id from `catalog.json`. Small JSON out.
4. Assets — free only: Aly's own library first (indexed with a local CLIP model on CPU), then Pexels /
   Pixabay APIs, Wikimedia Commons for history/geography. Download top 3 per slot; Aly picks.
5. Motion — fill library templates with plan data → render (Remotion CLI; nexrender for AE ones).
6. Timeline — OpenTimelineIO → XML for Premiere: V1 speech after cuts, V2 b-roll, V3 pictures,
   V4 motion, + captions SRT. Aly opens and polishes.
7. Shorts — Claude picks 3–5 clip ranges from the transcript → FFmpeg 9:16 + animated captions → into
   reels-publisher `01_Ready` (read its docs first; never break its rules).

## Phases
- Phase A (NOW): Motion Graphics Library (`05-motion-library-spec.md`).
- Phase 1: transcribe + mistake/retake removal → Premiere XML.
- Phase 2: edit plan + assets + full timeline.
- Phase 3: auto-fill motion from the plan.
- Phase 4: Shorts → reels-publisher.
