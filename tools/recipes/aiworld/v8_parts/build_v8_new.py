import re, shutil
S = r"C:/Users/alymo/AppData/Local/Temp/claude/bb73d722f7120fff/7b3085e9-3ce7-493b-8129-f027dceaff53/scratchpad"
s = open("work/scripts/v7_new.py", encoding="utf-8").read()
for a, b in [("timeline_v7.json", "timeline_v8.json"), ("_words_v7_v2part", "_words_v8_v2part"), ("words_v7.json", "words_v8.json"),
             ("audio_stems_v7", "audio_stems_v8"), ("props_v7", "props_v8"), ("import v7_new", "import v8_new")]:
    s = s.replace(a, b)
A = open(S + "/v8_patch_a.py", encoding="utf-8").read(); B = open(S + "/v8_patch_b.py", encoding="utf-8").read(); C = open(S + "/v8_patch_c.py", encoding="utf-8").read()
k = "# ---------- v6 time -> v7 time"
s = s.replace(k, A + "\n" + k, 1)
C = C.replace("import glob as _g", "import glob as _g, os")
tail = '''
# generic (v7 notes 8a/16/25): a board whose end falls on a silent hold stays through the hold
for sp_ in SPECS:
    for p_ in T8P:
        if p_["kind"] == "hold" and p_["t"] - 0.8 <= sp_["b"] <= p_["t"] + 0.3: sp_["b"] = round(p_["t"] + p_["dur"] - 0.05, 3)
'''
s = s + "\n" + B + "\n" + C + tail
def R(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)
R('T8("اعمل", 737.2)', 'T8("اعمل", mBl + 1.0)'); R('T8("فيبني", 739.4)', 'T8("فيبني", mBl + 1.5)')
R('src=V8 + "f201_first.jpg"', 'src=V8 + "f032_first.jpg"'); R('src=V8 + "f201_last.jpg"', 'src=V8 + "f032_last.jpg"')
R('"3. الموديل بيعمل اللي في النص", src=CL + "clip_201_C11.mp4", w=360, size=22)', '"3. الموديل بيعمل اللي في النص", src=CL + "clip_032_C02b.mp4", w=360, loop=6, size=22)')
R('''for it in s["items"]:
    if it.get("label") == "ريل Genjutsu: داشبورد فيسبوك": it.update(x=1300, y=640, w=380)
    if it.get("k") == "num": it.update(x=1300, y=830)''', '''s["items"] = [it for it in s["items"] if it.get("label") != "ريل Genjutsu: داشبورد فيسبوك"]
for it in s["items"]:
    if str(it.get("src", "")).endswith("hf_genjutsu_len.png"): it.update(x=1350, y=380, w=440)
    if it.get("k") == "num": it.update(x=1350, y=720)''')
R('N(tco + 0.3, 960, 430, src=V8 + "claude_session_2x.mp4", w=420, ar=1280 / 1004, loop=8)', 'N(tco + 0.3, 960, 470, src=V8 + "claude_session_2x.mp4", w=290, ar=1280 / 1004, loop=8)')
R('N(tco + 0.6, 960, 640, "Claude Cowork · ChatGPT agent", size=18)', 'N(tco + 0.6, 960, 660, "Claude Cowork · ChatGPT agent", size=18)')
SK = 'TY({t}, {x}, {y}, "---\\nname: aly-video-motion\\ndescription: الموشن بأسلوب علي\\n---\\n1. اقرا رقم الستايل\\n2. متقصش كلمة", w=400, head="SKILL.md", size=16, dur=20)'
R('N(cS, 960, 330, "Skills: كراسات خبرة بيقراها لما يحتاجها", src=P6 + "claude_skill_row.jpg", w=380, size=18)', 'N(cS, 960, 300, "Skills: كراسات خبرة بيقراها لما يحتاجها", emo="notebook", size=18)')
R('N(T8("ملف", 783.0), 1400, 430, "ملف SKILL.md: الخطوات + القواعد + أمثلة", src=P6 + "claude_skill_row.jpg", w=440, size=20)',
  'N(T8("ملف", 783.0), 1400, 330, "ملف SKILL.md: الخطوات + القواعد + أمثلة", size=20), ' + SK.format(t='T8("ملف", 783.0) + 0.3', x=1400, y=400))
R('N(kIn + 1.8, 1450, 700, "الـ skill اتحفظت ✓", src=P6 + "claude_skill_row.jpg", w=380, size=20, good=True)', 'N(kIn + 1.8, 1450, 640, "الـ skill اتحفظت ✓", emo="check_mark_button", size=22, good=True)')
R('N(rSk, 1400, 420, "2. skill السكريبت بنفس الأسلوب", src=P6 + "claude_skill_row.jpg", w=380, size=20)', 'N(rSk, 1400, 330, "2. skill السكريبت بنفس الأسلوب", emo="writing_hand", size=20)')
R('N(mThis, 960, 560, "الفيديو ده نفسه: من جوه Claude بس.. من غير ما أفتح أي برنامج تاني", src=V8 + "claude_session_2x.mp4", w=600, ar=1280 / 1004, loop=10, size=20, good=True)',
  'N(mThis, 960, 610, "الفيديو ده نفسه: من جوه Claude بس.. من غير ما أفتح أي برنامج تاني", src=V8 + "claude_session_2x.mp4", w=500, ar=1280 / 1004, loop=10, size=20, good=True)')
R('N(rBuilt, 960, 250, "اللي اتبنى بـ Claude Code.. على الجهاز", logo=LG("claude.svg"), size=22)', 'N(rBuilt, 960, 250, "اللي اتبنى بـ Claude Code.. على الجهاز", emo="laptop", size=22)')
R('return [N(t, 960, 232, f"خطوة {i} من 11", size=26, bg="mustard", out=o)]', 'return [N(t, 960, 285, f"خطوة {i} من 11", size=26, bg="mustard", out=o)]')
R('[N(t + 0.05, 1460 - j * 100, 300, str(j + 1)', '[N(t + 0.05, 1460 - j * 100, 350, str(j + 1)')
s = s.replace("N(steps[3] + 0.2, 960, 580,", "N(steps[3] + 0.2, 960, 620,")
open("work/scripts/v8_new.py", "w", encoding="utf-8").write(s)
import ast; ast.parse(s); print("ok, parses")
