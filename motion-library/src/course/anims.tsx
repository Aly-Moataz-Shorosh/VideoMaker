import React, {createContext, useContext} from 'react';
import {Easing, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, bi, CC, EN, G, lin, spr} from './kit';

// Concept animations for the left column (side mode, x 0..680). Each one explains what Aly is explaining at that moment.
type P = {dur: number; [k: string]: any};
// shorts: captions already carry the sentence, so the bottom note is hidden (it collided with captions/Kw)
export const HideNote = createContext(false);
const Col: React.FC<{dur: number; title: string; children: React.ReactNode; note?: string}> = ({dur, title, children, note}) => {
  const f = useCurrentFrame();
  const o = Math.min(lin(f, 0, 10), 1 - lin(f, dur - 10, dur));
  if (useContext(HideNote)) note = undefined;
  return (
    <div style={{position: 'absolute', left: 20, top: 150, width: 640, height: 780, opacity: o, transform: `translateX(${(1 - lin(f, 0, 12)) * -40}px)`}}>
      <div style={{fontFamily: AR, fontWeight: 900, fontSize: 44, color: G.ink, textAlign: 'center', direction: 'rtl', lineHeight: 1.3}}>{bi(title)}</div>
      <div style={{position: 'relative', width: 640, height: 600, marginTop: 20}}>{children}</div>
      {note ? <div style={{fontFamily: AR, fontWeight: 700, fontSize: 30, color: G.soft, textAlign: 'center', direction: 'rtl', lineHeight: 1.4, opacity: lin(f, 40, 56)}}>{bi(note)}</div> : null}
    </div>
  );
};
const box = (x: number, y: number, w: number, h: number, c: string, extra: React.CSSProperties = {}): React.CSSProperties =>
  ({position: 'absolute', left: x, top: y, width: w, height: h, background: c, borderRadius: 8, ...extra});

// Resolution: the same circle drawn with 10x10, 20x20, 40x40 pixels -> sharper.
const ResGrid: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const levels = [10, 20, 40];
  const k = Math.min(2, Math.floor(Math.max(0, f - 10) / 45));
  const n = levels[k], S = 360, c = S / n;
  const cells = [];
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
    const dx = (i + 0.5) / n - 0.5, dy = (j + 0.5) / n - 0.5;
    const on = Math.sqrt(dx * dx + dy * dy) < 0.38;
    if (on) cells.push(<div key={i + '-' + j} style={box(i * c, j * c, c - (n < 30 ? 1 : 0), c - (n < 30 ? 1 : 0), G.gold, {borderRadius: 0})} />);
  }
  return (
    <Col dur={dur} title="نفس المساحة.. بيكسلز أكتر = صورة أوضح" note={`${n} × ${n} بيكسل`}>
      <div style={{position: 'absolute', left: 140, top: 40, width: S, height: S, background: '#141B28', border: '2px solid rgba(255,255,255,0.25)'}}>{cells}</div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 430, display: 'flex', justifyContent: 'center', gap: 16, direction: 'ltr'}}>
        {levels.map((l, i) => <div key={l} style={{padding: '6px 18px', borderRadius: 20, fontFamily: EN, fontWeight: 900, fontSize: 28, background: i === k ? G.gold : 'rgba(255,255,255,0.1)', color: i === k ? '#14181F' : G.soft}}>{l}×{l}</div>)}
      </div>
    </Col>
  );
};

