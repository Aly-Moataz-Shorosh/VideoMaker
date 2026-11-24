#!/bin/sh
# rough cut v11 (Aly v10 notes, «متعيدش الموشن من الاول غير للحاجات اللي محتاجنها»): work/redo_v11.json says, per frame range, «v10» = cut from the
# v10 picture (D:/Temp/aiw10_chunks, same seconds, identical scene) or «new» = Remotion render. Every piece is checked for its exact frame count,
# then all pieces are decoded + joined (concat FILTER, not stream copy) + handles + the v11 mix -> ONE file output/rough_cut_v11.mp4 (v9 note 38).
set -e
PRJ="$(pwd)"; ML="$PRJ/../../motion-library"; C=/d/Temp/aiw11_parts; mkdir -p $C /d/Temp/aiw11_tmp; CW=$(cygpath -m $C)   # CW = the same folder for Windows python
export TEMP='D:\Temp\aiw11_tmp' TMP='D:\Temp\aiw11_tmp'
PROPS="$(cygpath -w "$PRJ/work/props_v11.json")"; B=D:/Temp/bundle_aiw11b
[ -f $C/v10pic.mp4 ] || { : > $C/v10list.txt; for p in $(ls /d/Temp/aiw10_chunks/part_*.mp4 | sort -V); do echo "file '$(cygpath -w $p)'" >> $C/v10list.txt; done
  ffmpeg -v error -y -f concat -safe 0 -i $C/v10list.txt -c copy $C/v10pic.mp4; }
python -X utf8 -c "
import json
S=json.load(open('work/redo_v11.json'))
out=[]
for i,x in enumerate(S):
    if x['src']=='new':
        a=x['a']
        while a<x['b']:
            b=min(x['b'],a+9000); out.append(f'new {a} {b}'); a=b
    else: out.append(f\"v10 {x['a']} {x['b']}\")
open('$CW/plan.txt','w',newline=chr(10)).write('\n'.join(out)+'\n')
"
i=0; : > $C/inputs.txt
while read kind a b; do
  b=$(printf %s "$b" | tr -d '
')
  f=$C/p_$(printf %03d $i)_$kind.mp4; n=$((b - a))
  if [ ! -f $f ]; then
    if [ $kind = v10 ]; then
      ffmpeg -v error -y -ss $(python -c "print($a/25)") -i $C/v10pic.mp4 -frames:v $n -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p -r 25 -an $f.tmp.mp4
    else
      (cd "$ML" && npx remotion render $B ai-world-v11 "$(cygpath -w $f.tmp.mp4)" --frames=$a-$((b - 1)) --muted --crf=20 --concurrency=6 --timeout=240000 --props="$PROPS" > $C/log_$i.txt 2>&1) || { echo "piece $i FAILED"; tail -5 $C/log_$i.txt; exit 1; }
      rm -rf /d/Temp/aiw11_tmp/*
    fi
    got=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nk=1:nw=1 $f.tmp.mp4 | tr -cd 0-9)
    [ "$got" = "$n" ] || { echo "piece $i ($kind $a-$b) has $got frames, expected $n"; exit 1; }
    mv $f.tmp.mp4 $f; echo "piece $i $kind $a-$b ok ($n frames) $(date +%T)"
  fi
  echo "$(cygpath -m $f)" >> $C/inputs.txt; i=$((i + 1))
done < $C/plan.txt
(cd "$ML" && npx remotion still $B ai-world-v11-handles "$(cygpath -w "$C/handles_layer.png")" --frame=0 --image-format=png --props='{"outW":1920,"duration":10}' > /dev/null 2>&1)
python -X utf8 -c "
import subprocess
fs=[l.strip() for l in open('$CW/inputs.txt') if l.strip()]; K=len(fs)
ins=[]; [ins.extend(['-i',f]) for f in fs]
fc=''.join(f'[{k}:v]setpts=PTS-STARTPTS[v{k}];' for k in range(K))+''.join(f'[v{k}]' for k in range(K))+f'concat=n={K}:v=1:a=0[cat];[cat][{K+1}]overlay=0:0[v]'
open('$CW/fc.txt','w').write(fc)
base=['ffmpeg','-v','error','-y',*ins,'-i','output/audio_stems_v11/mix_rough_v11.wav','-i','$CW/handles_layer.png','-filter_complex_script','$CW/fc.txt','-map','[v]','-map',f'{K}:a']
r=subprocess.run(base+['-c:v','h264_nvenc','-preset','p5','-cq','21','-c:a','aac','-b:a','256k','-shortest','output/rough_cut_v11.mp4'])
if r.returncode: subprocess.run(base+['-c:v','libx264','-crf','19','-preset','fast','-c:a','aac','-b:a','256k','-shortest','output/rough_cut_v11.mp4'],check=True)
"
echo "DONE $(date +%T)"; ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames:format=duration -of csv=p=0 output/rough_cut_v11.mp4
