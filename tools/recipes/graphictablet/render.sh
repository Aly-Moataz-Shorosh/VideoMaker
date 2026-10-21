#!/bin/sh
# Render the graphic tablet shorts from ONE bundle (out/bundle); Remotion temp in a folder deleted after every short.
# sh render.sh 6 3 5 2 7  -> output/_raw/short_N.mp4 -> finalize.py -> output/short_N.mp4 (-16 LUFS, CRF 23)
W="$(cd "$(dirname "$0")/.." && pwd)"
ML="$W/../../../motion-library"
P="public/projects/2026-10-21 shorts graphictablet"
cd "$ML" || exit 1
[ -f out/bundle/index.html ] || npx remotion bundle --out-dir out/bundle > /dev/null 2>&1
T="$ML/out/tmp_render"
mkdir -p "$W/../output/_raw"
for n in "$@"; do
  mkdir -p "$T"; export TEMP="$(cygpath -w "$T")" TMP="$(cygpath -w "$T")"
  start=$(date +%s)
  npx remotion render out/bundle film-short "$W/../output/_raw/short_$n.mp4" --props="$P/short_$n.json" --crf=18 --concurrency=6 --timeout=240000 \
    > "$W/render_$n.log" 2>&1 && echo "short $n OK $(( $(date +%s) - start ))s" || { echo "short $n FAILED"; tail -5 "$W/render_$n.log"; }
  rm -rf "$T"
done
