import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Base} from '../blocks/Base';
import {enter, lerp} from '../blocks/anim';
import {E, Hi, stickerBorder, Tape} from './kit';
import {Backdrop, clamp, Title} from './Board';

// ---------------- AI render: quick sketch -> flat colours -> prompt -> render -> night shot; hours vs seconds ----------------
export const entaRenderSchema = z.object({
  title: z.string().default('رندر بالـ*AI*'),
  sketch: z.string().default('projects/enta01/sketch.jpg'), color: z.string().default('projects/enta01/sketch_color.jpg'),
  render: z.string().default('projects/enta01/render.jpg'),
  colorAt: z.number().default(40), promptAt: z.number().default(80), renderAt: z.number().default(130), nightAt: z.number().default(170), vsAt: z.number().default(210),
  prompts: z.array(z.object({text: z.string(), at: z.number()})).default([
    {text: 'Render this sketch', at: 80}, {text: 'Change the wall material', at: 150}, {text: 'Night shot', at: 168}]),
  before: z.string().default('7-8 *ساعات*'), after: z.string().default('*ثواني*'),
  previewBg: z.string().default(''),
});
export const EntaRender: React.FC<z.infer<typeof entaRenderSchema>> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const iw = 900, ih = 640, ix = width * 0.5, iy = height * 0.19;
  const col = interpolate(frame, [p.colorAt, p.colorAt + 12], [0, 1], clamp);
  const ren = interpolate(frame, [p.renderAt, p.renderAt + 18], [0, 1], clamp); // wipe right -> left reveal
  const night = interpolate(frame, [p.nightAt, p.nightAt + 15], [0, 1], clamp);
  const vs = enter(frame, fps, p.vsAt);
  const img = (src: string, style: React.CSSProperties = {}) => (
    <Img src={staticFile(src)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', ...style}} />
  );
  const cur = [...p.prompts].reverse().find((q) => frame >= q.at);
  const typed = cur ? cur.text.slice(0, Math.floor(interpolate(frame, [cur.at, cur.at + 14], [0, cur.text.length], clamp))) : '';
  return (
    <Base previewBg={p.previewBg}>
      <Backdrop>
        <Title text={p.title} />
        <div style={{position: 'absolute', left: ix, top: iy, width: iw, height: ih, overflow: 'hidden', background: E.paper, ...stickerBorder(10),
          transform: `rotate(-1.5deg) scale(${enter(frame, fps, 2)})`}}>
          {img(p.sketch)}
          {img(p.color, {opacity: col})}
          {img(p.render, {clipPath: `inset(0 ${(1 - ren) * 100}% 0 0)`,
            filter: `brightness(${1 - night * 0.62}) saturate(${1 - night * 0.3}) hue-rotate(${night * 15}deg)`})}
          {night > 0 ? <AbsoluteFill style={{background: `radial-gradient(circle at 70% 60%, rgba(255,190,90,${0.45 * night}) 0%, transparent 35%)`, mixBlendMode: 'screen'}} /> : null}
          {ren > 0 && ren < 1 ? <div style={{position: 'absolute', top: 0, bottom: 0, left: `${ren * 100}%`, width: 10, background: E.white, boxShadow: `0 0 30px ${E.mustard}`}} /> : null}
        </div>
        <Tape w={170} rot={-10} style={{left: ix - 50, top: iy - 25}} />
        <Tape w={170} rot={12} olive style={{left: ix + iw - 110, top: iy + ih - 30}} />
        {cur ? (
          <div style={{position: 'absolute', left: ix + 40, top: iy + ih + 40, width: iw - 80, direction: 'ltr', background: '#141824', border: `4px solid ${E.white}`,
            borderRadius: 18, padding: '14px 24px', fontFamily: 'Montserrat', fontSize: 34, color: E.white, transform: `scale(${enter(frame, fps, p.prompts[0].at)})`,
            boxShadow: '0 12px 26px rgba(0,0,0,.5)', display: 'flex', alignItems: 'center', gap: 16}}>
            <span style={{color: E.mustard, fontWeight: 800}}>Prompt ›</span>
            <span>{typed}<span style={{opacity: frame % 16 < 8 ? 1 : 0}}>|</span></span>
          </div>
        ) : null}
        {frame >= p.vsAt ? (
          <div style={{position: 'absolute', right: width - ix + 70, top: iy + 40, width: 500, display: 'flex', flexDirection: 'column', gap: 34, transform: `scale(${vs})`}}>
            <div style={{background: E.paper, color: E.ink, borderRadius: 14, padding: '18px 26px', ...stickerBorder(6), transform: 'rotate(2deg)'}}>
              <div style={{fontSize: 36, fontWeight: 800, opacity: 0.7}}>من غير AI ⏳</div>
              <div style={{fontSize: 72, fontWeight: 900, textDecoration: frame > p.vsAt + 25 ? 'line-through' : 'none', textDecorationColor: '#C8392B'}}>
                <Hi text={p.before} color={E.orange} />
              </div>
            </div>
            <div style={{background: E.olive, color: E.ink, borderRadius: 14, padding: '18px 26px', ...stickerBorder(6), transform: `rotate(-2deg) scale(${enter(frame, fps, p.vsAt + 18)})`}}>
              <div style={{fontSize: 36, fontWeight: 800, opacity: 0.8}}>بالـAI ⚡</div>
              <div style={{fontSize: 72, fontWeight: 900}}><Hi text={p.after} color={E.white} /></div>
            </div>
          </div>
        ) : null}
      </Backdrop>
    </Base>
  );
};

