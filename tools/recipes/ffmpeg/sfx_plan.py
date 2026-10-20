"""Sound design for the ffmpeg shorts (look 'pop', 2026-10-14). Library: motion-library/public/sfx (tools/make_sfx.py).
Per scene: list of (beat name | seconds from scene start, sfx, volume[, duration s, loop]).
Generic rules in make_shorts.py: whoosh on every scene, pop on every other beat, typing / pop / ding on the CTA card."""

SFX = {
    'f1_hook': [(0, 'impact', 0.5), ('kb', 'pop_2', 0.5), ('diff', 'swish', 0.45), ('sky', 'swoop_down', 0.55)],
    'f1_google': [('type', 'typing', 0.45, 0.6), ('ff', 'magic', 0.45)],
    'f1_site': [('dl', 'click', 0.7), ('want', 'buzz_wrong', 0.35), ('win', 'click', 0.7)],
    'f1_bin': [(0.1, 'paper', 0.4), ('all', 'tick', 0.4), ('exe', 'ding', 0.5)],
    'f1_what': [('press', 'swoop_down', 0.45), ('conv', 'magic', 0.4), ('easy', 'stamp', 0.6)],
    'f1_cmd': [('search', 'click', 0.7), ('type', 'typing', 0.45, 0.5), ('enter', 'click', 0.8)],
    'f1_line': [('name', 'typing', 0.45, 0.5), ('space', 'click', 0.8), ('space2', 'click', 0.6), ('dash', 'typing', 0.4, 0.3), ('i', 'pop_1', 0.45)],
    'f1_in': [(0.1, 'swoop_up', 0.4), ('drop', 'pop_3', 0.55), ('fmt', 'tick', 0.45)],
    'f1_trick': [('trick', 'riser', 0.35, 2.5), ('mov', 'buzz_wrong', 0.45), ('mp4', 'impact', 0.55)],
    'f1_enter': [('enter', 'click', 0.9), ('enter', 'impact', 0.5)],
    'f1_end': [(0, 'typing', 0.35, 0.6), ('kb', 'pop_2', 0.5), ('mb', 'swoop_up', 0.45), ('diff', 'ding', 0.55)],
}
