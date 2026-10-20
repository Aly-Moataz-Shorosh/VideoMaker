import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, K, Halftone, Paper, Pop, Scene, Stamp, Strip, Tag, Title, lin, spr, useBeats, rnd} from './kit';
import {CrankCamera, Runner} from './draw';
import {Hook} from './s02';

// Short 5 — how video was born: many pictures fast, frames per second, silent cinema + live band, sound on film.
const PJ = 'projects/2026-10-08 shorts theodesy/';
type B = {b?: Record<string, number>};

const Card: React.FC<{t: number; w?: number; h?: number; seed?: number}> = ({t, w = 200, h = 250, seed = 1}) => (
  <Paper w={w} h={h} seed={seed} color={K.white}>
    <svg width={w} height={h} viewBox="-150 -300 300 340">
      <line x1={-150} y1={0} x2={150} y2={0} stroke="#141210" strokeWidth={6} />
      <Runner x={-10} y={0} s={1.1} t={t} />
    </svg>
  </Paper>
);

export const S5Hook: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  return (
    <Hook b={b} n={5} title="طب لو عايزين نحفظ *الحركة* نفسها؟" side={
      <div style={{position: 'absolute', left: 40, top: 860, transform: `rotate(-8deg) scale(${lin(f, 16, 28)})`}}><Card t={f / 3} w={240} h={300} seed={3} /></div>
    } />
  );
};

// 2 pictures? 3? 10? -> many, fast -> it moves = video.
export const S5Count: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const at = useBeats(b);
  const t2 = at('two', 5.1), t3 = at('three', 5.7), t10 = at('ten', 6.5), tMany = at('many', 7.2), tVideo = at('video', 9.3);
  const n = f < t2 ? 0 : f < t3 ? 2 : f < t10 ? 3 : f < tMany ? 10 : Math.min(60, 10 + Math.floor((f - tMany) * 1.6));
  const flip = f >= tVideo;
  return (
    <Scene bg="#191612">
      <div style={{position: 'absolute', top: 200, left: 60, right: 60, display: 'flex', justifyContent: 'center', opacity: 1 - lin(f, t2 - 8, t2)}}>
        <Title text="فيديو = *حركة*… نعملها إزاي؟" size={88} at={2} />
      </div>
      {!flip ? Array.from({length: n}, (_, i) => {
        const k = spr(f, fps, [t2, t2 + 3, t3, t10, t10 + 1, t10 + 2, t10 + 3, t10 + 4, t10 + 5, t10 + 6][i] ?? tMany + (i - 10) / 1.6, 220, 14);
        const x = 180 + rnd(i * 3) * 720, y = 560 + rnd(i * 7) * 700;
        return <div key={i} style={{position: 'absolute', left: x - 100, top: y - 125, transform: `scale(${k * (i < 10 ? 1 : 0.7)}) rotate(${(rnd(i) - 0.5) * 40}deg)`}}>
          <Card t={i * 0.7} seed={i + 2} />
        </div>;
      }) : (
        <div style={{position: 'absolute', left: 540 - 260, top: 600, transform: `scale(${spr(f, fps, tVideo, 160, 14)})`}}>
          <Card t={(f - tVideo) * 0.7} w={520} h={650} seed={7} />
        </div>
      )}
      {!flip ? (
        <div style={{position: 'absolute', top: 1340, left: 0, right: 0, textAlign: 'center', fontFamily: EN, fontWeight: 900, fontSize: 200, color: K.yellow, textShadow: '0 10px 0 #000'}}>
          {n ? (n >= 60 ? '∞' : n) : ''}
        </div>
      ) : null}
      {f >= tMany && !flip ? <Pop at={tMany} x={540} y={300}><Tag text="كتير جدًا… وبسرعة جدًا" bg={K.yellow} size={60} /></Pop> : null}
      <div style={{position: 'absolute', left: 300, top: 1330}}><Stamp text="ده الفيديو!" at={tVideo + 4} size={96} rot={-6} color={K.yellow} /></div>
    </Scene>
  );
};

