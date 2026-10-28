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
// patch = Meet's "speaking" dots (biz ep01 2026-10-28, on the guest's tile ~77 % of the call): a clean crop of the same spot from a
// frame without the dots ([[from sec, png], ...], the nearest earlier one is used), drawn INSIDE the picture with soft edges.
// keep = old tag text: the tag is at least that wide (a renamed tag fully covers the old one in a 'fix' overlay render).
// fix = drawn in the 'fix' overlay layer (Edit layer 'fix': only what changed, over an already rendered video).
type Mask = {who: 'G' | 'A'; box: number[]; tag?: string; keep?: string; patch?: [number, string][]; fix?: boolean}; // source px [x, y, w, h]
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

export const MeetStage: React.FC<{source: string; tiles: MeetTiles; cues: Cue[]; segments: {src: number; tl: number; len: number}[]; fix?: boolean}> = ({source, tiles: allTiles, cues, segments, fix = false}) => {
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
      <div key={who} style={{position: 'absolute', left: r.x, top: r.y, width: r.w, height: r.h, opacity: r.o, borderRadius: 28,
        overflow: 'hidden', boxShadow: fix ? undefined : '0 22px 50px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.06)'}}>
        <div style={{position: 'absolute', inset: 0, transform: `scale(${zoom.z})`, transformOrigin: `${zoom.x * 100}% ${zoom.y * 100}%`}}>
        {fix ? null : segments.map((sg, i) => (
          <Sequence key={i} from={f(sg.tl)} durationInFrames={Math.max(1, f(sg.tl + sg.len) - f(sg.tl))} layout="none">
            <OffthreadVideo src={staticFile(source)} startFrom={f(sg.src)} muted={!withAudio}
              style={{position: 'absolute', left: -t[0] * s, top: -t[1] * s, width: 1920 * s, height: 1080 * s, maxWidth: 'none'}} />
          </Sequence>
        ))}
        {(tiles.masks ?? []).filter((m) => m.who === who && m.patch).map((m, i) => {
          const sec = frame / fps, pp = m.patch as [number, string][];
          const src = ([...pp].reverse().find((q) => sec >= q[0]) ?? pp[0])[1];
          return <Img key={'pt' + i} src={staticFile(src)} style={{position: 'absolute', left: (m.box[0] - t[0]) * s, top: (m.box[1] - t[1]) * s, width: m.box[2] * s, height: m.box[3] * s,
            maskImage: 'radial-gradient(circle, black 55%, transparent 72%)', WebkitMaskImage: 'radial-gradient(circle, black 55%, transparent 72%)'}} />;
        })}
        </div>
        {/* (inner shadow ring removed — Aly 2026-10-27: "من غير ال inner shadow افضل"; radius 28 alone hides Meet's corners) */}
        {(tiles.masks ?? []).filter((m) => m.who === who && !m.patch && (!fix || m.fix)).map((m, i) => {
          const L = (m.box[0] - t[0]) * s, T = (m.box[1] - t[1]) * s, w = m.box[2] * s, h = m.box[3] * s;
          return m.tag ? (
            <div key={i} style={{position: 'absolute', left: L - 6, top: T + h / 2, transform: 'translateY(-50%) rotate(-2deg)', background: '#EFE6D2', color: '#1C2030', fontWeight: 900,
              fontSize: Math.max(16, h * 0.95), padding: `${h * 0.12}px ${h * 0.5}px`, borderRadius: 6, whiteSpace: 'nowrap', border: '3px solid #FBF7EE', boxShadow: fix ? undefined : '0 4px 10px rgba(0,0,0,.4)', direction: 'rtl',
              display: 'grid', justifyItems: 'center'}}>
              <span style={{gridArea: '1 / 1'}}>{m.tag}</span>
              {m.keep ? <span style={{gridArea: '1 / 1', visibility: 'hidden'}}>{m.keep}</span> : null}
            </div>
          ) : fix ? null : (
            <div key={i} style={{position: 'absolute', left: L, top: T, width: w, height: h, borderRadius: h / 2, backdropFilter: 'blur(7px)', WebkitBackdropFilter: 'blur(7px)'}} />
          );
        })}
        {who === 'G' && tiles.self && !fix ? (() => {
          // Meet drew Aly's self-view INSIDE the guest tile corner (biz ep01 0:17-3:07). Karim only here, no crop: blur ONLY the part of
          // the self-view that is inside the tile (Aly 2026-10-27: "مش محتاجين blur لكله… دي حتة صغيرة اوي"), soft edges, nothing else.
          const sv = tiles.self;
          const x0 = Math.max(sv[0], t[0]), x1 = Math.min(sv[0] + sv[2], t[0] + t[2]), y0 = Math.max(sv[1], t[1]), y1 = Math.min(sv[1] + sv[3], t[1] + t[3]);
          if (x1 <= x0 || y1 <= y0) return null;
          const pad = 6;
          return (
            <div style={{position: 'absolute', left: (x0 - t[0]) * s - pad, top: (y0 - t[1]) * s - pad, width: (x1 - x0) * s + 2 * pad, height: (y1 - y0) * s + 2 * pad,
              backdropFilter: 'blur(14px)', WebkitBackdropFilter: 'blur(14px)', borderRadius: 10,
              maskImage: 'linear-gradient(90deg, transparent, black 14px), linear-gradient(0deg, transparent, black 14px)', WebkitMaskImage: 'linear-gradient(90deg, transparent, black 14px)',
              maskComposite: 'intersect'}} />
          );
        })() : null}
      </div>
    );
  };
  // 'full' = his own intro/outro (the raw frame as it is, hard cut, no motion)
  if (cur === 'full' && fix) return null;
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
      {fix ? null : <MeetBg frame={frame} />}
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
  // one circle per side (biz ep01 2026-10-28: both people on a board while one explains and the other listens)
  const all = cues.filter((c) => c.t === 'pip').sort((a, b) => a.at - b.at);
  const sides = ['L', 'R'].map((sd) => all.filter((c) => (c.props.side ?? 'R') === sd));
  return <>{sides.map((pips, si) => <PipSide key={si} pips={pips} frame={frame} fps={fps} tiles={tiles} source={source} />)}</>;
};

