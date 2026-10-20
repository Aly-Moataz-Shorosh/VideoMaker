#!/bin/sh
# Reliable still check (stills.mjs drops parts of heavy SVG frames): one CLI still per frame -> one sheet.
# Uses ONE bundle in out/bundle (each fresh bundle copies public/ ~2 GB into C:\Temp — that filled C: on 2026-10-08).
# Usage (from motion-library): sh stills_cli.sh <comp> <props.json> <out.jpg> <frame> [<frame> ...]
# After changing src/: rm -rf out/bundle (it is rebuilt here).
comp=$1; props=$2; out=$3; shift 3
B=${BUNDLE:-out/bundle}
[ -f $B/index.html ] || npx remotion bundle --out-dir $B > /dev/null 2>&1
tmp=$(mktemp -d -p out); i=0
# Remotion copies assets into TEMP for every still (0.24 GB each, filled C: on 2026-10-18) -> keep it inside $tmp on E: and delete it
mkdir -p "$tmp/t"; export TEMP="$(cygpath -w "$PWD/$tmp/t")" TMP="$(cygpath -w "$PWD/$tmp/t")"
for f in "$@"; do
  npx remotion still $B "$comp" "$tmp/$(printf %02d $i).png" --frame=$f --scale=0.4 --timeout=240000 --props="$props" > "$tmp/log.txt" 2>&1 || { echo "fail $f"; tail -3 "$tmp/log.txt"; }
  rm -rf "$tmp/t"; mkdir -p "$tmp/t"   # every still copies public/ (incl. a 2 GB source) into TEMP: 11 stills filled E: on 2026-10-20
  i=$((i+1))
done
# montage with PIL (2026-10-14: the ffmpeg tile filter dropped the first frames of big sheets)
python -I -c "
import sys, glob
from PIL import Image
fs = sorted(glob.glob(sys.argv[1] + '/[0-9]*.png')); ims = [Image.open(f).convert('RGB') for f in fs]
c = min(5, len(ims)); r = (len(ims) + c - 1) // c; w, h = ims[0].size
s = Image.new('RGB', (c * (w + 6), r * (h + 6)))
for i, im in enumerate(ims): s.paste(im, ((i % c) * (w + 6), (i // c) * (h + 6)))
s.save(sys.argv[2], quality=82)" "$tmp" "$out"
rm -rf "$tmp"; echo "sheet $out"
