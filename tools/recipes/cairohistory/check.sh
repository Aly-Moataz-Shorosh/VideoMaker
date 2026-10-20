#!/bin/sh
# Still check of one short: 2 frames per scene (45% / 90%) -> work/sheets/s<n>_<tag>.jpg
# Usage (from anywhere): sh check.sh <n> [tag]
n=$1; tag=${2:-a}; SUF=${V:+_$V}
W="$(cd "$(dirname "$0")/.." && pwd)"
ML="$W/../../../motion-library"
P="public/projects/2026-10-09 shorts cairohistory"
cd "$ML" || exit 1
mkdir -p out/tmp
export TEMP="$(pwd)/out/tmp" TMP="$(pwd)/out/tmp"
FR=$(python -c "
import json
d=json.load(open('$P/short_$n$SUF.json',encoding='utf8')); fr=[]
for s in d['scenes']:
  a=s['at']*30; b=(s['at']+s['dur'])*30; fr+=[int(a+(b-a)*0.45), int(a+(b-a)*0.9)]
print(' '.join(map(str,sorted(set(fr)))))")
sh stills_cli.sh film-short "$P/short_$n$SUF.json" "$W/sheets/s${n}_$tag.jpg" $FR 2>&1 | tail -1