// The first movie camera: hand crank, frames shooting out.
export const S5Camera: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const t = f / 4;
  return (
    <Scene bg="#16130F">
      <svg width={1080} height={1920} style={{position: 'absolute'}}><CrankCamera x={420} y={860} s={1.5} t={t} /></svg>
      {Array.from({length: 7}, (_, i) => {
        const k = ((f + i * 8) % 56) / 56;
        return (
          <div key={i} style={{position: 'absolute', left: 820 + k * 320, top: 840 - k * 520 + i * 6, transform: `rotate(${-30 + k * 40}deg) scale(${0.5 + k * 0.6})`, opacity: 1 - k}}>
            <Card t={i} w={150} h={190} seed={i + 20} />
          </div>
        );
      })}
      <div style={{position: 'absolute', top: 200, left: 60, right: 60, display: 'flex', justifyContent: 'center'}}>
        <Title text="أول *كاميرا* في الدنيا" size={96} at={3} />
      </div>
      <Pop at={at('many', 6.4)} x={540} y={1380} rot={-3}><Tag text="بتصوّر صور عادية… بس كتير" bg={K.yellow} size={54} /></Pop>
    </Scene>
  );
};

// Frames per second: the runner gets smoother as the number grows (12 -> 16 -> 24 -> 30).
export const S5Fps: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const t16 = at('f16', 0.9), t12 = at('f12', 3), t24 = at('f24', 4.2), t30 = at('f30', 5.3), tMove = at('move', 8.2);
  const fpsNow = f < t12 ? 16 : f < t24 ? 12 : f < t30 ? 24 : 30;
  const step = 30 / fpsNow; // hold each drawing this many frames -> choppy at low fps
  const tq = Math.floor(f / step) * step;
  return (
    <Scene bg={K.ink}>
      <div style={{position: 'absolute', left: 90, top: 240, width: 900, height: 700, background: K.white, borderRadius: 10, overflow: 'hidden', boxShadow: '0 30px 60px rgba(0,0,0,0.6)'}}>
        <Halftone color="#000" size={10} dot={0.15} opacity={0.1} />
        <svg width={900} height={700}>
          <line x1={0} y1={600} x2={900} y2={600} stroke="#141210" strokeWidth={6} />
          {Array.from({length: 8}, (_, i) => <line key={i} x1={((i * 140 - tq * 9) % 1120 + 1120) % 1120 - 100} y1={630} x2={((i * 140 - tq * 9) % 1120 + 1120) % 1120 - 40} y2={630}
            stroke="#141210" strokeWidth={4} />)}
          <Runner x={450} y={600} s={1.6} t={tq / 3.2} />
        </svg>
      </div>
      <div style={{position: 'absolute', top: 1000, left: 0, right: 0, display: 'flex', justifyContent: 'center', alignItems: 'baseline', gap: 26, direction: 'rtl'}}>
        <div key={fpsNow} style={{fontFamily: EN, fontWeight: 900, fontSize: 280, color: K.yellow, lineHeight: 1, textShadow: '0 12px 0 #000'}}>{fpsNow}</div>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 70, color: K.white}}>صورة في الثانية</div>
      </div>
      <div style={{position: 'absolute', left: 280, top: 1350}}><Stamp text="بقت حركة!" at={tMove} size={96} rot={-6} color={K.yellow} /></div>
      {f < t16 ? null : <div style={{position: 'absolute', top: 1290, left: 0, right: 0, textAlign: 'center', fontFamily: AR, fontWeight: 900, fontSize: 48,
        color: fpsNow >= 24 ? K.cyan : K.dim}}>{fpsNow >= 24 ? 'ناعمة' : 'بتقطّع'}</div>}
    </Scene>
  );
};

