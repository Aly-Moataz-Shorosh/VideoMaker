import React from 'react';
import {Img, staticFile, useCurrentFrame, useVideoConfig, interpolate, Easing} from 'remotion';
import {z} from 'zod';
import {Base} from '../blocks/Base';
import {C, theme, isVertical} from '../blocks/theme';
import {enter, exit, lerp} from '../blocks/anim';

export const sidePictureSchema = z.object({
  src: z.string().default('test/sample_map.jpg'),
  caption: z.string().default('خريطة مصر الإسلامية'),
  source: z.string().default(''),
  side: z.enum(['left', 'right']).default('left'),
  accent: z.enum(['gold', 'blue']).default('gold'),
  tilt: z.number().default(-3),
  kenBurns: z.boolean().default(true),
  fit: z.enum(['cover', 'contain']).default('cover'), // contain = logos (never cropped)
  // cover crop position (object-position y, %). Pan from -> to over the cue (e.g. 100 -> 8 = bottom up, ends on the
  // faces). Get face % with tools/face_pos.py — never crop faces (Aly 2026-10-08).
  panFrom: z.number().default(50),
  panTo: z.number().default(50),
  previewBg: z.string().default(''),
});

export const SidePicture: React.FC<z.infer<typeof sidePictureSchema>> = (props) => {
  const {src, caption, source, side, accent, tilt, kenBurns, fit, previewBg, panFrom, panTo} = props;
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const vertical = isVertical(width, height);
  const pIn = enter(frame, fps);
  const pOut = exit(frame, durationInFrames);
  const capP = Math.min(enter(frame, fps, 8), pOut);
  const pan = panFrom !== panTo;
  const zoom = kenBurns && !pan ? interpolate(frame, [0, durationInFrames], [1.0, 1.12]) : 1;
  const posY = interpolate(frame, [4, Math.max(5, durationInFrames * 0.45)], [panFrom, panTo], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});

  const w = vertical ? width * 0.7 : width * 0.27; // Aly is usually centered -> stay in the outer 30%
  const h = w * 0.62;
  const dir = side === 'left' ? -1 : 1;
  const left = vertical ? (width - w) / 2 : side === 'left' ? width * 0.03 : width * 0.97 - w;
  // Vertical: in front of the chest (like R11 file tree), keeps the face clear.
  const top = vertical ? height * 0.4 : height * 0.2;
  const p = Math.min(pIn, pOut);

  return (
    <Base previewBg={previewBg}>
      <div
        style={{
          position: 'absolute',
          left,
          top,
          width: w,
          opacity: Math.min(1, p * 1.5),
          transform: `translateX(${lerp(pIn, dir * 260, 0) + lerp(pOut, dir * 120, 0)}px) rotate(${lerp(p, tilt * 3, tilt)}deg) scale(${lerp(p, 0.85, 1)})`,
        }}
      >
        <div
          style={{
            width: w,
            height: h,
            borderRadius: theme.radius,
            overflow: 'hidden',
            border: `6px solid ${C.ink}`,
            boxShadow: theme.shadow,
            background: C.panel,
          }}
        >
          <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: fit, objectPosition: `50% ${posY}%`, padding: fit === 'contain' ? '8%' : 0, transform: `scale(${zoom})`}} />
        </div>
        {caption ? (
          <div
            style={{
              position: 'absolute',
              bottom: -34,
              [side === 'left' ? 'right' : 'left']: 30,
              opacity: capP,
              transform: `translateY(${lerp(capP, 24, 0)}px) rotate(${-tilt}deg)`,
              background: C.panel,
              borderRadius: 999,
              padding: '10px 30px',
              fontSize: vertical ? 44 : 40,
              fontWeight: 800,
              display: 'flex',
              alignItems: 'center',
              gap: 14,
              boxShadow: theme.shadow,
              borderBottom: `4px solid ${C[accent]}`,
            }}
          >
            <span style={{width: 14, height: 14, borderRadius: 7, background: C[accent]}} />
            {caption}
          </div>
        ) : null}
        {source ? (
          <div style={{position: 'absolute', top: 14, left: 18, fontSize: 20, fontFamily: 'Montserrat', fontWeight: 600, color: C.inkSoft, direction: 'ltr', opacity: p * 0.9, textShadow: '0 1px 4px #000'}}>
            {source}
          </div>
        ) : null}
      </div>
    </Base>
  );
};
