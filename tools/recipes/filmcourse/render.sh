#!/bin/sh
# Render only the added pieces (composition `course`, 30 fps, WITH audio: they are short): sh render.sh teaser pages end
W="$(cd "$(dirname "$0")/.." && pwd)"; ML="$W/../../../motion-library"
R="$(cygpath -m "$W/render")"; mkdir -p "$W/render"
cd "$ML" || exit 1
T="$(pwd)/out/tmp_render"; mkdir -p "$T"; export TEMP="$(cygpath -w "$T")" TMP="$(cygpath -w "$T")"
npx remotion bundle --out-dir out/bundle > /dev/null 2>&1 || { echo BUNDLE FAILED; exit 1; }
for N in "$@"; do
  st=$(date +%s)
  npx remotion render out/bundle course "$R/$N.mp4" --props="$(cygpath -m "$W/props_$N.json")" --crf=16 --concurrency=6 --timeout=240000 > "$W/render_$N.log" 2>&1 \
    || { echo "$N FAILED"; tail -5 "$W/render_$N.log"; rm -rf "$T"; exit 1; }
  echo "$N $(( $(date +%s) - st ))s"
done
rm -rf "$T"
