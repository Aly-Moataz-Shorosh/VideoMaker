#!/bin/sh
# Whole course: 5-min MUTED chunks (temp on E: out/tmp_render, deleted after each chunk; existing chunks are skipped, delete one to
# redo it), join them, then mix_audio.py (session audio untouched) -> output/<name>.mp4
#   sh render_full.sh audio_course_full
N=${1:-audio_course_full}
W="$(cd "$(dirname "$0")/.." && pwd)"; ML="$W/../../../motion-library"
PROPS="$(cygpath -m "$W/props_full.json")"; OUT="$(cygpath -m "$W/../output")"; CHD="$OUT/_chunks"; mkdir -p "$CHD"
cd "$ML" || exit 1
[ -f out/bundle/index.html ] || npx remotion bundle --out-dir out/bundle > /dev/null 2>&1
TOTAL=$(python -c "import json;p=json.load(open(r'$PROPS',encoding='utf-8'));print(round(p['duration']*p['fps']))")
CH=9000; T="$(pwd)/out/tmp_render"; i=0; s=0
while [ $s -lt $TOTAL ]; do
  e=$((s + CH - 1)); [ $e -ge $TOTAL ] && e=$((TOTAL - 1))
  f="$CHD/v_$(printf %02d $i).mp4"
  if [ ! -f "$f" ]; then
    mkdir -p "$T"; export TEMP="$(cygpath -w "$T")" TMP="$(cygpath -w "$T")"
    st=$(date +%s)
    npx remotion render out/bundle course "$f.part.mp4" --props="$PROPS" --frames=$s-$e --muted --crf=20 --concurrency=6 --timeout=240000 > "$W/render_full_$i.log" 2>&1 \
      && mv "$f.part.mp4" "$f" && echo "chunk $i ($s-$e) OK $(( $(date +%s) - st ))s" || { echo "chunk $i FAILED"; tail -5 "$W/render_full_$i.log"; rm -rf "$T"; exit 1; }
    rm -rf "$T"
  fi
  i=$((i + 1)); s=$((e + 1))
done
ls "$CHD"/v_*.mp4 | sed "s/.*/file '&'/" > "$CHD/list.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$CHD/list.txt" -c copy "$OUT/_${N}_muted.mp4" || exit 1
python -X utf8 "$(cygpath -m "$W/scripts/mix_audio.py")" "$PROPS" "$OUT/_${N}_muted.mp4" "$OUT/$N.mp4" && rm "$OUT/_${N}_muted.mp4" && echo "DONE $OUT/$N.mp4"
