import React from 'react';
import {Easing, Img, staticFile, useCurrentFrame} from 'remotion';
import {useBeats} from '../film/kit';
import {AR, Bulb, Bust, Chip, Cursor, EN, G, GScene, Glass, In, Label, Mark, Orb, Pill, Sphere, Studio, Top, Type, lin, spr} from './kit';

// Lighting short (2026-10-14): one scene per chapter of his video; beats = seconds from scene start (make_short.py).
// The stage is the TOP part (y 0..~720): his camera (Cam) is always below / in the middle, never covered.
type B = {b?: Record<string, number>; pics?: string};
const ROWS = (on: {key?: number; back?: number; fill?: number}, start: {key?: boolean; back?: boolean} = {}) => [
  {id: 'key', en: 'Key Light', ar: 'الضوء الأساسي', color: G.key, on: on.key, start: start.key},
  {id: 'back', en: 'Back Light', ar: 'الضوء الخلفي', color: G.back, on: on.back, start: start.back},
  {id: 'fill', en: 'Ambient Light', ar: 'الإضاءة المحيطة', color: G.fill, on: on.fill},
];

// ---------- 0. hook: from THIS quality (his camera, full screen) to THAT (after card), with a phone only ----------
export const GlHook: React.FC<B> = ({b, pics = ''}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const that = at('that', 5.6), phone = at('phone', 8.8);
  const wipe = lin(f, that + 4, that + 26, 0, 1, Easing.inOut(Easing.cubic));
  return (
    <GScene>
      {f < that ? (
        <>
          <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 520, background: 'linear-gradient(180deg, rgba(5,8,14,0.85), transparent)'}} />
          <Top text="إزاي تطوّر جودة *كاميرا_الموبايل*" at={2} y={150} size={74} out={that - 8} />
          <In at={at('this', 3.9)} x={540} y={1430}><Pill text="الجودة دي 👇" color="rgba(255,255,255,0.92)" size={54} /></In>
        </>
      ) : null}
      <In at={that} x={540} y={385}>
        <div style={{position: 'relative'}}>
          <Glass w={960} h={560} pad={14} r={44} glow={G.fill}>
            <div style={{position: 'relative', width: '100%', height: '100%', borderRadius: 32, overflow: 'hidden', background: '#05070B'}}>
              <Img src={staticFile(pics + 'after.jpg')} style={{position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', clipPath: `inset(0 0 0 ${(1 - wipe) * 100}%)`}} />
            </div>
          </Glass>
          {wipe > 0 && wipe < 1 ? <Orb x={14 + 932 * (1 - wipe)} y={280} color={G.fill} r={22} /> : null}
          <div style={{position: 'absolute', right: 34, top: -34}}><Pill text="لكده ✨" size={56} /></div>
        </div>
      </In>
      <In at={phone} x={540} y={712}><Pill text="📱 بكاميرا الموبايل وبس" color={G.blue} ink="#fff" size={52} /></In>
    </GScene>
  );
};

// ---------- 1. the idea: light is not just to be seen -> it gives a 3rd dimension (2D circle -> 3D sphere by a shadow) ----------
export const GlIdea: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const goal = at('goal', 6), d3 = at('d3', 11), sh = at('shadow', 13), depth = at('depth', 15);
  const flat = 1 - lin(f, sh, sh + 22);
  const t = (f - sh) / 30;
  const ang = 135 + (f > sh ? 30 * Math.sin(t * 1.4) : 0);
  const ox = 540 + 230 * Math.cos((ang * Math.PI) / 180), oy = 470 - 230 * Math.sin((ang * Math.PI) / 180);
  return (
    <GScene>
      {f < goal ? (
        <>
          <Top text="النور مش هدفه إنك *تبان* وبس" at={2} y={200} size={78} out={goal - 8} />
          <In at={at('no', 4.5)} out={goal - 8} x={540} y={470}><Mark ok={false} s={1.6} /></In>
        </>
      ) : (
        <>
          <Top text="الهدف: *بُعد_تالت*" at={goal} y={110} size={74} />
          <In at={goal + 8} x={540} y={480}><Sphere d={300} flat={flat} ang={ang} /></In>
          {f > sh ? <Orb x={ox} y={oy} color={G.key} r={20} o={lin(f, sh, sh + 10)} /> : null}
          <In at={goal + 14} x={840} y={330}><Pill text={f < sh + 10 ? '2D' : '3D'} color={f < sh + 10 ? 'rgba(255,255,255,0.85)' : G.gold} font={EN} dir="ltr" size={60} /></In>
          {f >= d3 && f < sh ? <In at={d3} x={240} y={480}><Label text="دايرة مسطحة" size={44} color={G.soft} /></In> : null}
          <In at={depth} x={540} y={665}><Type text="الظل = [إحساس_بالعمق]" at={depth} size={58} /></In>
        </>
      )}
    </GScene>
  );
};

