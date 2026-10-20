import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, interpolate, Easing, random} from 'remotion';
import {z} from 'zod';
import {Base, Highlight} from '../blocks/Base';
import {C, theme} from '../blocks/theme';
import {enter, lerp} from '../blocks/anim';

// Genjutsu-style chapter break (long videos only): cinema bars squeeze in -> dark "old movie" stage with
// spotlight, film grain, curtain stripes, gold chapter title + VIDEO BLOG badge + signature -> bars open.
export const sectionTransitionSchema = z.object({
  number: z.string().default('الجزء الأول'),
  title: z.string().default('يعني إيه *سكتات*؟'),
  badge: z.boolean().default(true),
});

export const SectionTransition: React.FC<z.infer<typeof sectionTransitionSchema>> = ({number, title, badge}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const ease = Easing.bezier(0.7, 0, 0.2, 1);
  // A: bars close over the footage (0-10). B: stage with thin cinema bars. C: bars close over stage
  // (N-16..N-8), then open onto the footage (N-8..N).
  const N = durationInFrames;
  const o = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const, easing: ease};
  let bars: number;
  if (frame < 10) bars = interpolate(frame, [0, 10], [0, 0.5], o);
  else if (frame < N - 16) bars = interpolate(frame, [10, 16], [0.5, 0.09], o);
  else if (frame < N - 8) bars = interpolate(frame, [N - 16, N - 8], [0.09, 0.5], o);
  else bars = interpolate(frame, [N - 8, N], [0.5, 0], o);
  const stage = frame >= 10 && frame < N - 8;
  const t = enter(frame, fps, 14);
  const s = enter(frame, fps, 22);
  const flicker = 0.92 + random(`f${frame}`) * 0.08;
  return (
    <Base>
      {stage ? (
        <AbsoluteFill style={{background: '#07080B', opacity: flicker}}>
          {/* curtain stripes */}
          {Array.from({length: 26}).map((_, i) => (
            <div key={i} style={{position: 'absolute', top: 0, height: '62%', left: `${i * 4}%`, width: '2.4%',
              background: `linear-gradient(180deg, #2a2f3a, #0b0d12)`, opacity: 0.55 + 0.25 * Math.sin(i * 1.7)}} />
          ))}
          <AbsoluteFill style={{background: `radial-gradient(ellipse 38% 55% at 50% 42%, rgba(255,240,210,0.18), transparent 70%)`}} />
          {/* film grain + scratches */}
          <svg width={width} height={height} style={{position: 'absolute', inset: 0, opacity: 0.35, mixBlendMode: 'screen'}}>
            <filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.9" seed={frame % 10} /></filter>
            <rect width={width} height={height} filter="url(#g)" opacity={0.25} />
            <line x1={width * random(`s${Math.floor(frame / 3)}`)} x2={width * random(`s${Math.floor(frame / 3)}`) + 4} y1={0} y2={height} stroke="#fff" strokeWidth={2} opacity={0.4} />
          </svg>
          <div style={{position: 'absolute', top: height * 0.3, left: 0, right: 0, textAlign: 'center'}}>
            <div style={{fontSize: 60, fontWeight: 800, color: C.gold, opacity: t, letterSpacing: 2, transform: `translateY(${lerp(t, 20, 0)}px)`}}>{number}</div>
            <div style={{fontSize: 130, fontWeight: 900, opacity: t, transform: `scale(${lerp(t, 0.85, 1)})`, textShadow: theme.textShadow}}>
              <Highlight text={title} accent={C.gold} />
            </div>
          </div>
          {badge ? (
            <>
              <Img src={staticFile('brand/video-blog-badge.png')} style={{position: 'absolute', right: 40, bottom: 120, width: 300, opacity: s}} />
              <Img src={staticFile('brand/signature-calligraphy.png')} style={{position: 'absolute', left: 50, bottom: 125, width: 230, opacity: s,
                filter: 'invert(1) sepia(1) saturate(4) hue-rotate(-10deg) brightness(1.05)'}} />
            </>
          ) : null}
        </AbsoluteFill>
      ) : null}
      {/* cinema bars */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: height * bars, background: '#000'}} />
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: height * bars, background: '#000'}} />
    </Base>
  );
};
