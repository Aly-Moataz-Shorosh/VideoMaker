#!/bin/bash
# Render the رواد الأعمال ep01 opening scenes (biz_scenes.py) as transparent webm clips (1920x1080, 30 fps).
#   bash render_biz_clips.sh "name scene frames" ...  -> motion-library/public/projects/entabiz01/b3d/<name>.webm
# PNG frames stay in the episode's work/blender/<name>/ until checked (CLEAN=1 removes them).
B="${BLENDER_EXE:-E:/root/_assets/programs/Blender Foundation/Blender 5.2/blender.exe}"
H="$(cd "$(dirname "$0")/../.." && pwd)"
W="$(cygpath -m "$H/projects/انت بتشتغل ايه/2026-10-27 ep01 biz karim tamer/work/blender")"; mkdir -p "$W"
OUT="$H/motion-library/public/projects/entabiz01/b3d"; mkdir -p "$OUT"
for x in "$@"; do
  set -- $x; nm=$1; scn=$2; n=$3
  st=$(date +%s)
  "$B" -b --factory-startup --python-exit-code 1 -P "$(cygpath -m "$H/tools/blender/biz_scenes.py")" -- --scene $scn --frames $n --tex "$W/tex" --out "$W/$nm" > "$W/$nm.log" 2>&1 \
    || { echo "$nm FAILED"; tail -5 "$W/$nm.log"; continue; }
  ffmpeg -v error -y -framerate 30 -i "$W/$nm/%04d.png" -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 26 -row-mt 1 "$OUT/$nm.webm" \
    && echo "$nm OK $n frames $(( $(date +%s) - st ))s" && { [ -n "$CLEAN" ] && rm -rf "$W/$nm"; true; }
done
