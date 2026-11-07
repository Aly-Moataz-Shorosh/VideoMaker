import React from 'react';
import {Easing, Img, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, G, Glass, lin, Pill, spr} from '../glass/kit';
import {bi} from './kit';

// More explaining scenes for the film-making course shorts (2026-11-07, Aly: "عايزك تبدع"). All of them live inside the stage
// (y 560..1370) so they never touch his round webcam strip above it or the captions under it.
const GOLD = '#FFC21A', RED = '#E5232B', BLUE = '#3BA9F5', INK = '#14181F';
const fl = (n: string) => staticFile(`fluent/${n}.png`);

const Tag: React.FC<{text: string; y: number; at: number; c?: string; size?: number}> = ({text, y, at, c = GOLD, size: s0 = 48}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (f < at) return null;
  const size = Math.min(s0, Math.floor(920 / (text.length * 0.6 + 1)));
  const p = spr(f, fps, at, 180, 13);
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: y, display: 'flex', justifyContent: 'center', opacity: Math.min(1, p * 1.5), transform: `scale(${0.6 + 0.4 * p})`}}>
      <div style={{padding: '10px 28px', borderRadius: 34, background: 'rgba(10,12,18,0.92)', border: `3px solid ${c}`, fontFamily: AR, fontWeight: 900, fontSize: size,
        color: '#fff', direction: 'rtl', whiteSpace: 'nowrap', boxShadow: `0 0 34px ${c}55`}}>{bi(text)}</div>
    </div>
  );
};
const tagsAt = (f: number, fps: number, tags: {t: number; text: string; c?: string}[], y: number) => {
  const t = [...tags].reverse().find((q) => f >= q.t * fps);
  return t ? <Tag key={t.t} text={t.text} y={y} at={Math.round(t.t * fps)} c={t.c ?? GOLD} /> : null;
};
const keyAt = <T,>(f: number, fps: number, keys: [number, T][]) => { let i = 0; while (i + 1 < keys.length && f >= keys[i + 1][0] * fps) i++; return {i, k: keys[i]}; };
const ease = (f: number, fps: number, t: number) => lin(f, t * fps, t * fps + 16, 0, 1, Easing.inOut(Easing.cubic));
const Frame: React.FC<{dur: number; children: React.ReactNode; h?: number}> = ({dur, children, h = 800}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 140, 16), o = 1 - lin(f, dur - 8, dur);
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, opacity: Math.min(1, p * 1.4) * o}}>
      <div style={{position: 'absolute', left: 40, top: 560, transform: `translateY(${(1 - p) * 40}px)`}}><Glass w={1000} h={h} pad={0} r={40} glow={GOLD}><div /></Glass></div>
      {children}
    </div>
  );
};
const Person: React.FC<{c?: string}> = ({c = '#E9EEF5'}) => (
  <g>
    <circle cx={0} cy={-170} r={34} fill={c} />
    <path d="M -46 -126 Q 0 -140 46 -126 L 56 -10 L 26 -10 L 22 90 L -22 90 L -26 -10 L -56 -10 Z" fill={c} />
    <rect x={-24} y={90} width={18} height={70} rx={8} fill={c} /><rect x={6} y={90} width={18} height={70} rx={8} fill={c} />
  </g>
);
const CamIco: React.FC<{c?: string}> = ({c = GOLD}) => (
  <g><rect x={-46} y={-30} width={78} height={60} rx={12} fill={c} /><path d="M 32 -16 L 62 -32 L 62 32 L 32 16 Z" fill={c} />
    <circle cx={-26} cy={-38} r={14} fill={c} /><circle cx={6} cy={-38} r={14} fill={c} /></g>
);

