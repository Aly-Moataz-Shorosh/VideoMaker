"""His full-screen 9:16 camera for one short, at the best quality the RAW file gives (Aly 2026-10-19: "اعمل الجودة احسن ما يمكن").
RAW = input/20260908_103633.mp4 (1280x720 HEVC 10-bit HLG, ~8.6 Mb/s; his edit = raw + 88.01 s, re-encoded at 1.4 Mb/s).
Per frame: HLG -> SDR (zscale + hable, like his edit's colours), crop window that follows him (track_raw.json) with the short's
zoom keys, ONE Lanczos resample straight to 1080x1920 (warpAffine, sub-pixel), light unsharp, faces of OTHER people blurred
(Aly: "اي حد غيري المفروض ميظهرش"), x264 CRF 14.  Timeline = work/shorts/tl_NN.json from make_short.py.
Usage: python cam.py 1 [2 ...]   -> work/cam/cam_NN.mp4"""
import bisect, json, subprocess, sys
from pathlib import Path
import cv2
import numpy as np
P = Path(__file__).resolve().parents[2]
RAW = P / 'input' / '20260908_103633.mp4'
OFF = -88.01               # raw = main + OFF (sync.py: constant over the whole lecture)
W, H, SW, SH = 1080, 1920, 1280, 720
TONE = 'zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=bgr24'
# only real "him" boxes: feet on the stage floor (bottom >= 380) and a full body (>= 200 px). The roll-up banner on the right
# (x ~1125, bottom ~320) was detected as a person and pulled the frame off him (short 2 v3 hook).
trk = {float(k): v for k, v in json.load(open(P / 'work' / 'track_raw.json')).items() if v[2] >= 380 and v[2] - v[1] >= 200}
TK = sorted(trk)
FACES = [cv2.CascadeClassifier(cv2.data.haarcascades + n) for n in ('haarcascade_frontalface_default.xml', 'haarcascade_profileface.xml')]


def cx_raw(t):
    """his x in the raw at raw time t: nearest detection within 1.5 s (None if none)"""
    i = bisect.bisect_left(TK, t)
    near = [TK[j] for j in (i - 1, i) if 0 <= j < len(TK) and abs(TK[j] - t) < 1.5]
    return trk[min(near, key=lambda x: abs(x - t))][0] if near else None


def interp(keys, t):
    if t <= keys[0][0]: return keys[0][1]
    for i in range(1, len(keys)):
        if t <= keys[i][0]:
            (t0, v0), (t1, v1) = keys[i - 1], keys[i]
            return v0 + (v1 - v0) * (t - t0) / max(1e-6, t1 - t0)
    return keys[-1][1]


HOG = cv2.HOGDescriptor(); HOG.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def people(img):
    """every standing person in the whole raw frame (1280x720 coords) -> [(x, y, w, h, on_stage)]"""
    rects, w = HOG.detectMultiScale(img, winStride=(8, 8), padding=(8, 8), scale=1.05)
    out = []
    for (x, y, ww, hh), sc in zip(rects, w):
        if hh >= 160 and sc > 0.3:
            out.append((int(x), int(y), int(ww), int(hh), 360 <= y + hh <= 480))
    return out


BLUR = False  # automatic blur of other people (off: Aly does it himself)
PROJ = (545, 0, 1065, 300)  # projector screen in the raw frame: faces on slides are not people

import onnxruntime as ort
_RVM = ort.InferenceSession(str(P.parents[1] / 'tools' / 'models' / 'rvm_mobilenetv3_fp32.onnx'), providers=['CPUExecutionProvider'])
_REC = {'r': [np.zeros([1, 1, 1, 1], np.float32)] * 4}


def matte_reset():
    _REC['r'] = [np.zeros([1, 1, 1, 1], np.float32)] * 4


def matte(img):
    """human matte (0..1) of a raw BGR frame, at raw size; recurrent over consecutive frames"""
    small = cv2.resize(img, (640, 360), interpolation=cv2.INTER_AREA)
    x = (small[..., ::-1].astype(np.float32) / 255).transpose(2, 0, 1)[None].copy()
    r = _REC['r']
    fgr, pha, *r = _RVM.run(None, {'src': x, 'r1i': r[0], 'r2i': r[1], 'r3i': r[2], 'r4i': r[3], 'downsample_ratio': np.array([0.6], np.float32)})
    _REC['r'] = r
    return cv2.resize(pha[0, 0], (SW, SH), interpolation=cv2.INTER_LINEAR)


def win(z):  # same as stage/kit.tsx win(): head (~y 170) lands at y 430 under the headline
    ch = 705 / z; cw = ch * 9 / 16
    top = max(0.0, min(720 - ch, 170 - 430 * ch / H))
    return ch, cw, top


