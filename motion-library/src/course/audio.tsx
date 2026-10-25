import React from 'react';
import {AbsoluteFill, Easing, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Type} from '../glass/kit';
import {AR, bi, CC, CourseBg, EN, G, Glass, Ico, lin, spr, Src} from './kit';

// Audio course (audioproduction, 2026-10-24): his 2021 online session, nothing cut, his audio untouched.
// Opening scenes + small tags used over the screen. Chapters come in PARTS (Aly: one broad category per group of chapters).
type P = {dur: number; [k: string]: any};
const Out: React.FC<{dur: number; children: React.ReactNode}> = ({dur, children}) => {
  const f = useCurrentFrame();
  const o = Math.min(lin(f, 0, 10), 1 - lin(f, dur - 9, dur, 0, 1, Easing.in(Easing.cubic)));
  return (
    <AbsoluteFill style={{opacity: o, filter: o < 0.99 ? `blur(${(1 - o) * 12}px)` : undefined}}>
      <CourseBg />
      {/* Aly review 2: screens + text were too big -> everything of the opening pages at 82 %, centred */}
      <AbsoluteFill style={{transform: 'scale(0.82)'}}>{children}</AbsoluteFill>
    </AbsoluteFill>
  );
};
const Center: React.FC<{y: number; children: React.ReactNode}> = ({y, children}) => (
  <div style={{position: 'absolute', left: 0, right: 0, top: y, display: 'flex', justifyContent: 'center'}}>{children}</div>
);

