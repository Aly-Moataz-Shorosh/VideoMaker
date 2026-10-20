import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Base} from '../blocks/Base';
import {enter, lerp} from '../blocks/anim';
import {Backdrop, clamp, Title} from './Board';
import {E, Grain, Hi, Sticker, stickerBorder, Tape} from './kit';

// Full-screen boards for the cs episode "QA / Software Testing" (guest Aiman Ismail, 2026-10-20).
// Same calm Backdrop + paper Title as ep01. Real objects = Fluent 3D emoji (public/fluent) + real logos (public/logos, ISTQB
// badges from istqb.org). Every beat prop = frames from the cue start (placed on the speaker's words by make_plan.py).

const useF = () => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const pop = (at: number) => (frame < at ? 0 : enter(frame, fps, at));
  return {frame, fps, width, height, dur: durationInFrames, pop};
};
const fl = (n: string) => staticFile(`fluent/${n}.png`);

export const Emo: React.FC<{n: string; s: number; style?: React.CSSProperties}> = ({n, s, style}) => (
  <Img src={fl(n)} style={{width: s, height: s, filter: 'drop-shadow(0 10px 14px rgba(0,0,0,.45))', ...style}} />
);

// absolutely placed, centred on (x, y), pops in at `at`
const Pop: React.FC<{x: number; y: number; at: number; rot?: number; children: React.ReactNode; from?: number}> = ({x, y, at, rot = 0, children, from = 40}) => {
  const {pop, frame} = useF();
  if (frame < at) return null;
  const p = pop(at);
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%, -50%) translateY(${lerp(p, from, 0)}px) scale(${lerp(p, 0.4, 1)}) rotate(${rot * p}deg)`,
      opacity: Math.min(1, p * 1.6)}}>{children}</div>
  );
};

const Paper: React.FC<{w: number; h?: number; blue?: boolean; children: React.ReactNode; style?: React.CSSProperties; tape?: boolean}> = ({w, h, blue, children, style, tape = true}) => (
  <div style={{position: 'relative', width: w, height: h, background: blue ? E.bluePaper : E.paper, borderRadius: 10, ...stickerBorder(7),
    padding: '18px 24px', boxSizing: 'border-box', color: E.ink, ...style}}>
    <Grain opacity={0.28} seed={47} />
    <div style={{position: 'relative'}}>{children}</div>
    {tape ? <Tape w={120} rot={-6} style={{top: -24, left: w / 2 - 60}} /> : null}
  </div>
);

const Label: React.FC<{text: string; size?: number; color?: string; hi?: string; style?: React.CSSProperties}> = ({text, size = 44, color = E.white, hi = E.mustard, style}) => (
  <div style={{fontSize: size, fontWeight: 900, color, textAlign: 'center', whiteSpace: 'nowrap', textShadow: '0 4px 12px rgba(0,0,0,.5)', ...style}}><Hi text={text} color={hi} /></div>
);

export const LogoTile: React.FC<{src: string; s: number; pad?: number}> = ({src, s, pad = 0.18}) => (
  <div style={{width: s, height: s, background: E.white, borderRadius: s * 0.2, display: 'flex', alignItems: 'center', justifyContent: 'center',
    boxShadow: '0 12px 26px rgba(0,0,0,.5)', outline: '2px solid rgba(20,20,30,.4)'}}>
    <Img src={staticFile(src)} style={{width: s * (1 - 2 * pad), height: s * (1 - 2 * pad), objectFit: 'contain'}} />
  </div>
);

const Chip: React.FC<{text: string; bg?: string; size?: number; rot?: number}> = ({text, bg = E.blue, size = 36, rot = 0}) => (
  <div style={{background: bg, color: E.ink, fontWeight: 900, fontSize: size, padding: '6px 24px', borderRadius: 40, border: `4px solid ${E.white}`,
    whiteSpace: 'nowrap', boxShadow: '0 8px 16px rgba(0,0,0,.4)', transform: `rotate(${rot}deg)`}}><Hi text={text} color={E.white} /></div>
);

// round stamp ✓ / ✗ drawn (vector)
const Mark: React.FC<{ok: boolean; s?: number}> = ({ok, s = 70}) => <Sticker name={ok ? 'check' : 'cross'} size={s} />;

// ============ 1) Testing = ? (two sides: bugs? / as requested?) ============
export const qaWhatSchema = z.object({
  title: z.string().default('Testing *يعني إيه*؟'),
  appAt: z.number().default(8),
  bugsAt: z.number().default(60), bugsText: z.string().default('فيه *مشاكل*؟'),
  reqAt: z.number().default(120), reqText: z.string().default('بيعمل *المطلوب*؟'),
  req: z.array(z.object({text: z.string(), at: z.number()})).default([]),
  previewBg: z.string().default(''),
});
export const QaWhat: React.FC<z.infer<typeof qaWhatSchema>> = ({title, appAt, bugsAt, bugsText, reqAt, reqText, req, previewBg}) => {
  const {frame, width: W, height: H, pop} = useF();
  const scan = frame >= bugsAt ? (frame - bugsAt) / 70 : 0;
  const bugs = [[-170, -60, 0], [120, 40, 14], [-40, 110, 28]];
  return (
    <Base previewBg={previewBg}>
      <Backdrop><AbsoluteFill style={{direction: 'rtl'}}>
        <Title text={title} />
        {/* the software: laptop + phone + web */}
        <Pop x={W / 2} y={H * 0.52} at={appAt}>
          <div style={{position: 'relative', width: 520, height: 400}}>
            <Emo n="laptop" s={250} style={{position: "absolute", left: 135, top: 60}} />
            <Emo n="mobile_phone" s={170} style={{position: 'absolute', left: 0, top: 190}} />
            <Emo n="globe_with_meridians" s={150} style={{position: 'absolute', left: 380, top: 210}} />
            <Label text="*Software*" size={46} style={{position: 'absolute', top: 360, left: 0, right: 0}} />
            {/* bugs found on it, each circled in red */}
            {bugs.map(([x, y, d], i) => frame >= bugsAt + 20 + d ? (
              <div key={i} style={{position: 'absolute', left: 230 + x, top: 150 + y, transform: `scale(${pop(bugsAt + 20 + d)})`}}>
                <Emo n="lady_beetle" s={74} />
                <svg width={110} height={110} style={{position: 'absolute', left: -18, top: -18}}>
                  <circle cx={55} cy={55} r={48} fill="none" stroke={E.orange} strokeWidth={7} strokeDasharray={302}
                    strokeDashoffset={302 * (1 - interpolate(frame, [bugsAt + 30 + d, bugsAt + 42 + d], [0, 1], clamp))} />
                </svg>
              </div>
            ) : null)}
          </div>
        </Pop>
        {frame >= bugsAt && frame < bugsAt + 70 ? (
          <Emo n="magnifying_glass_tilted_left" s={170} style={{position: 'absolute', left: W / 2 - 200 + Math.sin(scan * 6) * 180, top: H * 0.38 + Math.cos(scan * 5) * 70}} />
        ) : null}
        {/* right panel (first): bugs? */}
        <Pop x={W - 330} y={H * 0.5} at={bugsAt} rot={2}>
          <Paper w={460}>
            <div style={{display: 'flex', alignItems: 'center', gap: 18, justifyContent: 'center'}}>
              <Emo n="bug" s={110} style={{filter: 'none'}} />
              <div style={{fontSize: 50, fontWeight: 900}}><Hi text={bugsText} color={E.orange} /></div>
            </div>
            <div style={{fontSize: 36, fontWeight: 800, textAlign: 'center', marginTop: 8, opacity: 0.8}}>Bugs · Issues</div>
          </Paper>
        </Pop>
        {/* left panel: as requested? checklist */}
        <Pop x={330} y={H * 0.5} at={reqAt} rot={-2}>
          <Paper w={500} blue>
            <div style={{display: 'flex', alignItems: 'center', gap: 18, justifyContent: 'center'}}>
              <Emo n="clipboard" s={100} style={{filter: 'none'}} />
              <div style={{fontSize: 48, fontWeight: 900}}><Hi text={reqText} color={E.orange} /></div>
            </div>
            <div style={{fontSize: 34, fontWeight: 800, textAlign: 'center', opacity: 0.8, marginBottom: 6}}>Requirements</div>
            {req.map((r, i) => frame >= r.at ? (
              <div key={i} style={{display: 'flex', alignItems: 'center', gap: 14, fontSize: 38, fontWeight: 800, marginTop: 8, opacity: Math.min(1, pop(r.at) * 1.5)}}>
                <div style={{transform: `scale(${pop(r.at + 8)})`}}><Mark ok s={50} /></div><Hi text={r.text} color={E.orange} />
              </div>
            ) : null)}
          </Paper>
        </Pop>
      </AbsoluteFill></Backdrop>
    </Base>
  );
};

// ============ 2) one requirement, three understandings ============
export const qaReqSchema = z.object({
  title: z.string().default('*Requirement* واحد… وكل واحد فهمه بطريقة'),
  req: z.string().default('عايز زرار *حفظ*'),
  people: z.array(z.object({emo: z.string(), label: z.string(), shape: z.enum(['circle', 'square', 'tri']), at: z.number()})).default([]),
  bugAt: z.number().default(200), bugText: z.string().default('ودي برضو *Bugs*'),
  previewBg: z.string().default(''),
});
const ShapeIcon: React.FC<{shape: string; c: string}> = ({shape, c}) => (
  <svg width={120} height={120} viewBox="0 0 100 100">
    {shape === 'circle' ? <circle cx={50} cy={50} r={38} fill={c} stroke={E.ink} strokeWidth={5} /> : null}
    {shape === 'square' ? <rect x={14} y={14} width={72} height={72} rx={8} fill={c} stroke={E.ink} strokeWidth={5} /> : null}
    {shape === 'tri' ? <path d="M50 10 L92 86 L8 86Z" fill={c} stroke={E.ink} strokeWidth={5} strokeLinejoin="round" /> : null}
  </svg>
);
export const QaReq: React.FC<z.infer<typeof qaReqSchema>> = ({title, req, people, bugAt, bugText, previewBg}) => {
  const {frame, width: W, height: H} = useF();
  const n = people.length || 1;
  return (
    <Base previewBg={previewBg}>
      <Backdrop><AbsoluteFill style={{direction: 'rtl'}}>
        <Title text={title} />
        <Pop x={W / 2} y={300} at={6}>
          <Paper w={560}><div style={{fontSize: 52, fontWeight: 900, textAlign: 'center'}}><Hi text={req} color={E.orange} /></div></Paper>
        </Pop>
        {people.map((p, i) => {
          const x = W - (W / n) * (i + 0.5); // RTL: first on the right
          const cols = [E.blue, E.orange, E.olive];
          return (
            <React.Fragment key={i}>
              <svg style={{position: 'absolute', left: 0, top: 0, width: W, height: H, pointerEvents: 'none'}}>
                {frame >= p.at ? <path d={`M${W / 2} 330 Q${(W / 2 + x) / 2} 420 ${x} 470`} stroke={E.white} strokeOpacity={0.5} strokeWidth={5} strokeDasharray="14 12" fill="none"
                  pathLength={1} style={{strokeDashoffset: 0}} /> : null}
              </svg>
              <Pop x={x} y={560} at={p.at}>
                <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
                  <div style={{background: E.white, borderRadius: 40, padding: 14, ...stickerBorder(4)}}><ShapeIcon shape={p.shape} c={cols[i % 3]} /></div>
                  <div style={{width: 0, height: 0, borderLeft: '16px solid transparent', borderRight: '16px solid transparent', borderTop: `22px solid ${E.white}`}} />
                  <Emo n={p.emo} s={200} style={{marginTop: 6}} />
                  <Label text={p.label} size={44} />
                </div>
              </Pop>
            </React.Fragment>
          );
        })}
        <Pop x={W / 2} y={H - 110} at={bugAt}>
          <div style={{display: 'flex', alignItems: 'center', gap: 16}}>
            <Emo n="bug" s={100} /><Chip text={bugText} bg={E.orange} size={46} />
          </div>
        </Pop>
      </AbsoluteFill></Backdrop>
    </Base>
  );
};

// ============ 3) developer vs tester: one angle vs many angles (three.js cube) ============
export const qaEyesSchema = z.object({
  title: z.string().default('نفس الحاجة… *بعين مختلفة*'),
  devAt: z.number().default(10), devText: z.string().default('إزاي *تشتغل*؟'),
  testAt: z.number().default(80), testText: z.string().default('إزاي *متشتغلش*؟'),
  anglesAt: z.number().default(160), anglesText: z.string().default('أكتر من *زاوية*'),
  previewBg: z.string().default(''),
});
// cube drawn as SVG (no WebGL): a real 3D box seen a little from above that turns around its vertical axis.
// Face 0 = ✓ (the side the developer looks at); the other faces = bugs the tester finds by turning it.
const IsoCube: React.FC<{t: number; s: number; bugs: boolean}> = ({t, s, bugs}) => {
  const a = t * Math.PI / 2 - Math.PI / 4 + 0.12;     // t = 0 -> face 0 almost frontal, a hint of the next side
  const r = s * 0.62, tilt = 0.32, h = s * 0.9, top = -h / 2;
  const V = [0, 1, 2, 3].map((j) => { const ph = a + Math.PI / 4 + j * Math.PI / 2; return {x: r * Math.sin(ph), z: r * Math.cos(ph)}; });
  const yT = (v: {z: number}) => top + v.z * tilt;      // nearer (z > 0) = lower on screen
  const faces = [0, 1, 2, 3].map((k) => ({k, p: V[k], q: V[(k + 1) % 4], z: (V[k].z + V[(k + 1) % 4].z) / 2}))
    .filter((f) => f.z > 0.5).sort((x, y) => x.z - y.z);
  return (
    <svg width={s * 1.8} height={s * 1.7} viewBox={`${-s * 0.9} ${-s * 0.85} ${s * 1.8} ${s * 1.7}`}>
      <ellipse cx={0} cy={h / 2 + r * tilt + 18} rx={r * 1.1} ry={r * 0.22} fill="rgba(0,0,0,.35)" />
      {faces.map((f) => {
        const isBug = bugs && f.k !== 0, w = Math.abs(f.q.x - f.p.x), light = 0.72 + 0.4 * (f.z / r);
        const cx = (f.p.x + f.q.x) / 2, cy = (yT(f.p) + yT(f.q)) / 2 + h / 2;
        return (
          <g key={f.k}>
            <path d={`M${f.p.x} ${yT(f.p)} L${f.q.x} ${yT(f.q)} L${f.q.x} ${yT(f.q) + h} L${f.p.x} ${yT(f.p) + h}Z`}
              fill={f.k === 0 ? E.olive : isBug ? E.orange : E.blue} stroke={E.ink} strokeWidth={5} strokeLinejoin="round" style={{filter: `brightness(${light})`}} />
            {w > s * 0.3 ? (
              <text x={cx} y={cy + s * 0.11} textAnchor="middle" fontSize={s * 0.3 * Math.min(1, w / (s * 0.8))} fontWeight={900} fill={E.white}
                fontFamily="Montserrat" transform={`translate(${cx} 0) scale(${Math.min(1, w / (s * 0.8))} 1) translate(${-cx} 0)`}>{f.k === 0 ? '✓' : isBug ? 'BUG' : '?'}</text>
            ) : null}
          </g>
        );
      })}
      <path d={`M${V.map((v) => `${v.x} ${yT(v)}`).join(' L')}Z`} fill={E.paper} stroke={E.ink} strokeWidth={5} strokeLinejoin="round" />
    </svg>
  );
};
export const QaEyes: React.FC<z.infer<typeof qaEyesSchema>> = ({title, devAt, devText, testAt, testText, anglesAt, anglesText, previewBg}) => {
  const {frame, width: W, height: H} = useF();
  const FRONT = -0.5764; // t where face 0 (✓) faces the camera
  const turn = FRONT + (frame < anglesAt ? 0 : (frame - anglesAt) / 45); // keeps turning
  return (
    <Base previewBg={previewBg}>
      <Backdrop><AbsoluteFill style={{direction: 'rtl'}}>
        <Title text={title} />
        {/* RTL: developer on the right, tester on the left */}
        <Pop x={W * 0.73} y={H * 0.55} at={devAt}>
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
            <IsoCube t={FRONT} s={190} bugs={false} />
            <div style={{display: 'flex', alignItems: 'center', gap: 14, marginTop: -10}}><Emo n="eye" s={90} /><Label text="Developer" size={50} /></div>
            <Label text={devText} size={56} />
          </div>
        </Pop>
        <Pop x={W * 0.27} y={H * 0.55} at={testAt}>
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
            <IsoCube t={turn} s={190} bugs />
            <div style={{display: 'flex', alignItems: 'center', gap: 14, marginTop: -10}}><Emo n="eyes" s={90} /><Label text="Tester" size={50} /></div>
            <Label text={testText} size={56} hi={E.orange} />
          </div>
        </Pop>
        <Pop x={W / 2} y={H - 90} at={anglesAt}><Chip text={anglesText} bg={E.mustard} size={44} /></Pop>
        <div style={{position: 'absolute', left: W / 2 - 3, top: 250, width: 6, height: H - 420, background: 'rgba(255,255,255,.15)', borderRadius: 3}} />
      </AbsoluteFill></Backdrop>
    </Base>
  );
};

// ============ 4) types of testing (tree) ============
const node = z.object({emo: z.string(), label: z.string(), sub: z.string().default(''), at: z.number(), logo: z.string().default('')});
export const qaTypesSchema = z.object({
  title: z.string().default('أنواع الـ*Testing*'),
  funcAt: z.number().default(10), nonAt: z.number().default(60),
  func: z.array(node).default([]), non: z.array(node).default([]),
  previewBg: z.string().default(''),
});
export const QaTypes: React.FC<z.infer<typeof qaTypesSchema>> = ({title, funcAt, nonAt, func, non, previewBg}) => {
  const {frame, width: W, height: H} = useF();
  const branch = (x: number, at: number, name: string, sub: string, kids: z.infer<typeof node>[], col: string) => (
    <>
      <svg style={{position: 'absolute', left: 0, top: 0, width: W, height: H}}>
        {frame >= at ? <path d={`M${W / 2} 240 Q${W / 2} 300 ${x} 330`} stroke={E.white} strokeOpacity={0.45} strokeWidth={6} fill="none" /> : null}
        {kids.map((k, i) => frame >= k.at ? (
          <path key={i} d={`M${x} 450 L${x + (i - (kids.length - 1) / 2) * 270} 600`} stroke={E.white} strokeOpacity={0.4} strokeWidth={5} fill="none" />
        ) : null)}
      </svg>
      <Pop x={x} y={390} at={at}>
        <div style={{background: col, color: E.ink, borderRadius: 16, padding: '12px 34px', ...stickerBorder(6), textAlign: 'center'}}>
          <div style={{fontSize: 54, fontWeight: 900, fontFamily: 'Montserrat'}}>{name}</div>
          <div style={{fontSize: 34, fontWeight: 800}}><Hi text={sub} color={E.white} /></div>
        </div>
      </Pop>
      {kids.map((k, i) => (
        <Pop key={i} x={x + (i - (kids.length - 1) / 2) * 270} y={730} at={k.at} rot={i % 2 ? 3 : -3}>
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', width: 250}}>
            {k.logo ? <LogoTile src={k.logo} s={140} /> : <Emo n={k.emo} s={150} />}
            <Label text={k.label} size={44} />
            {k.sub ? <div style={{fontSize: 30, fontWeight: 700, color: E.mustard, textAlign: 'center'}}>{k.sub}</div> : null}
          </div>
        </Pop>
      ))}
    </>
  );
  return (
    <Base previewBg={previewBg}>
      <Backdrop><AbsoluteFill style={{direction: 'rtl'}}>
        <Title text={title} />
        {branch(W * 0.73, funcAt, 'Functional', 'الفيتشر *شغالة*؟', func, E.olive)}
        {branch(W * 0.27, nonAt, 'Non-Functional', 'سريع؟ آمن؟ *سهل*؟', non, E.blue)}
      </AbsoluteFill></Backdrop>
    </Base>
  );
};

// ============ 5) login example: manual cases -> automation script -> report ============
const lcase = z.object({email: z.string(), pass: z.string(), ok: z.boolean(), msg: z.string(), at: z.number()});
export const qaLoginSchema = z.object({
  title: z.string().default('مثال: *Login*'),
  manualAt: z.number().default(10), cases: z.array(lcase).default([]),
  autoAt: z.number().default(200), code: z.array(z.string()).default([]),
  repeatAt: z.number().default(300), reportAt: z.number().default(360),
  previewBg: z.string().default(''),
});
export const QaLogin: React.FC<z.infer<typeof qaLoginSchema>> = ({title, manualAt, cases, autoAt, code, repeatAt, reportAt, previewBg}) => {
  const {frame, fps, width: W, height: H, pop} = useF();
  const auto = frame >= autoAt;
  // which case is on the form now: manual = by its beat; automation = cycles fast after repeatAt
  let ci = -1, local = 0;
  if (!auto) { for (let i = 0; i < cases.length; i++) if (frame >= cases[i].at) { ci = i; local = frame - cases[i].at; } }
  else if (frame >= repeatAt) { const per = 9; ci = Math.floor((frame - repeatAt) / per) % Math.max(1, cases.length); local = ((frame - repeatAt) % per) * 4; }
  const c = ci >= 0 ? cases[ci] : null;
  const typed = (s: string, d: number) => s.slice(0, Math.max(0, Math.floor((local - d) / 1.6)));
  const resShow = c && local > 26;
  const runs = frame >= repeatAt ? Math.min(100, Math.floor((frame - repeatAt) / 2.2) + 1) : 0;
  const fx = W * 0.66, fy = H * 0.55;
  return (
    <Base previewBg={previewBg}>
      <Backdrop><AbsoluteFill style={{direction: 'rtl'}}>
        <Title text={title} />
        {/* the browser with the login form */}
        <Pop x={fx} y={fy} at={4}>
          <div style={{width: 640, background: '#F6F4EF', borderRadius: 16, overflow: 'hidden', direction: 'ltr', ...stickerBorder(6)}}>
            <div style={{height: 46, background: '#D9D4C8', display: 'flex', alignItems: 'center', gap: 10, padding: '0 16px'}}>
              {[E.orange, E.mustard, E.olive].map((k, i) => <div key={i} style={{width: 16, height: 16, borderRadius: 8, background: k}} />)}
              <div style={{flex: 1, height: 26, background: '#fff', borderRadius: 13, marginLeft: 10, fontSize: 18, color: '#777', padding: '2px 14px', fontFamily: 'Montserrat'}}>myapp.com/login</div>
            </div>
            <div style={{padding: '30px 50px 40px', fontFamily: 'Montserrat', color: E.ink}}>
              <div style={{fontSize: 44, fontWeight: 800, textAlign: 'center', marginBottom: 20}}>Login</div>
              {[['Email', c ? typed(c.email, 0) : ''], ['Password', c ? '•'.repeat(typed(c.pass, 12).length) : '']].map(([k, v], i) => (
                <div key={i} style={{marginBottom: 16}}>
                  <div style={{fontSize: 22, fontWeight: 700, color: '#666'}}>{k}</div>
                  <div style={{height: 54, border: '3px solid #BDB6A8', borderRadius: 10, background: '#fff', fontSize: 28, padding: '8px 14px', boxSizing: 'border-box'}}>{v}</div>
                </div>
              ))}
              <div style={{height: 60, borderRadius: 12, background: E.blue, color: '#fff', fontSize: 30, fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center',
                transform: `scale(${c && local > 22 && local < 27 ? 0.95 : 1})`}}>Login</div>
              <div style={{height: 50, marginTop: 14, borderRadius: 10, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 26, fontWeight: 800,
                background: resShow ? (c!.ok ? '#DDEBC8' : '#F6D3C4') : 'transparent', color: resShow ? (c!.ok ? '#3D5A1E' : '#9A3412') : 'transparent'}}>{resShow ? c!.msg : '.'}</div>
            </div>
          </div>
        </Pop>
        {/* manual: hand + the list of tried cases */}
        {!auto ? (
          <>
            <Pop x={W * 0.25} y={250} at={manualAt}><div style={{display: 'flex', alignItems: 'center', gap: 16}}><Emo n="backhand_index_pointing_up" s={100} /><Chip text="*Manual*: بإيدك وبعينك" bg={E.olive} size={44} /></div></Pop>
            {cases.map((k, i) => frame >= k.at ? (
              <div key={i} style={{position: 'absolute', left: 90, top: 360 + i * 120, width: 700, display: 'flex', alignItems: 'center', gap: 18, transform: `translateX(${lerp(pop(k.at), -80, 0)}px)`, opacity: pop(k.at)}}>
                <div style={{transform: `scale(${frame >= k.at + 27 ? pop(k.at + 27) : 0})`}}><Mark ok={k.ok} s={64} /></div>
                <div style={{flex: 1, background: E.paper, borderRadius: 10, padding: '10px 20px', fontSize: 30, fontWeight: 800, color: E.ink, direction: 'ltr', fontFamily: 'Montserrat', ...stickerBorder(4)}}>
                  {k.email || '(empty)'} · {k.pass ? '••••' : '(empty)'}
                </div>
              </div>
            ) : null)}
          </>
        ) : (
          <>
            <Pop x={W * 0.25} y={250} at={autoAt}><div style={{display: 'flex', alignItems: 'center', gap: 16}}><Emo n="robot" s={100} /><Chip text="*Automation*: الكود يجرب" bg={E.blue} size={44} /></div></Pop>
            <Pop x={W * 0.25} y={H * 0.56} at={autoAt + 4}>
              <div style={{width: 700, background: '#1A1D26', borderRadius: 14, padding: '22px 26px', direction: 'ltr', fontFamily: 'Consolas, monospace', fontSize: 28, color: '#D8DEE9', ...stickerBorder(5)}}>
                {code.map((l, i) => {
                  const st = autoAt + 8 + i * 12, n = Math.max(0, Math.min(l.length, Math.floor((frame - st) * 1.8)));
                  return <div key={i} style={{whiteSpace: 'pre', minHeight: 38}}><span style={{color: '#7A8194'}}>{i + 1}  </span>{l.slice(0, n)}</div>;
                })}
              </div>
            </Pop>
            {runs ? <div style={{position: 'absolute', left: fx + 250, top: fy - 330, transform: `rotate(6deg) scale(${pop(repeatAt)})`}}><Chip text={`×${runs}`} bg={E.mustard} size={54} /></div> : null}
            {frame >= reportAt ? (
              <Pop x={fx} y={fy} at={reportAt}>
                <Paper w={520}>
                  <div style={{display: 'flex', alignItems: 'center', gap: 14, justifyContent: 'center', fontSize: 48, fontWeight: 900}}><Emo n="bar_chart" s={80} style={{filter: 'none'}} />Report</div>
                  {cases.map((k, i) => (
                    <div key={i} style={{display: 'flex', alignItems: 'center', gap: 14, marginTop: 10, fontSize: 28, fontWeight: 800, direction: 'ltr', fontFamily: 'Montserrat',
                      opacity: frame >= reportAt + 8 + i * 5 ? 1 : 0}}>
                      <Mark ok={k.ok} s={44} />{`Case ${i + 1}`}<span style={{opacity: 0.6, marginLeft: 'auto'}}>{k.ok ? 'pass' : 'pass ✓ (error shown)'}</span>
                    </div>
                  ))}
                </Paper>
              </Pop>
            ) : null}
          </>
        )}
      </AbsoluteFill></Backdrop>
    </Base>
  );
};

// ============ 6) API testing: UI -> API -> Backend ============
export const qaApiSchema = z.object({
  title: z.string().default('*API* Testing'),
  uiAt: z.number().default(10), selAt: z.number().default(30), apiAt: z.number().default(50), postmanAt: z.number().default(90), autoAt: z.number().default(150), libAt: z.number().default(200),
  previewBg: z.string().default(''),
});
export const QaApi: React.FC<z.infer<typeof qaApiSchema>> = ({title, uiAt, selAt, apiAt, postmanAt, autoAt, libAt, previewBg}) => {
  const {frame, width: W, height: H} = useF();
  const xs = [W * 0.2, W * 0.5, W * 0.8], y = H * 0.47;
  const box = (i: number, at: number, emo: string, name: string, sub: string, hl: boolean) => (
    <Pop x={xs[i]} y={y} at={at}>
      <div style={{width: 380, display: 'flex', flexDirection: 'column', alignItems: 'center', background: hl ? 'rgba(232,181,74,.18)' : 'rgba(255,255,255,.06)', borderRadius: 26,
        border: `4px ${hl ? 'solid' : 'dashed'} ${hl ? E.mustard : 'rgba(255,255,255,.3)'}`, padding: '20px 0 16px'}}>
        <Emo n={emo} s={170} />
        <div style={{fontSize: 54, fontWeight: 900, color: E.white, fontFamily: 'Montserrat'}}>{name}</div>
        <div style={{fontSize: 32, fontWeight: 800, color: E.mustard}}>{sub}</div>
      </div>
    </Pop>
  );
  const pkt = (i: number) => {
    const k = ((frame - apiAt) / 40 + i / 3) % 1;
    return <div key={i} style={{position: 'absolute', left: lerp(k, xs[0] + 200, xs[2] - 220), top: y - 14, width: 28, height: 28, borderRadius: 14, background: E.orange, boxShadow: `0 0 18px ${E.orange}`}} />;
  };
  return (
    <Base previewBg={previewBg}>
      <Backdrop><AbsoluteFill style={{direction: 'rtl'}}>
        <Title text={title} />
        {/* left to right like the request flow: browser -> API -> server */}
        <div style={{position: 'absolute', left: xs[0] + 190, top: y - 3, width: xs[2] - xs[0] - 380, height: 6, background: 'rgba(255,255,255,.25)', borderRadius: 3}} />
        {frame >= apiAt ? [0, 1, 2].map(pkt) : null}
        {box(0, uiAt, 'globe_with_meridians', 'UI', 'المتصفح', frame >= uiAt && frame < postmanAt)}
        {box(1, apiAt, 'link', 'API', 'بيكلّم الـBack End', frame >= postmanAt)}
        {box(2, apiAt + 10, 'file_cabinet', 'Back End', 'السيرفر والداتا', false)}
        <Pop x={xs[0]} y={y + 300} at={selAt}><div style={{display: 'flex', alignItems: 'center', gap: 14}}><LogoTile src="logos/selenium_c.svg" s={90} /><Label text="Selenium" size={40} /></div></Pop>
        <Pop x={xs[1]} y={y - 270} at={postmanAt} rot={-3}><div style={{display: 'flex', alignItems: 'center', gap: 14}}><LogoTile src="logos/postman_c.svg" s={110} /><Chip text="*Postman*: جرب كل الاحتمالات" bg={E.olive} size={38} /></div></Pop>
        <Pop x={xs[1]} y={y + 300} at={autoAt}><Chip text="API *Automation*" bg={E.blue} size={42} /></Pop>
        <Pop x={xs[1]} y={y + 390} at={libAt}><Label text="بـ *Libraries* تانية (زي REST Assured)" size={38} /></Pop>
      </AbsoluteFill></Backdrop>
    </Base>
  );
};

// ============ 7) performance + security ============
export const qaPerfSchema = z.object({
  title: z.string().default('*Security* و *Performance*'),
  secAt: z.number().default(10), perfAt: z.number().default(90),
  previewBg: z.string().default(''),
});
export const QaPerf: React.FC<z.infer<typeof qaPerfSchema>> = ({title, secAt, perfAt, previewBg}) => {
  const {frame, width: W, height: H} = useF();
  const load = frame < perfAt ? 0 : Math.min(1, (frame - perfAt) / 90);
  const dots = Math.floor(load * 40);
  return (
    <Base previewBg={previewBg}>
      <Backdrop><AbsoluteFill style={{direction: 'rtl'}}>
        <Title text={title} />
        <Pop x={W * 0.75} y={H * 0.5} at={secAt}>
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
            <Emo n="shield" s={230} />
            <Label text="Security" size={60} />
            <div style={{marginTop: 18}}><Chip text="*Cyber Security*: تخصص لوحده" bg={E.orange} size={38} /></div>
          </div>
        </Pop>
        {frame >= perfAt ? (
          <>
            {Array.from({length: dots}).map((_, i) => {
              const k = ((frame - perfAt) / 18 + (i * 0.137) % 1) % 1;
              return <div key={i} style={{position: 'absolute', left: lerp(k, 80, W * 0.3), top: H * 0.33 + ((i * 53) % 330), width: 16, height: 16, borderRadius: 8, background: E.mustard, opacity: 0.85}} />;
            })}
            <Pop x={W * 0.33} y={H * 0.5} at={perfAt}>
              <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
                <Emo n="desktop_computer" s={200} />
                <svg width={300} height={170} viewBox="0 0 300 170">
                  <path d="M30 150 A120 120 0 0 1 270 150" stroke="rgba(255,255,255,.25)" strokeWidth={22} fill="none" />
                  <path d="M30 150 A120 120 0 0 1 270 150" stroke={load > 0.75 ? E.orange : E.mustard} strokeWidth={22} fill="none" pathLength={1} strokeDasharray={`${load} 1`} />
                  <line x1={150} y1={150} x2={150 + 100 * Math.cos(Math.PI * (1 - load))} y2={150 - 100 * Math.sin(Math.PI * (1 - load))} stroke={E.white} strokeWidth={8} strokeLinecap="round" />
                </svg>
                <Label text="Performance" size={60} />
                <Label text="*Requests* كتير مرة واحدة" size={36} />
              </div>
            </Pop>
          </>
        ) : null}
      </AbsoluteFill></Backdrop>
    </Base>
  );
};

// ============ 8) road to the job ============
const rstep = z.object({emo: z.string().default(''), logo: z.array(z.string()).default([]), pic: z.string().default(''), label: z.string(), sub: z.string().default(''), at: z.number()});
export const qaRoadSchema = z.object({
  title: z.string().default('تبدأ *إزاي*؟'),
  steps: z.array(rstep).default([]),
  previewBg: z.string().default(''),
});
export const QaRoad: React.FC<z.infer<typeof qaRoadSchema>> = ({title, steps, previewBg}) => {
  const {frame, width: W, height: H} = useF();
  const n = steps.length || 1;
  const pt = (i: number) => ({x: W - 200 - i * ((W - 400) / Math.max(1, n - 1)), y: H * (i % 2 ? 0.66 : 0.42)});
  let reached = -1;
  steps.forEach((s, i) => { if (frame >= s.at) reached = i; });
  const d = steps.map((_, i) => { const p = pt(i); return `${i ? 'L' : 'M'}${p.x} ${p.y}`; }).join(' ');
  return (
    <Base previewBg={previewBg}>
      <Backdrop><AbsoluteFill style={{direction: 'rtl'}}>
        <Title text={title} />
        <svg style={{position: 'absolute', left: 0, top: 0, width: W, height: H}}>
          <path d={d} stroke="rgba(255,255,255,.18)" strokeWidth={14} fill="none" strokeLinecap="round" strokeLinejoin="round" strokeDasharray="2 26" />
        </svg>
        {steps.map((s, i) => {
          const p = pt(i);
          return (
            <Pop key={i} x={p.x} y={p.y} at={s.at} rot={i % 2 ? 2 : -2}>
              <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', width: 330, position: 'relative'}}>
                <div style={{position: 'absolute', top: -34, right: 40, width: 62, height: 62, borderRadius: 31, background: i <= reached ? E.orange : E.ink, color: E.white,
                  border: `5px solid ${E.white}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 34, fontWeight: 900, fontFamily: 'Montserrat', zIndex: 2}}>{i + 1}</div>
                <div style={{height: 170, display: 'flex', alignItems: 'center', gap: 10}}>
                  {s.pic ? <Img src={staticFile(s.pic)} style={{width: 160, height: 160, borderRadius: 12, ...stickerBorder(5)}} /> : null}
                  {s.emo ? <Emo n={s.emo} s={160} /> : null}
                  {s.logo.map((l, k) => <LogoTile key={k} src={l} s={s.logo.length > 2 ? 100 : 130} />)}
                </div>
                <Label text={s.label} size={44} />
                {s.sub ? <div style={{fontSize: 30, fontWeight: 700, color: E.mustard, textAlign: 'center'}}><Hi text={s.sub} color={E.white} /></div> : null}
              </div>
            </Pop>
          );
        })}
      </AbsoluteFill></Backdrop>
    </Base>
  );
};

