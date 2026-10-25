import React from 'react';
import {AbsoluteFill, Easing, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, G, Glass, lin, Pill, spr} from '../glass/kit';

// "Course" kit (premiere pro course, 2026-10-16). Aly: the screen recording is THE course -> it is never hidden; motion lives
// beside it (side mode) or on top of empty areas (taskbar strip, black around his slides). Look = glass (style 10/11) +
// Crash Course spirit (his reference Spgdy3HkcSs): "Fig N.N" cards, one bold coloured word, a recurring segment chip.
export const CC = {teal: '#19B5A5', coral: '#FF6B5B', paper: '#F4F1EA', ink: '#14181F', violet: '#9999FF', prBg: '#00005B'};
export const SRC_W = 1276, SRC_H = 720;
// Arabic line with English runs: isolate each Latin/number run (LRI..PDI) so "4K" never flips to "K4" inside RTL text.
export const bi = (s: string) => (s ?? '').replace(/[A-Za-z0-9][A-Za-z0-9 .,+:>&\/'-]*[A-Za-z0-9]|[A-Za-z0-9]/g, (m) => '⁦' + m + '⁩');

// ---------- the screen recording ----------
// keys: layout changes (timeline seconds). m = full | side | sideR. Optional crop (source px): sx, sy, sw (sh follows 16:9).
export type LKey = {t: number; m: string; sx?: number; sy?: number; sw?: number};
export type Part = {at: number; from: number; to: number; rate?: number; file: string};
const RECT: Record<string, {x: number; y: number; w: number}> = {
  full: {x: 0, y: 0, w: 1920},
  side: {x: 712, y: 150, w: 1160}, // graphics column on the left (0..680)
  sideR: {x: 48, y: 150, w: 1160}, // graphics column on the right
  wide: {x: 160, y: 96, w: 1600}, // a frame around it, bottom strip free for notes
  teaser: {x: 420, y: 268, w: 1080}, // audio course cold open: a smaller card = clearly 'a clip from later in the course'
};
export const Screen: React.FC<{parts: Part[]; keys: LKey[]}> = ({parts, keys}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  let i = 0;
  while (i + 1 < keys.length && f >= Math.round(keys[i + 1].t * fps)) i++;
  const get = (k: LKey) => {
    const r = RECT[k.m] ?? RECT.full;
    const sw = k.sw ?? SRC_W;
    return {x: r.x, y: r.y, w: r.w, sx: k.sx ?? 0, sy: k.sy ?? 0, sw};
  };
  // 'hide' = no screen at all (opening pages fade in/out over the background: the empty teaser card showed through, Aly review 4)
  if (keys[i]?.m === 'hide') return null;
  const cur = get(keys[i] ?? {t: 0, m: 'full'});
  const prev = i > 0 ? get(keys[i - 1]) : cur;
  const k = i > 0 ? lin(f, Math.round(keys[i].t * fps), Math.round(keys[i].t * fps) + 16, 0, 1, Easing.inOut(Easing.cubic)) : 1;
  const m = (a: number, b: number) => a + (b - a) * k;
  const R = {x: m(prev.x, cur.x), y: m(prev.y, cur.y), w: m(prev.w, cur.w), sx: m(prev.sx, cur.sx), sy: m(prev.sy, cur.sy), sw: m(prev.sw, cur.sw)};
  const h = R.w * 9 / 16;
  const sc = R.w / R.sw;
  const framed = R.w < 1919; // full = edge to edge (readable); otherwise a glass frame with rounded corners
  const vids = parts.map((p, j) => {
    const rate = p.rate ?? 1;
    const len = Math.round(((p.to - p.from) / rate) * fps);
    return (
      <Sequence key={j} from={Math.round(p.at * fps)} durationInFrames={len} layout="none">
        <OffthreadVideo src={staticFile(p.file)} startFrom={Math.round(p.from * fps)} playbackRate={rate} muted={rate > 1.01}
          style={{position: 'absolute', left: -R.sx * sc, top: -R.sy * sc, width: SRC_W * sc, height: SRC_H * sc}} />
      </Sequence>
    );
  });
  const fr = Math.min(1, (1920 - R.w) / 200);
  return (
    <div style={{position: 'absolute', left: R.x - 10 * fr, top: R.y - 10 * fr, padding: 10 * fr, borderRadius: 34 * fr,
      background: `rgba(255,255,255,${0.10 * fr})`, border: fr > 0.01 ? `2px solid rgba(255,255,255,${0.22 * fr})` : undefined,
      boxShadow: fr > 0.01 ? `0 30px 80px rgba(0,0,0,${0.5 * fr}), 0 0 70px ${G.blue}${Math.round(40 * fr).toString(16).padStart(2, '0')}` : undefined}}>
      <div style={{position: 'relative', width: R.w, height: h, overflow: 'hidden', borderRadius: 24 * fr, background: '#000'}}>{vids}</div>
      {framed ? null : null}
    </div>
  );
};

// ---------- background behind the screen (only visible in side / wide modes) ----------
export const CourseBg: React.FC = () => {
  const f = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const x = 22 + 12 * Math.sin(f / 110), y = 30 + 14 * Math.cos(f / 140);
  return (
    <AbsoluteFill style={{background: `linear-gradient(160deg, ${G.navy} 0%, ${G.bg} 60%, #07090D 100%)`}}>
      <AbsoluteFill style={{background: `radial-gradient(circle at ${x}% ${y}%, ${G.blue}40 0%, transparent 40%)`}} />
      <AbsoluteFill style={{background: `radial-gradient(circle at ${88 - x / 2}% ${80 - y / 3}%, ${G.royal}70 0%, transparent 45%)`}} />
      <Img src={staticFile(`bg/grain_${Math.floor(f / 2) % 3}.png`)} style={{position: 'absolute', width, height, opacity: 0.08, mixBlendMode: 'overlay'}} />
    </AbsoluteFill>
  );
};

// ---------- small building blocks ----------
const useIn = (dur: number, inF = 10, outF = 10) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 150, 17);
  const o = 1 - lin(f, dur - outF, dur, 0, 1, Easing.in(Easing.cubic));
  return {f, p, o: Math.min(1, p * 1.3) * o, inF};
};

