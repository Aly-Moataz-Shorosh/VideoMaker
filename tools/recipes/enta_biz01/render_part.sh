#!/bin/sh
# Render a PART of the episode with sound (for a quick review, e.g. the opening): sh render_part.sh review_01 0 6000 opening
# -> output/<name>_<tag>.mp4 (muted Remotion render of frames START..END, then his audio + sfx of that range mixed with ffmpeg).
NAME=$1; S=$2; E=$3; TAG=${4:-part}
W="$(cd "$(dirname "$0")/.." && pwd)"
ML="$W/../../../../motion-library"
OUT="$(cygpath -m "$W/../output")"; mkdir -p "$OUT/_parts"
PROPS="$(cygpath -m "$ML/public/projects/entabiz01/edit_$NAME.json")"
cd "$ML" || exit 1
[ -f out/bundle/index.html ] || npx remotion bundle --out-dir out/bundle > /dev/null 2>&1
T="$(pwd)/out/tmp_render"; mkdir -p "$T"; export TEMP="$(cygpath -w "$T")" TMP="$(cygpath -w "$T")"
npx remotion render out/bundle edit "$OUT/_parts/v_${TAG}.mp4" --props="$PROPS" --frames=$S-$E --muted --crf=20 --concurrency=8 --timeout=240000 > "$W/render_$TAG.log" 2>&1 \
  || { echo "render FAILED"; tail -5 "$W/render_$TAG.log"; rm -rf "$T"; exit 1; }
rm -rf "$T"
python -X utf8 "$W/scripts/mix_audio.py" "$PROPS" "$OUT/_parts" || exit 1
ffmpeg -v error -y -i "$OUT/_parts/v_${TAG}.mp4" -ss $(python -c "print($S/30)") -t $(python -c "print(($E-$S+1)/30)") -i "$OUT/_parts/audio.m4a" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "$OUT/${NAME}_${TAG}.mp4" \
  && rm -f "$OUT/_parts/audio.m4a" && echo "OK $OUT/${NAME}_${TAG}.mp4"
