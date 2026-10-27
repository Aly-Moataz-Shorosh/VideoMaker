import React from 'react';
import {Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, bi, lin, spr} from './kit';
import {FilmTag} from './audio';

// Idea scenes for the audio-course shorts while he talks without a screen (Aly 2026-10-26, reel 2: "حط icons تعبر عن اللي بقوله
// او موشن متخليش الشاشة مملة"). Fluent 3D emoji pictures + drawn sound waves, what he says in that sentence.
const TEAL = '#2EE6B6', VIOLET = '#8B5CF6', CORAL = '#FF6B5A';
const fl = (n: string) => staticFile(`fluent/${n}.png`);

const Pic: React.FC<{n: string; x: number; y: number; s: number; at?: number; rot?: number}> = ({n, x, y, s, at = 0, rot = 0}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, at, 170, 12);
  return <Img src={fl(n)} style={{position: 'absolute', left: x - s / 2, top: y - s / 2, width: s, height: s, opacity: Math.min(1, p * 1.5),
    transform: `scale(${p}) rotate(${rot + (1 - p) * -20}deg)`, filter: 'drop-shadow(0 18px 30px rgba(0,0,0,0.45))'}} />;
};
const Tag: React.FC<{text: string; y: number; at: number; c?: string; size?: number}> = ({text, y, at, c = TEAL, size = 52}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, at, 180, 13);
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: y, display: 'flex', justifyContent: 'center', opacity: Math.min(1, p * 1.5), transform: `scale(${0.6 + 0.4 * p})`}}>
      <div style={{padding: '12px 30px', borderRadius: 34, background: 'rgba(10,14,22,0.88)', border: `3px solid ${c}`, fontFamily: AR, fontWeight: 900, fontSize: size,
        color: '#fff', direction: 'rtl', boxShadow: `0 0 34px ${c}55`}}>{bi(text)}</div>
    </div>
  );
};
// a sound wave as an SVG path from x0 to x1; mess 0 = clean sine, 1 = crushed noisy and low (muffled)
const wavePath = (x0: number, x1: number, y: number, amp: number, t: number, mess: number) => {
  let d = '';
  for (let x = x0; x <= x1; x += 6) {
    const u = (x - x0) / (x1 - x0);
    const env = Math.sin(Math.PI * u);
    const clean = Math.sin(u * 22 - t * 0.35);
    const noisy = Math.sin(u * 97 + t * 1.3) * 0.6 + Math.sin(u * 211 - t * 2.1) * 0.4;
    const v = (clean * (1 - mess) + noisy * mess) * amp * env * (1 - 0.55 * mess);
    d += `${x === x0 ? 'M' : 'L'} ${x} ${(y + v).toFixed(1)} `;
  }
  return d;
};
const Wave: React.FC<{x0: number; x1: number; y: number; amp: number; mess: number; c: string; w?: number}> = ({x0, x1, y, amp, mess, c, w = 10}) => {
  const f = useCurrentFrame();
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
      <path d={wavePath(x0, x1, y, amp, f, mess)} fill="none" stroke={c} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" style={{filter: `drop-shadow(0 0 14px ${c})`}} />
    </svg>
  );
};

