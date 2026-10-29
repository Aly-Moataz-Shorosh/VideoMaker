# Aly 2026-10-27: "8 حاسه ممل و مش مفيد كفاية", "9 كان ممكن تعمل انيميشن يشرح بشكل احسن" -> every sentence of 08 (Hz) and 09 (sample rate)
# gets a full-screen Blender explainer (tools/blender/sound_scenes.py hz_* / sr_*, clips public/projects/audio/b3d/p_<scene>.webm), Arabic
# words as tags under the 3D (y 1190 = above the captions, one at a time: at/out frames). 09's last sentence stays on his own slide (low vs high sample rate).
def _clip(scene, *tags):
    return dict(file=f'projects/audio/b3d/p_{scene}.webm', full=True,
                tags=[dict(text=t, y=1190, at=a, out=o, c=c) for t, a, o, c in tags])

CLIPS = {  # (short, piece start a) -> (scene, tags (text, at frame, out frame or None, colour or None))
    (8, 1482.0): ('hz_b', [('عدد الموجات اللي بتعدي في ثانية', 45, 270, None)]),  # gone before the 3D writes '3 Hz' at the same height
    (8, 1458.6): ('hz_a', [('الموليكيولز بتقرب وتبعد = موجة', 30, 380, None), ('من قمة لقمة = موجة واحدة', 400, None, 'gold')]),
    (8, 1499.0): ('hz_c', [('الفيديو: صور في الثانية', 30, 320, None), ('الصوت: موجات في الثانية', 330, None, 'gold')]),
    (8, 1543.7): ('hz_d', [('قفلة + فتحة = سايكل', 75, 300, None), ('موجة بطيئة.. وموجة سريعة', 320, 400, None), ('البني آدم ليه رينج بيسمعه', 410, None, 'gold')]),
    (9, 1604.1): ('sr_b', [('الكاميرا بتلقط لقطات من الحركة', 270, 500, None), ('ولقطات من الموجة = Sample rate', 510, None, 'gold')]),
    (9, 1566.5): ('sr_a', [('الموجة حاجة متصلة.. مش أرقام', 30, 280, None), ('نقسمها مربعات', 295, 470, None), ('كل لقطة = رقم', 600, 820, None), ('الصوت بقى أرقام', 830, None, 'gold')]),
    (9, 1627.8): ('sr_c', [('لقطات أكتر = دقة أكتر', 30, None, 'gold')]),
    (9, 1653.6): ('sr_d', [('أقل حاجة: نقطتين', 220, 330, None), ('واحدة فوق.. وواحدة تحت', 345, None, 'gold')]),
}
HOOK_FIRST = {8: 1482.0, 9: 1604.1}  # the counting (1, 2, 3 = Hz) / the camera shots come first


def patch(SHORTS, CAP):
    for (n, a), (scene, tags) in CLIPS.items():
        p = next(p for p in SHORTS[n]['pieces'] if abs(p['a'] - a) < 0.05)
        for k in ('crop', 'zoom', 'clicks', 'src', 'kw', 'lab', 'labels', 'anim'): p.pop(k, None)
        p['show'] = 'BlenderClip'; p['anim'] = _clip(scene, *tags)
    for n, a in HOOK_FIRST.items():
        ps = SHORTS[n]['pieces']; k = next(i for i, p in enumerate(ps) if abs(p['a'] - a) < 0.05)
        if k:
            ps.insert(0, ps.pop(k)); CAP[n].insert(0, CAP[n].pop(k))