// ============ 9) tester = joker: skills around ============
export const qaJokerSchema = z.object({
  title: z.string().default('الـTester لازم يبقى *جوكر*'),
  skills: z.array(z.object({emo: z.string(), text: z.string(), at: z.number()})).default([]),
  previewBg: z.string().default(''),
});
export const QaJoker: React.FC<z.infer<typeof qaJokerSchema>> = ({title, skills, previewBg}) => {
  const {frame, width: W, height: H} = useF();
  const cx = W / 2, cy = H * 0.56, n = Math.max(1, skills.length);
  return (
    <Base previewBg={previewBg}>
      <Backdrop><AbsoluteFill style={{direction: 'rtl'}}>
        <Title text={title} />
        <Pop x={cx} y={cy} at={4}><Emo n="joker" s={250} style={{transform: `rotate(${Math.sin(frame / 30) * 4}deg)`}} /></Pop>
        {skills.map((s, i) => {
          const a = -Math.PI / 2 + (i / n) * Math.PI * 2;
          const x = cx + Math.cos(a) * 640, y = cy + Math.sin(a) * 300;
          return (
            <React.Fragment key={i}>
              {frame >= s.at ? <svg style={{position: 'absolute', left: 0, top: 0, width: W, height: H}}><line x1={cx} y1={cy} x2={x} y2={y} stroke="rgba(255,255,255,.18)" strokeWidth={4} strokeDasharray="10 10" /></svg> : null}
              <Pop x={x} y={y} at={s.at} rot={i % 2 ? 3 : -3}>
                <div style={{display: 'flex', alignItems: 'center', gap: 12, background: E.paper, borderRadius: 16, padding: '8px 22px 8px 14px', ...stickerBorder(5)}}>
                  <Emo n={s.emo} s={80} style={{filter: 'none'}} />
                  <div style={{fontSize: 38, fontWeight: 900, color: E.ink, whiteSpace: 'nowrap'}}><Hi text={s.text} color={E.orange} /></div>
                </div>
              </Pop>
            </React.Fragment>
          );
        })}
      </AbsoluteFill></Backdrop>
    </Base>
  );
};

