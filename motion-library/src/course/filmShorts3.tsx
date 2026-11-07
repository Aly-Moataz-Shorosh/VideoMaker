import React from 'react';
import {Easing, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, G, Glass, lin, Pill, spr} from '../glass/kit';
import {bi} from './kit';

// Review-1 scenes for the film-making course shorts (Aly 2026-11-07). Inside the stage (y 560..1370).
const GOLD = '#FFC21A', RED = '#E5232B', BLUE = '#3BA9F5', PINK = '#E05A9A', INK = '#14181F';

const Card: React.FC<{dur: number; h?: number; children: React.ReactNode}> = ({dur, h = 800, children}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 140, 16), o = 1 - lin(f, dur - 8, dur);
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, opacity: Math.min(1, p * 1.4) * o}}>
      <div style={{position: 'absolute', left: 40, top: 560}}><Glass w={1000} h={h} pad={0} r={40} glow={GOLD}><div /></Glass></div>
      {children}
    </div>
  );
};
const Tag: React.FC<{text: string; y: number; at: number; c?: string; size?: number}> = ({text, y, at, c = GOLD, size: s0 = 46}) => {
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
const Head: React.FC<{x: number; y: number; c: string; look: number; s?: number}> = ({x, y, c, look, s = 1}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <circle r={34} fill={c} stroke="#fff" strokeWidth={4} />
    <path d={`M ${look * 30} -10 L ${look * 58} 0 L ${look * 30} 10 Z`} fill={c} stroke="#fff" strokeWidth={3} />
  </g>
);

// ---------- the 180-degree rule: top view (two people, the line, the camera stays on one side) + what each shot shows ----------
export const Rule180: React.FC<{dur: number; crossAt?: number; tags?: {t: number; text: string; c?: string}[]}> = ({dur, crossAt, tags = []}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const crossed = crossAt !== undefined && f >= crossAt * fps;
  const k = crossAt === undefined ? 0 : lin(f, crossAt * fps, crossAt * fps + 16, 0, 1, Easing.inOut(Easing.cubic));
  const A = {x: 360, y: 760}, B = {x: 720, y: 760};
  const camY = 760 + 150 - 300 * k, camX = 540 + 120 * (1 - k);
  const tag = [...tags].reverse().find((q) => f >= q.t * fps);
  const frame = (x: number, who: 'A' | 'B', label: string) => {
    const look = who === 'A' ? 1 : -1, flip = crossed && who === 'B' ? -1 : 1;
    return (
      <div style={{position: 'absolute', left: x, top: 960, width: 420}}>
        <div style={{position: 'relative', width: 420, height: 240, borderRadius: 18, overflow: 'hidden', border: `4px solid ${crossed && who === 'B' ? RED : GOLD}`, background: '#1B2A44'}}>
          <svg width={420} height={240}><Head x={210} y={140} c={who === 'A' ? BLUE : PINK} look={look * flip} s={1.6} /></svg>
          <div style={{position: 'absolute', left: 10, bottom: 8, fontFamily: AR, fontWeight: 900, fontSize: 26, color: '#fff'}}>{bi(look * flip > 0 ? 'باصص يمين ←' : '→ باصص شمال')}</div>
        </div>
        <div style={{textAlign: 'center', fontFamily: AR, fontWeight: 800, fontSize: 28, color: G.soft, marginTop: 6}}>{bi(label)}</div>
      </div>
    );
  };
  return (
    <Card dur={dur}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 585, display: 'flex', justifyContent: 'center'}}><Pill text="قاعدة الـ 180 درجة" size={42} /></div>
      <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
        <line x1={120} y1={760} x2={960} y2={760} stroke={GOLD} strokeWidth={6} strokeDasharray="20 12" />
        <text x={950} y={745} textAnchor="end" fill={GOLD} fontFamily={AR} fontWeight={800} fontSize={26}>الخط</text>
        <path d={`M 200 760 A 340 150 0 0 0 880 760`} fill={crossed ? 'none' : 'rgba(255,194,26,0.08)'} stroke="rgba(255,255,255,0.25)" strokeWidth={3} />
        <Head x={A.x} y={A.y} c={BLUE} look={1} />
        <Head x={B.x} y={B.y} c={PINK} look={-1} />
        <g transform={`translate(${camX} ${camY}) rotate(${-90 + 180 * k})`}>
          <rect x={-30} y={-20} width={50} height={40} rx={8} fill={crossed ? RED : GOLD} /><path d="M 20 -10 L 40 -20 L 40 20 L 20 10 Z" fill={crossed ? RED : GOLD} />
        </g>
      </svg>
      {frame(80, 'A', 'لقطة 1')}
      {frame(580, 'B', 'لقطة 2')}
      {tag ? <Tag key={tag.t} text={tag.text} y={1265} at={Math.round(tag.t * fps)} c={tag.c ?? GOLD} /> : null}
    </Card>
  );
};