// Silent cinema: screen with the runner film, title card, audience.
export const S5Silent: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  return (
    <Scene bg="#0B0A09">
      <div style={{position: 'absolute', left: 80, top: 230, width: 920, height: 640, background: '#E9E4D8', overflow: 'hidden', boxShadow: `0 0 120px rgba(255,240,200,${0.25 + 0.05 * rnd(f)})`,
        filter: `brightness(${0.9 + 0.12 * rnd(f * 2)})`}}>
        <svg width={920} height={640} style={{filter: 'grayscale(1)'}}>
          <line x1={0} y1={540} x2={920} y2={540} stroke="#141210" strokeWidth={6} />
          <Runner x={460} y={540} s={1.4} t={Math.floor(f / 2) * 2 / 3.2} />
        </svg>
        {f >= at('silent', 2.5) ? (
          <div style={{position: 'absolute', inset: 0, background: '#000', display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: lin(f, at('silent', 2.5), at('silent', 2.5) + 6)}}>
            <div style={{border: `6px double ${K.paper}`, padding: '30px 60px', fontFamily: AR, fontWeight: 900, fontSize: 110, color: K.paper}}>سينما صامتة</div>
          </div>
        ) : null}
      </div>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        {Array.from({length: 3}, (_, r) => Array.from({length: 7}, (_, i) => {
          const x = 60 + i * 160 + (r % 2) * 80, y = 1180 + r * 120;
          return <g key={`${r}${i}`} fill="#000"><circle cx={x} cy={y - 60} r={36} /><rect x={x - 58} y={y - 28} width={116} height={130} rx={40} /></g>;
        }))}
      </svg>
      <Pop at={at('seq', 6)} x={540} y={980} rot={-3}><Tag text="صور ورا بعض = فيديو" bg={K.yellow} size={54} /></Pop>
      <Pop at={at('silent', 2.5) + 8} x={820} y={1080} rot={6}><div style={{fontSize: 110}}>🔇</div></Pop>
    </Scene>
  );
};

// A live band in front of the screen.
export const S5Band: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  return (
    <Scene bg="#0B0A09">
      <div style={{position: 'absolute', left: 80, top: 230, width: 920, height: 560, background: '#E9E4D8', overflow: 'hidden', opacity: 0.85}}>
        <svg width={920} height={560} style={{filter: 'grayscale(1)'}}><line x1={0} y1={470} x2={920} y2={470} stroke="#141210" strokeWidth={6} /><Runner x={460} y={470} s={1.2} t={Math.floor(f / 2) * 2 / 3.2} /></svg>
      </div>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        {/* piano */}
        <g transform="translate(250,1180)">
          <rect x={-160} y={-120} width={320} height={190} rx={12} fill="#1B1714" stroke="#3a332b" strokeWidth={5} />
          <rect x={-150} y={20} width={300} height={34} fill={K.white} />
          {Array.from({length: 14}, (_, i) => <rect key={i} x={-148 + i * 21.5} y={20} width={11} height={20} fill="#111" />)}
          <g transform={`translate(0,-40) rotate(${Math.sin(f / 4) * 4})`}><circle cx={0} cy={-150} r={40} fill="#000" /><rect x={-55} y={-115} width={110} height={130} rx={40} fill="#000" /></g>
        </g>
        {/* violinist */}
        <g transform={`translate(760,1150) rotate(${Math.sin(f / 5) * 5})`}>
          <circle cx={0} cy={-150} r={40} fill="#000" /><rect x={-55} y={-115} width={110} height={200} rx={40} fill="#000" />
          <ellipse cx={-60} cy={-90} rx={40} ry={22} fill="#7A4A22" transform="rotate(-30 -60 -90)" />
          <line x1={-130} y1={-40 + Math.sin(f / 3) * 30} x2={40} y2={-150 + Math.sin(f / 3) * 30} stroke="#C9A66B" strokeWidth={5} />
        </g>
        {Array.from({length: 10}, (_, i) => {
          const k = ((f + i * 11) % 70) / 70, x = 200 + rnd(i) * 680 + Math.sin(k * 6 + i) * 30, y = 1100 - k * 380;
          return <text key={i} x={x} y={y} fontSize={70} fill={i % 2 ? K.yellow : K.paper} opacity={1 - k}>{i % 3 ? '♪' : '♫'}</text>;
        })}
      </svg>
      <Pop at={at('band', 4.5)} x={540} y={1480} rot={-3}><Tag text="فرقة موسيقى عايشة في القاعة" bg={K.yellow} size={52} /></Pop>
    </Scene>
  );
};

