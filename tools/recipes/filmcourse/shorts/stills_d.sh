#!/bin/bash
# Still check sheets for the film shorts with the bundle + temp on D: (E: almost full, 2026-11-07).
#   bash stills_d.sh picks.txt   (lines: "NN frame frame ...")  -> work/shorts/st_NN.jpg
cd "$(dirname "$0")/../../../../motion-library"
W="$(cygpath -m "$(cd '../projects/2026-11-06 youtube intro to film making course/work/shorts' && pwd)")"
B=/d/Temp/fs_bundle
[ -f $B/index.html ] || npx remotion bundle --out-dir $B > /dev/null 2>&1
T=/d/Temp/fs_stills; mkdir -p $T
while read n frames; do
  i=0; mkdir -p $T/$n
  for fr in $frames; do
    mkdir -p $T/t; export TEMP="$(cygpath -w $T/t)" TMP="$(cygpath -w $T/t)"
    npx remotion still $B course-short "$T/$n/$(printf %02d $i).png" --frame=$fr --scale=0.4 --timeout=240000 --props="$W/props_$n.json" > $T/log.txt 2>&1 || { echo "fail $n $fr"; tail -2 $T/log.txt; }
    rm -rf $T/t; i=$((i+1))
  done
  python -I -c "
import sys, glob
from PIL import Image
fs = sorted(glob.glob(sys.argv[1] + '/*.png')); ims = [Image.open(f).convert('RGB') for f in fs]
w, h = ims[0].size; s = Image.new('RGB', (len(ims) * (w + 6), h))
for i, im in enumerate(ims): s.paste(im, (i * (w + 6), 0))
s.save(sys.argv[2], quality=80)" "$T/$n" "$W/st_$n.jpg"
  echo "sheet $n"
done < "$1"
rm -rf $T
