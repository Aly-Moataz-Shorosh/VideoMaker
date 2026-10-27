#!/bin/bash
# Night of 2026-10-27 (Aly "كمل"): after the Blender street clip and the 23-short batch finish -> Blender explainers of 08/09 -> shorts 02, 08, 09.
# Old 08/09 go to archive/before_1027 first (never deleted). Log: work/night_1027.log
cd "$(dirname "$0")"
H="$(cd ../../../.. && pwd)"; OUT=../../output/shorts; LOG=../night_1027.log
blender_busy() { tasklist 2>/dev/null | grep -qi '^blender.exe'; }
echo "$(date +%T) start" >> $LOG
until [ -f "$H/motion-library/public/projects/audio/b3d/p_street.webm" ] && ! blender_busy; do sleep 60; done
echo "$(date +%T) street clip ready" >> $LOG
CLEAN=1 bash "$H/tools/blender/render_sound_clips.sh" "p_hz_b hz_b 17.5" "p_hz_a hz_a 24.2" "p_hz_c hz_c 18.5" "p_hz_d hz_d 21.2" \
  "p_sr_b sr_b 24.4" "p_sr_a sr_a 38.0" "p_sr_c sr_c 25.5" "p_sr_d sr_d 19.0" >> $LOG 2>&1
echo "$(date +%T) explainer clips done" >> $LOG
until [ -f "$OUT/31_headphones.mp4" ]; do sleep 60; done   # the batch writes its levelled files in order, 31 is the last one
sleep 120
echo "$(date +%T) batch done" >> $LOG
for f in "$OUT"/08_*.mp4 "$OUT"/09_*.mp4; do b=$(basename "$f"); mv -n "$f" "$OUT/archive/before_1027/$b"; [ -f "$OUT/_raw/$b" ] && mv -n "$OUT/_raw/$b" "$OUT/archive/before_1027/_raw/$b"; done
rm -rf "$H/motion-library/out/bundle_s"   # src changed (BlenderClip tag out) -> fresh bundle
bash render_shorts.sh "2 02_what_sound_does" "8 08_hertz" "9 09_sample_rate" >> $LOG 2>&1
PYTHONIOENCODING=utf-8 python make_txt.py 2 8 9 >> $LOG 2>&1
echo "$(date +%T) ALL DONE" >> $LOG
