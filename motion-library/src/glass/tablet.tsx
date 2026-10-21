import React from 'react';
import {Img, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, Cursor, EN, G, GScene, Glass, In, Label, Mark, MONO, Pill, Type, lin, spr} from './kit';

// Graphic tablet shorts (2026-10-21, style 10 glass-face; end = QR of the full video like style 11).
// His camera (Cam) is ALWAYS on screen below; the stage is the TOP part (y 0..~700). Times in props are FRAMES from the
// scene start (make_shorts.py converts his source seconds). Most scenes are declarative: `items` = what appears when.
type It = {k: string; at: number; out?: number; x?: number; y?: number; text?: string; size?: number; color?: string; ink?: string;
  src?: string; w?: number; ok?: boolean; dir?: 'rtl' | 'ltr'; font?: string; sub?: string};

const PEN = '#1B1F27';

// ---------- vector props ----------
export const Tablet: React.FC<{w?: number; screen?: boolean; glow?: number; children?: React.ReactNode}> = ({w = 520, screen = false, glow = 0, children}) => {
  const h = w * 0.62;
  return (
    <div style={{position: 'relative', width: w, height: h, borderRadius: w * 0.045, background: 'linear-gradient(160deg, #2A2F38 0%, #0E1116 100%)',
      boxShadow: `0 30px 60px rgba(0,0,0,0.55), inset 0 2px 0 rgba(255,255,255,0.12)${glow ? `, 0 0 ${60 * glow}px ${G.blue}88` : ''}`, border: '2px solid rgba(255,255,255,0.12)'}}>
      {/* express keys + ring on the left, like his HS610 */}
      <div style={{position: 'absolute', left: w * 0.035, top: h * 0.14, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: h * 0.035}}>
        {[0, 1, 2].map((i) => <div key={i} style={{width: w * 0.05, height: h * 0.05, borderRadius: 6, background: '#3A404B'}} />)}
        <div style={{width: w * 0.085, height: w * 0.085, borderRadius: '50%', border: `${w * 0.008}px solid #3A404B`}} />
        {[0, 1, 2].map((i) => <div key={i} style={{width: w * 0.05, height: h * 0.05, borderRadius: 6, background: '#3A404B'}} />)}
      </div>
      <div style={{position: 'absolute', left: w * 0.16, top: h * 0.1, right: w * 0.05, bottom: h * 0.1, borderRadius: w * 0.02,
        background: screen ? 'linear-gradient(135deg, #3BA9F5 0%, #9B6BFF 50%, #FF8A5B 100%)' : 'rgba(255,255,255,0.03)',
        border: screen ? '3px solid rgba(255,255,255,0.35)' : `2px dashed rgba(255,255,255,0.18)`, overflow: 'hidden'}}>
        {children}
      </div>
    </div>
  );
};

