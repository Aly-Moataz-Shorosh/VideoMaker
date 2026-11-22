"""plan.py + timeline.json + ElevenLabs words -> props for composition 'uth-reel' (work/props.json)."""
import json, re
from pathlib import Path
import plan as P

W = Path(__file__).resolve().parents[1]
tl = json.loads((W / 'timeline.json').read_text())
el = [w for w in json.loads((W / 'el_words.json').read_text(encoding='utf-8'))['words'] if w['type'] == 'word']
H0, HL, RW, M0 = tl['hook'][1], tl['hookLen'], tl['rew'], tl['main0']


def T(s, hook=False):  # source second -> reel second
    return round(s - H0, 3) if hook else round(HL + RW + (s - M0), 3)


def words_of(a, b, text, hook):
    """English words of a phrase with times: the ElevenLabs words inside [a, b] in order; when the fixed text has a
    different count, spread the fixed words over the phrase by character length."""
    src = [w for w in el if w['start'] >= a - 0.05 and w['end'] <= b + 0.05]
    toks = text.split()
    if len(src) == len(toks):
        tm = [(w['start'], w['end']) for w in src]
    else:
        L = sum(len(t) for t in toks); tm = []; c = a
        for t in toks:
            d = (b - a) * len(t) / L; tm.append((c, c + d)); c += d
    return [{'w': t, 's': T(s, hook), 'e': T(e, hook)} for t, (s, e) in zip(toks, tm)]


def phrases(lst, hook):
    out = []
    for i, (a, b, en, ar) in enumerate(lst):
        nxt = lst[i + 1][0] if i + 1 < len(lst) else b + 0.6
        out.append({'t0': T(a, hook), 't1': T(min(nxt, b + 0.6), hook), 'en': words_of(a, b, en, hook), 'ar': ar})
    return out


def cues(lst, hook):
    return [{'t': T(a, hook), 'd': round(b - a, 3), 'k': k, 'p': p} for a, b, k, p in lst]


caps = phrases(P.HOOK_PHRASES, True) + phrases(P.PHRASES, False)
cs = cues(P.HOOK_CUES, True) + cues(P.CUES, False)
# sound: whoosh on each scene that comes in, pop on cards, cash/ding on the punch lines
sfx = []
for i, c in enumerate(cs):
    sfx.append({'t': c['t'], 'file': f'sfx/whoosh_{i % 3 + 1}.wav', 'vol': 0.22})
    if c['k'] in ('count',):
        sfx.append({'t': c['t'] + c['p']['at'], 'file': 'sfx/ding.wav', 'vol': 0.25})
    if c['k'] == 'versions':
        for key in ('at', 'c1', 'c2', 'riffs'):
            sfx.append({'t': c['t'] + c['p'][key], 'file': f'sfx/pop_{len(sfx) % 3 + 1}.wav', 'vol': 0.3})
        sfx.append({'t': c['t'] + c['p']['bad'], 'file': 'sfx/buzz_wrong.wav', 'vol': 0.2})
    if c['k'] == 'hire':
        sfx.append({'t': c['t'] + c['p']['at'], 'file': 'sfx/impact.wav', 'vol': 0.3})
    if c['k'] == 'term':
        sfx.append({'t': c['t'] + c['p'].get('at', 0.3), 'file': 'sfx/pop_2.wav', 'vol': 0.25})
sfx.append({'t': HL, 'file': 'sfx/tape.wav', 'vol': 0.35})
# zoom on him: hook pushes in, then every scene change alternates 1.0 / 1.08 (jump-cut energy), calm (<= 1.1)
zoom = [[0, 1.0], [HL - 0.05, 1.1], [HL, 1.0]]
z = 1.0
for c in cs[1:]:
    if c['t'] > HL:
        z = 1.08 if z == 1.0 else 1.0
        zoom += [[c['t'] - 0.01, zoom[-1][1]], [c['t'] + 0.35, z]]
props = {'duration': round(tl['duration'], 3), 'cam': 'projects/uth/cam.mp4', 'voice': 'projects/uth/voice.wav',
         'hookEnd': HL, 'rewind': {'t': HL, 'd': RW, 'from': '1:53', 'to': '0:04'},
         'head': P.HEAD, 'tag': P.TAG, 'tagAr': P.TAG_AR, 'caps': caps, 'cues': cs, 'sfx': sfx, 'zoom': zoom}
(W / 'props.json').write_text(json.dumps(props, ensure_ascii=False, indent=1), encoding='utf-8')
print('duration', props['duration'], 'caps', len(caps), 'cues', len(cs))
for c in caps:
    if c['t1'] <= c['t0']: print('BAD caption', c)
