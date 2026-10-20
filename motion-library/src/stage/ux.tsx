import React from 'react';
import {Easing, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, L, lin, Mark, S, spr, W} from './kit';

// Scenes for the UX shorts. Beats are seconds from the cue start (props.b).
const bt = (b: Record<string, number> | undefined, k: string, fps: number, d = 999) => Math.round((b?.[k] ?? d) * fps);

// ---------- ATM: mode 'ask' (what comes out first?), 'right' (card, then cash), 'wrong' (cash first -> he walks away, card left) ----------
const Atm: React.FC<{card: number; cash: number; blink?: boolean}> = ({card, cash, blink}) => {
  const f = useCurrentFrame();
  return (
    <svg width={520} height={760} viewBox="0 0 520 760" style={{overflow: 'visible'}}>
      <defs>
        <linearGradient id="atmb" x1="0" x2="1"><stop offset="0" stopColor="#2A3350" /><stop offset="1" stopColor="#1A2038" /></linearGradient>
        <linearGradient id="scr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#5B8CFF" /><stop offset="1" stopColor="#2F4FD0" /></linearGradient>
      </defs>
      <rect x={20} y={0} width={480} height={760} rx={36} fill="url(#atmb)" stroke="#3E4A73" strokeWidth={4} />
      <rect x={60} y={50} width={400} height={50} rx={12} fill="#11152A" />
      <text x={260} y={86} textAnchor="middle" fontFamily={EN} fontWeight={900} fontSize={30} fill={S.cyan} letterSpacing={6}>ATM</text>
      <rect x={70} y={130} width={380} height={230} rx={18} fill="url(#scr)" />
      {/* card slot + card */}
      <rect x={300} y={400} width={170} height={20} rx={8} fill="#0A0D1A" stroke={blink && Math.floor(f / 6) % 2 ? S.red : '#4A5785'} strokeWidth={4} />
      <g transform={`translate(0 ${-card * 150})`}>
        <rect x={318} y={300} width={134} height={118} rx={10} fill={S.yellow} opacity={card > 0.02 ? 1 : 0} />
        <rect x={330} y={330} width={30} height={22} rx={4} fill="#B8860B" opacity={card > 0.02 ? 1 : 0} />
      </g>
      <rect x={300} y={418} width={170} height={60} fill="url(#atmb)" />
      {/* keypad */}
      {[0, 1, 2, 3].map((r) => [0, 1, 2].map((c) => <rect key={r + '' + c} x={80 + c * 64} y={400 + r * 56} width={52} height={42} rx={8} fill="#3A4570" />))}
      {/* cash slot + bills */}
      <rect x={110} y={640} width={300} height={22} rx={8} fill="#0A0D1A" stroke="#4A5785" strokeWidth={4} />
      <g transform={`translate(0 ${cash * 130})`}>
        {[0, 1, 2].map((i) => <rect key={i} x={130 + i * 6} y={520 + i * 4} width={250} height={120} rx={8} fill={i === 2 ? '#35C27A' : '#2BA866'} stroke="#1D7A4A" strokeWidth={3}
          opacity={cash > 0.02 ? 1 : 0} />)}
        <text x={268} y={600} textAnchor="middle" fontFamily={EN} fontWeight={900} fontSize={54} fill="#14532D" opacity={cash > 0.02 ? 1 : 0}>$</text>
      </g>
      <rect x={110} y={660} width={300} height={100} fill="url(#atmb)" />
    </svg>
  );
};

