"""Download a YouTube video into a project's input folder (free, yt-dlp). For Aly's own videos (shorts mode).

Usage: python tools/fetch.py <youtube_url> projects/<folder>
"""
import subprocess, sys
from pathlib import Path

url, proj = sys.argv[1], Path(sys.argv[2])
(proj / 'input').mkdir(parents=True, exist_ok=True)
subprocess.run([sys.executable, '-m', 'yt_dlp', '--js-runtimes', 'node', '-N', '4', '-f', 'bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080]',
                '--merge-output-format', 'mp4', '-o', str(proj / 'input' / '%(id)s.%(ext)s'), url], check=True)