// English term -> quick Arabic meaning (Aly: every English word gets a fast explainer). Bottom strip (covers his taskbar).
export const Kw: React.FC<{en: string; ar: string; dur: number; x?: number; y?: number}> = ({en, ar, dur, x = 960, y = 1000}) => {
  const {p, o} = useIn(dur, 8, 8);
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) translateY(${(1 - p) * 40}px) scale(${0.85 + 0.15 * p})`, opacity: o,
      display: 'flex', alignItems: 'center', gap: 18, padding: '10px 28px 10px 12px', borderRadius: 60, direction: 'ltr', whiteSpace: 'nowrap',
      background: 'rgba(12,16,26,0.86)', border: '2px solid rgba(255,255,255,0.22)', boxShadow: `0 16px 40px rgba(0,0,0,0.5), 0 0 40px ${G.gold}33`}}>
      <Pill text={en} font={EN} dir="ltr" size={40} />
      <span style={{fontFamily: AR, fontWeight: 800, fontSize: 38, color: G.ink, direction: 'rtl'}}>{bi(ar)}</span>
    </div>
  );
};

// Source chip (every fact on screen carries its source).
export const Src: React.FC<{text: string; s?: number}> = ({text, s = 1}) => (
  <div style={{display: 'inline-flex', alignItems: 'center', gap: 10 * s, padding: `${6 * s}px ${16 * s}px`, borderRadius: 30 * s, background: 'rgba(255,255,255,0.10)',
    border: '1.5px solid rgba(255,255,255,0.25)', fontFamily: EN, fontWeight: 600, fontSize: 22 * s, color: G.soft, direction: 'ltr', whiteSpace: 'nowrap'}}>
    <span style={{fontFamily: AR, fontWeight: 700}}>المصدر:</span> {text}
  </div>
);

// Crash-Course style figure card: coloured "Fig" tab, picture (or children), caption, source.
export const Fig: React.FC<{n: string; title: string; sub?: string; img?: string; src?: string; dur: number; x?: number; y?: number; w?: number; color?: string; children?: React.ReactNode}> = (
  {n, title, sub, img, src, dur, x = 345, y = 520, w = 600, color = CC.teal, children}) => {
  const {p, o} = useIn(dur);
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) translateY(${(1 - p) * 50}px) rotate(${(1 - p) * -4}deg)`, opacity: o, width: w}}>
      <div style={{background: CC.paper, borderRadius: 18, padding: 16, boxShadow: '0 30px 70px rgba(0,0,0,0.55)', position: 'relative'}}>
        <div style={{position: 'absolute', left: -14, top: -26, background: color, color: '#fff', fontFamily: EN, fontWeight: 900, fontSize: 30, padding: '6px 18px',
          borderRadius: 10, transform: 'rotate(-3deg)', boxShadow: '0 8px 20px rgba(0,0,0,0.35)'}}>Fig {n}</div>
        {img ? <Img src={staticFile(img)} style={{width: '100%', borderRadius: 10, display: 'block'}} /> : children}
        <div style={{fontFamily: EN, fontWeight: 900, fontSize: 30, color: CC.ink, marginTop: 12, direction: 'ltr', lineHeight: 1.15}}>{title}</div>
        {sub ? <div style={{fontFamily: AR, fontWeight: 700, fontSize: 28, color: '#3A4250', direction: 'rtl', textAlign: 'right', marginTop: 4, lineHeight: 1.35}}>{bi(sub)}</div> : null}
      </div>
      {src ? <div style={{marginTop: 12, display: 'flex', justifyContent: 'center'}}><Src text={src} /></div> : null}
    </div>
  );
};

// Definition card: term (EN) + Arabic definition, optional source. Left column.
export const Def: React.FC<{term: string; ar: string; text: string; src?: string; dur: number; x?: number; y?: number; w?: number; color?: string}> = (
  {term, ar, text, src, dur, x = 345, y = 540, w = 600, color = G.gold}) => {
  const {f, p, o} = useIn(dur);
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) translateX(${(1 - p) * -60}px)`, opacity: o}}>
      <Glass w={w} pad={30} r={36} glow={color}>
        <div style={{fontFamily: AR, fontWeight: 700, fontSize: 26, color: G.dim, direction: 'rtl', textAlign: 'right'}}>تعريف</div>
        <div style={{display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', gap: 16, marginTop: 4}}>
          <span style={{fontFamily: EN, fontWeight: 900, fontSize: 58, color, direction: 'ltr'}}>{term}</span>
          <span style={{fontFamily: AR, fontWeight: 900, fontSize: 40, color: G.ink}}>{ar}</span>
        </div>
        <div style={{height: 3, background: `linear-gradient(90deg, ${color}, transparent)`, margin: '12px 0 14px', width: `${lin(f, 6, 22) * 100}%`}} />
        {/* whole sentence at once (word-by-word broke the order of English words inside Arabic), revealed by a soft wipe */}
        <div style={{fontFamily: AR, fontWeight: 700, fontSize: 34, color: G.soft, direction: 'rtl', textAlign: 'right', lineHeight: 1.45,
          WebkitMaskImage: `linear-gradient(270deg, #000 ${lin(f, 8, 34) * 100}%, transparent ${lin(f, 8, 34) * 100 + 15}%)`}}>{bi(text)}</div>
        {src ? <div style={{marginTop: 18, display: 'flex', justifyContent: 'flex-end'}}><Src text={src} s={0.9} /></div> : null}
      </Glass>
    </div>
  );
};

