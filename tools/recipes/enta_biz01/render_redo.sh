#!/bin/sh
# Smart re-render after a review (Aly 2026-10-28: "متعيدش الفيديو كله… عيد بس الموشن للحتت دي و بعدين جمع الفيديو"):
#   1) only the changed parts (work/redo_parts.json from redo_parts.py) are rendered, muted, as p_NN.mp4
#   2) the 'fix' overlay layer (Edit layer 'fix' = the renamed name tag + Meet's speaking dots covered, transparent elsewhere)
#      is rendered as PNGs for the whole timeline (empty while a board is on -> fast)
#   3) ffmpeg: old muted chunks + overlay, then every new part laid over its own frames -> one video; sound re-mixed whole
#      (his voice untouched + sfx, mix_audio.py) and joined.
# Usage (from anywhere): sh render_redo.sh review_02 <old chunks dir>   (big temp files on D:, E: is nearly full)
NAME=${1:-review_02}
OLD=${2:-D:/Temp/biz01_chunks}
W="$(cd "$(dirname "$0")/.." && pwd)"
ML="$W/../../../../motion-library"
D=${REDO_DIR:-D:/Temp/biz_redo_$NAME}; mkdir -p "$D/parts" "$D/fix"
PROPS="$(cygpath -m "$ML/public/projects/entabiz01/edit_$NAME.json")"
FIXP="$D/fix_props.json"
python -X utf8 -c "import json,sys; p=json.load(open(sys.argv[1],encoding='utf8')); p['layer']='fix'; json.dump(p,open(sys.argv[2],'w',encoding='utf8'),ensure_ascii=False)" "$PROPS" "$FIXP"
cd "$ML" || exit 1
[ -f out/bundle/index.html ] || npx remotion bundle --out-dir out/bundle > /dev/null 2>&1
T=${RTMP:-/d/Temp/biz_redo_tmp}
run() { mkdir -p "$T"; export TEMP="$(cygpath -w "$T")" TMP="$(cygpath -w "$T")"; "$@"; r=$?; rm -rf "$T"; return $r; }
# 1) changed parts
i=0
for pr in $(python -c "import json,sys; print(' '.join('%d-%d' % (a, b) for a, b in json.load(open(sys.argv[1]))))" "$(cygpath -w "$W/redo_parts.json")"); do
  f="$D/parts/p_$(printf %02d $i).mp4"
  if [ ! -f "$f" ]; then
    st=$(date +%s)
    run npx remotion render out/bundle edit "$f.part.mp4" --props="$PROPS" --frames=$pr --muted --crf=18 --concurrency=8 --timeout=240000 > "$W/redo_$i.log" 2>&1 \
      && mv "$f.part.mp4" "$f" && echo "part $i ($pr) OK $(( $(date +%s) - st ))s" || { echo "part $i FAILED"; tail -5 "$W/redo_$i.log"; exit 1; }
  fi
  i=$((i + 1))
done
# 2) the fix overlay, whole timeline, 9000-frame runs (PNG frames named by frame number)
TOTAL=$(python -c "import json;p=json.load(open(r'$PROPS',encoding='utf-8'));print(round(p['duration']*p['fps']))")
s=0
while [ $s -lt $TOTAL ]; do
  e=$((s + 8999)); [ $e -ge $TOTAL ] && e=$((TOTAL - 1))
  if [ ! -f "$D/fix/done_$s" ]; then
    st=$(date +%s)
    run npx remotion render out/bundle edit "$D/fix" --props="$FIXP" --frames=$s-$e --sequence --image-format=png --concurrency=10 --timeout=240000 > "$W/fix_$s.log" 2>&1 \
      && touch "$D/fix/done_$s" && echo "fix $s-$e OK $(( $(date +%s) - st ))s" || { echo "fix $s FAILED"; tail -5 "$W/fix_$s.log"; exit 1; }
  fi
  s=$((e + 1))
done
# 3) compose: old chunks + overlay, new parts over their frames; then the whole soundtrack
python -X utf8 "$W/scripts/compose_redo.py" "$OLD" "$D" "$(cygpath -w "$W/redo_parts.json")" "$D/video.mp4" || exit 1
python -X utf8 "$W/scripts/mix_audio.py" "$PROPS" "$D" || exit 1
# joined on D: (E: is nearly full) -> moved into output/ by hand once there is room
ffmpeg -v error -y -i "$D/video.mp4" -i "$D/audio.m4a" -map 0:v -map 1:a -c copy -movflags +faststart "$D/$NAME.mp4" && echo "JOINED $D/$NAME.mp4"
