import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig, interpolate, Easing} from 'remotion';
import {z} from 'zod';
import {Base, Highlight} from '../blocks/Base';
import {C, theme} from '../blocks/theme';
import {enter, lerp} from '../blocks/anim';

// Aly stays in front (matte from tools/matte.py); the room behind him is wiped away by a
// diagonal slash into a motion-graphics "world" (image / map), then optionally wiped back.
export const portalWorldSchema = z.object({
  footage: z.string().default('test/aly_clip.mp4'),
  matte: z.string().default('test/aly_matte.webm'),
  footageStart: z.number().default(0), // seconds into footage where this cue starts (matte starts here too)
  world: z.string().default('test/sample_map.jpg'),
  title: z.string().default('القاهرة *الإسلامية*'),
  accent: z.enum(['gold', 'blue']).default('blue'),
  wipeIn: z.number().default(0), // frame where wipe starts
  wipeBack: z.number().default(-1), // frame to wipe back to the room (-1 = never)
  shrink: z.number().default(0.9), // Aly scale inside the world
  cropX: z.number().default(0.5), // 9:16: same speaker framing as Edit (cropX / vShift)
  vShift: z.number().default(0),
  alyX: z.number().default(0), // slide Aly sideways in the world (fraction of width, e.g. -0.22) to make room for graphics
});

const WIPE = 14;

// Built-in world: an audio waveform scrolling behind Aly; silent stretches marked red (explains "silence").
const WaveWorld: React.FC<{frame: number; width: number; height: number}> = ({frame, width, height}) => {
  const bars = 90;
  const bw = width / bars;
  const shift = (frame * 3) % bars;
  return (
    <svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
      <rect width={width} height={height} fill={C.bg} />
      {[0.2, 0.4, 0.6, 0.8].map((y) => (
        <line key={y} x1={0} x2={width} y1={height * y} y2={height * y} stroke={C.panel} strokeWidth={2} />
      ))}
      {Array.from({length: bars}).map((_, i) => {
        const k = (i + shift) % bars;
        const silent = k % 30 > 20;
        const amp = silent ? 0.02 + 0.015 * Math.abs(Math.sin(k * 3.1)) : 0.08 + 0.3 * Math.abs(Math.sin(k * 0.7) * Math.cos(k * 0.23));
        const h = amp * height;
        return (
          <g key={i}>
            {silent ? <rect x={i * bw} y={height * 0.18} width={bw + 1} height={height * 0.64} fill={C.red} opacity={0.12} /> : null}
            <rect x={i * bw + bw * 0.2} y={height / 2 - h / 2} width={bw * 0.6} height={h} rx={bw * 0.3} fill={silent ? C.red : C.blue} />
          </g>
        );
      })}
    </svg>
  );
};

export const PortalWorld: React.FC<z.infer<typeof portalWorldSchema>> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const ease = Easing.bezier(0.7, 0, 0.2, 1);
  const wIn = interpolate(frame, [p.wipeIn, p.wipeIn + WIPE], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
  const wOut = p.wipeBack < 0 ? 1 : interpolate(frame, [p.wipeBack, p.wipeBack + WIPE], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
  const w = Math.min(wIn, wOut);
  // Diagonal slash: polygon edge travels from right to left (RTL reading direction).
  const slant = width * 0.18;
  const edge = lerp(w, width + slant, -slant);
  const clip = `polygon(${edge}px 0, ${width + slant}px 0, ${width + slant}px ${height}px, ${edge - slant}px ${height}px)`;
  const zoom = interpolate(frame, [0, durationInFrames], [1.08, 1.0]);
  const s = lerp(w, 1, p.shrink);
  const titleP = Math.min(enter(frame, fps, p.wipeIn + WIPE - 4), wOut);
  // footage + matte placed exactly like Edit's main footage (9:16 = crop around the speaker, lifted by vShift)
  const vert = height > width, footW = (height * 16) / 9;
  const foot: React.CSSProperties = vert
    ? {position: 'absolute', height: '100%', width: footW, left: Math.min(0, Math.max(width - footW, width / 2 - footW * p.cropX)), top: -p.vShift * height, maxWidth: 'none'}
    : {position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover'};

  const alyStyle: React.CSSProperties = {
    position: 'absolute', inset: 0, width: '100%', height: '100%',
    transform: `translateX(${lerp(w, 0, p.alyX * width)}px) scale(${s})`, transformOrigin: '50% 100%',
  };

  return (
    <Base>
      {/* 1. the real room */}
      <OffthreadVideo src={staticFile(p.footage)} startFrom={Math.round(p.footageStart * fps)} style={foot} muted />
      {/* 2. the world, revealed by the slash */}
      <AbsoluteFill style={{clipPath: clip}}>
        <AbsoluteFill style={{background: C.bg}} />
        {p.world === 'wave' ? (
          <WaveWorld frame={frame} width={width} height={height} />
        ) : (
          <Img src={staticFile(p.world)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`, filter: 'saturate(1.1) contrast(1.05)'}} />
        )}
        <AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 60%, transparent 35%, ${C.bg}EE 100%)`}} />
      </AbsoluteFill>
      {/* slash edge lines */}
      {w > 0 && w < 1 ? (
        <svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
          <line x1={edge} y1={0} x2={edge - slant} y2={height} stroke={C[p.accent]} strokeWidth={10} />
          <line x1={edge + 40} y1={0} x2={edge + 40 - slant} y2={height} stroke={C.gold} strokeWidth={4} />
        </svg>
      ) : null}
      {/* 3. Aly always on top, aligned with the footage */}
      <div style={{...alyStyle, filter: `drop-shadow(0 0 ${lerp(w, 0, 28)}px ${C[p.accent]}66)`}}>
        <OffthreadVideo src={staticFile(p.matte)} transparent muted style={foot} />
      </div>
      {/* 4. title in the world */}
      {p.title ? (
        <div style={{position: 'absolute', top: vert ? height * 0.05 : 70, left: 40, right: 40, textAlign: 'center', opacity: titleP,
          transform: `translateY(${lerp(titleP, -30, 0)}px)`, fontSize: 96, fontWeight: 900,
          textShadow: theme.textShadow, WebkitTextStroke: `3px ${C.outline}`, paintOrder: 'stroke fill'}}>
          <Highlight text={p.title} accent={C[p.accent]} />
        </div>
      ) : null}
    </Base>
  );
};
