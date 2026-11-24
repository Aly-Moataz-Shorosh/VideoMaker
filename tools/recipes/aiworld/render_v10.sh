#!/bin/sh
# rough cut v10 (1920x1080): muted picture in 4 chunks (D:/Temp/aiw10_chunks) -> concat -> + mix -> handles burned in. ONE video only (Aly v9 note 38: no clean copy, no Premiere).
set -e
PRJ="$(pwd)"; ML="$PRJ/../../motion-library"; C=/d/Temp/aiw10_chunks; mkdir -p $C /d/Temp/aiw3_tmp
export TEMP='D:\Temp\aiw3_tmp' TMP='D:\Temp\aiw3_tmp'
PROPS="$(cygpath -w "$PRJ/work/props_v10.json")"
N=$(python -c "import json;print(round(json.load(open('work/props_v10.json',encoding='utf-8'))['duration']*25))"); S=$(( (N + 3) / 4 ))
cd "$ML"
B=D:/Temp/bundle_aiw10; [ -f $B/index.html ] || npx remotion bundle --out-dir $B > /dev/null 2>&1
i=0; s=0
while [ $s -lt $N ]; do
  e=$((s + S - 1)); [ $e -ge $N ] && e=$((N - 1))
  f=$C/part_$i.mp4
  [ -f $f ] || { npx remotion render $B ai-world-v10 "$(cygpath -w $f.tmp.mp4)" --frames=$s-$e --muted --crf=20 --concurrency=6 --timeout=240000 --props="$PROPS" > $C/log_$i.txt 2>&1 && mv $f.tmp.mp4 $f && echo "part $i done $(date +%T)" || { echo "part $i FAILED"; exit 1; }; }
  rm -rf /d/Temp/aiw3_tmp/*; i=$((i + 1)); s=$((e + 1))
done
npx remotion still $B ai-world-v10-handles "$(cygpath -w "$C/handles_layer.png")" --frame=0 --image-format=png --props='{"outW":1920,"duration":10}' > /dev/null 2>&1
cd "$PRJ"; : > $C/list.txt; for p in $(ls $C/part_*.mp4 | sort -V); do echo "file '$(cygpath -w $p)'" >> $C/list.txt; done
ffmpeg -v error -y -f concat -safe 0 -i $C/list.txt -i output/audio_stems_v10/mix_rough_v10.wav -i $C/handles_layer.png -filter_complex "[0:v][2]overlay=0:0[v]" -map "[v]" -map 1:a -c:v h264_nvenc -preset p5 -cq 21 -c:a aac -b:a 256k -shortest output/rough_cut_v10.mp4 \
 || ffmpeg -v error -y -f concat -safe 0 -i $C/list.txt -i output/audio_stems_v10/mix_rough_v10.wav -i $C/handles_layer.png -filter_complex "[0:v][2]overlay=0:0[v]" -map "[v]" -map 1:a -c:v libx264 -crf 19 -preset fast -c:a aac -b:a 256k -shortest output/rough_cut_v10.mp4
echo "DONE $(date +%T)"; ffprobe -v error -show_entries format=duration -of csv=p=0 output/rough_cut_v10.mp4