// Resolution ladder: SD -> HD -> 4K boxes growing (numbers from Adobe).
const ResLadder: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const R = [{n: 'SD', w: 720, h: 480, c: G.dim}, {n: 'Full HD', w: 1920, h: 1080, c: G.blue}, {n: '4K', w: 3840, h: 2160, c: G.gold}];
  return (
    <Col dur={dur} title="كل ما البيكسلز تزيد.. الصورة أوضح" note="Full HD = 1920 × 1080 · 4K = 3840 × 2160 (Adobe)">
      {R.slice().reverse().map((r, i) => {
        const idx = R.length - 1 - i;
        const p = spr(f, fps, 8 + idx * 14, 140, 16);
        const sc = 560 / 3840;
        return (
          <div key={r.n} style={{position: 'absolute', left: 40, top: 40 + (2160 - r.h) * sc, width: r.w * sc * p, height: r.h * sc * p, border: `4px solid ${r.c}`, borderRadius: 6,
            background: `${r.c}18`, opacity: Math.min(1, p * 1.4)}}>
            <span style={{position: 'absolute', left: 8, top: 4, fontFamily: EN, fontWeight: 900, fontSize: 24, color: r.c, whiteSpace: 'nowrap'}}>{r.n}</span>
          </div>
        );
      })}
    </Col>
  );
};

// Timeline: events on tracks over time with a playhead.
const TimelineAnim: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const ph = 40 + ((f * 2.2) % 540);
  const clips = [[0, 40, 200, G.blue], [0, 280, 180, G.blue], [1, 140, 240, CC.violet], [2, 60, 380, G.green], [3, 200, 160, G.gold]] as const;
  return (
    <Col dur={dur} title="Timeline = خط الزمن" note="فوق: الثواني · تحت: الطبقات (Layers)">
      <div style={{position: 'absolute', left: 40, top: 30, width: 560, height: 30, borderBottom: '2px solid rgba(255,255,255,0.3)', display: 'flex', justifyContent: 'space-between', direction: 'ltr'}}>
        {[0, 1, 2, 3, 4, 5].map((s) => <span key={s} style={{fontFamily: EN, fontWeight: 700, fontSize: 20, color: G.dim}}>{s}s</span>)}
      </div>
      {clips.map(([tr, x, w, c], i) => <div key={i} style={box(40 + x, 80 + tr * 80, w * lin(f, 6 + i * 6, 26 + i * 6), 56, c, {opacity: 0.9})} />)}
      {[0, 1, 2, 3].map((tr) => <div key={tr} style={{position: 'absolute', left: 0, top: 96 + tr * 80, fontFamily: EN, fontWeight: 800, fontSize: 20, color: G.dim}}>{tr < 3 ? `V${3 - tr}` : 'A1'}</div>)}
      <div style={{position: 'absolute', left: ph, top: 20, width: 4, height: 400, background: '#FF5A5F', boxShadow: '0 0 12px #FF5A5F'}} />
    </Col>
  );
};

// Keyframe: ball at keyframe A and keyframe B, the program fills the frames in between.
const KeyAnim: React.FC<P> = ({dur, ease = false}) => {
  const f = useCurrentFrame();
  const t = ((f % 75) / 60);
  const u = Math.min(1, t);
  const e = ease ? (u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2) : u;
  const x = 60 + 440 * e;
  return (
    <Col dur={dur} title={ease ? 'Ease: يبدأ بالراحة ويهدى في الآخر' : 'Keyframe A ← → Keyframe B'} note="انت بتحط المكانين.. والبرنامج بيعمل الحركة اللي بينهم">
      <div style={{position: 'absolute', left: 60, top: 200, width: 500, height: 4, background: 'rgba(255,255,255,0.15)'}} />
      {[60, 500].map((kx, i) => (
        <div key={i} style={{position: 'absolute', left: kx + 12, top: 290, width: 30, height: 30, background: G.gold, transform: 'rotate(45deg)'}}>
          <span style={{position: 'absolute', left: -2, top: 34, transform: 'rotate(-45deg)', fontFamily: EN, fontWeight: 900, fontSize: 26, color: G.gold}}>{i ? 'B' : 'A'}</span>
        </div>
      ))}
      {Array.from({length: 9}).map((_, i) => <div key={i} style={{position: 'absolute', left: 60 + 440 * (ease ? (i / 8 < 0.5 ? 4 * (i / 8) ** 3 : 1 - Math.pow(-2 * (i / 8) + 2, 3) / 2) : i / 8) + 18, top: 186, width: 20, height: 20,
        borderRadius: '50%', border: '2px solid rgba(255,255,255,0.3)'}} />)}
      <div style={{position: 'absolute', left: x, top: 172, width: 56, height: 56, borderRadius: '50%', background: G.blue, boxShadow: `0 0 30px ${G.blue}`}} />
      <div style={{position: 'absolute', left: 60, top: 400, width: 500, height: 150, borderLeft: '2px solid rgba(255,255,255,0.3)', borderBottom: '2px solid rgba(255,255,255,0.3)'}}>
        <svg width={500} height={150} style={{position: 'absolute', left: 0, top: 0}}>
          <path d={ease ? 'M0 150 C 250 150, 250 0, 500 0' : 'M0 150 L500 0'} stroke={G.gold} strokeWidth={5} fill="none" />
        </svg>
        <span style={{position: 'absolute', right: 0, top: 156, fontFamily: EN, fontWeight: 700, fontSize: 20, color: G.dim}}>time →</span>
      </div>
    </Col>
  );
};

