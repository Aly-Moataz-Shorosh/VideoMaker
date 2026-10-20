import React from 'react';
import {AbsoluteFill, Easing, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, Scribble, Stamp, Title, circlePath, lin, spr, torn, useBeats} from '../film/kit';
import {CairoMap, M} from './map';

// Overlay scenes for the cairohistory shorts (look 'cairo'). The map itself is ONE back scene ('cmap') for the whole short.
type B = {b?: Record<string, number>};

// Big title over the map (top area), optional stamp.
export const CTitle: React.FC<B & {title: string; sub?: string; stamp?: string; top?: number; size?: number}> = ({b, title, sub, stamp, top = 0.3, size = 92}) => {
  const f = useCurrentFrame();
  const {durationInFrames: d, width, height} = useVideoConfig();
  const at = useBeats(b);
  const o = 1 - lin(f, d - 6, d, 0, 1, Easing.in(Easing.cubic));
  return (
    <AbsoluteFill style={{opacity: o}}>
      <AbsoluteFill style={{background: `linear-gradient(180deg, rgba(30,18,8,0.0) ${top * 100 - 18}%, rgba(30,18,8,0.55) ${top * 100}%, rgba(30,18,8,0.0) ${top * 100 + 26}%)`,
        opacity: lin(f, 0, 8)}} />
      <div style={{position: 'absolute', top: height * top - size, width, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <Title text={title} size={size} width={980} stroke color="#fff" />
        {sub ? <div style={{marginTop: 18, opacity: lin(f, 10, 18), fontFamily: AR, fontWeight: 800, fontSize: 48, color: M.ink, background: M.cream, padding: '2px 26px 8px',
          borderRadius: 12, border: `4px solid ${M.ink}`, direction: 'rtl'}}>{sub}</div> : null}
        {stamp ? <div style={{marginTop: 30}}><Stamp text={stamp} at={at('stamp', 0.8)} color={M.red} size={84} /></div> : null}
      </div>
    </AbsoluteFill>
  );
};

// One of Aly's old maps (crop of what he showed in the video) as a taped paper print that slides in.
// mark = [x%, y%, rx%, ry%] red marker circle on the print at beat 'mark'; tag = label under the print.
export const CPaper: React.FC<B & {src: string; w?: number; ratio: number; top?: number; rot?: number; mark?: number[]; mark2?: number[]; tag?: string; from?: 'left' | 'right';
  flip?: boolean}> = ({b, src, w = 900, ratio, top = 0.42, rot = -3, mark, mark2, tag, from = 'right', flip = false}) => {
  const f = useCurrentFrame();
  const {fps, durationInFrames: d, width, height} = useVideoConfig();
  const at = useBeats(b);
  const p = spr(f, fps, 0, 120, 15);
  const out = lin(f, d - 8, d, 0, 1, Easing.in(Easing.cubic));
  const h = w * ratio;
  const x = width / 2 + (from === 'right' ? 1 : -1) * ((1 - p) * width * 0.9 + out * width);
  const y = height * top;
  const m1 = lin(f, at('mark', 1), at('mark', 1) + 14), m2 = lin(f, at('mark2', 2), at('mark2', 2) + 14);
  // flip: the print is turned the right way up on beat 'spin' (Piri Reis' map is drawn upside down)
  const spin = flip ? 180 * lin(f, at('spin', 2), at('spin', 2) + 20, 0, 1, Easing.inOut(Easing.cubic)) : 0;
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{background: 'rgba(20,12,4,0.45)', opacity: Math.min(lin(f, 0, 8), 1 - out)}} />
      <div style={{position: 'absolute', left: x - w / 2, top: y - h / 2, width: w, height: h, transform: `rotate(${rot * (2 - p) + spin}deg)`,
        filter: 'drop-shadow(0 26px 40px rgba(0,0,0,0.6))'}}>
        <div style={{position: 'absolute', inset: -16, background: '#F4EBD6', clipPath: torn(7, 30, 0.9)}} />
        <Img src={staticFile(src)} style={{position: 'absolute', inset: 0, width: w, height: h, objectFit: 'cover', filter: 'sepia(0.25) contrast(1.05)'}} />
        <Img src={staticFile('bg/grain_1.png')} style={{position: 'absolute', inset: 0, width: w, height: h, opacity: 0.35, mixBlendMode: 'multiply'}} />
        {[[-0.06, -0.02, -18], [0.86, -0.03, 14]].map(([tx, ty, tr], i) => (
          <div key={i} style={{position: 'absolute', left: w * tx, top: h * ty - 18, width: 170, height: 46, background: 'rgba(240,228,190,0.82)', transform: `rotate(${tr}deg)`,
            boxShadow: '0 2px 6px rgba(0,0,0,0.2)'}} />
        ))}
        {mark ? <Scribble d={circlePath((mark[0] / 100) * w, (mark[1] / 100) * h, (mark[2] / 100) * w, (mark[3] / 100) * h)} p={m1} width={w} height={h} w={12} color={M.red} /> : null}
        {mark2 ? <Scribble d={circlePath((mark2[0] / 100) * w, (mark2[1] / 100) * h, (mark2[2] / 100) * w, (mark2[3] / 100) * h)} p={m2} width={w} height={h} w={12} color={M.red} /> : null}
      </div>
      {tag ? <div style={{position: 'absolute', top: y + h / 2 + 40, width, display: 'flex', justifyContent: 'center', opacity: lin(f, 8, 16) * (1 - out)}}>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 50, color: '#fff', background: M.red, padding: '2px 28px 8px', borderRadius: 12, border: `4px solid ${M.ink}`,
          direction: 'rtl', transform: `rotate(${rot / 2}deg)`}}>{tag}</div>
      </div> : null}
    </AbsoluteFill>
  );
};

// Quick "X ✗ / ✓" verdict chip over the map (e.g. الزمالك؟ ✗)
export const CChip: React.FC<B & {text: string; ok?: boolean; top?: number}> = ({text, ok = false, top = 0.62}) => {
  const f = useCurrentFrame();
  const {fps, durationInFrames: d, width, height} = useVideoConfig();
  const p = spr(f, fps, 0, 220, 11);
  const o = 1 - lin(f, d - 6, d);
  return (
    <div style={{position: 'absolute', top: height * top, width, display: 'flex', justifyContent: 'center', opacity: o}}>
      <div style={{transform: `scale(${p}) rotate(${(1 - p) * 10 - 3}deg)`, fontFamily: AR, fontWeight: 900, fontSize: 66, color: '#fff', background: ok ? '#3E8E3A' : M.red,
        padding: '4px 34px 12px', borderRadius: 16, border: `5px solid ${M.ink}`, direction: 'rtl', boxShadow: '0 12px 26px rgba(0,0,0,0.4)'}}>{text}</div>
    </div>
  );
};

export const cairoScenes: Record<string, React.FC<any>> = {
  cmap: CairoMap, ct: CTitle, cpaper: CPaper, cchip: CChip,
};
