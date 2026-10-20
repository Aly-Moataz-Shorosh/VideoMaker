#!/bin/bash
# Render stage shorts then level them:  bash render.sh 1 2 3   (props in work/shorts/props_NN.json)
cd "$(dirname "$0")/../../../../motion-library"
rm -rf out/bundle; npx remotion bundle --out-dir out/bundle > /dev/null 2>&1
P="$(cygpath -m "$(cd '../projects/2026-10-18 shorts newstage19shorts' && pwd)")"
mkdir -p "$P/output/_raw"
for x in "$@"; do
  n=$(printf %02d $x)
  T="$PWD/out/tmp_render"; mkdir -p "$T"; export TEMP="$T" TMP="$T"; st=$(date +%s)
  npx remotion render out/bundle stage-short "$P/output/_raw/short_$n.mp4" --props="$P/work/shorts/props_$n.json" --concurrency=4 > "out/render_ns_$n.log" 2>&1 \
    && echo "short $n OK $(( $(date +%s) - st ))s" || echo "short $n FAILED (out/render_ns_$n.log)"
  rm -rf "$T"
done
cd "$P/work/scripts"; PYTHONIOENCODING=utf-8 python level.py "$@"
