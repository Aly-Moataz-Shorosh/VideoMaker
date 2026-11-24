"""Compare the generated narration (Whisper transcript) with the script, word by word.
Input : assets/ai/heygen/voice_v1/voice_v1.json (chapters + durations, concat order)
        work/whisper_voice_v1/transcript.json (from tools/transcribe.py on work/voice_v1_all.wav)
Output: work/voice_check_v1.md  (per chapter: match %, every differing stretch with its time)
        work/voice_timing_v1.json (per chapter: start/end in the joined file, words with times)
Usage : python -X utf8 work/scripts/check_voice.py   (run from the project folder)"""
import difflib, json, re

P = json.load(open('assets/ai/heygen/voice_v1/voice_v1.json', encoding='utf-8'))
T = json.load(open('work/whisper_voice_v1/transcript.json', encoding='utf-8'))
words = [w for s in T['sentences'] for w in s['words']]

def norm(w):
    w = re.sub(r'[ً-ْـ]', '', w)          # diacritics, tatweel
    w = re.sub(r'[إأآ]', 'ا', w).replace('ى', 'ي').replace('ة', 'ه')
    w = re.sub(r'[^\w\-\.]', '', w.lower()).strip('.-')
    return w

def toks(text):
    return [t for t in (norm(x) for x in text.split()) if t]

out, timing, t0 = ['# voice check v1 (Whisper vs script)\n'], [], 0.0
for p in P['parts']:
    t1 = t0 + p['duration_s']
    ws = [w for w in words if t0 - 0.05 <= (w['start'] + w['end']) / 2 < t1]
    heard = [norm(w['w']) for w in ws]
    keep = [i for i, h in enumerate(heard) if h]
    heard = [heard[i] for i in keep]; ws = [ws[i] for i in keep]
    want = toks(p['text'])
    sm = difflib.SequenceMatcher(None, want, heard, autojunk=False)
    ratio = sm.ratio()
    diffs = []
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op == 'equal':
            continue
        at = ws[b1]['start'] - t0 if b1 < len(ws) else (ws[-1]['end'] - t0 if ws else 0)
        diffs.append((round(at, 1), ' '.join(want[a1:a2]), ' '.join(heard[b1:b2])))
    # name check: every «علي» in the script must be heard as علي (not عليا)
    name_bad = [w for w in ws if norm(w['w']) in ('عليا', 'اليا', 'عاليا')]
    out.append(f"\n## {p['chapter']} — {ratio*100:.0f}% ({p['duration_s']:.1f} s)\n")
    if name_bad:
        out.append('**⚠ الاسم: ' + ', '.join(f"{w['w']} @ {w['start']-t0:.1f}s" for w in name_bad) + '**\n')
    for at, a, b in diffs:
        out.append(f"- {at:>6} s | سكريبت: «{a}» | اتسمع: «{b}»\n")
    timing.append({'chapter': p['chapter'], 'start': round(t0, 3), 'end': round(t1, 3),
                   'words': [{'w': w['w'], 's': round(w['start'] - t0, 3), 'e': round(w['end'] - t0, 3)} for w in ws]})
    t0 = t1

open('work/voice_check_v1.md', 'w', encoding='utf-8').write(''.join(out))
json.dump(timing, open('work/voice_timing_v1.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(''.join(l for l in out if l.startswith('\n## ') or '⚠' in l))
