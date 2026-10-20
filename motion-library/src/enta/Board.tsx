import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Base} from '../blocks/Base';
import {enter, exit, lerp} from '../blocks/anim';
import {E, Grain, Hi, Sticker, stickerBorder, Tape} from './kit';

// Full-screen "board" scenes for the show (big explanations, like his reference's board graphics).
// Backdrop = calm: dark ink + one soft glow that drifts very slowly + vignette + static paper grain.
// (Aly ep01 review: the moving pixelated dust/scratches were too noisy -> clean and still.) Enters/leaves with a wipe.
export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

export const Backdrop: React.FC<{children: React.ReactNode; tint?: string}> = ({children, tint = E.ink}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const inP = interpolate(frame, [0, 8], [0, 1], clamp), out = interpolate(frame, [durationInFrames - 8, durationInFrames], [1, 0], clamp);
  const k = Math.min(inP, out);
  const gx = 30 + 10 * Math.sin(frame / 240), gy = 35 + 6 * Math.cos(frame / 300);
  return (
    <AbsoluteFill style={{clipPath: `inset(${(1 - k) * 50}% 0 ${(1 - k) * 50}% 0)`}}>
      <AbsoluteFill style={{background: tint}} />
      <AbsoluteFill style={{background: `radial-gradient(circle at ${gx}% ${gy}%, rgba(92,139,192,.22) 0%, transparent 45%), radial-gradient(circle at ${100 - gx}% ${100 - gy}%, rgba(224,100,46,.12) 0%, transparent 40%)`}} />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,.55) 100%)'}} />
      <AbsoluteFill>{children}</AbsoluteFill>
      <Grain opacity={0.18} seed={41} />
    </AbsoluteFill>
  );
};

