import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Sticker} from './kit';

// Online episode (Google Meet screen recording, cs ep01 2026-10-20). Aly: "simple, keep our focus on the video, hide the
// top and bottom parts" -> the Meet UI is never shown: each webcam tile is cut from the recording and laid on a calm dark
// background. Instead of zoom, the camera changes between layouts ("كادرات"), a soft slide/grow between them:
//   two = both side by side · G / A = one person big · GP / AP = one person on HIS side, card on the other side
//   (Aly 2026-10-20: Aly always LEFT, the guest always RIGHT — meet.left = 'A' — also for the speaker circle)
// Shots come from cues {t: 'shot', at, props: {m, z?, zx?, zy?}}; each change blends over BLEND frames.
// Zoom (Aly 2026-10-20: "inside the same frame of his cadre, only a little — it's a screen recording, not a camera"):
// z = gentle zoom of the picture INSIDE the tile (1.06-1.12), the tile itself keeps its size; zx/zy = focus (0..1 of the tile).

type Rect = {x: number; y: number; w: number; h: number; o: number};
type Cue = {t: string; at: number; dur: number; props: Record<string, any>};
export type MeetTiles = {G: number[]; A: number[]; left: 'G' | 'A'; phases?: {from: number; G: number[]; A: number[]; self?: number[]; masks?: Mask[]}[]; self?: number[]; masks?: Mask[]};
// Meet UI drawn inside a tile (name label, the crop button) is covered, never cropped away (Aly 2026-10-27: no crop the whole video):
// tag = our own paper name tag over the label; no tag = a small soft blur over the button. box = source px.
type Mask = {who: 'G' | 'A'; box: number[]; tag?: string}; // source px [x, y, w, h] of each tile
// phases (biz ep01 2026-10-27): the Meet layout changed during the call (guest big + Aly's tiny self-view -> side by side);
// each phase = the tile boxes from that source second on (G/A above = before the first phase).
export const tilesAt = (tiles: MeetTiles, sec: number): MeetTiles => {
  const ph = [...(tiles.phases ?? [])].reverse().find((p) => sec >= p.from);
  return ph ? {...tiles, G: ph.G, A: ph.A, self: ph.self, masks: ph.masks} : tiles;
};

const BLEND = 14;
const smooth = (x: number) => x * x * (3 - 2 * x);

const layout = (m: string, who: 'G' | 'A', ar: number, left: boolean, W: number, H: number): Rect => {
  const r = (w: number, x: number, y: number, o = 1) => ({x, y, w, h: w / ar, o});
  const tw = (W - 80) / 2; // two-shot: 40 px outer margin... 24 px gap
  const ty = H * 0.44 - tw / ar / 2;
  const two = left ? r(tw - 12, 40, ty) : r(tw - 12, W / 2 + 12, ty);
  if (m === 'two') return two;
  const big = 1480, side = 1180;
  if (m === who) return r(big, (W - big) / 2, H * 0.44 - big / ar / 2);
  if (m === who + 'P') return r(side, left ? 50 : W - side - 50, H * 0.5 - side / ar / 2); // person on his own side, card on the other
  // the other person leaves towards his own side of the screen
  return {...two, x: left ? -two.w - 60 : W + 60, o: 0};
};

const lerp = (a: Rect, b: Rect, k: number): Rect => ({
  x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k, w: a.w + (b.w - a.w) * k, h: a.h + (b.h - a.h) * k, o: a.o + (b.o - a.o) * k});

