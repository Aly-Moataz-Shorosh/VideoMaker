import React from 'react';
import {AbsoluteFill, Img, useCurrentFrame} from 'remotion';
import {AR, EN, HuwaLogo, In, JY, lin, logo, Pill, ProgBadge, Sc, spr} from './kit';
import {BouncingBall3D, Building3D, Cloner3D, Principles3D, Room3D, Spinner3D} from './three';

// "البرامج" — the 3D programs (ep 37, 3:20–4:31). Look = his program tree: dark teal, orange headings, white names,
// HIS logo files (png logos folder; 3ds Max cut from his video at its own size, never upscaled).
const C = JY.prog;
type B = Record<string, number>;
const at = (b: B, k: string, d = 0) => b[k] ?? d;
const ORANGE = '#F08A24', YEL = '#F7C531';
const H: React.FC<{t: string; en?: boolean; size?: number; color?: string}> = ({t, en, size = 64, color = ORANGE}) => (
  <div style={{fontFamily: en ? EN : AR, fontWeight: en ? 600 : 900, fontSize: size, color, whiteSpace: 'nowrap', direction: en ? 'ltr' : 'rtl'}}>{t}</div>
);
const PROGS = [
  {k: 'maya', file: 'maya.jpg', name: 'MAYA'}, {k: 'max', file: '3dsmax.png', name: '3Ds MAX'},
  {k: 'blender', file: 'blender.png', name: 'BLENDER'}, {k: 'c4d', file: 'c4d.png', name: 'CINEMA 4D'},
];
// one row of his tree: logo (max 120 px — his 3ds Max icon is 128 px) + name
const Row: React.FC<{p: typeof PROGS[0]; hi?: boolean; dim?: boolean; tag?: string}> = ({p, hi, dim, tag}) => (
  <div style={{display: 'flex', alignItems: 'center', gap: 28, direction: 'ltr', opacity: dim ? 0.35 : 1, transform: `scale(${hi ? 1.08 : 1})`, transformOrigin: 'left center'}}>
    <Img src={logo(p.file)} style={{width: 120, height: 120, objectFit: 'contain', borderRadius: p.k === 'maya' || p.k === 'max' ? 8 : 0,
      filter: hi ? `drop-shadow(0 0 18px ${YEL})` : 'drop-shadow(0 8px 14px rgba(0,0,0,0.3))'}} />
    <div style={{fontFamily: EN, fontWeight: 600, fontSize: 60, color: '#fff'}}>{p.name}</div>
    {tag ? <div style={{fontFamily: AR, fontWeight: 900, fontSize: 36, color: C.bg1, background: YEL, padding: '4px 18px', borderRadius: 24, direction: 'rtl'}}>{tag}</div> : null}
  </div>
);

// 1) the tree: البرامج -> audio ✓, pictures ✓, 3D (now), video
export const P3Branch: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const d3 = at(b, 'd3', 30);
  const cats = [{t: 'صوت', x: 860, done: true}, {t: 'صور', x: 640, done: true}, {t: '3D', x: 420, on: true}, {t: 'فيديو', x: 200}];
  return (
    <Sc>
      <In at={0} x={540} y={460}><ProgBadge d={190} /></In>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        {cats.map((c, i) => (
          <path key={i} d={`M 540 580 C 540 700, ${c.x} 640, ${c.x} 820`} stroke={c.on && f >= d3 ? YEL : '#9CC3C0'} strokeWidth={c.on && f >= d3 ? 8 : 5} fill="none"
            pathLength={1} strokeDasharray={`${lin(f, 4 + i * 4, 20 + i * 4)} 1`} />
        ))}
      </svg>
      {cats.map((c, i) => (
        <In key={i} at={14 + i * 4} x={c.x} y={880}>
          <div style={{textAlign: 'center', transform: `scale(${c.on && f >= d3 ? 1.35 : 1})`}}>
            <H t={c.t} size={58} color={c.on && f >= d3 ? YEL : ORANGE} en={c.t === '3D'} />
            {c.done ? <div style={{fontSize: 40, color: '#7DDB9A'}}>✓</div> : null}
          </div>
        </In>
      ))}
      <In at={d3} x={540} y={1150}><Pill text="نتجه بقى للـ 3D 🧊" bg={YEL} ink={C.bg1} size={52} /></In>
    </Sc>
  );
};

