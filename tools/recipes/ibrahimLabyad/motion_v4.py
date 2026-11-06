import cv2, numpy as np, json
S='work/src720_crop-ready.mp4'
shots=json.load(open('work/shots_v4.json'))
cap=cv2.VideoCapture(S); fps=cap.get(cv2.CAP_PROP_FPS)
frames=[]; i=0
while True:
    ok,f=cap.read()
    if not ok: break
    if i%2==0:
        g=cv2.cvtColor(f[88:620,28:1248],cv2.COLOR_BGR2GRAY)
        g=cv2.resize(g,(488,213))
        frames.append((i/fps,g))
    i+=1
res=[]
for s in shots:
    fr=[(t,g) for t,g in frames if s['s']+0.07<=t<=s['e']-0.07]
    tx=ty=0; sc=1; steps=[]
    for (t0,a),(t1,b) in zip(fr,fr[1:]):
        p0=cv2.goodFeaturesToTrack(a,300,0.01,6)
        if p0 is None or len(p0)<12: steps.append((0,0,1,0)); continue
        p1,st,_=cv2.calcOpticalFlowPyrLK(a,b,p0,None)
        m=st.ravel()==1
        if m.sum()<10: steps.append((0,0,1,0)); continue
        M,inl=cv2.estimateAffinePartial2D(p0[m],p1[m],ransacReprojThreshold=2)
        if M is None: steps.append((0,0,1,0)); continue
        scl=np.sqrt(M[0,0]**2+M[1,0]**2)
        steps.append((M[0,2],M[1,2],scl,inl.sum()/max(1,m.sum())))
    st=np.array(steps) if steps else np.zeros((1,4))
    dx=st[:,0]; dy=st[:,1]; scl=st[:,2]
    cumx=-dx.sum(); cumy=-dy.sum(); zoom=np.prod(scl)
    jit=np.sqrt(np.var(np.diff(dx))+np.var(np.diff(dy))) if len(dx)>2 else 0
    res.append(dict(n=s['n'],s=s['s'],d=round(s['e']-s['s'],2),camx=round(float(cumx),1),camy=round(float(cumy),1),zoom=round(float(zoom),3),jit=round(float(jit),2),inl=round(float(st[:,3].mean()),2)))
json.dump(res,open('work/motion_v4.json','w'))
pass
