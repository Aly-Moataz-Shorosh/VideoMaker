"""Title + description + pinned comment beside the short: output/short_1.txt  (Run: python work/scripts/write_meta.py)"""
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / 'output'
TXT = '''عناوين مقترحة (اختار واحد):
1) صوت مايك اللابتوب بقى نضيف في دقيقتين 🎧
2) 5 إفكتات في Adobe Audition بستخدمهم في كل فيديو
3) شيل الدوشة من صوتك بـ Adobe Audition

الوصف:
الصوت نص جودة الفيديو. دي الـ 5 إفكتات اللي بستخدمها لما أكون مستعجل (متجربة على مايك اللابتوب):
1) Noise Reduction: علّم على حتة ساكتة ← رايت كليك ← Capture Noise Print ← Ctrl+A ← Effects ‹ Noise Reduction / Restoration ‹ Noise Reduction (process) ← Apply.
2) Normalize: Effects ‹ Amplitude and Compression ‹ Normalize (process) ← 93.6% ← Apply.
3) Vocal Enhancer: Effects ‹ Special ‹ Vocal Enhancer ← Male أو Female ← Apply.
4) Mastering: Effects ‹ Special ‹ Mastering ← Preset: Make Room For Vocals ← Apply.
5) Parametric Equalizer: Effects ‹ Filter and EQ ‹ Parametric Equalizer ← Preset: Vocal Enhancer ← Apply.

الفيديو الكامل على القناة: https://youtu.be/IjVlRDHEBSY

#Adobe_Audition #تحسين_الصوت #مونتاج #صناعة_محتوى #علي_شرش

الكومنت المثبت:
عايز الفيديو الكامل؟ اكتب "يوتيوب" في كومنت وهيوصلك اللينك على طول 📩 أو امسح الـ QR اللي في آخر الفيديو.
'''
OUT.mkdir(exist_ok=True)
(OUT / 'short_1.txt').write_text(TXT, encoding='utf-8')
print('ok')
