import React from 'react';
import {AbsoluteFill, Easing, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Type} from '../glass/kit';
import {AR, bi, CourseBg, EN, G, Glass, Ico, lin, spr} from './kit';

// Audio course (audioproduction, 2026-10-24): his 2021 online session, nothing cut, his audio untouched.
// Opening scenes + small tags used over the screen. Chapters come in PARTS (Aly: one broad category per group of chapters).
type P = {dur: number; [k: string]: any};
const Out: React.FC<{dur: number; children: React.ReactNode}> = ({dur, children}) => {
  const f = useCurrentFrame();
  const o = Math.min(lin(f, 0, 10), 1 - lin(f, dur - 9, dur, 0, 1, Easing.in(Easing.cubic)));
  return (
    <AbsoluteFill style={{opacity: o, filter: o < 0.99 ? `blur(${(1 - o) * 12}px)` : undefined}}>
      <CourseBg />
      {children}
    </AbsoluteFill>
  );
};
const Center: React.FC<{y: number; children: React.ReactNode}> = ({y, children}) => (
  <div style={{position: 'absolute', left: 0, right: 0, top: y, display: 'flex', justifyContent: 'center'}}>{children}</div>
);

// A frame of the session itself, then a zoom onto a box of it (box = source px of a 1280x720 frame): proof of the date.
const OProofFrame: React.FC<P> = ({dur, img, box, line1, line2}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 8, 120, 18);
  const k = lin(f, 45, 105, 0, 1, Easing.inOut(Easing.cubic));
  const W = 1040, H = W * 9 / 16;
  const s1 = Math.min(W / (box[2] * 1.6), H / (box[3] * 2.4)); // final scale (source px -> card px)
  const s0 = W / 1280;
  const s = s0 + (s1 - s0) * k;
  const cx = box[0] + box[2] / 2, cy = box[1] + box[3] / 2;
  const left = (-(cx * s) + W / 2) * k, top = (-(cy * s) + H / 2) * k;
  const L = Math.min(0, Math.max(W - 1280 * s, left)), T = Math.min(0, Math.max(H - 720 * s, top));
  const hl = lin(f, 100, 112);
  return (
    <Out dur={dur}>
      <Center y={80}><Type text={line1} at={4} size={66} width={1600} /></Center>
      <div style={{position: 'absolute', left: 960, top: 590, transform: `translate(-50%,-50%) translateY(${(1 - p) * 60}px)`, opacity: Math.min(1, p * 1.3)}}>
        <Glass w={W + 28} pad={14} r={30} glow={G.gold}>
          <div style={{width: W, height: H, overflow: 'hidden', borderRadius: 20, position: 'relative', background: '#000'}}>
            <Img src={staticFile(img)} style={{position: 'absolute', width: 1280 * s, left: L, top: T}} />
            <div style={{position: 'absolute', left: L + (box[0] - 8) * s, top: T + (box[1] - 6) * s, width: (box[2] + 16) * s, height: (box[3] + 12) * s,
              border: `${4}px solid ${G.gold}`, borderRadius: 10, opacity: hl, boxShadow: `0 0 30px ${G.gold}`}} />
          </div>
        </Glass>
      </div>
      <Center y={975}><Type text={line2} at={75} size={44} width={1600} color={G.soft} /></Center>
    </Out>
  );
};

// The course map: every PART (category) as a card with its chapter range and time.
const OParts: React.FC<P> = ({dur, title, parts}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const cols = parts.length > 4 ? 4 : parts.length;
  return (
    <Out dur={dur}>
      <Center y={70}><Type text={title} at={2} size={64} width={1600} /></Center>
      <div style={{position: 'absolute', left: 90, right: 90, top: 210, display: 'grid', gridTemplateColumns: `repeat(${cols}, 1fr)`, gap: 28, direction: 'rtl'}}>
        {parts.map((pt: any, i: number) => {
          const p = spr(f, fps, 10 + i * 5, 150, 17);
          return (
            <div key={i} style={{opacity: Math.min(1, p * 1.4), transform: `translateY(${(1 - p) * 50}px)`, padding: '26px 24px', borderRadius: 30, minHeight: 300,
              background: 'rgba(255,255,255,0.07)', border: `2px solid ${pt.c}66`, boxShadow: `0 0 40px ${pt.c}22`, boxSizing: 'border-box'}}>
              <div style={{display: 'flex', alignItems: 'center', gap: 16}}>
                <div style={{width: 78, height: 78, borderRadius: 22, background: `${pt.c}22`, display: 'flex', alignItems: 'center', justifyContent: 'center'}}><Ico n={pt.ico} s={0.62} c={pt.c} /></div>
                <span style={{fontFamily: AR, fontWeight: 900, fontSize: 30, color: pt.c}}>الجزء {i + 1}</span>
              </div>
              <div style={{fontFamily: AR, fontWeight: 900, fontSize: 42, color: G.ink, marginTop: 18, lineHeight: 1.25}}>{bi(pt.title)}</div>
              <div style={{fontFamily: AR, fontWeight: 700, fontSize: 27, color: G.soft, marginTop: 10, lineHeight: 1.35}}>{bi(pt.sub)}</div>
              <div style={{fontFamily: EN, fontWeight: 800, fontSize: 26, color: G.gold, marginTop: 14, direction: 'ltr', textAlign: 'right'}}>{pt.time} · {pt.count} {pt.count > 1 ? 'chapters' : 'chapter'}</div>
            </div>
          );
        })}
      </div>
    </Out>
  );
};