export const Title: React.FC<{text: string; at?: number}> = ({text, at = 4}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = enter(frame, fps, at);
  return (
    <div style={{position: 'absolute', top: 60, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
      <div style={{position: 'relative', background: E.paper, color: E.ink, fontSize: 64, fontWeight: 900, padding: '10px 46px', borderRadius: 10,
        transform: `rotate(-1.5deg) scale(${p})`, ...stickerBorder(7), overflow: 'hidden'}}>
        <Grain opacity={0.3} seed={43} />
        <span style={{position: 'relative'}}><Hi text={text} color={E.orange} /></span>
      </div>
    </div>
  );
};

// ---------------- 1) pipeline: design -> technical design -> contractor -> site ----------------
const step = z.object({pic: z.string(), label: z.string(), sub: z.string().default(''), at: z.number()});
export const entaPipelineSchema = z.object({
  title: z.string().default('المبنى بيعدي على *مين*؟'),
  steps: z.array(step).default([
    {pic: 'enta/fx_bokeh.jpg', label: 'الديزاين', sub: 'شكل المبنى', at: 10},
    {pic: 'enta/fx_bokeh.jpg', label: 'التكنيكال', sub: 'رسومات تنفيذية', at: 40},
    {pic: 'enta/fx_bokeh.jpg', label: 'المقاول', sub: 'يستلم اللوح', at: 70},
    {pic: 'enta/fx_bokeh.jpg', label: 'الموقع', sub: 'التنفيذ', at: 100},
  ]),
  hi: z.number().default(1), // the guest's step
  hiAt: z.number().default(60),
  hiText: z.string().default('هنا شغل *أحمد*'),
  chips: z.array(z.object({text: z.string(), at: z.number()})).default([]), // departments around the highlighted step
  previewBg: z.string().default(''),
});
export const EntaPipeline: React.FC<z.infer<typeof entaPipelineSchema>> = ({title, steps, hi, hiAt, hiText, chips, previewBg}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const n = steps.length, cw = 330, gap = (width - 160 - n * cw) / Math.max(1, n - 1);
  // RTL story: first step on the RIGHT, arrows point left.
  const xOf = (i: number) => width - 80 - cw - i * (cw + gap);
  const y = height * 0.36;
  const hp = enter(frame, fps, hiAt);
  return (
    <Base previewBg={previewBg}>
      <Backdrop>
        <Title text={title} />
        {steps.map((s, i) => {
          const p = enter(frame, fps, s.at);
          if (frame < s.at) return null;
          const isHi = i === hi && frame >= hiAt;
          const sc = isHi ? lerp(hp, 1, 1.12) : 1;
          return (
            <React.Fragment key={i}>
              {i > 0 ? (
                <div style={{position: 'absolute', left: xOf(i) + cw + gap / 2 - 70, top: y + 120, transform: `scaleX(-1) scale(${p})`}}>
                  <Sticker name={['arrow_y', 'arrow_b', 'arrow_g'][i % 3]} size={140} />
                </div>
              ) : null}
              <div style={{position: 'absolute', left: xOf(i), top: y, width: cw, transform: `translateY(${lerp(p, 80, 0)}px) scale(${lerp(p, 0.6, 1) * sc}) rotate(${(i % 2 ? 2 : -2) * p}deg)`,
                opacity: Math.min(1, p * 1.5)}}>
                <div style={{height: 260, overflow: 'hidden', background: '#222', ...stickerBorder(9), outline: isHi ? `6px solid ${E.orange}` : stickerBorder().outline}}>
                  <Img src={staticFile(s.pic)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: isHi || frame < hiAt ? 'none' : 'grayscale(.6) brightness(.8)'}} />
                </div>
                <Tape w={130} rot={-8} style={{top: -22, left: cw / 2 - 65}} olive={i % 2 === 1} />
                <div style={{marginTop: 22, textAlign: 'center', color: E.white, fontSize: 52, fontWeight: 900}}>{s.label}</div>
                {s.sub ? <div style={{textAlign: 'center', color: E.mustard, fontSize: 34, fontWeight: 700}}>{s.sub}</div> : null}
                <div style={{position: 'absolute', top: -40, right: -30, width: 70, height: 70, borderRadius: 35, background: E.ink, color: E.white,
                  border: `5px solid ${E.white}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 38, fontWeight: 900, fontFamily: 'Montserrat'}}>{i + 1}</div>
              </div>
            </React.Fragment>
          );
        })}
        {frame >= hiAt ? (
          <div style={{position: 'absolute', left: xOf(hi) + cw / 2, top: y - 150, transform: `translateX(-50%) scale(${hp}) rotate(-4deg)`,
            background: E.orange, color: E.white, fontWeight: 900, fontSize: 44, padding: '8px 30px', borderRadius: 12, border: `5px solid ${E.white}`, whiteSpace: 'nowrap'}}>
            <Hi text={hiText} color={E.ink} />
          </div>
        ) : null}
        {chips.map((c, i) => {
          const p = enter(frame, fps, c.at);
          if (frame < c.at) return null;
          const row = (i - (chips.length - 1) / 2) * 215;
          return (
            <div key={i} style={{position: 'absolute', left: xOf(hi) + cw / 2 + row - 80, top: y + 440 + (i % 2) * 14, transform: `scale(${p}) rotate(${i % 2 ? 4 : -4}deg)`,
              background: [E.blue, E.olive, E.mustard, E.orange][i % 4], color: E.ink, fontWeight: 900, fontSize: 36, padding: '6px 22px', borderRadius: 30,
              border: `4px solid ${E.white}`, whiteSpace: 'nowrap', boxShadow: '0 8px 16px rgba(0,0,0,.4)'}}>{c.text}</div>
          );
        })}
      </Backdrop>
    </Base>
  );
};

// ---------------- 2) clash: building section, a duct crosses a space -> rerouted in the corridor ceiling ----------------
export const entaClashSchema = z.object({
  title: z.string().default('*تعارض* بين الأقسام'),
  ductAt: z.number().default(30), clashAt: z.number().default(70), fixAt: z.number().default(130),
  floors: z.array(z.string()).default(['مكاتب / سكني', 'مكاتب / سكني', 'مطاعم', 'بدروم: موتور']),
  clashText: z.string().default('الدكت طالع *في نص الفراغ*!'),
  fixText: z.string().default('نمشيه في *سقف الكوريدور*'),
  previewBg: z.string().default(''),
});
export const EntaClash: React.FC<z.infer<typeof entaClashSchema>> = ({title, ductAt, clashAt, fixAt, floors, clashText, fixText, previewBg}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const bx = width * 0.24, bw = width * 0.36, top = height * 0.24, fh = height * 0.15;
  const draw = interpolate(frame, [4, 30], [0, 1], clamp); // building lines draw on
  const duct = interpolate(frame, [ductAt, clashAt], [0, 1], clamp);
  const fix = interpolate(frame, [fixAt, fixAt + 30], [0, 1], clamp);
  const clashOn = frame >= clashAt && frame < fixAt;
  const flash = clashOn && Math.floor((frame - clashAt) / 5) % 2 === 0;
  const kitchenY = top + 2 * fh + fh * 0.6; // restaurants floor (index 2)
  const ductX = bx + bw * 0.45; // straight up through the middle of the spaces (bad)
  const shaftX = bx + bw - 40; // service shaft at the side (good)
  const L = 2 * fh + fh * 0.6 - 10; // duct length up to the roof
  const blue = 'rgba(169,198,228,.9)';
  return (
    <Base previewBg={previewBg}>
      <Backdrop tint="#14243A">
        <Title text={title} />
        <svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
          {/* blueprint grid */}
          {Array.from({length: 40}).map((_, i) => <line key={'g' + i} x1={i * 50} y1={0} x2={i * 50} y2={height} stroke="rgba(169,198,228,.07)" />)}
          {Array.from({length: 24}).map((_, i) => <line key={'h' + i} x1={0} y1={i * 50} x2={width} y2={i * 50} stroke="rgba(169,198,228,.07)" />)}
          {floors.map((_, i) => (
            <rect key={i} x={bx} y={top + i * fh} width={bw} height={fh} fill={i === floors.length - 1 ? 'rgba(92,139,192,.15)' : 'none'}
              stroke={blue} strokeWidth={5} strokeDasharray={2 * (bw + fh)} strokeDashoffset={(1 - draw) * 2 * (bw + fh)} />
          ))}
          {/* corridor ceiling band on the restaurants floor + shaft */}
          <rect x={bx} y={top + 2 * fh + 6} width={bw} height={22} fill={`rgba(232,181,74,${0.25 * fix})`} />
          <rect x={shaftX - 18} y={top} width={36} height={2 * fh + 30} fill="none" stroke={E.mustard} strokeDasharray="10 8" strokeWidth={3} opacity={fix} />
          {/* bad duct: straight up */}
          <line x1={ductX} y1={kitchenY} x2={ductX} y2={kitchenY - L * duct} stroke={flash ? '#ff3b30' : E.orange} strokeWidth={22}
            strokeLinecap="round" opacity={1 - fix} />
          {/* good duct: along the corridor ceiling to the shaft, then up */}
          <polyline points={`${ductX},${kitchenY} ${ductX},${top + 2 * fh + 17} ${shaftX},${top + 2 * fh + 17} ${shaftX},${top - 10}`}
            fill="none" stroke={E.olive} strokeWidth={22} strokeLinecap="round" strokeLinejoin="round"
            strokeDasharray={3000} strokeDashoffset={3000 * (1 - fix)} />
        </svg>
        {floors.map((f, i) => (
          <div key={i} style={{position: 'absolute', right: width - bx + 24, top: top + i * fh + fh / 2 - 26, color: E.white, fontSize: 40, fontWeight: 800,
            opacity: draw}}>{f}</div>
        ))}
        <div style={{position: 'absolute', left: ductX - 40, top: kitchenY - 10, opacity: enter(frame, fps, ductAt - 6)}}>
          <span style={{fontSize: 60}}>🍳</span>
        </div>
        {clashOn ? (
          <div style={{position: 'absolute', left: bx + bw + 40, top: top + fh * 0.6, transform: `scale(${enter(frame, fps, clashAt)}) rotate(-4deg)`,
            background: '#C8392B', color: E.white, fontSize: 46, whiteSpace: 'nowrap', fontWeight: 900, padding: '10px 28px', borderRadius: 12, border: `5px solid ${E.white}`}}>
            <Hi text={clashText} color={E.mustard} />
          </div>
        ) : null}
        {clashOn ? <div style={{position: 'absolute', left: ductX - 70, top: top + fh * 0.7, transform: `scale(${enter(frame, fps, clashAt + 3)})`}}><Sticker name="qmark" size={140} /></div> : null}
        {frame >= fixAt + 10 ? (
          <div style={{position: 'absolute', left: bx + bw + 40, top: top + fh * 1.9, transform: `scale(${enter(frame, fps, fixAt + 10)}) rotate(3deg)`,
            background: E.olive, color: E.ink, fontSize: 46, whiteSpace: 'nowrap', fontWeight: 900, padding: '10px 28px', borderRadius: 12, border: `5px solid ${E.white}`}}>
            ✔ <Hi text={fixText} color={E.white} />
          </div>
        ) : null}
      </Backdrop>
    </Base>
  );
};

// ---------------- 3) dead end: plan view, a corridor ends in a wall; > 9 m = no licence ----------------
export const entaDeadEndSchema = z.object({
  title: z.string().default('كود الحريق: *Dead End*'),
  walkAt: z.number().default(20), wallAt: z.number().default(70), ruleAt: z.number().default(95), stampAt: z.number().default(150),
  rule: z.string().default('مايزيدش عن *9 متر*'),
  stamp: z.string().default('مفيش رخصة'),
  // The limit is NOT fixed (Ahmed's correction): it changes with the use (residential / commercial / hotel...) and other factors.
  varyAt: z.number().default(-1), // frame: the number starts cycling through `values`, chips + note appear
  values: z.array(z.number()).default([6, 9, 12]),
  types: z.array(z.string()).default(['سكني', 'تجاري', 'فندقي']),
  note: z.string().default('الرقم *مش ثابت*: حسب نوع المبنى وعوامل تانية'),
  previewBg: z.string().default(''),
});
export const EntaDeadEnd: React.FC<z.infer<typeof entaDeadEndSchema>> = ({title, walkAt, wallAt, ruleAt, stampAt, rule, stamp, varyAt, values, types, note, previewBg}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const y0 = height * 0.5, cH = 150, x0 = width * 0.12, x1 = width * 0.82; // corridor (stair at the right, dead end at the left)
  const draw = interpolate(frame, [4, 28], [0, 1], clamp);
  const walk = interpolate(frame, [walkAt, wallAt], [0, 1], {...clamp, easing: (t) => 1 - (1 - t) * (1 - t)});
  const px = lerp(walk, x1 - 60, x0 + 50);
  const bump = frame >= wallAt ? Math.sin((frame - wallAt) / 2) * Math.exp(-(frame - wallAt) / 8) * 12 : 0;
  const ruleP = interpolate(frame, [ruleAt, ruleAt + 25], [0, 1], clamp);
  const sp = enter(frame, fps, stampAt);
  const blue = 'rgba(169,198,228,.95)';
  return (
    <Base previewBg={previewBg}>
      <Backdrop tint="#14243A">
        <Title text={title} />
        <svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
          {Array.from({length: 40}).map((_, i) => <line key={'g' + i} x1={i * 50} y1={0} x2={i * 50} y2={height} stroke="rgba(169,198,228,.07)" />)}
          {Array.from({length: 24}).map((_, i) => <line key={'h' + i} x1={0} y1={i * 50} x2={width} y2={i * 50} stroke="rgba(169,198,228,.07)" />)}
          {/* corridor walls */}
          <line x1={x1} y1={y0 - cH / 2} x2={lerp(draw, x1, x0)} y2={y0 - cH / 2} stroke={blue} strokeWidth={10} />
          <line x1={x1} y1={y0 + cH / 2} x2={lerp(draw, x1, x0)} y2={y0 + cH / 2} stroke={blue} strokeWidth={10} />
          {/* dead-end wall */}
          <line x1={x0} y1={y0 - cH / 2 - 5} x2={x0} y2={y0 + cH / 2 + 5} stroke={frame >= wallAt && frame < wallAt + 20 && (frame >> 2) % 2 ? '#ff3b30' : blue}
            strokeWidth={22} opacity={draw} />
          {/* stair (exit) */}
          {Array.from({length: 7}).map((_, i) => (
            <line key={i} x1={x1 + 20 + i * 22} y1={y0 - cH / 2 - 60} x2={x1 + 20 + i * 22} y2={y0 + cH / 2 + 60} stroke={E.mustard} strokeWidth={5} opacity={draw} />
          ))}
          {/* measuring line */}
          <line x1={x1} y1={y0 + cH / 2 + 70} x2={lerp(ruleP, x1, x0)} y2={y0 + cH / 2 + 70} stroke={E.orange} strokeWidth={6} />
          <line x1={x1} y1={y0 + cH / 2 + 50} x2={x1} y2={y0 + cH / 2 + 90} stroke={E.orange} strokeWidth={6} opacity={ruleP > 0 ? 1 : 0} />
          <line x1={x0} y1={y0 + cH / 2 + 50} x2={x0} y2={y0 + cH / 2 + 90} stroke={E.orange} strokeWidth={6} opacity={ruleP >= 1 ? 1 : 0} />
        </svg>
        <div style={{position: 'absolute', left: x1 + 10, top: y0 + cH / 2 + 100, color: E.mustard, fontSize: 38, fontWeight: 900, opacity: draw}}>السلم 🚪</div>
        <div style={{position: 'absolute', left: x0 - 10, top: y0 + cH / 2 + 100, color: E.white, fontSize: 38, fontWeight: 900, opacity: enter(frame, fps, wallAt)}}>حيطة سد!</div>
        {/* person running away from the fire, towards the dead end */}
        {frame >= walkAt - 5 ? (
          <div style={{position: 'absolute', left: px + bump - 40, top: y0 - 50, fontSize: 80, transform: 'scaleX(-1)'}}>🏃</div>
        ) : null}
        {frame >= walkAt - 5 && frame < wallAt + 40 ? <div style={{position: 'absolute', left: x1 - 120, top: y0 - 60, fontSize: 90, opacity: 0.9}}>🔥</div> : null}
        <div style={{position: 'absolute', left: (x0 + x1) / 2 - 220, top: y0 + cH / 2 + 100, width: 440, textAlign: 'center', fontSize: 52, fontWeight: 900,
          color: E.white, opacity: varyAt >= 0 && frame >= varyAt ? 0 : ruleP}}><Hi text={rule} color={E.orange} /></div>
        {varyAt >= 0 && frame >= varyAt ? (() => {
          const v = values[Math.floor((frame - varyAt) / 18) % values.length];
          const vp = enter(frame, fps, varyAt);
          return (
            <div style={{position: 'absolute', left: (x0 + x1) / 2 - 650, top: height * 0.17, width: 1300, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12}}>
              <div style={{display: 'flex', alignItems: 'center', gap: 22, transform: `scale(${vp})`}}>
                {values.map((x) => (
                  <span key={x} style={{fontSize: x === v ? 80 : 52, fontWeight: 900, color: x === v ? E.orange : 'rgba(251,247,238,.45)', fontFamily: 'Montserrat'}}>{x}</span>
                ))}
                <span style={{fontSize: 52, fontWeight: 900, color: E.white}}>متر؟</span>
              </div>
              <div style={{fontSize: 44, fontWeight: 900, color: E.white, whiteSpace: 'nowrap', opacity: enter(frame, fps, varyAt + 8)}}><Hi text={note} color={E.mustard} /></div>
              <div style={{display: 'flex', gap: 18}}>
                {types.map((t, i) => (
                  <span key={t} style={{background: [E.blue, E.olive, E.mustard, E.orange][i % 4], color: E.ink, fontWeight: 900, fontSize: 36, padding: '4px 22px',
                    borderRadius: 30, border: `4px solid ${E.white}`, transform: `scale(${enter(frame, fps, varyAt + 14 + i * 6)}) rotate(${i % 2 ? 3 : -3}deg)`}}>{t}</span>
                ))}
                <span style={{color: E.white, fontSize: 36, fontWeight: 800, opacity: enter(frame, fps, varyAt + 14 + types.length * 6)}}>…</span>
              </div>
            </div>
          );
        })() : null}
        {frame >= stampAt ? (
          <div style={{position: 'absolute', left: width * 0.5 - 300, top: y0 - 20, width: 600, whiteSpace: 'nowrap', textAlign: 'center', fontSize: 74, fontWeight: 900,
            color: '#E0442E', border: '10px solid #E0442E', borderRadius: 16, padding: '6px 0', transform: `rotate(-10deg) scale(${lerp(sp, 2.2, 1)})`,
            opacity: Math.min(1, sp * 2), background: 'rgba(239,230,210,.9)'}}>{stamp}</div>
        ) : null}
      </Backdrop>
    </Base>
  );
};
