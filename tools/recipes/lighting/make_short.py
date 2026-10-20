"""ONE full lighting short (Aly 2026-10-14: "شورت واحد كامل"; new look 'glass' from his Behance ref in his channel colours).
His face is on screen the WHOLE short (the video is about light: the viewer must SEE the effect) -> composition film-short,
look 'glass', prop `cam` = one continuous mp4 of the kept pieces (work/cam.mp4 -> public) + layout keys per chapter.
Run: python work/scripts/make_short.py  -> public/projects/<code>/short_1.json, cam.mp4, voice_1.wav
Piece = (chapter, first word start, last word start[, a_force, b_force]) fitted on the waveform, or ('raw', a, b) = a silent
moment of his video where a light switches on (his music is under it -> fixed -8 dB, no levelling)."""
import json, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))

W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
sys.stdout.reconfigure(encoding='utf-8')
CODE = P.name
PJ = f'projects/{CODE}/'
PUB = ROOT / 'motion-library' / 'public' / 'projects' / CODE
SRC = P / 'input' / 'o7QYL5qIY84.mp4'
tr = json.load(open(W / 'transcript.json', encoding='utf8'))
from edges import fit
import level_voice as LV
_words = [w for s in tr['sentences'] for w in s['words']]
KEEP = set()

PIECES = [
    ('hook', 5.31, 10.96), ('hook', 14.10, 15.04),
    ('idea', 87.25, 92.97), ('idea', 108.05, 114.55), ('idea', 120.31, 123.67),
    ('off', 129.27, 132.41), ('raw', 137.0, 138.8), ('off', 142.45, 145.05),
    ('key', 147.97, 151.15), ('raw', 163.6, 165.9),
    ('hs', 176.15, 178.11), ('hs', 180.45, 184.23), ('hs', 190.97, 192.99), ('hs', 209.53, 212.89), ('hs', 214.03, 218.13),
    ('ang', 229.99, 233.29), ('ang', 246.43, 250.05), ('ang', 255.43, 260.07),
    ('wall', 278.07, 281.37), ('wall', 285.59, 288.59),
    ('back', 300.65, 302.35, None, 303.12), ('back', 307.49, 311.09), ('back', 320.01, 324.29), ('raw', 329.4, 331.6), ('back', 336.94, 342.12),
    ('spill', 373.78, 376.16), ('spill', 383.34, 386.10), ('spill', 390.42, 393.40), ('spill', 399.42, 402.40),
    ('amb', 465.12, 467.52, None, 467.97), ('raw', 469.3, 472.6), ('amb', 493.01, 500.61),
    ('amb', 513.33, 515.41), ('amb', 518.03, 519.89),
    ('foc', 525.53, 529.39), ('foc', 540.79, 543.45), ('foc', 558.19, 561.81), ('foc', 603.29, 607.17),
    ('foc', 609.75, 613.33), ('raw', 622.9, 625.9),
    ('end', 631.86, 638.84), ('end', 681.12, 682.98),
]
# caption text of the KEPT words of every sentence (spelling + English terms in Latin)
TXT = {
    'S001': 'هنعرف إزاي نقدر نطوّر من الجودة اللي بنطلّعها من كاميرا الموبايل بتاعنا من الجودة دي لكده وبكاميرا الموبايل وبس',
    'S018': 'النور مش الهدف منه', 'S019': 'الأساسي في التصوير', 'S020': 'إن انت تظهر علشان ما تكونش مضلّم في الكاميرا',
    'S024': 'الهدف من الضوء واستخدامنا ليه في الفيديوهات هو إنه يدي بُعد ثلاثي الأبعاد 3D للفيديو بتاعك',
    'S026': 'فمحتاج إن انت تزوّد ظل عشان يدي لك إحساس بالبُعد',
    'S028': 'أول خطوة لازم نعملها نقفل كل الأنوار اللي في الأوضة', 'S029': 'انت دلوقتي مش شايفني خالص لإن الدنيا كلها ضلمة',
    'S031': 'النقطة الأولى اللي هتلاقيها كل الناس بتتكلم عليها وهي Key Light',
    'S038': 'نوع اسمه Hard Light ونوع اسمه Soft Light', 'S040': 'الفرق إن انت لو فتحت لمبة كده قصادك فدي إضاءة مباشرة قوي',
    'S043': 'بيخليك كأن الشكل بتاعك ناشف', 'S049': 'فالحل في حاجة زي كده إنك ممكن تستخدم سوفت بوكس',
    'S050': 'أو ممكن تعمله بنفسك إنك تجيب لمبة وتحط قدامها زي قماشة بيضا',
    'S055': 'النقطة التانية إنك تخلي الضوء مايجيلكش من وشك على طول', 'S060': 'الضوء هيخلي تقريبًا مفيش خالص Shadow أو ظل في وشك',
    'S063': 'لكن دلوقتي الضوء لما جايلي شوية Angle بزاوية سواء كده أو كده', 'S067': 'فده خلّى إحساس إن فيه بُعد أكتر',
    'S071': 'بمعنى إيه ما تتصورش وانت عندك الحيطة في ضهرك على طول', 'S073': 'فحاول على قد ما تقدر الحيطة بعيدة عنك شوية',
    'S077': 'تاني ضوء احنا عايزين نستخدمه هو Back Light', 'S079': 'ويكون الثانوي ده في الخلفية ورا وعكس اتجاه Key Light',
    'S083': 'وبرضو هيعمل لك زي حواف كده لجسمك أكتر هيظهرها لك بشكل أفضل',
    'S085': 'Key Light هو النور الأبيض، Back Light هو النور الأصفر بحيث إن هما يعملوا تباين أو Contrast',
    'S088': 'طب إزاي تعمل كده؟ إزاي تحدد', 'S089': 'مسار الضوء؟', 'S091': 'بس الفكرة إن احنا قفلناها بحاجة ألمونيوم',
    'S092': 'الضوء ما بيخرجش غير من', 'S093': 'الجانب اللي احنا سايبينه يخرج منه',
    'S095': 'زي كده في السوفت بوكس اللي عندي فيه حاجة اسمها Grid أو شبكة',
    'S102': 'ونضيف Ambient Light أو إضاءة محيطة في المكان', 'S112': 'طب يلا بينا بقى أنوّر كل Fill Light اللي عندي',
    'S119': 'وبرضو بقى عندي كمان كده شريط LED حاطه ورايا', 'S120': 'برضو منوّر بلون السيان وهو بمتين وعشرين جنيه بس فهو مش غالي',
    'S125': 'وفي نفس الوقت استخدمت شاشة الكمبيوتر', 'S127': 'كلون من الألوان المحيطة بيك',
    'S129': 'عايزين نخلي الخلفية تكون فيها شوية بلور', 'S130': 'ويكون الفوكس عليا أنا بس',
    'S134': 'بس أنا زي ما قلت أنا بستخدم كاميرا الموبايل بتاعتي', 'S135': 'طب في الكيس دي أنا نزّلت أبلكيشن اسمه Open Camera',
    'S139': 'كده أنا مشغّل Manual Focus وضابطه على الزاوية اللي أنا قاعد فيها وبس',
    'S149': 'الصورة ورا هي اللي معمولة شوية بلور وأنا اللي بقيت في', 'S150': 'الفوكس وإحساس كأنك بتصور بكاميرا',
    'S151': 'بعدسة وأنا أصلًا بصور بالموبايل', 'S153': 'فأعتقد إن دلوقتي الصورة تعتبر',
    'S154': 'احترافية جدًا من الأول لحد دلوقتي فيه اختلاف كبير جدًا', 'S165': 'Key Light Back Light Fill Light',
}
# chapter -> (scene id, beats in source seconds)
SCENES = {
    'hook': ('gl_hook', {'this': 9.27, 'that': 10.96, 'phone': 14.10}),
    'idea': ('gl_idea', {'no': 90.71, 'goal': 108.05, 'd3': 113.07, 'shadow': 121.83, 'depth': 123.35}),
    'off': ('gl_off', {'off': 137.6, 'dark': 142.45}),
    'key': ('gl_key', {'name': 150.57, 'on': 163.9}),
    'hs': ('gl_hardsoft', {'hard': 176.71, 'soft': 177.89, 'direct': 183.69, 'dry': 192.99, 'box': 209.53, 'cloth': 214.55}),
    'ang': ('gl_angle', {'front': 246.43, 'side': 255.43, 'depth': 258.49}),
    'wall': ('gl_wall', {'wall': 280.47, 'far': 285.59}),
    'back': ('gl_back', {'behind': 309.29, 'edge': 320.01, 'on': 330.0, 'white': 337.66, 'yellow': 339.30, 'contrast': 341.28}),
    'spill': ('gl_spill', {'foil': 383.34, 'out': 391.68, 'grid': 400.0}),
    'amb': ('gl_amb', {'on': 470.3, 'led': 493.01, 'price': 499.05, 'screen': 513.33}),
    'foc': ('gl_focus', {'me': 528.39, 'phone': 540.79, 'app': 543.09, 'mf': 558.19, 'bg': 603.29, 'lens': 609.75, 'mobile': 612.47, 'demo': 622.9}),
    'end': ('gl_end', {'diff': 638.0, 'k': 681.12, 'b': 681.74, 'f': 682.56}),
}
# camera layout changes (source second, mode); default 'low'
CAM = [(5.0, 'full'), (10.96, 'low'), (137.0, 'wide'), (142.45, 'low'), (163.6, 'wide'), (176.15, 'low'), (246.43, 'hide'), (255.43, 'low'),
       (278.07, 'wide'), (300.65, 'low'), (329.4, 'wide'), (336.94, 'low'), (469.3, 'wide'), (493.01, 'low'), (622.9, 'wide'), (631.86, 'low')]
