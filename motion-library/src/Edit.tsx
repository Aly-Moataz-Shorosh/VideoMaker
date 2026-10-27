import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Captions} from './templates/Captions';
import {registry} from './registry';
import {applyPack, C} from './blocks/theme';
import {MeetPip, MeetStage} from './enta/Meet';

// Whole-video assembly. edit.json is produced by tools/build_edit.py (all times in timeline seconds).
// layer: 'all' = review video (footage + motion + captions); 'captions' / 'motion' = alpha tracks only.
// Cue t='zoom' is a camera move on the footage (smart zoom), not a template:
//   props {to: 1.2, x: 0.5, y: 0.35, style: 'punch' | 'push' | 'out' | 'cut'}  ('cut' = camera switch on one speaker, wins over others)

type Cue = {t: string; at: number; dur: number; props: Record<string, any>};

const smooth = (x: number) => x * x * (3 - 2 * x);

const camera = (frame: number, fps: number, cues: Cue[]): React.CSSProperties => {
  let scale = 1, ox = 0.5, oy = 0.35, base = 1, hasCut = false;
  // 'cut' = camera switch on one speaker (interview): hard cut in/out, held still. Other zooms ride on top.
  for (const c of cues) {
    if (c.t !== 'zoom' || c.props.style !== 'cut') continue;
    const a = Math.round(c.at * fps), n = Math.round(c.dur * fps), k = frame - a;
    if (k < 0 || k >= n) continue;
    base = c.props.to ?? 1.5; // static crop: a slow push here + cutting back in looked like a repeated mistake (ep01 review)
    ox = c.props.x ?? 0.5; oy = c.props.y ?? 0.35; hasCut = true;
  }
  for (const c of cues) {
    if (c.t !== 'zoom' || c.props.style === 'cut') continue;
    const a = Math.round(c.at * fps), n = Math.round(c.dur * fps), k = frame - a;
    if (k < 0 || k >= n) continue;
    const to = c.props.to ?? 1.18, style = c.props.style ?? 'punch';
    const outEnv = Math.min(1, (n - k) / 8);
    let env = 1;
    if (style === 'punch') env = Math.min(1, k / 5) * outEnv;
    else if (style === 'push') env = smooth(Math.min(1, k / n)) * outEnv;
    else env = 1 - smooth(Math.min(1, k / n)); // 'out': starts zoomed, slowly pulls back
    scale = Math.max(scale, 1 + (to - 1) * env);
    if (!hasCut) { ox = c.props.x ?? 0.5; oy = c.props.y ?? 0.35; }
  }
  return {transform: `scale(${base * scale})`, transformOrigin: `${ox * 100}% ${oy * 100}%`};
};

// 9:16 split screen (Aly 2026-10-08: "screen recording much bigger, make me smaller"): while a cue with
// props.split is on, the speaker shrinks into the lower half and the graphic owns the top half. Eased in/out.
// Footage in split mode: shrinks into the lower half and melts into the background (soft gradient edges on top and
// sides instead of a hard frame). k = 0 -> normal full frame.
const splitStyle = (k: number, height: number): React.CSSProperties => {
  // bottom edge of the lifted footage (vShift 0.15 -> ends at 0.85) always melts into the background
  const bottom = 'linear-gradient(to bottom, #000 0%, #000 76%, transparent 85%)';
  if (k <= 0) return {maskImage: bottom, WebkitMaskImage: bottom} as React.CSSProperties;
  const a = (x: number) => `rgba(0,0,0,${1 - k * (1 - x)})`; // stop alpha: 1 when k = 0
  const top = `linear-gradient(to bottom, ${a(0)} 0%, ${a(0)} 12%, #000 30%, #000 76%, transparent 85%)`;
  const sides = `linear-gradient(to right, ${a(0)} 0%, #000 16%, #000 84%, ${a(0)} 100%)`;
  return {transformOrigin: '50% 30%', transform: `translateY(${k * 0.33 * height}px) scale(${1 - 0.36 * k})`,
    maskImage: `${top}, ${sides}`, WebkitMaskImage: `${top}, ${sides}`, maskComposite: 'intersect', WebkitMaskComposite: 'source-in'} as React.CSSProperties;
};

const splitAmount = (frame: number, fps: number, cues: Cue[]) => {
  let k = 0;
  for (const c of cues) {
    if (!c.props?.split) continue;
    const a = Math.round(c.at * fps), b = Math.round((c.at + c.dur) * fps);
    if (frame < a - 1 || frame > b + 10) continue;
    const v = Math.min(1, (frame - a) / 10, (b + 10 - frame) / 10);
    k = Math.max(k, smooth(Math.max(0, v)));
  }
  return k;
};