// 2) 3D is in many fields
export const P3Fields: React.FC<{b?: B}> = ({b = {}}) => {
  const many = at(b, 'many', 40);
  const fields = [['🏛️', 'عمارة'], ['🎮', 'ألعاب'], ['🎬', 'أفلام'], ['📺', 'إعلانات'], ['🖼️', 'ديزاين']];
  return (
    <Sc>
      <In at={0} x={540} y={420}><H t="الـ 3D داخل في مجالات كتير جدًا" size={58} color="#fff" /></In>
      <div style={{position: 'absolute', left: 140, top: 520}}><Spinner3D w={800} h={520} color={ORANGE} /></div>
      {fields.map(([e, t], i) => (
        <In key={t} at={many + i * 4} x={i < 3 ? 200 + i * 340 : 370 + (i - 3) * 340} y={i < 3 ? 1110 : 1250} slide={40}>
          <div style={{display: 'flex', alignItems: 'center', gap: 12, background: '#fff', borderRadius: 40, padding: '10px 28px', direction: 'rtl', boxShadow: '0 12px 24px rgba(0,0,0,0.25)'}}>
            <span style={{fontSize: 54}}>{e}</span><span style={{fontFamily: AR, fontWeight: 900, fontSize: 46, color: C.bg1}}>{t}</span>
          </div>
        </In>
      ))}
    </Sc>
  );
};

// 3) the SAME principles in every 3D program: one model goes modeling -> material -> lighting -> rigging -> animation;
//    learn one program -> moving to another is easy
export const P3Shared: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const move = at(b, 'move', 60);
  const steps = ['Modeling', 'Materials', 'Lighting', 'Rigging', 'Animation'];
  const stage = Math.min(4, Math.floor(Math.max(0, f - 6) / Math.max(8, (move - 6) / 5)));
  const hop = lin(f, move, move + 26);
  return (
    <Sc>
      <In at={0} x={540} y={420}><H t="نفس المبادئ في أغلب البرامج" size={58} color="#fff" /></In>
      <div style={{position: 'absolute', left: 190, top: 480}}><Principles3D w={700} h={560} stage={stage} /></div>
      <div style={{position: 'absolute', top: 1030, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 12, direction: 'ltr'}}>
        {steps.map((s, i) => (
          <div key={s} style={{fontFamily: EN, fontWeight: 700, fontSize: 30, padding: '8px 16px', borderRadius: 24, color: i <= stage ? C.bg1 : '#9CC3C0',
            background: i <= stage ? YEL : 'rgba(255,255,255,0.08)', transform: `scale(${i === stage ? 1.12 : 1})`}}>{s}</div>
        ))}
      </div>
      {f >= move ? (
        <div style={{position: 'absolute', top: 1120, left: 0, right: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 40, direction: 'ltr', opacity: lin(f, move, move + 8)}}>
          <Img src={logo('blender.png')} style={{width: 120, height: 120, objectFit: 'contain'}} />
          <div style={{position: 'relative', width: 260, height: 80}}>
            <svg width={260} height={80}><path d="M 10 60 Q 130 -20 250 60" stroke={YEL} strokeWidth={6} fill="none" strokeDasharray="12 10" /></svg>
            <div style={{position: 'absolute', left: 10 + 220 * hop - 20, top: 60 - 70 * Math.sin(Math.PI * hop) - 20, fontSize: 40}}>🧑‍🎓</div>
          </div>
          <Img src={logo('maya.jpg')} style={{width: 120, height: 120, objectFit: 'contain', borderRadius: 8}} />
        </div>
      ) : null}
      {f >= move ? <In at={move + 10} x={540} y={1290}><Pill text="اتعلمت برنامج؟ تنتقل لغيره بسهولة" bg={YEL} ink={C.bg1} size={42} /></In> : null}
    </Sc>
  );
};

