"""SFX stem for rough cut v6 (notes 1, 18, 32): glitch on the opening transitions, a soft whoosh on every sub-category card,
money (cash) on every price. Every sound separate: output/audio_stems_v10/sfx/sfx_timeline.wav, then the review mix voice + song + sfx.
Usage (project folder): python -X utf8 work/scripts/make_sfx_v5.py"""
import json, subprocess
from pathlib import Path
SFX = json.load(open("work/sfx_v10.json")); T5 = json.load(open("work/timeline_v10.json", encoding="utf-8")); TOTAL = T5["total"]
LIB = Path("../../motion-library/public/sfx"); GAIN = {"glitch": -6, "whoosh_2": -14, "cash": -10, "aly_show_sting": 0, "aly_transition_a": -8}
O = Path("output/audio_stems_v10/sfx"); O.mkdir(parents=True, exist_ok=True)
ins, fl = [], []
for i, (n, t) in enumerate(SFX):
    ins += ["-i", str(LIB / f"{n}.wav")]
    ms = max(0, int(round(t * 1000)) - (40 if n == "glitch" else 0))
    fl.append(f"[{i}]aresample=48000,aformat=channel_layouts=stereo,volume={(-3 if n.startswith("kids10_") else -2 if n == "audiobook_v10" else GAIN.get(n, -10))}dB,adelay={ms}|{ms}[s{i}]")
fl.append("".join(f"[s{i}]" for i in range(len(SFX))) + f"amix=inputs={len(SFX)}:normalize=0,apad,atrim=0:{TOTAL}[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fl), "-map", "[o]", "-c:a", "pcm_s24le", str(O / "sfx_timeline.wav")], check=True)
A = Path("output/audio_stems_v10")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(A / "voice_full_timeline.wav"), "-i", str(A / "music/song_C1_full_timeline.wav"), "-i", str(O / "sfx_timeline.wav"),
                "-filter_complex", "[0]pan=stereo|c0=c0|c1=c0[v];[1]volume=-3dB[s];[v][s][2]amix=inputs=3:normalize=0,alimiter=limit=0.95[o]",
                "-map", "[o]", "-c:a", "pcm_s16le", str(A / "mix_rough_v10.wav")], check=True)
print(len(SFX), "sfx:", {n: sum(1 for x in SFX if x[0] == n) for n in set(x[0] for x in SFX)})
