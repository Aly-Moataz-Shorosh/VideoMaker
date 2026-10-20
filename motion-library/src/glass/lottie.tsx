import React from 'react';
import {AbsoluteFill, Easing, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {useBeats} from '../film/kit';
import {AR, Chip, Cursor, EN, G, GScene, Glass, In, Label, Mark, MONO, Pill, SKey, SMark, Screen, Top, lin, rnd, spr} from './kit';

// "After Effects -> code" short (2026-10-16). Aly's notes: style "2 and 6 and 10" -> one mixed look 'lottie':
// 02 = grainy two-blue risograph background, 10 = frosted glass cards + typing words + gold pill + his face always on,
// 06 = light VHS touches (scanlines, tracking band, PLAY / PAUSE on-screen display, RGB fringe).
// Motif = HIS animation (the circle that fills with red water) rebuilt in vector, so it plays in every scene.
type B = {b?: Record<string, number>; cam?: string; camAt?: number; keys?: SKey[]; marks?: SMark[]; steps?: string[]; qr?: string; n?: string; stepKeys?: string[]; inside?: boolean};
const RED = '#C9564C', ICE = '#DCEEF8', TEAL = '#00DDB3', AE_BG = '#00005B', AE_INK = '#9999FF';

// ---------- background (style 02) + fx (style 06) ----------
export const LottieBg: React.FC = () => {
  const f = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const drift = (sx: number, sy: number, sp: number) =>
    `translate(${Math.sin(f / sp) * sx}px, ${Math.cos(f / (sp * 1.3)) * sy}px) scale(${1.04 + 0.02 * Math.sin(f / (sp * 2))})`;
  const im = (n: string, t: string, op = 1) => <Img src={staticFile(`bg/${n}.png`)} style={{position: 'absolute', inset: 0, width, height, transform: t, opacity: op}} />;
  return (
    <AbsoluteFill style={{background: '#0A2442', overflow: 'hidden'}}>
      {im('base', drift(10, 14, 140))}
      {im('blob_2', drift(40, 30, 95))}
      {im('blob_3', drift(-35, 25, 120))}
      {im('blob_1', drift(-30, 40, 110))}
      {im('blob_4', drift(20, -30, 70))}
      {im(`grain_${Math.floor(f / 2) % 3}`, 'none', 0.5)}
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(5,10,20,0.25), rgba(5,10,20,0.55))'}} />
    </AbsoluteFill>
  );
};

export const LottieFx: React.FC = () => {
  const f = useCurrentFrame();
  const {height, fps} = useVideoConfig();
  const band = ((f * 6) % (height + 400)) - 200;
  const s = Math.floor(f / fps);
  const tc = `0:${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <AbsoluteFill style={{opacity: 0.1, backgroundImage: 'repeating-linear-gradient(0deg, rgba(0,0,0,0.9) 0px, rgba(0,0,0,0.9) 2px, transparent 2px, transparent 5px)'}} />
      <div style={{position: 'absolute', left: 0, right: 0, top: band, height: 70, opacity: 0.07, background: 'linear-gradient(180deg, transparent, rgba(255,255,255,0.6) 45%, transparent)', filter: 'blur(2px)'}} />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, transparent 60%, rgba(2,6,14,0.5) 100%)'}} />
      <div style={{position: 'absolute', left: 40, top: 30, fontFamily: EN, fontWeight: 800, fontSize: 26, color: '#F2F2EE', letterSpacing: 2, direction: 'ltr', opacity: 0.7,
        textShadow: '2px 0 #FF3EA5aa, -2px 0 #33E1FFaa'}}>▶ PLAY <span style={{marginLeft: 14, opacity: 0.8}}>SP {tc}</span></div>
    </AbsoluteFill>
  );
};

// ---------- his animation, in vector: a circle that fills with red water (wave on top) + the red stripe ----------
export const Liquid: React.FC<{d?: number; level: number; stripe?: boolean}> = ({d = 420, level, stripe = true}) => {
  const f = useCurrentFrame();
  const id = React.useId().replace(/:/g, '');
  const y0 = d * (1 - Math.max(0, Math.min(1, level)));
  const amp = d * 0.035 * (level > 0.02 && level < 0.98 ? 1 : 0.3);
  let path = `M ${-20} ${d + 20} L ${-20} ${y0}`;
  for (let x = -20; x <= d + 20; x += 10) path += ` L ${x} ${y0 + amp * Math.sin(x / (d * 0.12) + f / 5)}`;
  path += ` L ${d + 20} ${d + 20} Z`;
  return (
    <svg width={d} height={d} viewBox={`0 0 ${d} ${d}`} style={{overflow: 'visible', filter: 'drop-shadow(0 20px 40px rgba(0,0,0,0.45))'}}>
      <defs><clipPath id={id}><circle cx={d / 2} cy={d / 2} r={d / 2} /></clipPath></defs>
      <g clipPath={`url(#${id})`}>
        <rect width={d} height={d} fill={ICE} />
        {stripe ? <rect x={d * 0.455} y={0} width={d * 0.09} height={d} fill={RED} /> : null}
        <path d={path} fill={RED} />
      </g>
    </svg>
  );
};

