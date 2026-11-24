# 37 — Aly's AI presenter + studio kit (reuse in ANY topic, ANY style)

Aly 2026-11-24: «احفظ … الافاتر و الستوديو لان بعد كدا ممكن اعمل فيديوهات عن توبكس كتير في نفس الستوديو ده حتى لو هختار ستايل تاني».
So this kit is NOT tied to style 27: any video where he is not on camera can use this presenter + studio with any look/style from styles/.
Files + IDs: `brand/avatar-studio/` (kit.json = every ID, اقرأني.txt = Aly's guide). Paid services rules: docs/33 (cost first, shortest test first).

## What is in the kit
| item | value | file |
| --- | --- | --- |
| HeyGen avatar group | f13f38cec9b54909949260ef321fc947 | — |
| Digital twin (motion reference) | c7e371d6395d4e0aa59618d58f57e326 | aly_twin_frame.jpg |
| Voice (HeyGen Voice, instant clone) | 68fd7b29cfa643748b68c0992c1dc70c | — |
| MAIN studio look «S4g» (Nefertari stars + Cairo mashrabiya, 16:9) | f1f77fad0dfae53462efdbd5de0c7634 | studio_S4g_with_aly.jpg, studio_S4g_empty_plate.png |
| Podcast studio look | bf8ea0fe5fa6b762b487f3e65805dd5f | look_podcast_studio.png |
| Standing presenter wide | 480af08953824ecbe27928647bbda8d4 | look_presenter_wide.png |
| Room, black t-shirt (real frame) | fbbb101ecad2a8e987ac830c6ffb7fe5 | — |
| Beach / jungle / galabeya Burj Khalifa | 730a4cb19467472533e464026d7cfcf0 / b6d60d4b61188382ad8efa20777f75fd / 7073dc887af2774dea1a06a6d76823fc | — |
| Portrait presenter (reels 9:16 only) | a7e1bb9b7018931d094475ee25d87042 | — |
| Higgsfield studio reference media | 58fced38-1a9d-4f39-8487-9d16c7c2aa34 | — |
| Higgsfield face reference media | 3e25541a-3062-4592-9ff8-31170430270b | aly_face_cutout.png |

## How to make the presenter talk (proven in v10 / v11)
1. Write the lines in HIS Egyptian Arabic (tool names in English), show them to him, say the credit cost (≈ 0.35 HeyGen credits / second of video).
2. ONE TTS request for all lines: `create_speech_without_player(voiceId=68fd…, language="ar", withTimestamps=true)`, lines separated by blank
   lines; split by the CHARACTER timestamps into one wav per line; Whisper-check every line (short lines: pad 1 s of silence + initial_prompt).
3. Join the lines with 0.4 s gaps into ONE wav + a parts map (sids, avatar_in, dur) -> upload as a HeyGen asset ->
   `create_video_from_avatar(avatarId=<look>, audioAssetId=…, engine={type: heygen-avatar-6-turbo, reference_look_id: c7e371d6…, motion_expressiveness: less},
   motionExpressiveness=less, aspectRatio=16:9, resolution=1080p)`. Log every id in the project's jobs file.
4. In the edit, place each part by its SENTENCE ID in the current timeline and add the line's trimmed leading silence (timeline file piece `a`)
   to the skip — else the circle runs 0.1–0.3 s early. Check: each circle's batch audio vs the voice track = 0 ms (corr ≥ 0.9).
5. Full-frame twin for openings / key lines; the talking CIRCLE (x250 y270 r110, face centred with MediaPipe) during long explanations;
   his face in ONE place at a time.

## New place for him (new look) — when a topic needs it
- Never let an image model redraw his face for a talking look (rejected): make the place as a NEW LOOK inside his twin's group
  (HeyGen look from the empty plate / a Higgsfield place image with his face reference), then lip-sync through the twin as above.
- Keep the main S4g studio as the channel's «home»; other looks only when the topic needs the place.

## Thumbnails with him
- Higgsfield `gpt_image_2_6` (16:9, 2k, high; 4 credits / 2 images) with his face reference (3e25541a…) + a layout reference,
  prompt «KEEP THE MAN EXACTLY AS IN REFERENCE … do not redraw», Arabic text quoted exactly, no AI-drawn app logos (they come out wrong).
- Approved direction (2026-11-24): puppet on golden strings from a robot «AI» hand, blue smoke background, moderately surprised face
  (not exaggerated), big yellow hook + white guide line + red badge (`thumbnail_example_puppet.jpg`).
- Always compare face crops with the reference and zoom on the Arabic spelling before sending.
