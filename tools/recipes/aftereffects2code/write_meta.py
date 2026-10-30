"""Title + description + pinned comment beside the short: output/short_1.txt  (Run: python work/scripts/write_meta.py)"""
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / 'output'
TXT = '''عناوين مقترحة (اختار واحد):
1) حوّل أنيميشن After Effects لكود يشتغل في موقعك ▶
2) أنيميشن After Effects بقى كود! (Bodymovin ببلاش)
3) Play و Pause لأنيميشن عملته على After Effects

الوصف:
إزاي تحوّل أنيميشن عملته على After Effects لكود (.json) وتشغّله في موقعك أو تطبيق Android، وتتحكم فيه بالكود:
1) نصيحة: الإفكتات زي Wave Warp مش بتتحول، اعمل الحركة في الـ Shape نفسه.
2) البلجن: Bodymovin (Open Source وببلاش) على GitHub. غيّر .zxp لـ .zip وفكّه في:
   Adobe After Effects ‹ Support Files ‹ extensions
3) Window ‹ Extensions ‹ Bodymovin ← علّم على الكومبوزيشن ← اختار المكان ← Render = ملف .json
4) Get the Player = ملف player.js
5) شغّل من سيرفر (XAMPP ← Apache)، مش بفتح ملف الـ HTML على طول.
6) bodymovin.loadAnimation({ path, container, loop, autoplay })
7) زرار PLAY / PAUSE: animation.play() و animation.pause()، والـ hover بـ addEventListener.
8) في الاختبار: الـ Shape Layer أحسن واحد (4 KB بس).

الفيديو الكامل على القناة: https://youtu.be/5C4KNFiJFjA
البلجن: https://github.com/airbnb/lottie-web

#After_Effects #Lottie #Bodymovin #موشن_جرافيك #ويب #علي_شرش

الكومنت المثبت:
عايز الفيديو الكامل؟ اكتب "يوتيوب" في كومنت وهيوصلك اللينك على طول 📩 أو امسح الـ QR اللي في آخر الفيديو.
'''
OUT.mkdir(exist_ok=True)
(OUT / 'short_1.txt').write_text(TXT, encoding='utf-8')
print('ok')
