"""Final pass (gain only): -16 LUFS with a transparent peak limiter, compressed like Aly's `ffmpeg -i in out` (x264 CRF 23 + AAC),
plus the .txt beside each video (starts with the exact header 'العناوين:' — his posting script reads it; no YouTube link).
python work/scripts/finalize.py 8 33 44   (output/_raw/short_N.mp4 -> output/NN_slug.mp4 + .txt)"""
import json, re, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding='utf-8')
from shorts_data import SHORTS

P = Path(__file__).resolve().parents[2]
TAGS = '#رحلة_إلى_مركز_الجرافيكس #جرافيكس #علي_شرش'
PIN = 'السلسلة كاملة على القناة: بلايليست "رحلة إلى مركز الجرافيكس" 🗺️ امسح الـ QR اللي في آخر الفيديو 📲'
META = {
    8: (['يعني ايه Vector؟ ✏️', 'ليه اللوجو بيتعمل Vector مش صورة عادية؟', 'Raster ولا Vector؟ الفرق في دقيقة'],
        'الصور الـ Raster عبارة عن بيكسلز (مربعات صغيرة كل واحد ليه لونه)، فلو كبرتها أو صغرتها هتبوظ، لأن الكمبيوتر هيزوّد أو يشيل بيكسلز '
        'من عنده. البديل هو الـ Vector: بدل ما تقول للكمبيوتر كل بيكسل لونه ايه، بتقوله خط هنا وشكل هنا وألوانهم ايه، وهو يرسمها، '
        'فالفايل يبقى أصغر ويكبر من غير ما يبوظ. بس الـ Raster لسه مهم للتفاصيل والصور الفوتوغرافية.\n\n'
        'الحلقة دي من سلسلة "هو ايه" (مصطلح 7 من 30)، أول مرحلة في مشروع "رحلة إلى مركز الجرافيكس".'),
    33: (['مجالات الجرافيك ديزاين في حكاية 🌽', 'خيال المآتة بيحكيلك مجالات الصور والجرافيك ديزاين', 'تختار أنهي مجال في الجرافيك ديزاين؟'],
         'دورثي ماشية على الطريق الأصفر رايحة لساحر مدينة أوز، وقابلت خيال المآتة في المزرعة اللي كلها شغالة في الصور والجرافيك ديزاين، '
         'فحكالها عن المجالات: UI و UX، البراندينج، المطبوعات واللياوتس، الباكدجنج، تصميمات السوشيال ميديا وبوسترات الأفلام، '
         'التصوير والريتاتش، الإليستريشن، والديجيتال بينتنج.\n\n'
         'ده الفصل التاني من "المجالات و ساحر مدينة أوز"، المرحلة التانية في مشروع "رحلة إلى مركز الجرافيكس".'),
    44: (['أنهي برنامج 3D تتعلمه؟ 🧊', 'Maya ولا 3ds Max ولا Blender ولا Cinema 4D؟', 'برامج الـ 3D وكل برنامج مميز في ايه'],
         'أغلب برامج الـ 3D شغالة بنفس المبادئ (Modeling, Materials, Lighting, Rigging, Animation)، فلو اتعلمت برنامج تنتقل لغيره بسهولة. '
         '3ds Max أكتر في الموديلينج والعمارة والتصميم الداخلي، Maya أكتر في التحريك (وبيستخدم في ديزني بإضافات وأدوات خاصة بيهم)، '
         'Blender مجاني و Open Source وبيعمل حاجات كتير غير الـ 3D، و Cinema 4D في رأيي من أسهل البرامج للبداية وبيستخدم كتير في '
         '3D Motion Graphics.\n\nمن مرحلة "البرامج"، آخر مرحلة في مشروع "رحلة إلى مركز الجرافيكس".'),
}


def lufs(f):
    r = subprocess.run(['ffmpeg', '-i', str(f), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True, errors='ignore').stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1])


for n in [int(a) for a in sys.argv[1:] if a.isdigit()]:
    raw = P / 'output' / '_raw' / f'short_{n}.mp4'
    name = f'{n:02d}_{SHORTS[n]["slug"]}'
    out = P / 'output' / f'{name}.mp4'
    L, trim = lufs(raw), 0.0
    for _ in range(4):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-c:v', 'libx264', '-crf', '23', '-preset', 'medium',
                        '-af', f'volume={-16 - L - trim:.2f}dB,alimiter=limit=0.84:attack=2:release=50:level=disabled',
                        '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(out)], check=True)
        got = lufs(out)
        if abs(got + 16) <= 0.3:
            break
        trim += got + 16
    titles, desc = META[n]
    real = [it['src'] for it in SHORTS[n].get('real', [])]
    if any(r.startswith('his_') for r in real):  # Aly 2026-10-22: his own work on screen -> his Behance
        desc += '\n\nشغلي على Behance: be.net/shorosh'
    cr = json.loads((P / 'assets' / 'commons' / 'credits.json').read_text(encoding='utf8'))
    used = [cr[k] for k in dict.fromkeys(r[2:].rsplit('.', 1)[0] for r in real if r.startswith('c_')) if k in cr]
    if used:  # free Commons pictures: author + license (CC BY / BY-SA need the credit)
        desc += '\n\nصور من Wikimedia Commons:\n' + '\n'.join(f"- {c['artist'].strip()} ({c['license']})" for c in used)
    txt = 'العناوين:\n' + '\n'.join(f'{i + 1}) {t}' for i, t in enumerate(titles))
    txt += f'\n\nالوصف:\n{desc}\n\n{TAGS}\n\nكومنت مثبت:\n{PIN}\n'
    (P / 'output' / f'{name}.txt').write_text(txt, encoding='utf-8', newline='\n')
    print(f'{name}: raw {L:.1f} -> {got:.1f} LUFS, {out.stat().st_size / 1e6:.1f} MB')