// ---------- focus: near person + far tree; shallow / deep / far / split diopter / fake (two halves glued) ----------
export const FocusScene: React.FC<{dur: number; keys?: [number, string][]; tags?: {t: number; text: string; c?: string}[]}> = ({dur, keys = [[0, 'shallow']], tags = []}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const val = (m: string) => ({shallow: [0, 14], deep: [0, 0], far: [14, 0], split: [0, 0], fake: [0, 0]} as Record<string, number[]>)[m] ?? [0, 0];
  const {i, k} = keyAt(f, fps, keys);
  const prev = keys[Math.max(0, i - 1)][1], u = i ? ease(f, fps, k[0]) : 1;
  const [nb, fb] = [0, 1].map((j) => val(prev)[j] + (val(k[1])[j] - val(prev)[j]) * u);
  const mode = k[1];
  const names: Record<string, string> = {shallow: 'Shallow focus · الخلفية مغبشة', deep: 'Deep focus · كله واضح', far: 'Rack focus · الفوكس اتنقل', split: 'Split diopter · الاتنين واضحين', fake: 'كنت فاكرهم بيلزقوا صورتين ✗'};
  const X0 = 90, Y0 = 680, W = 900, H = 470;
  return (
    <Frame dur={dur}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 590, display: 'flex', justifyContent: 'center'}}>
        <Pill text={names[mode] ?? mode} size={40} color={mode === 'fake' ? RED : GOLD} ink={mode === 'fake' ? '#fff' : INK} />
      </div>
      <div style={{position: 'absolute', left: X0, top: Y0, width: W, height: H, borderRadius: 26, overflow: 'hidden', border: `5px solid ${GOLD}`, background: 'linear-gradient(180deg,#25456E,#152238 60%,#2A2A2A 60%,#1A1A1A)'}}>
        {/* far: tree + small person */}
        <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0, filter: `blur(${mode === 'split' ? 0 : fb}px)`}}>
          <rect x={640} y={140} width={26} height={150} fill="#6B4A2B" /><circle cx={653} cy={130} r={78} fill="#2E8B57" /><circle cx={610} cy={170} r={50} fill="#3DA06A" /><circle cx={700} cy={168} r={52} fill="#3DA06A" />
          <g transform="translate(780 270) scale(0.55)"><Person c="#F5B83D" /></g>
        </svg>
        {/* near: big person on the left */}
        <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0, filter: `blur(${mode === 'split' ? 0 : nb}px)`}}>
          <g transform="translate(230 330) scale(1.45)"><Person /></g>
        </svg>
        {mode === 'split' ? <div style={{position: 'absolute', left: 430, top: 0, width: 90, height: H, backdropFilter: 'blur(10px)', background: 'rgba(255,255,255,0.05)'}} /> : null}
        {mode === 'fake' ? <div style={{position: 'absolute', left: 470, top: 0, width: 6, height: H, background: RED, boxShadow: `0 0 20px ${RED}`}} /> : null}
      </div>
      {/* side view under the frame: camera -> near -> far, gold line = where the focus is */}
      <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
        <line x1={150} y1={1265} x2={950} y2={1265} stroke="rgba(255,255,255,0.3)" strokeWidth={4} />
        <g transform="translate(170 1235) scale(0.6)"><CamIco /></g>
        <circle cx={420} cy={1245} r={18} fill="#E9EEF5" /><circle cx={800} cy={1245} r={18} fill="#F5B83D" />
        {(nb < 4 || mode === 'split' ? [420] : []).concat(fb < 4 || mode === 'split' ? [800] : []).map((x) => (
          <line key={x} x1={x} y1={1195} x2={x} y2={1295} stroke={GOLD} strokeWidth={6} strokeLinecap="round" style={{filter: `drop-shadow(0 0 8px ${GOLD})`}} />))}
        <text x={420} y={1330} textAnchor="middle" fill="#fff" fontFamily={AR} fontWeight={800} fontSize={26}>قريب</text>
        <text x={800} y={1330} textAnchor="middle" fill="#fff" fontFamily={AR} fontWeight={800} fontSize={26}>بعيد</text>
      </svg>
      {tagsAt(f, fps, tags, 1170)}
    </Frame>
  );
};