const PipSide: React.FC<{pips: Cue[]; frame: number; fps: number; tiles: MeetTiles; source: string}> = ({pips, frame, fps, tiles, source}) => {
  const f = (s: number) => Math.round(s * fps);
  const i = pips.findIndex((c) => frame >= f(c.at) && frame < f(c.at + c.dur));
  if (i < 0) return null;
  const c = pips[i], pc = i > 0 && Math.abs(f(pips[i - 1].at + pips[i - 1].dur) - f(c.at)) <= 1 ? pips[i - 1] : null;
  const nc = i + 1 < pips.length && Math.abs(f(c.at + c.dur) - f(pips[i + 1].at)) <= 1 ? pips[i + 1] : null;
  const k = frame - f(c.at), left = f(c.at + c.dur) - frame;
  const inP = pc ? 1 : smooth(Math.min(1, k / 10)), outP = nc ? 1 : smooth(Math.min(1, left / 10));
  const S = 250;
  const face = (cc: Cue, op: number) => {
    const who = cc.props.who as 'G' | 'A', t = tiles[who];
    if (cc.props.track) {  // face track in source px [[sec, cx, cy, faceH], ...]: the circle follows the face through Meet layout changes
      const tr = cc.props.track as number[][], sec = frame / fps;
      let j = 0; while (j + 1 < tr.length && tr[j + 1][0] <= sec) j++;
      const q = tr[Math.min(j + 1, tr.length - 1)], pq = tr[j], u = q[0] > pq[0] ? Math.min(1, Math.max(0, (sec - pq[0]) / (q[0] - pq[0]))) : 0;
      const cx = pq[1] + (q[1] - pq[1]) * u, cy = pq[2] + (q[2] - pq[2]) * u, fh = pq[3] + (q[3] - pq[3]) * u;
      const sc = (S * 0.4) / fh; // face = 40% of the circle, always the same size (no sudden zoom out)
      return (
        <div key={who + cc.at} style={{position: 'absolute', inset: 0, opacity: op, overflow: 'hidden', borderRadius: '50%'}}>
          <OffthreadVideo src={staticFile(source)} muted startFrom={0}
            style={{position: 'absolute', width: 1920 * sc, height: 1080 * sc, maxWidth: 'none', left: S / 2 - cx * sc, top: S * 0.5 - cy * sc}} />
        </div>
      );
    }
    const sc = ((S * 1.15) / t[3]) * (cc.props.zs ?? 1); // zs = extra zoom (a letterboxed side tile) // tile height ~1.15 circle: room around the head (Aly: "not so zoomed on the face")
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
