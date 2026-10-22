import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {Easing} from 'remotion';
import {VectorHeart3D, VoxelHeart} from './three';
import {AR, EN, FlatGuy, GFrame, grad, HuwaLogo, In, JY, lin, Logo, Pill, Sc, spr, Type} from './kit';

// Short "هو ايه | vectors" (ep 08). Props: b = {beat: scene frame}. One heart runs through the whole short:
// pixel heart (raster) → breaks when scaled → the same heart drawn with lines & curves (vector) → crisp at any size.
const C = JY.huwa;
type B = Record<string, number>;
const at = (b: B, k: string, d = 0) => b[k] ?? d;

// implicit heart: inside when (x²+y²-1)³ - x²y³ <= 0  (x,y in -1.3..1.3, y up)
const inHeart = (x: number, y: number) => (x * x + y * y - 1) ** 3 - x * x * y ** 3 <= 0;
const heartCol = (u: number) => {
  const a = [0xE8, 0x17, 0x5D], b = [0xF7, 0x93, 0x1E];
  return `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * u)).join(',')})`;
};

// pixel heart: n×n grid, cells appear in a sweep from `t0`; `px` = cell size
export const PixelHeart: React.FC<{n?: number; px: number; t0?: number; speed?: number; gap?: number; grid?: boolean}> = ({n = 14, px, t0 = 0, speed = 3, gap = 2, grid = true}) => {
  const f = useCurrentFrame();
  const cells: React.ReactNode[] = [];
  for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) {
    const x = ((c + 0.5) / n) * 2.6 - 1.3, y = 1.25 - ((r + 0.5) / n) * 2.6;
    const on = inHeart(x, y);
    const k = r + c;
    const show = f >= t0 + k * (1 / speed) * 2;
    cells.push(<rect key={r * n + c} x={c * px + gap / 2} y={r * px + gap / 2} width={px - gap} height={px - gap}
      fill={show ? (on ? heartCol(c / n) : '#F2F2F4') : 'transparent'} stroke={grid && show ? 'rgba(0,0,0,0.06)' : 'none'} />);
  }
  return <svg width={n * px} height={n * px}>{cells}</svg>;
};

// the heart as a vector path (two cubic curves meeting at the bottom point)
const HEART = 'M 100 178 C 30 128 0 92 0 56 C 0 22 26 0 56 0 C 76 0 92 12 100 30 C 108 12 124 0 144 0 C 174 0 200 22 200 56 C 200 92 170 128 100 178 Z';

// 1) raster recap: the pixel heart builds in a gradient frame, "Raster = بيكسلز" + monitor
export const V8Raster: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  return (
    <Sc>
      <In at={0} x={540} y={820} from={0.6}>
        <GFrame w={720} h={720}><VoxelHeart w={700} h={700} t0={2} /></GFrame>
      </In>
      <In at={at(b, 'sq', 30)} x={540} y={350}><Pill text="الصورة = مربعات صغيرة 🟥🟧" size={48} /></In>
      <In at={at(b, 'col', 60)} x={790} y={1260} rot={-4}><Pill text="كل مربع ليه لونه" bg={grad('huwa')} ink="#fff" size={42} /></In>
      <In at={at(b, 'show', 120)} x={290} y={1260} rot={4}><Pill text="Raster  =  Pixels" font={EN} dir="ltr" size={40} /></In>
      <div style={{position: 'absolute', left: 540 - 40, top: 820 - 40, width: 80, height: 80, borderRadius: '50%', border: '6px solid #fff',
        opacity: f > at(b, 'col', 60) && f < at(b, 'col', 60) + 40 ? 1 : 0, transform: `scale(${1 + 0.3 * Math.sin(f / 3)})`}} />
    </Sc>
  );
};