// ---------- the cut makes the meaning: shot A (a man looking) + shot B (a train) = "he is looking at the train" ----------
export const CutMeaning: React.FC<{dur: number; mode?: string; bAt?: number; result?: string; resultAt?: number}> = ({dur, mode = 'train', bAt = 0.35, result = '= بيبص على القطر', resultAt = 0.7}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const tb = Math.round(dur * bAt), tr = Math.round(dur * resultAt);
  const pa = spr(f, fps, 6, 150, 15), pb = spr(f, fps, tb, 150, 15), cut = lin(f, tb - 8, tb) * (1 - lin(f, tb, tb + 10));
  const shot = (x: number, label: string, p: number, child: React.ReactNode) => (
    <div style={{position: 'absolute', left: x, top: 650, width: 430, opacity: Math.min(1, p * 1.5), transform: `translateY(${(1 - p) * 50}px)`}}>
      <div style={{position: 'relative', width: 430, height: 300, borderRadius: 22, overflow: 'hidden', border: `5px solid ${GOLD}`, background: 'linear-gradient(180deg,#2B3A55,#1A2233)'}}>{child}</div>
      <div style={{marginTop: 10, textAlign: 'center', fontFamily: AR, fontWeight: 900, fontSize: 34, color: '#fff', direction: 'rtl'}}>{bi(label)}</div>
    </div>
  );
  return (
    <Frame dur={dur}>
      {shot(80, 'لقطة 1: واحد بيبص', pa, (
        <svg width={430} height={300}><g transform="translate(150 250) scale(0.9)"><Person /></g>
          <line x1={175} y1={95} x2={420} y2={95} stroke={GOLD} strokeWidth={4} strokeDasharray="12 10" /><circle cx={182} cy={95} r={6} fill={INK} /></svg>))}
      {mode === 'music' ? shot(570, 'لقطة 2: موسيقى', pb, (
        <>{[0, 1, 2].map((i) => <Img key={i} src={fl(i % 2 ? 'musical_note' : 'musical_notes')} style={{position: 'absolute', left: 60 + i * 120, top: 120 + 40 * Math.sin(f / 9 + i), width: 110, height: 110}} />)}</>))
        : shot(570, 'لقطة 2: قطر بيعدي', pb, (() => {
          const u = ((Math.max(0, f - tb) / (2.6 * fps)) % 1), sc = 0.12 + 1.9 * u * u;  // far -> near, accelerating
          const cx = 300 - 250 * u * u, cy = 95 + 150 * u * u;                         // along the rails to the bottom-left
          return (<>
            <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(180deg,#4A6A95 0%,#2B3A55 38%,#3A3328 38%,#241F18 100%)'}} />
            <svg width={430} height={300} style={{position: 'absolute', left: 0, top: 0}}>
              <path d="M 300 92 L -40 300 M 312 92 L 120 300" stroke="#9AA3AE" strokeWidth={5} />
              {Array.from({length: 9}).map((_, i) => { const v = (i / 9 + (f / 40) % (1 / 9)) ** 2; return <line key={i} x1={300 - 330 * v} y1={92 + 208 * v} x2={312 - 182 * v} y2={92 + 208 * v} stroke="#6B5A44" strokeWidth={2 + 8 * v} />; })}
            </svg>
            <Img src={fl('train')} style={{position: 'absolute', left: cx - 110 * sc, top: cy - 110 * sc, width: 220 * sc, height: 220 * sc, filter: `blur(${u > 0.85 ? 2 : 0}px)`}} />
          </>);
        })())}
      <div style={{position: 'absolute', left: 510, top: 760, width: 60, height: 60, opacity: f >= tb - 10 ? 1 : 0, transform: `scale(${1 + cut})`}}>
        <Img src={fl('scissors')} style={{width: 60, height: 60}} /></div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 1040, display: 'flex', justifyContent: 'center', opacity: lin(f, tb, tb + 10)}}>
        <Pill text="✂ قطع" size={40} color="rgba(10,14,22,0.9)" ink="#fff" glow={false} /></div>
      <Tag text={result} y={1160} at={tr} size={56} c={G.green} />
    </Frame>
  );
};