// mode 'hear': he talks, BOOM, his voice gets crushed and a "وش" rings in the ear
// mode 'plan': the clip on a timeline, cut (C) at the boom, the part after it is crushed
// mode 'outside': the boom far outside a closed house -> low and muffled inside
export const BoomScene: React.FC<{dur: number; mode?: string; boom?: number}> = ({dur, mode = 'hear', boom = 0.35}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const bf = Math.round(dur * boom);
  const hit = f >= bf;
  const flash = hit ? 1 - lin(f, bf, bf + 10) : 0;
  const shake = hit && f < bf + 14 ? Math.sin(f * 2.7) * 18 * (1 - lin(f, bf, bf + 14)) : 0;
  const mess = lin(f, bf, bf + 12);
  const o = 1 - lin(f, dur - 8, dur);
  const boomP = spr(f, fps, bf, 200, 9);
  let body: React.ReactNode = null;
  if (mode === 'hear') body = (
    <>
      <Pic n="speaking_head" x={230} y={860} s={300} />
      <Pic n="ear" x={860} y={860} s={240} at={6} />
      <Wave x0={380} x1={740} y={860} amp={90} mess={mess} c={hit ? CORAL : TEAL} />
      {hit ? <Img src={fl('collision')} style={{position: 'absolute', left: 540 - 230, top: 560 - 230, width: 460, height: 460, transform: `scale(${0.2 + 1.0 * boomP}) rotate(${(1 - boomP) * 40}deg)`,
        opacity: 1 - lin(f, bf + 40, bf + 60), filter: 'drop-shadow(0 0 40px #FFB020)'}} /> : null}
      {/* ringing "وش" around the ear */}
      {hit ? [0, 1, 2].map((k) => {
        const q = ((f - bf) / 22 + k / 3) % 1;
        return <div key={k} style={{position: 'absolute', left: 860 - 140 * (0.6 + q), top: 860 - 140 * (0.6 + q), width: 280 * (0.6 + q), height: 280 * (0.6 + q), borderRadius: '50%',
          border: `5px solid ${CORAL}`, opacity: (1 - q) * 0.8}} />;
      }) : null}
      <Tag text={hit ? 'صوتي اتغير فجأة.. ووِشّ' : 'بتكلم عادي'} y={1100} at={hit ? bf + 4 : 4} c={hit ? CORAL : TEAL} />
    </>
  );
  else if (mode === 'plan') {
    const X0 = 110, X1 = 970, cut = X0 + (X1 - X0) * 0.42;
    const sc = spr(f, fps, bf - 12, 180, 14);
    body = (
      <>
        <Tag text="الكليب بتاعي على التايم لاين" y={480} at={0} c={VIOLET} size={44} />
        <div style={{position: 'absolute', left: X0, top: 720, width: X1 - X0, height: 280, borderRadius: 26, background: 'rgba(139,92,246,0.18)', border: `3px solid ${VIOLET}`}} />
        <Wave x0={X0 + 20} x1={cut - 6} y={860} amp={95} mess={0} c={TEAL} />
        <Wave x0={cut + 6} x1={X1 - 20} y={860} amp={95} mess={mess} c={hit ? CORAL : TEAL} />
        {/* the cut: scissors come down, the line splits the clip */}
        <div style={{position: 'absolute', left: cut - 3, top: 690, width: 6, height: 340 * sc, background: '#fff', boxShadow: '0 0 20px #fff'}} />
        <Pic n="scissors" x={cut} y={640 + 40 * sc} s={150} at={bf - 14} rot={90} />
        {hit ? <Img src={fl('collision')} style={{position: 'absolute', left: (cut + X1) / 2 - 120, top: 560, width: 240, height: 240, transform: `scale(${boomP})`, filter: 'drop-shadow(0 0 30px #FFB020)'}} /> : null}
        <Tag text="قبل الانفجار: عادي" y={1060} at={8} c={TEAL} size={40} />
        <Tag text="بعد الانفجار: يدوّش ويبوظ" y={1150} at={bf + 6} c={CORAL} size={40} />
      </>
    );
  } else body = (
    <>
      <Pic n="house" x={420} y={880} s={420} />
      {/* the boom far away on the right, its rings get weak through the wall */}
      <Img src={fl('collision')} style={{position: 'absolute', left: 870 - 90, top: 640 - 90, width: 180, height: 180, transform: `scale(${spr(f, fps, 6, 200, 9)})`, filter: 'drop-shadow(0 0 30px #FFB020)'}} />
      {[0, 1, 2, 3].map((k) => {
        const q = ((f - 6) / 30 + k / 4) % 1;
        const r = 60 + 520 * q;
        return f < 6 ? null : <div key={k} style={{position: 'absolute', left: 870 - r, top: 640 - r, width: 2 * r, height: 2 * r, borderRadius: '50%', border: `${q < 0.5 ? 6 : 3}px solid ${CORAL}`,
          opacity: (1 - q) * (q < 0.5 ? 0.9 : 0.35)}} />;
      })}
      <Wave x0={260} x1={580} y={1010} amp={36} mess={0.7} c={TEAL} w={7} />
      <Tag text="الانفجار برّه.. والشبابيك مقفولة" y={460} at={4} c={CORAL} size={46} />
      <Tag text="صوته واطي ومكتوم" y={1180} at={20} c={TEAL} size={44} />
    </>
  );
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, opacity: o, transform: `translate(${shake}px, ${shake * 0.4}px)`}}>
      {body}
      {flash > 0 ? <div style={{position: 'absolute', inset: 0, background: '#FFF4D6', opacity: flash * 0.55}} /> : null}
    </div>
  );
};

// rows of pictures that build up with his words (e.g. picture: camera -> computer -> screen, sound: mic -> computer -> speaker);
// each row comes in at its own second (at), pictures one after another with arrows between them
type Row = {at: number; y: number; pics: string[]; tag?: string; c?: string};
export const IdeaRows: React.FC<{dur: number; rows: Row[]}> = ({dur, rows}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const o = 1 - lin(f, dur - 8, dur);
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, opacity: o}}>
      {rows.map((r, i) => {
        const a = Math.round(r.at * fps), n = r.pics.length, S = n > 2 ? 190 : 230, gap = n > 2 ? 330 : 380;
        const x0 = 540 + (gap * (n - 1)) / 2; // Arabic reading order: the first picture on the RIGHT, arrows point left
        return (
          <React.Fragment key={i}>
            {r.pics.map((p, k) => <Pic key={k} n={p} x={x0 - gap * k} y={r.y} s={S} at={a + 6 * k} />)}
            {r.pics.slice(1).map((_, k) => <Pic key={'a' + k} n="left_arrow" x={x0 - gap * k - gap / 2} y={r.y} s={70} at={a + 6 * k + 4} />)}
            {r.tag ? <Tag text={r.tag} y={r.y + S / 2 + 6} at={a + 4} c={r.c ?? TEAL} size={42} /> : null}
          </React.Fragment>
        );
      })}
    </div>
  );
};

export const shortScenes: Record<string, React.FC<any>> = {BoomScene, IdeaRows, FilmTag};  // FilmTag = film name card (shorts 03/04, the films he played)
