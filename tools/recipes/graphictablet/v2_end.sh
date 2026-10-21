#!/bin/sh
# v2 (Aly 2026-10-21: "اوعى تحط qr code لاي فيديو يوتيوب من غير ال thumbnail بتاعه"): only the END changed -> render just the end frames
# and splice them onto the v1 render (picture before the end + the whole v1 audio untouched) -> output/v2/short_N.mp4 (-16 LUFS, CRF 23)
W="$(cd "$(dirname "$0")/.." && pwd)"; O="$W/../output"
ML="$W/../../../motion-library"; P="public/projects/2026-10-21 shorts graphictablet"
cd "$ML" || exit 1
[ -f out/bundle/index.html ] || npx remotion bundle --out-dir out/bundle > /dev/null 2>&1
mkdir -p "$O/v2" "$W/tail"
T="$ML/out/tmp_render"
for n in "$@"; do
  F=$(python -c "import json;d=json.load(open('$P/short_$n.json',encoding='utf8'));e=[s for s in d['scenes'] if s['t']=='tb_end'][0];print(round(e['at']*30), round(d['duration']*30)-1)")
  set -- $F; a=$1; b=$2
  mkdir -p "$T"; export TEMP="$(cygpath -w "$T")" TMP="$(cygpath -w "$T")"
  npx remotion render out/bundle film-short "$W/tail/end_$n.mp4" --props="$P/short_$n.json" --frames=$a-$b --crf=18 --muted > "$W/tail/end_$n.log" 2>&1 || { echo "end $n FAILED"; tail -3 "$W/tail/end_$n.log"; continue; }
  rm -rf "$T"
  ffmpeg -v error -y -i "$O/_raw/short_$n.mp4" -i "$W/tail/end_$n.mp4" -filter_complex \
    "[0:v]trim=end_frame=$a,setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v]" \
    -map "[v]" -map 0:a -c:v libx264 -crf 18 -preset fast -c:a copy "$O/_raw/short_${n}_v2.mp4" && echo "short $n spliced at frame $a"
done