// Sequence / Nest: many clips packed into one box (like a function in code).
const NestAnim: React.FC<P> = ({dur, title = 'Sequence = علبة فيها كل حاجة', note = 'زي الـ function في البرمجة: تعملها مرة وتستخدمها كذا مرة'}) => {
  const f = useCurrentFrame();
  const k = lin(f, 30, 60, 0, 1, Easing.inOut(Easing.cubic));
  const items = [['🎬', G.blue], ['🖼', CC.violet], ['🎵', G.green], ['✨', G.gold], ['T', CC.coral]] as const;
  return (
    <Col dur={dur} title={title} note={note}>
      <div style={{position: 'absolute', left: 170, top: 160, width: 300, height: 220, borderRadius: 26, border: `4px dashed ${G.gold}`, opacity: k}} />
      {items.map(([ic, c], i) => {
        const x0 = 40 + i * 115, y0 = 20, x1 = 200 + (i % 3) * 82, y1 = 190 + Math.floor(i / 3) * 90;
        return (
          <div key={i} style={{...box(x0 + (x1 - x0) * k, y0 + (y1 - y0) * k, 70, 70, c, {borderRadius: 16}), display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 34,
            color: '#fff', fontFamily: EN, fontWeight: 900}}>{ic}</div>
        );
      })}
      <div style={{position: 'absolute', left: 0, right: 0, top: 410, textAlign: 'center', opacity: lin(f, 66, 80)}}>
        <span style={{padding: '8px 24px', borderRadius: 24, background: G.gold, fontFamily: EN, fontWeight: 900, fontSize: 32, color: '#14181F'}}>= 1 Sequence</span>
      </div>
    </Col>
  );
};

