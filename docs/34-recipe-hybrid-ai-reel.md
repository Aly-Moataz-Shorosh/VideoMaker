# Recipe: hybrid AI reel / video (Aly not on camera) — Aly 2026-11-20

Goal (Aly): a video where some shots are his REAL footage with a new mouth (lipsync), some shots are a fully
GENERATED Aly (the AI makes his body/hand motion, not only the mouth), and the rest is B-roll + motion graphics
(Remotion / HyperFrames / three.js / Blender, Higgsfield for cinematic shots and 3D) so the video looks impressive.
Rules, ids, credits and test history: docs/33. Read 33 first.

## Shot types (plan every sentence as one of these)
| Type | Tool | When | Notes |
|---|---|---|---|
| A. REAL + lipsync | HeyGen create_lipsync (precision) on a clip of his base take | hook, personal lines, CTA | source clip MUST keep its audio track; enableDynamicDuration=false; base take = eyes on camera, calm, small gestures |
| B. GENERATED Aly | HeyGen digital twin (Avatar V) → create_video_from_avatar with our audio; fallback create_video_from_image (motionExpressiveness "less") | explaining lines, "AI Aly" moments | photo-only motion looked over-acted to Aly (hands down, shoulder up) → prefer the twin (needs his consent recording) |
| C. B-roll cinematic | Higgsfield generate_video / image (Seedance, Kling, Veo…) | scenes, metaphors, history, trends | estimate credits first (estimate_video_cost); 1 take, no auto re-rolls |
| D. 3D | Blender (tools/blender, EEVEE) or Higgsfield scene_builder_3d / generate_3d (GLB/.blend) → render in Blender or three.js | objects, models, "complex model that moves" | Higgsfield 3D gives the asset, Blender/three.js gives exact camera + motion control |
| E. Motion graphics | Remotion motion-library (default) / HyperFrames (local, free) | numbers, costs, lists, tool cards, captions | captions always on; cost tables = counter/bar templates |
| F. Screen | his screen recordings / Chrome screenshots of the tools | proof ("this is the real bill") | screen_ui template |

Density rule from docs/14 still applies (never > 5 s without a visual event). Avatar on screen ~30-40 % max in reels.

## Voice
- Best = Aly records the script himself (phone/mic, no camera). AI voice clones so far sounded "AI" to him:
  ElevenLabs instant clones (v1 + v2) and a HeyGen instant clone. Upgrade path = ElevenLabs Professional Voice
  Clone (Creator plan+, 30+ min RAW mic audio, not edited timelines).
- Name pronunciation: write "شُرُش" (Aly's own spelling) or "شُرُوش"; check the take before using it.

## Pipeline
1. Script (aly-content-assistant) with a SHOT column (A–F) per line → `<project>/script.md`.
2. Voice: his recording or TTS → `assets/ai/voice.wav`; transcribe.py → word timings.
3. Generate A/B shots per sentence (cut the voice per sentence), C/D shots in parallel; save every paid result +
   its .json (prompt/ids/credits) in `assets/ai/`.
4. Compose in Remotion (9:16), captions, sfx, music; ffmpeg loudnorm -14 LUFS; NVENC encode.
5. output/<name>.mp4 + .txt with the AI-disclosure line.

## Where to run it
- Claude Code on Aly's PC (open in this folder): renders (Remotion, Blender, ffmpeg/NVENC), direct uploads to
  HeyGen (no proxy), git. MCP servers in `.mcp.json` → `/mcp` → authenticate heygen, elevenlabs, higgsfield once.
- Cowork / claude.ai chat: planning, scripts, quick generations through the connectors, browser steps
  (consent pages, voice clone UI). Its cloud VM can't reach S3 → uploads go through Chrome (docs/33).

## Aly 2026-11-20 (after reading the first reel script)
- "مش عايز اسجل اي حاجة.. عايزه كله AI": default for this kind of video = FULL-AI mode: no new filming, no voice
  recording. Voice = ElevenLabs clone, face = HeyGen (photo avatar now; digital twin once he records the one-time
  consent clip), everything else generated or coded. Existing footage may still feed lipsync shots.
- Never forget Whisper (tools/transcribe.py, large-v3-turbo: word timings → captions + cue timing) and HyperFrames
  (HTML → video, free, local) in the tool list.
- Don't send viewers to "the link in the first comment": show his related long videos INSIDE the video (thumbnails +
  spoken titles, "دوّر عليهم في قناتي"). His AI long videos: «عايز تبدأ تعمل فيديوهات AI؟ شوف ده الأول»,
  «إزاي تعمل فيديو AI زي المحترفين وتعرف هيكلفك كام؟ | مسابقة المليون دولار», «الموديل ده فتح مستوى جديد.. Genjutsu»,
  «ازاي تعمل UI UX بالـ AI | Figma Make».
- He wants more detail per tool: what it does, its strongest power (one concrete example), and its cost.
- "عايز فيديو مبهر ومليان flexing، ومفيش ولا ثانية مفيهاش حاجة معقدة ومبهرة بصرياً وصوتياً": for AI-showcase videos the
  density rule tightens to a visual event every 1-2 s + a sound event on every visual event; no static avatar shot ever;
  each tool gets its own "flex moment" scene and a unique transition; second-by-second QC table before every review.
  Full checklist: projects/2026-11-20 avatar aiFullVideoCost/RUN_v2.md.
- Aly also wants cinematic camera work (orbits, hard moves) and the PLACE changing while he talks (e.g. talking inside a
  fighter-jet cockpit → the jet explodes into parts → he assembles it in a lab with precision tools; money = vault/hologram
  invoice). Tools: HeyGen cinematic avatar, Higgsfield character + video + lipsync, Blender exploded views. Storyboard
  with keyframes first, then video. See RUN_v3.md of the aiFullVideoCost project.
- Aly (2026-11-20): mix styles in one video — live action / cinematic 3D / toy-style 3D (ORIGINAL characters only) / 2D
  cartoon / HUD motion — and generate smartly: Blender grey blockout for exact motion + camera → Higgsfield video-to-video /
  motion control for the look ("we control motion, AI controls the look"); show before/after as a flex.
