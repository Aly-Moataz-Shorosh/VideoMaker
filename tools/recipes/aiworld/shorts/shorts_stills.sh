#!/bin/sh
# still sheet of one short: shorts_stills.sh N "t1 t2 ..." (output seconds) -> D:/Temp/shst/NN_sheet.jpg
N=$(printf %02d $1); TS="$2"; O=/d/Temp/shst; mkdir -p $O/t; rm -f $O/${N}_*.png
cd "$(dirname "$0")/../../../../motion-library"
P="$(cygpath -w "$PWD/../projects/2026-11-20 avatar aiFullVideoCost/work/shorts/vprops_$N.json")"
i=0; for t in $TS; do
  f=$(python -c "print(round($t*25))")
  TEMP='D:\Temp\shst\t' TMP='D:\Temp\shst\t' npx remotion still D:/Temp/bundle_short ai-world-vshort "$O/${N}_$i.png" --frame=$f --scale=0.5 --timeout=240000 --props="$P" > $O/log.txt 2>&1 || { echo "fail $t"; tail -3 $O/log.txt; }
  rm -rf $O/t; mkdir -p $O/t; i=$((i+1))
done
python -I -c "
import glob,sys
from PIL import Image, ImageDraw
fs=sorted(glob.glob('D:/Temp/shst/$N'+'_*.png'),key=lambda f:int(f.split('_')[-1][:-4])); ts='$TS'.split()
ims=[Image.open(f).convert('RGB') for f in fs]; w,h=ims[0].size; n=len(ims); s=Image.new('RGB',(n*(w+8),h+30),(40,40,40))
for i,im in enumerate(ims): s.paste(im,(i*(w+8),30)); ImageDraw.Draw(s).text((i*(w+8)+6,8),ts[i]+'s',fill=(255,255,0))
s.save('D:/Temp/shst/${N}_sheet.jpg',quality=82); print('sheet', n)"
