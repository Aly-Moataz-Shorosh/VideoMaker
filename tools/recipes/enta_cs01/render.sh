#!/bin/sh
# Render the episode in 5-min MUTED chunks (temp on E: in out/tmp_render, deleted after each chunk), then the soundtrack with
# ffmpeg (his voice untouched + sfx cues, mix_audio.py) and join. Skips chunks that already exist.
# Usage (from anywhere): sh render.sh review_01
NAME=${1:-review_01}
W="$(cd "$(dirname "$0")/.." && pwd)"
ML="$W/../../../../motion-library"
OUT="$(cygpath -m "$W/../output/$NAME")"; mkdir -p "$OUT"
PROPS="$(cygpath -m "$ML/public/projects/entacs01/edit_$NAME.json")"
cd "$ML" || exit 1
[ -f out/bundle/index.html ] || npx remotion bundle --out-dir out/bundle > /dev/null 2>&1
TOTAL=$(python -c "import json;p=json.load(open(r'$PROPS',encoding='utf-8'));print(round(p['duration']*p['fps']))")
CH=9000; T="$(pwd)/out/tmp_render"; i=0; s=0
while [ $s -lt $TOTAL ]; do
  e=$((s + CH - 1)); [ $e -ge $TOTAL ] && e=$((TOTAL - 1))
  f="$OUT/v_$(printf %02d $i).mp4"
  if [ ! -f "$f" ]; then
    mkdir -p "$T"; export TEMP="$(cygpath -w "$T")" TMP="$(cygpath -w "$T")"
    st=$(date +%s)
    npx remotion render out/bundle edit "$f.part.mp4" --props="$PROPS" --frames=$s-$e --muted --crf=20 --concurrency=10 --timeout=240000 > "$W/render_$i.log" 2>&1 \
      && mv "$f.part.mp4" "$f" && echo "chunk $i ($s-$e) OK $(( $(date +%s) - st ))s" || { echo "chunk $i FAILED"; tail -5 "$W/render_$i.log"; exit 1; }
    rm -rf "$T"
  fi
  i=$((i + 1)); s=$((e + 1))
done
python -X utf8 "$W/scripts/mix_audio.py" "$PROPS" "$OUT" || exit 1
ls "$OUT"/v_*.mp4 | sed "s/.*/file '&'/" > "$OUT/list.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$OUT/list.txt" -i "$OUT/audio.m4a" -map 0:v -map 1:a -c copy -movflags +faststart "$OUT/../$NAME.mp4" && echo "JOINED $OUT/../$NAME.mp4"