// Small chip in a corner: callback ("فاكر..."), later ("هنرجع لها في ..."), weak ("معلومة ضعيفة المصدر"), fix (correction).
const CHIP: Record<string, {c: string; ico: string}> = {
  back: {c: G.blue, ico: '↩'}, later: {c: CC.teal, ico: '⏭'}, weak: {c: G.gold, ico: '⚠'}, fix: {c: CC.coral, ico: '✎'}, tip: {c: G.green, ico: '💡'}, new: {c: CC.violet, ico: '⚡'},
  same: {c: G.green, ico: '✓'}, ff: {c: G.soft, ico: '⏩'},
};
export const Chip: React.FC<{kind: string; text: string; dur: number; x?: number; y?: number; size?: number}> = ({kind, text, dur, x = 1860, y = 90, size = 32}) => {
  const {p, o} = useIn(dur);
  const {width} = useVideoConfig();
  const k = CHIP[kind] ?? CHIP.tip;
  return (
    <div style={{position: 'absolute', right: width - x, top: y, opacity: o, transform: `translateX(${(1 - p) * 60}px)`, display: 'flex', alignItems: 'center', gap: 14,
      padding: '10px 22px 10px 10px', borderRadius: 50, background: 'rgba(12,16,26,0.88)', border: `2px solid ${k.c}`, boxShadow: `0 0 36px ${k.c}55`, direction: 'rtl', maxWidth: 820}}>
      <div style={{width: 50, height: 50, borderRadius: '50%', background: k.c, color: '#14181F', fontSize: 28, fontWeight: 900, display: 'flex', alignItems: 'center',
        justifyContent: 'center', flexShrink: 0}}>{k.ico}</div>
      <span style={{fontFamily: AR, fontWeight: 800, fontSize: size, color: G.ink, lineHeight: 1.3}}>{bi(text)}</span>
    </div>
  );
};