// Behind Aly (middle): record the sound too.
export const S5Mic: React.FC<B> = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <svg width={1080} height={700} style={{position: 'absolute', top: 120}}>
        <g transform={`translate(540,260) scale(${lin(f, 0, 12)})`}>
          <rect x={-60} y={-160} width={120} height={200} rx={60} fill={K.paper} stroke="#141210" strokeWidth={8} />
          {Array.from({length: 6}, (_, i) => <line key={i} x1={-50} y1={-130 + i * 28} x2={50} y2={-130 + i * 28} stroke="#141210" strokeWidth={4} />)}
          <path d="M-95,0 Q-95,110 0,110 Q95,110 95,0" stroke={K.paper} strokeWidth={12} fill="none" />
          <line x1={0} y1={110} x2={0} y2={190} stroke={K.paper} strokeWidth={12} />
        </g>
        {Array.from({length: 3}, (_, i) => {
          const k = ((f + i * 10) % 30) / 30;
          return <circle key={i} cx={540} cy={200} r={120 + k * 220} fill="none" stroke={K.yellow} strokeWidth={8} opacity={1 - k} />;
        })}
      </svg>
      <Pop at={8} x={540} y={760} rot={-3}><Tag text="نسجّل الصوت كمان" bg={K.yellow} size={56} /></Pop>
    </AbsoluteFill>
  );
};

// Sound = a wave -> written on the side of the film strip (optical soundtrack).
export const S5Sound: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tWave = at('wave', 15.9), tSide = at('side', 18.3);
  const wave = (x: number) => Math.sin(x / 22 + f / 4) * 0.5 + Math.sin(x / 9 - f / 3) * 0.3 + Math.sin(x / 47) * 0.2;
  const strip = lin(f, tSide - 6, tSide + 10);
  const off = (f * 6) % 300;
  return (
    <Scene bg="#121010">
      {/* speaker -> wave */}
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <g transform="translate(140,420)" opacity={1 - strip * 0.7}>
          <path d="M-40,-50 L10,-50 L70,-110 L70,110 L10,50 L-40,50 Z" fill={K.paper} stroke="#141210" strokeWidth={6} />
          <path d={`M${100},${-60} Q140,0 100,60 M130,-100 Q190,0 130,100`} stroke={K.yellow} strokeWidth={8} fill="none" opacity={0.5 + 0.5 * Math.sin(f / 3)} />
        </g>
        <path d={Array.from({length: 120}, (_, i) => `${i ? 'L' : 'M'}${240 + i * 7},${420 + wave(i * 7) * 120 * lin(f, 4, 20)}`).join(' ')} stroke={K.yellow} strokeWidth={8} fill="none"
          opacity={1 - strip * 0.7} />
      </svg>
      <Pop at={at('rec', 3)} x={540} y={220} rot={-3}><Tag text="الصوت عبارة عن موجة" bg={K.yellow} size={58} /></Pop>
      {/* vertical film strip with the wave as a soundtrack next to the frames */}
      <div style={{position: 'absolute', left: 540, top: 640, transform: `translateX(-50%) scale(${strip})`, width: 620, height: 1000, overflow: 'hidden'}}>
        <div style={{position: 'absolute', top: -off}}>
          <Strip vertical frames={Array(6).fill(PJ + 'img/poster.jpg')} fw={420} fh={300} holes={4} gap={12}
            render={() => null} />
          <svg width={620} height={2000} style={{position: 'absolute', left: 0, top: 0}}>
            {Array.from({length: 6}, (_, i) => (
              <g key={i}>
                <rect x={78} y={i * 312 + 6} width={330} height={300} fill="#3a342c" />
                <g transform={`translate(${243},${i * 312 + 290}) scale(0.9)`}><line x1={-150} y1={0} x2={150} y2={0} stroke={K.paper} strokeWidth={6} /></g>
              </g>
            ))}
            <path d={Array.from({length: 200}, (_, i) => `${i ? 'L' : 'M'}${470 + wave(i * 10 + off) * 40},${i * 10}`).join(' ')} stroke={K.white} strokeWidth={36} fill="none" opacity={0.95} />
          </svg>
        </div>
      </div>
      <Pop at={tSide + 6} x={760} y={1560} rot={4}><Tag text="جنب الصورة على الشريط" bg={K.red} color={K.white} size={50} /></Pop>
    </Scene>
  );
};