// Slow motion math: shoot fps x speed % = timeline fps.
const SlowMath: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  // Aly 2026-10-18: 200% is a SPEED-UP, not slow motion -> its own labelled row under a divider
  const rows = [['30 fps', '80%', '24'], ['60 fps', '40%', '24'], ['120 fps', '20%', '24']];
  const pf = lin(f, 10 + 3 * 14, 24 + 3 * 14);
  const row = (r: string[], top: number, p: number, col: string) => (
    <div style={{position: 'absolute', left: 30, top, width: 580, height: 80, borderRadius: 20, background: 'rgba(255,255,255,0.06)', opacity: p,
      transform: `translateX(${(1 - p) * -40}px)`, display: 'flex', alignItems: 'center', justifyContent: 'space-around', direction: 'ltr', fontFamily: EN, fontWeight: 900, fontSize: 36}}>
      <span style={{color: G.blue}}>{r[0]}</span><span style={{color: G.dim}}>×</span><span style={{color: col}}>{r[1]}</span>
      <span style={{color: G.dim}}>=</span><span style={{color: G.gold}}>{r[2]}</span>
    </div>
  );
  return (
    <Col dur={dur} title="فريمات التصوير × السرعة = 24">
      <div style={{position: 'absolute', left: 30, top: 0, fontFamily: AR, fontWeight: 900, fontSize: 30, color: G.green, direction: 'rtl', width: 580, textAlign: 'right'}}>🐢 Slow motion</div>
      {rows.map((r, i) => row(r, 44 + i * 96, lin(f, 10 + i * 14, 24 + i * 14), G.green))}
      <div style={{position: 'absolute', left: 30, top: 350, width: 580, height: 3, background: 'rgba(255,255,255,0.15)', opacity: pf}} />
      <div style={{position: 'absolute', left: 30, top: 362, fontFamily: AR, fontWeight: 900, fontSize: 30, color: CC.coral, direction: 'rtl', width: 580, textAlign: 'right', opacity: pf}}>⏩ تسريع (مش Slow motion)</div>
      {row(['12 fps', '200%', '24'], 406, pf, CC.coral)}
    </Col>
  );
};

// Insert vs Overwrite: a new clip enters a row of clips.
const InsOver: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const k = lin(f, 20, 50, 0, 1, Easing.inOut(Easing.cubic));
  const row = (y: number, label: string, ins: boolean) => (
    <>
      <div style={{position: 'absolute', left: 0, top: y - 50, fontFamily: EN, fontWeight: 900, fontSize: 30, color: ins ? G.green : CC.coral}}>{label}</div>
      <div style={box(20, y, 180, 60, G.blue)} />
      <div style={box(200 + (ins ? 160 * k : 0), y, 200, 60, CC.violet, {opacity: ins ? 1 : 1 - 0.7 * k})} />
      <div style={box(400 + (ins ? 160 * k : 0), y, 160, 60, G.blue, {opacity: 0.8})} />
      <div style={box(200, y - 90 + 90 * k, 160, 60, G.gold, {zIndex: 2})} />
    </>
  );
  return (
    <Col dur={dur} title="Insert (,) ضد Overwrite (.)" note="Insert بيزق اللي بعده · Overwrite بيكتب فوقه">
      {row(110, 'Insert  ,', true)}
      {row(360, 'Overwrite  .', false)}
    </Col>
  );
};

// Ripple vs Rolling edit.
const RippleRoll: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const k = Math.sin(Math.min(1, lin(f, 20, 70)) * Math.PI);
  return (
    <Col dur={dur} title="Ripple ضد Rolling" note="Ripple: يقص ويقفل الفراغ · Rolling: يطوّل ده ويقصّر اللي جنبه">
      <div style={{position: 'absolute', left: 0, top: 50, fontFamily: EN, fontWeight: 900, fontSize: 30, color: G.green}}>Ripple</div>
      <div style={box(20, 100, 260 - 90 * k, 60, G.blue)} />
      <div style={box(280 - 90 * k, 100, 200, 60, CC.violet)} />
      <div style={box(480 - 90 * k, 100, 120, 60, G.blue, {opacity: 0.8})} />
      <div style={{position: 'absolute', left: 0, top: 300, fontFamily: EN, fontWeight: 900, fontSize: 30, color: G.gold}}>Rolling</div>
      <div style={box(20, 350, 260 + 80 * k, 60, G.blue)} />
      <div style={box(280 + 80 * k, 350, 200 - 80 * k, 60, CC.violet)} />
      <div style={box(480, 350, 120, 60, G.blue, {opacity: 0.8})} />
      <div style={{position: 'absolute', left: 278 + 80 * k, top: 340, width: 4, height: 80, background: G.gold}} />
    </Col>
  );
};