CTA_KEEP = (7.0, 11.95)
CTA_FIX = {'بعطلك': 'هبعتلك', 'طول.': 'طول'}
SFX = {  # (beat | seconds from scene start, sfx, volume[, dur])
    'gl_hook': [(0, 'impact', 0.45), ('this', 'pop_1', 0.4), ('that', 'magic', 0.5), ('phone', 'pop_2', 0.45)],
    'gl_idea': [('no', 'buzz_wrong', 0.35), ('goal', 'swoop_up', 0.4), ('shadow', 'magic', 0.45), ('depth', 'ding', 0.4)],
    'gl_off': [('off', 'click', 0.9), ('off', 'swoop_down', 0.45), ('dark', 'shh', 0.25)],
    'gl_key': [('name', 'pop_2', 0.4), ('on', 'click', 0.9), ('on', 'riser', 0.3, 1.5)],
    'gl_hardsoft': [('hard', 'pop_1', 0.45), ('soft', 'pop_3', 0.45), ('dry', 'buzz_wrong', 0.35), ('box', 'swoop_up', 0.4), ('cloth', 'paper', 0.4)],
    'gl_angle': [('front', 'buzz_wrong', 0.3), ('side', 'swish', 0.45), ('depth', 'ding', 0.45)],
    'gl_wall': [('wall', 'door_slam', 0.3), ('far', 'swoop_up', 0.45)],
    'gl_back': [('behind', 'pop_2', 0.4), ('edge', 'magic', 0.4), ('on', 'click', 0.9), ('white', 'pop_1', 0.4), ('yellow', 'pop_3', 0.4), ('contrast', 'impact', 0.35)],
    'gl_spill': [('foil', 'rustle', 0.45, 1.2), ('out', 'swish', 0.4), ('grid', 'tick', 0.45)],
    'gl_amb': [('on', 'click', 0.9), ('on', 'magic', 0.4), ('led', 'pop_2', 0.4), ('price', 'cash', 0.45), ('screen', 'pop_3', 0.4)],
    'gl_focus': [('me', 'shutter', 0.45), ('app', 'pop_2', 0.4), ('mf', 'tick', 0.45), ('lens', 'shutter', 0.4), ('mobile', 'ding', 0.45), ('demo', 'swoop_down', 0.35)],
    'gl_end': [('diff', 'swish', 0.45), ('k', 'pop_1', 0.45), ('b', 'pop_2', 0.45), ('f', 'pop_3', 0.45)],
}