// ---------- 2. step 1: switch every light in the room OFF ----------
export const GlOff: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const off = at('off', 4.2), dark = at('dark', 6);
  const dim = lin(f, off, off + 10, 0, 0.55);
  return (
    <GScene>
      <div style={{position: 'absolute', inset: 0, background: '#000', opacity: dim}} />
      <Top text={f < dark ? 'أول خطوة: *اقفل* كل الأنوار' : 'مش شايفني [خالص] 🌑'} at={f < dark ? 2 : dark} y={150} size={72} />
      <In at={6} out={dark + 30} x={540} y={430}>
        <Studio w={860} title="Room" rows={[
          {id: 'room', en: 'Room Lights', ar: 'نور الأوضة كله', color: '#FFE2A8', start: true, off},
          {id: 'lamp', en: 'Wall Lamp', ar: 'لمبة الحيطة', color: '#FFE2A8', start: true, off: off + 4},
        ]} />
      </In>
      <In at={off + 4} out={dark - 8} x={540} y={1460}><Pill text="Lights · OFF" font={EN} dir="ltr" color="rgba(255,255,255,0.85)" size={52} /></In>
      {f < off + 10 ? <Cursor x={lin(f, off - 26, off - 2, 980, 868)} y={lin(f, off - 26, off - 2, 640, 405)} click={off - 2} /> : null}
    </GScene>
  );
};

// ---------- 3. Key light ----------
export const GlKey: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const on = at('on', 3.6);
  return (
    <GScene>
      <Chip n="01" en="Key Light" ar="الضوء الأساسي" color={G.key} at={2} y={70} />
      <In at={at('name', 2.6)} x={540} y={430}><Studio w={880} rows={ROWS({key: on})} focus="key" /></In>
      <Cursor x={lin(f, on - 30, on - 3, 1000, 905)} y={lin(f, on - 30, on - 3, 720, 342)} click={on - 3} />
      <In at={on + 6} x={540} y={1460}><Pill text="Key Light · ON" font={EN} dir="ltr" color={G.key} size={52} /></In>
    </GScene>
  );
};