// ---------- logos / icons (vector) ----------
export const AeLogo: React.FC<{s?: number}> = ({s = 1}) => (
  <div style={{width: 190 * s, height: 185 * s, borderRadius: 36 * s, background: AE_BG, border: `${6 * s}px solid ${AE_INK}`, boxSizing: 'border-box',
    display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: `0 20px 60px ${AE_INK}66`}}>
    <span style={{fontFamily: EN, fontWeight: 700, fontSize: 104 * s, color: AE_INK, letterSpacing: -2 * s}}>Ae</span>
  </div>
);
export const LottieLogo: React.FC<{s?: number}> = ({s = 1}) => (
  <div style={{width: 190 * s, height: 190 * s, borderRadius: 44 * s, background: TEAL, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: `0 20px 60px ${TEAL}66`}}>
    <svg width={120 * s} height={120 * s} viewBox="0 0 100 100"><path d="M78 22 C 52 20 50 46 44 60 C 38 74 30 80 20 80" fill="none" stroke="#fff" strokeWidth={13} strokeLinecap="round" /></svg>
  </div>
);
export const GitHubMark: React.FC<{s?: number; color?: string}> = ({s = 1, color = '#fff'}) => (
  <svg width={110 * s} height={110 * s} viewBox="0 0 24 24"><path fill={color} d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" /></svg>
);
const Android: React.FC<{s?: number}> = ({s = 1}) => (
  <svg width={150 * s} height={150 * s} viewBox="0 0 100 100">
    <path d="M18 62 A32 32 0 0 1 82 62 Z" fill="#3DDC84" />
    <line x1={30} y1={30} x2={22} y2={18} stroke="#3DDC84" strokeWidth={5} strokeLinecap="round" />
    <line x1={70} y1={30} x2={78} y2={18} stroke="#3DDC84" strokeWidth={5} strokeLinecap="round" />
    <circle cx={36} cy={47} r={4.5} fill="#0A2442" /><circle cx={64} cy={47} r={4.5} fill="#0A2442" />
  </svg>
);
const Globe: React.FC<{s?: number}> = ({s = 1}) => (
  <svg width={140 * s} height={140 * s} viewBox="0 0 100 100" fill="none" stroke={G.blue} strokeWidth={6}>
    <circle cx={50} cy={50} r={42} /><ellipse cx={50} cy={50} rx={18} ry={42} /><line x1={8} y1={50} x2={92} y2={50} /><path d="M16 28 H84 M16 72 H84" />
  </svg>
);
const Xampp: React.FC<{s?: number}> = ({s = 1}) => (
  <div style={{width: 170 * s, height: 170 * s, borderRadius: 38 * s, background: '#FB7A24', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 20px 60px #FB7A2466'}}>
    <svg width={110 * s} height={110 * s} viewBox="0 0 100 100"><path d="M20 20 L80 80 M80 20 L20 80" stroke="#fff" strokeWidth={16} strokeLinecap="round" /></svg>
  </div>
);
// file icon with a coloured badge (json / js / html / zip / zxp)
export const FileIcon: React.FC<{ext: string; color: string; name?: string; s?: number; zip?: boolean}> = ({ext, color, name, s = 1, zip}) => (
  <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14 * s}}>
    <div style={{position: 'relative', width: 170 * s, height: 210 * s}}>
      <svg width={170 * s} height={210 * s} viewBox="0 0 170 210">
        <path d="M10 10 H120 L160 50 V200 H10 Z" fill="rgba(255,255,255,0.92)" stroke="#fff" strokeWidth={4} />
        <path d="M120 10 V50 H160" fill="#C9D1DC" />
        {zip ? [0, 1, 2, 3, 4, 5].map((i) => <rect key={i} x={i % 2 ? 78 : 70} y={20 + i * 14} width={12} height={10} fill="#7C8797" />) : null}
      </svg>
      <div style={{position: 'absolute', left: 6 * s, bottom: 30 * s, padding: `${4 * s}px ${14 * s}px`, borderRadius: 12 * s, background: color, color: '#fff',
        fontFamily: EN, fontWeight: 900, fontSize: 38 * s, direction: 'ltr'}}>{ext}</div>
    </div>
    {name ? <span style={{fontFamily: MONO, fontWeight: 700, fontSize: 34 * s, color: G.ink, direction: 'ltr', textShadow: '0 4px 16px rgba(0,0,0,0.6)'}}>{name}</span> : null}
  </div>
);

// ---------- vector browser + buttons ----------
const Btn: React.FC<{label: string; down?: boolean; color?: string}> = ({label, down, color = G.blue}) => (
  <div style={{padding: '14px 34px', borderRadius: 18, background: down ? color : '#F2F4F7', color: down ? '#fff' : '#14181F', fontFamily: EN, fontWeight: 900, fontSize: 36,
    border: `3px solid ${down ? color : '#C9D1DC'}`, transform: `scale(${down ? 0.94 : 1})`, boxShadow: down ? `0 0 30px ${color}AA` : '0 6px 14px rgba(0,0,0,0.2)', direction: 'ltr'}}>{label}</div>
);
export const Browser: React.FC<{w?: number; h?: number; url?: string; children?: React.ReactNode}> = ({w = 900, h = 720, url = 'localhost/live.html', children}) => (
  <div style={{width: w, height: h, borderRadius: 34, overflow: 'hidden', background: '#fff', boxShadow: '0 40px 90px rgba(0,0,0,0.55), 0 0 0 3px rgba(255,255,255,0.35)', position: 'relative'}}>
    <div style={{height: 76, background: '#E6EAF0', display: 'flex', alignItems: 'center', gap: 12, padding: '0 24px', direction: 'ltr'}}>
      {['#FF5F57', '#FEBC2E', '#28C840'].map((c) => <div key={c} style={{width: 20, height: 20, borderRadius: '50%', background: c}} />)}
      <div style={{marginLeft: 18, flex: 1, height: 44, borderRadius: 22, background: '#fff', display: 'flex', alignItems: 'center', padding: '0 22px', fontFamily: EN, fontSize: 26, color: '#4A5361'}}>🔒 {url}</div>
    </div>
    <div style={{position: 'absolute', top: 76, left: 0, right: 0, bottom: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 34, direction: 'ltr'}}>{children}</div>
  </div>
);

