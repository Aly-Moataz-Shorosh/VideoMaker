import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {fontCss} from '../blocks/theme';
import {Badge, Big, CamFull, Caps, Clip, Footage, Frame, Pop, Rewind, Slide, StageBg, Tray} from './kit';
import {stageScenes} from './scenes';

// Vertical shorts from the New Stage 19 lecture (Aly 2026-10-18). Timeline = the short's own mp4 (`src`: his pieces joined,
// hook first, then a reversed "rewind" bit, then the idea from its start). Props from the project's work/scripts/make_short.py.
const cue = z.object({t: z.number(), d: z.number(), k: z.string(), p: z.record(z.string(), z.any()).default({})});
export const stageShortSchema = z.object({
  duration: z.number().default(5),
  no: z.number().default(1),
  total: z.number().default(29),
  head: z.string().default(''),
  src: z.string().default(''),
  hookEnd: z.number().default(0),
  rewind: z.object({t: z.number(), d: z.number(), from: z.string(), to: z.string()}).nullable().default(null),
  thumb: z.string().default(''),
  qr: z.string().default(''),
  cues: z.array(cue).default([]),
  words: z.array(z.object({w: z.string(), start: z.number(), end: z.number(), hl: z.boolean().optional()})).default([]),
  capsHide: z.array(z.tuple([z.number(), z.number()])).default([]),
  sfx: z.array(z.object({t: z.number(), file: z.string(), vol: z.number().default(0.3)})).default([]),
  music: z.object({file: z.string(), vol: z.number().default(0.05)}).nullable().default(null),
  track: z.array(z.array(z.number())).default([]),   // [[t, cx]] his x in the hall camera (short time)
  zoom: z.array(z.array(z.number())).default([[0, 1]]),
  cam: z.string().default(''),   // v3: his 1080x1920 camera already cut from the RAW file (work/scripts/cam.py)
});
type Props = z.infer<typeof stageShortSchema>;

export const StageShort: React.FC<Props> = ({duration, no, total, head, src, hookEnd, rewind, thumb, qr, cues, words, capsHide, sfx, music, track, zoom, cam}) => {
  const {fps} = useVideoConfig();
  const now = useCurrentFrame();
  const fr = (s: number) => Math.round(s * fps);
  const D = fr(duration);
  const live = (t: number, d: number) => now >= fr(t) - 2 && now < fr(t + d) + 2;
  // the tray panel fades in/out with the scenes (none during the hook / rewind)
  const pops = cues.filter((c) => c.k === 'pop');
  const sc = cues.filter((c) => c.k !== 'hall' && c.k !== 'pop');
  const near = (c: {t: number; d: number}) => Math.min(1, Math.max(0, Math.min((now - fr(c.t)) / 6 + 1, (fr(c.t + c.d) - now) / 6)));
  const trayOn = sc.reduce((m, c) => Math.max(m, near(c)), 0);
  return (
    <AbsoluteFill style={{background: '#070912'}}>
      <style>{fontCss}</style>
      <StageBg />
      {cam ? <CamFull file={cam} /> : src && !pops.some((c) => live(c.t, c.d)) ? <Footage file={src} track={track} zoom={zoom} /> : null}
      {pops.map((c, i) => !live(c.t, c.d) ? null : (
        <Sequence key={'p' + i} from={fr(c.t)} durationInFrames={fr(c.d)} layout="none"><Pop file={src} at={c.t} dur={fr(c.d)} {...(c.p as any)} /></Sequence>))}
      {pops.some((c) => live(c.t, c.d)) ? null : <Tray on={trayOn}>
      {cues.map((c, i) => {
        if (!live(c.t, c.d) || c.k === 'hall' || c.k === 'pop') return null;
        const d = fr(c.d);
        const p = c.p as any;
        let el: React.ReactNode = null;
        if (c.k === 'slide') el = <Slide dur={d} {...p} />;
        else if (c.k === 'clip') el = <Clip dur={d} {...p} />;
        else if (c.k === 'big') el = <Big dur={d} size={110} {...p} />;
        else {
          const C = stageScenes[c.k];
          el = C ? <C dur={d} {...p} /> : null;
        }
        return <Sequence key={'c' + i} from={fr(c.t)} durationInFrames={d} layout="none">{el}</Sequence>;
      })}
      </Tray>}
      {rewind ? <Sequence from={fr(rewind.t)} durationInFrames={fr(rewind.d)} layout="none"><Rewind dur={fr(rewind.d)} from={rewind.from} to={rewind.to} /></Sequence> : null}
      <Caps words={words} hide={capsHide} />
      <Frame no={no} total={total} head={head} dur={D} hookEnd={fr(hookEnd)} />
      {thumb ? <Badge thumb={thumb} qr={qr} at={fr(hookEnd + (rewind?.d ?? 0))} big={D - fr(2.6)} /> : null}
      {src ? <Audio src={staticFile(src)} /> : null}
      {music ? <Audio src={staticFile(music.file)} volume={(f) => music.vol * Math.min(1, f / 20, (D - f) / 20)} /> : null}
      {sfx.map((s, i) => <Sequence key={'x' + i} from={fr(s.t)} durationInFrames={fr(2.5)} layout="none"><Audio src={staticFile(s.file)} volume={s.vol} /></Sequence>)}
    </AbsoluteFill>
  );
};