// A frame of the session itself, SMALL (Aly: the zoomed date was too pixelated), a gold box on the taskbar date; the date is
// written as clean text; most of the screen stays empty.
const OProofFrame: React.FC<P> = ({dur, img, box, line1, line2, line3}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 8, 120, 18);
  // Small card (Aly: "الشاشة نفسها تكون اصغر"), then a zoom INTO the date (source is 1280x720, so max ~2.2x of its own pixels: soft, not blocky).
  const W = 440, s = W / 1280, H = 720 * s;
  const hl = lin(f, 30, 40);
  const zp = lin(f, 44, 76, 0, 1, Easing.inOut(Easing.cubic));
  const Z = 2.2 / s, z = 1 + (Z - 1) * zp, k = s * z;
  const cx = box[0] + box[2] / 2, cy = box[1] + box[3] / 2;
  const tx = Math.min(0, Math.max(W - 1280 * k, W / 2 - cx * k)) * zp;
  const ty = Math.min(0, Math.max(H - 720 * k, H / 2 - cy * k)) * zp;
  return (
    <Out dur={dur}>
      <Center y={130}><Type text={line1} at={4} size={62} width={1600} /></Center>
      <div style={{position: 'absolute', left: 960, top: 450, transform: `translate(-50%,-50%) translateY(${(1 - p) * 50}px)`, opacity: Math.min(1, p * 1.3)}}>
        <Glass w={W + 20} pad={10} r={22} glow={G.gold}>
          <div style={{width: W, height: H, overflow: 'hidden', borderRadius: 14, position: 'relative', background: '#000'}}>
            <div style={{position: 'absolute', left: 0, top: 0, width: 1280, height: 720, transformOrigin: '0 0', transform: `translate(${tx}px,${ty}px) scale(${k})`}}>
              <Img src={staticFile(img)} style={{position: 'absolute', width: 1280, left: 0, top: 0}} />
              <div style={{position: 'absolute', left: box[0] - 8, top: box[1] - 5, width: box[2] + 16, height: box[3] + 10,
                border: `${3 / k}px solid ${G.gold}`, borderRadius: 6 / k, opacity: hl, boxShadow: `0 0 ${14 / k}px ${G.gold}`}} />
            </div>
          </div>
        </Glass>
      </div>
      <Center y={700}><Type text={line2} at={50} size={46} width={1600} color={G.soft} /></Center>
      {line3 ? <Center y={820}><Type text={line3} at={96} size={50} width={1600} pill={G.green} /></Center> : null}
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


// Cold-open teaser ("هتشوف في الكورس ده"): his clips play SMALLER in a card (layout 'teaser'), so it reads as a preview of
// what comes later; header + one progress segment per clip on top.
export const TeaserHead: React.FC<{dur: number; text: string; sub?: string; marks?: number[]}> = ({dur, text, sub, marks = []}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 140, 16);
  const o = Math.min(1, p * 1.3) * (1 - lin(f, dur - 8, dur, 0, 1));
  const t = f / fps;
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: 40, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14, opacity: o,
      transform: `translateY(${(1 - p) * -30}px)`, direction: 'rtl'}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 18}}>
        <div style={{width: 22, height: 22, borderRadius: '50%', background: '#FF5A5F', opacity: 0.5 + 0.5 * Math.sin(f / 4), boxShadow: '0 0 16px #FF5A5F'}} />
        <span style={{fontFamily: AR, fontWeight: 900, fontSize: 64, color: G.ink}}>{bi(text)}</span>
      </div>
      {sub ? <span style={{fontFamily: AR, fontWeight: 700, fontSize: 30, color: G.soft}}>{bi(sub)}</span> : null}
      <div style={{display: 'flex', gap: 10, direction: 'ltr', marginTop: 4}}>
        {marks.slice(0, -1).map((m, i) => {
          const k = Math.max(0, Math.min(1, (t - m) / (marks[i + 1] - m)));
          return <div key={i} style={{width: 150, height: 7, borderRadius: 4, background: 'rgba(255,255,255,0.18)', overflow: 'hidden'}}>
            <div style={{width: `${k * 100}%`, height: '100%', background: G.gold}} /></div>;
        })}
      </div>
    </div>
  );
};
// One teaser clip's promise (under the card): number, big words, the program, and WHERE in the course it comes.
export const TeaserCap: React.FC<{dur: number; text: string; app?: string; n?: number; total?: number; at?: string}> = ({dur, text, app, n, total, at}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 180, 14);
  const o = 1 - lin(f, dur - 5, dur, 0, 1);
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: 965, display: 'flex', justifyContent: 'center', opacity: Math.min(1, p * 1.5) * o}}>
      <div style={{transform: `translateY(-50%) scale(${0.85 + 0.15 * p})`, display: 'flex', alignItems: 'center', gap: 20, direction: 'rtl'}}>
        {n ? <div style={{padding: '4px 16px', borderRadius: 24, background: G.gold, fontFamily: EN, fontWeight: 900, fontSize: 32, color: '#14181F', direction: 'ltr'}}>{n}/{total}</div> : null}
        <span style={{fontFamily: AR, fontWeight: 900, fontSize: 62, color: G.ink, textShadow: '0 4px 20px rgba(0,0,0,0.6)'}}>{bi(text)}</span>
        {app ? <span style={{fontFamily: EN, fontWeight: 800, fontSize: 32, color: G.blue, direction: 'ltr'}}>{app}</span> : null}
        {at ? <span style={{padding: '4px 16px', borderRadius: 24, border: '2px solid rgba(255,255,255,0.3)', fontFamily: AR, fontWeight: 800, fontSize: 28, color: G.soft}}>
          في الدقيقة <span style={{fontFamily: EN, direction: 'ltr', unicodeBidi: 'isolate'}}>{at}</span></span> : null}
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
// Claude's opinion AS NUMBERS (Aly 2026-10-25): how much of each yardstick the course covers, each with its source.
// cards: [{head, v, n, of, unit, has, miss, src}] -> one ring per card.
const OCoverage: React.FC<P> = ({dur, q, sub, cards, foot}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const m = spr(f, fps, 2, 120, 14);
  const R = 96, C = 2 * Math.PI * R;
  // Aly review 4: the whole block centred vertically (with the link the cards are taller -> lift everything 70 px)
  const lift = cards.some((c: any) => c.link) ? -70 : 0;
  return (
    <Out dur={dur}>
      <AbsoluteFill style={{transform: `translateY(${lift}px)`}}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 50, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 24, direction: 'rtl'}}>
        <div style={{transform: `scale(${m})`}}><ClaudeMark s={0.9} spin={f * 0.6} /></div>
        <Type text={q} at={8} size={56} width={1400} />
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 150, textAlign: 'center', direction: 'rtl', fontFamily: AR, fontWeight: 700, fontSize: 30, color: G.soft, opacity: lin(f, 14, 28)}}>{bi(sub)}</div>
      <div style={{position: 'absolute', left: 70, right: 70, top: 225, display: 'flex', justifyContent: 'center', gap: 28, direction: 'rtl'}}>
        {cards.map((r: any, i: number) => {
          const at = 22 + i * 18;
          const p = spr(f, fps, at, 140, 16);
          const v = lin(f, at + 6, at + 46, 0, r.v, Easing.out(Easing.cubic));
          const col = r.v >= 0.75 ? G.green : r.v >= 0.5 ? G.gold : G.blue;
          return (
            <div key={i} style={{transform: `translateY(${(1 - p) * 60}px)`, opacity: Math.min(1, p * 1.4)}}>
              <Glass w={410} h={cards.some((c: any) => c.link) ? 880 : 720} pad={24} r={36} glow={col}>
                <div style={{display: 'flex', justifyContent: 'center'}}>
                  <svg width={230} height={230} viewBox="0 0 230 230">
                    <circle cx={115} cy={115} r={R} fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth={20} />
                    <circle cx={115} cy={115} r={R} fill="none" stroke={col} strokeWidth={20} strokeLinecap="round" strokeDasharray={`${C * v} ${C}`} transform="rotate(-90 115 115)" />
                    <text x={115} y={133} textAnchor="middle" fontFamily="Montserrat" fontWeight={900} fontSize={54} fill="#fff">{Math.round(v * 100)}%</text>
                  </svg>
                </div>
                <div style={{fontFamily: AR, fontWeight: 900, fontSize: 36, color: G.ink, textAlign: 'center', direction: 'rtl', lineHeight: 1.25, marginTop: 4}}>{bi(r.head)}</div>
                <div style={{fontFamily: AR, fontWeight: 800, fontSize: 27, color: col, textAlign: 'center', direction: 'rtl', marginTop: 8}}>{bi(`${r.n} من ${r.of} ${r.unit ?? 'نقطة'}`)}</div>
                {r.has ? <div style={{fontFamily: AR, fontWeight: 700, fontSize: 23, color: G.soft, textAlign: 'center', direction: 'rtl', lineHeight: 1.45, marginTop: 12}}>{bi(r.has)}</div> : null}
                {r.miss ? <div style={{fontFamily: AR, fontWeight: 700, fontSize: 22, color: '#FF8A7A', textAlign: 'center', direction: 'rtl', lineHeight: 1.45, marginTop: 10,
                  opacity: lin(f, at + 40, at + 52)}}>{bi('ناقص: ' + r.miss)}</div> : null}
                {r.ex ? <div style={{fontFamily: AR, fontWeight: 600, fontSize: 20, color: G.dim, textAlign: 'center', direction: 'rtl', lineHeight: 1.45, marginTop: 10,
                  opacity: lin(f, at + 46, at + 58)}}>{bi('اتشال من العدّ: ' + r.ex)}</div> : null}
                {r.link ? (  // Aly review 3: the full course of this program = its thumbnail + QR (a QR NEVER without the thumbnail)
                  <div style={{position: 'absolute', left: 20, right: 20, bottom: 76, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10,
                    opacity: lin(f, at + 56, at + 70), direction: 'rtl'}}>
                    <span style={{fontFamily: AR, fontWeight: 800, fontSize: 24, color: G.gold, textAlign: 'center'}}>{bi(r.link.text)}</span>
                    <div style={{display: 'flex', alignItems: 'center', gap: 12, direction: 'ltr'}}>
                      <Img src={staticFile(r.link.thumb)} style={{width: 200, height: 112, objectFit: 'cover', borderRadius: 10, border: '2px solid rgba(255,255,255,0.25)'}} />
                      <div style={{background: '#fff', padding: 6, borderRadius: 10}}><Img src={staticFile(r.link.qr)} style={{width: 100, height: 100, display: 'block'}} /></div>
                    </div>
                  </div>
                ) : null}
                <div style={{position: 'absolute', left: 0, right: 0, bottom: 22, display: 'flex', justifyContent: 'center'}}><Src text={r.src} s={0.72} /></div>
              </Glass>
            </div>
          );
        })}
      </div>
      {foot ? <Center y={cards.some((c: any) => c.link) ? 1135 : 985}><Type text={foot} at={95} size={36} width={1700} color={G.soft} pill={G.gold} /></Center> : null}
      </AbsoluteFill>
    </Out>
  );
};