// 2) scaling it up breaks it (blocks), red ✗ "هتبوظ"
export const V8Scale: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const bad = at(b, 'bad', 70);
  const z = lin(f, 6, bad, 0, 0.82, Easing.inOut(Easing.cubic));
  const shake = f > bad ? Math.sin(f * 2.2) * 6 * Math.max(0, 1 - (f - bad) / 12) : 0;
  return (
    <Sc>
      <In at={0} x={540} y={330}><Pill text="كبّر الصورة.. 🔍" size={52} /></In>
      <div style={{position: 'absolute', left: 540, top: 860, transform: `translate(-50%,-50%) translateX(${shake}px)`}}>
        <GFrame w={760} h={760}><VoxelHeart w={740} h={740} t0={-999} zoom={z} spin={false} gap={0.04} /></GFrame>
      </div>
      <In at={bad} x={540} y={860} from={2}><div style={{fontSize: 330, lineHeight: 1, color: '#E53935', fontFamily: EN, fontWeight: 900, textShadow: '0 10px 30px rgba(0,0,0,0.3)'}}>✕</div></In>
      <In at={bad + 6} x={540} y={1330}><Pill text="مربعات.. هتبوظ 😬" bg="#E53935" ink="#fff" size={58} /></In>
    </Sc>
  );
};

// 3) bigger = the computer ADDS pixels it guesses, smaller = it REMOVES pixels
export const V8AddRemove: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const add = at(b, 'add', 10), rm = at(b, 'rm', 90);
  const cell = 70;
  const small = [[0, 1, 1, 0], [1, 1, 1, 1], [1, 1, 1, 1], [0, 1, 1, 0]];
  const grid = (n: number, x0: number, y0: number, mode: 'add' | 'rm', t: number) => {
    const out: React.ReactNode[] = [];
    for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) {
      const orig = mode === 'add' ? (r % 2 === 0 && c % 2 === 0) : true;
      const src = small[Math.min(3, Math.floor((r / n) * 4))][Math.min(3, Math.floor((c / n) * 4))];
      const k = (r * n + c) % 7;
      const appear = orig ? 1 : lin(f, t + 8 + k * 3, t + 14 + k * 3);
      const gone = mode === 'rm' && (r % 2 === 1 || c % 2 === 1) ? lin(f, t + 8 + k * 3, t + 14 + k * 3) : 0;
      const col = src ? heartCol(c / n) : '#EDEDF0';
      out.push(
        <g key={r * n + c} opacity={appear * (1 - gone)}>
          <rect x={x0 + c * cell} y={y0 + r * cell} width={cell - 4} height={cell - 4} rx={6} fill={col} />
          {!orig && appear > 0 ? <text x={x0 + c * cell + cell / 2 - 2} y={y0 + r * cell + cell / 2 + 12} textAnchor="middle" fontSize={34} fontFamily={EN} fontWeight={900} fill="#fff" opacity={1 - lin(f, t + 30, t + 50)}>?</text> : null}
          {gone > 0 ? <text x={x0 + c * cell + cell / 2 - 2} y={y0 + r * cell + cell / 2 + 12} textAnchor="middle" fontSize={34} fontFamily={EN} fontWeight={900} fill="#E53935" opacity={gone * (1 - gone)}>−</text> : null}
        </g>);
    }
    return out;
  };
  const showRm = f >= rm;
  return (
    <Sc>
      <In at={0} x={540} y={330}><Pill text={showRm ? 'صغّر = هيشيل بيكسلز ➖' : 'كبّر = هيزوّد بيكسلز من عنده ➕'} bg={showRm ? '#E53935' : '#2DBE60'} ink="#fff" size={48} /></In>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        {showRm ? grid(8, 540 - 4 * cell, 560, 'rm', rm) : grid(8, 540 - 4 * cell, 560, 'add', add)}
      </svg>
      <In at={showRm ? rm + 40 : add + 40} x={540} y={1250}><Pill text={showRm ? 'التفاصيل بتضيع' : 'ألوان متخمّنة ❓'} size={44} /></In>
    </Sc>
  );
};