def span(t0, t1, a_force=None, b_force=None):
    i = min(range(len(_words)), key=lambda k: abs(_words[k]['start'] - t0))
    j = min(range(len(_words)), key=lambda k: abs(_words[k]['start'] - t1))
    prev = _words[i - 1]['end'] if i > 0 else None
    nxt = _words[j + 1]['start'] if j + 1 < len(_words) else None
    a, b, rep = fit(_words[i]['start'], _words[j]['end'], prev, nxt)
    if a_force: a = a_force; rep += f' START FORCED {a_force}'
    if b_force: b = b_force; rep += f' END FORCED {b_force}'
    KEEP.update(id(w) for w in _words[i:j + 1])
    print('   ', _words[i]['w'], '…', _words[j]['w'], rep)
    return [a, b]


def main():
    ranges, chap = [], []
    for p in PIECES:
        if p[0] == 'raw':
            ranges.append([p[1], p[2]]); print('    RAW', p[1], p[2])
        else:
            ranges.append(span(*p[1:]))
        chap.append(p[0])
    segs, tl = [], 0.0
    for (a, b), c in zip(ranges, chap):
        segs.append({'src': a, 'tl': round(tl, 3), 'len': round(b - a, 3), 'raw': c == 'raw'}); tl += b - a
    main_len = tl

    def to_tl(t):
        for s in segs:
            if s['src'] - 0.01 <= t <= s['src'] + s['len'] + 0.01:
                return s['tl'] + max(0.0, min(t - s['src'], s['len']))
        best = min([(abs(t - s['src']), s['tl']) for s in segs] + [(abs(t - s['src'] - s['len']), s['tl'] + s['len']) for s in segs])
        if best[0] <= 0.7:
            return best[1]
        raise ValueError(f'{t} outside ranges')

    # captions
    words = []
    for snt in tr['sentences']:
        kept = [w for w in snt['words'] if id(w) in KEEP]
        if not kept:
            continue
        txt = TXT.get(snt['id'])
        if txt is None:
            print('  !! no caption text for', snt['id'], ' '.join(w['w'] for w in kept))
        else:
            new = txt.split()
            if len(new) == len(kept):
                kept = [{**w, 'w': x} for w, x in zip(kept, new)]
            else:
                # different count: spread inside each kept RANGE separately is not possible -> only allowed for one-range sentences
                rs = {min(range(len(ranges)), key=lambda r: 0 if ranges[r][0] - 0.05 <= w['start'] < ranges[r][1] else 9) for w in kept}
                if len(rs) > 1:
                    print('  !! word count mismatch across ranges', snt['id'], len(new), len(kept))
                a0, b0 = kept[0]['start'], kept[-1]['end']
                tot = sum(len(x) + 1 for x in new); t = a0; kk = []
                for x in new:
                    d = (b0 - a0) * (len(x) + 1) / tot; kk.append({'w': x, 'start': t, 'end': t + d}); t += d
                kept = kk
        for w in kept:
            ra, rb = min(ranges, key=lambda r: 0 if r[0] - 0.05 <= w['start'] < r[1] else min(abs(w['start'] - r[0]), abs(w['start'] - r[1])))
            words.append({'w': w['w'], 'start': round(to_tl(max(w['start'], ra)), 3), 'end': round(to_tl(max(ra, min(w['end'], rb))), 3)})
    ct = json.load(open(W / 'cta' / 'transcript.json', encoding='utf8'))
    for w in [w for s_ in ct['sentences'] for w in s_['words'] if CTA_KEEP[0] - 0.05 <= w['start'] < CTA_KEEP[1] - 0.05]:
        x = CTA_FIX.get(w['w'], w['w'])
        if x:
            words.append({'w': x, 'start': round(main_len + w['start'] - CTA_KEEP[0], 3), 'end': round(main_len + w['end'] - CTA_KEEP[0], 3)})

    # scenes: one per chapter, from its first piece to the next chapter
    order = []
    for (a, b), c, s in zip(ranges, chap, segs):
        c2 = c if c != 'raw' else order[-1][0]
        if not order or order[-1][0] != c2:
            order.append([c2, s['tl'], s['tl'] + s['len']])
        else:
            order[-1][2] = s['tl'] + s['len']
    scenes = []
    for k, (c, a, b) in enumerate(order):
        t, beats = SCENES[c]
        b2 = order[k + 1][1] if k + 1 < len(order) else main_len
        props = {'b': {n: round(to_tl(v) - a, 3) for n, v in beats.items()}}
        if c in ('hook', 'end'):
            props['pics'] = PJ
        scenes.append({'t': t, 'at': round(a, 3), 'dur': round(b2 - a, 3), 'layer': 'front', 'props': props})
    keys = [{'t': round(to_tl(s) if s > 5.31 else 0, 3), 'm': m} for s, m in CAM]

    # sfx
    L = 'sfx/'
    sfx = []
    for i, s in enumerate(scenes):
        if s['at'] > 0.3:
            sfx.append({'file': L + f'whoosh_{i % 3 + 1}.wav', 'at': round(max(0, s['at'] - 0.12), 3), 'vol': 0.4})
        for it in SFX.get(s['t'], []):
            off = s['props']['b'].get(it[0]) if isinstance(it[0], str) else it[0]
            if off is None or off >= s['dur']:
                continue
            sfx.append({'file': L + it[1] + '.wav', 'at': round(s['at'] + off, 3), 'vol': it[2], 'dur': round(it[3] if len(it) > 3 else 3.0, 3)})
    for k in keys[1:]:
        sfx.append({'file': L + 'swish.wav', 'at': k['t'], 'vol': 0.25})
    c0 = main_len + 0.6
    sfx += [{'file': L + 'whoosh_1.wav', 'at': round(main_len - 0.1, 3), 'vol': 0.45}, {'file': L + 'typing.wav', 'at': round(c0 + 34 / 30, 3), 'vol': 0.45, 'dur': 0.9},
            {'file': L + 'pop_2.wav', 'at': round(c0 + 62 / 30, 3), 'vol': 0.55}, {'file': L + 'ding.wav', 'at': round(c0 + 84 / 30, 3), 'vol': 0.5}]

    # voice: speech pieces levelled (gain only); raw pieces = his music at a fixed -8 dB with soft fades
    if LV._src is None:
        LV._src = LV.rd(SRC)
    SR = LV.SR; parts, log = [], []
    for s in segs:
        a, b = s['src'], s['src'] + s['len']
        x = LV._src[int(a * SR):int(b * SR)].copy()
        if s['raw']:
            y = x * 10 ** (-8 / 20); fade = int(0.25 * SR); log.append('raw')
        else:
            y, gs = LV.level(x, [int((t - a) * SR) for t in LV._bounds if a < t < b]); fade = int(0.012 * SR); log.append(gs)
        y[:fade] *= np.linspace(0, 1, fade); y[-fade:] *= np.linspace(1, 0, fade)
        parts.append(y)
    c = LV.rd(ROOT / 'motion-library' / 'public' / (PJ + 'cta.mp4'))[int(CTA_KEEP[0] * SR):int(CTA_KEEP[1] * SR)]
    cy, _ = LV.level(c, []); parts.append(cy)
    out = PUB / 'voice_1.wav'; raw = out.with_suffix('.raw.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', str(raw)], input=np.concatenate(parts).astype(np.float32).tobytes(), check=True)
    m = subprocess.run(['ffmpeg', '-i', str(raw), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float(m.split('Integrated loudness:')[1].split('I:')[1].split('LUFS')[0])
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af', f'volume={-15 - I:.2f}dB,alimiter=limit=0.89:level=false', '-c:a', 'pcm_s16le', str(out)], check=True)
    raw.unlink()
    print('  voice gains:', log)

    # cam.mp4 = the kept pieces of his video, in order (no audio), keyframe every 15 frames for fast seeking
    cam = PUB / 'cam.mp4'
    if '--nocam' not in sys.argv:
        args = ['ffmpeg', '-v', 'error', '-y']
        for s in segs:
            args += ['-ss', f'{s["src"]:.3f}', '-t', f'{s["len"] + 0.2:.3f}', '-i', str(SRC)]
        # exact frame count per piece (= the frames of its range on the 30 fps timeline) -> no drift against the voice
        nf = [round((s['tl'] + s['len']) * 30) - round(s['tl'] * 30) for s in segs]
        fc = ''.join(f'[{i}:v]fps=30,trim=end_frame={nf[i]},setpts=PTS-STARTPTS,settb=1/30[v{i}];' for i in range(len(segs)))
        fc += ''.join(f'[v{i}]' for i in range(len(segs))) + f'concat=n={len(segs)}:v=1:a=0[v]'
        args += ['-filter_complex', fc, '-map', '[v]', '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', '-g', '15', '-pix_fmt', 'yuv420p', str(cam)]
        subprocess.run(args, check=True)
        d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(cam)], capture_output=True, text=True).stdout)
        print(f'  cam.mp4 {d:.2f}s (main {main_len:.2f}s)')
    for name, t in [('before.jpg', 30.0), ('after.jpg', 645.0)]:
        if not (PUB / name).exists():
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', str(SRC), '-frames:v', '1', '-q:v', '2', str(PUB / name)], check=True)

    dur = round(main_len + CTA_KEEP[1] - CTA_KEEP[0], 3)
    props = {'fps': 30, 'duration': dur, 'voice': PJ + 'voice_1.wav', 'segs': [{'src': 0, 'tl': 0, 'len': dur}], 'words': words, 'aly': [],
             'scenes': scenes, 'sfx': sfx, 'look': 'glass', 'capBottom': 0.07, 'ctaVol': 0.0, 'sfxGain': 1.0,
             'cam': {'file': PJ + 'cam.mp4', 'keys': keys},
             'cta': {'file': PJ + 'cta.mp4', 'tl': round(main_len, 3), 'len': round(CTA_KEEP[1] - CTA_KEEP[0], 3), 'src': CTA_KEEP[0]},
             'ctaCue': {'at': 0.6, 'dur': round(CTA_KEEP[1] - CTA_KEEP[0] - 0.6, 3), 'props': {
                 'title': 'اكتب في *كومنت*', 'keyword': 'يوتيوب', 'dm': 'ده لينك الفيديو كامل 🎬', 'typeAt': 34, 'sendAt': 62, 'dmAt': 84, 'top': 0.02}}}
    json.dump(props, open(PUB / 'short_1.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(f'short: {main_len:.1f}s + CTA = {dur:.1f}s ({int(dur // 60)}:{dur % 60:04.1f}) | {len(segs)} pieces, {len(scenes)} scenes')
    for s in scenes:
        print(f"   {s['t']:12s} {s['at']:7.2f} +{s['dur']:5.2f}  {s['props']['b']}")


main()