// ---------- more composition rules than thirds, one mini drawing each ----------
const RULES: {name: string; ar: string; draw: (p: number) => React.ReactNode}[] = [
  {name: 'Rule of thirds', ar: 'قاعدة الأثلاث', draw: (p) => <>{[1, 2].map((i) => <line key={i} x1={i * 93} y1={0} x2={i * 93} y2={170} stroke="#fff" strokeOpacity={0.5} strokeWidth={2} />)}{[1, 2].map((i) => <line key={'h' + i} x1={0} y1={i * 57} x2={280} y2={i * 57} stroke="#fff" strokeOpacity={0.5} strokeWidth={2} />)}<circle cx={186} cy={57} r={16 * p} fill={GOLD} /></>},
  {name: 'Leading lines', ar: 'خطوط بتشدّك', draw: (p) => <>{[-1, 1].map((s) => <line key={s} x1={140 + s * 150} y1={170} x2={140 + s * 150 * (1 - p)} y2={170 - 110 * p} stroke="#fff" strokeWidth={4} />)}<circle cx={140} cy={60} r={14} fill={GOLD} opacity={p} /></>},
  {name: 'Symmetry', ar: 'تماثل', draw: (p) => <><line x1={140} y1={0} x2={140} y2={170} stroke={GOLD} strokeWidth={3} strokeDasharray="8 6" />{[-1, 1].map((s) => <rect key={s} x={140 + s * 30 * p - (s < 0 ? 50 : 0)} y={50} width={50} height={80} fill="#fff" opacity={0.85} />)}</>},
  {name: 'Frame in frame', ar: 'كادر جوه كادر', draw: (p) => <><rect x={60} y={25} width={160} height={120} fill="none" stroke="#fff" strokeWidth={10 * p} /><circle cx={140} cy={85} r={18} fill={GOLD} /></>},
  {name: 'Negative space', ar: 'مساحة فاضية', draw: (p) => <circle cx={235} cy={130} r={14 + 4 * p} fill={GOLD} />},
  {name: 'Patterns', ar: 'تكرار.. وكسره', draw: (p) => <>{Array.from({length: 12}).map((_, i) => <circle key={i} cx={40 + (i % 6) * 40} cy={60 + Math.floor(i / 6) * 50} r={12} fill={i === 8 && p > 0.5 ? GOLD : '#fff'} opacity={0.85} />)}</>},
];
export const ComposeRules: React.FC<{dur: number; at?: number; step?: number}> = ({dur, at = 0.3, step = 0.8}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <Card dur={dur}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 580, display: 'flex', justifyContent: 'center'}}><Pill text="قوانين تكوين الكادر" size={42} /></div>
      {RULES.map((r, i) => {
        const t0 = (at + i * step) * fps;
        if (f < t0) return null;
        const p = spr(f, fps, t0, 160, 14), q = lin(f, t0 + 6, t0 + 26);
        return (
          <div key={i} style={{position: 'absolute', left: 90 + (i % 2) * 460, top: 670 + Math.floor(i / 2) * 230, width: 440, opacity: Math.min(1, p * 1.5), transform: `scale(${0.7 + 0.3 * p})`}}>
            <div style={{width: 280, height: 170, margin: '0 auto', borderRadius: 14, border: `4px solid ${GOLD}`, background: '#1B2A44', overflow: 'hidden'}}><svg width={280} height={170}>{r.draw(q)}</svg></div>
            <div style={{textAlign: 'center', fontFamily: AR, fontWeight: 900, fontSize: 30, color: '#fff', marginTop: 4, direction: 'rtl'}}>{bi(r.ar)} <span style={{fontFamily: EN, fontSize: 22, color: GOLD}}>{r.name}</span></div>
          </div>
        );
      })}
    </Card>
  );
};

