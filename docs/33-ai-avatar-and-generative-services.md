# AI avatar + voice + generative video (HeyGen / ElevenLabs / Higgsfield) — Aly 2026-11-20

Aly's decision (2026-11-20): he wants videos/reels where he is NOT on camera: his face + body = a HeyGen
avatar, his voice = an ElevenLabs clone (Egyptian Arabic), script written in his style, set in a professional
studio. He bought / signed into all three services. This is the ONLY approved exception to the
"free tools only" rule (see CLAUDE.md hard rules). Everything else in the pipeline stays free and local.

## 1. Services and their job (one job each — don't mix)
| Service | Job in our pipeline | Connect (Claude Code) | Cost |
|---|---|---|---|
| ElevenLabs | Aly's VOICE: clone + text-to-speech in Egyptian Arabic, voice isolation (clean his old audio) | MCP `elevenlabs` → `https://api.elevenlabs.io/v1/mcp` (OAuth, no API key) | credits per character |
| HeyGen | Aly's FACE/BODY: avatar (digital twin from video, or photo avatar), lip-sync to OUR audio file, studio backgrounds | MCP `heygen` → `https://mcp.heygen.com/mcp/v1/` (OAuth) | credits per minute of video |
| Higgsfield | CINEMATIC B-roll only: generated shots/scenes (history reenactment, trend visuals, camera moves), images for plates/textures | MCP `higgsfield` → `https://mcp.higgsfield.ai/mcp` (OAuth, needs paid plan) | credits per generation (expensive: ~6-10x HeyGen per 10 s) |

All three are declared in `.mcp.json` (video-maker root AND the project root). First time: in Claude Code run
`/mcp` → pick each server → Authenticate → sign in in the browser. Check: list voices (ElevenLabs), list
avatars (HeyGen), remaining credits (HeyGen / Higgsfield).

Comparison that decided the split (2026-11-20 research): HeyGen = best lip-sync accuracy + same face across
many videos (daily reels need ONE stable "Aly"); Higgsfield = better cinematic motion/physics but weaker
identity consistency and much more expensive → B-roll, not the talking head.

## 2. Hard rules for this mode
1. **Credits:** before EVERY paid generation say in one line what it will cost (seconds / characters / credits)
   and what's left. Generate the SHORTEST thing that proves the point first (test = 5-10 s). Never loop
   re-generations automatically — if a result is bad, stop and show Aly.
2. **Voice:** always generate audio in ElevenLabs FIRST, then send that audio file to HeyGen for lip-sync.
   Never use HeyGen's own TTS for Arabic (Egyptian is better in ElevenLabs). Script = Egyptian colloquial,
   short sentences, his words (use the `aly-content-assistant` skill to write it). Add diacritics/spelling hints
   only where a word is mispronounced.
3. **Consent / identity:** only Aly's own face and voice. Creating the HeyGen digital twin and the ElevenLabs
   Professional clone needs Aly himself (consent video / verification) — tell him, don't try to automate it.
4. **Disclosure:** realistic AI Aly must be labeled on YouTube ("altered or synthetic content"), Instagram/
   Facebook ("AI info") and TikTok (AI-generated label). Put this in the delivery .txt every time.
5. **Avatar screen share:** in reels the avatar is on screen ~30-40% max; the rest = B-roll, screenshots,
   motion graphics (motion density rule in docs/14 still applies: never > 5 s without a visual event).
   Personal / emotional / reaction content → Aly films himself; info / explainer / trend summary → avatar.
6. Keep every paid output (wav, avatar mp4, higgsfield clips) in `<project>/assets/ai/` with a `.json` next to
   it (prompt, voice/avatar id, settings, date) so we can re-use instead of paying again.