// ---------- clean vector code editor: lines type in on his words ----------
type Ln = {at: number; text: string; ind?: number; hi?: boolean};
const KW = /^(var|function|true|false|document)$/;
const tokens = (t: string) => t.split(/("[^"]*"?|<\/?[a-zA-Z]+|[{}()>;,.:=]|\s+)/).filter(Boolean);
const colour = (tk: string, next: string) => {
  if (tk.startsWith('"')) return '#CE9178';
  if (tk.startsWith('<')) return '#569CD6';
  if (KW.test(tk)) return '#569CD6';
  if (/^[{}()]$/.test(tk)) return '#FFD700';
  if (next === ':') return '#9CDCFE';
  if (/^[A-Za-z]+$/.test(tk) && next === '(') return '#DCDCAA';
  return '#D4D4D4';
};
export const Code: React.FC<{lines: Ln[]; w?: number; file?: string; size?: number; cps?: number}> = ({lines, w = 1000, file = 'live.html', size = 34, cps = 2.2}) => {
  const f = useCurrentFrame();
  return (
    <div style={{width: w, borderRadius: 30, overflow: 'hidden', background: 'rgba(20,22,28,0.94)', boxShadow: '0 40px 90px rgba(0,0,0,0.55), 0 0 0 2px rgba(255,255,255,0.18), 0 0 70px #3BA9F533', direction: 'ltr'}}>
      <div style={{height: 64, background: '#2A2D35', display: 'flex', alignItems: 'center', gap: 12, padding: '0 22px'}}>
        {['#FF5F57', '#FEBC2E', '#28C840'].map((c) => <div key={c} style={{width: 18, height: 18, borderRadius: '50%', background: c}} />)}
        <div style={{marginLeft: 16, padding: '8px 20px', borderRadius: 12, background: '#1E1E1E', fontFamily: MONO, fontSize: 26, color: '#E8C26E'}}>{file}</div>
      </div>
      <div style={{padding: '18px 0 24px'}}>
        {lines.map((l, i) => {
          if (f < l.at) return null;
          const n = Math.floor((f - l.at) * cps);
          const txt = l.text.slice(0, n);
          const typing = n < l.text.length;
          const tk = tokens(txt);
          const glow = l.hi && f < l.at + l.text.length / cps + 40;
          return (
            <div key={i} style={{display: 'flex', alignItems: 'center', minHeight: size * 1.5, background: glow ? 'rgba(245,184,61,0.16)' : undefined, borderLeft: `6px solid ${glow ? G.gold : 'transparent'}`}}>
              <span style={{width: 70, textAlign: 'right', paddingRight: 22, fontFamily: MONO, fontSize: size * 0.8, color: '#5A6270'}}>{i + 1}</span>
              <span style={{fontFamily: MONO, fontSize: size, whiteSpace: 'pre', paddingLeft: (l.ind ?? 0) * size * 1.2}}>
                {tk.map((t, j) => <span key={j} style={{color: colour(t, (tk.slice(j + 1).find((x) => x.trim()) ?? '').trim())}}>{t}</span>)}
                {typing ? <span style={{display: 'inline-block', width: 3, height: size, background: '#fff', verticalAlign: 'middle'}} /> : null}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// ---------- his REAL screen in the glass card ----------
const Stage: React.FC<{p: B; y?: number; w?: number; h?: number; at?: number; out?: number}> = ({p, y = 600, w = 1020, h = 860, at = 4, out}) =>
  p.cam && p.keys ? <In at={at} out={out} x={540} y={y}><Screen file={p.cam} startFrom={p.camAt ?? 0} keys={p.keys} marks={p.marks} w={w} h={h} /></In> : null;

// arrow that draws itself between two points
const Arrow: React.FC<{x1: number; y1: number; x2: number; y2: number; at: number; color?: string}> = ({x1, y1, x2, y2, at, color = G.gold}) => {
  const f = useCurrentFrame();
  const p = lin(f, at, at + 14);
  if (p <= 0) return null;
  const x = x1 + (x2 - x1) * p, y = y1 + (y2 - y1) * p;
  const a = Math.atan2(y2 - y1, x2 - x1);
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible', pointerEvents: 'none'}}>
      <line x1={x1} y1={y1} x2={x} y2={y} stroke={color} strokeWidth={10} strokeLinecap="round" strokeDasharray="2 22" />
      {p > 0.95 ? <path d={`M ${x2} ${y2} l ${-36 * Math.cos(a - 0.5)} ${-36 * Math.sin(a - 0.5)} M ${x2} ${y2} l ${-36 * Math.cos(a + 0.5)} ${-36 * Math.sin(a + 0.5)}`} stroke={color} strokeWidth={10} strokeLinecap="round" fill="none" /> : null}
    </svg>
  );
};

// ================= scenes =================
// 0. HOOK: his real result (Play -> water fills, Pause -> it stops) rebuilt big + "this was made in After Effects... now it's code"
export const LtHook: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const play = at('play', 0.8), pause = at('pause', 2.6), ctl = at('ctl', 3.6);
  const level = f < play ? 0.06 : lin(f, play, play + 110, 0.06, 1, Easing.inOut(Easing.sin));
  const lv = f < pause ? level : lin(pause, play, play + 110, 0.06, 1, Easing.inOut(Easing.sin));
  return (
    <GScene>
      <Top text="أنيميشن *After_Effects* ⬅ بقى [كود]" at={2} y={70} size={66} />
      <In at={4} x={540} y={640}>
        <Browser w={900} h={780}>
          <Liquid d={430} level={lv} />
          <div style={{display: 'flex', gap: 30}}>
            <Btn label="▶ PLAY" down={f >= play && f < play + 8} color={G.green} />
            <Btn label="❚❚ PAUSE" down={f >= pause && f < pause + 8} color={G.red} />
          </div>
        </Browser>
      </In>
      {f >= play - 10 && f < pause + 20 ? <Cursor x={f < pause - 12 ? 395 : 395 + lin(f, pause - 12, pause - 2, 0, 250)} y={f < play ? 990 + (play - f) * 4 : 990} click={f < pause - 12 ? play : pause} /> : null}
      {f >= play ? <In at={play} x={300} y={1150}><Pill text="▶ PLAY = اشتغل" color={G.green} ink="#fff" size={44} /></In> : null}
      {f >= pause ? <In at={pause} x={760} y={1150}><Pill text="PAUSE = وقف ❚❚" color={G.red} ink="#fff" size={44} /></In> : null}
      {f >= ctl ? <In at={ctl} x={420} y={1260}><Pill text="تتحكم فيه بالكود 🎮" size={48} /></In> : null}
    </GScene>
  );
};

// 1. what we'll do: AE animation -> code -> Android app / website (his big webcam under it)
export const LtIntro: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const ae = at('ae', 1.9), code = at('code', 3.2), and = at('android', 4.4), web = at('web', 5.9);
  return (
    <GScene>
      <Top text="من *After_Effects* لـ [كود]" at={2} y={80} size={70} />
      <In at={ae} x={250} y={400}><AeLogo s={1.1} /></In>
      <Arrow x1={380} y1={400} x2={690} y2={400} at={code - 8} />
      <In at={code} x={840} y={400}><FileIcon ext="{ }" color={G.royal} name="code" s={0.95} /></In>
      <Arrow x1={840} y1={560} x2={620} y2={760} at={and - 10} color={G.blue} />
      <Arrow x1={840} y1={560} x2={900} y2={760} at={web - 10} color={G.blue} />
      <In at={and} x={500} y={860}><div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6}}><Android s={1} /><Label text="Android App" font={EN} dir="ltr" size={38} /></div></In>
      <In at={web} x={880} y={860}><div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6}}><Globe s={0.9} /><Label text="Website" font={EN} dir="ltr" size={38} /></div></In>
    </GScene>
  );
};