// ---------- camera moves on a tripod: static / tilt / pan / push / dolly zoom (+ what the camera sees) ----------
export const MoveScene: React.FC<{dur: number; keys?: [number, string][]; tags?: {t: number; text: string; c?: string}[]; cam?: {file: string; from: number} | null; cin?: boolean; cout?: boolean}> = ({dur, keys = [[0, 'static']], tags = [], cam = null}) => {
  const NOTE: Record<string, [string, string][]> = {
    intro: [['⬅ ➡', 'يمين وشمال'], ['⬆ ⬇', 'فوق وتحت'], ['🎥', 'قدام وورا']],
    static: [['🔒', 'الكاميرا مش بتتحرك'], ['👁', 'المتفرج بيركز في اللي جوه الكادر']],
    tilt: [['⬆', 'تبص لفوق'], ['⬇', 'تبص لتحت'], ['📍', 'الترايبود ثابت مكانه']],
    pan: [['⬅', 'تلف شمال'], ['➡', 'تلف يمين'], ['📍', 'الترايبود ثابت مكانه']],
    push: [['🎥 ➡', 'الكاميرا نفسها بتقرّب'], ['🧍', 'الشخص بيكبر في الكادر']],
    dolly: [['🎥 ⬅', 'الكاميرا بترجع لورا'], ['🔍 ➕', 'وزوم لقدام في نفس الوقت'], ['🌀', 'الشخص ثابت.. والخلفية بتتمط']],
  };
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {k} = keyAt(f, fps, keys);
  const m = k[1], t = f - k[0] * fps;
  const osc = Math.sin(t / 16);
  const names: Record<string, string> = {intro: 'Camera movement · حركة الكاميرا', static: 'Static · الكاميرا ثابتة', tilt: 'Tilt · فوق وتحت', pan: 'Pan · يمين وشمال',
    push: 'Push in · تقرّب لقدام', dolly: 'Dolly zoom · ترجع لورا وتعمل زوم'};
  const tilt = m === 'tilt' ? osc * 22 : 0, pan = m === 'pan' ? osc : 0;
  const prog = lin(t, 0, 3 * fps, 0, 1, Easing.inOut(Easing.cubic)) * (m === 'push' || m === 'dolly' ? 1 : 0);
  const tx = m === 'push' ? prog * 120 : m === 'dolly' ? -prog * 120 : 0;
  // preview: push -> subject grows; dolly -> subject same size, background grows; tilt/pan -> view slides
  const subS = m === 'push' ? 1 + prog * 0.8 : 1, bgS = m === 'dolly' ? 1 + prog * 1.2 : m === 'push' ? 1 + prog * 0.4 : 1;
  const vy = m === 'tilt' ? -osc * 60 : 0, vx = m === 'pan' ? -osc * 90 : 0;
  return (
    <Frame dur={dur}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 590, display: 'flex', justifyContent: 'center'}}><Pill text={names[m] ?? m} size={40} /></div>
      <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
        <line x1={80} y1={1300} x2={520} y2={1300} stroke="rgba(255,255,255,0.3)" strokeWidth={4} />
        {m === 'dolly' || m === 'push' ? <path d={`M 120 1318 L 500 1318`} stroke="#8A8F99" strokeWidth={8} strokeDasharray="20 10" /> : null}
        <g transform={`translate(${290 + tx} 0)`}>
          {/* tripod */}
          <line x1={0} y1={980} x2={-90} y2={1300} stroke="#C9D1DC" strokeWidth={10} strokeLinecap="round" />
          <line x1={0} y1={980} x2={90} y2={1300} stroke="#C9D1DC" strokeWidth={10} strokeLinecap="round" />
          <line x1={0} y1={980} x2={0} y2={1300} stroke="#C9D1DC" strokeWidth={10} strokeLinecap="round" />
          <g transform={`translate(0 930) rotate(${-tilt}) scale(${1 - 0.35 * Math.abs(pan)} 1)`}><g transform="scale(1.5)"><CamIco /></g></g>
          {m === 'static' ? <text x={0} y={1080} textAnchor="middle" fontSize={60}>🔒</text> : null}
          {m === 'pan' ? <path d={`M -110 860 Q 0 800 110 860`} fill="none" stroke={GOLD} strokeWidth={6} markerEnd="" /> : null}
          {m === 'tilt' ? <path d={`M 120 860 Q 170 930 120 1000`} fill="none" stroke={GOLD} strokeWidth={6} /> : null}
          {m === 'intro' ? ['M 0 760 L 0 700', 'M 0 1100 L 0 1160', 'M -150 930 L -210 930', 'M 150 930 L 210 930'].map((d, i) => <path key={i} d={d} stroke={GOLD} strokeWidth={10} strokeLinecap="round" opacity={0.5 + 0.5 * Math.sin(f / 6 + i)} />) : null}
        </g>
      </svg>
      {/* his own webcam while he shows the move on the real tripod (whole width: the tripod is at the left edge) */}
      {cam ? <div style={{position: 'absolute', left: 470, top: 650, width: 560, height: 315, borderRadius: 20, overflow: 'hidden', border: `5px solid ${GOLD}`, background: '#000', zIndex: 2}}>
        <OffthreadVideo muted src={staticFile(cam.file)} startFrom={Math.round(cam.from * fps)} style={{width: 560, height: 315}} /></div> : null}
      {/* what the camera sees */}
      <div style={{position: 'absolute', left: 560, top: cam ? 975 : 760, width: 440, height: cam ? 160 : 330, borderRadius: 22, overflow: 'hidden', border: `5px solid ${GOLD}`, background: '#1B2A44'}}>
        <div style={{position: 'absolute', inset: 0, transform: `translate(${vx}px, ${vy}px) scale(${bgS})`}}>
          {Array.from({length: 8}).map((_, i) => <div key={i} style={{position: 'absolute', left: -200 + i * 110, top: -100, width: 50, height: 600, background: 'rgba(255,255,255,0.08)'}} />)}
          <div style={{position: 'absolute', left: -200, right: -200, top: 230, height: 300, background: '#2B2B33'}} />
        </div>
        <svg width={440} height={330} style={{position: 'absolute', left: 0, top: 0}}>
          <g transform={`translate(${220 + vx * 0.4} ${300 + vy}) scale(${0.7 * subS})`}><Person /></g>
        </svg>
        <div style={{position: 'absolute', left: 14, top: 10, fontFamily: EN, fontWeight: 800, fontSize: 24, color: '#fff'}}><span style={{color: RED}}>●</span> REC</div>
      </div>
      <div style={{position: 'absolute', left: 560, top: 1100, width: 440, textAlign: 'center', fontFamily: AR, fontWeight: 800, fontSize: 26, color: G.soft}}>الكاميرا شايفة كده</div>
      <div style={{position: 'absolute', left: 560, top: 1150, width: 440, display: 'flex', flexDirection: 'column', gap: 8, direction: 'rtl'}}>
        {(NOTE[m] ?? []).map(([ic, tx], i) => (<div key={m + i} style={{display: 'flex', alignItems: 'center', gap: 12, opacity: lin(t, 8 + i * 10, 18 + i * 10), fontFamily: AR, fontWeight: 900, fontSize: 30, color: '#fff'}}>
          <span style={{fontSize: 30, minWidth: 70, textAlign: 'center'}}>{ic}</span>{bi(tx)}</div>))}
      </div>
      {tagsAt(f, fps, tags, 1280)}
    </Frame>
  );
};