export const MeetStage: React.FC<{source: string; tiles: MeetTiles; cues: Cue[]; segments: {src: number; tl: number; len: number}[]}> = ({source, tiles: allTiles, cues, segments}) => {
  const frame = useCurrentFrame();
  const {fps, width: W, height: H} = useVideoConfig();
  const tiles = tilesAt(allTiles, frame / fps);
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
        {(tiles.masks ?? []).filter((m) => m.who === who).map((m, i) => {
          const L = (m.box[0] - t[0]) * s, T = (m.box[1] - t[1]) * s, w = m.box[2] * s, h = m.box[3] * s;
          return m.tag ? (
            <div key={i} style={{position: 'absolute', left: L - 6, top: T + h / 2, transform: 'translateY(-50%) rotate(-2deg)', background: '#EFE6D2', color: '#1C2030', fontWeight: 900,
              fontSize: Math.max(16, h * 0.95), padding: `${h * 0.12}px ${h * 0.5}px`, borderRadius: 6, whiteSpace: 'nowrap', border: '3px solid #FBF7EE', boxShadow: '0 4px 10px rgba(0,0,0,.4)', direction: 'rtl'}}>{m.tag}</div>
          ) : (
            <div key={i} style={{position: 'absolute', left: L, top: T, width: w, height: h, borderRadius: h / 2, backdropFilter: 'blur(7px)', WebkitBackdropFilter: 'blur(7px)'}} />
          );
        })}
        {who === 'G' && tiles.self ? (() => {
          // Meet drew Aly's self-view INSIDE the guest tile (biz ep01 0:17-3:07); no crop of the guest (Aly: "مش عايز كروب طول الفيديو")
          // -> cover that corner with our own framed picture of Aly (his self-view itself, a bit bigger, sticker border)
          const sv = tiles.self, a = tiles.A, k = 1.3;
          const bw = sv[2] * s * k, bh = sv[3] * s * k;
          const cx = (sv[0] - t[0] + sv[2] / 2) * s, cy = (sv[1] - t[1] + sv[3] / 2) * s;
          const bx = Math.min(r.w - bw - 10, cx - bw / 2), by = Math.min(r.h - bh - 10, cy - bh / 2);
          // Aly 2026-10-27: this part = Karim ONLY -> the corner is a soft blur with the ON AIR badge, not his picture
          return (
            <div style={{position: 'absolute', left: bx, top: by, width: bw, height: bh, borderRadius: 16, overflow: 'hidden', backdropFilter: 'blur(16px)', WebkitBackdropFilter: 'blur(16px)',
              background: 'rgba(18,20,25,.35)', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
              <Sticker name="onair" size={Math.min(bw, bh * 1.6) * 0.8} />
            </div>
          );
        })() : null}
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
      {/* fine grain = pre-made noise PNGs (an SVG feTurbulence over the full frame made the render ~1 fps) */}
      <Img src={staticFile(`enta/meet_grain_${Math.floor(frame / 3) % 3}.png`)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: 0.05, mixBlendMode: 'screen'}} />
    </AbsoluteFill>
  );
};

// Speaker circle over the full-screen boards (Aly 2026-10-20: when an explanation board stays > ~5 s, show whoever is talking in
// a circle in a corner "so people see him while he talks"; skip it only where the board itself is busy with motion).
// Cues {t: 'pip', at, dur, props: {who: 'G' | 'A', zx, zy, side: 'L' | 'R'}} — consecutive cues crossfade, a new run pops in.
// side: he looks towards the left of the screen -> circle on the RIGHT, and the other way round (Aly 2026-10-20; work/scripts/gaze.py).
export const MeetPip: React.FC<{source: string; tiles: MeetTiles; cues: Cue[]}> = ({source, tiles: allTiles, cues}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const tiles = tilesAt(allTiles, frame / fps);
  const f = (s: number) => Math.round(s * fps);
  const pips = cues.filter((c) => c.t === 'pip').sort((a, b) => a.at - b.at);
  const i = pips.findIndex((c) => frame >= f(c.at) && frame < f(c.at + c.dur));
  if (i < 0) return null;
  const c = pips[i], pc = i > 0 && Math.abs(f(pips[i - 1].at + pips[i - 1].dur) - f(c.at)) <= 1 ? pips[i - 1] : null;
  const nc = i + 1 < pips.length && Math.abs(f(c.at + c.dur) - f(pips[i + 1].at)) <= 1 ? pips[i + 1] : null;
  const k = frame - f(c.at), left = f(c.at + c.dur) - frame;
  const inP = pc ? 1 : smooth(Math.min(1, k / 10)), outP = nc ? 1 : smooth(Math.min(1, left / 10));
  const S = 250;
  const face = (cc: Cue, op: number) => {
    const who = cc.props.who as 'G' | 'A', t = tiles[who];
    const sc = (S * 1.15) / t[3]; // tile height ~1.15 circle: room around the head (Aly: "not so zoomed on the face")
    const fx = (cc.props.zx ?? 0.5) * t[2], fy = (cc.props.zy ?? 0.4) * t[3];
    return (
      <div key={who + cc.at} style={{position: 'absolute', inset: 0, opacity: op, overflow: 'hidden', borderRadius: '50%'}}>
        <OffthreadVideo src={staticFile(source)} muted startFrom={0}
          style={{position: 'absolute', width: 1920 * sc, height: 1080 * sc, maxWidth: 'none', left: S / 2 - (t[0] + fx) * sc, top: S * 0.45 - (t[1] + fy) * sc}} />
      </div>
    );
  };
  const xfade = pc && pc.props.who !== c.props.who ? smooth(Math.min(1, k / 8)) : 1;
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <div style={{position: 'absolute', [c.props.side === 'R' ? 'right' : 'left']: 44, top: 44, width: S, height: S, borderRadius: '50%', transform: `scale(${Math.min(inP, outP)})`,
        boxShadow: '0 16px 34px rgba(0,0,0,.55)', border: '7px solid #FBF7EE', outline: '3px solid rgba(20,20,30,.5)', background: '#111'}}>
        {pc && xfade < 1 ? face(pc, 1) : null}
        {face(c, xfade)}
      </div>
    </AbsoluteFill>
  );
};