// ---------- one film frame cut to different aspect ratios (what you lose in each) ----------
export const AspectCut: React.FC<{dur: number; img: string; keys: [number, string, string][]; credit?: string}> = ({dur, img, keys, credit}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  let i = 0; while (i + 1 < keys.length && f >= keys[i + 1][0] * fps) i++;
  const r = (s: string) => { const [a, b] = s.split(':').map(Number); return a / b; };
  const prev = keys[Math.max(0, i - 1)], cur = keys[i], u = i ? lin(f, cur[0] * fps, cur[0] * fps + 16, 0, 1, Easing.inOut(Easing.cubic)) : 1;
  const ar = r(prev[1]) + (r(cur[1]) - r(prev[1])) * u;
  const IW = 920, IH = 518, X = 80, Y = 650; // the full frame (16:9 source still)
  let w = IW, h = IW / ar; if (h > IH) { h = IH; w = IH * ar; }
  const x = X + (IW - w) / 2, y = Y + (IH - h) / 2;
  const phone = cur[1] === '9:16' ? lin(f, cur[0] * fps, cur[0] * fps + 20) : 0;
  return (
    <Card dur={dur}>
      <Img src={staticFile(img)} style={{position: 'absolute', left: X, top: Y, width: IW, height: IH, objectFit: 'cover', borderRadius: 12}} />
      {/* what is cut away = dark + red cross lines */}
      <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
        <path fillRule="evenodd" d={`M ${X} ${Y} h ${IW} v ${IH} h ${-IW} Z M ${x} ${y} v ${h} h ${w} v ${-h} Z`} fill="rgba(5,6,10,0.78)" />
        <rect x={x} y={y} width={w} height={h} fill="none" stroke={GOLD} strokeWidth={6} />
      </svg>
      {phone ? <div style={{position: 'absolute', left: 540 - 50, top: 590, fontSize: 60, transform: `rotate(${-90 + 90 * phone}deg)`}}>📱</div> : null}
      <div style={{position: 'absolute', left: 0, right: 0, top: 1190, display: 'flex', justifyContent: 'center', gap: 18, direction: 'rtl'}}>
        <Pill text={cur[1]} size={58} font={EN} dir="ltr" />
        <Pill text={cur[2]} size={46} color="rgba(10,14,22,0.9)" ink="#fff" glow={false} />
      </div>
      {credit ? <div style={{position: 'absolute', left: 90, top: 1172, fontFamily: AR, fontSize: 22, color: G.soft}}>{bi(credit)}</div> : null}
    </Card>
  );
};

// ---------- a dated fact with its source (Aly: say WHEN; every fact with a source) ----------
export const FactCard: React.FC<{dur: number; title: string; text: string; src: string; at?: number}> = ({dur, title, text, src, at = 0.2}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, at * fps, 150, 15), o = 1 - lin(f, dur - 8, dur);
  return (
    <div style={{position: 'absolute', left: 70, right: 70, top: 1000, opacity: Math.min(1, p * 1.4) * o, transform: `translateY(${(1 - p) * 40}px)`}}>
      <div style={{padding: '16px 24px', borderRadius: 28, background: 'rgba(12,16,26,0.95)', border: `3px solid ${GOLD}`, direction: 'rtl', boxShadow: `0 0 40px ${GOLD}55`}}>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 34, color: GOLD}}>{bi(title)}</div>
        <div style={{fontFamily: AR, fontWeight: 800, fontSize: 32, color: '#fff', lineHeight: 1.35, marginTop: 4}}>{bi(text)}</div>
        <div style={{fontFamily: AR, fontWeight: 700, fontSize: 22, color: G.soft, marginTop: 8}}>{bi('المصدر: ' + src)}</div>
      </div>
    </div>
  );
};


