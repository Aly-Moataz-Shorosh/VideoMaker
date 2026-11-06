"""Sound events: AST (AudioSet) labels on the NON-vocal stem (drums+other+bass) in 0.96 s windows, hop 0.48 s.
Prints top non-speech/non-music labels per window + onsets of the non-vocal stem."""
import json, numpy as np, torch, librosa, sys
from pathlib import Path
from transformers import ASTForAudioClassification, AutoFeatureExtractor
sys.stdout.reconfigure(encoding='utf-8')
W = Path(__file__).resolve().parents[1]
S = W / 'stems/htdemucs/scene_audio'
y = sum(librosa.load(str(S / f'{k}.wav'), sr=16000, mono=True)[0] for k in ('drums', 'other', 'bass'))
mix = librosa.load(str(W / 'scene_audio.wav'), sr=16000, mono=True)[0]
m = 'MIT/ast-finetuned-audioset-10-10-0.4593'
fe = AutoFeatureExtractor.from_pretrained(m); net = ASTForAudioClassification.from_pretrained(m).eval()
lab = net.config.id2label
SKIP = ('Speech', 'Music', 'Male speech', 'Conversation', 'Narration', 'Silence', 'Inside, small room', 'Inside, large room',
        'Musical instrument', 'Male singing', 'Singing', 'Ambient music', 'Soundtrack music', 'Background music', 'Drone music')
out = []
win, hop = 0.96, 0.48
T = np.arange(0, len(y) / 16000 - win, hop)
for i in range(0, len(T), 16):
    chunk = [y[int(t * 16000):int((t + win) * 16000)] for t in T[i:i + 16]]
    x = fe(chunk, sampling_rate=16000, return_tensors='pt')
    with torch.no_grad():
        pr = torch.sigmoid(net(**x).logits).numpy()
    for t, p in zip(T[i:i + 16], pr):
        top = [(lab[j], round(float(p[j]), 2)) for j in np.argsort(-p)[:8] if lab[j] not in SKIP and p[j] > 0.08][:4]
        out.append({'t': round(float(t), 2), 'top': top, 'rms': round(float(20 * np.log10(np.sqrt(np.mean(y[int(t * 16000):int((t + win) * 16000)] ** 2)) + 1e-9)), 1)})
        print(f"{t:6.2f} {out[-1]['rms']:6.1f}  " + ' | '.join(f'{a} {b}' for a, b in top), flush=True)
on = librosa.onset.onset_detect(y=y, sr=16000, units='time', backtrack=True, delta=0.25)
json.dump({'win': out, 'onsets': [round(float(o), 3) for o in on]}, open(W / 'sfx_events.json', 'w', encoding='utf-8'), ensure_ascii=False)