export const Monitor: React.FC<{w?: number; children?: React.ReactNode}> = ({w = 520, children}) => {
  const h = w * 0.58;
  return (
    <div style={{position: 'relative', width: w, height: h + w * 0.16}}>
      <div style={{position: 'absolute', left: 0, top: 0, width: w, height: h, borderRadius: 18, background: '#0B0E14', border: '10px solid #2A2F38',
        boxShadow: '0 30px 60px rgba(0,0,0,0.5)', overflow: 'hidden', boxSizing: 'border-box'}}>
        <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(180deg, #F4F6FA 0%, #E3E8F0 100%)'}} />
        {children}
      </div>
      <div style={{position: 'absolute', left: w * 0.44, top: h, width: w * 0.12, height: w * 0.1, background: '#2A2F38'}} />
      <div style={{position: 'absolute', left: w * 0.3, top: h + w * 0.1, width: w * 0.4, height: w * 0.05, borderRadius: 10, background: '#3A404B'}} />
    </div>
  );
};

export const PenIcon: React.FC<{s?: number; rot?: number}> = ({s = 1, rot = -35}) => (
  <svg width={60 * s} height={300 * s} viewBox="0 0 60 300" style={{transform: `rotate(${rot}deg)`, transformOrigin: '50% 100%', overflow: 'visible', filter: 'drop-shadow(0 10px 14px rgba(0,0,0,0.5))'}}>
    <path d="M18 10 Q30 0 42 10 L44 230 L30 296 L16 230 Z" fill={PEN} stroke="#5B6575" strokeWidth={3} />
    <rect x={20} y={120} width={20} height={34} rx={6} fill="#3A404B" />
    <path d="M24 262 L30 296 L36 262 Z" fill="#C9D1DC" />
  </svg>
);

// Word tile (vector: blue tile with W, the product's own colours)
export const WordLogo: React.FC<{s?: number}> = ({s = 1}) => (
  <div style={{width: 170 * s, height: 170 * s, borderRadius: 34 * s, background: 'linear-gradient(160deg, #2B7CD3 0%, #185ABD 100%)', display: 'flex',
    alignItems: 'center', justifyContent: 'center', boxShadow: '0 20px 50px rgba(43,124,211,0.5)'}}>
    <span style={{fontFamily: EN, fontWeight: 900, fontSize: 110 * s, color: '#fff'}}>W</span>
  </div>
);

export const Word: React.FC<{text: string; size?: number; color?: string}> = ({text, size = 90, color = '#fff'}) => (
  <span style={{fontFamily: EN, fontWeight: 900, fontSize: size, letterSpacing: size * 0.12, color, textShadow: '0 8px 30px rgba(0,0,0,0.5)'}}>{text}</span>
);

// ---------- generic item renderer (positions = stage px, times = frames from the scene start) ----------
const Item: React.FC<{it: It}> = ({it}) => {
  const x = it.x ?? 540, y = it.y ?? 360;
  let body: React.ReactNode = null;
  switch (it.k) {
    case 'type': body = <Type text={it.text ?? ''} size={it.size ?? 72} width={it.w ?? 980} at={0} />; break;
    case 'pill': body = <Pill text={it.text ?? ''} size={it.size ?? 52} color={it.color ?? G.gold} ink={it.ink ?? '#14181F'} font={it.font === 'en' ? EN : AR} dir={it.dir ?? 'rtl'} />; break;
    case 'label': body = <Label text={it.text ?? ''} size={it.size ?? 44} color={it.color ?? G.ink} w={it.w} font={it.font === 'en' ? EN : AR} dir={it.dir ?? 'rtl'} />; break;
    case 'emoji': body = <span style={{fontSize: it.size ?? 140, filter: 'drop-shadow(0 12px 24px rgba(0,0,0,0.5))'}}>{it.text}</span>; break;
    case 'mark': body = <Mark ok={!!it.ok} s={(it.size ?? 76) / 76} />; break;
    case 'logo': body = <Img src={staticFile(it.src ?? '')} style={{width: it.size ?? 150, height: it.size ?? 150, objectFit: 'contain', filter: 'drop-shadow(0 12px 30px rgba(0,0,0,0.45))'}} />; break;
    case 'word': body = <WordLogo s={(it.size ?? 170) / 170} />; break;
    case 'brand': body = <Word text={it.text ?? ''} size={it.size ?? 90} color={it.color ?? '#fff'} />; break;
    case 'tablet': body = <Tablet w={it.size ?? 520} screen={!!it.ok} />; break;
    case 'monitor': body = <Monitor w={it.size ?? 520} />; break;
    case 'pen': body = <PenIcon s={(it.size ?? 300) / 300} />; break;
    case 'card': body = (
      <Glass w={it.w ?? 460} pad={22} r={34} glow={it.color}>
        <div style={{display: 'flex', alignItems: 'center', gap: 18, direction: 'rtl'}}>
          {it.src ? <span style={{fontSize: (it.size ?? 50) * 1.5}}>{it.src}</span> : null}
          <div>
            <div style={{fontFamily: AR, fontWeight: 900, fontSize: it.size ?? 50, color: it.color ?? G.ink, lineHeight: 1.2}}>{it.text}</div>
            {it.sub ? <div style={{fontFamily: EN, fontWeight: 700, fontSize: (it.size ?? 46) * 0.62, color: G.soft, direction: 'ltr', textAlign: 'right'}}>{it.sub}</div> : null}
          </div>
        </div>
      </Glass>
    ); break;
  }
  return <In at={it.at} out={it.out} x={x} y={y}>{body}</In>;
};

const Shade: React.FC<{h?: number; o?: number}> = ({h = 760, o = 0.85}) => (
  <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: h, background: `linear-gradient(180deg, rgba(5,8,14,${o}) 60%, transparent)`}} />
);