// Claude's honest reasons to watch (Aly review 2: "قول انت تنصح بالفيديو ليه"); every reason = something really in the session.
const ORecommend: React.FC<P> = ({dur, q, rows}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const m = spr(f, fps, 2, 120, 14);
  return (
    <Out dur={dur}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 120, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 22, direction: 'rtl'}}>
        <div style={{transform: `scale(${m})`}}><ClaudeMark s={0.8} spin={f * 0.6} /></div>
        <Type text={q} at={6} size={56} width={1400} />
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 270, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 22}}>
        {rows.map((r: any, i: number) => {
          const p = spr(f, fps, 10 + i * 9, 160, 16);
          return (
            <div key={i} style={{transform: `translateX(${(1 - p) * 80}px)`, opacity: Math.min(1, p * 1.4)}}>
              <Glass w={1240} pad={22} r={28} glow={r.c}>
                <div style={{display: 'flex', alignItems: 'center', gap: 26, direction: 'rtl'}}>
                  <div style={{width: 84, height: 84, borderRadius: 24, background: `${r.c}22`, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>
                    <Ico n={r.ico} s={0.62} c={r.c} /></div>
                  <div style={{display: 'flex', flexDirection: 'column', gap: 6}}>
                    <span style={{fontFamily: AR, fontWeight: 900, fontSize: 42, color: G.ink}}>{bi(r.head)}</span>
                    <span style={{fontFamily: AR, fontWeight: 700, fontSize: 30, color: G.soft}}>{bi(r.sub)}</span>
                  </div>
                </div>
              </Glass>
            </div>
          );
        })}
      </div>
    </Out>
  );
};

