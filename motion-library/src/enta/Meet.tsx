import React from 'react';
import {AbsoluteFill, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

// Online episode (Google Meet screen recording, cs ep01 2026-10-20). Aly: "simple, keep our focus on the video, hide the
// top and bottom parts" -> the Meet UI is never shown: each webcam tile is cut from the recording and laid on a calm dark
// background. Instead of zoom, the camera changes between layouts ("كادرات"), a soft slide/grow between them:
//   two = both side by side · G / A = one person big · GP / AP = one person on the LEFT (card on the right)
// Shots come from cues {t: 'shot', at, props: {m, z?, zx?, zy?}}; each change blends over BLEND frames.
// Zoom (Aly 2026-10-20: "inside the same frame of his cadre, only a little — it's a screen recording, not a camera"):
// z = gentle zoom of the picture INSIDE the tile (1.06-1.12), the tile itself keeps its size; zx/zy = focus (0..1 of the tile).

type Rect = {x: number; y: number; w: number; h: number; o: number};
type Cue = {t: string; at: number; dur: number; props: Record<string, any>};
export type MeetTiles = {G: number[]; A: number[]; left: 'G' | 'A'}; // source px [x, y, w, h] of each tile

const BLEND = 14;
const smooth = (x: number) => x * x * (3 - 2 * x);

const layout = (m: string, who: 'G' | 'A', ar: number, left: boolean, W: number, H: number): Rect => {
  const r = (w: number, x: number, y: number, o = 1) => ({x, y, w, h: w / ar, o});
  const tw = (W - 80) / 2; // two-shot: 40 px outer margin... 24 px gap
  const ty = H * 0.44 - tw / ar / 2;
  const two = left ? r(tw - 12, 40, ty) : r(tw - 12, W / 2 + 12, ty);
  if (m === 'two') return two;
  const big = 1480, side = 1060;
  if (m === who) return r(big, (W - big) / 2, H * 0.44 - big / ar / 2);
  if (m === who + 'P') return r(side, 70, H * 0.47 - side / ar / 2);
  // the other person leaves towards his own side of the screen
  return {...two, x: left ? -two.w - 60 : W + 60, o: 0};
};

const lerp = (a: Rect, b: Rect, k: number): Rect => ({
  x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k, w: a.w + (b.w - a.w) * k, h: a.h + (b.h - a.h) * k, o: a.o + (b.o - a.o) * k});

export const MeetStage: React.FC<{source: string; tiles: MeetTiles; cues: Cue[]; segments: {src: number; tl: number; len: number}[]}> = ({source, tiles, cues, segments}) => {
  const frame = useCurrentFrame();
  const {fps, width: W, height: H} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  const shots = cues.filter((c) => c.t === 'shot').sort((a, b) => a.at - b.at);
  let cur = 'two', prev = 'two', k = 1, d = 999;
  let zc = {z: 1, x: 0.5, y: 0.35}, zp = zc;
  const zOf = (c?: Cue) => ({z: c?.props.z ?? 1, x: c?.props.zx ?? 0.5, y: c?.props.zy ?? 0.35});
  for (let i = 0; i < shots.length; i++) {
    const a = f(shots[i].at);
    if (a > frame) break;
    prev = i ? shots[i - 1].props.m : 'two'; cur = shots[i].props.m; d = frame - a; k = smooth(Math.min(1, d / BLEND));
    zp = zOf(i ? shots[i - 1] : undefined); zc = zOf(shots[i]);
  }
  // inner zoom eases slower than the layout change (calm, never a punch)
  const kz = smooth(Math.min(1, d / (BLEND * 2.2)));
  const zoom = {z: zp.z + (zc.z - zp.z) * kz, x: zp.x + (zc.x - zp.x) * kz, y: zp.y + (zc.y - zp.y) * kz};
  const rectOf = (who: 'G' | 'A') => {
    const t = tiles[who], ar = t[2] / t[3], left = tiles.left === who;
    return lerp(layout(prev, who, ar, left, W, H), layout(cur, who, ar, left, W, H), k);
  };
  const tile = (who: 'G' | 'A', withAudio: boolean) => {
    const t = tiles[who], r = rectOf(who), s = r.w / t[2];
    if (r.o <= 0.01 && !withAudio) return null;
    return (
      <div key={who} style={{position: 'absolute', left: r.x, top: r.y, width: r.w, height: r.h, opacity: r.o, borderRadius: 18,
        overflow: 'hidden', boxShadow: '0 22px 50px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.06)'}}>
        <div style={{position: 'absolute', inset: 0, transform: `scale(${zoom.z})`, transformOrigin: `${zoom.x * 100}% ${zoom.y * 100}%`}}>
        {segments.map((sg, i) => (
          <Sequence key={i} from={f(sg.tl)} durationInFrames={Math.max(1, f(sg.tl + sg.len) - f(sg.tl))} layout="none">
            <OffthreadVideo src={staticFile(source)} startFrom={f(sg.src)} muted={!withAudio}
              style={{position: 'absolute', left: -t[0] * s, top: -t[1] * s, width: 1920 * s, height: 1080 * s, maxWidth: 'none'}} />
          </Sequence>
        ))}
        </div>
      </div>
    );
  };
  // 'full' = his own intro/outro (the raw frame as it is, hard cut, no motion)
  if (cur === 'full') return (
    <AbsoluteFill style={{background: '#000'}}>
      {segments.map((sg, i) => (
        <Sequence key={i} from={f(sg.tl)} durationInFrames={Math.max(1, f(sg.tl + sg.len) - f(sg.tl))}>
          <OffthreadVideo src={staticFile(source)} startFrom={f(sg.src)} style={{width: '100%', height: '100%'}} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
  if (prev === 'full') { prev = cur; } // coming out of the intro: no slide from nowhere
  return (
    <AbsoluteFill>
      <MeetBg frame={frame} />
      {tile('G', false)}
      {tile('A', true)}
    </AbsoluteFill>
  );
};

// Calm dark background: charcoal-navy, two very soft glows in the show colours (blue / orange) drifting slowly, fine grain.
export const MeetBg: React.FC<{frame: number}> = ({frame}) => {
  const d = (sp: number, a: number) => Math.sin(frame / sp) * a;
  return (
    <AbsoluteFill style={{background: '#121419', overflow: 'hidden'}}>
      <AbsoluteFill style={{background: `radial-gradient(ellipse 55% 60% at ${22 + d(400, 4)}% ${30 + d(530, 5)}%, rgba(92,139,192,.16), transparent 70%)`}} />
      <AbsoluteFill style={{background: `radial-gradient(ellipse 50% 55% at ${80 + d(470, 4)}% ${75 + d(610, 4)}%, rgba(224,100,46,.10), transparent 70%)`}} />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse 80% 80% at 50% 50%, transparent 55%, rgba(0,0,0,.45))'}} />
      <svg style={{position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: 0.07, mixBlendMode: 'screen'}}>
        <filter id="meetgrain"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed={Math.floor(frame / 3) % 4} /></filter>
        <rect width="100%" height="100%" filter="url(#meetgrain)" />
      </svg>
    </AbsoluteFill>
  );
};
