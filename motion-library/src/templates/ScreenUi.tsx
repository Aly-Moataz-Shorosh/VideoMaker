import React from 'react';
import {Freeze, OffthreadVideo, interpolate, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {z} from 'zod';
import {Base, Highlight} from '../blocks/Base';
import {C, theme, isVertical} from '../blocks/theme';
import {enter, exit, lerp} from '../blocks/anim';

// A cropped piece of a screen recording (real software UI) as a floating card, with a camera move between
// two crop rects and glowing highlight boxes on the buttons/fields being talked about.
// All rects are in source pixels [x, y, w, h]; mark times are frames from the cue start.
const rect = z.tuple([z.number(), z.number(), z.number(), z.number()]);
export const screenUiSchema = z.object({
  src: z.string().default('test/aly_clip.mp4'),
  start: z.number().default(0), // seconds into the recording
  still: z.boolean().default(false), // freeze on `start` (UI that does not move)
  crop: rect.default([0, 0, 1920, 1080]),
  crop2: rect.optional(), // camera move target
  moveAt: z.number().default(0), // frame the move starts
  moveDur: z.number().default(18),
  marks: z.array(z.object({x: z.number(), y: z.number(), w: z.number(), h: z.number(),
    from: z.number().default(0), to: z.number().default(9999), label: z.string().default('')})).default([]),
  title: z.string().default(''), // Arabic pill above the card, *highlight* allowed
  tag: z.string().default('DaVinci Resolve'),
  logo: z.string().default('logos/davinci-resolve.png'),
  top: z.number().default(0.385), // 9:16: card top (fraction of height)
  width: z.number().default(0.9), // 9:16: card width (fraction of width) — tall crops narrower so captions stay clear
  accent: z.enum(['gold', 'blue', 'red', 'green']).default('gold'),
  hx: z.number().default(0.5), // 16:9: card center x (fraction) — Aly on the left -> ~0.74
  hw: z.number().default(0.46), // 16:9: card width (fraction of width)
  htop: z.number().default(0.12), // 16:9: card top (fraction of height)
  volume: z.number().default(0), // >0 plays the recording's own sound
  split: z.boolean().default(false), // 9:16: BIG card in the top half; Edit shrinks the speaker into the lower half
  previewBg: z.string().default(''),
});

const ease = Easing.inOut(Easing.cubic);

export const ScreenUi: React.FC<z.infer<typeof screenUiSchema>> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const vertical = isVertical(width, height);
  const acc = C[p.accent];
  const pIn = enter(frame, fps);
  const pOut = exit(frame, durationInFrames);
  const k = Math.min(pIn, pOut);

  const m = p.crop2 ? interpolate(frame, [p.moveAt, p.moveAt + p.moveDur], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease}) : 0;
  const cr = p.crop.map((v, i) => lerp(m, v, p.crop2 ? p.crop2[i] : v));
  const big = vertical && p.split;
  const [cr0w, cr0h] = [p.crop[2], p.crop[3]];
  const W = big ? Math.min(width * 0.96, (height * 0.4 * cr0w) / cr0h) : vertical ? width * p.width : width * p.hw;
  const s = W / cr[2];
  const H = cr[3] * s;
  const left = vertical ? (width - W) / 2 : width * p.hx - W / 2;
  const top = big ? height * 0.085 : vertical ? height * p.top : height * p.htop;

  const video = (
    <OffthreadVideo muted={p.volume <= 0} volume={p.volume} src={staticFile(p.src)} startFrom={Math.round(p.start * fps)}
      style={{position: 'absolute', width: 1920 * s, height: 1080 * s, left: -cr[0] * s, top: -cr[1] * s, maxWidth: 'none'}} />
  );

  return (
    <Base previewBg={p.previewBg}>
      {p.title ? (
        <div style={{position: 'absolute', left: 0, right: 0, top: top - 92, display: 'flex', justifyContent: 'center',
          opacity: enter(frame, fps, 5) * pOut, transform: `translateY(${lerp(enter(frame, fps, 5), 30, 0)}px)`}}>
          <div style={{background: C.panel, borderRadius: 999, padding: '6px 34px', fontSize: 52, fontWeight: 900,
            boxShadow: theme.shadow, borderBottom: `5px solid ${acc}`}}>
            <Highlight text={p.title} accent={acc} />
          </div>
        </div>
      ) : null}
      <div style={{position: 'absolute', left, top, width: W, height: H, opacity: Math.min(1, k * 1.4),
        transform: `translateY(${lerp(pIn, 160, 0)}px) scale(${lerp(k, 0.82, 1)}) rotate(${lerp(k, -4, 0)}deg)`}}>
        <div style={{position: 'absolute', inset: -8, borderRadius: theme.radius + 8,
          background: `linear-gradient(135deg, ${acc}, ${C.blue})`, boxShadow: `${theme.shadow}, 0 0 40px ${acc}55`}} />
        <div style={{position: 'absolute', inset: 0, borderRadius: theme.radius, overflow: 'hidden', background: '#000'}}>
          {p.still ? <Freeze frame={0}>{video}</Freeze> : video}
          {p.marks.map((mk, i) => {
            const a = interpolate(frame, [mk.from, mk.from + 6, mk.to - 4, mk.to], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
            if (a <= 0) return null;
            const pulse = 1 + 0.04 * Math.sin((frame - mk.from) / 4);
            return (
              <div key={i} style={{position: 'absolute', left: (mk.x - cr[0]) * s, top: (mk.y - cr[1]) * s, width: mk.w * s, height: mk.h * s,
                border: `5px solid ${acc}`, borderRadius: 12, opacity: a, transform: `scale(${lerp(a, 1.3, 1) * pulse})`,
                boxShadow: `0 0 0 4000px rgba(0,0,0,${0.35 * a}), 0 0 26px ${acc}`}}>
              </div>
            );
          })}
        </div>
        {p.marks.map((mk, i) => {
          const a = interpolate(frame, [mk.from + 4, mk.from + 10, mk.to - 4, mk.to], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          if (a <= 0 || !mk.label) return null;
          const below = (mk.y - cr[1]) * s < 70; // no room above the box -> put the label under it
          return (
            <div key={'l' + i} style={{position: 'absolute', left: (mk.x - cr[0]) * s, width: mk.w * s, display: 'flex', justifyContent: 'center',
              top: below ? (mk.y + mk.h - cr[1]) * s + 12 : (mk.y - cr[1]) * s - 70, opacity: a, transform: `translateY(${lerp(a, 16, 0)}px)`}}>
              <div style={{whiteSpace: 'nowrap', background: acc, color: C.outline, fontWeight: 900, fontSize: 40, padding: '0 22px',
                borderRadius: 12, boxShadow: theme.shadow}}>
                {mk.label}
              </div>
            </div>
          );
        })}
        {p.tag ? (
          <div style={{position: 'absolute', bottom: -26, left: 26, display: 'flex', alignItems: 'center', gap: 10, background: C.panel,
            borderRadius: 999, padding: '6px 20px 6px 8px', direction: 'ltr', fontFamily: 'Montserrat', fontWeight: 700, fontSize: 26,
            boxShadow: theme.shadow, opacity: enter(frame, fps, 8) * pOut}}>
            {p.logo ? <img src={staticFile(p.logo)} style={{width: 38, height: 38, objectFit: 'contain'}} /> : null}
            {p.tag}
          </div>
        ) : null}
      </div>
    </Base>
  );
};
