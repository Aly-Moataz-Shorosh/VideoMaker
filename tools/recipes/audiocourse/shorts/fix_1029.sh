#!/bin/bash
# 2026-10-29 night: 08/09 failed (tag out = null -> NaN, fixed in sound3d.tsx), 19 failed (Chrome start timeout); level_shorts crashed on
# the missing 19 raw, so 20-31 were rendered but not levelled. -> render 19 08 09 (+ level them), level 20-31, txt, then cleanup.
cd "$(dirname "$0")"
H="$(cd ../../../.. && pwd)"; LOG=../night_1027.log
echo "$(date +%T) fix_1029 start" >> $LOG
mv ../../motion_public/audio "$H/motion-library/public/projects/audio"
rm -rf "$H/motion-library/out/bundle_s"
bash render_shorts.sh "19 19_film_music" "8 08_hertz" "9 09_sample_rate" >> $LOG 2>&1
PYTHONIOENCODING=utf-8 python level_shorts.py 20_dialogue 21_ambience 22_sync 23_camera_or_mic_sync 26_phone_explosion 27_wave_to_samples \
  29_audition_effects 30_record_export 31_headphones >> $LOG 2>&1
PYTHONIOENCODING=utf-8 python make_txt.py 8 9 19 20 21 22 23 26 27 29 30 31 >> $LOG 2>&1
echo "$(date +%T) fix_1029 done" >> $LOG
