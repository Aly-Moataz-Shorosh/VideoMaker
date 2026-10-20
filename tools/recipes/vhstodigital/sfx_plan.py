"""Sound design for the vhstodigital shorts (2026-10-09). Library: motion-library/public/sfx (tools/make_sfx.py).
Per scene: list of (beat name | seconds from scene start, sfx, volume[, duration s, loop]).
Generic rules in make_shorts.py: whoosh on every full-screen scene, swish on scenes behind Aly, pop on every other beat,
whoosh when Aly pops in, impact on the hook, typing / pop / ding on the CTA comment card."""

SFX = {
    'v1_hook': [('stamp', 'stamp', 0.75)],
    'v1_idea': [(0, 'tape', 0.5), ('cam', 'click', 0.6), ('pc', 'ding', 0.45)],
    'v1_hours': [(0, 'clock', 0.35, 4.0, True), ('n', 'tick', 0.5), ('copy', 'buzz_wrong', 0.5)],
    'v1_convert': [('rca', 'click', 0.7), ('box', 'magic', 0.4), ('hdmi', 'click', 0.7)],
    'v1_why': [('no', 'buzz_wrong', 0.55), ('cap', 'magic', 0.45)],
    'v1_chain': [('vcr', 'tape', 0.5), ('av', 'click', 0.6), ('conv', 'click', 0.6), ('hdmi', 'click', 0.6), ('cap', 'click', 0.6),
                 ('usb', 'click', 0.6), ('pc', 'ding', 0.55)],
    'v1_result': [(0, 'crackle', 0.25, 5.5, True), ('color', 'magic', 0.45)],
    'v2_shop': [('give', 'swoop_up', 0.45), ('give', 'cash', 0.6), ('done', 'stamp', 0.75), ('costly', 'coins', 0.5)],
    'v2_price': [('now', 'cash', 0.6), ('many', 'coins', 0.55)],
    'v2_privacy': [('eyes', 'shh', 0.45), ('lock', 'click', 0.8)],
    'v2_home': [('best', 'ding', 0.5)],
    'v4_easy': [('usb', 'click', 0.7)],
    'v4_problem': [(0, 'glitch', 0.4), ('bw', 'buzz_wrong', 0.45), ('cut', 'glitch', 0.5)],
    'v4_versus': [(0, 'glitch', 0.35), ('x', 'buzz_wrong', 0.5), ('win', 'ding', 0.55), ('win', 'stamp', 0.6)],
    'v1_end': [],
    'v8_real': [(0, 'tape', 0.5), ('fall', 'door_slam', 0.5)],
    'v8_box': [(0, 'rustle', 0.45), ('copy', 'stamp', 0.75)],
    'v8_play': [(0, 'tape', 0.55), (0.4, 'crackle', 0.25, 4.0, True)],
    'v8_save': [('dig', 'magic', 0.5), ('fam', 'ding', 0.45)],
    'v8_end': [(0.4, 'strings', 0.4)],
    'vt': [('stamp', 'stamp', 0.7)],
}
