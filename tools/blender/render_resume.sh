#!/bin/bash
# Blender 5.2 EEVEE on the GTX 1050 Ti crashes now and then (EXCEPTION_ACCESS_VIOLATION in eevee render_read_result, with motion
# blur) -> render each scene in a loop that resumes from the first missing frame until all N frames exist, then encode the webm.
#   bash render_resume.sh "name scene frames" ...   (same names as render_biz_clips.sh)
B="${BLENDER_EXE:-E:/root/_assets/programs/Blender Foundation/Blender 5.2/blender.exe}"
H="$(cd "$(dirname "$0")/../.." && pwd)"
W="$(cygpath -m "$H/projects/انت بتشتغل ايه/2026-10-27 ep01 biz karim tamer/work/blender")"
OUT="$H/motion-library/public/projects/entabiz01/b3d"; mkdir -p "$OUT"
for x in "$@"; do
  set -- $x; nm=$1; scn=$2; n=$3; tries=0
  while :; do
    s=0; while [ -f "$W/$nm/$(printf %04d $s).png" ]; do s=$((s + 1)); done
    [ $s -ge $n ] && break
    tries=$((tries + 1)); [ $tries -gt 25 ] && { echo "$nm gave up at $s"; break; }
    echo "$nm from $s (try $tries)"
    "$B" -b --factory-startup --python-exit-code 1 -P "$(cygpath -m "$H/tools/blender/biz_scenes.py")" -- --scene $scn --frames $n --start $s --tex "$W/tex" --out "$W/$nm" > "$W/$nm.resume.log" 2>&1
  done
  ffmpeg -v error -y -framerate 30 -i "$W/$nm/%04d.png" -frames:v $n -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 26 -row-mt 1 "$OUT/$nm.webm" && echo "$nm OK"
done
