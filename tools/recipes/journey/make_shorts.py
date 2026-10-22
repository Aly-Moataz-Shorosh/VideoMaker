"""Journey series shorts (2026-10-22): faceless, his original voice (gain only), scenes in the look of each section.
Run: python work/scripts/make_shorts.py 8 33 44
 -> motion-library/public/projects/<code>/short_N.json, voice_N.wav, qr_playlist.png, thumbs (playlist = video 01's 1280 thumb)."""
import json, shutil, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding='utf-8')
import jy_audio as A
from shorts_data import SHORTS, PLAYLIST, PL_NAME
from oz_data import OZ
SHORTS.update(OZ)  # Oz chapters 1, 3, 4, 5 (shorts 32, 34-40)
from prog_data import PROG
SHORTS.update(PROG)  # programs (shorts 41-43, 45-48)
from intro_data import INTRO
SHORTS.update(INTRO)  # short 1 = the project intro

W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
CODE = P.name
PJ = f'projects/{CODE}/'
PUB = ROOT / 'motion-library' / 'public' / 'projects' / CODE
FPS = 30
TAIL = 4.5  # end card after his last word


def words_of(ep):
    out = []
    for s in A.transcript(ep)['sentences']:
        for i, w in enumerate(s['words']):
            out.append({**w, 'sid': s['id'], 'i': i})
    return out