// Last chapter "تتعلم إيه بعد كده" (Claude's picks): his own Premiere course (thumbnail + QR) + what the official guides have that
// this session didn't cover (the "ناقص" of the coverage cards), each with its source.
const ONextA: React.FC<P> = ({dur, course, rows, foot}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pc = spr(f, fps, 10, 130, 16);
  return (
    <Out dur={dur}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 70, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 20, direction: 'rtl'}}>
        <ClaudeMark s={0.8} spin={f * 0.6} />
        <Type text="تتعلم إيه بعد الكورس ده؟" at={4} size={58} width={1300} />
      </div>
      <div style={{position: 'absolute', left: 90, right: 90, top: 210, display: 'flex', gap: 40, direction: 'rtl', alignItems: 'flex-start'}}>
        <div style={{opacity: Math.min(1, pc * 1.4), transform: `translateY(${(1 - pc) * 50}px)`}}>
          <Glass w={760} pad={26} r={34} glow={CC.violet}>
            <div style={{fontFamily: AR, fontWeight: 900, fontSize: 40, color: G.ink, direction: 'rtl'}}>{bi(course.title)}</div>
            <div style={{fontFamily: AR, fontWeight: 700, fontSize: 28, color: G.soft, direction: 'rtl', marginTop: 8}}>{bi(course.sub)}</div>
            <div style={{display: 'flex', gap: 20, alignItems: 'center', marginTop: 22, direction: 'ltr'}}>
              <Img src={staticFile(course.thumb)} style={{width: 500, height: 281, objectFit: 'cover', borderRadius: 16, border: '2px solid rgba(255,255,255,0.25)'}} />
              <div style={{background: '#fff', padding: 10, borderRadius: 14}}><Img src={staticFile(course.qr)} style={{width: 170, height: 170, display: 'block'}} /></div>
            </div>
          </Glass>
        </div>
        <div style={{flex: 1, display: 'flex', flexDirection: 'column', gap: 18}}>
          {rows.map((r: any, i: number) => {
            const p = spr(f, fps, 30 + i * 14, 150, 16);
            return (
              <div key={i} style={{opacity: Math.min(1, p * 1.4), transform: `translateX(${(1 - p) * -60}px)`}}>
                <Glass w={890} pad={20} r={26} glow={G.blue}>
                  <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 16, direction: 'rtl'}}>
                    <div>
                      <div style={{fontFamily: AR, fontWeight: 900, fontSize: 34, color: G.ink}}>{bi(r.head)}</div>
                      <div style={{fontFamily: AR, fontWeight: 700, fontSize: 25, color: G.soft, marginTop: 4}}>{bi(r.sub)}</div>
                    </div>
                    <Src text={r.src} s={0.72} />
                  </div>
                </Glass>
              </div>
            );
          })}
        </div>
      </div>
      {foot ? <Center y={960}><Type text={foot} at={110} size={34} width={1700} color={G.soft} /></Center> : null}
    </Out>
  );
};

export const audioScenes: Record<string, React.FC<P>> = {OProofFrame, OParts, OStampsParts, OCoverage, ORecommend, ONextA};