// ============ 10) ISTQB certificates ============
export const qaIstqbSchema = z.object({
  title: z.string().default('شهادة *ISTQB*'),
  logo: z.string().default(''),
  certs: z.array(z.object({pic: z.string().default(''), name: z.string(), at: z.number(), his: z.boolean().default(false)})).default([]),
  stampAt: z.number().default(9999), stampText: z.string().default('أيمن *أخدها*'),
  chips: z.array(z.object({text: z.string(), at: z.number()})).default([]),
  previewBg: z.string().default(''),
});
export const QaIstqb: React.FC<z.infer<typeof qaIstqbSchema>> = ({title, logo, certs, stampAt, stampText, chips, previewBg}) => {
  const {frame, width: W, height: H, pop} = useF();
  const n = Math.max(1, certs.length), cw = 300, gap = 60, x0 = W / 2 + ((n - 1) * (cw + gap)) / 2;
  return (
    <Base previewBg={previewBg}>
      <Backdrop><AbsoluteFill style={{direction: 'rtl'}}>
        <Title text={title} />
        {logo ? <Pop x={W / 2} y={265} at={6}><div style={{background: E.white, borderRadius: 18, padding: '12px 30px', ...stickerBorder(4)}}><Img src={staticFile(logo)} style={{height: 110}} /></div></Pop> : null}
        {certs.map((c, i) => {
          const x = x0 - i * (cw + gap); // RTL: first on the right
          const his = c.his && frame >= stampAt;
          return (
            <Pop key={i} x={x} y={H * 0.6} at={c.at} rot={i % 2 ? 2 : -2}>
              <div style={{width: cw, display: 'flex', flexDirection: 'column', alignItems: 'center', position: 'relative'}}>
                {c.pic ? <Img src={staticFile(c.pic)} style={{width: cw - 40, height: cw - 40, borderRadius: 14, ...stickerBorder(6), filter: frame >= stampAt && !c.his ? 'grayscale(.7) brightness(.7)' : 'none'}} />
                  : <div style={{width: cw - 40, height: cw - 40, borderRadius: 14, background: E.bluePaper, ...stickerBorder(6), display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: 46, fontWeight: 900, color: E.ink, fontFamily: 'Montserrat', filter: frame >= stampAt && !c.his ? 'grayscale(.7) brightness(.7)' : 'none'}}>{c.name}</div>}
                <Label text={c.name} size={36} style={{marginTop: 12}} />
                {his ? <div style={{position: 'absolute', top: -30, right: -20, transform: `scale(${pop(stampAt + i * 6)}) rotate(-12deg)`}}><Mark ok s={110} /></div> : null}
              </div>
            </Pop>
          );
        })}
        {frame >= stampAt ? <Pop x={W / 2} y={H - 120} at={stampAt}><Chip text={stampText} bg={E.olive} size={44} /></Pop> : null}
        {chips.map((c, i) => <Pop key={i} x={W / 2 + (i - (chips.length - 1) / 2) * 620} y={H - 120 - (frame >= stampAt ? 110 : 0)} at={c.at}><Chip text={c.text} bg={[E.mustard, E.blue][i % 2]} size={38} /></Pop>)}
      </AbsoluteFill></Backdrop>
    </Base>
  );
};

