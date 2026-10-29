#!/bin/bash
# Resume of the 2026-10-27 night render (Aly stopped it at 14:20 to shut the PC down; run again after his "كمل").
# Already rendered (raw, not levelled yet): 01 03 04 06 10-18 in output/shorts/_raw. Blender hz_a-d, sr_a, sr_b done.
# Left: Blender sr_c (restart, 612 old frames overwritten) + sr_d -> level 01-18 -> render 19-23 26 27 29-31 -> archive old 08/09 ->
# render 02 08 09 -> txt. Old versions are never deleted (archive/before_1027). Log: work/night_1027.log
cd "$(dirname "$0")"
H="$(cd ../../../.. && pwd)"; OUT=../../output/shorts; LOG=../night_1027.log
echo "$(date +%T) resume" >> $LOG
CLEAN=1 bash "$H/tools/blender/render_sound_clips.sh" "p_sr_c sr_c 25.5" "p_sr_d sr_d 19.0" >> $LOG 2>&1
echo "$(date +%T) explainer clips done" >> $LOG
PYTHONIOENCODING=utf-8 python level_shorts.py 01_sound_half 03_film_music_comedy 04_sound_in_his_head 06_video_numbers 10_bit_depth 11_mic_types \
  12_polar_patterns 13_event_mic 14_podcast_mic 15_vlog_mic 16_multi_mic 17_pop_filter 18_four_sounds >> $LOG 2>&1
rm -rf "$H/motion-library/out/bundle_s"   # fresh bundle with every src change (BlenderClip tag out)
bash render_shorts.sh "19 19_film_music" "20 20_dialogue" "21 21_ambience" "22 22_sync" "23 23_camera_or_mic_sync" "26 26_phone_explosion" \
  "27 27_wave_to_samples" "29 29_audition_effects" "30 30_record_export" "31 31_headphones" >> $LOG 2>&1
for f in "$OUT"/08_*.mp4 "$OUT"/09_*.mp4; do b=$(basename "$f"); mv -n "$f" "$OUT/archive/before_1027/$b"; [ -f "$OUT/_raw/$b" ] && mv -n "$OUT/_raw/$b" "$OUT/archive/before_1027/_raw/$b"; done
bash render_shorts.sh "2 02_what_sound_does" "8 08_hertz" "9 09_sample_rate" >> $LOG 2>&1
PYTHONIOENCODING=utf-8 python make_txt.py 1 2 3 4 6 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 26 27 29 30 31 >> $LOG 2>&1
rm -rf "$H/motion-library/out/bundle_s"   # temp bundle (copy of public/)
mkdir -p ../../motion_public && mv "$H/motion-library/public/projects/audio" ../../motion_public/audio   # assets live in the project (2026-10-28)
echo "$(date +%T) ALL DONE" >> $LOG
