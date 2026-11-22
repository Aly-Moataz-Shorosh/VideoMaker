"""Cut the reel's camera + voice from the phone file, frame-exact (30 fps): hook | rewind (hook reversed, fast) | main.
Video and audio are built SEPARATELY (lip-sync rule). Edges picked on the waveform (work/scripts notes in plan.py).
Usage: python make_cam.py  -> motion-library/public/projects/uth/cam.mp4 + voice.wav, work/timeline.json"""
import json, subprocess
from pathlib import Path
from plan import HOOK, MAIN, REW_F, FPS

PRJ = Path(__file__).resolve().parents[2]
SRC = str(PRJ / 'input' / '20261120_194608.mp4')
PUB = PRJ.parents[1] / 'motion-library' / 'public' / 'projects' / 'uth'
PUB.mkdir(parents=True, exist_ok=True)

f = lambda s: round(s * FPS)
h0, h1 = f(HOOK[0]), f(HOOK[1])
m0, m1 = f(MAIN[0]), f(MAIN[1])
step = max(1, (h1 - h0) // REW_F)
# one ffmpeg run per piece (a split=3 graph dropped 38 frames), then concat the decoded pieces -> exact frame count
TMP = PRJ / 'work' / 'tmp'
TMP.mkdir(exist_ok=True)
base = f'fps={FPS},scale=1080:1920:flags=lanczos,setsar=1,'
pieces = [(f'trim=start_frame={h0}:end_frame={h1},setpts=N/{FPS}/TB', h1 - h0),
          (f'trim=start_frame={h0}:end_frame={h1},reverse,select=not(mod(n\\,{step})),trim=end_frame={REW_F},setpts=N/{FPS}/TB', REW_F),
          (f'trim=start_frame={m0}:end_frame={m1},setpts=N/{FPS}/TB', m1 - m0)]
for i, (vf, n) in enumerate(pieces):
    out = TMP / f'v{i}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-vf', base + vf, '-an', '-c:v', 'libx264', '-crf', '14', '-preset', 'fast',
                    '-pix_fmt', 'yuv420p', '-r', str(FPS), str(out)], check=True)
    got = int(subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v', '-show_entries', 'stream=nb_read_frames',
                              '-of', 'csv=p=0', str(out)], capture_output=True, text=True).stdout.strip())
    assert got == n, f'piece {i}: {got} frames, want {n}'
ins = sum([['-i', str(TMP / f'v{i}.mp4')] for i in range(3)], [])
subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', '[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]', '-map', '[v]',
                '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(FPS), str(PUB / 'cam.mp4')], check=True)
# audio: exact piece lengths (atrim + apad to whole frames), rewind = silence (sfx in Remotion), short fades at the edges
hd, md, rd = (h1 - h0) / FPS, (m1 - m0) / FPS, REW_F / FPS
af = (f'[0:a]atrim={h0 / FPS}:{h1 / FPS},asetpts=N/SR/TB,afade=t=in:d=0.03,afade=t=out:st={hd - 0.06}:d=0.06,apad=whole_dur={hd}[a1];'
      f'anullsrc=r=48000:cl=stereo,atrim=0:{rd}[a2];'
      f'[0:a]atrim={m0 / FPS}:{m1 / FPS},asetpts=N/SR/TB,afade=t=in:d=0.03,afade=t=out:st={md - 0.5}:d=0.5,apad=whole_dur={md}[a3];'
      '[a1][a2][a3]concat=n=3:v=0:a=1,aresample=48000[a]')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-filter_complex', af, '-map', '[a]', '-ac', '2', '-ar', '48000',
                str(PUB / 'voice.wav')], check=True)
tl = {'hook': [HOOK[0], h0 / FPS, h1 / FPS], 'hookLen': hd, 'rew': rd, 'main0': m0 / FPS, 'mainLen': md,
      'duration': hd + rd + md}
(PRJ / 'work' / 'timeline.json').write_text(json.dumps(tl, indent=1))
print(tl)