// free scene: only items (+ an optional top shade so text reads over his room)
export const TbFree: React.FC<{items?: It[]; shade?: boolean}> = ({items = [], shade = true}) => (
  <GScene>
    {shade ? <Shade /> : null}
    {items.map((it, i) => <Item key={i} it={it} />)}
  </GScene>
);

// ---------- his picture-in-picture insert (a clip he put in the top-left of his edit) shown BIG on the stage ----------
// cam = cam.mp4 (the short's own timeline), camAt = timeline frame of the scene start; crop = source rect of the insert.
export const TbClip: React.FC<{cam: string; camAt: number; crop?: number[]; items?: It[]; label?: string; y?: number}> = ({cam, camAt, crop = [66, 314, 806, 452], items = [], label, y = 380}) => {
  const [sx, sy, sw, sh] = crop;
  const W = 1000, H = Math.round((W * sh) / sw), sc = W / sw;
  return (
    <GScene>
      <Shade h={820} o={0.95} />
      <In at={0} x={540} y={y}>
        <Glass w={W + 24} h={H + 24} pad={12} r={38} glow={G.blue}>
          <div style={{position: 'relative', width: W, height: H, borderRadius: 28, overflow: 'hidden', background: '#000'}}>
            <OffthreadVideo muted src={staticFile(cam)} startFrom={camAt} style={{position: 'absolute', left: -sx * sc, top: -sy * sc, width: 1920 * sc, height: 1080 * sc}} />
          </div>
        </Glass>
      </In>
      {label ? <In at={6} x={540} y={y - H / 2 - 22}><Pill text={label} size={46} /></In> : null}
      {items.map((it, i) => <Item key={i} it={it} />)}
    </GScene>
  );
};

