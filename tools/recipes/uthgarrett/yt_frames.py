"""Grab full-quality stills from a YouTube stream at given seconds (no download of the video).
Usage: python yt_frames.py <id> <prefix> <outdir> t1 t2 ...   -> <outdir>/<prefix>_<t>.jpg"""
import subprocess, sys
from pathlib import Path
vid, pre, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
url = subprocess.run([sys.executable, '-m', 'yt_dlp', '--js-runtimes', 'node', '-f', 'bv[height<=1080][ext=mp4]/bv[height<=1080]', '-g',
                      f'https://www.youtube.com/watch?v={vid}'], capture_output=True, text=True).stdout.split('\n')[0]
for t in sys.argv[4:]:
    f = out / f'{pre}_{t}.jpg'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', t, '-i', url, '-frames:v', '1', '-q:v', '2', str(f)])
    print(f.name, f.exists())