// Slip vs Slide.
const SlipSlide: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const k = Math.sin(lin(f, 10, dur - 10) * Math.PI * 2);
  return (
    <Col dur={dur} title="Slip ضد Slide" note="Slip: نفس المكان، جزء تاني من الكليب · Slide: الكليب نفسه بيتحرك">
      <div style={{position: 'absolute', left: 0, top: 40, fontFamily: EN, fontWeight: 900, fontSize: 30, color: G.green}}>Slip</div>
      <div style={box(20, 90, 180, 70, G.blue)} />
      <div style={{...box(200, 90, 220, 70, '#1d2840'), overflow: 'hidden', border: `3px solid ${G.gold}`}}>
        {[1, 2, 3, 4, 5, 6, 7].map((d) => <span key={d} style={{position: 'absolute', left: 30 + (d - 1) * 60 + 40 * k - 60, top: 12, fontFamily: EN, fontWeight: 900, fontSize: 36, color: G.gold}}>{d}</span>)}
      </div>
      <div style={box(420, 90, 180, 70, G.blue, {opacity: 0.8})} />
      <div style={{position: 'absolute', left: 0, top: 300, fontFamily: EN, fontWeight: 900, fontSize: 30, color: G.gold}}>Slide</div>
      <div style={box(20, 350, 180 + 60 * k, 70, G.blue)} />
      <div style={box(200 + 60 * k, 350, 220, 70, CC.violet, {border: `3px solid ${G.gold}`})} />
      <div style={box(420 + 60 * k, 350, 180 - 60 * k, 70, G.blue, {opacity: 0.8})} />
    </Col>
  );
};

// Linear / Hold / Bezier: three balls side by side.
const InterpAnim: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const u = Math.min(1, (f % 80) / 60);
  const kinds = [['Linear', u, G.blue], ['Hold', u < 0.98 ? 0 : 1, CC.coral], ['Bezier', u < 0.5 ? 4 * u ** 3 : 1 - Math.pow(-2 * u + 2, 3) / 2, G.gold]] as const;
  return (
    <Col dur={dur} title="3 أنواع Keyframes" note="Linear: بالتساوي · Hold: فجأة · Bezier: بنعومة">
      {kinds.map(([n, v, c], i) => (
        <div key={n}>
          <div style={{position: 'absolute', left: 0, top: 40 + i * 160, fontFamily: EN, fontWeight: 900, fontSize: 30, color: c}}>{n}</div>
          <div style={{position: 'absolute', left: 150, top: 70 + i * 160, width: 440, height: 4, background: 'rgba(255,255,255,0.15)'}} />
          <div style={{position: 'absolute', left: 150 + 400 * v, top: 48 + i * 160, width: 48, height: 48, borderRadius: '50%', background: c, boxShadow: `0 0 24px ${c}`}} />
        </div>
      ))}
    </Col>
  );
};

// Blend mode: white background disappears with Multiply.
const BlendAnim: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const k = lin(f, 30, 50);
  return (
    <Col dur={dur} title="Multiply: الأبيض بيختفي" note="فاكر الـ Blending modes في Photoshop؟ هي هي">
      <div style={{position: 'absolute', left: 120, top: 40, width: 400, height: 300, borderRadius: 16, background: 'linear-gradient(135deg, #3BA9F5, #9999FF 60%, #F5B83D)'}} />
      <div style={{position: 'absolute', left: 170, top: 90, width: 300, height: 200, borderRadius: 12, background: '#fff', mixBlendMode: k > 0.5 ? 'multiply' : 'normal', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <svg width={220} height={150} viewBox="0 0 220 150"><path d="M20 120 C 60 20, 120 140, 200 30" stroke="#14181F" strokeWidth={18} fill="none" strokeLinecap="round" /></svg>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 380, textAlign: 'center'}}>
        <span style={{padding: '8px 24px', borderRadius: 24, background: k > 0.5 ? G.gold : 'rgba(255,255,255,0.12)', fontFamily: EN, fontWeight: 900, fontSize: 32, color: k > 0.5 ? '#14181F' : G.soft}}>{k > 0.5 ? 'Multiply' : 'Normal'}</span>
      </div>
    </Col>
  );
};

