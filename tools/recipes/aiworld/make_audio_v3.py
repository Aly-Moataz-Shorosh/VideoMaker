"""Audio v3 = v2 stems with the two re-voiced sentences («كلام مكتوب», S007.2 + S009.2) put in place of the old ones
(work/timeline_v3_shift.json from make_props_v3.py); everything after each one moves by its delta. Every sound separate:
output/audio_stems_v3/voice_full_timeline.wav, music/song_C1_*_timeline.wav, mix_rough_v3.wav (review only).
Usage (project folder): python -X utf8 work/scripts/make_audio_v3.py"""
import json, subprocess
from pathlib import Path

SR = 48000
sh = sorted(json.load(open("work/timeline_v3_shift.json", encoding="utf-8")), key=lambda x: x["v2_start"])
m2 = json.load(open("work/rough_v2_map.json", encoding="utf-8"))
total = m2["total"] + sum(x["delta"] for x in sh)
O = Path("output/audio_stems_v3"); (O / "music").mkdir(parents=True, exist_ok=True)
run = lambda a: subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)

# voice: cut v2 voice at the old sentences, put the new trimmed sentences in, concat
src = "output/audio_stems_v2/voice_full_timeline.wav"
ins, flt, cur, k = ["-i", src], [], 0.0, 0
for i, x in enumerate(sh):
    ins += ["-i", x["file"]]
    flt.append(f"[0]atrim={cur}:{x['v2_start']},asetpts=N/SR/TB,aresample={SR}[p{k}]"); k += 1
    a, b = x["trim"]
    flt.append(f"[{i + 1}]atrim={a}:{b},asetpts=N/SR/TB,aresample={SR},aformat=channel_layouts=mono[p{k}]"); k += 1
    cur = x["v2_end"]
flt.append(f"[0]atrim={cur},asetpts=N/SR/TB,aresample={SR}[p{k}]"); k += 1
flt.append("".join(f"[p{i}]" for i in range(k)) + f"concat=n={k}:v=0:a=1,apad,atrim=0:{total}[o]")
run(ins + ["-filter_complex", ";".join(flt), "-map", "[o]", "-c:a", "pcm_s24le", str(O / "voice_full_timeline.wav")])

# song (all three stems) moved by the total shift (it starts after both sentences)
s0 = m2["song_start"] + sum(x["delta"] for x in sh)
ms = int(round(s0 * 1000))
for n in ("song_C1_full", "song_C1_vocals", "song_C1_music_only"):
    run(["-i", f"output/audio_stems_v1/music/{n}.wav", "-af", f"aresample={SR},adelay={ms}|{ms},apad,atrim=0:{total}", "-c:a", "pcm_s24le",
         str(O / "music" / f"{n}_timeline.wav")])
run(["-i", str(O / "voice_full_timeline.wav"), "-i", str(O / "music/song_C1_full_timeline.wav"), "-filter_complex",
     "[0]pan=stereo|c0=c0|c1=c0[v];[1]volume=-3dB[s];[v][s]amix=inputs=2:normalize=0,alimiter=limit=0.95[o]", "-map", "[o]",
     "-c:a", "pcm_s16le", str(O / "mix_rough_v3.wav")])
print("ok total", round(total, 3), "song at", round(s0, 3))
