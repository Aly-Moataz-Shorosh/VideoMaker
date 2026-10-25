#!/bin/bash
# Render the Blender version of the audio-course 3D scenes as transparent webm clips for the shorts (Aly 2026-10-26).
#   bash render_sound_clips.sh  "name scene seconds [--bar]" ...
#   -> motion-library/public/projects/audio/b3d/<name>.webm  (VP9 + alpha; frames kept in work/blender/<name>/ until checked)
B="${BLENDER_EXE:-E:/root/_assets/programs/Blender Foundation/Blender 5.2/blender.exe}"
H="$(cd "$(dirname "$0")/../.." && pwd)"
W="$(cygpath -m "$H/projects/2026-10-20 youtube audioproduction/work/blender")"; mkdir -p "$W"
OUT="$H/motion-library/public/projects/audio/b3d"; mkdir -p "$OUT"
for x in "$@"; do
  set -- $x; nm=$1; scn=$2; sec=$3; extra=$4
  n=$(python -c "import math;print(math.ceil($sec*30)+6)")
  st=$(date +%s)
  "$B" -b --factory-startup --python-exit-code 1 -P "$(cygpath -m "$H/tools/blender/sound_scenes.py")" -- --scene $scn --frames $n --out "$W/$nm" $extra > "$W/$nm.log" 2>&1 \
    || { echo "$nm FAILED"; tail -5 "$W/$nm.log"; continue; }
  ffmpeg -v error -y -framerate 30 -i "$W/$nm/%04d.png" -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 28 -row-mt 1 "$OUT/$nm.webm" \
    && echo "$nm OK $n frames $(( $(date +%s) - st ))s"
done
