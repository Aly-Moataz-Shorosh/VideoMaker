p = "work/scripts/make_timeline_v8.py"; s = open(p, encoding="utf-8").read()
def R(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)
R('"""Timeline v7 = v6 +', '"""Timeline v8 = v7 + Aly\'s v7 notes 1, 7, 16, 20, 21, 25, 37, 41, 45, 48 (see review_rough_v7_notes.md). Was: Timeline v7 = v6 +')
R('"S003.3": "assets/ai/heygen/voice_fix_v7/S003.3_fix.wav"', '"S003.3": "assets/ai/heygen/voice_fix_v8/S003.3_v8.wav"')
R('"S009.2": "assets/ai/heygen/voice_fix_v1/S009.2_kalam_maktoob.wav"', '"S009.2": "assets/ai/heygen/voice_fix_v8/S009.2a.wav"')
R('"S016.5": F6 + "S016.5_3d.wav"', '"S016.5": "assets/ai/heygen/voice_fix_v8/S016.5_gs.wav"')
R('NEW = {"N1": F6 + "N1_llm_agent.wav"', 'TAIL = {"S009.2b": "assets/ai/heygen/voice_fix_v8/S009.2b.wav"}   # note 7: «وأقوى حاجة:» starts the NEXT part, after the hold\nNEW = {"N1": F6 + "N1_llm_agent.wav"')
R('KEEP = {"S034.4": (626.80, 629.42), "S036.6": (666.30, 669.02)}', 'KEEP = {"S034.4": (627.53, 629.42), "S036.6": (666.30, 669.02), "S041.7": (761.50, 764.02)}   # v8: 37 (no «ب و» before «تحويل»), 48 (no PowerShell)\nEXACT = {"S034.4", "S041.7"}')
R('DROP = {"S006.9", "S032.1", "S032.2", "S032.3", "S032.4", "S032.5", "S035.4", "S036.2"}', 'DROP = {"S006.9", "S032.1", "S032.2", "S032.3", "S032.4", "S032.5", "S035.4", "S036.2", "S042.7", "S042.8"}   # v8 note 41: no .mcp.json / /mcp')
# order moves: 20 (Blender by code -> MCP), 45 («the video was made with» -> end of MCP)
R('+ [SEP(0, "3D")] + ids("S016.1", "S017.4")', '+ [SEP(0, "3D")] + ["S016.1", "S016.2", "S016.5"] + ids("S017.1", "S017.4")')
R('+ [SEP(3, "الـ MCP")] + ["S035.1", "S035.2", "N2"] + ids("S035.3", "S035.7")', '+ [SEP(3, "الـ MCP")] + ["S035.1", "S035.2", "N2"] + ["S035.3", "S035.4", "S016.3", "S016.4"] + ids("S035.5", "S035.7") + ids("S031.1", "S031.3")')
R('+ [SEP(4, "الفيديو ده اتعمل بإيه")] + ids("S031.1", "S031.3")', '')
R('ids("S009.1", "S010.7")', '["S009.1", "S009.2", "S009.2b"] + ids("S009.3", "S010.7")')
R('missing = [k for k in S if k not in used and k not in DROP]', 'missing = [k for k in S if k not in used and k not in DROP]   # (S009.2b is a tail piece, not a sentence id)')
R('HOLD_AFTER = {"S009.2": 1.0, "S009.3": 1.8, "S009.5": 1.8}', 'HOLD_AFTER = {"S009.2": 2.0, "S009.3": 1.8, "S009.5": 2.2, "S012.9": 2.0, "S025.5": 2.5}   # v8 notes 7, 8, 9, 16, 25')
R('FIRST_SEP, SEP_DUR = 4.43, 2.6', 'FIRST_SEP, SEP_DUR = 3.2, 3.0   # v8 note 3: the tree is already drawn, stays a bit longer (no sting)')
R('''    if x in NEW:''', '''    if x in TAIL:
        ta, tb = file_span(TAIL[x]); pieces.append({"kind": "file", "f": TAIL[x], "a": ta, "b": tb, "sids": [x]}); continue
    if x in NEW:''')
R('''    p["a"] = snap(p["a"] - 0.08, 0.12 if p.get("fixed") else 0.3, 0.12); p["b"] = snap(p["b"] + 0.08, 0.12, 0.12 if p.get("fixed") else 0.35)''',
  '''    if p["sids"][0] in EXACT: continue   # measured by hand on the waveform (v8 notes 37, 48)
    p["a"] = snap(p["a"] - 0.08, 0.12 if p.get("fixed") else 0.3, 0.12); p["b"] = snap(p["b"] + 0.08, 0.12, 0.12 if p.get("fixed") else 0.35)''')
open(p, "w", encoding="utf-8").write(s); print("ok")
