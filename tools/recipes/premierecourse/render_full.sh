#!/bin/sh
# Render the whole course in 20-min video chunks (muted) + ONE audio pass, then join (no audio seams between chunks).
# Temp on E: in out/tmp_render, deleted after every chunk (Remotion temp filled the disks before).
# Usage: sh render_full.sh            (skips chunks that already exist; delete a chunk file to re-render it)
W="$(cd "$(dirname "$0")/.." && pwd)"
ML="$W/../../../motion-library"
OUT="$(cygpath -m "$W/../output/full")"; mkdir -p "$OUT"; FINAL="$(cygpath -m "$W/../output")/premiere_course_full.mp4"
PROPS="$(cygpath -m "$W/props_full.json")"
cd "$ML" || exit 1
[ -f out/bundle/index.html ] || npx remotion bundle --out-dir out/bundle > /dev/null 2>&1
TOTAL=$(python -c "import json;p=json.load(open(r'$PROPS',encoding='utf-8'));print(round(p['duration']*p['fps']))")
CH=30000
T="$(pwd)/out/tmp_render"
i=0; s=0
while [ $s -lt $TOTAL ]; do
  e=$((s + CH - 1)); [ $e -ge $TOTAL ] && e=$((TOTAL - 1))
  f="$OUT/v_$(printf %02d $i).mp4"
  if [ ! -f "$f" ]; then
    mkdir -p "$T"; export TEMP="$T" TMP="$T"
    st=$(date +%s)
    npx remotion render out/bundle course "$f.part.mp4" --props="$PROPS" --frames=$s-$e --muted --crf=20 --concurrency=6 --timeout=240000 > "$W/render_full_$i.log" 2>&1 \
      && mv "$f.part.mp4" "$f" && echo "chunk $i ($s-$e) OK $(( $(date +%s) - st ))s" || { echo "chunk $i FAILED"; tail -5 "$W/render_full_$i.log"; exit 1; }
    rm -rf "$T"
  fi
  i=$((i + 1)); s=$((e + 1))
done
if [ ! -f "$OUT/audio.wav" ]; then
  mkdir -p "$T"; export TEMP="$T" TMP="$T"
  npx remotion render out/bundle course "$OUT/audio.wav" --props="$PROPS" --codec=wav --timeout=240000 > "$W/render_full_audio.log" 2>&1 && echo "audio OK" || { echo "audio FAILED"; tail -5 "$W/render_full_audio.log"; exit 1; }
  rm -rf "$T"
fi
ls "$OUT"/v_*.mp4 | sed "s/.*/file '&'/" > "$OUT/list.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$OUT/list.txt" -i "$OUT/audio.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -movflags +faststart "$FINAL" && echo "JOINED"