// ---------- film -> sequences -> scenes -> shots (built while he says it) ----------
export const TreeScene: React.FC<{dur: number; seqAt?: number; sceneAt?: number; shotAt?: number; tags?: {t: number; text: string; c?: string}[]; film?: string}> = ({dur, seqAt = 1, sceneAt = 2.5, shotAt = 4, tags = [], film = 'الفيلم'}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const box = (x: number, y: number, w: number, text: string, sub: string, c: string, at: number, key: string) => {
    const p = spr(f, fps, at * fps, 170, 14);
    if (f < at * fps) return null;
    return (
      <div key={key} style={{position: 'absolute', left: x - w / 2, top: y, width: w, padding: '10px 6px', borderRadius: 18, background: 'rgba(10,14,22,0.92)', border: `4px solid ${c}`, textAlign: 'center',
        opacity: Math.min(1, p * 1.5), transform: `scale(${0.6 + 0.4 * p})`, boxShadow: `0 0 26px ${c}55`}}>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: w > 300 ? 42 : 30, color: '#fff'}}>{bi(text)}</div>
        <div style={{fontFamily: EN, fontWeight: 800, fontSize: w > 300 ? 26 : 20, color: c}}>{sub}</div>
      </div>
    );
  };
  const line = (x1: number, y1: number, x2: number, y2: number, at: number, key: string) => f < at * fps ? null :
    <line key={key} x1={x1} y1={y1} x2={x2} y2={y2} stroke="rgba(255,255,255,0.5)" strokeWidth={4} strokeDasharray={300} strokeDashoffset={300 * (1 - lin(f, at * fps, at * fps + 12))} />;
  const SX = [220, 540, 860], CX = [380, 540, 700], HX = [445, 505, 575, 635];
  return (
    <Frame dur={dur}>
      <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
        {SX.map((x, i) => line(540, 700, x, 790, seqAt, 's' + i))}
        {CX.map((x, i) => line(540, 880, x, 975, sceneAt, 'c' + i))}
        {HX.map((x, i) => line(540, 1065, x, 1160, shotAt, 'h' + i))}
      </svg>
      {box(540, 600, 420, film, 'FILM', GOLD, 0.1, 'f')}
      {SX.map((x, i) => box(x, 790, 250, 'تتابع', 'Sequence', BLUE, seqAt + i * 0.15, 'S' + i))}
      {CX.map((x, i) => box(x, 975, 150, 'مشهد', 'Scene', G.green, sceneAt + i * 0.15, 'C' + i))}
      {HX.map((x, i) => f < (shotAt + i * 0.12) * fps ? null : (
        <div key={'H' + i} style={{position: 'absolute', left: x - 26, top: 1160, width: 52, height: 40, borderRadius: 6, border: `3px solid ${RED}`, background: '#22293A', opacity: spr(f, fps, (shotAt + i * 0.12) * fps, 170, 14)}} />))}
      {f >= shotAt * fps ? <div style={{position: 'absolute', left: 0, right: 0, top: 1210, textAlign: 'center', fontFamily: AR, fontWeight: 900, fontSize: 32, color: RED}}>لقطات · Shots</div> : null}
      {tagsAt(f, fps, tags, 1270)}
    </Frame>
  );
};

