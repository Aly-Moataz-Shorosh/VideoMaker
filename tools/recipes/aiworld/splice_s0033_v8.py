import subprocess, numpy as np, sys
SR=48000
def load(f,a=None,b=None):
    args=["ffmpeg","-v","error"]+(["-ss",str(a),"-t",str(b-a)] if a is not None else [])+["-i",f,"-ac","1","-ar",str(SR),"-f","f32le","-"]
    return np.frombuffer(subprocess.run(args,capture_output=True).stdout,np.float32).copy()
s0=float(sys.argv[1]); out_f=sys.argv[2]
A=load("assets/ai/heygen/voice_fix_v6/S003.3_qeta.wav",0.0,0.86)
B=load("output/audio_stems_v2/voice_full_timeline.wav",s0,37.22)
r=lambda x: float(np.sqrt((x[np.abs(x)>0.01]**2).mean()))
B=B*(r(A)/r(B)); f=int(0.01*SR); A[-f:]*=np.linspace(1,0,f); B[:f]*=np.linspace(0,1,f); B[-f:]*=np.linspace(1,0,f)
out=np.concatenate([A,np.zeros(int(0.06*SR),np.float32),B,np.zeros(int(0.1*SR),np.float32)])
subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","-","-c:a","pcm_s24le",out_f],input=out.tobytes())