// old man with a cane (flat figure); walk = 0..1 walks him off to the left, `hand` raises the hand to the slot
const OldMan: React.FC<{walk: number; hand: number; cane?: boolean; money?: boolean}> = ({walk, hand, cane = true, money}) => {
  const f = useCurrentFrame();
  const step = walk > 0 && walk < 1 ? Math.sin(f / 3) * 10 : 0;
  return (
    <svg width={300} height={620} viewBox="0 0 300 620" style={{overflow: 'visible', transform: `translateX(${-walk * 900}px)`}}>
      <circle cx={150} cy={90} r={56} fill="#E8B48C" />
      <path d="M96 80 Q100 30 150 28 Q200 30 204 80 Q190 56 150 54 Q110 56 96 80 Z" fill="#E6E6EE" />
      <rect x={128} y={100} width={44} height={6} rx={3} fill="#555" />
      <path d="M92 170 Q150 140 208 170 L220 400 L80 400 Z" fill="#6C7BA8" />
      <path d={`M100 400 L${90 + step} 590 M200 400 L${210 - step} 590`} stroke="#3C4466" strokeWidth={34} strokeLinecap="round" />
      {/* arm to the machine */}
      <path d={`M200 190 L${250 + 60 * hand} ${300 - 120 * hand}`} stroke="#6C7BA8" strokeWidth={30} strokeLinecap="round" />
      <circle cx={250 + 60 * hand} cy={300 - 120 * hand} r={18} fill="#E8B48C" />
      {money ? <rect x={232 + 60 * hand} y={268 - 120 * hand} width={70} height={40} rx={6} fill="#35C27A" stroke="#1D7A4A" strokeWidth={3} /> : null}
      {cane ? <><path d="M100 200 L60 420" stroke="#6C7BA8" strokeWidth={30} strokeLinecap="round" /><path d="M60 410 L40 600 M40 410 Q36 380 64 384" stroke="#8B5A2B" strokeWidth={12} strokeLinecap="round" fill="none" /></> : null}
    </svg>
  );
};

export const AtmScene: React.FC<{dur: number; mode: 'ask' | 'right' | 'wrong'; b?: Record<string, number>}> = ({dur, mode, b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 140, 16), o = 1 - lin(f, dur - 7, dur);
  const kCard = bt(b, 'card', fps), kCash = bt(b, 'cash', fps), kWalk = bt(b, 'walk', fps);
  const card = lin(f, kCard, kCard + 14, 0, 1, Easing.out(Easing.back(1.6)));
  const cash = lin(f, kCash, kCash + 14, 0, 1, Easing.out(Easing.back(1.4)));
  const walk = lin(f, kWalk, kWalk + 40, 0, 1, Easing.inOut(Easing.quad));
  const hand = mode === 'wrong' ? Math.min(lin(f, kCash + 10, kCash + 22), 1 - lin(f, kWalk, kWalk + 10)) : mode === 'right' ? lin(f, kCard + 6, kCard + 18) : 0;
  const cardTaken = mode === 'right' && f > kCash + 20;
  const y0 = L.stageTop + 20;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: W, height: 1920, opacity: Math.min(1, p * 1.4) * o}}>
      <div style={{position: 'absolute', left: 470, top: y0, transform: `scale(${0.8 + 0.2 * p})`, transformOrigin: 'top center'}}>
        <Atm card={mode === 'wrong' ? (f > kWalk ? 1 : 0) * lin(f, kWalk + 20, kWalk + 30) : cardTaken ? 0 : card} cash={mode === 'wrong' ? (f > kWalk ? 0 : cash) : cash}
          blink={mode === 'wrong' && f > kWalk + 30} />
        {/* the screen text */}
        <div style={{position: 'absolute', left: 70, top: 130, width: 380, height: 230, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: AR, fontWeight: 900,
          fontSize: mode === 'ask' ? 150 : 44, color: '#fff', direction: 'rtl', textAlign: 'center', lineHeight: 1.3}}>
          {mode === 'ask' ? <span style={{transform: `scale(${1 + 0.08 * Math.sin(f / 6)})`, display: 'inline-block'}}>؟</span>
            : f < kCard ? 'استلم الكارت' : f < kCash ? 'استلم الكارت 👆' : 'خد فلوسك 💵'}
        </div>
      </div>
      <div style={{position: 'absolute', left: 90, top: y0 + 140}}>
        <OldMan walk={mode === 'wrong' ? walk : 0} hand={hand} money={mode === 'wrong' && f > kCash + 18} />
      </div>
      {/* order chips */}
      {mode !== 'ask' ? (
        <div style={{position: 'absolute', left: 60, top: y0 + 20, display: 'flex', flexDirection: 'column', gap: 16, direction: 'rtl'}}>
          {(mode === 'right' ? [['1', 'الكارت', kCard], ['2', 'الفلوس', kCash]] : [['1', 'الفلوس', kCash], ['2', 'الكارت', kWalk + 26]]).map(([n, t, k], i) => {
            const q = spr(f, fps, (k as number) + 4, 220, 12);
            return <div key={i} style={{display: 'flex', alignItems: 'center', gap: 12, opacity: q, transform: `translateX(${(1 - q) * -60}px)`}}>
              <span style={{width: 64, height: 64, borderRadius: 32, background: mode === 'right' ? S.green : S.red, color: '#fff', fontFamily: EN, fontWeight: 900, fontSize: 40,
                display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{n}</span>
              <span style={{fontFamily: AR, fontWeight: 900, fontSize: 48, color: '#fff'}}>{t}</span>
            </div>;
          })}
        </div>
      ) : null}
      {mode === 'wrong' && f > kWalk + 34 ? (
        <div style={{position: 'absolute', left: 520, top: y0 + 300, display: 'flex', alignItems: 'center', gap: 16, direction: 'rtl'}}>
          <Mark ok={false} at={kWalk + 34} />
          <span style={{fontFamily: AR, fontWeight: 900, fontSize: 56, color: '#fff', background: S.red, padding: '0 18px 6px', borderRadius: 14, opacity: lin(f, kWalk + 38, kWalk + 46)}}>نسي الكارت!</span>
        </div>
      ) : null}
      {mode === 'right' && f > kCash + 16 ? <div style={{position: 'absolute', left: 120, top: y0 + 600}}><Mark ok at={kCash + 16} /></div> : null}
    </div>
  );
};