// ---------- the film-making process as a vertical pipeline (active step lights up) ----------
export const Pipeline: React.FC<{dur: number; items: {name: string; ar: string; img: string; at: number}[]; hi?: [number, number][]; tags?: {t: number; text: string; c?: string}[]}> = ({dur, items: steps, hi = [], tags = []}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const cur = hi.length ? keyAt(f, fps, hi).k[1] : -1;
  const n = steps.length, gap = Math.min(200, 700 / Math.max(1, n));
  return (
    <Frame dur={dur}>
      {steps.map((s, i) => {
        const p = spr(f, fps, s.at * fps, 170, 14);
        if (f < s.at * fps) return null;
        const on = i === cur, y = 590 + i * gap;
        return (
          <div key={i} style={{position: 'absolute', left: 70, top: y, width: 940, height: gap - 18, display: 'flex', alignItems: 'center', gap: 22, direction: 'rtl', padding: '0 22px', boxSizing: 'border-box',
            borderRadius: 26, background: on ? GOLD : 'rgba(10,14,22,0.85)', border: `3px solid ${on ? '#fff' : 'rgba(255,255,255,0.25)'}`, opacity: Math.min(1, p * 1.5),
            transform: `translateX(${(1 - p) * 80}px) scale(${on ? 1.04 : 1})`, boxShadow: on ? `0 0 40px ${GOLD}99` : 'none'}}>
            <Img src={fl(s.img)} style={{width: gap - 50, height: gap - 50}} />
            <div style={{flex: 1}}>
              <div style={{fontFamily: AR, fontWeight: 900, fontSize: n > 3 ? 40 : 48, color: on ? INK : '#fff'}}>{bi(s.ar)}</div>
              <div style={{fontFamily: EN, fontWeight: 800, fontSize: 26, color: on ? INK : GOLD}}>{s.name}</div>
            </div>
            <div style={{fontFamily: EN, fontWeight: 900, fontSize: 44, color: on ? INK : 'rgba(255,255,255,0.4)'}}>{i + 1}</div>
          </div>
        );
      })}
      {tagsAt(f, fps, tags, 1270)}
    </Frame>
  );
};