// ---------- two kinds of beauty (Aly 2026-11-07, short 08): FORM (shape, tools) vs CONTENT (meaning, tools) — in writing, then in video ----------
export const TwoBeauty: React.FC<{dur: number; mode?: string; leftAt?: number; rightAt?: number; step?: number}> = ({dur, mode = 'writing', leftAt = 0.3, rightAt = 3, step = 0.7}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const W = mode === 'writing'
    ? {title: 'في الكتابة', L: {h: 'جمال الشكل', sub: 'شكل الحروف', ex: ['✒️ الخط العربي', '🏺 الهيروغليفي'], tools: ['🖌️ فرشة', '🎨 ألوان']},
       R: {h: 'جمال المضمون', sub: 'المعنى وطريقة توصيله', ex: ['📜 كلام يوصل', '💡 معنى عميق'], tools: ['النحو', 'البلاغة']}}
    : {title: 'في الفيديو', L: {h: 'بلاغة الصورة والمزيكا', sub: 'المتعة اللي تخليك تكمل', ex: ['🎞️ الست', '🐘 الفيل الأزرق'], tools: ['🎨 ألوان', '🎵 صوت', '💡 رسم بالضوء', '🎥 حركة']},
       R: {h: 'بلاغة المحتوى', sub: 'معنى حلو.. بطريقة عميقة', ex: ['🎯 الأدوات في خدمة المعنى', 'مش بس الانتباه والمتعة'], tools: ['حركة الكاميرا', 'حجم اللقطة', 'القطع ✂️']}};
  const col = (side: 'L' | 'R', x: number, at: number, c: string) => {
    const d = W[side], p = spr(f, fps, at * fps, 150, 15);
    if (f < at * fps) return null;
    return (
      <div style={{position: 'absolute', left: x, top: 660, width: 445, opacity: Math.min(1, p * 1.4), transform: `translateY(${(1 - p) * 50}px)`, direction: 'rtl'}}>
        <div style={{padding: '14px 18px', borderRadius: 26, background: 'rgba(10,14,22,0.9)', border: `4px solid ${c}`, boxShadow: `0 0 34px ${c}44`, minHeight: 600}}>
          <div style={{fontFamily: AR, fontWeight: 900, fontSize: 40, color: c}}>{bi(d.h)}</div>
          <div style={{fontFamily: AR, fontWeight: 800, fontSize: 26, color: G.soft, marginTop: 2}}>{bi(d.sub)}</div>
          <div style={{marginTop: 16, display: 'flex', flexDirection: 'column', gap: 10}}>
            {d.ex.map((e, i) => { const q = spr(f, fps, (at + 0.5 + i * step) * fps, 170, 14); return f < (at + 0.5 + i * step) * fps ? null :
              <div key={i} style={{fontFamily: AR, fontWeight: 900, fontSize: 32, color: '#fff', transform: `scale(${0.7 + 0.3 * q})`, transformOrigin: 'right center'}}>{bi(e)}</div>; })}
          </div>
          <div style={{marginTop: 18, fontFamily: AR, fontWeight: 800, fontSize: 24, color: G.soft}}>الأدوات:</div>
          <div style={{display: 'flex', flexWrap: 'wrap', gap: 8, marginTop: 6}}>
            {d.tools.map((t, i) => { const tt = at + 0.5 + (d.ex.length + i) * step; if (f < tt * fps) return null; const q = spr(f, fps, tt * fps, 200, 12);
              return <div key={i} style={{padding: '6px 14px', borderRadius: 16, background: c, fontFamily: AR, fontWeight: 900, fontSize: 26, color: INK, transform: `scale(${q})`}}>{bi(t)}</div>; })}
          </div>
        </div>
      </div>
    );
  };
  return (
    <Card dur={dur}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 585, display: 'flex', justifyContent: 'center'}}><Pill text={'الجمال نوعين ' + W.title} size={42} /></div>
      {col('L', 545, leftAt, GOLD)}
      {col('R', 70, rightAt, BLUE)}
    </Card>
  );
};


