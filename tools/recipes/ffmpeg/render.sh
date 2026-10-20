#!/bin/sh
# Render shorts to projects/<code>/output/short_<n>.mp4 from ONE bundle (out/bundle), temp on C: in a folder that is
# deleted after every short (Remotion temp filled the disks before). Usage: sh render.sh 1 2 3 ...
# V=v3 sh render.sh 1 ...  -> props short_<n>_v3.json, output output/v3/short_<n>.mp4 (AI voice version)
W="$(cd "$(dirname "$0")/.." && pwd)"
ML="$W/../../../motion-library"
P="public/projects/2026-10-14 shorts ffmpeg"
cd "$ML" || exit 1
[ -f out/bundle/index.html ] || npx remotion bundle --out-dir out/bundle > /dev/null 2>&1
T="/c/Users/alymo/AppData/Local/Temp/vhs_render"
SUF=${V:+_$V}; OUT="$W/../output${V:+/$V}"
mkdir -p "$OUT"
for n in "$@"; do
  mkdir -p "$T"; export TEMP="$T" TMP="$T"
  start=$(date +%s)
  npx remotion render out/bundle film-short "$OUT/short_$n.mp4" --props="$P/short_$n$SUF.json" --crf=20 --concurrency=6 --timeout=240000 \
    > "$W/render_$n$SUF.log" 2>&1 && echo "short $n OK $(( $(date +%s) - start ))s" || { echo "short $n FAILED"; tail -5 "$W/render_$n$SUF.log"; }
  rm -rf "$T"
done
