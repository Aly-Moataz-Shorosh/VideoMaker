#!/bin/sh
# whole song vertical reel: sh scripts/render_vsong.sh   (run from work/, after song_vreel_props.py)
# audio = v11 final mix of the song (exact) + 8 s calm instrumental under the end card (-14 dB, fades), levelled -16 LUFS / -1.5 dBTP.
# picture = comp ai-world-vsong (fresh bundle D:/Temp/bundle_vsong, temp on D:), frame count checked, CRF 23 -> output/shorts/song_full_vertical.mp4
set -e
W="$PWD"; ML="$W/../../../motion-library"; SRC="$W/../output/rough_cut_v11.mp4"; MUS="$W/../output/audio_stems_v11/music/song_C1_music_only_timeline.wav"
T=/d/Temp/vsong; mkdir -p $T "$W/../output/shorts"
P="$(cygpath -w "$W/shorts/vsong_props.json")"
read A SD D <<EOF
$(python -c "import json;p=json.load(open(r'$P',encoding='utf-8'));print(p['start'],p['songDur'],p['duration'])")
EOF
E=$(python -c "print(round($D-$SD,3))")
ffmpeg -v error -y -ss $A -t $SD -i "$SRC" -ss $(python -c "print($A+2.0)") -t $E -i "$MUS" -filter_complex \
 "[0:a]aresample=48000,asetpts=PTS-STARTPTS[s];[1:a]aresample=48000,volume=-14dB,afade=t=in:d=1.0,afade=t=out:st=$(python -c "print($E-2.0)"):d=2.0[m];[s][m]concat=n=2:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=11[a]" \
 -map "[a]" -ar 48000 -ac 2 $T/a.wav
if [ ! -d /d/Temp/bundle_vsong ]; then (cd "$ML" && npx remotion bundle src/index.ts --out-dir D:/Temp/bundle_vsong > $T/bundle.txt 2>&1); fi
NF=$(python -c "print(round($D*25))")
(cd "$ML" && TEMP='D:\Temp\vsong\t' TMP='D:\Temp\vsong\t' npx remotion render D:/Temp/bundle_vsong ai-world-vsong "$(cygpath -w $T/v.mp4)" --muted --crf=18 \
   --concurrency=6 --timeout=240000 --props="$P" > $T/log.txt 2>&1) || { echo "render FAILED"; tail -5 $T/log.txt; exit 1; }
rm -rf $T/t
got=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nk=1:nw=1 $T/v.mp4 | tr -cd 0-9)
[ "$got" = "$NF" ] || echo "WARNING frames $got expected $NF"
OUT="$W/../output/shorts/song_full_vertical.mp4"
ffmpeg -v error -y -i $T/v.mp4 -i $T/a.wav -map 0:v -map 1:a -c:v libx264 -crf 23 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
echo "done -> $OUT ($(du -h "$OUT" | cut -f1))"
