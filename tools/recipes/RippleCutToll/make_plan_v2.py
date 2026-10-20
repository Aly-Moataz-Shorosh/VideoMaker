# Writes plan.json cues for short_02 (Aly review v2). Anchors = source seconds in his edit (cue "src").
import json
p = json.load(open('plan.json', encoding='utf8'))
R = 'projects/2026-10-06 shorts RippleCutToll/rec_a.mp4'
D = [745, 398, 430, 250]  # 'Remove Silence' dialog crop


def z(src, to=1.15, st='punch', d=1.0):
    return {"t": "zoom", "src": src, "dur": d, "props": {"to": to, "style": st}}


def dlg(src, dur, marks, **kw):
    return {"t": "screen_ui", "src": src, "dur": dur, "props": {"src": R, "start": 50, "still": True, "crop": D,
                                                                 "width": 0.8, "top": 0.36, "marks": marks, **kw}}


p['note'] = "v2 (Aly review): cuts only in real pauses (snap_edges.py), CTA = last clean take whole, -20 dB, explainer diagrams. v1 = plan_v1.json"
p['fix'] = {"A1:S001": "لو عايز نسخة الفيديو على اليوتيوب اكتب في كومنت يوتيوب وهو هيبعتلك اللينك على طول"}
p['cues'] = [
    z(13.75, 1.22, 'punch', 1.3),
    {"t": "keyword_pop", "src": 13.75, "dur": 3.4, "props": {"text": "أصعب *مرحلة* في المونتاج", "accent": "gold"}},
    z(15.8, 1.12, 'push', 1.4),
    {"t": "icon_pop", "src": 15.9, "dur": 1.1, "props": {"icon": "😩", "x": 0.78, "y": 0.27}},
    {"t": "screen_ui", "src": 17.3, "dur": 3.15, "props": {"src": R, "start": 65, "still": True, "crop": [880, 650, 1000, 300],
                                                          "title": "مليانة *سكتات*", "top": 0.42}},
    z(19.2, 1.16, 'punch', 1.1),
    # seg 2: free DaVinci, tool, steps
    z(32.94, 1.12, 'push', 3.5),
    {"t": "side_picture", "src": 33.2, "dur": 1.7, "props": {"src": "logos/davinci-resolve.png", "caption": "DaVinci Resolve", "fit": "contain", "accent": "blue"}},
    {"t": "keyword_pop", "src": 34.9, "dur": 2.2, "props": {"text": "النسخة *المجانية*", "tag": "DaVinci Resolve", "accent": "gold"}},
    {"t": "icon_pop", "src": 37.3, "dur": 1.2, "props": {"icon": "🔥", "x": 0.78, "y": 0.27}},
    z(38.8, 1.18),
    z(39.64, 1.2),
    {"t": "screen_ui", "src": 39.64, "dur": 2.9, "props": {"src": R, "start": 69.1, "crop": [880, 650, 1000, 300],
                                                          "title": "بتشيل *كل* السكتات", "top": 0.42}},
    {"t": "icon_pop", "src": 41.5, "dur": 1.0, "props": {"icon": "⚡", "x": 0.8, "y": 0.3}},
    z(42.6, 1.14),
    {"t": "steps_list", "src": 43.3, "dur": 5.9, "props": {"items": ["نزّل DaVinci Resolve", "افتح البرنامج", "حط الفيديو"], "stagger": 70}},
    z(45.5, 1.12, 'push', 1.2), z(46.9),
    # seg 3: menu -> dialog -> threshold
    {"t": "screen_ui", "src": 56.9, "dur": 4.4, "props": {"src": R, "start": 14.87, "crop": [180, 0, 760, 400], "crop2": [300, 220, 820, 420],
                                                         "moveAt": 64, "moveDur": 18, "marks": [
        {"x": 318, "y": 2, "w": 56, "h": 28, "from": 26, "to": 64, "label": "Clip"},
        {"x": 325, "y": 341, "w": 322, "h": 26, "from": 70, "to": 9999, "label": "Audio Operations"}]}},
    z(61.3),
    {"t": "screen_ui", "src": 61.3, "dur": 4.3, "props": {"src": R, "start": 19.27, "crop": D, "width": 0.8, "top": 0.36, "title": "هيطلع لك *ده*",
                                                         "marks": [{"x": 753, "y": 402, "w": 413, "h": 26, "from": 6, "to": 9999, "label": ""}]}},
    z(63.6, 1.12, 'push', 1.2),
    {"t": "screen_ui", "src": 65.6, "dur": 6.4, "props": {"src": R, "start": 23.57, "crop": D, "width": 0.8, "top": 0.36,
                                                         "marks": [{"x": 765, "y": 447, "w": 400, "h": 28, "from": 10, "label": "Threshold = حد الصمت"}]}},
    z(67.4, 1.12, 'push', 1.2), z(69.3, 1.2, 'punch', 1.2),
    {"t": "threshold_wave", "src": 72.0, "dur": 7.38, "props": {"db": "-20 dB", "silenceAt": 66, "keepAt": 141, "collapseAt": 171}},
    {"t": "icon_pop", "src": 74.9, "dur": 1.0, "props": {"icon": "🤫", "x": 0.8, "y": 0.27}},
    z(74.9, 1.18, 'punch', 0.9),
    # seg 4 (from 80.61): above line = speech, pre/post, min strip
    z(81.4),
    dlg(84.1, 3.6, [{"x": 765, "y": 473, "w": 400, "h": 54, "from": 6, "label": "Pre head + Post tail"}]),
    z(84.15, 1.1, 'push', 1.7), z(86.4),
    {"t": "trim_handles", "src": 87.7, "dur": 7.2, "props": {"cutAt": 10, "preAt": 66, "postAt": 114, "closeAt": 144}},
    z(89.9, 1.12, 'push', 1.0), z(91.5),
    z(95.0),
    {"t": "counter", "src": 95.0, "dur": 3.0, "props": {"value": 3, "suffix": " فريم", "label": "اختيار علي: من 0 لـ 3", "accent": "blue"}},
    {"t": "keyword_pop", "src": 98.0, "dur": 2.1, "props": {"text": "عايز الفيديو *سريع*", "accent": "gold"}},
    {"t": "icon_pop", "src": 99.0, "dur": 1.0, "props": {"icon": "⚡", "x": 0.8, "y": 0.28}},
    dlg(100.2, 7.79, [{"x": 765, "y": 525, "w": 400, "h": 27, "from": 3, "to": 208, "label": "Minimum to strip"},
                      {"x": 1032, "y": 524, "w": 62, "h": 29, "from": 210, "to": 9999, "label": "5 فريم"}]),
    z(100.25, 1.1, 'push', 1.5), z(102.6), z(104.7, 1.12, 'push', 1.2), z(107.2, 1.18),
    # seg 5 (from 114.39): cross fade
    dlg(114.45, 2.95, [{"x": 765, "y": 550, "w": 400, "h": 26, "from": 25, "label": "Cross fade audio"}]),
    z(114.45, 1.1, 'push', 1.4), z(116.2),
    {"t": "audio_crossfade", "src": 117.4, "dur": 8.05, "props": {"overlapAt": 108, "doneAt": 150}},
    {"t": "icon_pop", "src": 118.5, "dur": 1.2, "props": {"icon": "🎧", "x": 0.8, "y": 0.27}},
    z(119.5, 1.12, 'push', 1.2), z(121.0), z(123.0, 1.12, 'push', 1.2), z(124.4),
    # seg 6: keep it ON
    z(130.35),
    {"t": "screen_ui", "src": 130.35, "dur": 2.3, "props": {"src": R, "start": 50, "still": True, "crop": D, "crop2": [820, 500, 340, 120],
                                                           "moveAt": 0, "moveDur": 18, "marks": [{"x": 885, "y": 550, "w": 200, "h": 26, "from": 8, "label": "خليها ON ✅"}]}},
    # CTA: last clean take, whole
    {"t": "zoom", "at": "A1:S001", "word": 7, "dur": 1.2, "props": {"to": 1.18, "style": "punch"}},
    {"t": "comment_cta", "at": "A1:S001", "word": 7, "dur": 4.82, "props": {"title": "", "top": 0.02, "keyword": "يوتيوب",
                                                                        "dm": "ده لينك الفيديو كامل 🎬", "typeAt": 49, "sendAt": 80, "dmAt": 105}},
    {"t": "zoom", "at": "A1:S001", "word": 13, "dur": 1.2, "props": {"to": 1.2, "style": "punch"}},
]
json.dump(p, open('plan.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(len(p['cues']), 'cues')