// ---------- ketchup: the pretty glass bottle (UI) vs the squeeze bottle (UX). beats: shake, squeeze ----------
const Glass: React.FC<{tilt: number; shake: number}> = ({tilt, shake}) => (
  <svg width={220} height={560} viewBox="0 0 220 560" style={{overflow: 'visible', transform: `rotate(${tilt + shake}deg)`, transformOrigin: '50% 60%'}}>
    <path d="M86 0 H134 V40 Q134 70 150 110 Q190 170 190 240 V520 Q190 556 154 556 H66 Q30 556 30 520 V240 Q30 170 70 110 Q86 70 86 40 Z" fill="#C8102E" stroke="#fff" strokeOpacity={0.5} strokeWidth={4} />
    <rect x={80} y={-24} width={60} height={30} rx={6} fill="#EDEDED" />
    <rect x={44} y={290} width={132} height={150} rx={12} fill="#F6F1E4" />
    <text x={110} y={360} textAnchor="middle" fontFamily={EN} fontWeight={900} fontSize={30} fill="#C8102E">TOMATO</text>
    <text x={110} y={396} textAnchor="middle" fontFamily={EN} fontWeight={800} fontSize={24} fill="#333">KETCHUP</text>
    <path d="M50 250 Q46 380 56 500" stroke="#fff" strokeOpacity={0.35} strokeWidth={10} strokeLinecap="round" fill="none" />
  </svg>
);
const Squeeze: React.FC<{press: number}> = ({press}) => (
  <svg width={260} height={480} viewBox="0 0 260 480" style={{overflow: 'visible'}}>
    {/* upside down: cap at the bottom */}
    <path d={`M${20 + press * 18} 20 Q130 ${-10 + press * 10} ${240 - press * 18} 20 Q${250 - press * 26} 200 ${210 - press * 10} 360 Q190 400 130 400 Q70 400 ${50 + press * 10} 360 Q${10 + press * 26} 200 ${20 + press * 18} 20 Z`}
      fill="#D7142E" stroke="#fff" strokeOpacity={0.5} strokeWidth={4} />
    <rect x={80} y={392} width={100} height={70} rx={12} fill="#F2F2F2" />
    <rect x={56} y={130} width={148} height={140} rx={16} fill="#F6F1E4" />
    <text x={130} y={196} textAnchor="middle" fontFamily={EN} fontWeight={900} fontSize={30} fill="#C8102E">TOMATO</text>
    <text x={130} y={230} textAnchor="middle" fontFamily={EN} fontWeight={800} fontSize={24} fill="#333">KETCHUP</text>
  </svg>
);
const Plate: React.FC<{fill: number}> = ({fill}) => (
  <svg width={300} height={110} viewBox="0 0 300 110">
    <ellipse cx={150} cy={70} rx={145} ry={36} fill="#E9ECF5" />
    <ellipse cx={150} cy={62} rx={110} ry={24} fill="#fff" />
    <ellipse cx={150} cy={58} rx={70 * fill} ry={14 * fill} fill="#C8102E" />
  </svg>
);
export const KetchupScene: React.FC<{dur: number; b?: Record<string, number>}> = ({dur, b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 140, 16), o = 1 - lin(f, dur - 7, dur);
  const kS = bt(b, 'shake', fps, 1.5), kQ = bt(b, 'squeeze', fps, 4);
  const tilt = lin(f, kS - 6, kS + 6, 0, 150);
  const shake = f > kS + 6 && f < kQ ? Math.sin(f * 1.6) * 9 : 0;
  const press = f > kQ ? 0.5 + 0.5 * Math.sin((f - kQ) / 4 - Math.PI / 2) : 0;
  const flow = lin(f, kQ + 4, kQ + 26);
  const y0 = L.stageTop;
  const lab = (t: string, sub: string, c: string, k: number) => {
    const q = spr(f, fps, k, 200, 13);
    return <div style={{textAlign: 'center', opacity: q, transform: `scale(${0.7 + 0.3 * q})`}}>
      <div style={{fontFamily: EN, fontWeight: 900, fontSize: 70, color: c}}>{t}</div>
      <div style={{fontFamily: AR, fontWeight: 900, fontSize: 44, color: '#fff', direction: 'rtl'}}>{sub}</div>
    </div>;
  };
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: W, height: 1920, opacity: Math.min(1, p * 1.4) * o}}>
      <div style={{position: 'absolute', left: 90, top: y0 + 10, width: 400, display: 'flex', justifyContent: 'center'}}>{lab('UI', 'الأجمل شكلًا', S.cyan, 4)}</div>
      <div style={{position: 'absolute', left: 590, top: y0 + 10, width: 400, display: 'flex', justifyContent: 'center'}}>{lab('UX', 'الأسهل استخدامًا', S.yellow, 10)}</div>
      <div style={{position: 'absolute', left: W / 2 - 3, top: y0 + 20, width: 6, height: 780, borderRadius: 3, background: 'rgba(255,255,255,0.15)'}} />
      <div style={{position: 'absolute', left: 180, top: y0 + 170}}><Glass tilt={tilt} shake={shake} /></div>
      <div style={{position: 'absolute', left: 140, top: y0 + 690}}><Plate fill={0} /></div>
      <div style={{position: 'absolute', left: 660, top: y0 + 190}}><Squeeze press={press} /></div>
      {/* the flow */}
      <div style={{position: 'absolute', left: 783, top: y0 + 660, width: 14, height: 60 * flow, borderRadius: 7, background: '#C8102E', opacity: flow > 0 && flow < 1 ? 1 : 0}} />
      <div style={{position: 'absolute', left: 640, top: y0 + 690}}><Plate fill={flow} /></div>
      {f > kS + 30 ? <div style={{position: 'absolute', left: 230, top: y0 + 470}}><Mark ok={false} at={kS + 30} /></div> : null}
      {f > kQ + 20 ? <div style={{position: 'absolute', left: 730, top: y0 + 470}}><Mark ok at={kQ + 20} /></div> : null}
    </div>
  );
};