// 4) bigger cameras + stronger computers → huge files, "مش عملي"
export const V8Heavy: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const mp = Math.round(12 + 88 * lin(f, 6, at(b, 'pc', 40)));
  const size = lin(f, at(b, 'file', 70), at(b, 'file', 70) + 50);
  return (
    <Sc>
      <In at={0} x={300} y={560}>
        <div style={{width: 360, height: 250, background: '#2C2C34', borderRadius: 40, position: 'relative', boxShadow: '0 20px 40px rgba(0,0,0,0.3)'}}>
          <div style={{position: 'absolute', left: 105, top: 50, width: 150, height: 150, borderRadius: '50%', background: '#111', border: '14px solid #555'}} />
          <div style={{position: 'absolute', left: 30, top: -30, width: 90, height: 40, background: '#2C2C34', borderRadius: 10}} />
          <div style={{position: 'absolute', right: 20, top: 16, fontFamily: EN, fontWeight: 900, fontSize: 34, color: C.b}}>{mp}MP</div>
        </div>
      </In>
      <In at={at(b, 'pc', 40)} x={780} y={560}>
        <div style={{width: 300, height: 340, background: '#2C2C34', borderRadius: 24, position: 'relative', boxShadow: '0 20px 40px rgba(0,0,0,0.3)'}}>
          {[0, 1, 2].map((i) => <div key={i} style={{position: 'absolute', left: 30, top: 40 + i * 50, width: 240, height: 24, borderRadius: 6, background: '#44444E'}} />)}
          <div style={{position: 'absolute', left: 30, bottom: 40, width: 240, height: 70, borderRadius: 12, background: `linear-gradient(90deg, ${C.a}, ${C.b})`, opacity: 0.5 + 0.5 * Math.abs(Math.sin(f / 4))}} />
          <div style={{position: 'absolute', top: -60, width: '100%', textAlign: 'center', fontSize: 60}}>💪</div>
        </div>
      </In>
      <In at={at(b, 'file', 70)} x={540} y={1020}>
        <div style={{width: 860, background: '#fff', borderRadius: 30, padding: 30, boxShadow: '0 20px 40px rgba(0,0,0,0.2)', direction: 'rtl'}}>
          <div style={{fontFamily: AR, fontWeight: 900, fontSize: 44, color: C.ink}}>حجم الملف 📁</div>
          <div style={{height: 60, marginTop: 18, borderRadius: 30, background: '#EEE', overflow: 'hidden'}}>
            <div style={{width: `${8 + 92 * size}%`, height: '100%', background: size > 0.7 ? '#E53935' : C.b, borderRadius: 30}} />
          </div>
        </div>
      </In>
      <In at={at(b, 'bad', 100)} x={540} y={1300} rot={-3}><Pill text="بس ده مش عملي قوي" bg="#E53935" ink="#fff" size={54} /></In>
    </Sc>
  );
};

