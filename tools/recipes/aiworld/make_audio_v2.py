"""Audio for rough cut v2 (every sound separate, same length as the video, all start at 0):
output/audio_stems_v2/
  voice_full_timeline.wav          = voice_v1_timeline.wav with +EXTRA s of silence inserted at the end of the old music slot
  music/song_C1_full_timeline.wav  = the song (C1) at the start of C11, silence elsewhere
  music/song_C1_vocals_timeline.wav / song_C1_music_only_timeline.wav = its two stems placed the same way
  mix_rough_v2.wav                 = voice + song (song -3 dB so it sits near the voice level) -> only for the rough cut
Usage (project folder): python -X utf8 work/scripts/make_audio_v2.py"""
import json, subprocess
from pathlib import Path

m = json.load(open("work/rough_v2_map.json", encoding="utf-8"))
S0, EXTRA, TOTAL = m["song_start"], m["extra"], m["total"]
S1 = S0 + 180.0
O = Path("output/audio_stems_v2"); (O / "music").mkdir(parents=True, exist_ok=True)
SR = 48000

def run(args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)

# voice: [0,S1] + silence EXTRA + [S1,end], 48 kHz mono 24-bit
run(["-i", "work/voice_v1_timeline.wav", "-filter_complex",
     f"[0]aresample={SR},asplit[a][b];[a]atrim=0:{S1},asetpts=N/SR/TB[a1];[b]atrim={S1},asetpts=N/SR/TB[b1];"
     f"anullsrc=r={SR}:cl=mono,atrim=0:{EXTRA}[z];[a1][z][b1]concat=n=3:v=0:a=1,apad,atrim=0:{TOTAL}[o]",
     "-map", "[o]", "-c:a", "pcm_s24le", str(O / "voice_full_timeline.wav")])
# song + stems on the timeline (stereo 48 kHz)
src = {"song_C1_full": "output/audio_stems_v1/music/song_C1_full.wav",
       "song_C1_vocals": "output/audio_stems_v1/music/song_C1_vocals.wav",
       "song_C1_music_only": "output/audio_stems_v1/music/song_C1_music_only.wav"}
ms = int(round(S0 * 1000))
for name, f in src.items():
    run(["-i", f, "-af", f"aresample={SR},adelay={ms}|{ms},apad,atrim=0:{TOTAL}", "-c:a", "pcm_s24le",
         str(O / "music" / f"{name}_timeline.wav")])
# rough-cut mix
run(["-i", str(O / "voice_full_timeline.wav"), "-i", str(O / "music" / "song_C1_full_timeline.wav"), "-filter_complex",
     "[0]pan=stereo|c0=c0|c1=c0[v];[1]volume=-3dB[s];[v][s]amix=inputs=2:normalize=0,alimiter=limit=0.95[o]",
     "-map", "[o]", "-c:a", "pcm_s16le", str(O / "mix_rough_v2.wav")])
# chapter starts on the new timeline (the chapter wav files are the same as v1: output/audio_stems_v1/voice_chapters/)
p = json.load(open("work/props_rough_v2_720.json", encoding="utf-8"))
mm = lambda x: f"{int(x) // 60}:{int(x) % 60:02d}"
(O / "chapters_v2.txt").write_text("\n".join(f"{mm(c['start'])} {c['id']} {c['title']}" for c in p["chapters"]) + "\n", encoding="utf-8")
print("ok", TOTAL)