// ---------- pictures instead of text (Aly 2026-11-07, short 08: "حط الصور محدش هيقرا كل ده"): one big picture at a time + a short label ----------
export const PicBoard: React.FC<{dur: number; items: {t: number; img: string; label: string; credit?: string}[]; title?: string}> = ({dur, items, title}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const o = 1 - lin(f, dur - 8, dur);
  let i = -1; items.forEach((it, j) => { if (f >= it.t * fps) i = j; });
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, opacity: o}}>
      {title ? <div style={{position: 'absolute', left: 0, right: 0, top: 575, display: 'flex', justifyContent: 'center'}}><Pill text={title} size={42} /></div> : null}
      {items.map((it, j) => {
        if (j !== i && j !== i - 1) return null;
        const p = spr(f, fps, it.t * fps, 150, 15), out = j === i - 1 ? lin(f, items[i].t * fps, items[i].t * fps + 10) : 0;
        if (j === i - 1 && out >= 1) return null;
        return (
          <div key={j} style={{position: 'absolute', left: 70, top: 660, width: 940, opacity: Math.min(1, p * 1.4) * (1 - out), transform: `scale(${0.85 + 0.15 * p}) rotate(${(j % 2 ? 1.5 : -1.5) * (1 - p)}deg)`}}>
            <div style={{padding: 12, borderRadius: 26, background: '#fff', boxShadow: '0 30px 70px rgba(0,0,0,0.6)'}}>
              <Img src={staticFile(it.img)} style={{width: 916, height: 520, objectFit: 'contain', background: '#111', borderRadius: 16, display: 'block'}} />
              <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 8px 2px', direction: 'rtl'}}>
                <span style={{fontFamily: AR, fontWeight: 900, fontSize: 44, color: INK}}>{bi(it.label)}</span>
                {it.credit ? <span style={{fontFamily: AR, fontWeight: 700, fontSize: 22, color: '#5A6270'}}>{bi(it.credit)}</span> : null}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};


// ---------- short 08 (Aly review 3): a line splits الشكل (right) / المحتوى (left); a picture per side when he says it; small chips for styles ----------
export const BeautySplit: React.FC<{dur: number; items?: {t: number; side: string; img: string; label: string}[]; chips?: {t: number; side: string; text: string}[]; cin?: boolean; cout?: boolean; under?: boolean}> = ({dur, items = [], chips = [], cin = false, cout = false}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pIn = cin ? 1 : spr(f, fps, 0, 140, 16), o = cout ? 1 : 1 - lin(f, dur - 8, dur);
  const col = (side: string, x: number, title: string, c: string) => {
    const it = [...items].reverse().find((q) => q.side === side && f >= q.t * fps);
    const ch = [...chips].reverse().find((q) => q.side === side && f >= q.t * fps && (!it || q.t >= it.t));
    const p = it ? spr(f, fps, it.t * fps, 150, 15) : 0;
    return (
      <div style={{position: 'absolute', left: x, top: 330, width: 470, direction: 'rtl'}}>
        <div style={{textAlign: 'center', fontFamily: AR, fontWeight: 900, fontSize: 40, color: c}}>{title}</div>
        {it ? <div key={it.t} style={{marginTop: 10, opacity: Math.min(1, p * 1.5), transform: `scale(${0.85 + 0.15 * p})`}}>
          <Img src={staticFile(it.img)} style={{width: 470, height: 300, objectFit: 'cover', borderRadius: 18, border: `4px solid ${c}`, display: 'block', boxShadow: `0 0 30px ${c}55`}} />
          <div style={{marginTop: 8, textAlign: 'center', fontFamily: AR, fontWeight: 900, fontSize: 32, color: '#fff'}}>{bi(it.label)}</div>
        </div> : null}
        {ch ? <div key={'c' + ch.t} style={{position: 'absolute', left: 0, right: 0, top: it ? 410 : 120, display: 'flex', justifyContent: 'center', transform: `scale(${spr(f, fps, ch.t * fps, 200, 12)})`}}>
          <div style={{padding: '8px 20px', borderRadius: 22, background: c, fontFamily: AR, fontWeight: 900, fontSize: 32, color: INK}}>{bi(ch.text)}</div></div> : null}
      </div>
    );
  };
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, opacity: Math.min(1, pIn * 1.4) * o}}>
      <div style={{position: 'absolute', left: 40, top: 320}}><Glass w={1000} h={548} pad={0} r={36} glow={GOLD}><div /></Glass></div>
      <div style={{position: 'absolute', left: 538, top: 340, width: 4, height: 500, background: `linear-gradient(180deg, ${GOLD}, ${BLUE})`, borderRadius: 2}} />
      {col('form', 560, 'جمال الشكل', GOLD)}
      {col('content', 50, 'جمال المحتوى', BLUE)}
    </div>
  );
};

export const filmScenes3: Record<string, React.FC<any>> = {Rule180, ComposeRules, AspectCut, FactCard, TwoBeauty, PicBoard, BeautySplit};
