#!/bin/bash
# Render course shorts (course-short composition) then level them.
#   bash render_shorts.sh "6 06_adjustment_layer" "7 07_tint" ...
cd "$(dirname "$0")/../../../../motion-library"
rm -rf out/bundle; npx remotion bundle --out-dir out/bundle > /dev/null 2>&1
P="$(cygpath -m "$(cd '../projects/2026-10-16 youtube premiere pro course' && pwd)")"
names=()
for x in "$@"; do
  set -- $x; n=$(printf %02d $1); nm=$2
  T="$PWD/out/tmp_render"; mkdir -p "$T"; export TEMP="$T" TMP="$T"; st=$(date +%s)
  npx remotion render out/bundle course-short "$P/output/shorts/_raw/$nm.mp4" --props="$P/work/shorts/props_$n.json" --concurrency=4 > "out/render_$n.log" 2>&1 \
    && echo "$nm OK $(( $(date +%s) - st ))s" || echo "$nm FAILED (out/render_$n.log)"
  rm -rf "$T"; names+=("$nm")
done
cd "$P/work/scripts"; PYTHONIOENCODING=utf-8 python level_shorts.py "${names[@]}"
