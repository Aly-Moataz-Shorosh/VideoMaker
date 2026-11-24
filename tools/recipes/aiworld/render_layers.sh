#!/bin/sh
# Transparent HUD layers (Tip 2): WebM VP9 alpha (+ ProRes 4444 for the main ones) -> output/layers_alpha_v1/
# Run from anywhere: sh work/scripts/render_layers.sh   (bundle = motion-library/out/bundle_aiw)
cd "$(dirname "$0")/../../../../motion-library" || exit 1
O="../projects/2026-11-20 avatar aiFullVideoCost/output/layers_alpha_v1"; mkdir -p "$O" out/tmp/t
export TEMP="$(cygpath -w "$PWD/out/tmp/t")" TMP="$(cygpath -w "$PWD/out/tmp/t")"
r() { # name props [mov]
  [ -f "$O/$1.webm" ] || npx remotion render out/bundle_aiw ai-world-hud "$O/$1.webm" --image-format=png --codec=vp9 --pixel-format=yuva420p --concurrency=6 --props="$2" > out/tmp/l.log 2>&1 || echo "FAIL $1"
  [ -n "$3" ] && { [ -f "$O/$1.mov" ] || npx remotion render out/bundle_aiw ai-world-hud "$O/$1.mov" --image-format=png --codec=prores --prores-profile=4444 --pixel-format=yuva444p10le --concurrency=6 --props="$2" > out/tmp/l.log 2>&1 || echo "FAIL $1.mov"; }
  echo "done $1"
}
r badge_10s '{"kind":"badge","duration":10}' mov
r families_8s '{"kind":"families","duration":8}' mov
r counter_3_to_28 '{"kind":"counter","from":3,"to":28,"label":"فيديو في الأسبوع","duration":5}' mov
r counter_474k '{"kind":"counter","from":0,"to":474000,"label":"مشاهدة في آخر شهر","duration":5}' mov
r counter_31_shorts '{"kind":"counter","from":1,"to":31,"label":"شورت من كورس واحد","duration":5}'
python -I -X utf8 -c "
import json,sys
tl=json.load(open(sys.argv[1],encoding='utf-8'))
for c in tl['chapters']: print(c['id']+'\t'+c['title'])" "$(cygpath -w "$PWD/../projects/2026-11-20 avatar aiFullVideoCost/work/timeline_v1.json")" | tr -d '\r' | while IFS="$(printf '\t')" read id title; do
  r "card_$id" "{\"kind\":\"card\",\"title\":\"$title\",\"sub\":\"عالم الـ AI كله\",\"duration\":5}"
done
rm -rf out/tmp/t; echo ALL_LAYERS_DONE