// ---------- 4. hard vs soft, then the soft options ----------
export const GlHardSoft: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const hard = at('hard', 0.4), soft = at('soft', 1.6), direct = at('direct', 4), dry = at('dry', 7.5), box = at('box', 9), cloth = at('cloth', 12);
  const Card: React.FC<{en: string; ar: string; h: number; good?: boolean; mark?: number}> = ({en, ar, h, good, mark}) => (
    <Glass w={470} h={560} pad={26} r={40} glow={good && mark !== undefined && f > mark ? G.green : undefined}>
      <div style={{fontFamily: EN, fontWeight: 900, fontSize: 52, color: G.ink, textAlign: 'center', direction: 'ltr'}}>{en} Light</div>
      <div style={{fontFamily: AR, fontWeight: 700, fontSize: 38, color: G.soft, textAlign: 'center'}}>{ar}</div>
      <div style={{position: 'absolute', left: 115, top: 170}}><Sphere d={240} hard={h} ang={140} /></div>
      {mark !== undefined && f >= mark ? <div style={{position: 'absolute', right: 20, top: 20, transform: `scale(${spr(f, 30, mark)})`}}><Mark ok={!!good} /></div> : null}
    </Glass>
  );
  return (
    <GScene>
      {f < box ? (
        <>
          <Top text="نوعين: *Hard* و *Soft*" at={1} y={90} size={66} />
          <In at={hard} x={790} y={450}><Card en="Hard" ar="مباشر · حاد" h={1} mark={dry} /></In>
          <In at={soft} x={290} y={450}><Card en="Soft" ar="ناعم" h={0} good mark={dry} /></In>
          {f >= direct ? <Orb x={lin(f, direct, direct + 14, 1060, 860)} y={lin(f, direct, direct + 14, 200, 290)} color={G.key} r={18} /> : null}
          {f >= dry ? <In at={dry} x={790} y={760}><Pill text="شكلك ناشف" color={G.red} ink="#fff" size={44} /></In> : null}
        </>
      ) : (
        <>
          <Top text="عايز ضوء *ناعم* على وشك؟" at={box} y={110} size={68} />
          <In at={box + 6} x={540} y={360}><Opt icon={<SoftboxIcon />} en="Softbox" ar="سوفت بوكس" /></In>
          <In at={cloth} x={540} y={560}><Opt icon={<Bulb s={0.9} />} en="DIY" ar="لمبة + قماشة بيضا قدامها" /></In>
        </>
      )}
    </GScene>
  );
};
const Opt: React.FC<{icon: React.ReactNode; en: string; ar: string; extra?: React.ReactNode}> = ({icon, en, ar, extra}) => (
  <Glass w={900} h={170} pad={22} r={36}>
    <div style={{display: 'flex', alignItems: 'center', gap: 26, direction: 'rtl', height: '100%'}}>
      <div style={{width: 120, height: 120, borderRadius: 30, background: 'rgba(255,255,255,0.08)', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{icon}</div>
      <div style={{flex: 1}}>
        <div style={{fontFamily: AR, fontWeight: 800, fontSize: 52, color: G.ink}}>{ar}</div>
        <div style={{fontFamily: EN, fontWeight: 700, fontSize: 32, color: G.dim, direction: 'ltr', textAlign: 'right'}}>{en}</div>
      </div>
      {extra}
    </div>
  </Glass>
);
const SoftboxIcon: React.FC<{s?: number}> = ({s = 1}) => (
  <svg width={100 * s} height={100 * s} viewBox="0 0 100 100">
    <path d="M10 22 L90 22 L72 78 L28 78 Z" fill="#F7F3EA" stroke="#fff" strokeWidth={3} />
    <path d="M10 22 L90 22" stroke="#9AA6B5" strokeWidth={6} />
    <rect x={44} y={78} width={12} height={16} fill="#7C8797" />
    <circle cx={50} cy={48} r={30} fill={G.key} opacity={0.35} style={{filter: 'blur(6px)'}} />
  </svg>
);

// ---------- 5. angle: light straight from the front = no shadow; from an angle = depth ----------
export const GlAngle: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const front = at('front', 3.4), side = at('side', 7), depth = at('depth', 11);
  // light position: starts from the side (sentence 1), front (sentence 2, his camera is hidden -> the bust is big), side again
  const toFront = lin(f, front, front + 14), toSide = lin(f, side, side + 18);
  const ang = 40 + 50 * toFront - 55 * toSide;
  const big = f >= front && f < side;
  const W = big ? 470 : 300;
  const cx = 540, cy = big ? 900 : 470;
  const r = big ? 380 : 260;
  // side light: the dot circles beside the head; light from the front: the dot sits in front of him (low, under the chin, big glow)
  const sideX = cx + r * Math.cos((ang * Math.PI) / 180), sideY = cy - W * 0.2;
  const fr = lin(f, front, front + 14) * (1 - lin(f, side, side + 18));
  const ox = sideX + (cx - sideX) * fr, oy = sideY + (cy + W * 0.75 - sideY) * fr;
  return (
    <GScene>
      <Top text={f < front ? 'خلّي الضوء *بزاوية*' : f < side ? 'ضوء من قدام = *مفيش_ظل*' : 'بزاوية = [عمق] أكتر'} at={f < front ? 2 : f < side ? front : side} y={big ? 260 : 110} size={70} />
      <In at={4} x={cx} y={cy} key={big ? 'b' : 's'} from={0.94} dy={10}><Bust w={W} ang={ang} /></In>
      <Orb x={ox} y={oy} color={G.key} r={big ? 34 : 20} />
      {big ? <In at={front + 8} x={540} y={cy + W * 0.75 + 90}><Label text="الضوء قدامك بالظبط" size={40} color={G.soft} /></In> : null}
      {big ? <In at={front + 12} x={540} y={1540}><Mark ok={false} s={1.4} /></In> : null}
      {f >= side + 20 ? <In at={side + 20} x={850} y={420}><Mark ok s={1.1} /></In> : null}
      {f >= depth ? <In at={depth} x={540} y={700}><Pill text="ظل خفيف في الجنب ✓" color={G.gold} size={46} /></In> : null}
    </GScene>
  );
};

// ---------- 6. keep the wall far behind you ----------
export const GlWall: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const wall = at('wall', 2.2), far = at('far', 4.4);
  const wx = lin(f, far, far + 20, 560, 860, Easing.inOut(Easing.cubic));
  return (
    <GScene>
      <Top text={f < far ? 'متصوّرش و*الحيطة* في ضهرك' : '[بعّد] عن الحيطة'} at={f < far ? 2 : far} y={100} size={66} />
      <In at={4} x={540} y={450}>
        <Glass w={960} h={480} pad={0} r={40}>
          <svg width={960} height={480} style={{position: 'absolute', left: 0, top: 0}}>
            {/* floor with perspective lines (depth) */}
            {Array.from({length: 9}, (_, i) => <line key={i} x1={60 + i * 105} y1={400} x2={480 + (i - 4) * 30} y2={300} stroke="rgba(255,255,255,0.10)" strokeWidth={2} />)}
            <line x1={40} y1={400} x2={920} y2={400} stroke="rgba(255,255,255,0.35)" strokeWidth={3} />
            {/* camera */}
            <rect x={90} y={250} width={110} height={74} rx={14} fill={G.blue} /><circle cx={200} cy={287} r={22} fill="#0B1220" stroke="#fff" strokeWidth={4} />
            <line x1={145} y1={324} x2={145} y2={400} stroke="#9AA6B5" strokeWidth={6} />
            {/* wall */}
            <rect x={wx} y={90} width={34} height={310} rx={6} fill={f < far ? '#FF5A5F' : G.green} opacity={0.9} />
            {f >= far ? (
              <>
                <line x1={500} y1={130} x2={wx - 14} y2={130} stroke={G.gold} strokeWidth={5} strokeDasharray="14 10" />
                <path d={`M${wx - 30} 116 L${wx - 10} 130 L${wx - 30} 144`} fill="none" stroke={G.gold} strokeWidth={5} />
              </>
            ) : null}
          </svg>
          <div style={{position: 'absolute', left: 380, top: 160}}><Bust w={170} ang={50} /></div>
          {f >= wall && f < far ? <div style={{position: 'absolute', left: 620, top: 40, transform: `scale(${spr(f, 30, wall)})`}}><Mark ok={false} /></div> : null}
          {f >= far + 18 ? <div style={{position: 'absolute', right: 40, top: 30, transform: `scale(${spr(f, 30, far + 18)})`}}><Mark ok /></div> : null}
        </Glass>
      </In>
    </GScene>
  );
};