// Timestamps page grouped by part: a category band, then its chapters.
const OStampsParts: React.FC<P> = ({dur, groups}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const rows: any[] = [];
  groups.forEach((g: any) => { rows.push({head: g}); g.items.forEach((it: any) => rows.push({it, c: g.c})); });
  const half = Math.ceil(rows.length / 2);
  let cut = half;
  while (cut < rows.length && !rows[cut].head) cut++; // never split a part between the columns when it fits
  if (cut - half > 3) cut = half;
  const colsR = [rows.slice(0, cut), rows.slice(cut)];
  const per = Math.max(colsR[0].length, colsR[1].length);
  const rh = Math.min(66, 880 / per);
  let idx = 0;
  return (
    <Out dur={dur}>
      <div style={{position: 'absolute', right: 90, left: 90, top: 70, display: 'flex', gap: 60, direction: 'rtl'}}>
        {colsR.map((col, c) => (
          <div key={c} style={{flex: 1}}>
            {col.map((r: any, i: number) => {
              const p = spr(f, fps, 6 + (idx++) * 2, 160, 17);
              const st = {opacity: Math.min(1, p * 1.4), transform: `translateX(${(1 - p) * -40}px)`, height: rh, display: 'flex', alignItems: 'center'};
              if (r.head) return (
                <div key={i} style={{...st, gap: 16, marginTop: i ? 8 : 0}}>
                  <div style={{padding: '4px 18px', borderRadius: 24, background: r.head.c, fontFamily: AR, fontWeight: 900, fontSize: rh * 0.42, color: '#14181F', whiteSpace: 'nowrap'}}>{bi(r.head.title)}</div>
                  <div style={{flex: 1, height: 2, background: `${r.head.c}66`}} />
                </div>
              );
              return (
                <div key={i} style={{...st, gap: 16}}>
                  <div style={{width: 50, display: 'flex', justifyContent: 'center'}}><Ico n={r.it.ico} s={Math.min(0.46, rh / 140)} c={r.c} /></div>
                  <span style={{fontFamily: EN, fontWeight: 800, fontSize: rh * 0.42, color: G.gold, direction: 'ltr', width: 120, textAlign: 'right'}}>{r.it.time}</span>
                  <span style={{fontFamily: AR, fontWeight: 800, fontSize: rh * 0.45, color: G.ink, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>{bi(r.it.ar)}</span>
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </Out>
  );
};

// Small tag over the screen: the name of a film / video he plays (bottom-left, above the taskbar).
export const FilmTag: React.FC<{dur: number; title: string; year?: string; note?: string; x?: number; y?: number}> = ({dur, title, year, note, x = 40, y = 960}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 150, 17);
  const o = Math.min(1, p * 1.3) * (1 - lin(f, dur - 10, dur, 0, 1, Easing.in(Easing.cubic)));
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translateY(-100%) translateX(${(1 - p) * -60}px)`, opacity: o, display: 'flex', alignItems: 'center', gap: 14,
      padding: '10px 24px 10px 12px', borderRadius: 40, background: 'rgba(12,16,26,0.86)', border: '2px solid rgba(255,255,255,0.22)', boxShadow: '0 14px 40px rgba(0,0,0,0.5)'}}>
      <div style={{width: 46, height: 46, borderRadius: 14, background: G.gold, display: 'flex', alignItems: 'center', justifyContent: 'center'}}><Ico n="film" s={0.38} c="#14181F" live={false} /></div>
      <div style={{direction: 'ltr'}}>
        <div style={{fontFamily: EN, fontWeight: 800, fontSize: 30, color: G.ink}}>{title}{year ? <span style={{color: G.gold}}> · {year}</span> : null}</div>
        {note ? <div style={{fontFamily: AR, fontWeight: 700, fontSize: 24, color: G.soft, direction: 'rtl', textAlign: 'left'}}>{bi(note)}</div> : null}
      </div>
    </div>
  );
};


// Cold-open teaser ("هتشوف في الكورس ده"): his own clips play in wide mode; this is the header over all of them.
export const TeaserHead: React.FC<{dur: number; text: string}> = ({dur, text}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 140, 16);
  const o = 1 - lin(f, dur - 8, dur, 0, 1);
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: 18, display: 'flex', justifyContent: 'center', opacity: Math.min(1, p * 1.3) * o, transform: `translateY(${(1 - p) * -30}px)`}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 14, padding: '8px 26px 8px 12px', borderRadius: 40, background: 'rgba(12,16,26,0.88)', border: `2px solid ${G.gold}`, direction: 'rtl'}}>
        <div style={{width: 18, height: 18, borderRadius: '50%', background: '#FF5A5F', opacity: 0.5 + 0.5 * Math.sin(f / 4)}} />
        <span style={{fontFamily: AR, fontWeight: 900, fontSize: 38, color: G.ink}}>{bi(text)}</span>
      </div>
    </div>
  );
};
// One teaser clip's promise (bottom): big words + the program it happens in.
export const TeaserCap: React.FC<{dur: number; text: string; app?: string; n?: number; total?: number}> = ({dur, text, app, n, total}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 180, 14);
  const o = 1 - lin(f, dur - 5, dur, 0, 1);
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: 1000, display: 'flex', justifyContent: 'center', opacity: Math.min(1, p * 1.5) * o}}>
      <div style={{transform: `translateY(-50%) scale(${0.8 + 0.2 * p})`, display: 'flex', alignItems: 'center', gap: 18, padding: '10px 30px 10px 14px', borderRadius: 60,
        background: 'rgba(12,16,26,0.9)', border: '2px solid rgba(255,255,255,0.22)', boxShadow: `0 0 50px ${G.gold}44`, direction: 'rtl'}}>
        {n ? <div style={{padding: '2px 14px', borderRadius: 24, background: G.gold, fontFamily: EN, fontWeight: 900, fontSize: 30, color: '#14181F', direction: 'ltr'}}>{n}/{total}</div> : null}
        <span style={{fontFamily: AR, fontWeight: 900, fontSize: 50, color: G.ink}}>{bi(text)}</span>
        {app ? <span style={{fontFamily: EN, fontWeight: 800, fontSize: 30, color: G.blue, direction: 'ltr'}}>{app}</span> : null}
      </div>
    </div>
  );
};

// Claude's spark (vector, drawn here): rounded rays of different lengths around a centre.
export const ClaudeMark: React.FC<{s?: number; spin?: number}> = ({s = 1, spin = 0}) => {
  const L = [40, 30, 44, 34, 42, 28, 38, 46, 32, 40, 30, 36];
  return (
    <svg width={100 * s} height={100 * s} viewBox="-50 -50 100 100" style={{overflow: 'visible'}}>
      <g transform={`rotate(${spin})`}>
        {L.map((l, i) => <rect key={i} x={-3.6} y={-l} width={7.2} height={l} rx={3.6} fill="#D97757" transform={`rotate(${i * 30 + (i % 2) * 6})`} />)}
      </g>
    </svg>
  );
};
// Claude's opinion of the course + real numbers from the course itself (counted by Claude).
const OClaude: React.FC<P> = ({dur, q, stats, lines, sign}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const m = spr(f, fps, 2, 120, 14);
  return (
    <Out dur={dur}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 60, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 26, direction: 'rtl'}}>
        <div style={{transform: `scale(${m})`}}><ClaudeMark s={1.05} spin={f * 0.6} /></div>
        <Type text={q} at={8} size={58} width={1300} />
      </div>
      <div style={{position: 'absolute', left: 120, right: 120, top: 230, display: 'grid', gridTemplateColumns: `repeat(${stats.length}, 1fr)`, gap: 26, direction: 'rtl'}}>
        {stats.map((st: any, i: number) => {
          const p = spr(f, fps, 24 + i * 6, 150, 16);
          const k = lin(f, 26 + i * 6, 60 + i * 6, 0, 1, Easing.out(Easing.cubic));
          const v = typeof st.v === 'number' ? Math.round(st.v * k) : st.v;
          return (
            <div key={i} style={{opacity: Math.min(1, p * 1.4), transform: `translateY(${(1 - p) * 40}px)`, padding: '24px 18px', borderRadius: 28, textAlign: 'center',
              background: 'rgba(255,255,255,0.07)', border: '2px solid rgba(217,119,87,0.45)'}}>
              <div style={{fontFamily: EN, fontWeight: 900, fontSize: 76, color: '#F0A27E', direction: 'ltr'}}>{v}{st.unit ?? ''}</div>
              <div style={{fontFamily: AR, fontWeight: 800, fontSize: 30, color: G.ink, marginTop: 6}}>{bi(st.ar)}</div>
            </div>
          );
        })}
      </div>
      {lines.map((l: string, i: number) => (
        <Center key={i} y={540 + i * 108}><Type text={l} at={70 + i * 40} size={44} width={1640} pill={i === lines.length - 1 ? G.blue : G.gold} /></Center>
      ))}
      <div style={{position: 'absolute', left: 140, bottom: 70, display: 'flex', alignItems: 'center', gap: 14, opacity: lin(f, 70 + lines.length * 40, 86 + lines.length * 40)}}>
        <ClaudeMark s={0.42} />
        <span style={{fontFamily: EN, fontWeight: 800, fontSize: 38, color: '#F0A27E'}}>{sign}</span>
      </div>
    </Out>
  );
};

export const audioScenes: Record<string, React.FC<P>> = {OProofFrame, OParts, OStampsParts, OClaude};
