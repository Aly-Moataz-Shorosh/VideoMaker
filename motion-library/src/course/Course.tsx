import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {fontCss} from '../blocks/theme';
import {Alt, Chip, CourseBg, Def, Fig, Hud, Key, Kw, New26, Screen, Sep} from './kit';
import {courseScenes} from './scenes';
import {courseAnims} from './anims';
import {audioScenes, FilmTag, TeaserCap, TeaserHead} from './audio';
import {audioAnims} from './audioAnims';

// Long course video (premiere pro course, 2026-10-16): his screen recordings stay on screen the whole time (full / side
// modes), motion beside or on top of empty areas; full-screen scenes only in the opening and between chapters.
// Props built by projects/<code>/work/scripts/make_course.py. All times = timeline seconds.
const cue = z.object({t: z.number(), d: z.number(), k: z.string(), p: z.record(z.string(), z.any()).default({})});
export const courseSchema = z.object({
  fps: z.number().default(25),
  duration: z.number().default(5),
  parts: z.array(z.object({at: z.number(), from: z.number(), to: z.number(), rate: z.number().default(1), file: z.string()})).default([]),
  keys: z.array(z.object({t: z.number(), m: z.string(), sx: z.number().optional(), sy: z.number().optional(), sw: z.number().optional()})).default([]),
  cues: z.array(cue).default([]), // over the screen: Kw, Def, Fig, Chip, side animations (Flip, FpsRace...)
  scenes: z.array(cue).default([]), // full screen (opening, Sep)
  huds: z.array(z.object({t: z.number(), d: z.number(), ep: z.number(), n: z.number(), total: z.number(), title: z.string()})).default([]),
  music: z.array(z.object({t: z.number(), d: z.number(), file: z.string(), from: z.number().default(0), vol: z.number().default(0.12), fade: z.number().default(1)})).default([]),
  sfx: z.array(z.object({t: z.number(), file: z.string(), vol: z.number().default(0.25)})).default([]),
});
type Props = z.infer<typeof courseSchema>;

const OVER: Record<string, React.FC<any>> = {Kw, Def, Fig, Chip, Key, Alt, New26, FilmTag, TeaserCap, TeaserHead, ...courseAnims, ...audioAnims};

export const Course: React.FC<Props> = ({parts, keys, cues, scenes, huds, music, sfx}) => {
  const {fps} = useVideoConfig();
  const now = useCurrentFrame();
  const fr = (s: number) => Math.round(s * fps);
  const live = (t: number, d: number) => now >= fr(t) - 2 && now < fr(t) + fr(d) + 2;
  return (
    <AbsoluteFill style={{background: '#07090D'}}>
      <style>{fontCss}</style>
      <CourseBg />
      <Screen parts={parts} keys={keys} />
      {huds.map((h, i) => !live(h.t, h.d) ? null : (
        <Sequence key={'h' + i} from={fr(h.t)} durationInFrames={Math.max(1, fr(h.d))} layout="none"><Hud {...h} /></Sequence>
      ))}
      {cues.map((c, i) => {
        if (!live(c.t, c.d)) return null;
        const C = OVER[c.k] ?? courseScenes[c.k] ?? audioScenes[c.k];
        if (!C) return null;
        return <Sequence key={'c' + i} from={fr(c.t)} durationInFrames={Math.max(1, fr(c.d))} layout="none"><C {...c.p} dur={fr(c.d)} /></Sequence>;
      })}
      {scenes.map((c, i) => {
        if (!live(c.t, c.d)) return null;
        const C = c.k === 'Sep' ? Sep : courseScenes[c.k] ?? audioScenes[c.k];
        if (!C) return null;
        return <Sequence key={'s' + i} from={fr(c.t)} durationInFrames={Math.max(1, fr(c.d))}><C {...c.p} dur={fr(c.d)} /></Sequence>;
      })}
      {music.map((m, i) => {
        const d = fr(m.d), fd = fr(m.fade);
        return (
          <Sequence key={'m' + i} from={fr(m.t)} durationInFrames={d} layout="none">
            <Audio src={staticFile(m.file)} startFrom={fr(m.from)}
              volume={(f) => m.vol * Math.min(1, f / Math.max(1, fd), (d - f) / Math.max(1, fd))} />
          </Sequence>
        );
      })}
      {sfx.map((s, i) => (
        <Sequence key={'x' + i} from={fr(s.t)} durationInFrames={fr(3)} layout="none"><Audio src={staticFile(s.file)} volume={s.vol} /></Sequence>
      ))}
    </AbsoluteFill>
  );
};