## 3. Pipeline (script → finished video)
1. Script (`aly-content-assistant`) → `<project>/script.md` (Arabic text + per-sentence visual notes).
2. ElevenLabs TTS with Aly's cloned voice → `assets/ai/voice.wav` (+ split per sentence if B-roll timing needs it).
3. `tools/transcribe.py` on voice.wav → word timings (captions + cue timing), same as his real recordings.
4. HeyGen: avatar + `voice.wav` as audio source → `assets/ai/avatar.mp4`. Background: green/plain if we will
   composite in Remotion (preferred — we control the studio), or a HeyGen studio background for quick tests.
5. (optional) Higgsfield: B-roll shots for the sentences that need a scene → `assets/ai/broll_NN.mp4`.
6. Composite in Remotion like any of his edits: `matte.py` (or HeyGen green bg → chroma key) → studio
   background → motion-library templates (keyword_pop, side_picture, counter, maps, …), captions always on.
   9:16 for reels, 16:9 for YouTube. Same plan/build_edit flow as docs/13 + docs/14.
7. ffmpeg: loudnorm (-14 LUFS for reels), final encode (NVENC on Aly's PC), `output/<name>.mp4` + `.txt`
   (title, caption, hashtags, AI-disclosure line).
8. Ready reels → his reels-publisher `01_Ready` folder only if he asks.

## 4. The "professional studio" — 3 ways (cheapest first)
- A) Remotion: our own studio background (blurred set, LED lines, logo wall from `brand/`) behind the matted avatar.
- B) three.js in Remotion (`@remotion/three`, already used: sound3d.tsx, set3d.tsx) — a 3D studio set with slow
  camera drift; avatar as a plane/video texture.