// ---------- shield: UX protects the customer (or hurts him) ----------
export const Shield: React.FC<{dur: number; b?: Record<string, number>}> = ({dur, b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 140, 13), o = 1 - lin(f, dur - 7, dur);
  const kHurt = bt(b, 'hurt', fps, 1.5), kGood = bt(b, 'good', fps, 3);
  const y0 = L.stageTop + 60;
  const row = (k: number, ok: boolean, t: string) => {
    const q = spr(f, fps, k, 200, 13);
    return <div style={{display: 'flex', alignItems: 'center', gap: 22, direction: 'rtl', opacity: q, transform: `translateX(${(1 - q) * 80}px)`}}>
      <Mark ok={ok} s={0.8} at={k} /><span style={{fontFamily: AR, fontWeight: 900, fontSize: 56, color: '#fff'}}>{t}</span></div>;
  };
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: y0, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 40, opacity: o}}>
      <svg width={300} height={340} viewBox="0 0 300 340" style={{transform: `scale(${p})`}}>
        <defs><linearGradient id="sh" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor={S.blue} /><stop offset="1" stopColor={S.violet} /></linearGradient></defs>
        <path d="M150 10 L280 60 Q280 240 150 330 Q20 240 20 60 Z" fill="url(#sh)" stroke="#fff" strokeOpacity={0.4} strokeWidth={6} />
        <text x={150} y={205} textAnchor="middle" fontFamily={EN} fontWeight={900} fontSize={90} fill="#fff">UX</text>
      </svg>
      <div style={{display: 'flex', flexDirection: 'column', gap: 26}}>
        {row(kHurt, false, 'ممكن تأذي الزبون')}
        {row(kGood, true, 'أو تبقى في مصلحته')}
      </div>
    </div>
  );
};