// Background behind the footage (seen in 9:16 split / lifted footage): two blues mixed (main + darker, a soft moving
// glow) + film grain, never one flat color (Aly 2026-10-08).
const GrainBg: React.FC<{frame: number; width: number; height: number}> = ({frame, width, height}) => {
  // Textures from tools/make_grain_bg.py (stippled two-blue base, dotted shapes, strong film grain) — Aly's references:
  // risograph / grainy-gradient motion graphics. Shapes drift slowly (parallax); grain "boils" every 2 frames.
  const drift = (sx: number, sy: number, sp: number) =>
    `translate(${Math.sin(frame / sp) * sx}px, ${Math.cos(frame / (sp * 1.3)) * sy}px) scale(${1.04 + 0.02 * Math.sin(frame / (sp * 2))})`;
  const img = (n: string, t: string, op = 1) => (
    <Img src={staticFile(`bg/${n}.png`)} style={{position: 'absolute', inset: 0, width, height, transform: t, opacity: op}} />
  );
  return (
    <AbsoluteFill style={{background: '#0A2442', overflow: 'hidden'}}>
      {img('base', drift(10, 14, 140))}
      {img('blob_2', drift(40, 30, 95))}
      {img('blob_3', drift(-35, 25, 120))}
      {img('blob_1', drift(-30, 40, 110))}
      {img('blob_4', drift(20, -30, 70))}
      {img(`grain_${Math.floor(frame / 2) % 3}`, 'none', 0.65)}
    </AbsoluteFill>
  );
};

export const editSchema = z.object({
  source: z.string().default(''),
  fps: z.number().default(30),
  duration: z.number().default(3),
  layer: z.enum(['all', 'captions', 'motion']).default('all'),
  pack: z.string().default('charcoal'), // color pack from brand/packs.json (per video)
  cropX: z.number().default(0.5), // 9:16: where the speaker is in the 16:9 footage (0..1) -> centered in the crop
  vShift: z.number().default(0), // 9:16: lift the main footage (fraction of height) so the face sits higher
  // 9:16 roto mode (Aly 2026-10-08: "rotoscope me the whole video, all motion graphics behind, make me smaller"):
  // the speaker = cut-out (alpha webm from tools/matte.py --fps 30) standing at the bottom over GrainBg.
  roto: z.array(z.object({start: z.number(), file: z.string()})).default([]),
  rotoScale: z.number().default(0.62), // footage height as a fraction of the screen (bottom-anchored)
  gShift: z.number().default(0), // roto mode: lift the chest-zone graphics into the top area (fraction of height)
  capBottom: z.number().default(-1), // captions bottom (fraction); -1 = default
  captions: z.boolean().default(true), // Aly 2026-10-13: captions only in reels/shorts, OFF in long videos (Whisper mistakes)
  segments: z.array(z.object({src: z.number(), tl: z.number(), len: z.number(), source: z.string().optional(), fit: z.string().optional()})).default([]), // source: appended clip (CTA); fit 'cover' = clip already in the output aspect
  // Online interview (Google Meet recording): webcam tiles cut out of the screen recording, layouts via 'shot' cues (enta/Meet.tsx)
  meet: z.object({G: z.array(z.number()), A: z.array(z.number()), left: z.enum(['G', 'A']),
    phases: z.array(z.object({from: z.number(), G: z.array(z.number()), A: z.array(z.number()), self: z.array(z.number()).optional(),
      masks: z.array(z.object({who: z.enum(['G', 'A']), box: z.array(z.number()), tag: z.string().optional()})).optional()})).optional()}).nullable().default(null),
  words: z.array(z.object({w: z.string(), start: z.number(), end: z.number()})).default([]),
  cues: z.array(z.object({t: z.string(), at: z.number(), dur: z.number(), props: z.record(z.string(), z.any())})).default([]),
});