// ---------- 7. back light: opposite the key, gives depth + rim on the edges ----------
export const GlBack: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const behind = at('behind', 3), edge = at('edge', 7), on = at('on', 11), white = at('white', 14), yellow = at('yellow', 15.5), contrast = at('contrast', 17);
  const keyOn = 1, backOn = lin(f, behind, behind + 12);
  return (
    <GScene>
      <Chip n="02" en="Back Light" ar="الضوء الخلفي" color={G.back} at={2} y={60} />
      {f < edge ? (
        <In at={6} x={540} y={430} out={edge - 8}>
          <Glass w={940} h={520} pad={0} r={40}>
            <svg width={940} height={520} style={{position: 'absolute', left: 0, top: 0}}>
              <defs>
                <radialGradient id="kc"><stop offset="0" stopColor={G.key} stopOpacity={0.55} /><stop offset="1" stopColor={G.key} stopOpacity={0} /></radialGradient>
                <radialGradient id="bc"><stop offset="0" stopColor={G.back} stopOpacity={0.7} /><stop offset="1" stopColor={G.back} stopOpacity={0} /></radialGradient>
              </defs>
              <path d="M170 420 L430 230 L520 330 Z" fill="url(#kc)" opacity={keyOn} />
              <path d="M790 110 L450 250 L540 320 Z" fill="url(#bc)" opacity={backOn} />
              <circle cx={470} cy={280} r={52} fill="#AEB7C4" stroke={backOn > 0.5 ? G.back : '#fff'} strokeWidth={6} />
              <rect x={430} y={440} width={80} height={52} rx={10} fill={G.blue} /><circle cx={470} cy={440} r={16} fill="#0B1220" stroke="#fff" strokeWidth={3} />
            </svg>
            <div style={{position: 'absolute', left: 110, top: 380}}><Bulb color={G.key} s={0.9} /></div>
            <div style={{position: 'absolute', left: 750, top: 50, opacity: backOn}}><Bulb color={G.back} s={0.9} /></div>
            <div style={{position: 'absolute', left: 40, top: 300, fontFamily: EN, fontWeight: 800, fontSize: 30, color: G.key}}>KEY</div>
            <div style={{position: 'absolute', left: 760, top: 150, fontFamily: EN, fontWeight: 800, fontSize: 30, color: G.back, opacity: backOn}}>BACK</div>
            {f >= behind + 10 ? <div style={{position: 'absolute', right: 40, bottom: 30}}><Pill text="ورا · عكس الـ Key" color={G.back} size={40} /></div> : null}
          </Glass>
        </In>
      ) : f < on ? (
        <>
          <Top text="بيرسم [حواف] جسمك" at={edge} y={160} size={68} />
          <In at={edge + 4} x={540} y={490}><Bust w={300} ang={150} rim={G.back} rimK={lin(f, edge + 10, edge + 30, 0, 0.95)} /></In>
        </>
      ) : f < white ? (
        <>
          <In at={on - 14} x={540} y={400}><Studio w={880} rows={ROWS({back: on}, {key: true})} focus="back" /></In>
          <Cursor x={lin(f, on - 30, on - 3, 1000, 905)} y={lin(f, on - 30, on - 3, 720, 462)} click={on - 3} ring={G.back} />
          <In at={on + 6} x={540} y={1460}><Pill text="Back Light · ON" font={EN} dir="ltr" color={G.back} size={52} /></In>
        </>
      ) : (
        <>
          <In at={white} x={540} y={260}><Swatch c={G.key} en="Key" ar="أبيض" /></In>
          <In at={yellow} x={540} y={450}><Swatch c={G.back} en="Back" ar="أصفر" /></In>
          <In at={contrast} x={540} y={640}><Pill text="= تباين · Contrast" size={52} /></In>
        </>
      )}
    </GScene>
  );
};
const Swatch: React.FC<{c: string; en: string; ar: string}> = ({c, en, ar}) => (
  <Glass w={720} h={150} pad={20} r={36} glow={c}>
    <div style={{display: 'flex', alignItems: 'center', gap: 24, height: '100%', direction: 'ltr'}}>
      <div style={{width: 110, height: 110, borderRadius: 28, background: c, boxShadow: `0 0 40px ${c}`}} />
      <span style={{fontFamily: EN, fontWeight: 900, fontSize: 56, color: G.ink}}>{en}</span>
      <span style={{fontFamily: AR, fontWeight: 800, fontSize: 56, color: c, marginLeft: 'auto'}}>{ar}</span>
    </div>
  </Glass>
);

