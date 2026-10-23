#!/bin/sh
# Render Journey shorts from ONE bundle (out/bundle); Remotion temp in a folder deleted after every short.
# sh work/scripts/render.sh 8 33 44 -> output/_raw/short_N.mp4 -> finalize.py -> output/NN_slug.mp4 (-16 LUFS, CRF 23)
W="$(cd "$(dirname "$0")/.." && pwd)"
ML="$W/../../../motion-library"
P="public/projects/2026-10-22 shorts Journey to the center of computer graphics"
cd "$ML" || exit 1
# the bundle holds a COPY of public/: rebuild it when any short's json/voice/cam changed after it (2026-10-23: short 1 rendered with a
# stale voice_1.wav from the bundle -> voice 2.5 s off and silent at the end while the captions went on)
if [ -f out/bundle/index.html ] && [ -n "$(find "$P" -newer out/bundle/index.html -type f | head -1)" ]; then rm -rf out/bundle; fi
[ -f out/bundle/index.html ] || npx remotion bundle --out-dir out/bundle > /dev/null 2>&1
T="$ML/out/tmp_render"
mkdir -p "$W/../output/_raw"
for n in "$@"; do
  mkdir -p "$T"; export TEMP="$(cygpath -w "$T")" TMP="$(cygpath -w "$T")"
  start=$(date +%s)
  npx remotion render out/bundle film-short "$W/../output/_raw/short_$n.mp4" --props="$P/short_$n.json" --crf=18 --concurrency=4 --timeout=240000 \
    > "$W/render_$n.log" 2>&1 && echo "short $n OK $(( $(date +%s) - start ))s" || { echo "short $n FAILED"; tail -5 "$W/render_$n.log"; }
  rm -rf "$T"
done
