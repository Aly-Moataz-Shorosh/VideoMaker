#!/bin/sh
# Final video in ONE ffmpeg pass (NVENC, ~20 min): teaser -> intro sting -> opening pages -> course (untouched audio) -> ending -> outro.
# Outro = his alpha render (_branding/outro.avi) over the frozen last page of the ending (QR codes stay visible under it).
#   sh assemble.sh            (needs work/render/{teaser,pages,end}.mp4 from render.sh)
W="$(cd "$(dirname "$0")/.." && pwd)"; P="$W/.."
R="$W/render"; OUT="$P/output"; mkdir -p "$OUT"
SRC="$P/input/2026-11-06 14-39-41.mp4"
INTRO="$W/../../../brand/clips/genjutsu_intro_sting.mp4"
OUTRO="E:/root/output/Youtube/Aly Shorosh New/_branding/outro.avi"
ED=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$R/end.mp4")
FT=$(python -c "print(round($ED-0.6,3))")
ffmpeg -v error -y -ss "$FT" -i "$R/end.mp4" -frames:v 1 "$R/end_last.png" || exit 1
V='fps=60,scale=1920:1080,setsar=1,format=yuv420p'
A='aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo'
st=$(date +%s)
ffmpeg -v error -stats -y -i "$R/teaser.mp4" -i "$INTRO" -i "$R/pages.mp4" -i "$SRC" -i "$R/end.mp4" -loop 1 -framerate 30 -i "$R/end_last.png" -i "$OUTRO" \
  -filter_complex "[0:v]$V[v0];[0:a]$A[a0];[1:v]$V[v1];[1:a]$A[a1];[2:v]$V[v2];[2:a]$A[a2];[3:v]$V[v3];[3:a]$A[a3];[4:v]$V[v4];[4:a]$A[a4];\
[5:v]format=yuv420p[bg];[6:v]format=yuva420p[ov];[bg][ov]overlay=shortest=1,$V[v5];[6:a]$A[a5];\
[v0][a0][v1][a1][v2][a2][v3][a3][v4][a4][v5][a5]concat=n=6:v=1:a=1[v][a]" \
  -map '[v]' -map '[a]' -c:v h264_nvenc -preset p5 -rc vbr -cq 24 -b:v 0 -maxrate 8M -bufsize 16M -profile:v high \
  -c:a aac -b:a 256k -movflags +faststart "$OUT/film_making_course_full.mp4" || exit 1
echo "done $(( $(date +%s) - st ))s"