// ---------- 8. control the spill: foil / any cover -> light out of one side only; softbox grid ----------
export const GlSpill: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const foil = at('foil', 2.6), out = at('out', 5.4), grid = at('grid', 8.6);
  const cap = lin(f, foil, foil + 16);
  const cx = 540, cy = 470;
  const rays = Array.from({length: 16}, (_, i) => (i / 16) * 360);
  return (
    <GScene>
      <Top text={f < foil ? 'إزاي [تحدد] مسار الضوء؟' : f < grid ? 'غطّيها *ألمونيوم*' : 'أو *Grid* · شبكة'} at={f < foil ? 2 : f < grid ? foil : grid} y={110} size={70} />
      {f < grid ? (
        <In at={4} x={0} y={0}>
          <svg width={1080} height={760} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
            {rays.map((a, i) => {
              const fwd = Math.abs(((a + 180) % 360) - 180) < 30; // rays toward screen right stay
              const op = fwd ? 1 : 1 - cap;
              const pul = 0.75 + 0.25 * Math.sin(f / 5 + i);
              const r0 = 90, r1 = fwd && f > out ? 470 : 230 * pul;
              const rad = (a * Math.PI) / 180;
              return <line key={i} x1={cx + r0 * Math.cos(rad)} y1={cy - r0 * Math.sin(rad)} x2={cx + r1 * Math.cos(rad)} y2={cy - r1 * Math.sin(rad)}
                stroke={G.key} strokeWidth={fwd && f > out ? 10 : 7} strokeLinecap="round" opacity={op * 0.9} />;
            })}
            {f > out ? <path d={`M${cx + 80} ${cy - 50} L${cx + 520} ${cy - 230} L${cx + 520} ${cy + 230} L${cx + 80} ${cy + 50} Z`} fill={G.key} opacity={0.12 * lin(f, out, out + 10)} /> : null}
            {/* foil cap: silver half shell closing around the back of the bulb */}
            <path d={`M${cx + 60} ${cy - 100} A110 110 0 1 0 ${cx + 60} ${cy + 100}`} fill="none" stroke="url(#alu)" strokeWidth={34} strokeLinecap="round"
              strokeDasharray="700" strokeDashoffset={700 * (1 - cap)} />
            <defs><linearGradient id="alu" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#F2F5F8" /><stop offset="0.5" stopColor="#9AA6B5" /><stop offset="1" stopColor="#DDE3EA" /></linearGradient></defs>
          </svg>
          <div style={{position: 'absolute', left: cx - 58, top: cy - 62}}><Bulb s={1.3} /></div>
        </In>
      ) : (
        <In at={grid} x={540} y={450}>
          <Glass w={560} h={420} pad={0} r={36} glow={G.key}>
            <div style={{position: 'absolute', inset: 24, borderRadius: 20, background: '#F7F3EA', boxShadow: `0 0 80px ${G.key}`}} />
            <svg width={560} height={420} style={{position: 'absolute', left: 0, top: 0}}>
              {Array.from({length: 9}, (_, i) => <line key={'v' + i} x1={24 + (i + 1) * 51} y1={24} x2={24 + (i + 1) * 51} y2={396} stroke="#14181F" strokeWidth={8} />)}
              {Array.from({length: 6}, (_, i) => <line key={'h' + i} x1={24} y1={24 + (i + 1) * 53} x2={536} y2={24 + (i + 1) * 53} stroke="#14181F" strokeWidth={8} />)}
            </svg>
          </Glass>
        </In>
      )}
      {f >= out && f < grid ? <In at={out} x={300} y={700}><Pill text="يطلع من ناحية واحدة" size={44} /></In> : null}
      {f >= grid + 16 ? <In at={grid + 16} x={540} y={720}><Pill text="الضوء مايروحش يمين وشمال" size={44} /></In> : null}
    </GScene>
  );
};

