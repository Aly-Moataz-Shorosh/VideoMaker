"""Cut Aly out of his footage (free rotoscope) with RobustVideoMatting on CPU.

Usage: python tools/matte.py <video> <start_sec> <dur_sec> <out.webm|out.mov> [--png frame_out.png] [--fps 30]
       [--model resnet50|mobilenetv3] [--ratio 0.5]
Quality (Aly: first result not good enough): default mobilenetv3 + ratio 0.4 (2.6 fps) + edge colors from the model's
de-spilled foreground (no room-color halo) + tiny alpha cleanup.
Output keeps alpha: .webm (VP9 alpha, small, for Remotion) or .mov (ProRes 4444, for Premiere).
"""
import subprocess, sys, time, json
from pathlib import Path
import numpy as np
import onnxruntime as ort

MODELS = Path(__file__).parent / 'models'


def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                          'stream=width,height,r_frame_rate', '-of', 'json', path],
                         capture_output=True, text=True, check=True).stdout
    s = json.loads(out)['streams'][0]
    num, den = s['r_frame_rate'].split('/')
    return s['width'], s['height'], float(num) / float(den)


def main():
    src, start, dur, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    png = sys.argv[sys.argv.index('--png') + 1] if '--png' in sys.argv else None
    w, h, fps = probe(src)
    arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
    vf = []
    if '--fps' in sys.argv:  # e.g. 60 fps source, 30 fps render -> half the work
        fps = float(arg('--fps', fps)); vf = ['-vf', f'fps={fps}']
    model = arg('--model', 'mobilenetv3')  # resnet50 tested: slower (1.3 fps), not cleaner on Aly's footage
    sess = ort.InferenceSession(str(MODELS / f'rvm_{model}_fp32.onnx'), providers=['CPUExecutionProvider'])
    reader = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(start), '-t', str(dur), '-i', src, *vf,
                               '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    if out.endswith('.webm'):
        enc = ['-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-b:v', '6M', '-auto-alt-ref', '0']
    else:
        enc = ['-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le']
    writer = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba',
                               '-s', f'{w}x{h}', '-r', f'{fps}', '-i', '-', *enc, out], stdin=subprocess.PIPE)
    rec = [np.zeros([1, 1, 1, 1], np.float32)] * 4
    ratio = np.array([float(arg('--ratio', 0.4))], np.float32)
    n, t0 = 0, time.time()
    while True:
        buf = reader.stdout.read(w * h * 3)
        if len(buf) < w * h * 3:
            break
        rgb = np.frombuffer(buf, np.uint8).reshape(h, w, 3)
        x = (rgb.astype(np.float32) / 255).transpose(2, 0, 1)[None]
        fgr, pha, *rec = sess.run(None, {'src': x, 'r1i': rec[0], 'r2i': rec[1], 'r3i': rec[2],
                                         'r4i': rec[3], 'downsample_ratio': ratio})
        al = pha[0, 0]
        al = np.where(al < 0.04, 0, np.where(al > 0.96, 1, al))  # kill faint haze / pinholes
        # Inside: original pixels. Edges: model's de-spilled foreground color (removes room-light halo).
        fg = (fgr[0].transpose(1, 2, 0) * 255).clip(0, 255)
        mix = np.where(al[..., None] > 0.98, rgb.astype(np.float32), fg)
        rgba = np.dstack([mix.astype(np.uint8), (al * 255).astype(np.uint8)])
        writer.stdin.write(rgba.tobytes())
        if png and n == int(len(range(0, int(dur * fps))) // 2):
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s',
                            f'{w}x{h}', '-i', '-', png], input=rgba.tobytes(), check=True)
        n += 1
    writer.stdin.close(); writer.wait(); reader.wait()
    print(f'{n} frames in {time.time() - t0:.1f}s ({n / max(time.time() - t0, 1e-6):.1f} fps) -> {out}')


if __name__ == '__main__':
    main()
