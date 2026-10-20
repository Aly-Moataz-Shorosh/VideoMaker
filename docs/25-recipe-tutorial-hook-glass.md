# Recipe: tutorial short with a before/after HOOK, glass look (adobeaudition, 2026-10-15). APPROVED v4 ("تمام") = style 11

Job: `projects/2026-10-15 shorts adobeaudition`: his 9:12 video "طريقة سهلة وسريعة لتحسين صوت الفيديو" (YouTube IjVlRDHEBSY).
It opens as a talking head (0:00–1:30), then a screen recording of Adobe Audition with his webcam in the bottom-right corner
(x 1232–1920, y 692–1080). Notes: style 10, CTA yes, face yes. Asked first: ONE full short.

## Review history (what each version taught)
- v1 (2:02, glass style 10 as is): rejected because "ده شورت مش فيديو طبيعي فا محتاج يبدأ ب hook". It kept the long video's intro (sound = 50%, laptop mic).
- v2: hook first, steps right away, more motion, less face, voice enhanced. Rejected the hook: I had picked two takes myself.
- v3: hook = a before/after he played mid-video (1:53 / 1:59). Still wrong: "الفيديو في اوله هتلاقي مثال ال before و ال after".
- v4: hook = HIS OPENING demo (burned-in labels: red "Before" 0:00–10.8, green "After" from 10.8). APPROVED.
  How I found the switch: per-frame share of red vs green pixels in the label corner.

## Structure (make_short_v4.py)
1. `au_hook2` (≈6 s): before piece (0.05–3.5) then after piece (11.1–14.0). Cam `wide` shows his real clip with the labels in
   the middle. Title "من ده 👎" → "لـ ده 👍", voice bars (`Sound`, real RMS per frame, red with a noise band → gold/clean), then
   "بـ 5 خطوات بس". The demo audio is only levelled (gain), never enhanced (`RAWVOICE`).
2. `au_tool` (3 s): Audition logo (vector `AuLogo`), his sentence naming the program, cam `mini`.
3. One `au_step` per effect: chip "0N Name · Arabic", `Screen` = cam_v4.mp4 (full frame), cropped through `keys`. `zoom_on()` adds
   one zoom key 0.35 s before every click box, so the card follows his mouse. On every click: gold box + cursor ripple + English
   label. Below: current step (number + text, on his words), then progress dots (`Chain`). Cam `cmini` = round webcam bottom-right.
4. `au_end`: list of the 5 effects + QR card of the full video. CTA clip after, `CommentCta` with `qr` (the stack fades out, the QR card
   takes the top, never over his face). Check that the QR decodes from the RENDERED mp4 (cv2.QRCodeDetector).

## Clicks
Menus/dialogs found from a 2-s contact sheet of the screen part + full-res crops at each spoken click (Effects menu at x 175 y 9;
submenus open to the right). Write the click boxes in 1920x1080 source px in `SCREEN` = (src second, duration, x, y, w, h, label).
A time inside a cut gap snaps to the nearest kept edge (`rel()`).

## Voice
On his request only: speech pieces come from `work/voice_enh.wav` = ffmpeg `highpass 80, afftdn nf -28 nr 14, EQ -2 dB@250,
+3 dB@3.2k, +2 dB shelf 9k, compressor 3:1`. Then the usual per-sentence gain (`level_voice.py`) + -15 LUFS.

Outputs: `output/v4/short_1.mp4` (1:31) + .txt, `v4/sfx_only`, `v4/voice_original` (= the enhanced voice track). v1–v3 kept.
