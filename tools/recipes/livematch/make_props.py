"""Props for the 'match-reel' composition (live Playmobil match reel, 2026-11-01).
Run from video-maker/:  python "projects/2026-11-01 reel-h livematchligo/work/scripts/make_props.py"
Writes work/props.json. Every time = his source second (no cut, no pause: Aly allowed dropping the MBC3 pause).
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
SRC = WORK.parent / 'input' / '20261101_085903.mp4'
DUR = 91.83

# ---- captions: Whisper words + fixes checked with 3 re-transcriptions (prompts TRACAB/EA/FIFA, Skeleton, MBC3) ----
FIX = {0.96: 'مبارح', 1.28: 'live', 1.78: 'MBC3', 3.3: 'لعبة', 4.04: 'ده', 5.02: 'ودورتموند', 6.3: 'خلص', 9.32: 'اللعيب', 12.94: 'ده؟',
       13.94: 'البوندسليجا', 15.18: 'الألماني', 16.5: 'ومعاها', 23.84: 'لعيب', 25.8: 'بتشوف', 25.92: 'اللعيبة', 27.5: 'بتسجلهم',
       30.3: '3D', 30.66: '', 31.3: 'Skeleton', 32.06: 'Skeleton', 32.68: '21', 33.14: '', 34.2: 'والكتاف', 35.18: 'ومفاصل', 35.6: 'الإيد',
       36.76: 'وأطراف', 37.22: 'الصوابع', 46.86: 'Semi', 47.16: 'Automated', 47.6: 'Offside', 47.74: '', 48.36: 'الداتا', 49.3: 'بتقرر',
       51.46: 'العرايس', 52.08: 'الهيكل', 52.8: 'السكيلتون', 53.56: 'بيتحط', 55.22: 'Playmobil', 55.52: '', 55.9: 'Playmobil', 56.02: '',
       57.9: 'ليها', 59.94: 'والكاركترز', 62.36: 'Unreal', 62.88: 'Engine', 63.24: 'بتاع', 63.56: 'الألعاب', 64.02: 'اللعيب', 65.38: 'اللعيب',
       69.68: 'لايف', 70.52: 'حقيقي', 72.32: 'نوعها', 72.7: 'للبوندسليجا', 74.54: 'العرض', 76.1: 'قوي', 76.34: 'خدت', 76.92: 'البث',
       78.24: 'البث', 79.06: 'الأول', 81.18: '6', 84.56: 'بتتعرض', 84.98: 'MBC3', 87.64: 'أول', 87.84: 'بأول', 89.22: 'وقولي', 89.42: '',
       90.26: 'بالطريقة'}
SECOND = [('من', 17.26), ('شركة', 17.58), ('TRACAB', 17.98), ('وعلى', 18.46), ('فكرة', 18.74), ('دي', 19.04), ('شركة', 19.3), ('EA', 19.72),
          ('اشترتها', 20.06), ('أه', 20.88), ('EA', 21.6), ('بتاعت', 21.76), ('FIFA', 22.12)]
ADD = [('فروح', 85.6, 86.1)]


def words():
    tr = json.load(open(WORK / 'transcript.json', encoding='utf-8'))
    ws = [w for s in tr['sentences'] for w in s['words']]
    out = []
    for w in ws:
        if 17.2 <= w['start'] < 22.4:
            continue
        txt = FIX.get(w['start'], w['w'])
        if txt:
            out.append({'w': txt, 'start': w['start'], 'end': w['end']})
    for i, (t, s) in enumerate(SECOND):
        e = SECOND[i + 1][1] if i + 1 < len(SECOND) else 22.42
        out.append({'w': t, 'start': s, 'end': round(min(e, s + 0.6), 2)})
    for t, s, e in ADD:
        out.append({'w': t, 'start': s, 'end': e})
    out.sort(key=lambda w: w['start'])
    hl = {'MBC3', 'AI', 'لعبة', '21', 'Skeleton', 'TRACAB', 'EA', 'FIFA', 'Playmobil', 'Unreal', 'Engine', 'لايف', 'حقيقي', 'ازاي'}
    for w in out:
        if w['w'] in hl:
            w['hl'] = True
    return out


def amp():
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(SRC), '-ac', '1', '-ar', '30000', '-f', 's16le', '-'], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    n = len(a) // 1000
    db = 20 * np.log10(np.sqrt((a[: n * 1000].reshape(n, 1000) ** 2).mean(1)) + 1e-9)
    v = np.clip((db + 36) / 24, 0, 1)
    v = np.convolve(v, [0.25, 0.5, 0.25], 'same')
    return [round(float(x), 2) for x in v]


C = lambda t, d, k, **p: {'t': t, 'd': d, 'k': k, 'p': p}
CUES = [
    # hook: live on MBC3, not AI, not a game
    C(0.0, 1.7, 'behind', text='LIVE', color='#FF3D3D', size=300),
    C(1.72, 1.95, 'behind', text='MBC3', color='#8BC34A', size=280),
    C(0.05, 3.62, 'clip', file='p_celeb', live=True,
      w=900, h=500, grid=[{'file': 'goalP', 'from': 3.0}, {'file': 'p_penalty', 'from': 0.8}, {'file': 'p_heli', 'from': 0.0},
            {'file': 'p_moon', 'from': 0.0}, {'file': 'p_fire', 'from': 0.0}, {'file': 'p_fans', 'from': 0.4}], logos=[{'file': 'mbc3.png', 'at': 1.75, 'x': 450, 'y': 250, 'h': 130}],
      stamps=[{'text': '✗ مش AI', 'at': 2.55, 'x': 680, 'y': 130, 'size': 56}, {'text': '✗ مش لعبة', 'at': 3.2, 'x': 230, 'y': 380, 'size': 56, 'r': 7}]),
    # the real Bayern-Dortmund, ended 2-2
    C(3.66, 3.5, 'vs', b={'a': 0.92, 'b': 1.36, 'real': 1.9, 'score': 2.62}),
    C(6.3, 0.9, 'behind', text='2-2', color='#FFD43B', size=320),
    # every doll moves like the real player: real (top) vs Playmobil (bottom), same goal
    C(7.16, 4.55, 'split', top='goalR', bot='goalP', **{'from': 2.0}, words=[[3.62, 'لحظة بلحظة', 'لحظة بلحظة']]),
    C(11.8, 1.32, 'behind', text='ازاي؟', color='#FFD43B', size=300),
    C(13.1, 2.5, 'map', b={'logo': 0.84}),
    C(15.62, 1.66, 'clip', file='s_cam', **{'from': 3.0}, label='كاميرات تتبع', stamps=[{'text': '+ AI', 'at': 1.4, 'x': 160, 'y': 120, 'size': 56, 'color': '#2F6BFF'}]),
    C(17.9, 1.75, 'behind', text='TRACAB', color='#FFFFFF', size=190),
    C(17.3, 5.15, 'chain', b={'ea': 2.42, 'fc': 4.3}),
    C(22.48, 2.95, 'track'),
    C(25.44, 4.05, 'cams', b={'photo': 2.5}),
    C(29.5, 12.1, 'skel', b={'name': 1.8, 'count': 2.56},
      groups=[['head', 4.32], ['sh', 4.7], ['mid', 5.2], ['arm', 5.68], ['leg', 6.36], ['heel', 6.8], ['tip', 7.26]],
      tags=[{'text': 'الكمبيوتر عارف كل حركة', 'at': 8.3, 'x': 175, 'y': 395, 'size': 30}]),
    C(32.6, 2.3, 'behind', text='21', color='#FFD43B', size=420),
    C(41.65, 4.1, 'clip', file='p_ref', **{'from': 2.8}, stamps=[{'text': 'مش للعرض', 'at': 0.95, 'x': 560, 'y': 120, 'size': 56}]),
    C(45.8, 3.45, 'offside', b={'off': 0.35, 'name': 1.05}),
    C(46.1, 1.85, 'behind', text='تسلل', color='#FF3D3D', size=300),
    C(49.3, 2.7, 'flow', b={'move': 1.8}),
    C(52.05, 4.2, 'wrap', b={'skin': 1.5, 'logo': 3.15}),
    C(55.15, 1.15, 'behind', text='PLAYMOBIL', color='#FFFFFF', size=160),
    C(56.3, 3.4, 'brands', b={'lego': 1.1, 'plastic': 1.9}),
    C(59.75, 4.1, 'render', file='p_heli', rate=0.88, b={'logo': 2.6}),
    C(62.3, 1.5, 'behind', text='UNREAL', color='#FFFFFF', size=200),
    # runs / shoots: real (top) vs Playmobil (bottom)
    C(63.92, 3.08, 'split', top='chanceR', bot='chanceP', **{'from': 0.4}, words=[[0.42, 'يجري', 'يجري'], [1.78, 'يشوت', 'يشوت']],
      labels=['اللعيب', 'الكاركتر']),
    # Aly as a Playmobil reporter
    C(67.0, 6.6, 'reporter', bg='p_lineup', b={'real': 14},
      cards=[{'k': 'mocap', 'at': 0.08, 'd': 2.5}, {'k': 'live', 'at': 2.62, 'd': 1.7}, {'k': 'first', 'at': 4.38, 'd': 2.2}]),
    C(73.62, 5.85, 'channels', b={'rights': 2.7, 'beta': 4.6}),
    C(76.3, 1.6, 'behind', text='حقوق البث', color='#FFD43B', size=190),
    C(79.5, 7.7, 'old', b={'year': 1.65, 'qr': 1.0, 'note': 2.3}),
    C(80.95, 2.1, 'behind', text='6 سنين', color='#FFD43B', size=230),
    C(83.6, 1.0, 'behind', text='خيال', color='#FFFFFF', size=280),
    C(87.22, 1.95, 'follow'),
    C(89.18, 2.65, 'poll', b={'real': 1.42}),
    C(89.2, 2.6, 'behind', text='؟', color='#FFD43B', size=420),
]
ZOOM = [[0, 1.16], [0.45, 1.0], [2.5, 1.0], [2.62, 1.07], [3.6, 1.0], [11.7, 1.0], [11.86, 1.14], [13.0, 1.14], [13.2, 1.0], [32.5, 1.0], [32.7, 1.06],
        [34.8, 1.0], [41.6, 1.0], [45.6, 1.05], [46.1, 1.0], [52.0, 1.0], [55.9, 1.05], [56.2, 1.0], [73.6, 1.0], [76.3, 1.06], [79.4, 1.0],
        [83.55, 1.0], [83.7, 1.1], [84.6, 1.0], [89.1, 1.0], [89.25, 1.1], [91.83, 1.04]]


def sfx():
    out = []
    wh = ['whoosh_1', 'whoosh_2', 'whoosh_3']
    for i, c in enumerate(CUES):
        if c['k'] == 'behind':
            out.append({'t': c['t'], 'file': 'sfx/swish.wav', 'vol': 0.22})
        elif c['k'] in ('split', 'reporter'):
            out.append({'t': max(0, c['t'] - 0.15), 'file': 'sfx/swoop_up.wav', 'vol': 0.3})
        else:
            out.append({'t': c['t'], 'file': f'sfx/{wh[i % 3]}.wav', 'vol': 0.22})
        for s in c['p'].get('stamps', []):
            out.append({'t': c['t'] + s['at'], 'file': 'sfx/stamp.wav', 'vol': 0.3})
        for l in c['p'].get('logos', []):
            out.append({'t': c['t'] + l['at'], 'file': 'sfx/pop_2.wav', 'vol': 0.3})
        b = c['p'].get('b', {})
        for k, f in (('a', 'pop_1'), ('b', 'pop_3'), ('score', 'impact'), ('ea', 'pop_2'), ('fc', 'pop_1'), ('photo', 'shutter'), ('off', 'stamp'),
                     ('move', 'swish'), ('skin', 'magic'), ('lego', 'pop_3'), ('plastic', 'stamp'), ('logo', 'pop_2'), ('beta', 'stamp'), ('real', 'pop_1')):
            if k in b and c['k'] != 'reporter':
                out.append({'t': round(c['t'] + b[k], 2), 'file': f'sfx/{f}.wav', 'vol': 0.28})
        if c['k'] == 'skel':
            out.append({'t': c['t'] + b['count'] + 0.75, 'file': 'sfx/ding.wav', 'vol': 0.3})
        if c['k'] == 'reporter':
            out += [{'t': c['t'] + 2.62, 'file': 'sfx/stamp.wav', 'vol': 0.3}, {'t': c['t'] + 4.38, 'file': 'sfx/impact.wav', 'vol': 0.3}]
        if c['k'] == 'follow':
            out.append({'t': c['t'] + 0.66, 'file': 'sfx/click.wav', 'vol': 0.4})
    return sorted(out, key=lambda s: s['t'])


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    props = {'duration': DUR, 'src': 'projects/livematch/source.mp4', 'roto': 'projects/livematch/roto.webm', 'cues': CUES,
             'words': words(), 'zoom': ZOOM, 'sfx': sfx(), 'amp': amp(), 'capsHide': []}
    (WORK / 'props.json').write_text(json.dumps(props, ensure_ascii=False), encoding='utf-8')
    # density check: never > 2 s without a tray/full scene/behind text
    spans = sorted((c['t'], c['t'] + c['d']) for c in CUES)
    end, gaps = 0, []
    for a, b in spans:
        if a - end > 0.4:
            gaps.append((round(end, 2), round(a, 2)))
        end = max(end, b)
    print('cues', len(CUES), 'words', len(props['words']), 'sfx', len(props['sfx']), 'gaps>0.4s', gaps, 'end', round(end, 2))
