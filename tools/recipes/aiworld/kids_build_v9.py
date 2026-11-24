# cut each name from the 3 kid voices (whisper word times), layer them into a crowd + cheer -> kids_NN.wav
import json, subprocess, numpy as np
SR=48000
NAMES=['الصور','الفيديو','الأفاتار','الصوت','المزيكا','3D','مواقع التوليد','ElevenLabs','Higgsfield','Suno','على جهازك ببلاش','يعني إيه LLM و agent','الـ AI اللي بيفهم','Claude','Codex','الموديلات الصيني','الـ agents بتشتغل إزاي','السكريبتات','الـ MCP','الـ skills','تجربة حقيقية','خطوة بخطوة','تريكات','الأسعار','دور الإنسان','علامة الـ AI','الأغنية','OPEN']
NW={'piku':[1,1,1,1,1,1,2,2,1,1,3,4,4,1,1,2,3,1,2,1,2,2,1,1,2,3,1,7],
    'mini':[1,1,1,1,1,1,2,2,1,1,3,4,4,1,1,2,3,1,2,1,2,2,1,1,2,3,1,7],
    'mishi':[1,1,1,1,1,1,2,2,1,1,3,4,3,1,1,2,3,1,1,1,2,2,1,1,2,2,1,6]}
W=json.load(open('words.json',encoding='utf-8'))
def load(f): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout,np.float32).copy()
def pitch(x,semi):
    r=2**(semi/12); idx=np.arange(0,len(x)-1,r); return np.interp(idx,np.arange(len(x)),x).astype(np.float32)
A={v:load(f'kids_{v}.mp3') for v in NW}; cheer=load('cheer_a.mp3')
def env(x): w=int(.01*SR); return np.sqrt(np.convolve(x**2,np.ones(w)/w,'same'))
spans={}
for v,counts in NW.items():
    ws=W[v]; assert sum(counts)==len(ws),(v,sum(counts),len(ws)); i=0; spans[v]=[]
    for c in counts:
        a=ws[i]['a']; b=ws[i+c-1]['b']; nxt=ws[i+c]['a'] if i+c<len(ws) else len(A[v])/SR
        spans[v].append((max(0,a-0.05),min(nxt-0.02,b+0.35))); i+=c
SPEECH=[]
for k,name in enumerate(NAMES):
    layers=[]
    for j,v in enumerate(NW):
        a,b=spans[v][k]; x=A[v][int(a*SR):int(b*SR)]
        e=env(x); on=np.where(e>0.02)[0]; x=x[max(0,on[0]-int(.02*SR)):on[-1]+int(.06*SR)]   # tight trim
        layers.append((x,[0,.012,.022][j],[1.0,.8,.8][j])); layers.append((pitch(x,[1.0,-0.8,1.6][j]),[.03,.04,.018][j],.22))
    L=max(len(x)+int(d*SR) for x,d,g in layers)+int(.4*SR)
    out=np.zeros(L+len(cheer),np.float32)
    for x,d,g in layers: s=int(d*SR); out[s:s+len(x)]+=x*g
    speech=max(len(x) for x,d,g in layers); c=cheer*0.30; s=int(speech*0.75); out[s:s+len(c)]+=c[:len(out)-s]
    out=out[:speech+int(1.3*SR)]   # the cheer ends 1.3 s after the shout: never under the next sentence (gap = 0.35 + speech + 1.4)
    out=out/np.abs(out).max()*0.89
    f=int(.01*SR); out[:f]*=np.linspace(0,1,f); out[-int(.5*SR):]*=np.linspace(1,0,int(.5*SR))
    subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","-","-c:a","pcm_s16le",f"kids_{k:02d}.wav"],input=out.tobytes())
    SPEECH.append(round(speech/SR,2)); print(k,name,round(speech/SR,2),round(len(out)/SR,2))
json.dump({"names":NAMES,"speech":SPEECH},open('kids_index.json','w',encoding='utf-8'),ensure_ascii=False)
