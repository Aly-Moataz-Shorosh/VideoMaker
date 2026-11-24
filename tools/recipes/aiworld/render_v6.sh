#!/bin/sh
# rough cut v6: muted picture in 4 chunks (D:/Temp/aiw6_chunks, delete one to redo it) -> concat -> + mix_rough_v6.wav. Old versions untouched.
set -e
PRJ="$(pwd)"; ML="$PRJ/../../motion-library"; C=/d/Temp/aiw6_chunks; mkdir -p $C /d/Temp/aiw3_tmp
export TEMP='D:\Temp\aiw3_tmp' TMP='D:\Temp\aiw3_tmp'
PROPS="$(cygpath -w "$PRJ/work/props_v6.json")"; N=34887; S=8722
cd "$ML"
B=D:/Temp/bundle_aiw6; [ -f $B/index.html ] || npx remotion bundle --out-dir $B > /dev/null 2>&1
i=0; s=0
while [ $s -lt $N ]; do
  e=$((s + S - 1)); [ $e -ge $N ] && e=$((N - 1))
  f=$C/part_$i.mp4
  [ -f $f ] || { npx remotion render $B ai-world-v6 "$(cygpath -w $f.tmp.mp4)" --frames=$s-$e --muted --crf=20 --concurrency=6 --timeout=240000 --props="$PROPS" > $C/log_$i.txt 2>&1 && mv $f.tmp.mp4 $f && echo "part $i done $(date +%T)" || { echo "part $i FAILED"; exit 1; }; }
  rm -rf /d/Temp/aiw3_tmp/*; i=$((i + 1)); s=$((e + 1))
done
cd "$PRJ"; : > $C/list.txt; for p in $(ls $C/part_*.mp4 | sort -V); do echo "file '$(cygpath -w $p)'" >> $C/list.txt; done
ffmpeg -v error -y -f concat -safe 0 -i $C/list.txt -c copy $C/video.mp4
ffmpeg -v error -y -i $C/video.mp4 -i output/audio_stems_v6/mix_rough_v6.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest output/rough_cut_v6.mp4
echo "DONE $(date +%T)"; ffprobe -v error -show_entries format=duration -of csv=p=0 output/rough_cut_v6.mp4
