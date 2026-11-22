"""Dense contact sheet of a YouTube video from its stream (no download): one frame every STEP s, time on each.
Usage: python yt_sheet.py <id> <step> <out.jpg>"""
import subprocess, sys
vid, step, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
url = subprocess.run([sys.executable, '-m', 'yt_dlp', '--js-runtimes', 'node', '-f', 'bv[height<=480]/b[height<=480]', '-g',
                      f'https://www.youtube.com/watch?v={vid}'], capture_output=True, text=True).stdout.split('\n')[0]
font = r"fontfile='C\:/Windows/Fonts/arial.ttf'"
vf = (f"fps=1/{step},scale=256:-2,drawtext={font}:text='%{{pts\\:hms}}':x=4:y=4:fontsize=16:fontcolor=yellow:box=1:boxcolor=black,"
      "tile=8x12:padding=2")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', url, '-vf', vf, '-q:v', '4', out.replace('.jpg', '_%d.jpg')], check=True)
