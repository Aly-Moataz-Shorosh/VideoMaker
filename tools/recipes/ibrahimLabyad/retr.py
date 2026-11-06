"""Re-transcribe windows: A = script text as prompt, B = no prompt. Word times printed."""
import json, subprocess, sys, numpy as np
from pathlib import Path
from faster_whisper import WhisperModel
sys.stdout.reconfigure(encoding='utf-8')
W = Path(__file__).resolve().parents[1]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(W / 'src720_crop-ready.mp4'), '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True, check=True).stdout
A = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
m = WhisperModel(str(Path.home() / 'ai-models/faster-whisper-large-v3-turbo'), device='cpu', compute_type='int8', cpu_threads=10)
P55a = 'سيبت معلمك ليه دي دواخلك ماتستوقفنيش. لكن اللي هايهمني يا غالي هو لو انت جيت فكرت في يوم تسيب شغلي. انت مسألتنيش لكن أنا أقولك أنا اخترتك ليه يا سيد ابراهيم. لأن الزول اللي بيصون أسرار شغل سيده يبقى. ماليش سيد. رغم أنك مفارق سيدك ومش راجع. لما أنا حاولت اسرسب منك معلومة قطمت. ولما ضغط اكتر توهت. أهم حاجة سرنا يكون جوانا ويدفن معانا.'
P55b = 'لكن انت سبيتني بمجيتك. ليا شرطين. أولهم مالكش حماية عندي. يعني بضاعة وفلوس وسر مدفون رابطنا زي حبل الوريد. وتانيهم فزورة لو حلتها يبقى هانبسمل ونغمز لو محلتهاش يبقى مافيش نصيب.'
P55c = 'أسد يحكم مملكة، روحه في بنته اللي مجابش غيرها. تقوم تتعتر في ضبع خسيس تهواه ويصير روحها فيه وللأسف تجيب منه ذرية هي نور عينه. هذا الضبع دحلاب وسخ. الأسد خده في كنفه ورفع شأنه وعمله دراعه اليمين. سنين وتشاء العناية الإلهية الأسد يعرف إن الضبع قام بوشاية كان هايودي الأسد في ستين داهية ويورث هو الملك كله. لا يقدر يقتله ولا يقدر يسيبه. فكرك يعمل إيه يا سيد ابراهيم.'
P56 = 'عشري: ابراهيم فضل يشرب ويشرب ويبلع ويسف أي نوع برشام كان بيلاقيه. اسم ابراهيم إنه نازل حتة كان بيشل الخلق. كان جيش لوحده. الفلوس كترت والحفرة اتملت وحفرنا غيرها أوسع. وعمنا زرزور هس بس. المصيبة جاية جاية.'
WIN = [(6, 46, P55a), (44, 76, P55b), (75, 112, P55c), (110, 147, P55c), (145, 182, P55c), (178, 205, P55c + ' ' + P56), (203, 242.03, P56)]
res = []
for a, b, p in WIN:
    for tag, prompt in (('A', p), ('B', None)):
        seg, _ = m.transcribe(A[int(a * 16000):int(b * 16000)], language='ar', word_timestamps=True, initial_prompt=prompt,
                              vad_filter=False, condition_on_previous_text=False, beam_size=5)
        for s in seg:
            ws = [(w.word.strip(), round(a + w.start, 2), round(a + w.end, 2), round(w.probability, 2)) for w in s.words]
            res.append({'win': [a, b], 'tag': tag, 'start': round(a + s.start, 2), 'end': round(a + s.end, 2), 'text': s.text.strip(), 'words': ws})
            print(tag, f'{a + s.start:6.2f}-{a + s.end:6.2f}', s.text.strip(), flush=True)
    print('-----')
json.dump(res, open(W / 'tr/retr.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
