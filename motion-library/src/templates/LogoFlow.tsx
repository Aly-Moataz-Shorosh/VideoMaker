import React from 'react';
import {Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Base, Highlight} from '../blocks/Base';
import {C, theme} from '../blocks/theme';
import {enter, exit, lerp} from '../blocks/anim';

// Tool chain: logo tiles appear one by one with arrows; a small "packet" (prompt / code file) travels along each arrow.
// 16:9: vertical chain in a side column (Aly on one side); `side: 'center'` = horizontal row in the middle.
export const logoFlowSchema = z.object({
  items: z.array(z.object({logo: z.string(), label: z.string(), at: z.number().default(-1)})).default([
    {logo: 'logos/claude.svg', label: 'Claude', at: -1}, {logo: 'logos/figma.svg', label: 'Figma Make', at: -1}]),
  packet: z.string().default('Prompt'), // text on the travelling chip ('' = none)
  title: z.string().default(''),
  arrows: z.boolean().default(true), // false = just a list of logos (options, not a chain)
  stagger: z.number().default(24), // frames between items when item.at = -1
  side: z.enum(['left', 'right', 'center']).default('right'),
  accent: z.enum(['gold', 'blue', 'red', 'green']).default('gold'),
  previewBg: z.string().default(''),
});

export const LogoFlow: React.FC<z.infer<typeof logoFlowSchema>> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const out = exit(frame, durationInFrames);
  const acc = C[p.accent];
  const n = p.items.length;
  const vert = height > width; // 9:16: always a row in the graphics zone (chest, 0.40-0.68)
  const row = p.side === 'center' || vert;
  const tile = vert ? (n > 3 ? 150 : 190) : n > 3 ? 160 : 210;
  const gap = row ? Math.min(330, (width * (vert ? 0.92 : 0.8)) / n) : Math.min(330, (height * 0.8) / n);
  const cx = p.side === 'right' ? width * 0.79 : p.side === 'left' ? width * 0.21 : width / 2;
  const pos = (i: number) => row
    ? [width / 2 + (i - (n - 1) / 2) * gap * -1, height * (vert ? 0.54 : 0.5)] // RTL: first item on the right
    : [cx, height * 0.55 + (i - (n - 1) / 2) * gap];
  const at = (i: number) => (p.items[i].at >= 0 ? p.items[i].at : 4 + i * p.stagger);
  return (
    <Base previewBg={p.previewBg}>
      <div style={{position: 'absolute', inset: 0, opacity: out}}>
        {p.title ? (
          <div style={{position: 'absolute', left: row ? 0 : cx - 380, width: row ? width : 760, top: vert ? height * 0.41 : row ? height * 0.2 : height * 0.08,
            textAlign: 'center', fontSize: 66, fontWeight: 900, textShadow: theme.textShadow, opacity: enter(frame, fps)}}>
            <Highlight text={p.title} accent={acc} />
          </div>
        ) : null}
        <svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
          {(p.arrows ? p.items.slice(1) : []).map((_, k) => {
            const [x1, y1] = pos(k), [x2, y2] = pos(k + 1);
            const a = interpolate(frame, [at(k + 1) - 14, at(k + 1)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
            const r = tile / 2 + 18;
            const dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy), ux = dx / L, uy = dy / L;
            const sx = x1 + ux * r, sy = y1 + uy * r, ex = x2 - ux * r, ey = y2 - uy * r;
            return (
              <g key={k} opacity={a > 0 ? 1 : 0}>
                <line x1={sx} y1={sy} x2={lerp(a, sx, ex)} y2={lerp(a, sy, ey)} stroke={acc} strokeWidth={8} strokeDasharray="18 12"
                  strokeDashoffset={-frame * 2} strokeLinecap="round" />
                {a >= 1 ? <polygon points={`${ex},${ey} ${ex - ux * 26 - uy * 16},${ey - uy * 26 + ux * 16} ${ex - ux * 26 + uy * 16},${ey - uy * 26 - ux * 16}`} fill={acc} /> : null}
              </g>
            );
          })}
        </svg>
        {p.items.map((it, i) => {
          const a = enter(frame, fps, at(i));
          if (a <= 0.01) return null;
          const [x, y] = pos(i);
          return (
            <div key={i} style={{position: 'absolute', left: x - tile / 2, top: y - tile / 2, width: tile, opacity: Math.min(1, a * 1.5),
              transform: `scale(${lerp(a, 0.3, 1)}) rotate(${lerp(a, -12, 0)}deg)`}}>
              <div style={{width: tile, height: tile, borderRadius: 36, background: '#FFFFFF', boxShadow: `${theme.shadow}, 0 0 0 6px ${C.panel}, 0 0 30px ${acc}66`,
                display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                <Img src={staticFile(it.logo)} style={{width: tile * 0.62, height: tile * 0.62, objectFit: 'contain'}} />
              </div>
              <div style={{position: 'absolute', top: row ? tile + 14 : tile / 2 - 30, [row ? 'left' : 'right']: row ? -100 : tile + 22, width: row ? tile + 200 : 'auto',
                textAlign: 'center', whiteSpace: 'nowrap', fontFamily: /[a-z]/i.test(it.label) ? 'Montserrat' : 'Cairo', fontWeight: 800, fontSize: 40,
                direction: /[a-z]/i.test(it.label) ? 'ltr' : 'rtl', textShadow: theme.textShadow}}>{it.label}</div>
            </div>
          );
        })}
        {p.packet && p.arrows ? p.items.slice(1).map((_, k) => {
          const s = at(k + 1) - 14, e = at(k + 1) + 4;
          if (frame < s || frame > e + 6) return null;
          const t = interpolate(frame, [s, e], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          const [x1, y1] = pos(k), [x2, y2] = pos(k + 1);
          const fade = interpolate(frame, [e, e + 6], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          return (
            <div key={'p' + k} style={{position: 'absolute', left: lerp(t, x1, x2) - 90, top: lerp(t, y1, y2) - 28, width: 180, display: 'flex',
              justifyContent: 'center', opacity: fade}}>
              <div style={{background: acc, color: '#0B0E13', borderRadius: 12, padding: '4px 18px', fontFamily: 'Montserrat', fontWeight: 800, fontSize: 30,
                boxShadow: theme.shadow, direction: 'ltr'}}>📄 {p.packet}</div>
            </div>
          );
        }) : null}
      </div>
    </Base>
  );
};
