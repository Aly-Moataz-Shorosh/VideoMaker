# Short 08 from his 2 phone recordings (Aly 2026-11-07: "تاخد الفيديو اللي انا ادتهولك تستخدمه احسن") — same builder, other voice source.
#   python make_f08.py   -> work/shorts/props_08.json
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_fshorts as M
import fs_data as SD
M.SRC = M.PROJ / 'input/20261107_075352.mp4'
M.VOICE = 'rec08_720.mp4'
M.DB_CACHE = 'work/rec_075352/db10.npy'
_t = json.load(open(M.PROJ / 'work/rec_075352/transcript.json', encoding='utf-8'))
M.EPW = [(w['w'].strip(), w['start'], w['end']) for s_ in _t['sentences'] for w in s_['words'] if w['w'].strip()]
M._db.clear()
M.build(8)
