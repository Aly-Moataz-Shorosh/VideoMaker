#!/bin/sh
# render vertical shorts: sh scripts/render_shorts.sh N [N ...]   (run from work/)
# audio = the v11 final mix cut per piece (10 ms fades) + silence under an end card, levelled -16 LUFS / -1.5 dBTP;
# picture = comp ai-world-vshort (bundle D:/Temp/bundle_short, temp on D:), frame count checked; output compressed (CRF 23) to output/shorts/.
set -e
W="$PWD"; ML="$W/../../../motion-library"; SRC="$W/../output/rough_cut_v11.mp4"; T=/d/Temp/shr; mkdir -p $T "$W/../output/shorts"
for n in "$@"; do
  N=$(printf %02d $n)
  SLUG=$(python -c "import sys;sys.path.insert(0,'scripts');from shorts_data import SHORTS;print([s['slug'] for s in SHORTS if s['n']==$n][0])")
  P="$(cygpath -w "$W/shorts/vprops_$N.json")"
  # ---- audio
  python -I - "$P" "$(cygpath -w "$SRC")" "$(cygpath -w $T/a_$N.wav)" <<'PY'
import json, subprocess, sys
p = json.load(open(sys.argv[1], encoding='utf-8')); src, out = sys.argv[2], sys.argv[3]
fl, ins = [], []
for i, pc in enumerate(p['pieces']):
    d = pc['b'] - pc['a']
    fl.append(f"[0:a]atrim={pc['a']:.3f}:{pc['b']:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={max(0, d - 0.01):.3f}:d=0.01[p{i}]"); ins.append(f"[p{i}]")
tail = p['duration'] - sum(pc['b'] - pc['a'] for pc in p['pieces'])
if tail > 0.05: fl.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{tail:.3f}[sil]"); ins.append("[sil]")
fl.append(''.join(ins) + f"concat=n={len(ins)}:v=0:a=1,aresample=48000,loudnorm=I=-16:TP=-1.5:LRA=11[a]")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-filter_complex', ';'.join(fl), '-map', '[a]', '-ar', '48000', '-ac', '2', out], check=True)
PY
  # ---- picture
  NF=$(python -c "import json;p=json.load(open(r'$P',encoding='utf-8'));print(round(p['duration']*25))")
  (cd "$ML" && TEMP='D:\Temp\shr\t' TMP='D:\Temp\shr\t' npx remotion render D:/Temp/bundle_short ai-world-vshort "$(cygpath -w $T/v_$N.mp4)" --muted --crf=18 \
     --concurrency=6 --timeout=240000 --props="$P" > $T/log_$N.txt 2>&1) || { echo "#$N render FAILED"; tail -5 $T/log_$N.txt; continue; }
  rm -rf $T/t
  got=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nk=1:nw=1 $T/v_$N.mp4 | tr -cd 0-9)
  [ "$got" = "$NF" ] || echo "#$N WARNING frames $got expected $NF"
  OUT="$W/../output/shorts/${N}_$SLUG.mp4"
  ffmpeg -v error -y -i $T/v_$N.mp4 -i $T/a_$N.wav -map 0:v -map 1:a -c:v libx264 -crf 23 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
  echo "#$N done -> output/shorts/${N}_$SLUG.mp4 ($(du -h "$OUT" | cut -f1))"
done