// ---------- 9. ambient light: colours in the room (cyan) — LED strip (220 EGP) + the PC screen ----------
export const GlAmb: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const on = at('on', 4.6), led = at('led', 8), price = at('price', 10), screen = at('screen', 12.5);
  return (
    <GScene>
      <Chip n="03" en="Ambient Light" ar="الإضاءة المحيطة" color={G.fill} at={2} y={60} />
      {f < led ? (
        <>
          <In at={6} x={540} y={420}><Studio w={880} rows={ROWS({fill: on}, {key: true, back: true})} focus="fill" /></In>
          <Cursor x={lin(f, on - 30, on - 3, 1000, 905)} y={lin(f, on - 30, on - 3, 760, 582)} click={on - 3} ring={G.fill} />
          <In at={on + 6} out={led - 8} x={540} y={1460}><Pill text="Ambient Light · ON" font={EN} dir="ltr" color={G.fill} size={52} /></In>
        </>
      ) : (
        <>
          <In at={led} x={540} y={300}><Opt icon={<Led on={lin(f, led + 4, led + 30)} />} en="LED Strip" ar="شريط LED ورايا" /></In>
          {f >= price ? <In at={price} x={330} y={410} z={5}><Pill text="220 جنيه بس" size={46} /></In> : null}
          <In at={screen} x={540} y={540}><Opt icon={<Screen />} en="PC Screen" ar="شاشة الكمبيوتر = لون" /></In>
        </>
      )}
    </GScene>
  );
};
const Led: React.FC<{on: number}> = ({on}) => (
  <svg width={110} height={60} viewBox="0 0 110 60">
    <rect x={2} y={22} width={106} height={16} rx={8} fill="#2A3240" />
    {Array.from({length: 7}, (_, i) => <circle key={i} cx={10 + i * 15} cy={30} r={5} fill={i / 7 < on ? G.fill : '#55606F'} style={{filter: i / 7 < on ? `drop-shadow(0 0 6px ${G.fill})` : undefined}} />)}
  </svg>
);
const Screen: React.FC = () => (
  <svg width={100} height={90} viewBox="0 0 100 90">
    <rect x={4} y={6} width={92} height={58} rx={8} fill={G.blue} stroke="#fff" strokeWidth={3} style={{filter: `drop-shadow(0 0 10px ${G.blue})`}} />
    <rect x={44} y={64} width={12} height={14} fill="#9AA6B5" /><rect x={28} y={78} width={44} height={6} rx={3} fill="#9AA6B5" />
  </svg>
);

