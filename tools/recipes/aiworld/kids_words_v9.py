import sys, json, subprocess, numpy as np
from faster_whisper import WhisperModel
m=WhisperModel(str(__import__("pathlib").Path.home()/"ai-models"/"faster-whisper-large-v3-turbo"),device="cpu",compute_type="int8",cpu_threads=10)
R={}
for v in sys.argv[1:]:
    segs,_=m.transcribe(np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f"kids_{v}.mp3","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32),language="ar",word_timestamps=True,vad_filter=False,beam_size=5)
    W=[{"w":w.word.strip(),"a":round(w.start,2),"b":round(w.end,2)} for s in segs for w in s.words]
    R[v]=W; print(v," | ".join(f"{x['w']}@{x['a']}" for x in W))
json.dump(R,open("words.json","w",encoding="utf-8"),ensure_ascii=False)