// 2. tip: the Wave Warp EFFECT does not go into the code -> draw the wave in the shape itself
export const LtTip: React.FC<B> = (p) => {
  const f = useCurrentFrame();
  const at = useBeats(p.b);
  const fx = at('fx', 3.3), nw = at('new', 5.5), wave = at('wave', 9.5);
  return (
    <GScene>
      <Chip n="!" en="Tip" ar="الإفكتات مش بتتحول" color={G.red} at={2} y={40} />
      <Stage p={p} y={560} h={700} />
      {f >= fx && f < nw ? <In at={fx} x={540} y={1010}><Pill text="Wave Warp ✕ = خط مستقيم" color={G.red} ink="#fff" size={48} font={EN} dir="ltr" /></In> : null}
      {f >= nw ? <In at={nw} x={540} y={1010}><Pill text="✓ ارسم الموجة في الـ Shape نفسه" color={G.green} ink="#fff" size={46} /></In> : null}
      {f >= wave ? <In at={wave} x={190} y={1180}><Liquid d={190} level={0.55} /></In> : null}
    </GScene>
  );
};

// 3. the plugin: Bodymovin, open source, free, on GitHub
export const LtPlugin: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const free = at('free', 2.8), name = at('name', 6.2), gh = at('gh', 7.5);
  return (
    <GScene>
      <Top text="البلجن *ببلاش* و Open Source" at={2} y={90} size={66} />
      <In at={6} x={540} y={430}><LottieLogo s={1.3} /></In>
      {f >= free ? <In at={free} x={290} y={680}><Pill text="$0 ✓" color={G.green} ink="#fff" size={58} font={EN} dir="ltr" /></In> : null}
      {f >= free + 6 ? <In at={free + 6} x={780} y={680}><Pill text="Open Source" color={G.blue} ink="#fff" size={50} font={EN} dir="ltr" /></In> : null}
      {f >= name ? <In at={name} x={540} y={850}><Pill text="Bodymovin" color={TEAL} ink="#06302A" size={84} font={EN} dir="ltr" /></In> : null}
      {f >= gh ? <In at={gh} x={540} y={1050}><div style={{display: 'flex', alignItems: 'center', gap: 22}}><GitHubMark s={0.8} /><Label text="GitHub" font={EN} dir="ltr" size={56} /></div></In> : null}
    </GScene>
  );
};