// ============ 11) AI at work: two screens; replaces us? ============
export const qaAiSchema = z.object({
  title: z.string().default('الـ*AI* في شغلنا'),
  meAt: z.number().default(10), aiAt: z.number().default(40), tasks: z.array(z.object({text: z.string(), at: z.number()})).default([]),
  qAt: z.number().default(9999), qEnd: z.number().default(99999), aAt: z.number().default(9999), qText: z.string().default('هيستبدلنا؟'), aText: z.string().default('لأ… *بيسرّعنا*'),
  previewBg: z.string().default(''),
});
const Screen: React.FC<{emo: string; label: string; children?: React.ReactNode; tint: string}> = ({emo, label, children, tint}) => (
  <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
    <div style={{width: 640, height: 400, background: '#1A1D26', borderRadius: 18, border: `10px solid ${E.paper}`, boxShadow: '0 20px 40px rgba(0,0,0,.5)', position: 'relative', overflow: 'hidden'}}>
      <div style={{position: 'absolute', inset: 0, background: `radial-gradient(circle at 30% 20%, ${tint}, transparent 70%)`, opacity: 0.35}} />
      <div style={{position: 'absolute', left: 20, top: 20}}><Emo n={emo} s={110} /></div>
      <div style={{position: 'absolute', left: 150, right: 20, top: 26}}>{children}</div>
    </div>
    <div style={{width: 140, height: 50, background: E.paper, clipPath: 'polygon(20% 0, 80% 0, 100% 100%, 0 100%)'}} />
    <Label text={label} size={44} />
  </div>
);
export const QaAi: React.FC<z.infer<typeof qaAiSchema>> = ({title, meAt, aiAt, tasks, qAt, qEnd, aAt, qText, aText, previewBg}) => {
  const {frame, width: W, height: H, pop} = useF();
  const q = frame >= qAt && frame < qEnd;
  const code = (k: number) => Array.from({length: 6}).map((_, i) => (
    <div key={i} style={{height: 16, margin: '12px 0', borderRadius: 8, background: ['#5C8BC0', '#8E9A5B', '#E8B54A', '#C9C3B6'][(i + k) % 4], width: `${40 + ((i * 37 + k * 11) % 55)}%`,
      transform: `scaleX(${Math.min(1, Math.max(0, (frame - meAt - i * 6) / 10))})`, transformOrigin: 'left', opacity: 0.85}} />
  ));
  return (
    <Base previewBg={previewBg}>
      <Backdrop><AbsoluteFill style={{direction: 'rtl'}}>
        <Title text={title} />
        <div style={{opacity: q ? 0.25 : 1, filter: q ? 'blur(3px)' : 'none'}}>
          <Pop x={W * 0.73} y={H * 0.5} at={meAt}><Screen emo="man_technologist" label="شاشتي: *شغال*" tint={E.blue}>{code(0)}</Screen></Pop>
          <Pop x={W * 0.27} y={H * 0.5} at={aiAt}>
            <Screen emo="robot" label="شاشة الـ*AI*: شغال برضو" tint={E.orange}>
              {tasks.map((t, i) => frame >= t.at ? (
                <div key={i} style={{display: 'flex', alignItems: 'center', gap: 10, color: E.white, fontSize: 30, fontWeight: 800, marginBottom: 10, opacity: pop(t.at)}}>
                  <Mark ok s={40} /><Hi text={t.text} color={E.mustard} />
                </div>
              ) : null)}
            </Screen>
          </Pop>
          {frame >= aiAt + 20 ? (
            <svg style={{position: 'absolute', left: 0, top: 0, width: W, height: H}}>
              <path d={`M${W * 0.58} ${H * 0.4} Q${W / 2} ${H * 0.3} ${W * 0.42} ${H * 0.4}`} stroke={E.mustard} strokeWidth={6} fill="none" strokeDasharray="12 10" strokeDashoffset={-frame * 2} />
              <path d={`M${W * 0.42} ${H * 0.62} Q${W / 2} ${H * 0.72} ${W * 0.58} ${H * 0.62}`} stroke={E.blue} strokeWidth={6} fill="none" strokeDasharray="12 10" strokeDashoffset={-frame * 2} />
            </svg>
          ) : null}
        </div>
        {q ? <Pop x={W / 2} y={H * 0.45} at={qAt}><div style={{fontSize: 110, fontWeight: 900, color: E.white, textShadow: '0 8px 20px rgba(0,0,0,.6)'}}><Hi text={qText} color={E.orange} /></div></Pop> : null}
        {frame >= aAt && frame < qEnd ? <Pop x={W / 2} y={H * 0.65} at={aAt}><div style={{display: 'flex', alignItems: 'center', gap: 20}}><Mark ok={false} s={100} /><Chip text={aText} bg={E.olive} size={60} /></div></Pop> : null}
      </AbsoluteFill></Backdrop>
    </Base>
  );
};

