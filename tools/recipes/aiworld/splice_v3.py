"""Put re-rendered frame ranges back into the full v3 render (only the changed scenes were rendered again).
parts: work/_fix_teaser.mp4 = frames 7042-7116, work/_fix_song.mp4 = frames 26133-30874 of work/_full_v3_video.mp4.
Out: output/rough_cut_v3.mp4 (+ v3 mix audio). Usage (project folder): python -X utf8 work/scripts/splice_v3.py"""
import subprocess
FULL, N = "work/_full_v3_video.mp4", 31632
FIX = [(7042, 7116, "work/_fix_teaser.mp4"), (26133, 30874, "work/_fix_song.mp4")]
ins, fl, k, cur = ["-i", FULL], [], 0, 0
for i, (a, b, f) in enumerate(FIX):
    ins += ["-i", f]
    fl.append(f"[0:v]trim=start_frame={cur}:end_frame={a},setpts=PTS-STARTPTS[v{k}]"); k += 1
    fl.append(f"[{i + 1}:v]setpts=PTS-STARTPTS[v{k}]"); k += 1
    cur = b + 1
fl.append(f"[0:v]trim=start_frame={cur}:end_frame={N},setpts=PTS-STARTPTS[v{k}]"); k += 1
fl.append("".join(f"[v{i}]" for i in range(k)) + f"concat=n={k}:v=1:a=0[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-i", "output/audio_stems_v3/mix_rough_v3.wav", "-filter_complex", ";".join(fl),
                "-map", "[o]", "-map", f"{len(FIX) + 1}:a", "-c:v", "libx264", "-crf", "20", "-preset", "fast", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-shortest", "output/rough_cut_v3.mp4"], check=True)
print("ok")