// ---------------- BIM: each department's model -> merged -> clash report ----------------
export const entaMergeSchema = z.object({
  title: z.string().default('*BIM*: كل قسم عامل موديل'),
  models: z.array(z.object({label: z.string(), at: z.number()})).default([
    {label: 'معماري', at: 10}, {label: 'ميكانيكا', at: 35}, {label: 'إنشائي', at: 60}]),
  mergeAt: z.number().default(90), reportAt: z.number().default(130),
  report: z.array(z.string()).default(['ماسورة × كمرة', 'دكت × عمود', 'باب × دكت']),
  done: z.string().default('✔ تتحل على الكمبيوتر، مش في الموقع'),
  previewBg: z.string().default(''),
});
export const EntaMerge: React.FC<z.infer<typeof entaMergeSchema>> = ({title, models, mergeAt, reportAt, report, done, previewBg}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const cw = 480, ch = 400, cy = height * 0.3;
  const m = interpolate(frame, [mergeAt, mergeAt + 20], [0, 1], {...clamp, easing: (t) => t * t * (3 - 2 * t)});
  const cols = [E.blue, E.orange, E.olive];
  const homeX = (i: number) => width - 140 - cw - i * (cw + 90); // RTL: first on the right
  const mergedX = width * 0.5 - cw / 2 - (frame >= reportAt ? 330 * enter(frame, fps, reportAt) : 0);
  // simple front-elevation drawings per department (SVG 480x400): walls+windows / pipes / columns+beams
  const draw = (i: number) => {
    const c = cols[i % 3];
    if (i % 3 === 0) return (<g stroke={c} strokeWidth={6} fill="none">
      <rect x={40} y={40} width={400} height={330} /><line x1={40} y1={150} x2={440} y2={150} /><line x1={40} y1={260} x2={440} y2={260} />
      {[0, 1, 2].map((r) => [0, 1, 2, 3].map((k) => <rect key={r * 9 + k} x={70 + k * 95} y={65 + r * 110} width={50} height={60} />))}</g>);
    if (i % 3 === 1) return (<g stroke={c} strokeWidth={9} fill="none" strokeLinecap="round">
      <path d="M 20 205 H 300 V 95 H 470" /><path d="M 60 320 H 380 V 40" /></g>);
    return (<g stroke={c} strokeWidth={14} fill="none">
      {[60, 240, 420].map((x) => <line key={x} x1={x} y1={30} x2={x} y2={380} />)}
      {[150, 260].map((y) => <line key={y} x1={40} y1={y} x2={440} y2={y} />)}</g>);
  };
  const clashes = [[240, 205], [380, 260], [300, 150]]; // where the pipes cross beams / columns
  return (
    <Base previewBg={previewBg}>
      <Backdrop tint="#14243A">
        <Title text={title} />
        {models.map((md, i) => {
          const p = enter(frame, fps, md.at);
          if (frame < md.at) return null;
          const x = lerp(m, homeX(i), mergedX);
          return (
            <div key={i} style={{position: 'absolute', left: x, top: cy, width: cw, height: ch, opacity: Math.min(1, p * 1.5),
              transform: `scale(${lerp(p, 0.5, 1)}) rotate(${lerp(m, (i - 1) * 3, 0)}deg)`}}>
              <div style={{position: 'absolute', inset: 0, background: `rgba(20,36,58,${0.85 * (1 - m)})`, border: `5px solid rgba(251,247,238,${1 - m})`, borderRadius: 12}} />
              <svg width={cw} height={ch} style={{position: 'absolute', inset: 0}}>{draw(i)}</svg>
              <div style={{position: 'absolute', bottom: -70, left: 0, right: 0, textAlign: 'center', fontSize: 46, fontWeight: 900, color: cols[i % 3], opacity: 1 - m}}>{md.label}</div>
            </div>
          );
        })}
        {clashes.map(([x, y], k) => {
          const a = mergeAt + 24 + k * 8;
          if (frame < a) return null;
          const blink = Math.floor((frame - a) / 6) % 2 === 0;
          return <div key={k} style={{position: 'absolute', left: mergedX + x - 34, top: cy + y - 34, width: 68, height: 68, borderRadius: 34,
            border: `7px solid ${blink ? '#ff3b30' : E.white}`, transform: `scale(${enter(frame, fps, a)})`, boxShadow: '0 0 24px #ff3b30'}} />;
        })}
        {frame >= mergeAt + 10 ? (
          <div style={{position: 'absolute', left: mergedX + cw / 2 - 250, top: cy + ch + 24, width: 500, textAlign: 'center', direction: 'ltr', fontFamily: 'Montserrat',
            fontWeight: 800, fontSize: 36, color: E.white, opacity: enter(frame, fps, mergeAt + 10)}}>Revit · Merged Model</div>
        ) : null}
        {frame >= reportAt ? (
          <div style={{position: 'absolute', left: width * 0.53, top: cy - 10, width: 640, background: E.paper, color: E.ink, borderRadius: 14, padding: '20px 30px',
            ...stickerBorder(8), transform: `rotate(2deg) translateX(${lerp(enter(frame, fps, reportAt), 500, 0)}px)`}}>
            <div style={{direction: 'ltr', fontFamily: 'Montserrat', fontWeight: 900, fontSize: 48, color: '#C8392B'}}>Clash Report</div>
            {report.map((r, k) => (
              <div key={k} style={{display: 'flex', alignItems: 'center', gap: 16, fontSize: 42, fontWeight: 800, marginTop: 14, opacity: enter(frame, fps, reportAt + 12 + k * 10)}}>
                <span style={{background: '#C8392B', color: E.white, borderRadius: 8, padding: '0 14px', fontFamily: 'Montserrat'}}>{k + 1}</span>{r}
              </div>
            ))}
            <div style={{marginTop: 18, fontSize: 36, fontWeight: 900, color: '#5E6B30', opacity: enter(frame, fps, reportAt + 20 + report.length * 10)}}>{done}</div>
          </div>
        ) : null}
      </Backdrop>
    </Base>
  );
};