// 5) ads you blow up huge + logos used everywhere (same logo: card → t-shirt → billboard)
export const V8Sizes: React.FC<{b?: B}> = ({b = {}}) => {
  const lg = at(b, 'logo', 40);
  const heart = (w: number) => <svg width={w} height={w * 0.9} viewBox="0 0 200 180"><path d={HEART} fill="url(#hg)" /><defs><linearGradient id="hg"><stop offset="0" stopColor={C.a} /><stop offset="1" stopColor={C.b} /></linearGradient></defs></svg>;
  return (
    <Sc>
      <In at={0} x={540} y={560}>
        <div style={{width: 900, height: 420, background: '#fff', border: '14px solid #2C2C34', borderRadius: 10, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 40, position: 'relative'}}>
          {heart(240)}
          <div style={{fontFamily: AR, fontWeight: 900, fontSize: 70, color: C.ink}}>إعلان ضخم</div>
          <div style={{position: 'absolute', bottom: -170, left: 200, width: 24, height: 160, background: '#2C2C34'}} />
          <div style={{position: 'absolute', bottom: -170, right: 200, width: 24, height: 160, background: '#2C2C34'}} />
        </div>
      </In>
      <In at={lg} x={230} y={1180} rot={-6}><div style={{width: 280, height: 170, background: '#fff', borderRadius: 16, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 14px 30px rgba(0,0,0,0.25)'}}>{heart(80)}</div><div style={{textAlign: 'center', fontFamily: AR, fontWeight: 800, fontSize: 32, marginTop: 8}}>كارت</div></In>
      <In at={lg + 8} x={540} y={1190}>
        <svg width={260} height={230} viewBox="0 0 260 230"><path d="M70 10 L20 40 L0 100 L50 110 L50 230 L210 230 L210 110 L260 100 L240 40 L190 10 Q130 50 70 10 Z" fill="#2C2C34" /></svg>
        <div style={{position: 'absolute', left: 95, top: 80}}>{heart(70)}</div>
        <div style={{textAlign: 'center', fontFamily: AR, fontWeight: 800, fontSize: 32}}>تيشيرت</div>
      </In>
      <In at={lg + 16} x={850} y={1180} rot={6}><div style={{width: 120, height: 220, background: '#fff', borderRadius: 20, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 14px 30px rgba(0,0,0,0.25)'}}>{heart(50)}</div><div style={{textAlign: 'center', fontFamily: AR, fontWeight: 800, fontSize: 32, marginTop: 8}}>قلم</div></In>
      <In at={lg + 24} x={540} y={330}><Pill text="نفس اللوجو.. مقاسات مختلفة" bg={grad('huwa')} ink="#fff" size={46} /></In>
    </Sc>
  );
};

// 6) "the alternative": telling the computer pixel by pixel (a list that never ends) vs lines & shapes (pen tool draws the heart)
export const V8Alt: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const list = at(b, 'list', 40), shapes = at(b, 'shapes', 160);
  const lines = Array.from({length: 40}, (_, i) => `بيكسل ${(i * 7919 + 1).toLocaleString('en')}: (${(i * 37) % 1920}, ${(i * 53) % 1080}) لونه ${['🟥', '🟧', '🟨', '⬜'][i % 4]}`);
  const scroll = Math.max(0, f - list) * 9;
  return (
    <Sc>
      <In at={0} x={540} y={330}><div style={{fontFamily: AR, fontWeight: 900, fontSize: 96, color: C.ink}}>البديل <span style={{background: grad('huwa'), WebkitBackgroundClip: 'text', color: 'transparent'}}>؟</span></div></In>
      {f >= list && f < shapes ? (
        <>
          <FlatGuy x={250} y={1260} s={1.6} pose="point" talk />
          <div style={{position: 'absolute', left: 430, top: 560, width: 600, height: 620, background: '#1E1E24', borderRadius: 30, overflow: 'hidden', boxShadow: '0 20px 40px rgba(0,0,0,0.3)',
            transform: `scale(${spr(f, fps, list)})`}}>
            <div style={{transform: `translateY(${-scroll}px)`, padding: 24, direction: 'rtl'}}>
              {lines.map((l, i) => <div key={i} style={{fontFamily: AR, fontWeight: 700, fontSize: 32, color: '#E9E9EE', lineHeight: 1.6, whiteSpace: 'nowrap'}}>{l}</div>)}
            </div>
          </div>
          <In at={list + 50} x={730} y={1280}><Pill text="بيكسلاية بيكسلاية 😮‍💨" size={42} /></In>
        </>
      ) : null}
    </Sc>
  );
};

// 7) "lines & shapes": the pen draws the heart (anchors + handles), then "a line here", "a triangle here", their colours,
//    and the computer renders it (Aly ep 08: "يقوله عندك خط هنا ومثلث هنا وهم ألوانهم ايه وهو هيرندر")
export const V8Pen: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const ln = at(b, 'line', 70), tri = at(b, 'tri', 85), col = at(b, 'color', 110), rd = at(b, 'render', 140);
  const draw = lin(f, 4, ln - 6);
  const lineP = lin(f, ln, ln + 10), triP = lin(f, tri, tri + 14);
  const fill = lin(f, col, col + 14);
  const render = lin(f, rd, rd + 18);
  const pts = [[100, 178], [0, 56], [56, 0], [100, 30], [144, 0], [200, 56]];
  const s = 2.6, ox = 540 - 100 * s, oy = 520;
  const pen = draw < 1 ? pts[Math.min(pts.length - 1, Math.floor(draw * pts.length))] : null;
  const handles = render < 0.5;
  const anchor = (x: number, y: number, k: number) => <rect key={k} x={x - 9} y={y - 9} width={18} height={18} fill="#fff" stroke="#2D7FF9" strokeWidth={3} />;
  return (
    <Sc>
      <In at={0} x={540} y={330}><Pill text="بالخطوط والأشكال ✏️" bg={grad('huwa')} ink="#fff" size={52} /></In>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <defs><linearGradient id="pg"><stop offset="0" stopColor={C.a} /><stop offset="1" stopColor={C.b} /></linearGradient></defs>
        <g transform={`translate(${ox} ${oy}) scale(${s})`} opacity={1 - render}>
          <path d={HEART} fill="url(#pg)" opacity={fill} />
          <path d={HEART} fill="none" stroke={handles ? '#1E1E24' : 'transparent'} strokeWidth={1.6} pathLength={1} strokeDasharray={`${draw} 1`} />
          {handles ? pts.map(([x, y], i) => <rect key={i} x={x - 3.5} y={y - 3.5} width={7} height={7} fill="#fff" stroke="#2D7FF9" strokeWidth={1.2} opacity={draw * pts.length > i ? 1 : 0} />) : null}
          {handles && draw > 0.3 ? <g opacity={lin(f, 20, 30)}><line x1={0} y1={22} x2={0} y2={92} stroke="#2D7FF9" strokeWidth={1} /><circle cx={0} cy={22} r={3.4} fill="#2D7FF9" /><circle cx={0} cy={92} r={3.4} fill="#2D7FF9" /></g> : null}
        </g>
        {/* a line here */}
        <line x1={150} y1={1130} x2={150 + 300 * lineP} y2={1130 - 120 * lineP} stroke={fill > 0 ? '#2D7FF9' : '#1E1E24'} strokeWidth={14} strokeLinecap="round" />
        {handles && lineP > 0 ? [anchor(150, 1130, 1), anchor(150 + 300 * lineP, 1130 - 120 * lineP, 2)] : null}
        {/* a triangle here */}
        <polygon points="760,1000 900,1170 620,1170" fill={fill > 0 ? '#2DBE60' : 'none'} fillOpacity={fill} stroke="#1E1E24" strokeWidth={8} strokeLinejoin="round"
          pathLength={1} strokeDasharray={`${triP} 1`} opacity={triP > 0 ? 1 : 0} />
        {handles && triP > 0.9 ? [anchor(760, 1000, 3), anchor(900, 1170, 4), anchor(620, 1170, 5)] : null}
        {pen ? <text x={ox + pen[0] * s + 10} y={oy + pen[1] * s} fontSize={70}>🖊️</text> : null}
        {/* colour swatches */}
        {[C.a, '#2D7FF9', '#2DBE60'].map((c, i) => <circle key={i} cx={430 + i * 110} cy={1300} r={36 * spr(f, 30, col + i * 3)} fill={c} stroke="#fff" strokeWidth={6} />)}
      </svg>
      <In at={ln} out={tri} x={300} y={1240}><Pill text="خط هنا" size={44} /></In>
      <In at={tri} out={col} x={760} y={1260}><Pill text="ومثلث هنا 🔺" size={44} /></In>
      <In at={col} out={rd} x={540} y={1420}><Pill text="وألوانهم ايه 🎨" size={44} /></In>
      <In at={rd} x={540} y={1420}><Pill text="والكمبيوتر يرسمها (Render)" bg="#1E1E24" ink="#fff" size={44} /></In>
      {f >= rd ? <div style={{position: 'absolute', left: 90, top: 380, opacity: render}}><VectorHeart3D w={900} h={820} t0={rd} scale={1.05} /></div> : null}
    </Sc>
  );
};

// 8) file size: raster vs vector (same heart), label "مثال"
export const V8FileSize: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const g = lin(f, 10, 40);
  const row = (name: string, ext: string, pct: number, col: string, y: number, d: number) => (
    <In at={d} x={540} y={y}>
      <div style={{width: 900, direction: 'ltr', display: 'flex', alignItems: 'center', gap: 24}}>
        <div style={{width: 190, height: 230, background: '#fff', borderRadius: 18, position: 'relative', boxShadow: '0 14px 30px rgba(0,0,0,0.2)', display: 'flex', alignItems: 'flex-end', justifyContent: 'center', paddingBottom: 20}}>
          <span style={{fontFamily: EN, fontWeight: 900, fontSize: 40, color: col}}>{ext}</span>
          <div style={{position: 'absolute', left: 40, top: 30}}>{name === 'r' ? <PixelHeart px={8} n={14} t0={-999} gap={1} grid={false} /> : <svg width={110} height={100} viewBox="0 0 200 180"><path d={HEART} fill={C.a} /></svg>}</div>
        </div>
        <div style={{flex: 1, height: 70, borderRadius: 35, background: 'rgba(255,255,255,0.6)', overflow: 'hidden'}}>
          <div style={{width: `${pct * g}%`, height: '100%', background: col, borderRadius: 35}} />
        </div>
      </div>
    </In>
  );
  return (
    <Sc>
      <In at={0} x={540} y={330}><Pill text="مساحة الفايل أصغر كتير 📉" size={50} /></In>
      {row('r', '.PNG', 92, '#7A7A85', 640, 4)}
      {row('v', '.SVG', 9, C.a, 960, 12)}
      <In at={30} x={880} y={1180} rot={-5}><Pill text="مثال" bg="#1E1E24" ink="#fff" size={36} /></In>
    </Sc>
  );
};

// 9) but raster keeps the DETAILS (photos): a detailed drawn landscape photo ✓
export const V8Photo: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const z = 1 + 0.35 * lin(f, at(b, 'det', 40), at(b, 'det', 40) + 50);
  const trees = Array.from({length: 46}, (_, i) => ({x: (i * 97) % 700, y: 430 + ((i * 53) % 150), s: 0.6 + ((i * 31) % 10) / 14}));
  return (
    <Sc>
      <In at={0} x={540} y={330}><Pill text="بس مش هنقدر نتخلى عن الـ Raster" size={44} /></In>
      <In at={4} x={540} y={850}>
        <GFrame w={800} h={640}>
          <div style={{position: 'absolute', inset: 0, transform: `scale(${z})`, transformOrigin: '40% 70%'}}>
            <svg width={780} height={620} viewBox="0 0 780 620">
              <defs>
                <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#F7A35C" /><stop offset="0.6" stopColor="#FBD3A0" /><stop offset="1" stopColor="#FCE8C8" /></linearGradient>
              </defs>
              <rect width={780} height={620} fill="url(#sky)" />
              <circle cx={560} cy={210} r={60} fill="#FFF1C9" opacity={0.9} />
              <path d="M0 400 L120 250 L210 340 L330 200 L470 360 L590 260 L780 390 L780 620 L0 620 Z" fill="#7A6A8E" />
              <path d="M0 450 L160 330 L290 420 L420 300 L560 430 L700 350 L780 420 L780 620 L0 620 Z" fill="#5B5675" />
              <rect y={470} width={780} height={150} fill="#3E5A3A" />
              {trees.map((t, i) => <g key={i} transform={`translate(${t.x + 30} ${t.y}) scale(${t.s})`}><polygon points="0,-60 22,0 -22,0" fill={i % 3 ? '#2F4A2C' : '#3D6338'} /><rect x={-3} y={0} width={6} height={12} fill="#4A3426" /></g>)}
            </svg>
          </div>
        </GFrame>
      </In>
      <In at={at(b, 'det', 40)} x={300} y={1280} rot={-4}><Pill text="✓ فيها تفاصيل" bg="#2DBE60" ink="#fff" size={48} /></In>
      <In at={at(b, 'photo', 100)} x={780} y={1280} rot={4}><Pill text="📷 الصور الفوتوغرافية" size={44} /></In>
    </Sc>
  );
};

