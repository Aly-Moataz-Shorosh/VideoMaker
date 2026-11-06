#!/bin/bash
# Render audio-course shorts (course-short composition) -> output/shorts/_raw, then level + compress -> output/shorts.
#   bash render_shorts.sh "1 01_phone" "2 02_explosion" ...
# One bundle (out/bundle_f, rebuild it after changing src/: npx remotion bundle --out-dir out/bundle_f), TEMP on E: and cleaned.
cd "$(dirname "$0")/../../../../motion-library"
B=${BUNDLE:-/d/Temp/fs_bundle}  # bundle + temp on D: (E: almost full, 2026-11-07)
[ -f $B/index.html ] || npx remotion bundle --out-dir $B > /dev/null 2>&1
P="$(cygpath -m "$(cd '../projects/2026-11-06 youtube intro to film making course' && pwd)")"
mkdir -p "$P/output/shorts/_raw"
names=()
for x in "$@"; do
  set -- $x; n=$(printf %02d $1); nm=$2
  T="/d/Temp/fs_tmp_render"; mkdir -p "$T"; export TEMP="$(cygpath -w "$T")" TMP="$(cygpath -w "$T")"; st=$(date +%s)
  npx remotion render $B course-short "$P/output/shorts/_raw/$nm.mp4" --props="$P/work/shorts/props_${PROPS:-$n}.json" --concurrency=6 --timeout=240000 > "out/render_short_$n.log" 2>&1 \
    && echo "$nm OK $(( $(date +%s) - st ))s" || echo "$nm FAILED (out/render_short_$n.log)"
  rm -rf "$T"; names+=("$nm")
done
cd "$P/work/scripts"; PYTHONIOENCODING=utf-8 python level_fshorts.py "${names[@]}"
