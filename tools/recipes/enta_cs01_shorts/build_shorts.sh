#!/bin/bash
# Whole meet-short, end to end:  bash build_shorts.sh 1 2 3
#   make_short (edges, tiles strip + review strip, cadres, captions) -> ONE bundle -> Remotion render meet-short -> level.py
S="$(cd "$(dirname "$0")" && pwd)"
ML="$S/../../../../../motion-library"
P="$(cygpath -m "$(cd "$S/../.." && pwd)")"
mkdir -p "$P/output/shorts/_raw"
cd "$ML"; [ -f out/bundle/index.html ] || npx remotion bundle --out-dir out/bundle > /dev/null 2>&1
for x in "$@"; do
  n=$(printf %02d $x); st=$(date +%s)
  cd "$S"
  PYTHONIOENCODING=utf8 python make_short.py $x > "$S/../shorts/build_$n.log" 2>&1 || { echo "short $n make_short FAILED"; continue; }
  cd "$ML"
  rm -rf out/bundle/public/projects/entacs01s; mkdir -p out/bundle/public/projects; cp -r public/projects/entacs01s out/bundle/public/projects/   # fresh media without re-bundling
  T="$PWD/out/tmp_render"; mkdir -p "$T"; export TEMP="$(cygpath -w "$T")" TMP="$(cygpath -w "$T")"
  npx remotion render out/bundle meet-short "$P/output/shorts/_raw/$n.mp4" --props="$P/work/shorts/props_$n.json" --concurrency=10 --crf=16 >> "$S/../shorts/build_$n.log" 2>&1 \
    || { echo "short $n render FAILED"; rm -rf "$T"; continue; }
  rm -rf "$T"
  cd "$S"; PYTHONIOENCODING=utf8 python level.py $x
  echo "short $n done in $(( $(date +%s) - st ))s"
done