// Adjustment layer: one layer on top colours every clip under it.
const AdjAnim: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const k = lin(f, 30, 50);
  return (
    <Col dur={dur} title="Adjustment layer: طبقة فاضية فوق الكل" note="أي إفكت عليها بيتطبق على كل اللي تحتها مرة واحدة">
      <div style={box(40, 60 - 40 * (1 - k), 560, 70, `rgba(245,184,61,${0.25 + 0.35 * k})`, {border: `3px dashed ${G.gold}`, opacity: k})}>
        <span style={{position: 'absolute', left: 16, top: 16, fontFamily: EN, fontWeight: 900, fontSize: 28, color: '#fff'}}>Adjustment Layer</span>
      </div>
      {[0, 1, 2].map((i) => <div key={i} style={box(40 + i * 190, 170 + i * 90, 180, 70, G.blue, {filter: `sepia(${k}) saturate(${1 + k})`, opacity: 0.95})} />)}
    </Col>
  );
};


// Keyframe interpolation, drawn correctly (Adobe helpx): ball positions at EQUAL time steps (ghost dots) + value/time graph.
//   linear = straight line, equal steps · hold = flat then jumps at the next keyframe · bezier = slow-fast-slow (S)
//   easeIn = slows down ENTERING the keyframe (end) · easeOut = speeds up gradually LEAVING the keyframe (start)
const IFN: Record<string, (u: number) => number> = {
  linear: (u) => u,
  hold: (u) => (u < 1 ? 0 : 1),
  bezier: (u) => (u < 0.5 ? 4 * u ** 3 : 1 - Math.pow(-2 * u + 2, 3) / 2),
  easeIn: (u) => 1 - Math.pow(1 - u, 3),
  easeOut: (u) => u ** 3,
};
const ICOL: Record<string, string> = {linear: G.blue, hold: CC.coral, bezier: G.gold, easeIn: G.gold, easeOut: G.gold};
const ITXT: Record<string, [string, string]> = {
  linear: ['Linear', 'نفس الخطوة كل فريم.. ناشفة زي الروبوت'],
  hold: ['Hold', 'واقف مكانه.. وفجأة ينط'],
  bezier: ['Bezier', 'يبدأ بالراحة.. يسرع.. ويهدى'],
  easeIn: ['Ease In', 'بيهدى وهو داخل على الكيفريم'],
  easeOut: ['Ease Out', 'بيبدأ بالراحة وهو خارج من الكيفريم'],
};
const IRow: React.FC<{k: string; u: number; y: number; w: number; gh: number; big?: boolean}> = ({k, u, y, w, gh, big}) => {
  const fn = IFN[k], c = ICOL[k], N = 8;
  const pts = Array.from({length: 41}, (_, i) => i / 40);
  const path = k === 'hold'
    ? `M0 ${gh} H${w * Math.min(u, 0.999)}` + (u >= 1 ? ` H${w} V0` : '')
    : 'M' + pts.filter((p) => p <= u + 1e-6).map((p) => `${w * p} ${gh * (1 - fn(p))}`).join(' L');
  return (
    <div style={{position: 'absolute', left: 0, top: y, width: 640}}>
      <div style={{position: 'absolute', left: 0, top: 0, fontFamily: EN, fontWeight: 900, fontSize: big ? 40 : 30, color: c}}>{ITXT[k][0]}</div>
      {/* track: ghost dots = where the ball is at each equal time step */}
      <div style={{position: 'absolute', left: 40, top: big ? 92 : 62, width: w, height: 4, background: 'rgba(255,255,255,0.15)'}} />
      {Array.from({length: N + 1}, (_, i) => (
        <div key={i} style={{position: 'absolute', left: 40 + w * fn(i / N) - 9, top: (big ? 92 : 62) - 8, width: 18, height: 18, borderRadius: '50%',
          border: `2px solid ${c}`, opacity: i / N <= u ? 0.55 : 0}} />
      ))}
      <div style={{position: 'absolute', left: 40 + w * fn(u) - 24, top: (big ? 92 : 62) - 22, width: 48, height: 48, borderRadius: '50%', background: c, boxShadow: `0 0 24px ${c}`}} />
      {/* graph: position over time */}
      <div style={{position: 'absolute', left: 40, top: big ? 150 : 100, width: w, height: gh, borderLeft: '2px solid rgba(255,255,255,0.35)', borderBottom: '2px solid rgba(255,255,255,0.35)'}}>
        <svg width={w} height={gh} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
          <path d={path} stroke={c} strokeWidth={5} fill="none" strokeLinejoin="round" />
          {[[0, gh], [w, 0]].map(([x, yy], i) => <rect key={i} x={x - 9} y={yy - 9} width={18} height={18} fill={G.gold} transform={`rotate(45 ${x} ${yy})`} opacity={i === 0 || u >= 1 ? 1 : 0.35} />)}
        </svg>
        {big ? <>
          <span style={{position: 'absolute', right: 0, top: gh + 6, fontFamily: AR, fontWeight: 700, fontSize: 22, color: G.dim}}>الوقت →</span>
          <span style={{position: 'absolute', left: -34, top: -34, fontFamily: AR, fontWeight: 700, fontSize: 22, color: G.dim}}>المكان ↑</span>
        </> : null}
      </div>
    </div>
  );
};
const InterpGraph: React.FC<P> = ({dur, kind = 'linear'}) => {
  const f = useCurrentFrame();
  const u = Math.min(1, Math.max(0, ((f - 10) % 90) / 66));
  if (kind === 'all') {
    return (
      <Col dur={dur} title="نفس الكيفريمين.. 3 أنواع حركة">
        {['linear', 'hold', 'bezier'].map((k, i) => <IRow key={k} k={k} u={u} y={i * 200} w={540} gh={80} />)}
      </Col>
    );
  }
  return (
    <Col dur={dur} title={ITXT[kind][1]}>
      <IRow k={kind} u={u} y={40} w={540} gh={300} big />
    </Col>
  );
};


