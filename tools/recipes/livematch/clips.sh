# Match clips for the reel: crop the score bug + watermark away, mirror (flip), 960 wide, no sound (Aly: avoid claims).
D=/d/Temp/livematch
O="E:/root/output/_claude/Aly Shorosh - Content Creator/automations/video-maker/motion-library/public/projects/livematch/clips"
mkdir -p "$O"
R=$D/real_qK32EAZLRDs.mp4; P=$D/real_zm9kftTvCOQ.mp4; S=$D/playmobil_stream.mp4
cut(){ ffmpeg -v error -ss $2 -t $3 -i "$1" -an -vf "crop=iw*0.84:ih*0.84:iw*0.08:ih*0.12,hflip,scale=960:-2,fps=30" -c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p "$O/$4.mp4" -y; echo $4; }
cut $R 28.5 6.4 goalR;   cut $P 51.5 6.4 goalP
cut $R 21 4.2 chanceR;   cut $P 44 4.2 chanceP
cut $P 0.3 3.4 p_moon;   cut $P 3 3.2 p_fire;  cut $P 7 3.6 p_heli
cut $P 12 3.5 p_lineup;  cut $P 28 5 p_penalty; cut $P 57.6 3.6 p_celeb
cut $P 74 7 p_ref;       cut $P 96 7 p_fans
cut $S 296 8 s_cam;      cut $S 2396 8 s_stats; cut $S 5996 8 s_stats2
# hook insert (MBC3, original Arabic sound kept, < 3 s) — placeholder = MBC3 promo until Aly's TikTok clips arrive
ffmpeg -v error -ss 1.0 -t 2.8 -i $D/../../../"E:/root/output/_claude/Aly Shorosh - Content Creator/automations/video-maker/projects/2026-11-01 reel-h livematchligo/assets/dl/mbc3_yt.mp4" -y /dev/null 2>/dev/null
ffmpeg -v error -ss 1.0 -t 2.8 -i "E:/root/output/_claude/Aly Shorosh - Content Creator/automations/video-maker/projects/2026-11-01 reel-h livematchligo/assets/dl/mbc3_yt.mp4" -vf "scale=1920:-2,fps=30" -c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p -c:a aac -b:a 192k "$O/hook_mbc3.mp4" -y; echo hook
