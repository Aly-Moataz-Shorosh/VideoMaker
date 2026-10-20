"""REVIEW 2026-10-19 (Aly: "حلو اوي اوي ممتاز" + notes on 7 9 10 11 12 14 15 16 19 21 22 23 25 26 27 28 29 30).
Applied on top of shorts_data.SHORTS (imported at the end of shorts_data.py). Old versions: output/v3/archive/.
Media = motion-library/public/projects/newstage19/media (prep_media.py)."""


def apply(SHORTS):
    def rep(n, src, kind, new):
        """replace the cue of short n that starts at src (and has that kind) by `new` (list of cue tuples)"""
        cs = SHORTS[n]['cues']
        i = next(j for j, c in enumerate(cs) if abs(c[0] - src) < 0.05 and c[1] == kind)
        cs[i:i + 1] = new

    H = {'_hook': True}

    # 9 — balls on every "دي كورة", a real 3D ball the mouse drags materials onto, one bear in 3 renders, WING IT! (looks 2D, is 3D)
    balls = {'items': [{'file': f'ball_{k}.jpg'} for k in ('glass', 'melon', 'gravel', 'grass', 'honey')], 'size': 280, 'cols': 3, 'round': True}
    beats = {'p0': 2517.85, 'p1': 2518.64, 'p2': 2519.4, 'p3': 2519.85, 'p4': 2520.2}
    SHORTS[9]['cues'][1:1] = [(2517.1, 'pics', {**balls, **H}, dict(beats))]
    rep(9, 2516.1, 'slide', [(2516.1, 'pics', {**balls, 'title': 'Material'}, dict(beats))])
    rep(9, 2525.3, 'list', [(2525.3, 'mat3d', {}, {'color': 2528.0, 'metal': 2529.6, 'glass': 2534.9, 'melon': 2535.5, 'honey': 2536.3, 'rock': 2537.6})])
    rep(9, 2562.1, 'flow', [(2562.1, 'looks3d', {}, {'ad': 2564.2, 'toy': 2565.8, 'cine': 2568.4})])
    rep(9, 2569.9, 'slide', [(2572.6, 'slide', {'n': 108, 'w': 1000, 'label': 'Rendering'}, {})])
    rep(9, 2581.0, 'big', [(2581.0, 'clip', {'file': 'wingit_cat.mp4', 'label': 'WING IT! · Blender Studio (CC BY)'}, {}),
                           (2584.8, 'clip', {'file': 'wingit_blender.mp4', 'label': 'ده جوه Blender: 3D'}, {})])

    # 10 — the meme on "أعمل كذا وأقعد أتفرج"
    SHORTS[10]['cues'] = [c for c in SHORTS[10]['cues'] if not (c[1] == 'big' and abs(c[0] - 1095.3) < 0.05)]
    SHORTS[10]['cues'] += [(1090.9, 'clip', {'file': 'meme_c19.mp4', 'w': 640, 'h': 640}, {}),
                           (1097.4, 'big', {'text': 'الكود بقى *مينيمم*', 'top': 'robot'}, {})]

    # 11 — the game he talks about = Bonto (his slide 62)
    bonto = {'items': [{'file': 'bonto_logo.jpg', 't': 'بونطو'}, {'file': 'bonto_game.jpg'}], 'size': 300}
    SHORTS[11]['cues'][1:1] = [(1694.0, 'pics', {**bonto, **H}, {'p0': 1694.3, 'p1': 1694.9})]
    SHORTS[11]['cues'].append((1694.0, 'pics', bonto, {'p0': 1694.3, 'p1': 1694.9}))

    # 14 — Uber without / with UI (his slide videos), the real burger and the duck feast
    rep(14, 1166.4, 'hero', [(1166.4, 'clip', {'file': '032_media3.mp4', 'from': 2, 'label': 'Uber من غير UI'}, {})])
    rep(14, 1176.2, 'hero', [(1176.2, 'clip', {'file': '033_media4.mp4', 'from': 2, 'label': 'Uber بالـ UI'}, {})])
    rep(14, 1180.4, 'vs', [(1180.4, 'pics', {'items': [{'file': 'burger.jpg', 't': 'برجر'}, {'file': 'duck_feast.jpg', 't': 'محشي وبط'}], 'size': 330},
                            {'p0': 1186.2, 'p1': 1188.4})])
    rep(14, 1207.0, 'hero', [(1207.0, 'pic', {'file': 'burger.jpg', 'w': 860, 'h': 570, 'label': 'في الشارع؟ برجر'}, {})])
    rep(14, 1217.5, 'vs', [(1217.5, 'pics', {'items': [{'file': 'duck_feast.jpg', 't': 'UI: طعمه أحلى'}, {'file': 'burger.jpg', 't': 'UX: تاكله وإنت ماشي'}],
                                             'size': 330}, {'p0': 1218.8, 'p1': 1221.6})])

    # 15 — his slide videos for every way to cut/paste, his heart + watch and QR + map pictures (motion stays between them)
    rep(15, 1375.4, 'flow', [(1375.4, 'clip', {'file': '041_media5.mp4', 'from': 3, 'label': 'Command'}, {}),
                             (1379.9, 'clip', {'file': '042_media6.mp4', 'from': 1, 'label': 'Cut · Paste'}, {}),
                             (1384.8, 'clip', {'file': '043_media7.mp4', 'from': 2, 'label': 'Drag'}, {})])
    rep(15, 1386.5, 'flow', [(1386.5, 'clip', {'file': '044_media8.mp4', 'from': 5, 'label': 'لمسة'}, {}),
                             (1392.1, 'pic', {'file': 'touch_voice.jpg', 'w': 980, 'h': 470, 'fit': 'contain', 'label': 'بالكلام'}, {})])
    rep(15, 1401.9, 'hero', [(1401.9, 'pic', {'file': 'heart_ecg.jpg', 'w': 980, 'h': 470, 'fit': 'contain', 'label': 'نبضات القلب'}, {})])
    rep(15, 1432.3, 'hero', [(1430.7, 'pic', {'file': 'qr_map.jpg', 'w': 980, 'h': 470, 'fit': 'contain', 'label': 'QR كود · خريطة'}, {})])

    # 19 — real VR / AR clips (CC), the commentator clips under the hook and 38–54 with his note
    note = 'انا مليش في الكورة بس انا والله بحبك اوي يا استاذ ابراهيم ربنا يزيدك من فضله يارب ♥️'
    rep(19, 1988.8, 'hero', [(1988.8, 'clip', {'file': 'vr_headset.mp4', 'label': 'VR'}, {}),
                             (1994.6, 'clip', {'file': 'vr_world.mp4', 'label': 'Virtual Reality'}, {})])
    rep(19, 2000.0, 'hero', [(1999.9, 'clip', {'file': 'ar_spider.mp4', 'label': 'AR', 'w': 600, 'h': 760}, {}),
                             (2004.0, 'hero', {'e': 'mobile_phone', 't': 'زي Pokémon GO'}, {})])
    SHORTS[19]['cues'][1:1] = [(2040.14, 'clip', {'file': 'ibrahim_a.mp4', 'from': 5, 'note': note, **H}, {})]
    rep(19, 2037.2, 'big', [(2037.2, 'clip', {'file': 'ibrahim_a.mp4', 'note': note}, {}), (2048.2, 'clip', {'file': 'ibrahim_b.mp4', 'note': note}, {})])

    # 21 — his real "8 years ago" video (After Effects -> Code) + QR, the SHADER site video that was playing, his exact words
    rep(21, 1564.3, 'slide', [(1564.3, 'thumbs', {'items': [{'file': 'yt_5C4KNFiJFjA.jpg', 't': 'After effects animation to a Code'}], 'cols': 1,
                                                  'qr': 'qr_ae2code.png', 'title': 'الفيديو اللي عملته'}, {})])
    rep(21, 1596.0, 'big', [(1596.0, 'clip', {'file': '056_media13.mp4', 'from': 2, 'label': 'الكواليتي اللي لازم تطلّعها'}, {})])
    for i, c in enumerate(SHORTS[21]['cues']):
        if c[1] == 'list':
            SHORTS[21]['cues'][i] = (c[0], 'list', {'items': [{'e': 'straight_ruler', 't': 'تظبط الـ Div'}, {'e': 'level_slider', 't': 'تعلّي الـ Width'},
                                                              {'e': 'memo', 't': 'تعمل الـ Border'}]}, c[3])
        if c[1] == 'big' and 'الشطارة' in c[2]['text']:
            SHORTS[21]['cues'][i] = (c[0], 'big', {'text': 'الشطارة دلوقتي: *مهندس* بيترجم', 'top': 'man_technologist'}, {})

    # 22 — ONE map that flies Egypt -> Germany -> USA
    rep(22, 1847.0, 'flow', [(1847.0, 'map', {}, {'s0': 1847.0, 's1': 1850.3, 's2': 1857.7})])

    # 23 — the channel's real videos, the graphics ones circled
    rep(23, 1967.0, 'list', [(1966.8, 'thumbs', {'items': [{'file': 'yt_Ae9q7KsRbuI.jpg', 'mark': True}, {'file': 'yt_uO5cvkzh3P0.jpg', 'mark': True},
                                                           {'file': 'yt_zJvN8PDX1is.jpg', 'mark': True}, {'file': 'yt_eVBJIUxv8N8.jpg'}], 'qr': 'qr_2mp.png',
                                                 'title': 'Two Minute Papers'}, {'mark': 1969.5})])

    # 26 — explain pixels vs vectors, what a video is, a 3D object that turns, a real 3D printer
    rep(26, 768.2, 'slide', [(768.2, 'pixvec', {}, {'zoom': 770.1})])
    rep(26, 775.5, 'hero', [(775.5, 'flipbook', {}, {'play': 776.0})])
    rep(26, 777.4, 'hero', [(777.4, 'rot3d', {}, {'spin': 783.8})])
    rep(26, 785.8, 'hero', [(785.8, 'clip', {'file': 'printer3d.mp4', 'label': '3D Printing'}, {})])

    # 28 — stronger hook (one plane -> video, picture, game), his plane video + QR, his game, Behance pictures, the design photo
    #      (zoom on the plane, then out), the famous tutorial playlist + QR, his "هو ايه" 3D episodes + QR
    SHORTS[28]['head'] = 'طيارة واحدة عملتها.. بقت *فيديو* وصورة ولعبة'
    SHORTS[28]['hook'] = (2602.7, 2610.6)
    SHORTS[28]['cues'] = [
        (2602.7, 'hall', {}, {}),
        (2602.8, 'pic', {'file': 'behance_2.jpg', 'w': 960, 'h': 540, **H}, {}),          # 2nd review: the plane INSIDE the 3D program
        (2606.9, 'clip', {'file': 'plane_close.mp4', 'qr': 'qr_plane.png', **H}, {}),
        (2608.0, 'pic', {'file': 'plane_design.jpg', 'from': [27, 76, 3.2], 'to': [50, 50, 1], **H}, {'z0': 2608.4, 'z1': 2609.6}),
        (2609.8, 'clip', {'file': 'plane_game.mp4', **H}, {}),
        (2240.7, 'slide', {'n': 87, 'w': 1000, 'label': '3D Printing'}, {}),
        (2602.7, 'slide', {'n': 109, 'w': 1000, 'label': 'من البريزنتيشن'}, {}),        # 2nd review: the slide he showed
        (2606.9, 'clip', {'file': 'plane_close.mp4', 'label': 'طبّقتها في فيديو', 'qr': 'qr_plane.png'}, {}),
        (2608.0, 'pic', {'file': 'plane_design.jpg', 'label': 'في صورة', 'from': [27, 76, 3.2], 'to': [50, 50, 1]}, {'z0': 2608.4, 'z1': 2609.6}),
        (2609.8, 'clip', {'file': 'plane_game.mp4', 'label': 'في جيم'}, {}),
        (2614.3, 'hero', {'e': 'video_game', 't': 'مشروع مادة في الكلية'}, {}),
        (2619.7, 'thumbs', {'items': [{'file': 'yt_j48LtUkZRjU.jpg', 't': 'How to make a Video Game'}, {'file': 'yt_IlKaB1etrik.jpg', 't': 'BASICS (E01)'}],
                            'qr': 'qr_brackeys.png', 'title': 'الجيم الأشهر في الـ Tutorials'}, {}),
        (2636.8, 'thumbs', {'items': [{'file': f'yt_{v}.jpg'} for v in ('Ag22uTUIvPo', 'owZdBNisOpA', '2_PwpcOQQyE', 'tCV5jp5jZsE', 'ssB6HYUIR4w', 'a6QAqmP51TQ')],
                            'cols': 3, 'qr': 'qr_howayh.png', 'title': 'مفاهيم الـ 3D · هو ايه'}, {}),
        (2652.0, 'vs', {'a': {'e': 'money_bag', 't': 'برامج 3D', 'sub': 'غالية', 'ok': False}, 'b2': {'e': 'logo:blender', 't': 'Blender', 'sub': 'ببلاش', 'ok': True}},
         {'a': 2652.0, 'ma': 2652.7, 'b': 2653.8, 'mb': 2654.3}),
    ]

    # 29 — the slide he showed was 123
    rep(29, 2900.0, 'slide', [(2900.0, 'slide', {'n': 123, 'w': 1000, 'label': 'شوت واحد = شغلانات كتير'}, {})])

    # 30 — his own AI videos on YouTube (+ QR)
    SHORTS[30]['cues'].append((3008.0, 'thumbs', {'items': [{'file': f'yt_{v}.jpg'} for v in ('H5oOZypINf0', '10UXB0cT4Ss', '8d4jkySoXe4', 'gSewGtCDhHY')],
                                                  'qr': 'qr_ai_start.png', 'title': 'فيديوهاتي عن الـ AI'}, {}))