// ---------- 10. focus: blurred background with the phone (OpenCamera, manual focus) ----------
export const GlFocus: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const me = at('me', 3), phone = at('phone', 4.5), app = at('app', 6), mf = at('mf', 9), demo = at('demo', 12), bg = at('bg', 15), lens = at('lens', 18), mobile = at('mobile', 19.5);
  const slide = lin(f, mf + 6, mf + 30, 0.15, 0.62, Easing.inOut(Easing.cubic));
  return (
    <GScene>
      <Chip n="04" en="Focus" ar="الفوكس" color={G.blue} at={2} y={60} />
      {f < phone ? (
        <>
          <In at={4} x={540} y={430}>
            <Glass w={900} h={500} pad={0} r={40}>
              <div style={{position: 'absolute', inset: 0, borderRadius: 38, overflow: 'hidden'}}>
                {Array.from({length: 14}, (_, i) => (
                  <div key={i} style={{position: 'absolute', left: (i * 137) % 860, top: 30 + ((i * 89) % 420), width: 70 + (i % 4) * 30, height: 70 + (i % 4) * 30, borderRadius: '50%',
                    background: [G.fill, G.blue, G.back, G.key][i % 4], opacity: 0.45, filter: 'blur(14px)'}} />
                ))}
              </div>
              <div style={{position: 'absolute', left: 340, top: 120}}><Bust w={220} ang={60} /></div>
              {f >= me ? <FocusBox x={315} y={100} w={270} h={340} at={me} /> : null}
            </Glass>
          </In>
          <Top text="الخلفية *بلور* والفوكس عليك" at={2} y={120} size={60} />
        </>
      ) : f < bg ? (
        <>
          <In at={phone} x={720} y={400}><Phone slide={slide} mf={f >= mf} /></In>
          <In at={app} x={270} y={300}><Pill text="Open Camera" font={EN} dir="ltr" color={G.blue} ink="#fff" size={50} /></In>
          {f >= mf ? <In at={mf} x={270} y={460}><Pill text="Manual Focus" font={EN} dir="ltr" size={50} /></In> : null}
          {f >= mf + 10 ? <In at={mf + 10} x={270} y={600}><Label text="اضبطه على مكانك" size={42} /></In> : null}
        </>
      ) : f < demo ? (
        <>
          <Top text="الخلفية بلور… وانت في *الفوكس*" at={bg} y={130} size={64} />
          {f >= lens ? <In at={lens} x={540} y={420}><Pill text="📷 كأنها كاميرا بعدسة" color="rgba(255,255,255,0.92)" size={54} /></In> : null}
          {f >= mobile ? <In at={mobile} x={540} y={600}><Pill text="📱 وهي موبايل!" size={60} /></In> : null}
        </>
      ) : (
        <>
          <Top text="ولما أرجع ورا… [أنا] اللي ببقى بلور" at={demo} y={240} size={64} />
          <In at={demo + 6} x={540} y={1460}><Pill text="الفوكس ثابت على الكرسي 🎯" color={G.blue} ink="#fff" size={48} /></In>
        </>
      )}
    </GScene>
  );
};
const FocusBox: React.FC<{x: number; y: number; w: number; h: number; at: number}> = ({x, y, w, h, at}) => {
  const f = useCurrentFrame();
  const p = spr(f, 30, at, 200, 14);
  const L = 50, s = 1.25 - 0.25 * p;
  const c = (l: number, t: number, sx: number, sy: number) => (
    <path key={`${l}${t}`} d={`M${l} ${t + L * sy} L${l} ${t} L${l + L * sx} ${t}`} stroke={G.gold} strokeWidth={7} fill="none" strokeLinecap="round" />
  );
  return (
    <svg width={w} height={h} style={{position: 'absolute', left: x, top: y, transform: `scale(${s})`, opacity: p, overflow: 'visible'}}>
      {c(4, 4, 1, 1)}{c(w - 4, 4, -1, 1)}{c(4, h - 4, 1, -1)}{c(w - 4, h - 4, -1, -1)}
    </svg>
  );
};
const Phone: React.FC<{slide: number; mf: boolean}> = ({slide, mf}) => (
  <div style={{width: 330, height: 640, borderRadius: 56, background: '#0A0D12', border: '8px solid #2B3340', boxShadow: '0 40px 80px rgba(0,0,0,0.6)', position: 'relative', overflow: 'hidden'}}>
    <div style={{position: 'absolute', inset: 0, background: `radial-gradient(circle at 30% 30%, ${G.fill}55, transparent 40%), radial-gradient(circle at 75% 60%, ${G.blue}55, transparent 45%), #111826`,
      filter: `blur(${mf ? 10 * slide : 0}px)`}} />
    <div style={{position: 'absolute', left: 95, top: 190, filter: `blur(${mf ? 0 : 3}px)`}}><Bust w={140} ang={60} /></div>
    <div style={{position: 'absolute', top: 26, left: 0, right: 0, textAlign: 'center', fontFamily: EN, fontWeight: 700, fontSize: 22, color: '#fff', direction: 'ltr'}}>● REC  1080p</div>
    {/* manual focus slider */}
    <div style={{position: 'absolute', left: 30, right: 30, bottom: 70, height: 8, borderRadius: 4, background: 'rgba(255,255,255,0.25)'}}>
      <div style={{position: 'absolute', left: `${slide * 100}%`, top: -16, width: 40, height: 40, marginLeft: -20, borderRadius: '50%', background: mf ? G.gold : '#fff', boxShadow: mf ? `0 0 20px ${G.gold}` : undefined}} />
    </div>
    <div style={{position: 'absolute', left: 0, right: 0, bottom: 22, textAlign: 'center', fontFamily: EN, fontWeight: 800, fontSize: 24, color: mf ? G.gold : G.soft, direction: 'ltr'}}>MF · {(0.4 + slide * 2).toFixed(1)} m</div>
  </div>
);