// 10) vector → PNG when you use it as a picture; raster → vector (trace) loses details
export const V8Convert: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const tr = at(b, 'trace', 70);
  const second = f >= tr;
  const arrow = (d: number) => <In at={d} x={540} y={840}><div style={{fontSize: 120, color: C.ink, fontFamily: EN, fontWeight: 900}}>←</div></In>;
  const box = (child: React.ReactNode, label: string, x: number, d: number, en = true) => (
    <In at={d} x={x} y={840}>
      <GFrame w={330} h={330}><div style={{width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{child}</div></GFrame>
      <div style={{textAlign: 'center', marginTop: 14, fontFamily: en ? EN : AR, fontWeight: 900, fontSize: 40, color: C.ink}}>{label}</div>
    </In>
  );
  const vec = <svg width={220} height={200} viewBox="0 0 200 180"><path d={HEART} fill={C.a} /></svg>;
  const photo = (
    <svg width={300} height={300} viewBox="0 0 300 300">
      <rect width={300} height={300} fill="#FBD3A0" /><circle cx={210} cy={90} r={30} fill="#FFF1C9" />
      <path d="M0 200 L60 120 L110 170 L170 100 L240 180 L300 140 L300 300 L0 300 Z" fill="#6E6488" />
      {Array.from({length: 22}, (_, i) => <polygon key={i} points={`${(i * 41) % 300},${230 + (i * 17) % 40} ${(i * 41) % 300 + 10},${260 + (i * 17) % 40} ${(i * 41) % 300 - 10},${260 + (i * 17) % 40}`} fill="#2F4A2C" />)}
    </svg>
  );
  const traced = (
    <svg width={300} height={300} viewBox="0 0 300 300">
      <rect width={300} height={300} fill="#F7C08A" /><circle cx={210} cy={90} r={34} fill="#FFF" />
      <path d="M0 210 L80 120 L160 190 L300 130 L300 300 L0 300 Z" fill="#5B5675" /><rect y={250} width={300} height={50} fill="#2F4A2C" />
    </svg>
  );
  return (
    <Sc>
      {!second ? (
        <>
          <In at={0} x={540} y={330}><Pill text="عايز تستخدمه كصورة؟" size={50} /></In>
          {box(vec, 'Vector', 820, 4)}{arrow(16)}{box(<div style={{transform: 'scale(1.1)'}}><PixelHeart px={18} n={14} t0={-999} gap={1} grid={false} /></div>, 'PNG', 260, 26)}
        </>
      ) : (
        <>
          <In at={tr} x={540} y={330}><Pill text="وممكن العكس.. بس الشكل هيتغير" size={44} /></In>
          {box(photo, 'Raster', 820, tr + 4)}{arrow(tr + 14)}{box(traced, 'Vector', 260, tr + 24)}
          <In at={tr + 40} x={540} y={1250}><Pill text="التفاصيل هتقل" bg="#E53935" ink="#fff" size={48} /></In>
        </>
      )}
    </Sc>
  );
};

// 11) file formats + programs
export const V8Tools: React.FC<{b?: B}> = ({b = {}}) => {
  const pr = at(b, 'progs', 60);
  const fmts = ['SVG', 'AI', 'EPS', 'PDF'];
  return (
    <Sc>
      <In at={0} x={540} y={330}><Pill text="صيغ ملفات معينة 📄" size={50} /></In>
      {fmts.map((x, i) => (
        <In key={x} at={6 + i * 5} x={180 + i * 240} y={600} rot={(i % 2 ? 5 : -5)}>
          <div style={{width: 190, height: 220, background: '#fff', borderRadius: 18, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 14px 30px rgba(0,0,0,0.2)',
            borderTop: `16px solid ${i % 2 ? C.b : C.a}`}}>
            <span style={{fontFamily: EN, fontWeight: 900, fontSize: 52, color: C.ink}}>.{x}</span>
          </div>
        </In>
      ))}
      <In at={pr} x={540} y={900}><Pill text="وبرامج معينة 🖥️" bg={grad('huwa')} ink="#fff" size={50} /></In>
      <In at={pr + 6} x={220} y={1180}><Logo src="illustrator.svg" w={210} h={210} name="Illustrator" /></In>
      <In at={pr + 12} x={540} y={1180}><Logo src="inkscape.png" w={210} h={210} name="Inkscape" /></In>
      <In at={pr + 18} x={860} y={1180}><Logo src="affinity.png" w={210} h={210} name="Affinity" /></In>
    </Sc>
  );
};

// 12) "ده كان هو ايه؟ vectors" + the next term (keeps them going to the playlist)
export const HuwaOutro: React.FC<{term: string; next?: string; b?: B}> = ({term, next, b = {}}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const nx = at(b, 'next', 50);
  return (
    <Sc>
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 30, marginTop: -120}}>
        <div style={{transform: `scale(${spr(f, fps, 0, 160, 11)})`}}><HuwaLogo h={330} /></div>
        <div style={{marginTop: 10, fontFamily: EN, fontWeight: 900, fontSize: 92, letterSpacing: 6, color: C.ink, opacity: lin(f, 10, 20), textTransform: 'uppercase'}}>{term}</div>
        {next ? (
          <div style={{opacity: lin(f, nx, nx + 10), transform: `translateY(${(1 - lin(f, nx, nx + 12)) * 40}px)`, marginTop: 40, direction: 'rtl', textAlign: 'center'}}>
            <div style={{fontFamily: AR, fontWeight: 800, fontSize: 38, color: C.soft}}>المصطلح الجاي في السلسلة</div>
            <div style={{marginTop: 12}}><Pill text={`${next} ؟`} bg={grad('huwa')} ink="#fff" size={52} font={EN} dir="ltr" /></div>
          </div>
        ) : null}
      </AbsoluteFill>
    </Sc>
  );
};

export const vectorScenes: Record<string, React.FC<any>> = {
  v8_raster: V8Raster, v8_scale: V8Scale, v8_addrm: V8AddRemove, v8_heavy: V8Heavy, v8_sizes: V8Sizes, v8_alt: V8Alt, v8_pen: V8Pen,
  v8_size: V8FileSize, v8_photo: V8Photo, v8_convert: V8Convert, v8_tools: V8Tools, huwa_outro: HuwaOutro,
};
export {Type};
