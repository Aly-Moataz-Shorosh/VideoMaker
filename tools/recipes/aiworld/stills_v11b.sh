#!/bin/sh
# still check of every v11 note (work/still_checks_v11b.json) -> D:/Temp/st11b/NN.png + sheets of 12
cd ../../motion-library
P="$(cygpath -w "$PWD/../projects/2026-11-20 avatar aiFullVideoCost/work/props_v11.json")"; O=/d/Temp/st11b; rm -rf $O; mkdir -p $O/t
python -X utf8 -c "import json;[print(round(t*25)) for n,t in json.load(open('../projects/2026-11-20 avatar aiFullVideoCost/work/still_checks_v11b.json',encoding='utf-8'))]" > $O/frames.txt
i=0; while read f; do
  TEMP='D:\Temp\st11b\t' TMP='D:\Temp\st11b\t' npx remotion still D:/Temp/bundle_aiw11 ai-world-v11 "$O/$(printf %02d $i).png" --frame=$f --scale=0.4 --timeout=240000 --props="$P" > $O/log.txt 2>&1 || { echo "fail $f"; tail -2 $O/log.txt; }
  rm -rf $O/t; mkdir -p $O/t; i=$((i+1))
done < $O/frames.txt
python -I -c "
import glob, json
from PIL import Image, ImageDraw
L=json.load(open(r'../projects/2026-11-20 avatar aiFullVideoCost/work/still_checks_v11b.json',encoding='utf-8'))
fs=sorted(glob.glob('D:/Temp/st11b/[0-9]*.png'))
for k in range(0,len(fs),12):
  ims=[Image.open(f).convert('RGB') for f in fs[k:k+12]]; w,h=ims[0].size; s=Image.new('RGB',(3*(w+6),4*(h+6)))
  for i,im in enumerate(ims):
    n,t=L[k+i]; ImageDraw.Draw(im).rectangle((0,0,330,22),fill=(0,0,0)); ImageDraw.Draw(im).text((4,4),f'{k+i} {n} {int(t//60)}:{t%60:04.1f}',fill=(255,255,0)); s.paste(im,((i%3)*(w+6),(i//3)*(h+6)))
  s.save(f'D:/Temp/st11b/sheet_{k//12}.jpg',quality=85)
print('sheets', (len(fs)+11)//12)"