// ============ 12) testing on production: money + reputation ============
export const qaProdSchema = z.object({
  title: z.string().default('تجرب على *Production*؟'),
  usersAt: z.number().default(10), refundAt: z.number().default(60), moneyAt: z.number().default(100), repAt: z.number().default(180), bankAt: z.number().default(9999),
  previewBg: z.string().default(''),
});
export const QaProd: React.FC<z.infer<typeof qaProdSchema>> = ({title, usersAt, refundAt, moneyAt, repAt, bankAt, previewBg}) => {
  const {frame, width: W, height: H, pop} = useF();
  return (
    <Base previewBg={previewBg}>
      <Backdrop><AbsoluteFill style={{direction: 'rtl'}}>
        <Title text={title} />
        <Pop x={W * 0.75} y={H * 0.48} at={usersAt}>
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
            <div style={{display: 'flex'}}>{['man_technologist', 'woman_technologist', 'man_office_worker'].map((e, i) => <Emo key={i} n={e} s={140} style={{margin: '0 -12px'}} />)}</div>
            <Label text="ناس *حقيقية* بتستخدمه" size={42} />
          </div>
        </Pop>
        <Pop x={W * 0.5} y={H * 0.5} at={refundAt}>
          <div style={{background: E.orange, color: E.white, fontSize: 56, fontWeight: 900, padding: '16px 46px', borderRadius: 18, ...stickerBorder(6), fontFamily: 'Montserrat',
            transform: `scale(${frame > moneyAt - 6 && frame < moneyAt ? 0.92 : 1})`}}>Refund</div>
        </Pop>
        {frame >= moneyAt ? Array.from({length: 7}).map((_, i) => {
          const k = ((frame - moneyAt) / 50 + i / 7) % 1;
          return <Emo key={i} n="money_with_wings" s={110} style={{position: 'absolute', left: W * 0.42 - k * 520 + (i % 3) * 40, top: H * 0.5 - 60 - k * 260 + (i * 47) % 140, opacity: 1 - k}} />;
        }) : null}
        {frame >= moneyAt + 20 ? <Pop x={W * 0.2} y={H * 0.36} at={moneyAt + 20}><Chip text="خسارة *فلوس*" bg={E.mustard} size={46} /></Pop> : null}
        <Pop x={W * 0.24} y={H * 0.68} at={repAt}>
          <div style={{display: 'flex', alignItems: 'center', gap: 16}}><Emo n="chart_decreasing" s={150} /><Label text="سمعة *الشركة*" size={54} hi={E.orange} /></div>
        </Pop>
        {frame >= bankAt ? (
          <Pop x={W * 0.5} y={H - 110} at={bankAt}>
            <div style={{display: 'flex', alignItems: 'center', gap: 16, transform: `scale(${pop(bankAt)})`}}><Emo n="bank" s={100} /><Emo n="hourglass_not_done" s={80} /><Chip text="تطبيق بنك: الناس *مستنية* الحل" bg={E.blue} size={40} /></div>
          </Pop>
        ) : null}
      </AbsoluteFill></Backdrop>
    </Base>
  );
};