// 4) "we explained the 3D principles in other videos" -> his هو ايه episode tiles 13..21 (link to the series)
export const P3Huwa: React.FC = () => {
  const tiles = ['Modeling', 'Materials & Shaders', 'Lighting', 'Sculpting', 'Rendering', 'Rigging', 'Animating', '2D & 3D Physics', '3D Simulations'];
  return (
    <Sc>
      <In at={0} x={540} y={430}><H t="شرحناها في سلسلة" size={56} color="#fff" /></In>
      <In at={2} x={540} y={530}><HuwaLogo h={120} /></In>
      {tiles.map((t, i) => (
        <In key={t} at={6 + i * 2} x={210 + (i % 3) * 330} y={720 + Math.floor(i / 3) * 190}>
          <div style={{width: 300, height: 160, background: '#ECECEF', borderRadius: 10, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 14px', boxSizing: 'border-box', boxShadow: '0 10px 20px rgba(0,0,0,0.3)'}}>
            <div style={{textAlign: 'center', flex: 1}}>
              <div style={{width: 42, height: 42, borderRadius: 21, background: '#1E1E24', color: '#F7931E', fontFamily: EN, fontWeight: 800, fontSize: 24, lineHeight: '42px', margin: '0 auto 4px'}}>{13 + i}</div>
              <div style={{fontFamily: EN, fontWeight: 700, fontSize: 24, color: '#1E1E24', lineHeight: 1.1}}>{t}</div>
            </div>
            <HuwaLogo h={110} />
          </div>
        </In>
      ))}
    </Sc>
  );
};

// 5) the four programs: any of them does what you want, but each one is better at something
export const P3List: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const any = at(b, 'any', 100), each = at(b, 'each', 170);
  return (
    <Sc>
      <In at={0} x={540} y={430}><H t="3D" en size={90} color={YEL} /></In>
      <div style={{position: 'absolute', left: 150, top: 540, borderLeft: '4px solid #fff', paddingLeft: 40, display: 'flex', flexDirection: 'column', gap: 34}}>
        {PROGS.map((p, i) => (
          <div key={p.k} style={{opacity: lin(f, 6 + i * 6, 14 + i * 6), transform: `translateX(${(1 - lin(f, 6 + i * 6, 16 + i * 6)) * -60}px)`}}>
            <Row p={p} tag={f >= each ? '؟' : f >= any ? '✓' : undefined} />
          </div>
        ))}
      </div>
      <In at={any} out={each - 4} x={540} y={1310}><Pill text="أي واحد منهم يعمل اللي انت عايزه" bg={YEL} ink={C.bg1} size={42} /></In>
      <In at={each} x={540} y={1310}><Pill text="بس كل برنامج مميز في حاجة" bg={ORANGE} ink="#fff" size={44} /></In>
    </Sc>
  );
};

// 6) 3ds Max: modeling, architecture, interior design
export const P3Max: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const arch = at(b, 'arch', 110), inter = at(b, 'interior', 140);
  return (
    <Sc>
      <In at={0} x={540} y={420}><Row p={PROGS[1]} hi /></In>
      <In at={at(b, 'model', 90)} x={540} y={540}><Pill text="Modeling" font={EN} dir="ltr" bg={YEL} ink={C.bg1} size={40} /></In>
      {f < inter ? (
        <div style={{position: 'absolute', left: 90, top: 600, opacity: lin(f, 2, 10)}}><Building3D w={900} h={640} t0={4} /></div>
      ) : (
        <div style={{position: 'absolute', left: 90, top: 600, opacity: lin(f, inter, inter + 8)}}><Room3D w={900} h={640} /></div>
      )}
      <In at={arch} out={inter - 2} x={540} y={1280}><Pill text="🏛️ العمارة" size={46} /></In>
      <In at={inter} x={540} y={1280}><Pill text="🛋️ التصميم الداخلي" size={46} /></In>
    </Sc>
  );
};

// 7) Maya: animation; used at Disney; Disney's Maya ≠ the Maya you buy (many plugins + their own software)
export const P3Maya: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const dis = at(b, 'disney', 120), diff = at(b, 'diff', 180), plug = at(b, 'plugins', 260), own = at(b, 'own', 330);
  const second = f >= diff;
  const plugins = ['Plugin', 'Plugin', 'Plugin', 'Plugin', 'أدواتهم الخاصة'];
  return (
    <Sc>
      <In at={0} x={540} y={420}><Row p={PROGS[0]} hi /></In>
      {!second ? (
        <>
          <In at={at(b, 'anim', 40)} x={540} y={540}><Pill text="التحريك (Animation)" bg={YEL} ink={C.bg1} size={40} /></In>
          <div style={{position: 'absolute', left: 90, top: 600}}><BouncingBall3D w={900} h={580} /></div>
          <In at={dis} x={540} y={1260}><Pill text="✨ بيستخدم في ديزني" bg="#fff" ink={C.bg1} size={48} /></In>
        </>
      ) : (
        <>
          {[{t: 'Maya بتاعة ديزني', x: 290, rich: true}, {t: 'Maya اللي هتشتريها', x: 790}].map((c, i) => (
            <In key={i} at={diff + i * 6} x={c.x} y={860}>
              <div style={{width: 420, textAlign: 'center'}}>
                <div style={{display: 'flex', flexDirection: 'column-reverse', alignItems: 'center', gap: 8, minHeight: 470, justifyContent: 'flex-start'}}>
                  <Img src={logo('maya.jpg')} style={{width: 120, height: 120, borderRadius: 8}} />
                  {c.rich ? plugins.map((pl, k) => {
                    const t0 = k < 4 ? plug + k * 5 : own;
                    return f >= t0 ? <div key={k} style={{width: 300 - k * 10, padding: '10px 0', borderRadius: 14, background: k < 4 ? ORANGE : YEL, color: k < 4 ? '#fff' : C.bg1,
                      fontFamily: k < 4 ? EN : AR, fontWeight: 800, fontSize: 30, transform: `scale(${spr(f, 30, t0)})`}}>{pl}</div> : null;
                  }) : null}
                </div>
                <div style={{marginTop: 14, fontFamily: AR, fontWeight: 900, fontSize: 40, color: '#fff', direction: 'rtl'}}>{c.t}</div>
              </div>
            </In>
          ))}
          <In at={diff + 10} x={540} y={760}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 90, color: YEL}}>≠</div></In>
        </>
      )}
    </Sc>
  );
};