// Keyboard shortcut (bottom-right): keycaps that press down + what it does. keys = ['Ctrl', 'Z'].
export const Key: React.FC<{keys: string[]; ar: string; dur: number; x?: number; y?: number}> = ({keys, ar, dur, x = 1880, y = 930}) => {
  const {f, p, o} = useIn(dur, 8, 8);
  const {width} = useVideoConfig();
  // mouse actions are not keys (Aly 2026-10-18): draw a mouse with the pressed button lit
  const mouse = keys.join(' ').match(/^(Right|Double|Left) Click$/);
  if (mouse) {
    const side = mouse[1];
    const lit = (f % 20) < 10;
    return (
      <div style={{position: 'absolute', right: width - x, top: y, opacity: o, transform: `translateY(${(1 - p) * 40}px)`, display: 'flex', alignItems: 'center', gap: 18,
        padding: '12px 22px', borderRadius: 26, background: 'rgba(12,16,26,0.9)', border: '2px solid rgba(255,255,255,0.22)', direction: 'rtl'}}>
        <svg width={64} height={92} viewBox="0 0 64 92">
          <rect x={4} y={4} width={56} height={84} rx={28} fill="#E9EDF3" />
          <path d="M32 4 V40" stroke="#9AA6B5" strokeWidth={3} /><path d="M4 40 H60" stroke="#9AA6B5" strokeWidth={3} />
          {side !== 'Right' ? <path d="M32 4 A28 28 0 0 0 4 32 V40 H32 Z" fill={lit ? G.gold : '#E9EDF3'} /> : null}
          {side === 'Right' ? <path d="M32 4 A28 28 0 0 1 60 32 V40 H32 Z" fill={lit ? G.gold : '#E9EDF3'} /> : null}
        </svg>
        <div>
          <div style={{fontFamily: EN, fontWeight: 900, fontSize: 32, color: G.gold, direction: 'ltr', textAlign: 'right'}}>{side === 'Double' ? 'Double click' : `${side} click`}</div>
          <div style={{fontFamily: AR, fontWeight: 800, fontSize: 28, color: G.ink}}>{bi(ar)}</div>
        </div>
      </div>
    );
  }
  return (
    <div style={{position: 'absolute', right: width - x, top: y, opacity: o, transform: `translateY(${(1 - p) * 40}px)`, display: 'flex', alignItems: 'center', gap: 16,
      padding: '12px 18px', borderRadius: 26, background: 'rgba(12,16,26,0.9)', border: '2px solid rgba(255,255,255,0.22)', boxShadow: `0 16px 40px rgba(0,0,0,0.5), 0 0 40px ${G.blue}33`}}>
      <span style={{fontFamily: AR, fontWeight: 800, fontSize: 32, color: G.ink, direction: 'rtl'}}>{bi(ar)}</span>
      <div style={{display: 'flex', alignItems: 'center', gap: 8, direction: 'ltr'}}>
        {keys.map((kk, i) => {
          const down = f >= 10 + i * 4 && f < 18 + i * 4;
          return (
            <React.Fragment key={i}>
              {i > 0 ? <span style={{fontFamily: EN, fontWeight: 900, fontSize: 30, color: G.dim}}>+</span> : null}
              <div style={{minWidth: 62, height: 62, padding: '0 14px', boxSizing: 'border-box', borderRadius: 12, background: down ? G.gold : '#E9EDF3', color: '#14181F',
                fontFamily: EN, fontWeight: 900, fontSize: kk.length > 3 ? 24 : 30, display: 'flex', alignItems: 'center', justifyContent: 'center',
                boxShadow: down ? '0 1px 0 #8a6d1f' : '0 6px 0 #9AA6B5', transform: `translateY(${down ? 5 : 0}px)`}}>{kk}</div>
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};

// Same tool in another program (bottom-left, small): "في DaVinci Resolve اسمها Blade" (Aly's request).
export const Alt: React.FC<{app?: string; name: string; note?: string; src?: string; dur: number}> = ({app = 'DaVinci Resolve', name, note, src = 'Blackmagic', dur}) => {
  const {p, o} = useIn(dur);
  return (
    <div style={{position: 'absolute', left: 24, bottom: 104, opacity: o, transform: `translateX(${(1 - p) * -50}px)`, display: 'flex', alignItems: 'center', gap: 14,
      padding: '8px 18px 8px 10px', borderRadius: 40, background: 'rgba(12,16,26,0.9)', border: '2px solid rgba(255,255,255,0.18)', direction: 'rtl'}}>
      <svg width={44} height={44} viewBox="0 0 44 44"><circle cx={22} cy={22} r={20} fill="#1B1B1F" />{['#F44336', '#FFC107', '#4CAF50', '#2196F3'].map((c, i) =>
        <circle key={i} cx={22 + 9 * Math.cos((i * Math.PI) / 2)} cy={22 + 9 * Math.sin((i * Math.PI) / 2)} r={6} fill={c} />)}</svg>
      <span style={{fontFamily: AR, fontWeight: 700, fontSize: 26, color: G.soft}}>في {bi(app)} اسمها</span>
      <span style={{fontFamily: EN, fontWeight: 900, fontSize: 30, color: G.gold, direction: 'ltr'}}>{name}</span>
      {note ? <span style={{fontFamily: AR, fontWeight: 700, fontSize: 24, color: G.dim}}>{bi(note)}</span> : null}
      <span style={{fontFamily: EN, fontWeight: 600, fontSize: 16, color: G.dim, direction: 'ltr'}}>· {src}</span>
    </div>
  );
};

// "⚡ أسهل في Premiere 2026" / "✓ لسه زي ما هي" card (left column, side mode): what changed + how + the best video for it
// (thumbnail + QR). Aly: "قول ان كلود اللي مرشحه مش انا". src = the official Adobe page that says it.
export const New26: React.FC<{title: string; how: string; thumb?: string; qr?: string; vtitle?: string; channel?: string; src: string; dur: number; kind?: string}> = (
  {title, how, thumb, qr, vtitle, channel, src, dur, kind = 'new'}) => {
  const {f, p, o} = useIn(dur, 12, 12);
  const same = kind === 'same';
  const col = same ? G.green : CC.violet;
  return (
    <div style={{position: 'absolute', left: 345, top: 545, transform: `translate(-50%,-50%) translateX(${(1 - p) * -70}px)`, opacity: o}}>
      <Glass w={620} pad={24} r={34} glow={col}>
        <div style={{display: 'flex', direction: 'rtl'}}>
          <div style={{padding: '4px 16px', borderRadius: 20, background: col, fontFamily: AR, fontWeight: 900, fontSize: 26, color: '#fff'}}>{same ? '✓ لسه زي ما هي في 2026' : '⚡ أسهل في Premiere 2026'}</div>
        </div>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 40, color: G.ink, direction: 'rtl', textAlign: 'right', marginTop: 12, lineHeight: 1.25}}>{bi(title)}</div>
        <div style={{fontFamily: AR, fontWeight: 700, fontSize: 28, color: G.soft, direction: 'rtl', textAlign: 'right', marginTop: 8, lineHeight: 1.4}}>{bi(how)}</div>
        {thumb && qr ? (
          <>
            <div style={{display: 'flex', gap: 16, marginTop: 16, alignItems: 'center', direction: 'rtl', opacity: lin(f, 30, 44)}}>
              <div style={{position: 'relative', width: 300, height: 169, borderRadius: 14, overflow: 'hidden', flexShrink: 0, border: '2px solid rgba(255,255,255,0.25)'}}>
                <Img src={staticFile(thumb)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
                <div style={{position: 'absolute', left: '50%', top: '50%', width: 60, height: 42, marginLeft: -30, marginTop: -21, borderRadius: 12, background: '#FF0033',
                  display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                  <div style={{width: 0, height: 0, borderLeft: '18px solid #fff', borderTop: '11px solid transparent', borderBottom: '11px solid transparent', marginLeft: 4}} />
                </div>
              </div>
              <div style={{background: '#fff', padding: 8, borderRadius: 12}}><Img src={staticFile(qr)} style={{width: 150, height: 150, display: 'block'}} /></div>
            </div>
            <div style={{fontFamily: EN, fontWeight: 700, fontSize: 18, color: G.soft, direction: 'ltr', marginTop: 8, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
              opacity: lin(f, 30, 44)}}>{vtitle} · {channel}</div>
            <div style={{fontFamily: AR, fontWeight: 800, fontSize: 24, color: G.gold, direction: 'rtl', textAlign: 'right', marginTop: 6, opacity: lin(f, 40, 54)}}>Claude هو اللي بيرشح الفيديو ده، مش علي</div>
          </>
        ) : null}
        <div style={{marginTop: 12, display: 'flex', justifyContent: 'flex-end'}}><Src text={src} s={0.85} /></div>
      </Glass>
    </div>
  );
};

// Persistent HUD (top-left): chapter number + chapter name. Small, so it never hides the recording.
export const Hud: React.FC<{ep: number; n: number; total: number; title: string}> = ({ep, n, total, title}) => {
  const f = useCurrentFrame();
  const p = lin(f, 0, 14);
  return (
    <div style={{position: 'absolute', left: 24, top: 22, opacity: 0.92 * p, display: 'flex', alignItems: 'center', gap: 12, padding: '6px 18px 6px 8px', borderRadius: 40,
      background: 'rgba(10,14,22,0.78)', border: '1.5px solid rgba(255,255,255,0.18)', direction: 'rtl', transform: `translateY(${(1 - p) * -20}px)`}}>
      <div style={{padding: '2px 12px', borderRadius: 20, background: G.gold, fontFamily: EN, fontWeight: 900, fontSize: 20, color: '#14181F', direction: 'ltr'}}>{n}/{total}</div>
      <span style={{fontFamily: AR, fontWeight: 800, fontSize: 22, color: G.ink}}>{bi(title)}</span>
    </div>
  );
};

// ---------- vector icons (one per chapter type), with a small loop motion ----------
export const Ico: React.FC<{n: string; s?: number; c?: string; live?: boolean}> = ({n, s = 1, c = G.gold, live = true}) => {
  const f = useCurrentFrame();
  const t = live ? f : 0;
  const bob = Math.sin(t / 9) * 3;
  const W = 96;
  const st = {fill: 'none', stroke: c, strokeWidth: 6, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const};
  const sf = {fill: c};
  const body: Record<string, React.ReactNode> = {
    play: <><circle cx={48} cy={48} r={34} {...st} /><path d="M40 32 L64 48 L40 64 Z" {...sf} /></>,
    film: <><rect x={18} y={14} width={60} height={68} rx={6} {...st} />{[24, 40, 56, 72].map((y) => <rect key={y} x={10} y={y - 4} width={6} height={8} {...sf} />)}{[24, 40, 56, 72].map((y) => <rect key={'r' + y} x={80} y={y - 4} width={6} height={8} {...sf} />)}<rect x={30} y={30 + ((t / 4) % 24)} width={36} height={14} rx={3} {...sf} opacity={0.6} /></>,
    grid: <>{[0, 1, 2].map((i) => [0, 1, 2].map((j) => <rect key={i + '' + j} x={16 + i * 22} y={16 + j * 22} width={18} height={18} rx={3} {...sf} opacity={0.35 + 0.65 * ((i + j + Math.floor(t / 8)) % 3 === 0 ? 1 : 0)} />))}</>,
    timeline: <><path d="M10 30 H86 M10 52 H86 M10 74 H86" {...st} strokeWidth={4} opacity={0.4} /><rect x={14} y={22} width={30} height={16} rx={4} {...sf} /><rect x={40} y={44} width={36} height={16} rx={4} {...sf} opacity={0.8} /><rect x={22} y={66} width={44} height={16} rx={4} {...sf} opacity={0.6} /><path d={`M${20 + ((t * 1.2) % 60)} 12 V88`} {...st} stroke="#FF5A5F" strokeWidth={4} /></>,
    key: <><path d="M10 60 H86" {...st} opacity={0.4} /><path d="M26 46 L38 58 L26 70 L14 58 Z" {...sf} /><path d="M70 46 L82 58 L70 70 L58 58 Z" {...sf} /><circle cx={30 + 36 * (0.5 - 0.5 * Math.cos(t / 15))} cy={30} r={10} {...sf} /></>,
    seq: <><rect x={12} y={12} width={72} height={72} rx={10} {...st} /><rect x={26} y={26} width={44} height={44} rx={8} {...st} /><rect x={38} y={38} width={20} height={20} rx={5} {...sf} /></>,
    app: <><rect x={10} y={16} width={76} height={64} rx={8} {...st} /><path d="M10 32 H86" {...st} /><text x={48} y={68} textAnchor="middle" fontFamily="Montserrat" fontWeight={900} fontSize={28} fill={c}>Pr</text></>,
    import: <><path d="M10 34 H38 L44 40 H86 V80 H10 Z" {...st} /><path d={`M48 ${8 + ((t / 2) % 20)} V58 M36 46 L48 58 L60 46`} {...st} /></>,
    gear: <g transform={`rotate(${t * 2} 48 48)`}><circle cx={48} cy={48} r={16} {...st} />{[0, 45, 90, 135, 180, 225, 270, 315].map((a) => <rect key={a} x={44} y={14} width={8} height={14} rx={2} {...sf} transform={`rotate(${a} 48 48)`} />)}</g>,
    slow: <><path d="M14 70 Q14 40 44 40 Q70 40 70 62 Q70 74 56 74 Q44 74 44 62 Q44 54 52 54" {...st} /><path d="M14 74 H84" {...st} /><path d="M70 50 L80 34 M74 52 L88 40" {...st} strokeWidth={4} /></>,
    mic: <><rect x={36} y={10} width={24} height={44} rx={12} {...sf} /><path d="M24 44 Q24 70 48 70 Q72 70 72 44 M48 70 V86 M34 86 H62" {...st} /></>,
    patch: <><rect x={10} y={20} width={32} height={22} rx={5} {...sf} /><rect x={10} y={54} width={32} height={22} rx={5} {...sf} opacity={0.6} /><text x={26} y={37} textAnchor="middle" fontFamily="Montserrat" fontWeight={900} fontSize={16} fill="#14181F">V1</text><text x={26} y={71} textAnchor="middle" fontFamily="Montserrat" fontWeight={900} fontSize={16} fill="#14181F">A1</text><path d="M48 31 H82 M48 65 H82" {...st} /></>,
    io: <><path d="M20 20 H32 V76 H20 M76 20 H64 V76 H76" {...st} /><text x={48} y={58} textAnchor="middle" fontFamily="Montserrat" fontWeight={900} fontSize={22} fill={c}>I·O</text></>,
    lock: <><rect x={22} y={44} width={52} height={40} rx={8} {...sf} /><path d={`M32 44 V${32 - Math.max(0, Math.sin(t / 12)) * 6} Q32 16 48 16 Q64 16 64 32 V44`} {...st} /></>,
    link: <><rect x={10} y={36} width={40} height={24} rx={12} {...st} /><rect x={46} y={36} width={40} height={24} rx={12} {...st} /></>,
    arrow: <path d="M28 12 L28 78 L44 62 L54 86 L64 82 L54 58 L76 58 Z" {...sf} />,
    razor: <><path d="M10 48 H86" {...st} strokeDasharray="8 8" opacity={0.5} /><path d={`M${48 + Math.sin(t / 8) * 2} 10 V86`} {...st} stroke="#FF5A5F" /><path d="M36 22 L60 22 L56 38 L40 38 Z" {...sf} /></>,
    ripple: <><rect x={8} y={36} width={26} height={24} rx={4} {...sf} /><rect x={38 + 12 * (0.5 + 0.5 * Math.sin(t / 10))} y={36} width={26} height={24} rx={4} {...sf} opacity={0.7} /><path d="M70 30 Q86 48 70 66" {...st} /></>,
    rate: <><path d="M14 70 A36 36 0 0 1 82 70" {...st} /><path d={`M48 70 L${48 + 28 * Math.cos(Math.PI + (0.5 + 0.5 * Math.sin(t / 10)) * Math.PI)} ${70 + 28 * Math.sin(Math.PI + (0.5 + 0.5 * Math.sin(t / 10)) * Math.PI)}`} {...st} /><circle cx={48} cy={70} r={6} {...sf} /></>,
    slip: <><rect x={14} y={34} width={68} height={28} rx={5} {...st} /><rect x={24 + 10 * Math.sin(t / 10)} y={40} width={48} height={16} rx={3} {...sf} /><path d="M8 80 L20 74 M8 80 L20 86 M88 80 L76 74 M88 80 L76 86 M8 80 H88" {...st} strokeWidth={4} /></>,
    magnet: <><path d="M22 18 V50 Q22 76 48 76 Q74 76 74 50 V18" {...st} strokeWidth={14} stroke={c} /><path d="M22 18 V30 M74 18 V30" {...st} strokeWidth={14} stroke="#FF5A5F" /></>,
    plus: <><rect x={10} y={22} width={60} height={14} rx={4} {...sf} opacity={0.5} /><rect x={10} y={42} width={60} height={14} rx={4} {...sf} opacity={0.7} /><path d="M78 56 V84 M64 70 H92" {...st} /></>,
    export: <><path d="M20 40 V82 H76 V40" {...st} /><path d={`M48 ${58 - ((t / 2) % 16)} V12 M34 26 L48 12 L62 26`} {...st} /></>,
    folder: <path d="M10 26 H38 L44 32 H86 V78 H10 Z" {...sf} />,
    watch: <><circle cx={48} cy={52} r={32} {...st} /><path d="M40 12 H56 M48 12 V20" {...st} /><path d={`M48 52 L${48 + 22 * Math.sin(t / 6)} ${52 - 22 * Math.cos(t / 6)}`} {...st} /></>,
    curve: <><path d="M10 84 H86 M10 84 V10" {...st} strokeWidth={4} opacity={0.4} /><path d="M12 80 C 50 80, 46 18, 84 16" {...st} /><circle cx={12 + 72 * ((t / 60) % 1)} cy={80 - 64 * (3 * ((t / 60) % 1) ** 2 - 2 * ((t / 60) % 1) ** 3)} r={7} {...sf} /></>,
    blend: <><circle cx={36} cy={48} r={24} fill={c} opacity={0.7} /><circle cx={60} cy={48} r={24} fill={G.blue} opacity={0.7} style={{mixBlendMode: 'screen'}} /></>,
    fade: <><rect x={10} y={30} width={44} height={36} rx={5} {...sf} /><rect x={42} y={30} width={44} height={36} rx={5} fill={G.blue} opacity={0.5 + 0.5 * Math.sin(t / 10)} /></>,
    trans: <><rect x={8} y={30} width={40} height={36} rx={5} {...sf} /><rect x={48} y={30} width={40} height={36} rx={5} fill={G.blue} /><path d="M48 22 V74" {...st} stroke="#fff" strokeWidth={4} /></>,
    fx: <>{[0, 72, 144, 216, 288].map((a) => <path key={a} d="M48 48 L48 14" {...st} transform={`rotate(${a + t * 1.5} 48 48)`} />)}<circle cx={48} cy={48} r={10} {...sf} /></>,
    mask: <><circle cx={48} cy={48} r={30} {...st} strokeDasharray="10 8" strokeDashoffset={-t} /><path d="M62 24 L80 10 L86 16 L70 32 Z" {...sf} /></>,
    text: <><text x={48} y={72} textAnchor="middle" fontFamily="Montserrat" fontWeight={900} fontSize={70} fill={c}>T</text><path d={`M${70 + (Math.floor(t / 12) % 2) * 100} 24 V76`} {...st} strokeWidth={4} /></>,
    slides: <>{[0, 1, 2].map((i) => <rect key={i} x={14 + i * 10} y={18 + i * 10} width={52} height={40} rx={5} fill={i === 2 ? c : 'none'} stroke={c} strokeWidth={5} />)}</>,
    nest: <><rect x={10} y={10} width={76} height={76} rx={10} {...st} /><rect x={22} y={22} width={22} height={14} rx={3} {...sf} /><rect x={48} y={22} width={26} height={14} rx={3} {...sf} opacity={0.7} /><rect x={22} y={42} width={52} height={14} rx={3} {...sf} opacity={0.5} /><rect x={22} y={62} width={34} height={14} rx={3} {...sf} opacity={0.8} /></>,
    wave: <>{Array.from({length: 11}).map((_, i) => { const hh = 10 + 30 * Math.abs(Math.sin(i * 1.3 + t / 6)); return <rect key={i} x={10 + i * 7.4} y={48 - hh / 2} width={4.5} height={hh} rx={2} {...sf} />; })}</>,
    pan: <><text x={18} y={62} fontFamily="Montserrat" fontWeight={900} fontSize={26} fill={c}>L</text><text x={66} y={62} fontFamily="Montserrat" fontWeight={900} fontSize={26} fill={c}>R</text><circle cx={48 + 10 * Math.sin(t / 10)} cy={52} r={10} {...sf} /><path d="M38 30 H58" {...st} strokeWidth={4} /></>,
    knob: <><circle cx={48} cy={50} r={30} {...st} /><path d={`M48 50 L${48 + 22 * Math.cos(-2.3 + 1.6 * (0.5 + 0.5 * Math.sin(t / 12)))} ${50 + 22 * Math.sin(-2.3 + 1.6 * (0.5 + 0.5 * Math.sin(t / 12)))}`} {...st} /><text x={48} y={94} textAnchor="middle" fontFamily="Montserrat" fontWeight={800} fontSize={14} fill={c}>dB</text></>,
    layers: <>{[0, 1, 2].map((i) => <path key={i} d={`M48 ${20 + i * 18} L84 ${36 + i * 18} L48 ${52 + i * 18} L12 ${36 + i * 18} Z`} fill={i === 0 ? c : 'none'} stroke={c} strokeWidth={5} opacity={i === 0 ? 0.6 + 0.4 * Math.sin(t / 10) : 1} />)}</>,
    drop: <path d="M48 12 Q72 44 72 60 Q72 84 48 84 Q24 84 24 60 Q24 44 48 12 Z" fill={c} />,
    wheel: <g transform={`rotate(${t} 48 48)`}>{['#FF5A5F', '#F5B83D', '#35D07F', '#3BA9F5', '#9999FF', '#FF6BD5'].map((col, i) => <path key={i} d="M48 48 L48 12 A36 36 0 0 1 79.2 30 Z" fill={col} transform={`rotate(${i * 60} 48 48)`} />)}</g>,
    freeze: <><rect x={22} y={18} width={16} height={60} rx={4} {...sf} /><rect x={58} y={18} width={16} height={60} rx={4} {...sf} /></>,
    newfile: <><path d="M20 10 H58 L76 28 V86 H20 Z" {...st} /><path d="M48 40 V72 M32 56 H64" {...st} /></>,
    green: <><rect x={10} y={16} width={76} height={64} rx={8} fill="#2BD15F" /><circle cx={48} cy={40} r={10} fill="#14181F" /><path d="M30 80 Q30 56 48 56 Q66 56 66 80" fill="#14181F" /></>,
    windows: <><rect x={10} y={14} width={34} height={30} rx={4} {...sf} /><rect x={52} y={14} width={34} height={30} rx={4} {...sf} opacity={0.6} /><rect x={10} y={52} width={76} height={30} rx={4} {...sf} opacity={0.8} /></>,
    flag: <><path d="M22 86 V12" {...st} /><path d={`M22 14 Q40 ${6 + 4 * Math.sin(t / 8)} 56 16 Q70 ${24 - 4 * Math.sin(t / 8)} 82 16 V46 Q70 54 56 46 Q40 38 22 46 Z`} {...sf} /></>,
    ear: <><path d="M62 70 Q58 86 44 84 Q34 82 34 72 Q34 64 40 58 Q30 52 30 38 Q30 14 52 14 Q74 14 74 38 Q74 50 66 58" {...st} /><path d="M50 40 Q50 32 56 32 Q62 32 62 40 Q62 46 56 50" {...st} strokeWidth={5} />{[0, 1].map((i) => <path key={i} d={`M${80 + i * 8} ${30 - i * 4} Q${88 + i * 8} 48 ${80 + i * 8} ${66 + i * 4}`} {...st} strokeWidth={4} opacity={0.3 + 0.7 * ((Math.floor(t / 10) + i) % 2)} />)}</>,
    sine: <><path d="M8 48 H88" {...st} strokeWidth={3} opacity={0.35} /><path d={Array.from({length: 41}).map((_, i) => `${i ? 'L' : 'M'}${8 + i * 2} ${48 - 26 * Math.sin(i / 40 * Math.PI * 4 + t / 6)}`).join(' ')} {...st} /></>,
    bits: <>{Array.from({length: 8}).map((_, i) => { const hh = 8 + 8 * Math.round(4 * Math.abs(Math.sin(i * 0.9 + t / 14))); return <rect key={i} x={8 + i * 10.5} y={84 - hh} width={8} height={hh} rx={1} {...sf} />; })}{[20, 36, 52, 68].map((y) => <path key={y} d={`M6 ${y} H90`} {...st} strokeWidth={1.5} opacity={0.35} />)}</>,
    clap: <><rect x={12} y={44} width={72} height={40} rx={5} {...sf} /><g transform={`rotate(${-18 * Math.max(0, Math.sin(t / 7))} 14 40)`}><rect x={12} y={28} width={72} height={12} rx={3} {...sf} />{[0, 1, 2, 3].map((i) => <path key={i} d={`M${22 + i * 18} 28 L${30 + i * 18} 40`} stroke="#14181F" strokeWidth={5} />)}</g></>,
    ques: <><circle cx={48} cy={48} r={36} {...st} /><text x={48} y={64} textAnchor="middle" fontFamily="Montserrat" fontWeight={900} fontSize={46} fill={c}>?</text></>,
    phones: <><path d="M18 60 V48 Q18 18 48 18 Q78 18 78 48 V60" {...st} /><rect x={12} y={54} width={18} height={30} rx={6} {...sf} /><rect x={66} y={54} width={18} height={30} rx={6} {...sf} /></>,
    music: <><path d="M34 70 V22 L74 14 V60" {...st} /><circle cx={26} cy={70} r={10} {...sf} /><circle cx={66} cy={62} r={10} {...sf} /></>,
    cam: <><rect x={10} y={30} width={56} height={44} rx={8} {...sf} /><path d="M66 44 L88 32 V72 L66 60 Z" {...sf} /><circle cx={24} cy={20} r={10} {...st} strokeWidth={5} /><circle cx={50} cy={20} r={10} {...st} strokeWidth={5} /></>,
  };
  return (
    <svg width={W * s} height={W * s} viewBox="0 0 96 96" style={{overflow: 'visible', transform: `translateY(${bob * s}px)`}}>
      {body[n] ?? body.play}
    </svg>
  );
};

// ---------- chapter separator (between chapters): music + "next chapter" title; a still of the coming screen keeps the
// recording visible (Aly: never a moment without the screen). ----------
export const Sep: React.FC<{n: number; total: number; ep: number; title: string; en?: string; ico: string; thumb?: string; dur: number; part?: string; partN?: number; partC?: string}> = ({n, total, ep, title, en, ico, thumb, dur, part, partN, partC = G.blue}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 120, 16), q = spr(f, fps, 6, 140, 16);
  const o = 1 - lin(f, dur - 10, dur, 0, 1, Easing.in(Easing.cubic));
  const bar = lin(f, 0, dur - 6, 0, 1, Easing.linear);
  return (
    <AbsoluteFill style={{opacity: o}}>
      <CourseBg />
      {thumb ? (
        <div style={{position: 'absolute', right: 120, top: 270, width: 760, height: 428, borderRadius: 26, overflow: 'hidden', transform: `translateX(${(1 - q) * 120}px) scale(${0.96 + 0.04 * q})`,
          opacity: q, border: '2px solid rgba(255,255,255,0.25)', boxShadow: `0 30px 80px rgba(0,0,0,0.6), 0 0 60px ${G.blue}44`}}>
          <Img src={staticFile(thumb)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        </div>
      ) : null}
      <div style={{position: 'absolute', left: 120, top: 250, width: 880, direction: 'rtl', transform: `translateX(${(1 - p) * -80}px)`, opacity: Math.min(1, p * 1.4)}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 22, justifyContent: 'flex-start'}}>
          <div style={{padding: '6px 22px', borderRadius: 30, background: G.gold, fontFamily: AR, fontWeight: 900, fontSize: 34, color: '#14181F'}}>الفصل {n} من {total}</div>
          {part ? <div style={{padding: '4px 20px', borderRadius: 30, border: `2px solid ${partC}`, color: partC, fontFamily: AR, fontWeight: 900, fontSize: 30}}>{partN ? `الجزء ${partN}: ` : ''}{bi(part)}</div> : null}
        </div>
        <div style={{display: 'flex', alignItems: 'center', gap: 30, marginTop: 34}}>
          <div style={{width: 150, height: 150, borderRadius: 40, background: 'rgba(255,255,255,0.08)', border: '2px solid rgba(255,255,255,0.18)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>
            <Ico n={ico} s={1.1} />
          </div>
          <div>
            <div style={{fontFamily: AR, fontWeight: 900, fontSize: 76, color: G.ink, lineHeight: 1.2}}>{bi(title)}</div>
            {en ? <div style={{fontFamily: EN, fontWeight: 800, fontSize: 40, color: G.blue, direction: 'ltr', textAlign: 'right', marginTop: 6}}>{en}</div> : null}
          </div>
        </div>
        <div style={{marginTop: 60, height: 8, width: 700, borderRadius: 8, background: 'rgba(255,255,255,0.12)', overflow: 'hidden'}}>
          <div style={{height: '100%', width: `${((n - 1 + bar) / total) * 100}%`, background: `linear-gradient(90deg, ${G.blue}, ${G.gold})`, marginRight: 0, marginLeft: 'auto'}} />
        </div>
      </div>
    </AbsoluteFill>
  );
};

export {AR, EN, G, Glass, lin, Pill, spr};
