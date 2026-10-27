#!/bin/sh
# Aly's tiny Meet self-view (0:17-2:04, source px 1688,808 160x102 — the self-view is 1658-1887 wide) cut out and scaled 3.2x with lanczos + a light unsharp
# -> public/projects/entabiz01/aly_open.mp4 (480x306, centred on his face x 1768, Meet name label cut off, 30 fps, starts at 17.12 = the biz_open cue start). Aly: "كبرها بقدر كافي".
cd "$(dirname "$0")/../../../../.."
P="projects/انت بتشتغل ايه/2026-10-27 ep01 biz karim tamer"
ffmpeg -v error -y -ss 17.12 -t 108 -i "$P/input/2026-10-27 16-06-01.mp4" -an \
  -vf "crop=160:102:1688:808,scale=480:306:flags=lanczos,unsharp=5:5:0.6:5:5:0.0,fps=30" -c:v libx264 -crf 16 -preset slow -g 30 \
  motion-library/public/projects/entabiz01/aly_open.mp4 && echo ok