// 4. install: $0 cart -> rename .zxp to .zip -> extract into ...\Support Files\extensions
export const LtInstall: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const zip = at('zip', 3.3), z2 = at('z2', 5.5), path = at('path', 6.4);
  const pp = [path, at('p2', 7.9), at('p3', 9.3), at('p4', 13)];
  const parts = ['E:', 'Adobe After Effects', 'Support Files', 'extensions'];
  return (
    <GScene>
      <Chip n="01" en="Install" ar="تسطيب البلجن" color={G.gold} at={2} y={40} />
      {f < zip ? (
        <>
          <In at={4} x={540} y={420}>
            <Glass w={760} pad={40}>
              <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', direction: 'ltr'}}>
                <LottieLogo s={0.6} />
                <div style={{position: 'relative', fontFamily: EN, fontWeight: 900, fontSize: 96, color: G.soft}}>
                  $20<div style={{position: 'absolute', left: -10, right: -10, top: '52%', height: 10, background: G.red, transform: `scaleX(${lin(f, 20, 34)})`, transformOrigin: 'left'}} />
                </div>
                <span style={{fontFamily: EN, fontWeight: 900, fontSize: 96, color: G.green, opacity: lin(f, 34, 42)}}>$0</span>
              </div>
            </Glass>
          </In>
          <In at={40} x={540} y={680}><Btn label="🛒 Add to Cart" down={f >= 60 && f < 70} color={G.gold} /></In>
          {f >= 50 ? <Cursor x={600} y={700} click={60} /> : null}
        </>
      ) : f < path ? (
        <>
          <In at={zip} x={540} y={430}><FileIcon ext={f < z2 - 6 ? '.zxp' : '.zip'} color={f < z2 - 6 ? '#7C3AED' : G.gold} zip={f >= z2 - 6} name={f < z2 - 6 ? 'bodymovin.zxp' : 'bodymovin.zip'} s={1.4} /></In>
          {f >= zip + 8 ? <In at={zip + 8} x={540} y={800}><Pill text="Rename: .zxp → .zip" size={50} font={EN} dir="ltr" /></In> : null}
        </>
      ) : (
        <>
          <Top text="فُكّه هنا 📂" at={path} y={150} size={70} />
          {parts.map((t, i) => (f >= pp[i] ? (
            <In key={t} at={pp[i]} x={540} y={330 + i * 175}>
              <Glass w={i === 3 ? 760 : 680} pad={22} r={30} glow={i === 3 ? G.gold : undefined}>
                <div style={{display: 'flex', alignItems: 'center', gap: 22, direction: 'ltr'}}>
                  <span style={{fontSize: 56}}>{i === 0 ? '💽' : '📁'}</span>
                  <span style={{fontFamily: EN, fontWeight: 800, fontSize: 46, color: i === 3 ? G.gold : G.ink}}>{t}</span>
                </div>
              </Glass>
            </In>) : null))}
          {f >= pp[3] + 4 ? <In at={pp[3] + 4} x={540} y={1080}><FileIcon ext="{ }" color={TEAL} name="bodymovin" s={0.6} /></In> : null}
        </>
      )}
    </GScene>
  );
};