// His own example (ch 4): a rose on a layer. Stage 1: at frame 10 the rose is at A -> press (stopwatch) -> "Save" = keyframe.
// Stage 2: go to frame 20, move the rose to B -> second "Save" -> play: the program moves it A -> B by itself.
const RoseKey: React.FC<P> = ({dur, stage = 1}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const T = 1.0 * fps;                      // beats
  const AX = 90, BX = 470, TY = 330, TL = 70, TW = 500;
  const fx = (fr: number) => TL + TW * (fr / 30);  // timeline ruler: frames 0..30
  let rose = AX, ph = 10, k1 = 0, k2 = 0, s1 = 0, s2 = 0, play = 0;
  if (stage === 1) {
    ph = 10;
    k1 = spr(f, fps, 1.2 * T, 200, 14); s1 = lin(f, 1.2 * T, 1.5 * T) * (1 - lin(f, 4 * T, 4.4 * T));
  } else {
    k1 = 1;
    const mv = lin(f, 0.3 * T, 1.3 * T, 0, 1, Easing.inOut(Easing.cubic));       // playhead to frame 20
    ph = 10 + 10 * mv;
    const drag = lin(f, 1.6 * T, 2.8 * T, 0, 1, Easing.inOut(Easing.cubic));     // he drags the rose to B
    rose = AX + (BX - AX) * drag;
    k2 = spr(f, fps, 3.0 * T, 200, 14); s2 = lin(f, 3.0 * T, 3.3 * T) * (1 - lin(f, 5.2 * T, 5.6 * T));
    const P0 = 5.8 * T;                                                        // play: from frame 10 to 20, the program moves it
    if (f > P0) {
      const u = ((f - P0) % (2.4 * T)) / (2 * T);
      play = 1; ph = 10 + 10 * Math.min(1, u); rose = AX + (BX - AX) * Math.min(1, u);
    }
  }
  const pill = (txt: string, x: number, o: number) => o <= 0 ? null : (
    <div style={{position: 'absolute', left: x - 90, top: 120, width: 180, textAlign: 'center', opacity: o, transform: `translateY(${(1 - o) * 14}px)`}}>
      <span style={{padding: '8px 18px', borderRadius: 30, background: G.gold, color: '#14181F', fontFamily: EN, fontWeight: 900, fontSize: 30}}>💾 Save</span>
      <div style={{fontFamily: AR, fontWeight: 700, fontSize: 24, color: G.ink, marginTop: 10, direction: 'rtl'}}>{txt}</div>
    </div>
  );
  return (
    <Col dur={dur} title={stage === 1 ? 'فريم 10: الوردة هنا ← Save' : play ? 'Play: البرنامج حرّكها لوحده' : 'فريم 20: حرّكها ← Save تاني'}>
      {/* the stage */}
      <div style={{position: 'absolute', left: 30, top: 0, width: 580, height: 260, borderRadius: 18, background: 'rgba(255,255,255,0.05)', border: '2px solid rgba(255,255,255,0.15)'}} />
      {['A', 'B'].map((l, i) => <div key={l} style={{position: 'absolute', left: (i ? BX : AX) + 6, top: 222, fontFamily: EN, fontWeight: 900, fontSize: 26, color: G.dim}}>{l}</div>)}
      <div style={{position: 'absolute', left: rose - 10, top: 70, fontSize: 110, lineHeight: 1}}>🌹</div>
      {pill('فريم 10 · المكان A', AX + 40, stage === 1 ? s1 : 0)}
      {pill('فريم 20 · المكان B', BX + 40, s2)}
      {/* the timeline with the playhead and the keyframes */}
      <div style={{position: 'absolute', left: TL, top: TY + 40, width: TW, height: 70, borderRadius: 10, background: 'rgba(255,255,255,0.06)'}} />
      <div style={{position: 'absolute', left: TL, top: TY + 52, width: TW, height: 46, borderRadius: 8, background: G.blue + '55', fontFamily: AR, fontSize: 22, color: G.ink, direction: 'rtl', paddingRight: 12, lineHeight: '46px'}}>Layer: الوردة</div>
      {[0, 10, 20, 30].map((fr) => <div key={fr} style={{position: 'absolute', left: fx(fr) - 20, top: TY, width: 40, textAlign: 'center', fontFamily: EN, fontWeight: 700, fontSize: 20, color: G.dim}}>{fr}</div>)}
      {[[10, k1], [20, k2]].map(([fr, q], i) => q > 0 ? <div key={i} style={{position: 'absolute', left: fx(fr) - 14, top: TY + 61, width: 28, height: 28, background: G.gold, transform: `rotate(45deg) scale(${q})`, boxShadow: `0 0 20px ${G.gold}`}} /> : null)}
      <div style={{position: 'absolute', left: fx(ph) - 2, top: TY + 26, width: 4, height: 100, background: '#FF5A5F'}} />
      <div style={{position: 'absolute', left: fx(ph) - 40, top: TY + 130, width: 80, textAlign: 'center', fontFamily: EN, fontWeight: 900, fontSize: 24, color: '#FF5A5F'}}>{Math.round(ph)}</div>
    </Col>
  );
};

export const courseAnims: Record<string, React.FC<P>> = {RoseKey, InterpGraph, ResGrid, ResLadder, TimelineAnim, KeyAnim, NestAnim, SlowMath, InsOver, RippleRoll, SlipSlide, InterpAnim, BlendAnim, AdjAnim};
