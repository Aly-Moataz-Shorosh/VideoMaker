#!/bin/bash
# Whole short, end to end:  bash build.sh 1 2 3
#   make_short (edges, voice track, captions, cues) -> cam.py (his 1080x1920 camera from the RAW file) ->
#   Remotion render (bundle per short: only this short's cam is in public/) -> level.py (-16 LUFS, CRF 23) -> output/v3/
S="$(cd "$(dirname "$0")" && pwd)"
ML="$S/../../../../motion-library"
P="$(cygpath -m "$(cd "$S/../.." && pwd)")"
mkdir -p "$P/output/_raw"
for x in "$@"; do
  n=$(printf %02d $x); st=$(date +%s)
  cd "$S"
  PYTHONIOENCODING=utf8 python make_short.py $x > "$S/../shorts/build_$n.log" 2>&1 || { echo "short $n make_short FAILED"; continue; }
  # the camera only depends on the timeline (pieces + zoom): reuse it when that did not change (motion-only edits)
  # (compare with the timeline the camera was BUILT from, saved next to it — short 28 once reused an old camera: he froze at the end)
  if [ -f "$P/work/cam/cam_$n.mp4" ] && cmp -s "$S/../shorts/tl_$n.json" "$P/work/cam/tl_$n.json" && [[ " $FORCE_CAM " != *" $x "* ]]; then
    echo "short $n: camera reused" >> "$S/../shorts/build_$n.log"
  else
    PYTHONIOENCODING=utf8 python cam.py $x >> "$S/../shorts/build_$n.log" 2>&1 || { echo "short $n cam FAILED"; continue; }
    cp "$S/../shorts/tl_$n.json" "$P/work/cam/tl_$n.json"
  fi
  # camera length must equal the short (tail end) — else he freezes / drifts
  python -c "import json,subprocess,sys;t=json.load(open(sys.argv[1]))['segs'][-1];L=t['st']+t['d'];c=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',sys.argv[2]]));sys.exit(0 if abs(c-L)<0.15 else print(f'short $n CAMERA LENGTH {c:.2f} != {L:.2f}') or 1)" "$S/../shorts/tl_$n.json" "$P/work/cam/cam_$n.mp4" || continue
  python qc_cam.py $x | tee -a "$S/../shorts/build_$n.log"     # camera keeps him in frame? (logged; Aly checks the list)
  cd "$ML"
  rm -f public/projects/newstage19/cam_*.mp4; cp "$P/work/cam/cam_$n.mp4" public/projects/newstage19/
  rm -rf out/bundle; npx remotion bundle --out-dir out/bundle > /dev/null 2>&1
  T="$PWD/out/tmp_render"; mkdir -p "$T"; export TEMP="$T" TMP="$T"
  npx remotion render out/bundle stage-short "$P/output/_raw/short_$n.mp4" --props="$P/work/shorts/props_$n.json" --concurrency=10 --crf=16 >> "$S/../shorts/build_$n.log" 2>&1 \
    || { echo "short $n render FAILED"; rm -rf "$T"; continue; }
  rm -rf "$T"; rm -f public/projects/newstage19/cam_$n.mp4
  cd "$S"; PYTHONIOENCODING=utf8 python level.py $x
  echo "short $n done in $(( $(date +%s) - st ))s"
done