// 8) Blender: open source + free, general purpose (3D + video editing + 2D animation + compositing)
export const P3Blender: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const free = at(b, 'free', 60), gen = at(b, 'general', 110);
  const uses = [{e: '🧊', t: '3D', k: 'd3'}, {e: '🎞️', t: 'مونتاج', k: 'edit'}, {e: '✏️', t: '2D Animation', k: 'anim2d'}, {e: '🧩', t: 'كمبوزيتنج', k: 'comp'}];
  return (
    <Sc>
      <In at={0} x={540} y={420}><Row p={PROGS[2]} hi /></In>
      <In at={free} x={540} y={550}><Pill text="Open Source  +  Free" font={EN} dir="ltr" bg="#7DDB9A" ink={C.bg1} size={44} /></In>
      <div style={{position: 'absolute', left: 290, top: 640}}><Spinner3D w={500} h={500} color="#E87D0D" /></div>
      {f >= gen ? <In at={gen} x={540} y={1210}><Pill text="General Purpose" font={EN} dir="ltr" bg={YEL} ink={C.bg1} size={40} /></In> : null}
      {uses.map((u, i) => {
        const t0 = at(b, u.k, gen + 10 + i * 20);
        const [x, y] = [[250, 720], [830, 720], [250, 1040], [830, 1040]][i];
        return (
          <In key={u.k} at={t0} x={x} y={y}>
            <div style={{background: '#fff', borderRadius: 30, padding: '10px 22px', display: 'flex', alignItems: 'center', gap: 10, boxShadow: '0 12px 24px rgba(0,0,0,0.3)', direction: 'rtl'}}>
              <span style={{fontSize: 46}}>{u.e}</span><span style={{fontFamily: AR, fontWeight: 900, fontSize: 38, color: C.bg1, whiteSpace: 'nowrap'}}>{u.t}</span>
            </div>
          </In>
        );
      })}
    </Sc>
  );
};

// 9) Cinema 4D: in Aly's opinion the easiest 3D program to start with; used a lot in 3D motion graphics
export const P3C4d: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const op = at(b, 'opinion', 70), easy = at(b, 'easy', 90), mg = at(b, 'mg', 230);
  return (
    <Sc>
      <In at={0} x={540} y={420}><Row p={PROGS[3]} hi /></In>
      {f < mg ? (
        <>
          <In at={op} x={540} y={600}><Pill text="💬 رأي علي" bg="#fff" ink={C.bg1} size={40} /></In>
          <In at={easy} x={540} y={760}><H t="من أسهل برامج الـ 3D" size={64} color={YEL} /></In>
          <In at={easy + 6} x={540} y={860}><H t="تبدأ تتعلم فيها" size={56} color="#fff" /></In>
          <div style={{position: 'absolute', left: 240, top: 980, width: 600, height: 40, borderRadius: 20, background: 'rgba(255,255,255,0.12)', overflow: 'hidden', opacity: lin(f, easy, easy + 8)}}>
            <div style={{width: `${92 * lin(f, easy + 6, easy + 40)}%`, height: '100%', background: `linear-gradient(90deg, #7DDB9A, ${YEL})`, borderRadius: 20}} />
          </div>
          <In at={easy + 20} x={540} y={1080}><div style={{fontFamily: AR, fontWeight: 800, fontSize: 36, color: '#CFE3E1'}}>سهولة البداية</div></In>
        </>
      ) : (
        <>
          <div style={{position: 'absolute', left: 90, top: 520, opacity: lin(f, mg, mg + 8)}}><Cloner3D w={900} h={700} /></div>
          <In at={mg} x={540} y={1280}><Pill text="3D Motion Graphics" font={EN} dir="ltr" bg={YEL} ink={C.bg1} size={46} /></In>
        </>
      )}
    </Sc>
  );
};

export const progScenes: Record<string, React.FC<any>> = {
  p3_branch: P3Branch, p3_fields: P3Fields, p3_shared: P3Shared, p3_huwa: P3Huwa, p3_list: P3List, p3_max: P3Max, p3_maya: P3Maya,
  p3_blender: P3Blender, p3_c4d: P3C4d,
};