def frames(a, d, fps=None):
    vf = TONE if fps is None else f'fps={fps:.5f},' + TONE
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{a:.3f}', '-t', f'{d:.3f}', '-i', str(RAW), '-vf', vf, '-r', '30' if fps is None else f'{fps:.5f}',
                          '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    while True:
        b = p.stdout.read(SW * SH * 3)
        if len(b) < SW * SH * 3: break
        yield np.frombuffer(b, np.uint8).reshape(SH, SW, 3)
    p.wait()


def build(n):
    tl = json.load(open(P / 'work' / 'shorts' / f'tl_{n:02d}.json', encoding='utf8'))
    zoom = tl['zoom']
    # his x along the short (smoothed ~2 s), from the raw tracker
    # v4 (Aly review 2026-10-19: the crop followed a girl in short 25; people on stage / front rows were not blurred):
    # per piece, detect EVERY person 10x/s, keep the one nearest his previous x = him, the others' heads get blurred.
    xs, others, mes = [], [], []
    for s in tl['segs']:
        if s['kind'] != 'seg': continue
        a = s['a'] + OFF
        init = [v for v in (cx_raw(a + k * 0.5) for k in range(int((s['b'] - s['a']) / 0.5) + 1)) if v is not None]
        prev = sorted(init)[len(init) // 2] if init else 640
        raw = []
        matte_reset()
        miss = 0
        for i, img in enumerate(frames(a, s['b'] - s['a'], fps=10)):
            # v5 (Aly 2026-10-19: the camera stopped following him in 7 / 12 / 13 — the person detector lost him for seconds):
            # him = the people-matte blob standing on the stage floor (feet 360-495 px, tall), nearest his last x.
            al = matte(img) > 0.5
            nl, lab, st, cen = cv2.connectedComponentsWithStats(al.astype(np.uint8))
            cands = [cen[q][0] for q in range(1, nl) if st[q][cv2.CC_STAT_HEIGHT] >= 150 and 360 <= st[q][cv2.CC_STAT_TOP] + st[q][cv2.CC_STAT_HEIGHT] <= 540]
            tall = [cen[q][0] for q in sorted(range(1, nl), key=lambda q: -st[q][cv2.CC_STAT_HEIGHT])
                    if st[q][cv2.CC_STAT_HEIGHT] >= 150 and 360 <= st[q][cv2.CC_STAT_TOP] + st[q][cv2.CC_STAT_HEIGHT] <= 540]
            near = min(cands, key=lambda v: abs(v - prev), default=None)
            if i == 0 and tall:                       # start of a piece: begin on the person really standing on the stage
                prev, miss = tall[0], 0
            elif near is not None and abs(near - prev) < 300:
                prev, miss = near, 0
            else:
                miss = miss + 1 if i else 0
                if miss >= 10 and tall:               # lost him > 1 s (he walked far): jump to the person on the stage
                    prev, miss = tall[0], 0
            boxes = people(img) if BLUR else []
            stage = [bx for bx in boxes if bx[4]]
            me = min(stage, key=lambda bx: abs(bx[0] + bx[2] / 2 - prev), default=None)
            raw.append(prev)
            t = s['st'] + i / 10
            mebox = me[:4] if me else (prev - 60, 120, 120, 300)
            mes.append((t, mebox))
            # others = boxes that are not him (a second hit on his own body is dropped)
            others += [(t, bx[:4]) for bx in boxes if abs(bx[0] + bx[2] / 2 - (mebox[0] + mebox[2] / 2)) > 0.55 * mebox[2]]
        med = [sorted(raw[max(0, i - 5):i + 6])[len(raw[max(0, i - 5):i + 6]) // 2] for i in range(len(raw))]  # median kills single wrong hits
        sm = [sum(med[max(0, i - 8):i + 9]) / len(med[max(0, i - 8):i + 9]) for i in range(len(med))]   # ~1.7 s smooth
        xs += [[s['st'] + k / 10, v] for k, v in enumerate(sm)]
    xs.sort()
    out = P / 'work' / 'cam' / f'cam_{n:02d}.mp4'
    out.parent.mkdir(exist_ok=True)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                            '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p', str(out)], stdin=subprocess.PIPE)
    face_regions, fi = [], 0

    def emit(img, t):
        nonlocal fi
        z = interp(zoom, t)
        ch, cw, top = win(z)
        cx = max(cw / 2, min(SW - cw / 2, interp(xs, t)))
        k = H / ch
        M = np.float32([[k, 0, -(cx - cw / 2) * k], [0, k, -top * k]])
        o = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
        o = cv2.addWeighted(o, 1.35, cv2.GaussianBlur(o, (0, 0), 2.2), -0.35, 0)  # light unsharp after the upscale
        # Aly 2026-10-19: blur the WHOLE BODY of everyone who isn't him, with a soft feather (like his own edit).
        # People = RVM human matte of the raw frame; him = the matte blob under his tracked box; the projector is never blurred.
        if not BLUR:  # Aly 2026-10-19: "ال blur وحش.. وقف اي blur" -> no automatic blur; he blurs by hand where needed
            fi += 1
            enc.stdin.write(o.tobytes())
            return o
        al = matte(img)
        people = al > 0.4
        # him = the people-matte inside a band around his tracked x (the track is stable); his head = top of that band
        hx = interp(xs, t)
        band = np.zeros_like(people); band[80:490, int(max(0, hx - 85)):int(min(SW, hx + 85))] = True
        # faces of anyone else (frontal/profile, Haar on the raw frame every 3rd frame): not on the projector, not his head
        if fi % 3 == 0:
            g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            fb = []
            for c in FACES:
                fb += [tuple(r) for r in c.detectMultiScale(g, 1.1, 5, minSize=(14, 14))]
                fb += [(SW - x - w, y, w, h) for (x, y, w, h) in c.detectMultiScale(cv2.flip(g, 1), 1.1, 5, minSize=(14, 14))]
            face_regions[:] = []
            for (x, y, w, h) in fb:
                fx, fy = x + w / 2, y + h / 2
                his_head = abs(fx - hx) < 60 and fy < 80 + (490 - 80) * 0.3
                proj = PROJ[0] <= fx <= PROJ[2] and PROJ[1] <= fy <= PROJ[3]
                if not his_head and not proj:
                    face_regions.append((int(max(0, x - 1.2 * w)), int(max(0, y - 0.5 * h)), int(min(SW, x + 2.2 * w)), int(min(SH, y + 7 * h))))
        fr = np.zeros_like(people)
        for (x0, y0, x1, y1) in face_regions:
            fr[y0:y1, x0:x1] = True
        him = people & band & ~fr
        oth = (people & ~band) | (fr & (people | (al > 0.15)))   # a face region blurs that person's body (matte or not)
        for (x0, y0, x1, y1) in face_regions:                     # and at least the face itself
            oth[y0:min(SH, y0 + (y1 - y0) // 4), x0:x1] = True
        oth[PROJ[1]:PROJ[3], PROJ[0]:PROJ[2]] &= fr[PROJ[1]:PROJ[3], PROJ[0]:PROJ[2]]
        if oth.any():
            m = cv2.dilate(oth.astype(np.uint8) * 255, np.ones((15, 15), np.uint8)).astype(np.float32) / 255
            m = cv2.GaussianBlur(m, (0, 0), 9)                    # feather (raw px)
            m *= 1 - cv2.GaussianBlur(him.astype(np.float32), (0, 0), 2)   # never blur him
            mo = cv2.warpAffine(m, M, (W, H), flags=cv2.INTER_LINEAR)[..., None]
            if mo.max() > 0.02:
                bl = cv2.GaussianBlur(o, (0, 0), 24)
                o = (o.astype(np.float32) * (1 - mo) + bl.astype(np.float32) * mo).astype(np.uint8)
        fi += 1
        enc.stdin.write(o.tobytes())
        return o

    last = None
    for s in tl['segs']:
        matte_reset()
        if s['kind'] == 'seg':
            nfr = round((s['b'] - s['a']) * 30)
            for i, img in enumerate(frames(s['a'] + OFF, s['b'] - s['a'] + 0.2)):
                if i >= nfr: break
                last = emit(img, s['st'] + i / 30)
            for j in range(i + 1, nfr):  # decoder came up short: hold
                enc.stdin.write(last.tobytes())
        elif s['kind'] == 'rew':  # the span played backwards in REW seconds
            span = s['b'] - s['a']; nfr = round(s['d'] * 30)
            pics = list(frames(s['a'] + OFF, span, fps=nfr / span))[::-1][:nfr]
            for i in range(nfr):
                img = pics[min(i, len(pics) - 1)]
                g = cv2.convertScaleAbs(img, alpha=1.15, beta=-10)
                last = emit(g, s['st'] + i / 30)
        else:  # tail: hold the last frame
            for i in range(round(s['d'] * 30)):
                enc.stdin.write(last.tobytes())
    enc.stdin.close(); enc.wait()
    print('cam', n, out, round(out.stat().st_size / 1e6, 1), 'MB')


if __name__ == '__main__':
    for n in map(int, sys.argv[1:]):
        build(n)