// ============ 13) market demand: junior vs senior (Aly's opinion, not a statistic) ============
export const qaDemandSchema = z.object({
  title: z.string().default('الطلب على المجال *(رأي علي)*'),
  seniorAt: z.number().default(10), juniorAt: z.number().default(60),
  more: z.array(z.object({text: z.string(), at: z.number()})).default([]),
  previewBg: z.string().default(''),
});
export const QaDemand: React.FC<z.infer<typeof qaDemandSchema>> = ({title, seniorAt, juniorAt, more, previewBg}) => {
  const {frame, width: W, height: H} = useF();
  return (
    <Base previewBg={previewBg}>
      <Backdrop><AbsoluteFill style={{direction: 'rtl'}}>
        <Title text={title} />
        <Pop x={W * 0.73} y={H * 0.5} at={seniorAt}>
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
            <Emo n="man_technologist" s={220} /><Label text="Senior" size={64} />
            <Chip text="الطلب *زي ما هو*" bg={E.olive} size={42} />
          </div>
        </Pop>
        <Pop x={W * 0.27} y={H * 0.5} at={juniorAt}>
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
            <Emo n="student" s={200} /><Label text="Junior" size={64} />
            <Chip text="المطلوب منه *أكتر بكتير*" bg={E.orange} size={42} />
            {more.map((m, i) => frame >= m.at ? <div key={i} style={{marginTop: 12, transform: `rotate(${i % 2 ? 2 : -2}deg)`}}><Paper w={420} tape={false} style={{padding: '8px 18px'}}><div style={{fontSize: 32, fontWeight: 800, textAlign: 'center'}}><Hi text={m.text} color={E.orange} /></div></Paper></div> : null)}
          </div>
        </Pop>
      </AbsoluteFill></Backdrop>
    </Base>
  );
};
