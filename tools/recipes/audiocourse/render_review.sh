#!/bin/sh
# Render props_<name>.json muted (TEMP on E:, deleted after), then mix_audio.py -> output/<name>.mp4
#   sh render_review.sh review1
N=$1
W="$(cd "$(dirname "$0")/.." && pwd)"; ML="$W/../../../motion-library"
PROPS="$(cygpath -m "$W/props_$N.json")"; OUT="$(cygpath -m "$W/../output")"; mkdir -p "$OUT"
cd "$ML" || exit 1
[ -f out/bundle/index.html ] || npx remotion bundle --out-dir out/bundle > /dev/null 2>&1
T="$(pwd)/out/tmp_render"; mkdir -p "$T"; export TEMP="$(cygpath -w "$T")" TMP="$(cygpath -w "$T")"
st=$(date +%s)
npx remotion render out/bundle course "$OUT/_${N}_muted.mp4" --props="$PROPS" --muted --crf=20 --concurrency=6 --timeout=240000 > "$W/render_$N.log" 2>&1 || { echo FAILED; tail -5 "$W/render_$N.log"; rm -rf "$T"; exit 1; }
rm -rf "$T"
echo "video $(( $(date +%s) - st ))s"
python "$(cygpath -m "$W/scripts/mix_audio.py")" "$PROPS" "$OUT/_${N}_muted.mp4" "$OUT/$N.mp4" && rm "$OUT/_${N}_muted.mp4"