// 5. export: Window > Extensions > Bodymovin -> Selected -> destination -> Render = .json (his real AE screen)
const Steps: React.FC<{items: string[]; ats: number[]; y?: number}> = ({items, ats, y = 1110}) => {
  const f = useCurrentFrame();
  let cur = 0;
  ats.forEach((t, i) => { if (f >= t) cur = i; });
  return (
    <In at={ats[0]} x={480} y={y}>
      <div style={{display: 'flex', alignItems: 'center', gap: 16, direction: 'rtl'}}>
        <div style={{width: 64, height: 64, borderRadius: '50%', background: G.gold, color: '#14181F', fontFamily: EN, fontWeight: 900, fontSize: 34,
          display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${spr(f, 30, ats[cur], 220, 12)})`}}>{cur + 1}</div>
        <span key={cur} style={{fontFamily: AR, fontWeight: 800, fontSize: 44, color: G.ink, opacity: lin(f, ats[cur], ats[cur] + 8), textShadow: '0 4px 20px rgba(0,0,0,0.6)'}}>{items[cur]}</span>
      </div>
    </In>
  );
};
export const LtExport: React.FC<B> = (p) => {
  const f = useCurrentFrame();
  const at = useBeats(p.b);
  const json = at('json', 11);
  const steps = p.steps ?? [];
  const ats = (p.stepKeys ?? ['s1', 's2', 's3', 's4', 'json']).map((k, i) => at(k, 1 + i * 2));
  return (
    <GScene>
      <Chip n={p.n ?? "02"} en="Export" ar="حوّله لكود" color={G.gold} at={2} y={40} />
      <Stage p={p} out={json - 4} />
      {f >= json ? <In at={json} x={540} y={560}><FileIcon ext=".json" color={TEAL} name="myAnimation.json" s={1.5} /></In> : null}
      {f >= json + 10 ? <In at={json + 10} x={540} y={930}><Pill text="الكود ده = الأنيميشن 🤯" size={52} /></In> : null}
      <Steps items={steps} ats={ats} />
    </GScene>
  );
};

// 6. Get the Player -> player.js (the JavaScript that plays it)
export const LtPlayer: React.FC<B> = (p) => {
  const f = useCurrentFrame();
  const at = useBeats(p.b);
  const js = at('js', 5.1);
  return (
    <GScene>
      <Chip n="03" en="Player" ar="ملف التشغيل" color={G.gold} at={2} y={40} />
      <Stage p={p} y={560} h={760} out={js + 20} />
      {f >= js + 20 ? <In at={js + 20} x={300} y={520}><FileIcon ext=".json" color={TEAL} name="myAnimation.json" s={1} /></In> : null}
      {f >= js + 28 ? <In at={js + 28} x={780} y={520}><FileIcon ext=".js" color="#E8C21A" name="player.js" s={1} /></In> : null}
      {f >= js ? <In at={js} x={540} y={1110}><Pill text="player.js = اللي بيشغّل الأنيميشن ▶" size={44} /></In> : null}
    </GScene>
  );
};

// 7. run it from a server, not by opening the html file (XAMPP / Apache)
export const LtServer: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const no = at('no', 0.7), yes = at('yes', 3.9), xa = at('xampp', 5.6);
  return (
    <GScene>
      <Top text="لازم [سيرفر] 🖥️" at={2} y={90} size={74} />
      <In at={no} x={290} y={500}>
        <Glass w={420} pad={30} glow={G.red}>
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14}}>
            <FileIcon ext=".html" color="#E44D26" s={0.8} />
            <Label text="file:///live.html" font={MONO} dir="ltr" size={30} color={G.soft} />
            <Mark ok={false} />
          </div>
        </Glass>
      </In>
      {f >= yes ? (
        <In at={yes} x={790} y={500}>
          <Glass w={420} pad={30} glow={G.green}>
            <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14}}>
              <div style={{height: 238, display: 'flex', alignItems: 'center'}}>{f >= xa ? <Xampp s={1} /> : <span style={{fontSize: 150}}>🖥️</span>}</div>
              <Label text="localhost/live.html" font={MONO} dir="ltr" size={30} color={G.soft} />
              <Mark ok />
            </div>
          </Glass>
        </In>
      ) : null}
      {f >= xa ? <In at={xa} x={540} y={900}><Pill text="XAMPP → Start Apache" color="#FB7A24" ink="#fff" size={50} font={EN} dir="ltr" /></In> : null}
    </GScene>
  );
};

// 8. the code (clean vector editor, typed on his words)
export const LtCode: React.FC<B> = ({b, n}) => {
  const at = useBeats(b);
  // v2 (one short sentence): missing beats -> the lines type in fast one after another
  const load = at('load', 0.1), path = at('path', 2.4), cont = at('cont', 3.6), get = at('get', 3.6);
  const f = useCurrentFrame();
  const lines: Ln[] = [
    {at: 4, text: '<div id="animeHERE"></div>'},
    {at: 12, text: '<script src="player.js"></script>'},
    {at: 22, text: '<script>'},
    {at: load + 20, text: 'bodymovin.loadAnimation({', ind: 1, hi: true},
    {at: path + 6, text: 'path: "myAnimation.json",', ind: 2, hi: true},
    {at: get, text: 'container: document.getElementById("animeHERE")', ind: 2, hi: true},
    {at: load + 40, text: '})', ind: 1},
    {at: 30, text: '</script>'},
  ];
  // the lines appear in this order on screen; sort by array index (closing lines show early, like a skeleton)
  return (
    <GScene>
      <Chip n={n ?? "04"} en="HTML + JS" ar="الكود" color={G.gold} at={2} y={40} />
      <In at={2} x={540} y={520}><Code lines={lines} size={30} w={1020} cps={2.6} /></In>
      {f >= load + 6 && f < path ? <In at={load + 6} x={540} y={940}><Pill text="loadAnimation = هات الأنيميشن" size={46} /></In> : null}
      {f >= path && f < cont ? <In at={path} x={540} y={940}><Pill text="path = مكان ملف الـ json 📄" size={46} /></In> : null}
      {f >= cont ? <In at={cont} x={540} y={940}><Pill text="container = الـ div اللي هيتعرض فيه 📦" size={42} /></In> : null}
    </GScene>
  );
};

// 9. run: plays once -> loop: true -> loops (his real browser)
export const LtRun: React.FC<B> = (p) => {
  const f = useCurrentFrame();
  const at = useBeats(p.b);
  const once = at('once', 7.6), loop = at('loop', 12.3), tr = at('true', 15.7);
  const lines: Ln[] = [{at: loop - 10, text: 'path: "myAnimation.json",'}, {at: loop - 10, text: 'container: ...,'}, {at: loop + 4, text: 'loop: true', hi: true}];
  return (
    <GScene>
      <Chip n={p.n ?? "05"} en="Run" ar="شغّله" color={G.gold} at={2} y={40} />
      {f < loop - 12 ? <Stage p={p} y={560} h={760} /> : null}
      {f >= 10 && f < once ? <In at={10} x={540} y={1060}><Pill text="زي الفل ✓ 10/10" color={G.green} ink="#fff" size={52} /></In> : null}
      {f >= once && f < loop - 12 ? <In at={once} x={540} y={1060}><Pill text="بس اشتغل مرة واحدة ووقف ⏹" color={G.red} ink="#fff" size={48} /></In> : null}
      {f >= loop - 12 ? (
        <>
          <In at={loop - 12} x={540} y={430}><Code lines={lines} size={36} w={900} file="loop" /></In>
          <In at={loop} x={540} y={800}><Pill text="default = loop: false" color="rgba(255,255,255,0.9)" size={44} font={EN} dir="ltr" /></In>
          {f >= tr ? <In at={tr} x={540} y={1000}><div style={{display: 'flex', alignItems: 'center', gap: 26}}><Liquid d={170} level={(f % 60) / 60} /><Pill text="🔁 بيعيد على طول" size={48} /></div></In> : null}
        </>
      ) : null}
    </GScene>
  );
};

// 10. scale: a video pixelates, the code animation never does (vector)
export const LtScale: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const px = at('px', 1), vec = at('vec', 4.2);
  const z = lin(f, px, px + 40, 1, 2.4);
  const z2 = lin(f, vec, vec + 40, 1, 2.4);
  const cells = 12;
  return (
    <GScene>
      <Top text="كبّر براحتك = مفيش *بكسلة*" at={2} y={90} size={64} />
      <In at={px} x={290} y={560}>
        <Glass w={440} h={560} pad={20} glow={G.red}>
          <div style={{width: 400, height: 400, overflow: 'hidden', borderRadius: 22, background: '#fff', position: 'relative'}}>
            <div style={{position: 'absolute', left: 200 - 100 * z, top: 200 - 100 * z, width: 200 * z, height: 200 * z, display: 'grid', gridTemplateColumns: `repeat(${cells}, 1fr)`}}>
              {Array.from({length: cells * cells}).map((_, i) => {
                const x = (i % cells) + 0.5 - cells / 2, y = Math.floor(i / cells) + 0.5 - cells / 2;
                const inC = x * x + y * y < (cells / 2) * (cells / 2);
                return <div key={i} style={{background: inC ? (y > -1 + 0.6 * Math.sin(x) ? RED : ICE) : '#fff'}} />;
              })}
            </div>
          </div>
          <Label text="فيديو / صورة ✕" size={40} color={G.red} />
        </Glass>
      </In>
      {f >= vec ? (
        <In at={vec} x={790} y={560}>
          <Glass w={440} h={560} pad={20} glow={G.green}>
            <div style={{width: 400, height: 400, overflow: 'hidden', borderRadius: 22, background: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
              <div style={{transform: `scale(${z2})`}}><Liquid d={200} level={0.45} /></div>
            </div>
            <Label text="كود (Vector) ✓" size={40} color={G.green} />
          </Glass>
        </In>
      ) : null}
    </GScene>
  );
};

// 11. control: autoplay false + PLAY / PAUSE buttons call animation.play() / pause()
export const LtControl: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const auto = at('auto', 2.1), play = at('play', 6.6), pause = at('pause', 12);
  const lines: Ln[] = [
    {at: 4, text: '<button onclick="goON()">PLAY</button>'},
    {at: 10, text: '<button onclick="enough()">PAUSE</button>'},
    {at: 16, text: 'var animation = bodymovin.loadAnimation({ ... })'},
    {at: auto, text: '  autoplay: false', hi: true},
    {at: play - 24, text: 'function goON(){ animation.play() }', hi: true},
    {at: pause - 24, text: 'function enough(){ animation.pause() }', hi: true},
  ];
  const lv = f < play ? 0.06 : lin(Math.min(f, pause), play, play + 150, 0.06, 1, Easing.inOut(Easing.sin));
  return (
    <GScene>
      <Chip n="06" en="Control" ar="اتحكم فيه" color={G.gold} at={2} y={40} />
      <In at={2} x={540} y={330}><Code lines={lines} size={27} w={1020} cps={3} /></In>
      <In at={play - 20} x={400} y={870}>
        <Browser w={700} h={480}>
          <Liquid d={250} level={lv} />
          <div style={{display: 'flex', gap: 24}}>
            <Btn label="PLAY" down={f >= play && f < play + 8} color={G.green} />
            <Btn label="PAUSE" down={f >= pause && f < pause + 8} color={G.red} />
          </div>
        </Browser>
      </In>
      {f >= play - 12 ? <Cursor x={f < pause - 14 ? 290 : 290 + lin(f, pause - 14, pause - 2, 0, 170)} y={1060} s={0.8} click={f < pause - 14 ? play : pause} /> : null}
      {f >= auto && f < play - 20 ? <In at={auto} x={540} y={800}><Pill text="autoplay: false = مايشتغلش لوحده" size={44} /></In> : null}
    </GScene>
  );
};

// 12. hover: event listener -> mouse enters = play, leaves = stop
export const LtHover: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const ev = at('ev', 1.6), inn = at('in', 4.6), play = at('play', 7.5), stop = at('stop', 8.8);
  const lines: Ln[] = [
    {at: ev, text: 'logo.addEventListener("mouseenter", () => animation.play())', hi: true},
    {at: ev + 30, text: 'logo.addEventListener("mouseleave", () => animation.stop())', hi: true},
  ];
  const over = f >= inn && f < stop;
  const lv = !over ? 0.06 : lin(f, inn, inn + 90, 0.06, 1);
  const cx = f < inn ? 200 + lin(f, inn - 30, inn, 0, 300) : f < stop ? 540 + 30 * Math.sin(f / 12) : 540 + lin(f, stop, stop + 14, 0, 330);
  return (
    <GScene>
      <Chip n="07" en="Hover" ar="أول ما الماوس يقف عليه" color={G.gold} at={2} y={40} />
      <In at={2} x={540} y={330}><Code lines={lines} size={23} w={1020} file="javascript.js" cps={3.5} /></In>
      <In at={8} x={540} y={790}>
        <div style={{padding: 30, borderRadius: 40, border: `5px dashed ${over ? G.gold : 'rgba(255,255,255,0.35)'}`, boxShadow: over ? `0 0 60px ${G.gold}66` : undefined}}><Liquid d={340} level={lv} /></div>
      </In>
      {f >= 8 ? <Cursor x={cx} y={860} click={inn} /> : null}
      {f >= play ? <In at={play} x={300} y={1110}><Pill text="دخل = Play ▶" color={G.green} ink="#fff" size={44} /></In> : null}
      {f >= stop ? <In at={stop} x={720} y={1110}><Pill text="خرج = Stop ⏹" color={G.red} ink="#fff" size={44} /></In> : null}
    </GScene>
  );
};

// 13. efficiency test: shape layer vs jpg/png (his real smileys) -> shape layer = 4 KB, sharp
export const LtEff: React.FC<B> = (p) => {
  const f = useCurrentFrame();
  const at = useBeats(p.b);
  const best = at('best', 1.6), png = at('png', 3.8), kb = at('kb', 13.5);
  return (
    <GScene>
      <Chip n={p.n ?? "08"} en="Test" ar="مين أخف وأحسن؟" color={G.gold} at={2} y={40} />
      <Stage p={p} y={560} h={720} />
      {f >= best ? <In at={best} x={540} y={1020}><Pill text="🏆 الأحسن: Shape Layer" size={50} /></In> : null}
      {/* v3 (Aly): say what a shape layer is = the drawing made INSIDE After Effects -> saves the most space */}
      {p.inside && f >= best + 14 ? (
        <In at={best + 14} x={540} y={1140}>
          <div style={{display: 'flex', alignItems: 'center', gap: 18}}><AeLogo s={0.4} /><Pill text="= مرسوم جوه After Effects" size={42} color="#F2F4F7" /></div>
        </In>
      ) : null}
      {!p.inside && f >= png && f < kb ? <In at={png} x={540} y={1130}><Pill text="PNG / JPG = بكسلة شوية ✕" color={G.red} ink="#fff" size={42} /></In> : null}
      {f >= kb ? <In at={kb} x={540} y={p.inside ? 1232 : 1130}><Pill text={p.inside ? 'أكتر حاجة بتوفّر مساحة: 4 كيلو بايت بس ✓' : 'Shape Layer = 4 KB بس ✓'} color={G.green} ink="#fff" size={44} font={p.inside ? AR : EN} dir={p.inside ? 'rtl' : 'ltr'} /></In> : null}
    </GScene>
  );
};

// v3 (Aly 2026-10-16): his animation inside After Effects, shown BEFORE the extension
export const LtAeLook: React.FC<B> = (p) => (
  <GScene>
    <div style={{position: 'absolute', top: 40, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><AeLogo s={0.55} /></div>
    <Stage p={p} y={640} h={760} />
    <In at={10} x={540} y={1110}><Pill text="الأنيميشن على After Effects 🎬" size={50} /></In>
  </GScene>
);

// v3: he presses PLAY / PAUSE on his real page, then what you can build: many animations with their own buttons, even a game
export const LtUse: React.FC<B> = (p) => {
  const f = useCurrentFrame();
  const at = useBeats(p.b);
  const play = at('play', 0.5), pause = at('pause', 3.5), shapes = at('shapes', 7), btns = at('btns', 10), game = at('game', 12);
  return (
    <GScene>
      <Chip n={p.n ?? '05'} en="Use it" ar="تعمل بيه إيه؟" color={G.gold} at={2} y={40} />
      {f < shapes - 6 ? <Stage p={p} y={600} h={800} out={shapes - 8} /> : null}
      {f >= play && f < shapes - 6 ? <In at={play} x={300} y={1100}><Pill text="▶ PLAY" color={G.green} ink="#fff" size={46} font={EN} dir="ltr" /></In> : null}
      {f >= pause && f < shapes - 6 ? <In at={pause} x={760} y={1100}><Pill text="PAUSE ❚❚" color={G.red} ink="#fff" size={46} font={EN} dir="ltr" /></In> : null}
      {f >= shapes ? (
        <>
          <Top text="أكتر من *أنيميشن* 🎨" at={shapes} y={170} size={66} out={game - 6} />
          {[0, 1, 2].map((i) => {
            const t0 = shapes + i * 6, on = f >= btns + i * 8;
            return (
              <In key={i} at={t0} x={200 + i * 340} y={560}>
                <Glass w={300} pad={20} r={30} glow={on ? [G.green, G.blue, G.gold][i] : undefined}>
                  <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 18}}>
                    <Liquid d={200} level={on ? lin(f, btns + i * 8, btns + i * 8 + 50, 0.08, 0.3 + 0.3 * i) : 0.08} stripe={i !== 1} />
                    <Btn label={['▶ 1', '▶ 2', '▶ 3'][i]} down={f >= btns + i * 8 && f < btns + i * 8 + 8} color={[G.green, G.blue, G.gold][i]} />
                  </div>
                </Glass>
              </In>
            );
          })}
          {f >= btns ? <In at={btns} x={540} y={860}><Pill text="كل واحد بزرار لوحده 🔘" size={48} /></In> : null}
          {f >= game ? <In at={game} x={540} y={1040}><Pill text="🎮 وممكن تعمل جيم كمان" color={G.blue} ink="#fff" size={56} /></In> : null}
        </>
      ) : null}
    </GScene>
  );
};

// 14. end: the whole chain + QR of the full video
export const LtEnd: React.FC<B> = ({qr}) => {
  const f = useCurrentFrame();
  const items: [React.ReactNode, string][] = [
    [<AeLogo key="a" s={0.5} />, 'After Effects'], [<LottieLogo key="b" s={0.5} />, 'Bodymovin'], [<FileIcon key="c" ext=".json" color={TEAL} s={0.45} />, 'myAnimation.json'],
    [<FileIcon key="d" ext=".js" color="#E8C21A" s={0.45} />, 'player.js'], [<Globe key="e" s={0.65} />, 'Website ▶'],
  ];
  return (
    <GScene>
      <Top text="الخطوات *كلها*" at={2} y={60} size={66} />
      <div style={{position: 'absolute', top: 170, left: 30, width: 640, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12}}>
        {items.map(([ic, t], i) => {
          const s0 = 8 + i * 9;
          if (f < s0) return null;
          const k = spr(f, 30, s0, 160, 16);
          return (
            <div key={t} style={{opacity: Math.min(1, k * 1.4), transform: `translateX(${(1 - k) * 80}px)`}}>
              <Glass w={600} pad={12} r={28}>
                <div style={{display: 'flex', alignItems: 'center', gap: 22, direction: 'ltr', height: 100}}>
                  <div style={{width: 110, display: 'flex', justifyContent: 'center'}}>{ic}</div>
                  <span style={{fontFamily: EN, fontWeight: 800, fontSize: 38, color: G.ink}}>{t}</span>
                </div>
              </Glass>
            </div>
          );
        })}
      </div>
      {qr ? (
        <In at={20} x={870} y={480}>
          <div style={{background: '#fff', borderRadius: 30, padding: 18, border: `6px solid ${G.gold}`, boxShadow: `0 0 50px ${G.gold}66`, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8}}>
            <Img src={staticFile(qr)} style={{width: 270, height: 270, display: 'block'}} />
            <div style={{fontFamily: AR, fontWeight: 900, fontSize: 34, color: '#14181F'}}>الفيديو كامل 📲</div>
          </div>
        </In>
      ) : null}
      <In at={30} x={870} y={860}><Liquid d={200} level={0.3 + 0.7 * ((f % 90) / 90)} /></In>
    </GScene>
  );
};

export const lottieScenes: Record<string, React.FC<any>> = {
  lt_hook: LtHook, lt_intro: LtIntro, lt_tip: LtTip, lt_plugin: LtPlugin, lt_install: LtInstall, lt_export: LtExport, lt_player: LtPlayer,
  lt_server: LtServer, lt_code: LtCode, lt_run: LtRun, lt_scale: LtScale, lt_control: LtControl, lt_hover: LtHover, lt_eff: LtEff, lt_end: LtEnd, lt_aelook: LtAeLook, lt_use: LtUse,
};
export {rnd};