def build(n):
    S = SHORTS[n]; ep = S['ep']
    print(f'== short {n} ({S["slug"]}) from video {ep}')
    WORDS = words_of(ep)
    segs, kept = [], []
    for p in S['pieces']:
        i = min(range(len(WORDS)), key=lambda k: abs(WORDS[k]['start'] - p[0]))
        j = min(range(len(WORDS)), key=lambda k: abs(WORDS[k]['start'] - p[1]))
        a, b, rep = A.fit(ep, WORDS[i]['start'], WORDS[j]['end'], WORDS[i - 1]['end'] if i else None, WORDS[j + 1]['start'] if j + 1 < len(WORDS) else None)
        if len(p) > 2 and p[2]: a = p[2]; rep += f' START FORCED {a}'
        if len(p) > 3 and p[3]: b = p[3]; rep += f' END FORCED {b}'
        print('   ', WORDS[i]['w'], '…', WORDS[j]['w'], rep)
        segs.append({'src': a, 'len': b - a}); kept.append(WORDS[i:j + 1])
    tl = 0
    for s in segs:  # whole frames on the timeline
        s['src'] = round(s['src'] * FPS) / FPS; k = max(1, round(s['len'] * FPS)); s['tl'] = tl / FPS; s['len'] = k / FPS; tl += k
    main = tl / FPS
    dur = round(main + TAIL, 3)

    def to_tl(t, lo=0.0):
        best = None
        for s in segs:
            if s['tl'] + s['len'] < lo - 0.01:
                continue
            if s['src'] - 0.02 <= t <= s['src'] + s['len'] + 0.02:
                return max(lo, s['tl'] + min(max(t - s['src'], 0), s['len']))
            for e, v in ((abs(t - s['src']), s['tl']), (abs(t - s['src'] - s['len']), s['tl'] + s['len'])):
                if best is None or e < best[0]:
                    best = (e, max(lo, v))
        if best and best[0] <= 6.0:
            return best[1]
        raise ValueError(f'{t} outside the pieces of short {n}')

    # ---------- several pieces -> one camera file of exactly those frames (picture stays in sync with the voice) ----------
    CAM = None
    if S.get('cam') or (len(segs) > 1 and (S.get('face') or any(sc['t'] == 'jy_clip' or 'clip' in sc for sc in S['scenes']))):
        CAM = f'cam_{n}.mp4'; kk = len(segs)
        fc = f'[0:v]fps={FPS},split={kk}' + ''.join(f'[i{j}]' for j in range(kk)) + ';'
        fc += ''.join(f'[i{j}]trim=start_frame={round(sg["src"] * FPS)}:end_frame={round(sg["src"] * FPS) + round(sg["len"] * FPS)},setpts=PTS-STARTPTS[v{j}];' for j, sg in enumerate(segs))
        fc += ''.join(f'[v{j}]' for j in range(kk)) + f'concat=n={kk}:v=1:a=0,settb=1/{FPS},setpts=N[v]'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(A.src(ep)), '-filter_complex', fc, '-map', '[v]', '-an', '-r', str(FPS),
                        '-c:v', 'libx264', '-crf', '18', '-preset', 'fast', '-g', '15', '-pix_fmt', 'yuv420p', str(PUB / CAM)], check=True)
        nb = int(subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0',
                                 str(PUB / CAM)], capture_output=True, text=True).stdout.strip())
        print(f'  {CAM}: {nb} frames (pieces {sum(round(sg["len"] * FPS) for sg in segs)})')

    # ---------- scenes (chained: each lasts until the next one) ----------
    starts, lo = [], 0.0
    for k, sc in enumerate(S['scenes']):
        a = 0.0 if k == 0 else to_tl(sc['at'], lo); lo = a; starts.append(a)
    scenes = []
    for k, sc in enumerate(S['scenes']):
        a = starts[k]; b = starts[k + 1] if k + 1 < len(starts) else main
        props = {kk: v for kk, v in sc.items() if kk not in ('t', 'at', 'b')}
        if sc['t'] == 'jy_clip' or 'clip' in sc:  # his own video plays in sync: source second at the scene start
            if CAM:  # several pieces: his frames of exactly the kept pieces (cam_N.mp4), so time = timeline time
                props['from'] = round(a, 3)
                if 'clip' in sc: props['clip'] = PJ + CAM
                if sc['t'] == 'jy_clip': props['src'] = CAM
            else:
                props['from'] = round(sc['at'] if k else segs[0]['src'], 3)
                if 'clip' in sc: props['clip'] = PJ + sc['clip']
                if sc['t'] == 'jy_clip': props['src'] = sc['src']
        if 'b' in sc:
            props['b'] = {kk: max(0, round((to_tl(v, a) - a) * FPS)) for kk, v in sc['b'].items()}
        if 'chips' in sc:  # light words under his clip, popping on his words (Aly v3 review)
            props['chips'] = [{**c, 't': max(0, round((to_tl(c['t'], a) - a) * FPS))} for c in sc['chips']]
        scenes.append({'t': sc['t'], 'at': round(a, 3), 'dur': round(b - a, 3), 'layer': 'front', 'props': props})
    # real example pictures (Aly review 2026-10-22): one overlay over the whole short; t / until = source seconds
    if S.get('real'):
        items = []
        for it in S['real']:
            d = {k: v for k, v in it.items() if k not in ('t', 'until')}
            d['at'] = round(to_tl(it['t']) * FPS)
            if 'until' in it:
                d['out'] = round(to_tl(it['until']) * FPS)
            items.append(d)
        scenes.append({'t': 'jy_real', 'at': 0, 'dur': round(main, 3), 'layer': 'front', 'props': {'sec': S['sec'], 'items': items}})
    scenes.append({'t': 'jy_end', 'at': round(main - 0.3, 3), 'dur': round(TAIL + 0.3, 3), 'layer': 'front',
                   'props': {'sec': S['sec'], 'plThumb': PJ + 'thumb_playlist.jpg', 'plName': PL_NAME, 'qr': PJ + 'qr_playlist.png',
                             'vidThumb': PJ + f'thumb_{ep}.jpg', 'vidTitle': S['vid_title']}})

    # ---------- captions: his words (WFIX = word fixes, '--' hides an unsure word) ----------
    fx = S.get('WFIX', {})
    words = []
    for s, ws in zip(segs, kept):
        a, b = s['src'], s['src'] + s['len']
        for w in ws:
            x = fx.get(w['w'].strip(), w['w'].strip())
            if x == '--' or not x:
                continue
            words.append({'w': x, 'start': round(s['tl'] + max(0, w['start'] - a), 3), 'end': round(s['tl'] + min(b - a, max(0.05, w['end'] - a)), 3)})

    # ---------- sound effects: whoosh per scene, pop per beat ----------
    sfx = []
    for i, s in enumerate(scenes):
        if s['t'] == 'jy_real':
            for it in s['props']['items']:
                sfx.append({'file': 'sfx/pop_2.wav', 'at': round(it['at'] / FPS, 3), 'vol': 0.3})
            continue
        if s['t'] == 'jy_end':
            sfx.append({'file': 'sfx/magic.wav', 'at': s['at'] + 0.2, 'vol': 0.4}); continue
        if s['at'] > 0.3:
            sfx.append({'file': f'sfx/whoosh_{i % 3 + 1}.wav', 'at': round(max(0, s['at'] - 0.1), 3), 'vol': 0.32})
        for j, (kk, fr) in enumerate(sorted(s['props'].get('b', {}).items(), key=lambda x: x[1])):
            if fr / FPS < s['dur'] - 0.2:
                snd = 'buzz_wrong' if kk == 'bad' else 'pop_%d' % (j % 3 + 1)
                sfx.append({'file': f'sfx/{snd}.wav', 'at': round(s['at'] + fr / FPS, 3), 'vol': 0.28})
    sfx += [{'file': 'sfx/pop_1.wav', 'at': 1.0, 'vol': 0.3}]  # station lights up in the series bar

    PUB.mkdir(parents=True, exist_ok=True)
    face_track = []  # his face moves (chapter 1 room): circle follows it; track times (source) -> timeline
    if S.get('face_track'):
        for o in json.load(open(W / S['face_track'])):
            if any(sg['src'] <= o['t'] <= sg['src'] + sg['len'] for sg in segs):
                face_track.append({**o, 't': round(to_tl(o['t']), 2)})
    log = A.voice(ep, segs, TAIL, PUB / f'voice_{n}.wav')
    print('  voice gains:', log)
    shutil.copy(next((P / 'input').glob(f'{ep}_*.jpg')), PUB / f'thumb_{ep}.jpg')
    props = {'fps': FPS, 'duration': dur, 'voice': PJ + f'voice_{n}.wav', 'segs': [{'src': 0, 'tl': 0, 'len': dur}], 'words': words, 'aly': [],
             'scenes': scenes, 'sfx': sfx, 'look': 'journey', 'capBottom': 0.115, 'sfxGain': 1.0, 'series': {'sec': S['sec'], 'label': S['label']},
             'face': {'file': PJ + (CAM or S['face']), 'from': 0 if CAM else segs[0]['src'], 'track': face_track, 'center': S.get('face_center', [960, 740]), 'r': S.get('face_r', 230), 'until': round(main, 3), 'keys': [dict(t=round(s['at'], 3), **dict(zip(('x', 'y', 'd', 'hide'), S.get('face_pos', {}).get(s['t'], (900, 1390, 220, 0))))) for s in scenes if s['t'] not in ('jy_real', 'jy_end')]} if S.get('face') else None}
    json.dump(props, open(PUB / f'short_{n}.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(f'  short {n}: {main:.1f}s + end {TAIL}s = {dur:.1f}s | {len(segs)} pieces, {len(scenes)} scenes, {len(words)} words')
    for s in scenes:
        print(f"     {s['t']:12s} {s['at']:6.2f} +{s['dur']:5.2f}")
    assert dur < 180, 'a short must stay under 3:00'


if __name__ == '__main__':
    import qrcode
    PUB.mkdir(parents=True, exist_ok=True)
    qrcode.make(PLAYLIST, border=2).save(PUB / 'qr_playlist.png')
    shutil.copy(next((P / 'input').glob('01_*.jpg')), PUB / 'thumb_playlist.jpg')  # the playlist cover = video 01's thumbnail (1280)
    for a in sys.argv[1:]:
        if a.isdigit():
            build(int(a))
