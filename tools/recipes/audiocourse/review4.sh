#!/bin/sh
# Aly review 4: opening (0 - 80 s) + ending (last 32 s) only, sound from the FULL mix (mix_audio.py, session audio untouched)
W="$(cd "$(dirname "$0")/.." && pwd)"; ML="$W/../../../motion-library"; OUT="$(cygpath -m "$W/../output")"
PROPS="$(cygpath -m "$W/props_full.json")"; R="$OUT/_r4"; mkdir -p "$R"
D=$(python -c "import json;print(json.load(open(r'$PROPS',encoding='utf-8'))['duration'])")
E0=$(python -c "print(round(($D-32)*30))"); E1=$(python -c "print(round($D*30)-1)")
cd "$ML" || exit 1
T="$(pwd)/out/tmp_render"
for seg in "0-2399" "$E0-$E1"; do
  f="$R/v_$seg.mp4"; [ -f "$f" ] && continue
  mkdir -p "$T"; export TEMP="$(cygpath -w "$T")" TMP="$(cygpath -w "$T")"
  npx remotion render out/bundle course "$f" --props="$PROPS" --frames=$seg --muted --crf=20 --concurrency=6 --timeout=240000 > "$W/review4.log" 2>&1 || { echo "FAIL $seg"; tail -5 "$W/review4.log"; rm -rf "$T"; exit 1; }
  rm -rf "$T"
done
ffmpeg -v error -y -f lavfi -i "color=c=black:s=64x36:r=1:d=$D" -c:v libx264 "$R/blank.mp4"
python -X utf8 "$(cygpath -m "$W/scripts/mix_audio.py")" "$PROPS" "$R/blank.mp4" "$R/mix.mp4" || exit 1
ffmpeg -v error -y -i "$R/v_0-2399.mp4" -ss 0 -t 80 -i "$R/mix.mp4" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k "$R/a.mp4"
ffmpeg -v error -y -i "$R/v_$E0-$E1.mp4" -ss $(python -c "print($E0/30)") -t 32 -i "$R/mix.mp4" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest "$R/b.mp4"
printf "file '%s'\nfile '%s'\n" "$R/a.mp4" "$R/b.mp4" > "$R/list.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$R/list.txt" -c copy "$OUT/review4.mp4" && echo "DONE $OUT/review4.mp4"