- C) Blender 5.2 (`E:/root/_assets/programs/Blender Foundation/Blender 5.2`, scripts in `tools/blender/`,
  EEVEE, GTX 1050 Ti ~1-3 s/frame) — the most realistic set (like biz ep01 RWA studio). Render the set ONCE
  as a loop/plate per camera angle and reuse it for every avatar video (don't re-render per video).
  Higgsfield images can be used as textures/backdrops/plates inside Blender or Remotion.
  Optional later: `blender-mcp` (community MCP + Blender add-on) for live scene editing from Claude — not
  installed; our headless `blender --background --python` scripts already cover rendering.

## 5. Other tools in the stack (all free/local) and when to use them
- **Remotion** (motion-library): main compositor + all templates. Default.
- **HyperFrames** (HeyGen, open source Apache-2.0, HTML/CSS/GSAP → MP4, `npx hyperframes init/preview/render`,
  agent skills `npx skills add heygen-com/hyperframes`): use for quick HTML-style motion cards/slides when a
  template doesn't exist in Remotion yet, or to reuse HyperFrames catalog blocks. Render to webm/mp4 and drop
  into Remotion as a clip. Local render = free; do NOT use HyperFrames cloud rendering (paid).
- **three.js** via Remotion: 3D scenes in code (fast, real-time-ish).
- **Blender**: realistic 3D (sets, objects, cinematic shots).
- **ffmpeg**: cutting, concat (separate audio/video concat — lip-sync lesson from docs/28), loudnorm, encode.
- **Python tools** (`tools/`): transcribe (Whisper large-v3-turbo), matte (RVM), build_edit, fetch (yt-dlp).

## 6. Inputs Aly gave (2026-11-20) — `C:\_working pc\sample for ai`
- `Timeline 1 (Resolve)f.mp4` — 10:02, 1920x1080 30 fps, Aly talking (black t-shirt, desk + 2 monitors). It is
  an EDITED timeline (jump cuts) — OK for tests; for the final HeyGen digital twin record 2-5 min continuous,
  no cuts, no music, steady camera, natural gestures, mouth closed for 1-2 s at start/end.
- `Screenshot_306..311.png` — 1919x1079 stills, second look (light-blue hoodie, blue LED room, mic arm).
  Good for a HeyGen PHOTO avatar test.
- Prepared copies in `projects/2026-11-20 avatar avatarTest/input/`.

## 7. Lessons (fill after each avatar job)
- 2026-11-20 first test (done from Cowork chat, connectors HeyGen/ElevenLabs/Higgsfield added in claude.ai via Chrome):
  - ElevenLabs: Aly ALREADY has a cloned voice "Aly Shorosh - Hakayetna" (voice_id eXI6Aav1MNPeoXcPWDTH, ar-egyptian). Use it,
    don't re-clone. eleven_v4, 2 takes of the 8.7 s script = 210 credits (starter plan ~39k chars/month). ElevenLabs flow
    EH5LrZ9f98DT0ySZb76r. Its content URLs are signed (expire ~2 h) and public -> pass straight to HeyGen as audioUrl.
  - HeyGen plan: Creator, 600 premium credits/month. HeyGen MCP needs URL without trailing slash in claude.ai
    (`https://mcp.heygen.com/mcp/v1`, OAuth "Register automatically").
  - Digital twin needs Aly's own consent recording (not automatable). Avatar V learns from ~15 s; longer footage does
    NOT improve it (HeyGen webinar). Quick path with NO twin: create_video_from_image (his photo + our audio), 9:16.
  - Uploading a local file to HeyGen from the cloud session: sandbox/VM network blocks S3 -> create_asset_upload_batch,
    then in Chrome on app.heygen.com inject an <input type=file>, Claude-in-Chrome file_upload (<=3.8 MB), JS fetch PUT
    to upload_url with the returned headers, then complete_asset_batch. Photo asset 329a8ecf93c2498b8c16b90926cb94d2.
  - Test video id 7d34ac9f2ff656b6681515f1cc38b556 (Avatar 6 Turbo, 1080p, 9:16).
- 2026-11-20 Aly review of test 01: "شرش" mispronounced -> write it "شُرُوش" (Shorosh); voice sounded AI; mouth/face motion
  too extreme, not his way of talking. Fixes in test 02: NEW instant clone "Aly Shorosh v2 (Nov 2026)"
  (voice_id 7TksFpngO1KQ1UuIx4TJ, from 170 s of his clean audio, background-noise removal on) + eleven_multilingual_v2;
  his black-shirt desk look (frame from the Resolve video, asset ec500c1349004f02a6a1079342590046); HeyGen
  motionExpressiveness "less" + calm motion prompt. Video 3d47d40c8508a8a1acb13a2f045e30ee.
  Professional Voice Clone needs a higher ElevenLabs plan than Starter. "30min audio.mp3" is really 10:02.
- 2026-11-20 test 03 = REAL footage (8 s of the Resolve video, 9:16 crop) + HeyGen create_lipsync (precision, ~4 min render;
  source video MUST keep its audio track or it fails) + voice v2. Aly: "better" than photo avatars, but his body/eyes don't
  follow the new words — he looks away from the camera a lot in that footage. => Lipsync base footage must be a purpose-made
  "base take": eyes on camera, calm neutral face, small generic gestures, no strong emotion. Best motion-follows-speech =
  digital twin (Avatar V, 15 s) — needs his consent recording. Lipsync id f0a43c621cc249639bb3304893e1fb21.
- 2026-11-20 Aly: ElevenLabs instant-clone audio itself "very bad, obviously AI" (raw mp3, not a HeyGen issue). Test 04 =
  HeyGen instant voice clone "Aly Shorosh (HeyGen test)" voice_id 3f69c6e2949b46188d82774ecb0d512d (same 170 s sample,
  similarity max) + create_lipsync on the real clip with enableDynamicDuration=false (lipsync b6a552cbdf1345d2b0e60bc897346896).
  Options told to Aly: (1) record the script in his own voice (best, no camera), (2) ElevenLabs PVC (needs plan upgrade +
  30 min RAW mic audio), (3) HeyGen clone (this test).
- 2026-11-20 DIGITAL TWIN READY (Aly made it on HeyGen): look "Aly Moataz -- 1" avatar_id c7e371d6395d4e0aa59618d58f57e326
  (digital_twin, portrait 720x1280, group f13f38cec9b54909949260ef321fc947; photo look f13f38cec9b54909949260ef321fc947),
  default HeyGen voice "Aly Moataz" voice_id 68fd7b29cfa643748b68c0992c1dc70c (instant clone from the twin recording,
  engine heygen_voice / heygen-voice-1). Twin test 01: its own voice + script, removeBackground + generated pro studio bg
  (HeyGen create_image nano-banana-2, 9:16, 3 credits), video 573316a0011812bbe414af27f5b43685.
- 2026-11-20 twin test 01 review (Aly): name came out wrong again on the 2nd "علي" (read like "عليا") — writing alone
  (شُرُش/شُرُوش, diacritics) is NOT reliable. Fix: HeyGen Voice inline IPA: `<pron ipa="/ˈali ʃoˈroʃ/">علي شروش</pron>`
  and `<pron ipa="/ˈali/">علي</pron>` (ʕ and æ are rejected: "unsupported phones" → use plain a/i). Speech via
  create_speech_without_player, then pass audio_url to the video. Also end sentences with "." before "أنا مش علي".
  Background: keyed avatar over a generated image looked pasted — light didn't match ("محتاج تجانس"). Fix = generate a
  NEW LOOK of the twin inside the set (HeyGen create_avatar_looks / look remix) so the set and the lighting on him are one
  image; then render that look with the twin as motion reference. Never key-over a mismatched plate again; if compositing
  in Remotion, match light (color grade + rim light + shadow) on the avatar layer.
- 2026-11-20 studio look made by Aly in the HeyGen looks card: "Aly sitting/standing as the presenter" look_id
  a7e1bb9b7018931d094475ee25d87042 (photo look in the twin's group, 1536x2752). Twin test 02 = that look + IPA-name audio
  (HeyGen voice) + engine heygen-avatar-6-turbo with reference_look_id = twin c7e371d6395d4e0aa59618d58f57e326, 9:16.
  Video bcce41f321ed0c06097db91152ae6f8a.
- 2026-11-20 NAME FIX (Aly): correct = «عَلِي شُرُش» (Ali Shurush). HeyGen Voice (instant clone) turns ع into a hamza —
  Latin "Ali Shorosh", diacritics and IPA /ali ʃuˈruʃ/ all failed (ʕ not in its IPA set). Trying: ElevenLabs eleven_v3
  (voice v2, text «عَلِي شُرُش») for correct pronunciation → HeyGen convert_speech (speech-to-speech) into the twin's
  HeyGen voice 68fd7b29… (keeps words + timing, swaps timbre). Files: EL take sXmKoaupBT6urHoDytud, STS
  id=103c3465f5514213a0d21838298291b3.wav. Waiting for Aly's verdict.
- 2026-11-20 Aly: ElevenLabs v3 → HeyGen STS = ع correct ✓, but timbre "not very similar" to him in the rest. Next try:
  STS into the HeyGen clone made from the 170 s sample (3f69c6e2…, id=7ea911414b724614babe2e558f2013e9.wav).
  Real fix for similarity = a Professional clone from 30+ min RAW mic audio (ElevenLabs Creator plan; HeyGen professional
  voices can't be STS targets but can do TTS).
- 2026-11-20 ElevenLabs-only chain (Aly asked): natural Egyptian library voice "Ahmed Yahia" (rMheqEfwsIJckq2yCdb5,
  eleven_v3, «عَلِي شُرُش») → ElevenLabs Voice Changer (eleven_multilingual_sts_v2) into Aly v2 voice. In a flow the
  voice-changer node needs voice set via creative_update_node (voice_id param on generate_in_flow alone failed).
  STS ≈ 137 credits per 8 s. Result erSwVSp8xCcMZ1Jus3yO. Idea: STS keeps the SOURCE's natural prosody, only the timbre changes.
- 2026-11-20 Aly verdict on voices: library-voice → Voice Changer = NO. HeyGen voice/STS = no. Best = "Aly twin test 02"
  visuals (studio look a7e1bb9b… + twin motion) and the earlier ElevenLabs takes of his own clone ("نسخ eleven labs
  القديمة احسن"). => DEFAULT VOICE: ElevenLabs TTS with "Aly Shorosh v2" (7TksFpngO1KQ1UuIx4TJ), eleven_v3, name written
  «عَلِي شُرُش» (ع correct) → pass audio_url to HeyGen create_video_from_avatar (studio look + reference_look_id twin).
  Twin test 03 = exactly that: video ecd49e3777eb40ed49515504ae6f2f02.
- 2026-11-20 Aly: "في الأول كنت بتطلع صوت قريب مني في الموقعين، دلوقتي بعيد — ارجع زي ما كنت". The early setups he means:
  ElevenLabs = OLD clone "Aly Shorosh - Hakayetna" (eXI6Aav1MNPeoXcPWDTH) + eleven_v4 + plain text with "... [pause]";
  HeyGen = the twin's own voice via plain script TTS (as in twin test 01). Later changes (full diacritics, IPA tags, v3,
  STS, library voice + voice changer) pushed the voice AWAY from him → don't use them. Only touch the name: «علي شُرُش».
  Back-to-basics takes: EL Hakayetna v4 (flow node rPrk0UPSsrehL32j2BEt), HeyGen plain TTS id=8fa74622….
- 2026-11-20 Aly CHOSE: HeyGen twin voice (68fd7b29…) with PLAIN script TTS (no IPA, no full diacritics) = "ده أحسن".
  Only issue: «مش علي» at a sentence end is read «مش عليا» → never end a phrase on «علي»; add a word after it
  («مش علي الحقيقي»). Name in text: «علي شُرُش». Take id=bf8dec2090184fd5ac774f6aaf97b980.
- 2026-11-20 even «مش علي الحقيقي» still came out «عليا» → Aly's fix: rephrase to «أنا مش هو الحقيقي». Rule: avoid «علي»
  right after «مش»/at phrase end in HeyGen voice; rephrase around it.
- 2026-11-20 RUN_v9 (YouTube 16:9 «عالم الـ AI كله», autonomous, no paid generation): balances via claude.ai connectors (HeyGen
  get_current_user 574, ElevenLabs account_get_usage 33,240 chars, Higgsfield balance 3000.35 ultra; Suno needs `/mcp`).
  Higgsfield estimates: Seedance 2.5 5 s 1080p = 80 / 720p = 35, Seedance 2.5 Flash 720p = 25, Cinema Studio 4.0 1080p = 80,
  Kling 4.0 5 s 1080p = 16.25 (10 s = 32.5), Kling 3.0 Omni Edit 5 s = 10, nano_banana_2 image = 1.5, gpt_image_2_6 = 0.25.
  HeyGen pricing page gives NO credits-per-minute → always a 10 s test first and read the balance diff.
  HeyGen calls the twin model "Avatar 6" (not "Avatar V"). New free pieces: Remotion `ai-world-rough` / `ai-world-hud`
  (src/aiworld, alpha needs --image-format=png), Blender `tools/blender/aiworld_blockouts.py` (Blender 5.x: media_type VIDEO),
  `tools/fetch_logos.py` (Tip 13), draft styles 21-25. Project files: cost_plan_v1.md, sources_v5.md, work/, output/.
- 2026-11-20 HeyGen REAL PRICES (10 s test, Aly picked bundle "المقترح"): twin voice TTS 12 s = 1 credit (≈ 5/min),
  Avatar 6 Turbo 1080p 12 s = 4 credits (≈ 20/min, ≈ 0.33/s). Real speech rate of the twin voice = 2.6 words/s (not 2.2).
  create_speech_without_player withTimestamps gives word timings (can replace Whisper for timing). The studio look
  a7e1bb9b… is PORTRAIT → 16:9 YouTube needs a landscape look in the set (create_avatar_looks), never a 16:9 cover crop.
- 2026-11-20 full narration (23 create_speech_without_player calls, one per chapter, 17:40 total) = 23 credits → HeyGen
  voice ≈ 1 credit PER REQUEST (a 3:52 chapter = 1 credit), not per minute. Long texts read slower (2.29 w/s avg).
  QA without listening: tools/transcribe.py + word diff vs script (project work/scripts/check_voice.py); Whisper's VAD
  drops some sentences → re-check suspect spots with vad_filter=False before calling them missing.
- RULE (Aly 2026-11-20): every audio SEPARATE so the AI voice can be swapped or he records himself: project
  `output/audio_stems_vN/` = voice_full_timeline.wav (video length) + voice_chapters/NN_Cxx.wav + sfx/ + music/ (each
  also one full-length wav) + سكريبت_التسجيل.txt (text per chapter + start time). Timing is built FROM the voice files
  (build_timeline_v2.py), so his own recording per chapter = re-run timing, nothing else changes.
- 2026-11-20 keyframes: 30 × Higgsfield nano_banana_2 16:9 1k = 45 credits (refs: studio look photo for Aly, Blender
  last frames for jet/lab/bridge → same face + same camera as the blockout). A false "nsfw" flag is NOT charged; reword
  once. Uploads to Higgsfield: PUT needs header `If-None-Match: *` (it is in SignedHeaders). HeyGen NEW LOOK (e.g.
  landscape 16:9): create_avatar_looks only opens a card — the owner clicks Generate (prompt look = 1 credit).
- 2026-11-20 Aly on his generated face: "مش بهي كفاية وانا من غير دقن"، "مش اصلع عندي شعر خفيف"، then "اعملني بالظبط زي
  شكلي بالتيشيرت الاسود في الاوضة وورايا الـ pc". RULE: never describe his face in words (beard/bald guesses were wrong);
  the ONLY face reference = a real frame of his black-t-shirt room video (`C:\_working pc\sample for ai\Timeline 1 (Resolve)f.mp4`)
  + prompt "the EXACT man from the reference photo… do not change or beautify". Presenter = HeyGen photo look made from
  that real 1920x1080 frame INSIDE the twin group (create_photo_avatar with avatarGroupId, 1 credit) → native 16:9, then
  Avatar 6 Turbo + reference_look_id twin + motionExpressiveness "less" (12 s = 4 credits). Look fbbb101ecad2a8e987ac830c6ffb7fe5.
- 2026-11-20 RUN_v9 clips (bundle المقترح): REAL Higgsfield prices: Kling 4.0 image-to-video 1080p = 3.75/s (5 s 18.75, 6 s 22.5 —
  the 16.25 in cost_plan_v1 was text-to-video), Seedance 2.5 omni_reference start_image 720p 5 s no audio = 35, Kling 3.0
  Omni Edit pro (video_references = blockout mp4 + image_references = keyframe) ≈ 12 per 5-6 s. 37 clips = 861.5 credits,
  all done in ~5 min in 3 parallel batches. Keyframe job ids work directly as start_image values. Kling outputs 1924x1076
  (scale to 1080p). Blockout→look worked for the bridge, too abstract for the jet (blockout shapes dominate) → give the edit
  a detailed blockout or use image-to-video from a keyframe instead. Prompt rule: "keep the man's face" ONLY on shots with
  Aly; other shots "keep the scene… do not add people".
- 2026-11-20 AVATAR BATCH TRICK: cut the voice of every avatar shot from the timeline wav, join them with 0.4 s silence,
  ONE create_video_from_avatar call (audioAssetId; upload via create_asset_upload_batch + PUT + complete_asset_batch),
  then cut the result back per shot (project work/scripts/cut_avatar.py). 34 shots / 208 s = 70 credits (~0.34/s), ~10 min.
- 2026-11-20 Suno via connector: custom lyrics + style, 1 call = 2 songs = 10 credits (v6, 180 s). Downloading a song costs a
  suno.com DOWNLOAD credit (audio-download → requires_credit; cdn1 mp3 links are 403) → download only the version Aly picks.
