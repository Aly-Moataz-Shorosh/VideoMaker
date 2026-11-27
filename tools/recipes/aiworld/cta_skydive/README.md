# Skydive CTA (aiFullVideoCost, approved v4 2026-11-27)

Outro CTA for the reels: Aly (Soul ID face) skydiving over Giza, holding the video thumbnail, banner with his logo +
YouTube icon, QR of the long video top-right, handles footer + Follow, his voice lip-synced, wind under it.

Pipeline that won (after 7 Seedance drafts + Cinema Studio test; Aly picked Grok):
1. Soul ID (soul_2) from 11 REAL frames of his videos (25 cr) -> keyframe soul_2 + nano_banana_2_1 edit (thumbnail held, banner).
2. `real_ground.py` keyframe.png aerial.jpg out.png --horizon 0.36 --top 0.40 --scale 1.75: REAL aerial Commons photo
   under him (image models keep fake pyramids; do NOT per-channel colour match -> blue city became water).
3. `grok_video_v15` 720p 9 s from that keyframe: whole-body freefall motion, hands on the paper to the last frame,
   stays high (40.5 cr). Seedance 2.5 = head-only motion + rigid paper (rejected 6x).
4. `sync_so` on the voice, speaker point on the REAL face (printed face is a 2nd face) (32.55 cr).
   ⚠ sync_so's output audio is the voice delayed +0.13 s -> always mux ITS OWN audio track, never the voice file at 0.
5. Upscale 1080x1920 (lanczos + crop), then `paper_thumb.py ... --no-paper` (QR card, footer_follow.png, wind_clean.wav).
6. Cut right after the last word (mouth kept moving after the voice).

Aly: do NOT paste the thumbnail over the clip a second time («متحطش الصورة مرتين») -> freeze_print.py / freeze_sift.py
/ fit_thumb.py exist (static print via optical flow / per-frame SIFT) but were NOT used in the approved version.
`ground_video.py` (per-frame real ground) also not used. Credit line for the aerial photo is required (CC BY-SA 4.0).
