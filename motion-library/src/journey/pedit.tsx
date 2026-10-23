import React from 'react';
import {useCurrentFrame} from 'remotion';
import {AR, EN, GFrame, grad, In, JY, lin, Pill, Sc} from './kit';

// Short 10 (Photo Editing & Retouching): my motion instead of the other channel's clip in his episode (Aly 2026-10-23).
// One photo in an editor; every edit happens on his word: remove the unwanted thing, light, colours, background blur, freckles.
const C = JY.huwa;
type B = Record<string, number>;
const at = (b: B, k: string, d: number) => b[k] ?? d;
const W = 840, H = 600; // photo inside the frame

const Photo: React.FC<{f: number; b: B}> = ({f, b}) => {
  const rm = at(b, 'remove', 20), li = at(b, 'light', 70), co = at(b, 'colors', 110), bl = at(b, 'blur', 150), fr = at(b, 'freckles', 230);
  const gone = lin(f, rm + 8, rm + 34);
  const bright = 0.62 + 0.38 * lin(f, li, li + 24), sat = 0.35 + 0.8 * lin(f, co, co + 24), blur = 9 * lin(f, bl, bl + 26);
  const freck = 1 - lin(f, fr + 6, fr + 30);
  // brush circle: over the bin while removing, over the cheeks while retouching
  const brush = f >= rm && f < rm + 40 ? {x: 700 + 20 * Math.sin(f / 3), y: 430 + 14 * Math.cos(f / 4)} : f >= fr && f < fr + 36 ? {x: 420 + 60 * Math.sin(f / 4), y: 300} : null;
  return (
    <div style={{position: 'absolute', inset: 0, filter: `brightness(${bright}) saturate(${sat})`}}>
      <svg width={W} height={H} style={{position: 'absolute', inset: 0, filter: `blur(${blur}px)`}}>
        <defs><linearGradient id="pe_sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#7EC8F2" /><stop offset="1" stopColor="#D8F0FF" /></linearGradient></defs>
        <rect width={W} height={H} fill="url(#pe_sky)" />
        <circle cx={700} cy={110} r={55} fill="#FFD95A" />
        <path d="M0 380 Q 200 300 420 360 T 840 330 V600 H0Z" fill="#7CC36A" />
        <path d="M0 450 Q 260 400 840 440 V600 H0Z" fill="#5EA94F" />
        {[[90, 330, 70], [210, 310, 55], [620, 300, 65], [770, 320, 50]].map(([x, y, r], i) => (
          <g key={i}><rect x={x - 8} y={y} width={16} height={90} fill="#7A5230" /><circle cx={x} cy={y} r={r} fill="#3E8E41" /></g>
        ))}
        <path d="M360 600 Q 420 470 470 380 L 500 380 Q 470 470 520 600Z" fill="#E8D7A8" />
        {/* the unwanted thing: a trash bin behind him */}
        <g opacity={1 - gone}><rect x={668} y={390} width={66} height={92} rx={8} fill="#5B6770" /><rect x={660} y={378} width={82} height={16} rx={6} fill="#47525A" />
          {[684, 701, 718].map((x) => <rect key={x} x={x} y={404} width={6} height={64} rx={3} fill="#47525A" />)}</g>
      </svg>
      {/* the person stays sharp (only the background gets the blur) */}
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <path d="M250 600 Q 260 430 420 410 Q 580 430 590 600Z" fill="#E8175D" />
        <rect x={392} y={340} width={56} height={80} fill="#E9B98F" />
        <circle cx={420} cy={265} r={98} fill="#E9B98F" />
        <path d="M322 250 Q 330 150 420 152 Q 520 150 520 255 Q 500 200 420 205 Q 345 200 322 250Z" fill="#3A2416" />
        <circle cx={385} cy={270} r={9} fill="#2A1E17" /><circle cx={455} cy={270} r={9} fill="#2A1E17" />
        <path d="M388 318 Q 420 342 452 318" stroke="#9C4A3A" strokeWidth={7} fill="none" strokeLinecap="round" />
        <g opacity={freck}>{[[360, 300], [372, 312], [350, 312], [480, 300], [468, 312], [490, 312], [365, 292], [475, 292]].map(([x, y], i) => <circle key={i} cx={x} cy={y} r={4} fill="#A9643F" />)}</g>
      </svg>
      {brush ? <div style={{position: 'absolute', left: brush.x - 34, top: brush.y - 34, width: 68, height: 68, borderRadius: '50%', border: '4px solid #fff',
        boxShadow: '0 0 0 3px rgba(0,0,0,0.35)', background: 'rgba(255,255,255,0.18)'}} /> : null}
    </div>
  );
};

export const PEdit: React.FC<{b?: B; title?: string}> = ({b = {}, title = 'Photo Editing & Retouching'}) => {
  const f = useCurrentFrame();
  const steps = [['remove', '🧹', 'تشيل اللي مش عايزه'], ['light', '💡', 'الإضاءة'], ['colors', '🎨', 'الألوان'], ['blur', '🌫️', 'بلور للخلفية'], ['freckles', '✨', 'تشيل النمش']];
  const defaults = [20, 70, 110, 150, 230];
  const cur = steps.reduce((k, s, i) => (f >= at(b, s[0], defaults[i]) ? i : k), -1);
  return (
    <Sc>
      <In at={0} x={540} y={340}><Pill text={title} bg={grad('huwa')} ink="#fff" size={46} font={EN} dir="ltr" /></In>
      <div style={{position: 'absolute', left: 110, top: 450}}>
        <GFrame w={W + 20} h={H + 20}><Photo f={f} b={b} /></GFrame>
      </div>
      {/* the editor's tools: the active one lights up, its slider fills */}
      <div style={{position: 'absolute', left: 70, right: 70, top: 1110, display: 'flex', justifyContent: 'center', gap: 14, direction: 'rtl'}}>
        {steps.map(([k, e], i) => {
          const on = i === cur, done = i < cur;
          return <div key={k} style={{width: 150, height: 96, borderRadius: 22, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 50,
            background: on ? grad('huwa') : '#fff', opacity: on || done ? 1 : 0.55, boxShadow: on ? '0 12px 26px rgba(232,23,93,0.35)' : '0 6px 14px rgba(0,0,0,0.12)',
            transform: `scale(${on ? 1.08 : 1})`}}>{e}</div>;
        })}
      </div>
      {cur >= 0 ? (
        <div key={cur} style={{position: 'absolute', left: 0, right: 0, top: 1232, display: 'flex', justifyContent: 'center'}}>
          <div style={{fontFamily: AR, fontWeight: 900, fontSize: 44, color: C.ink, direction: 'rtl', opacity: lin(f, at(b, steps[cur][0], defaults[cur]), at(b, steps[cur][0], defaults[cur]) + 6)}}>{steps[cur][1]} {steps[cur][2]}</div>
        </div>
      ) : null}
    </Sc>
  );
};

export const peditScenes: Record<string, React.FC<any>> = {pe_edit: PEdit};