// ---------- visual literacy: everyone enjoys it, few can read/write it -> learn the letters of cinema ----------
export const LiteracyScene: React.FC<{dur: number; rows: {img: string; a: string; b: string; at: number}[]; letters?: string[]; lettersAt?: number}> = ({dur, rows, letters = [], lettersAt = 99}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <Frame dur={dur}>
      {rows.map((r, i) => {
        const p = spr(f, fps, r.at * fps, 170, 14), q = spr(f, fps, (r.at + 0.9) * fps, 170, 14);
        if (f < r.at * fps) return null;
        return (
          <div key={i} style={{position: 'absolute', left: 80, top: 620 + i * 230, width: 920, height: 200, display: 'flex', alignItems: 'center', gap: 28, direction: 'rtl', opacity: Math.min(1, p * 1.5), transform: `translateX(${(1 - p) * 80}px)`}}>
            <Img src={fl(r.img)} style={{width: 170, height: 170}} />
            <div style={{flex: 1, display: 'flex', flexDirection: 'column', gap: 6}}>
              <div style={{fontFamily: AR, fontWeight: 900, fontSize: 50, color: '#fff'}}>✓ {bi(r.a)}</div>
              <div style={{fontFamily: AR, fontWeight: 900, fontSize: 50, color: RED, opacity: Math.min(1, q * 1.5)}}>✗ {bi(r.b)}</div>
            </div>
          </div>
        );
      })}
      {letters.length && f >= lettersAt * fps ? (
        <div style={{position: 'absolute', left: 70, right: 70, top: 1110, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: 14, direction: 'rtl'}}>
          {letters.map((l, i) => { const p = spr(f, fps, (lettersAt + i * 0.18) * fps, 200, 12); return (
            <div key={i} style={{padding: '8px 20px', borderRadius: 18, background: GOLD, fontFamily: EN, fontWeight: 900, fontSize: 32, color: INK, transform: `scale(${p})`, direction: 'ltr'}}>{l}</div>); })}
        </div>) : null}
    </Frame>
  );
};

// ---------- aspect ratio: one frame morphing 4:3 -> 16:9 -> 9:16 -> 1:1 ----------
export const AspectScene: React.FC<{dur: number; keys?: [number, string, string][]}> = ({dur, keys = [[0, '4:3', '']]}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const r = (s: string) => { const [a, b] = s.split(':').map(Number); return a / b; };
  const {i, k} = keyAt(f, fps, keys.map((q) => [q[0], q] as [number, [number, string, string]]));
  const prev = keys[Math.max(0, i - 1)], u = i ? ease(f, fps, k[1][0]) : 1;
  const ar = r(prev[1]) + (r(k[1][1]) - r(prev[1])) * u;
  const H = Math.min(560, 820 / ar), W = H * ar;
  return (
    <Frame dur={dur}>
      <div style={{position: 'absolute', left: 540 - W / 2, top: 920 - H / 2, width: W, height: H, borderRadius: 18, border: `6px solid ${GOLD}`, overflow: 'hidden', background: 'linear-gradient(180deg,#25456E,#152238)', boxShadow: `0 0 50px ${GOLD}55`}}>
        <svg width={W} height={H}><g transform={`translate(${W / 2} ${H - 20}) scale(${H / 420})`}><Person /></g></svg>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 1230, display: 'flex', justifyContent: 'center', gap: 18, direction: 'rtl'}}>
        <Pill text={k[1][1]} size={54} font={EN} dir="ltr" />
        {k[1][2] ? <Pill text={k[1][2]} size={44} color="rgba(10,14,22,0.9)" ink="#fff" glow={false} /> : null}
      </div>
    </Frame>
  );
};

export const filmScenes2: Record<string, React.FC<any>> = {FocusScene, CutMeaning, MoveScene, TreeScene, Pipeline, LiteracyScene, AspectScene};
