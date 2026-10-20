import React from 'react';
import {Freeze, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {z} from 'zod';
import {Base, Highlight} from '../blocks/Base';
import {C, theme, isVertical} from '../blocks/theme';
import {enter, exit, lerp} from '../blocks/anim';

// App tour: ONE phone card stays on screen; the app's pages (crops of real screen recordings) slide in one after
// another with a name chip + page counter. Each page: src recording, start (s), still or playing, at (frame).
const rect = z.tuple([z.number(), z.number(), z.number(), z.number()]);
export const phoneTourSchema = z.object({
  pages: z.array(z.object({src: z.string(), start: z.number(), still: z.boolean().default(true), at: z.number(),
    label: z.string().default(''), crop: rect.default([940, 150, 420, 860])})).default([]),
  title: z.string().default(''),
  hx: z.number().default(0.76), // 16:9 card center x
  h: z.number().default(0.8), // card height (fraction of screen height)
  accent: z.enum(['gold', 'blue', 'red', 'green']).default('gold'),
  split: z.boolean().default(false), // 9:16: big phone in the top half (Edit shrinks the speaker)
  previewBg: z.string().default(''),
});

const io = Easing.inOut(Easing.cubic);

export const PhoneTour: React.FC<z.infer<typeof phoneTourSchema>> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const vertical = isVertical(width, height);
  const acc = C[p.accent];
  const pIn = enter(frame, fps), pOut = exit(frame, durationInFrames);
  const k = Math.min(pIn, pOut);
  const big = vertical && p.split;
  const H = height * (big ? 0.4 : vertical ? 0.3 : p.h); // 9:16: under the face, above the captions (0.355-0.655)
  const c0 = p.pages[0]?.crop ?? [940, 150, 420, 860];
  const W = (H * c0[2]) / c0[3];
  const left = vertical ? (width - W) / 2 : width * p.hx - W / 2;
  const top = big ? height * 0.075 : vertical ? height * 0.355 : (height - H) / 2 + 30;
  let cur = 0;
  p.pages.forEach((pg, i) => {if (pg.at <= frame) cur = i;});
  const page = (i: number) => {
    const pg = p.pages[i];
    const s = W / pg.crop[2];
    const v = (
      <OffthreadVideo muted src={staticFile(pg.src)} startFrom={Math.round(pg.start * fps)}
        style={{position: 'absolute', width: 1920 * s, height: 1080 * s, left: -pg.crop[0] * s, top: -pg.crop[1] * s, maxWidth: 'none'}} />
    );
    return pg.still ? <Freeze frame={0}>{v}</Freeze> : v;
  };
  return (
    <Base previewBg={p.previewBg}>
      {p.title ? (
        <div style={{position: 'absolute', left: vertical ? 0 : left - 200, width: vertical ? width : W + 400, top: big ? height * 0.012 : vertical ? height * 0.03 : top - 96, display: 'flex', justifyContent: 'center', opacity: k}}>
          <div style={{background: C.panel, borderRadius: 999, padding: '6px 34px', fontSize: 52, fontWeight: 900, boxShadow: theme.shadow,
            borderBottom: `5px solid ${acc}`}}><Highlight text={p.title} accent={acc} /></div>
        </div>
      ) : null}
      <div style={{position: 'absolute', left, top, width: W, height: H, opacity: Math.min(1, k * 1.4),
        transform: `translateY(${lerp(pIn, 160, 0)}px) scale(${lerp(k, 0.85, 1)}) rotate(${lerp(k, 4, 0)}deg)`}}>
        <div style={{position: 'absolute', inset: -8, borderRadius: theme.radius + 8, background: `linear-gradient(135deg, ${acc}, ${C.blue})`,
          boxShadow: `${theme.shadow}, 0 0 40px ${acc}55`}} />
        <div style={{position: 'absolute', inset: 0, borderRadius: theme.radius, overflow: 'hidden', background: '#000'}}>
          {p.pages.map((pg, i) => {
            if (i < cur - 1 || i > cur) return null;
            const next = p.pages[i + 1];
            const end = next ? next.at + 10 : durationInFrames;
            // slide in from the right over 10 frames; the previous page slides out to the left underneath
            const inP = interpolate(frame, [pg.at, pg.at + 10], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: io});
            const outP = next ? interpolate(frame, [next.at, next.at + 10], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: io}) : 0;
            const x = i === 0 ? -outP * 0.35 : (1 - inP) - outP * 0.35;
            return (
              <Sequence key={i} from={pg.at} durationInFrames={Math.max(1, end - pg.at)} layout="none">
                <div style={{position: 'absolute', inset: 0, transform: `translateX(${x * W}px)`, opacity: 1 - outP * 0.6, zIndex: i}}>{page(i)}</div>
              </Sequence>
            );
          })}
        </div>
        {/* page name + counter */}
        {p.pages.map((pg, i) => {
          if (i !== cur || !pg.label) return null;
          const a = enter(frame, fps, pg.at + 4);
          return (
            <div key={'l' + i} style={{position: 'absolute', right: W + (big ? 16 : 26), top: H * 0.42, alignItems: 'flex-end', display: 'flex', flexDirection: 'column',
              gap: 10, opacity: a * pOut, transform: `translateX(${lerp(a, 60, 0)}px)`}}>
              <div style={{background: acc, color: '#0B0E13', fontWeight: 900, fontSize: big ? 34 : 46, padding: big ? '2px 16px' : '2px 26px', borderRadius: 14, whiteSpace: 'nowrap',
                boxShadow: theme.shadow, fontFamily: /^[a-z0-9 %]+$/i.test(pg.label) ? 'Montserrat' : 'Cairo'}}>{pg.label}</div>
              <div style={{fontFamily: 'Montserrat', fontWeight: 800, fontSize: 28, color: C.inkSoft, direction: 'ltr'}}>{i + 1} / {p.pages.length}</div>
            </div>
          );
        })}
      </div>
    </Base>
  );
};