// ---------- short 6: "9 things that change the choice" grid; `need` = the ones he keeps (✓), the rest fade ----------
type Tile = {e: string; ar: string; en: string; at: number; need?: boolean};
export const TbCheck: React.FC<{tiles: Tile[]; decide?: number; title?: string; regret?: number}> = ({tiles, decide = 99999, title = 'قبل ما تشتري *تابلت* شوف', regret = 99999}) => {
  const f = useCurrentFrame();
  const cw = 336, ch = 190, gap = 14;
  return (
    <GScene>
      <Shade h={840} o={0.9} />
      <div style={{position: 'absolute', top: 40, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Type text={f < decide ? title : 'خلي *اللي_محتاجه* بس'} at={f < decide ? 2 : decide} size={60} /></div>
      <div style={{position: 'absolute', top: 150, left: (1080 - 3 * cw - 2 * gap) / 2, width: 3 * cw + 2 * gap, display: 'flex', flexWrap: 'wrap', gap, direction: 'rtl'}}>
        {tiles.map((t, i) => {
          if (f < t.at) return <div key={i} style={{width: cw, height: ch}} />;
          const p = spr(f, 30, t.at, 170, 15);
          const lit = f < t.at + 24; // glow while he is saying it
          const dec = lin(f, decide, decide + 10);
          const keep = !!t.need;
          return (
            <div key={i} style={{width: cw, height: ch, borderRadius: 30, boxSizing: 'border-box', padding: '14px 16px', position: 'relative',
              background: keep && dec > 0 ? `rgba(245,184,61,${0.16 + 0.1 * dec})` : 'rgba(255,255,255,0.09)', backdropFilter: 'blur(20px)',
              border: `2px solid ${lit || (keep && dec > 0) ? G.gold : 'rgba(255,255,255,0.18)'}`, boxShadow: lit ? `0 0 40px ${G.gold}77` : '0 20px 40px rgba(0,0,0,0.35)',
              opacity: Math.min(1, p * 1.3) * (keep ? 1 : 1 - 0.65 * dec), transform: `scale(${0.85 + 0.15 * p})`,
              display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 4}}>
              <span style={{fontSize: 60, lineHeight: 1}}>{t.e}</span>
              <span style={{fontFamily: AR, fontWeight: 900, fontSize: 40, color: G.ink, textAlign: 'center', lineHeight: 1.15}}>{t.ar}</span>
              <span style={{fontFamily: EN, fontWeight: 700, fontSize: 24, color: G.soft}}>{t.en}</span>
              {keep && dec > 0 ? <div style={{position: 'absolute', top: -14, left: -14, transform: `scale(${spr(f, 30, decide + i * 2, 200, 12)})`}}><Mark ok s={0.6} /></div> : null}
            </div>
          );
        })}
      </div>
      {f >= decide ? <In at={decide + 6} x={120} y={110}><Pill text="مثال" color="rgba(255,255,255,0.92)" size={34} /></In> : null}
      {f >= regret ? <In at={regret} x={540} y={790}><Pill text="عشان متندمش بعد ما تشتريه 😩" color={G.red} ink="#fff" size={44} /></In> : null}
    </GScene>
  );
};

// ---------- short 3: the computer screen lives INSIDE the tablet's rectangle (pen here -> cursor there) ----------
export const TbMap: React.FC<{strokes?: number[]; mouse?: number; sense?: number}> = ({strokes = [], mouse = 99999, sense = 99999}) => {
  const f = useCurrentFrame();
  // one zigzag path in 0..1 coords, drawn piece by piece on his "كده … كده"
  const P = [[0.12, 0.7], [0.3, 0.25], [0.48, 0.72], [0.66, 0.28], [0.86, 0.66], [0.9, 0.3]];
  const n = P.length - 1;
  let prog = 0;
  strokes.forEach((t, i) => { prog = Math.max(prog, i + lin(f, t, t + 10)); });
  prog = Math.min(n, prog);
  const pts = (W: number, H: number) => {
    const out: number[][] = [];
    for (let i = 0; i <= Math.floor(prog); i++) out.push([P[i][0] * W, P[i][1] * H]);
    const k = prog - Math.floor(prog), i = Math.floor(prog);
    if (k > 0 && i < n) out.push([(P[i][0] + (P[i + 1][0] - P[i][0]) * k) * W, (P[i][1] + (P[i + 1][1] - P[i][1]) * k) * H]);
    return out;
  };
  const tip = (W: number, H: number) => { const p = pts(W, H); return p[p.length - 1]; };
  const MW = 470, MH = MW * 0.58 - 20, TW = 520 * 0.79 - 0, TH = 520 * 0.62 * 0.8;
  const line = (W: number, H: number, c: string) => (
    <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
      <polyline points={pts(W, H).map((p) => p.join(',')).join(' ')} fill="none" stroke={c} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
  const [tx, ty] = tip(TW, TH), [mx, my] = tip(MW - 20, MH);
  const glow = 0.5 + 0.5 * Math.sin(f / 8);
  return (
    <GScene>
      <Shade h={840} o={0.9} />
      <div style={{position: 'absolute', top: 30, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Type text="الشاشة *جوه* المستطيل ده" at={2} size={60} /></div>
      {/* monitor right, tablet left; dashed lines from the tablet's area to the screen corners */}
      <div style={{position: 'absolute', left: 560, top: 150}}>
        <Monitor w={MW}><div style={{position: 'absolute', left: 0, top: 0, width: MW - 20, height: MH}}>{line(MW - 20, MH, G.royal)}{prog > 0 ? <Cursor x={mx} y={my} s={0.55} /> : null}</div></Monitor>
      </div>
      <div style={{position: 'absolute', left: 40, top: 300}}>
        <Tablet w={520} glow={glow * 0.6}>
          <div style={{position: 'absolute', inset: 0}}>{line(TW, TH, G.gold)}</div>
        </Tablet>
        {prog > 0 ? <div style={{position: 'absolute', left: 520 * 0.16 + tx - 4, top: 520 * 0.062 + ty - 300 * 0.62 * 1.0}}><PenIcon s={0.62} rot={-28} /></div> : null}
      </div>
      <svg width={1080} height={760} style={{position: 'absolute', left: 0, top: 0, pointerEvents: 'none'}}>
        {[[123, 332, 572, 162], [500, 332, 1018, 162], [123, 590, 572, 412], [500, 590, 1018, 412]].map(([a, b, c, d], i) => (
          <line key={i} x1={a} y1={b} x2={c} y2={d} stroke={G.blue} strokeWidth={3} strokeDasharray="10 10" opacity={0.55 * lin(f, 14, 30)} />
        ))}
      </svg>
      {f >= mouse ? <In at={mouse} x={800} y={640}><Pill text="🖱️ زي فكرة الماوس" color={G.blue} ink="#fff" size={42} /></In> : null}
      {f >= sense ? <In at={sense} x={540} y={712}><Pill text="مرة واحدة وتاخد على الإحساس ✓" color={G.green} ink="#fff" size={42} /></In> : null}
    </GScene>
  );
};

// ---------- short 3: two kinds side by side ----------
export const TbTypes: React.FC<{a?: number; b?: number; cheap?: number; focus?: string}> = ({a = 0, b = 99999, cheap = 99999}) => {
  const f = useCurrentFrame();
  const card = (t: number, screen: boolean, en: string, ar: string, x: number, dim: boolean) => (
    <In at={t} x={x} y={400}>
      <div style={{opacity: dim ? 0.45 : 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 18}}>
        <Tablet w={430} screen={screen} />
        <Pill text={ar} size={42} color={screen ? G.blue : G.gold} ink={screen ? '#fff' : '#14181F'} />
        <span style={{fontFamily: EN, fontWeight: 800, fontSize: 30, color: G.soft}}>{en}</span>
      </div>
    </In>
  );
  return (
    <GScene>
      <Shade h={840} o={0.9} />
      <div style={{position: 'absolute', top: 40, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}><Type text="فيه *نوعين* أساسيين" at={2} size={64} /></div>
      {card(a, true, 'Pen Display', 'بشاشة 🖥️', 780, f >= b && f < cheap)}
      {card(b, false, 'Pen Tablet', 'من غير شاشة', 300, false)}
      {f >= cheap ? <In at={cheap} x={300} y={150}><Pill text="أرخص بكتير 💰" color={G.green} ink="#fff" size={44} /></In> : null}
    </GScene>
  );
};

// ---------- short 5: keyboard (code you type) vs pen (you just write it) ----------
export const TbMath: React.FC<{kb?: number; pen?: number; free?: number}> = ({kb = 0, pen = 99999, free = 99999}) => {
  const f = useCurrentFrame();
  const code = 'x_k=\\frac{1}{N}\\sum_{n=0}^{N-1}x_n e^{-i2\\pi kn/N}';
  const n = Math.max(0, Math.min(code.length, Math.floor((f - kb - 6) * 1.6)));
  const w = lin(f, pen + 4, pen + 40);
  return (
    <GScene>
      <Shade h={840} o={0.9} />
      <In at={kb} x={540} y={170}>
        <Glass w={980} pad={24} r={32} glow={G.red}>
          <div style={{display: 'flex', alignItems: 'center', gap: 18, direction: 'rtl', marginBottom: 10}}>
            <span style={{fontSize: 48}}>⌨️</span><Label text="بالكيبورد" size={40} /><div style={{flex: 1}} />{f > kb + 40 ? <Mark ok={false} s={0.7} /> : null}
          </div>
          <div style={{fontFamily: MONO, fontSize: 34, color: '#FFB4B4', direction: 'ltr', wordBreak: 'break-all', lineHeight: 1.3, minHeight: 90}}>{code.slice(0, n)}<span style={{opacity: f % 20 < 10 ? 1 : 0}}>▍</span></div>
        </Glass>
      </In>
      {f >= pen ? (
        <In at={pen} x={540} y={470}>
          <Glass w={980} pad={24} r={32} glow={G.green}>
            <div style={{display: 'flex', alignItems: 'center', gap: 18, direction: 'rtl', marginBottom: 6}}>
              <span style={{fontSize: 48}}>🖊️</span><Label text="بالقلم" size={40} /><div style={{flex: 1}} />{w > 0.95 ? <Mark ok s={0.7} /> : null}
            </div>
            <div style={{position: 'relative', height: 150, direction: 'ltr', display: 'flex', alignItems: 'center', justifyContent: 'center', clipPath: `inset(0 ${(1 - w) * 100}% 0 0)`}}>
              <span style={{fontFamily: 'Cambria Math, "Times New Roman", serif', fontStyle: 'italic', fontSize: 74, color: '#fff'}}>
                x<sub style={{fontSize: 40}}>k</sub> = <span style={{display: 'inline-flex', flexDirection: 'column', alignItems: 'center', verticalAlign: 'middle', fontSize: 44, lineHeight: 1}}><span>1</span><span style={{borderTop: '3px solid #fff', width: 40}}>N</span></span>
                {' '}<span style={{display: 'inline-flex', flexDirection: 'column', alignItems: 'center', verticalAlign: 'middle', lineHeight: 0.9}}><span style={{fontSize: 26}}>N−1</span><span style={{fontSize: 90, fontStyle: 'normal'}}>Σ</span><span style={{fontSize: 26}}>n=0</span></span>
                {' '}x<sub style={{fontSize: 40}}>n</sub> e<sup style={{fontSize: 36}}>−i2πkn/N</sup>
              </span>
            </div>
          </Glass>
        </In>
      ) : null}
      {f >= free ? <In at={free} x={540} y={700}><Pill text="حرية مش طبيعية ✨" size={48} /></In> : null}
    </GScene>
  );
};

// ---------- short 2: the big whiteboard he studied on (scribbles write themselves) + the story turned into a map ----------
export const TbBoard: React.FC<{lines?: number; map?: number; pins?: number[]; items?: It[]}> = ({lines = 0, map = 99999, pins = [], items = []}) => {
  const f = useCurrentFrame();
  const L = [[60, 70, 380], [60, 130, 300], [60, 190, 420], [60, 250, 260], [520, 70, 300], [520, 130, 380], [520, 190, 240]];
  const isMap = f >= map;
  const PINS = [[180, 110, '🏠'], [470, 70, '🏫'], [720, 130, '⛵'], [330, 230, '🌳'], [640, 245, '🏰']] as const;
  return (
    <GScene>
      <Shade h={840} o={0.9} />
      <In at={0} x={540} y={340}>
        <div style={{width: 960, height: 360, borderRadius: 18, background: '#F7F8FA', border: '16px solid #C8102E', boxShadow: '0 30px 70px rgba(0,0,0,0.55)', position: 'relative', overflow: 'hidden'}}>
          <svg width={928} height={328} style={{position: 'absolute', left: 0, top: 0}}>
            {!isMap ? L.map(([x, y, w], i) => {
              const t = lines + i * 6, k = lin(f, t, t + 14);
              let d = `M${x} ${y}`;
              for (let s = 0; s < 14; s++) d += ` q ${w / 28} ${s % 2 ? 14 : -14} ${w / 14} 0`;
              return <path key={i} d={d} fill="none" stroke={i % 3 === 2 ? '#C8102E' : '#1F4E9F'} strokeWidth={6} strokeLinecap="round" strokeDasharray={w * 1.6} strokeDashoffset={w * 1.6 * (1 - k)} />;
            }) : (
              <>
                {PINS.slice(1).map((p, i) => {
                  const a = PINS[i], t = (pins[i + 1] ?? map + 10 * (i + 1));
                  const k = lin(f, t, t + 14);
                  return <line key={i} x1={a[0]} y1={a[1]} x2={a[0] + (p[0] - a[0]) * k} y2={a[1] + (p[1] - a[1]) * k} stroke="#1F4E9F" strokeWidth={6} strokeDasharray="14 12" strokeLinecap="round" />;
                })}
              </>
            )}
          </svg>
          {isMap ? PINS.map((p, i) => {
            const t = pins[i] ?? map + 10 * i;
            if (f < t) return null;
            const s = spr(f, 30, t, 220, 12);
            return <div key={i} style={{position: 'absolute', left: p[0] - 40, top: p[1] - 50, fontSize: 70, transform: `scale(${s})`}}>{p[2]}</div>;
          }) : null}
        </div>
      </In>
      <In at={4} x={540} y={100}><Pill text={isMap ? 'القصة بقت خريطة 🗺️' : 'السبورة = مكان المذاكرة 🧑‍🏫'} size={46} /></In>
      {items.map((it, i) => <Item key={i} it={it} />)}
    </GScene>
  );
};

// ---------- end: QR of the full video (style 11's CTA idea, without a face clip) ----------
export const TbEnd: React.FC<{qr: string; title?: string; at?: number}> = ({qr, title = 'الفيديو كامل على القناة', at = 0}) => {
  return (
    <GScene>
      <div style={{position: 'absolute', inset: 0, background: 'rgba(5,8,14,0.55)'}} />
      <In at={at} x={540} y={560}><Type text={title.replace('كامل', '*كامل*')} size={70} /></In>
      <In at={at + 6} x={540} y={930}>
        <div style={{background: '#fff', borderRadius: 34, padding: 20, border: `6px solid ${G.gold}`, boxShadow: `0 0 60px ${G.gold}66`, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8}}>
          <Img src={staticFile(qr)} style={{width: 420, height: 420, display: 'block'}} />
          <div style={{fontFamily: AR, fontWeight: 900, fontSize: 42, color: '#14181F'}}>امسح وشوفه 📲</div>
        </div>
      </In>
    </GScene>
  );
};

// rewind flash after the hook (⏪ + streaks)
export const TbRewind: React.FC = () => {
  const f = useCurrentFrame();
  const {durationInFrames: d} = useVideoConfig();
  const o = Math.min(lin(f, 0, 4), 1 - lin(f, d - 5, d));
  return (
    <div style={{position: 'absolute', inset: 0, opacity: o, pointerEvents: 'none'}}>
      {Array.from({length: 9}).map((_, i) => (
        <div key={i} style={{position: 'absolute', left: ((i * 137 + f * 90) % 1400) - 200, top: 120 + i * 190, width: 340, height: 6, borderRadius: 3, background: 'rgba(255,255,255,0.35)'}} />
      ))}
      <div style={{position: 'absolute', left: 0, right: 0, top: 330, display: 'flex', justifyContent: 'center'}}><Pill text="⏪ نرجع للأول" color="rgba(255,255,255,0.92)" size={58} /></div>
    </div>
  );
};

export const tabletScenes: Record<string, React.FC<any>> = {
  tb_free: TbFree, tb_clip: TbClip, tb_check: TbCheck, tb_map: TbMap, tb_types: TbTypes, tb_math: TbMath, tb_board: TbBoard, tb_end: TbEnd, tb_rewind: TbRewind,
};