export const Edit: React.FC<z.infer<typeof editSchema>> = ({source, segments, words, cues, layer, pack, cropX, vShift, roto, rotoScale, gShift, capBottom, captions, meet}) => {
  applyPack(pack);
  const {fps, width, height} = useVideoConfig();
  const frame = useCurrentFrame();
  const f = (s: number) => Math.round(s * fps);
  const vertical = height > width;
  // 9:16: footage is a centered vertical crop (Aly is usually centered), scaled to fill the height.
  const footW = (height * 16) / 9;
  const footStyle: React.CSSProperties = vertical
    ? {position: 'absolute', height: '100%', width: footW, left: Math.min(0, Math.max(width - footW, width / 2 - footW * cropX)), top: -vShift * height, maxWidth: 'none'}
    : {width: '100%', height: '100%'};
  const useRoto = vertical && roto.length > 0;
  const rH = height * rotoScale, rW = (rH * 16) / 9;
  const rotoStyle: React.CSSProperties = {position: 'absolute', height: rH, width: rW, top: height - rH,
    left: width / 2 - rW * cropX, maxWidth: 'none'};
  const fade = (s: {len: number}) => (k: number) => Math.min(1, k / 3, (f(s.len) - k) / 3); // no clicks at cuts
  const FULL = ['egypt_crowd', 'judge_scene', 'portal_world'];
  return (
    <AbsoluteFill style={{background: 'transparent'}}>
      {layer === 'all' && vertical ? <GrainBg frame={frame} width={width} height={height} /> : null}
      {layer === 'all' && useRoto ? (
        <AbsoluteFill style={camera(frame, fps, cues as Cue[])}>
          {segments.map((s, i) => {
            const r = s.source ? null : [...roto].reverse().find((x) => x.start <= s.src + 0.01);
            return (
              <Sequence key={i} from={f(s.tl)} durationInFrames={Math.max(1, f(s.tl + s.len) - f(s.tl))}>
                {r ? (
                  <>
                    <Audio src={staticFile(source)} startFrom={f(s.src)} volume={fade(s)} />
                    <OffthreadVideo transparent muted src={staticFile(r.file)} startFrom={f(s.src - r.start)} style={rotoStyle} />
                  </>
                ) : (
                  <OffthreadVideo src={staticFile(s.source ?? source)} startFrom={f(s.src)} volume={fade(s)}
                    style={{width: '100%', height: '100%', objectFit: 'cover'}} />
                )}
              </Sequence>
            );
          })}
        </AbsoluteFill>
      ) : null}
      {layer === 'all' && meet && !vertical ? <MeetStage source={source} tiles={meet} cues={cues as Cue[]} segments={segments} /> : null}
      {layer === 'all' && !useRoto && !(meet && !vertical) ? (
        <AbsoluteFill style={vertical && !segments.some((s) => s.fit === 'cover' && frame >= f(s.tl) && frame < f(s.tl + s.len)) ? splitStyle(splitAmount(frame, fps, cues as Cue[]), height) : {}}>
        <AbsoluteFill style={camera(frame, fps, cues as Cue[])}>
          {segments.map((s, i) => (
            <Sequence key={i} from={f(s.tl)} durationInFrames={Math.max(1, f(s.tl + s.len) - f(s.tl))}>
              <OffthreadVideo src={staticFile(s.source ?? source)} startFrom={f(s.src)}
                style={s.fit === 'cover' ? {width: '100%', height: '100%', objectFit: 'cover'} : footStyle} />
            </Sequence>
          ))}
        </AbsoluteFill>
        </AbsoluteFill>
      ) : null}
      {layer !== 'captions'
        ? cues.map((c, i) => {
            if (c.t === 'sfx') // sound effect from public/sfx (tools/make_sfx.py), props {name, volume}
              return layer === 'all' ? (
                <Sequence key={'c' + i} from={f(c.at)} durationInFrames={Math.max(1, f(c.dur))}>
                  <Audio src={staticFile(`sfx/${c.props.name}.wav`)} volume={c.props.volume ?? 0.5} />
                </Sequence>
              ) : null;
            const e = registry[c.t];
            if (!e || c.t === 'captions') return null;
            return (
              <Sequence key={'c' + i} from={f(c.at)} durationInFrames={f(c.dur)}>
                {gShift && !FULL.includes(c.t) && !c.props?.split && c.t !== 'comment_cta' ? (
                  <AbsoluteFill style={{transform: `translateY(${-gShift * height}px)`}}>
                    <e.C {...(e.schema.parse(c.props) as Record<string, unknown>)} />
                  </AbsoluteFill>
                ) : (
                  <e.C {...(e.schema.parse(c.props) as Record<string, unknown>)} />
                )}
              </Sequence>
            );
          })
        : null}
      {layer === 'all' && meet && !vertical ? <MeetPip source={source} tiles={meet} cues={cues as Cue[]} /> : null}
      {layer !== 'motion' && captions ? <Captions words={words} maxWords={5} accent="gold" previewBg="" lift={vertical && !useRoto ? splitAmount(frame, fps, cues as Cue[]) : 0} bottomFrac={capBottom} /> : null}
    </AbsoluteFill>
  );
};