// ---------- 11. end: before / after + the 3 lights ----------
export const GlEnd: React.FC<B> = ({b, pics = ''}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const diff = at('diff', 3.5), k = at('k', 7), bk = at('b', 7.6), fl = at('f', 8.3);
  const wipe = lin(f, 18, diff + 20, 0.92, 0.08, Easing.inOut(Easing.cubic));
  return (
    <GScene>
      <Top text="من *الأول* لحد دلوقتي" at={2} y={40} size={62} />
      <In at={4} x={540} y={455}>
        <div style={{position: 'relative'}}>
          <Glass w={960} h={560} pad={14} r={44} glow={G.fill}>
            <div style={{position: 'relative', width: '100%', height: '100%', borderRadius: 32, overflow: 'hidden'}}>
              <Img src={staticFile(pics + 'before.jpg')} style={{position: 'absolute', width: '100%', height: '100%', objectFit: 'cover'}} />
              <Img src={staticFile(pics + 'after.jpg')} style={{position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', clipPath: `inset(0 0 0 ${wipe * 100}%)`}} />
              <div style={{position: 'absolute', top: 0, bottom: 0, left: `${wipe * 100}%`, width: 6, marginLeft: -3, background: '#fff', boxShadow: '0 0 20px #fff'}} />
              <div style={{position: 'absolute', top: '50%', left: `${wipe * 100}%`, width: 64, height: 64, margin: '-32px 0 0 -32px', borderRadius: '50%', background: 'rgba(255,255,255,0.9)',
                display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: EN, fontWeight: 900, color: '#14181F', fontSize: 28}}>‹ ›</div>
            </div>
          </Glass>
          <div style={{position: 'absolute', left: 34, top: 30}}><Pill text="قبل" color="rgba(255,255,255,0.9)" size={42} /></div>
          <div style={{position: 'absolute', right: 34, top: 30}}><Pill text="بعد" size={42} /></div>
        </div>
      </In>
      <div style={{position: 'absolute', top: 770, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 22, direction: 'ltr'}}>
        {[[k, 'Key', G.key], [bk, 'Back', G.back], [fl, 'Ambient', G.fill]].map(([t, n, c]) => (
          <div key={n as string} style={{opacity: lin(f, t as number, (t as number) + 8), transform: `scale(${f >= (t as number) ? spr(f, 30, t as number) : 0})`}}>
            <Pill text={n as string} font={EN} dir="ltr" color={c as string} size={46} />
          </div>
        ))}
      </div>
    </GScene>
  );
};

export const glassScenes: Record<string, React.FC<any>> = {
  gl_hook: GlHook, gl_idea: GlIdea, gl_off: GlOff, gl_key: GlKey, gl_hardsoft: GlHardSoft, gl_angle: GlAngle, gl_wall: GlWall,
  gl_back: GlBack, gl_spill: GlSpill, gl_amb: GlAmb, gl_focus: GlFocus, gl_end: GlEnd,
};
