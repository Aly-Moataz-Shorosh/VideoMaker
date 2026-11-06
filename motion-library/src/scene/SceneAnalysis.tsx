import React from 'react';
import {AbsoluteFill, Img, interpolate, OffthreadVideo, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {fontCss} from '../blocks/theme';
import {Anim, KIND, MiniIcon, MoveGlyph, SC, SizeGlyph, kindIcon} from './anims';

// Scene analysis (Ibrahim El Abyad sc 55/56, 2026-11-06). 16:9. The film plays untouched (audio muxed later with ffmpeg).
// ONE place for each thing: film (top-left) · script (right: SOUND + PICTURE windows) · card strip (under the film) ·
// Premiere-style timeline (bottom). Props from projects/<code>/work/scripts/make_props.py.
export const sceneAnalysisSchema = z.object({
  duration: z.number().default(10),
  tc0: z.number().default(0),
  shots: z.array(z.any()).default([]),
  lines: z.array(z.any()).default([]),
  pics: z.array(z.any()).default([]),
  cards: z.array(z.any()).default([]),
  notes: z.array(z.any()).default([]),
  marks: z.array(z.any()).default([]),
  markers: z.array(z.any()).default([]),
  a1: z.array(z.any()).default([]),
  a2: z.array(z.any()).default([]),
  a3: z.array(z.any()).default([]),
});
type Props = z.infer<typeof sceneAnalysisSchema>;
const P = 'projects/ibrahim/';
const BG = '#0D1015', PANEL = '#141920', LINE = '#252C36', INK = '#EDEFF2', SOFT = '#9AA4B2', DIM = '#5B6573';
const AUD = '#2E9E6B';
const EN = 'Montserrat', AR = 'Cairo';
const VID = {x: 640, y: 78, w: 1240, h: 540};   // film RIGHT (Arabic eye starts right), script LEFT
const RC = {x: 40, w: 570};
const SW = {y: 78, h: 296};   // sound window
const PW = {y: 384, h: 234};  // picture window
const CARD = {x: 640, y: 632, w: 1240, h: 138};
const TL = {x: 40, y: 786, w: 1840, h: 278};
const SCN: Record<string, string> = {'55': 'Sc 55', '56': 'Sc 56', add: 'Film addition', x: 'Not in script'};
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const tc = (s: number) => {
  const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), x = s % 60;
  return `${h}:${String(m).padStart(2, '0')}:${x.toFixed(1).padStart(4, '0')}`;
};
const at = <T extends {t0: number; t1: number}>(arr: T[], t: number) => arr.find((a) => t >= a.t0 && t < a.t1);
const last = <T extends {t0: number; t1: number}>(arr: T[], t: number) => {
  let r: T | undefined;
  for (const a of arr) if (a.t0 <= t) r = a;
  return r;
};
const inOut = (t: number, t0: number, t1: number, k = 0.3) => interpolate(t, [t0, t0 + k, t1 - k, t1], [0, 1, 1, 0], clamp);

// ---------------- header ----------------
const Header: React.FC = () => (
  <div style={{position: 'absolute', left: 40, top: 14, width: 1840, height: 52, display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
    <div style={{display: 'flex', alignItems: 'center', gap: 12}}>
      <Img src={staticFile(P + 'ch_face.png')} style={{height: 46}} />
      <Img src={staticFile(P + 'ch_name.png')} style={{height: 26}} />
    </div>
    <div style={{direction: 'rtl', textAlign: 'right'}}>
      <div style={{fontFamily: AR, fontWeight: 800, fontSize: 26, color: INK, lineHeight: 1.1}}>تحليل مشهد · إبراهيم الأبيض (2009)</div>
      <div style={{fontFamily: AR, fontWeight: 600, fontSize: 15, color: SOFT}}>إخراج مروان حامد · سيناريو عباس أبو الحسن · تصوير سامح سليم · خام 35 مم</div>
    </div>
  </div>
);

// ---------------- film + shot label + marks ----------------
const Label: React.FC<{icon: string; c: string; text: string; sub?: string; o?: number}> = ({icon, c, text, sub, o = 1}) => (
  <div style={{display: 'flex', alignItems: 'center', gap: 12, opacity: o}}>
    <div style={{width: 56, height: 36, border: `3px solid ${c}`, borderRadius: 6, background: 'rgba(10,12,16,0.55)', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <MiniIcon k={icon} c={INK} />
    </div>
    <div style={{fontFamily: EN, fontWeight: 800, fontSize: 22, color: '#fff', letterSpacing: 1.2, textShadow: '0 2px 6px rgba(0,0,0,0.85)', whiteSpace: 'nowrap'}}>
      {text}{sub && <span style={{fontWeight: 600, color: '#D6DCE4'}}>{sub}</span>}
    </div>
  </div>
);


// Shot label: every term gets its own drawing (size = framed person, move = looping mini animation).
const ShotLabel: React.FC<{shot: any; c: string; o: number}> = ({shot, c, o}) => {
  const T = {fontFamily: EN, fontWeight: 800, fontSize: 22, color: '#fff', letterSpacing: 1.2, textShadow: '0 2px 6px rgba(0,0,0,0.85)', whiteSpace: 'nowrap' as const};
  const G = {background: 'rgba(10,12,16,0.6)', borderRadius: 6, padding: '2px 3px', display: 'flex', boxShadow: `0 0 0 2px ${c}`};
  const sep = (x: string, k: string) => <span key={k} style={{...T, color: '#AEB6C2', fontWeight: 600}}>{x}</span>;
  const term = (g: React.ReactNode, txt: string, k: string) => (
    <span key={k} style={{display: 'flex', alignItems: 'center', gap: 7}}><span style={G}>{g}</span><span style={{...T, fontWeight: 700}}>{txt}</span></span>);
  const parts: React.ReactNode[] = [];
  shot.size.split('→').map((x: string) => x.trim()).forEach((x: string, i: number) => {
    if (i) parts.push(sep('→', 'sa' + i));
    parts.push(term(<SizeGlyph k={x} />, x, 'sz' + i));
  });
  const toks = [shot.extra, shot.move].filter(Boolean).join(' · ').split(/( \+ | · | → )/);
  toks.forEach((x: string, i: number) => {
    if (!x.trim()) return;
    if (/^ (\+|·|→) $/.test(x)) { parts.push(sep(x.trim(), 'mp' + i)); return; }
    const tx = x.trim();
    parts.push(term(/^(OTS|CU|MCU|MS|MLS|LS|WS|ELS|ECU|Insert)$/.test(tx) ? <SizeGlyph k={tx} /> : <MoveGlyph k={x} />, tx, 'mv' + i));
  });
  return <div style={{display: 'flex', alignItems: 'center', gap: 10, opacity: o, flexWrap: 'nowrap'}}>
    <span style={{...T, fontWeight: 900, background: c, color: '#0D1015', textShadow: 'none', borderRadius: 6, padding: '2px 10px'}}>SHOT {shot.n}</span>
    {sep('·', 'd0')}{parts}
  </div>;
};

const Film: React.FC<Props> = (p) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  const shot = p.shots.find((s: any) => t >= s.s && t < s.e) ?? p.shots[p.shots.length - 1];
  const sinceCut = t - shot.s;
  const lo = interpolate(sinceCut, [0, 0.18], [0.35, 1], clamp);
  const mark = at(p.marks as any[], t);
  return (
    <div style={{position: 'absolute', left: VID.x, top: VID.y, width: VID.w, height: VID.h, borderRadius: 10, overflow: 'hidden', background: '#000',
      boxShadow: '0 0 0 1px #20262F'}}>
      <OffthreadVideo src={staticFile(P + 'scene.mp4')} muted style={{width: VID.w, height: VID.h}} />
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 120, background: 'linear-gradient(transparent, rgba(0,0,0,0.6))'}} />
      <div style={{position: 'absolute', left: 22, bottom: 18}}>
        <ShotLabel shot={shot} c={SC[shot.scene]} o={lo} />
      </div>
      {mark && (() => {
        const o = inOut(t, mark.t0, mark.t1, 0.25);
        const b = mark.box;
        return <>
          {b && <div style={{position: 'absolute', left: b[0] * VID.w, top: b[1] * VID.h, width: (b[2] - b[0]) * VID.w, height: (b[3] - b[1]) * VID.h,
            border: `3px solid ${KIND.camera}`, borderRadius: 8, opacity: o, boxShadow: '0 0 0 1px rgba(0,0,0,0.5)'}} />}
          {mark.arrow && <Arrow k={mark.arrow} o={o} t={t - mark.t0} />}
          <div style={{position: 'absolute', left: b ? b[0] * VID.w + 14 : 22, top: b ? b[1] * VID.h + 12 : 20}}>
            <Label icon={mark.icon} c={KIND.camera} text={mark.term} o={o} />
          </div>
        </>;
      })()}
    </div>
  );
};
const Arrow: React.FC<{k: string; o: number; t: number}> = ({k, o, t}) => {
  const p = interpolate(t, [0.1, 1.4], [0, 1], clamp);
  const d = k === 'arc' ? 'M300 420 Q620 520 940 420' : 'M520 470 L520 230 Q520 170 600 170 L820 170';
  const len = 900;
  return <svg width={VID.w} height={VID.h} style={{position: 'absolute', left: 0, top: 0, opacity: o}}>
    <path d={d} stroke={KIND.camera} strokeWidth={5} fill="none" strokeLinecap="round" strokeDasharray={len} strokeDashoffset={len * (1 - p)} />
    <path d={d} stroke="rgba(0,0,0,0.35)" strokeWidth={9} fill="none" strokeLinecap="round" strokeDasharray={len} strokeDashoffset={len * (1 - p)} style={{mixBlendMode: 'multiply'}} />
  </svg>;
};

// ---------------- script windows ----------------
const PAGE_W = 595, PX = 3; // page images rendered 3 px / pt
const Win: React.FC<{y: number; h: number; head: React.ReactNode; color: string; target: any; prev: any; k: number; dimHl?: boolean; foot?: React.ReactNode; empty?: React.ReactNode}> = (
  {y, h, head, color, target, prev, k, dimHl, foot, empty}) => {
  const HEAD = 34;
  const bodyH = h - HEAD;
  const view = (r: any) => {
    const vw = Math.max(330, r[3] - r[1] + 24);
    const s = RC.w / vw;
    return {page: r[0], s, cx: (r[1] + r[3]) / 2, cy: (r[2] + r[4]) / 2, r};
  };
  const a = target?.r && target.r[0] ? view(target.r) : null;
  const b = prev?.r && prev.r[0] ? view(prev.r) : a;
  const mix = (u: number, v: number) => (b ? v + (u - v) * k : u);
  const pageImg = (vv: any, o: number) => {
    const s = vv.s;
    const left = RC.w / 2 - vv.cx * s;
    const top = bodyH / 2 - vv.cy * s;
    return <Img key={vv.page} src={staticFile(`${P}p${vv.page}.png`)} style={{position: 'absolute', left, top, width: PAGE_W * s, opacity: o}} />;
  };
  let body: React.ReactNode = empty;
  if (a) {
    const same = b && b.page === a.page;
    const s = same ? mix(a.s, b!.s) : a.s;
    const cx = same ? mix(a.cx, b!.cx) : a.cx, cy = same ? mix(a.cy, b!.cy) : a.cy;
    const cur = {page: a.page, s, cx, cy};
    const r = a.r;
    const hl = {x: RC.w / 2 + (r[1] - cx) * s - 6, y: bodyH / 2 + (r[2] - cy) * s - 3, w: (r[3] - r[1]) * s + 12, h: (r[4] - r[2]) * s + 6};
    body = <>
      <div style={{position: 'absolute', inset: 0, background: '#fff'}} />
      {!same && b && pageImg(b, 1 - k)}
      {pageImg(cur, same ? 1 : k)}
      <div style={{position: 'absolute', left: hl.x, top: hl.y, width: hl.w, height: hl.h, border: `3px solid ${color}`, borderRadius: 6,
        background: dimHl ? 'transparent' : `${color}22`, opacity: dimHl ? 0.45 : k}} />
    </>;
  }
  return (
    <div style={{position: 'absolute', left: RC.x, top: y, width: RC.w, height: h, borderRadius: 10, overflow: 'hidden', background: PANEL, boxShadow: `0 0 0 1px ${LINE}`}}>
      <div style={{height: HEAD, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 12px', borderBottom: `3px solid ${color}`, background: '#10141A'}}>{head}</div>
      <div style={{position: 'absolute', top: HEAD, left: 0, width: RC.w, height: bodyH, overflow: 'hidden'}}>
        {body}
        {foot}
      </div>
    </div>
  );
};
const Chip: React.FC<{c: string; children: React.ReactNode}> = ({c, children}) => (
  <span style={{fontFamily: EN, fontWeight: 800, fontSize: 14, color: '#0D1015', background: c, borderRadius: 5, padding: '2px 8px', letterSpacing: 0.8}}>{children}</span>
);
const Empty: React.FC<{title: string; ar: string}> = ({title, ar}) => (
  <div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 8, background: '#171C23'}}>
    <div style={{fontFamily: EN, fontWeight: 800, fontSize: 20, color: SC.x, letterSpacing: 2, border: `2px solid ${SC.x}`, borderRadius: 6, padding: '4px 12px'}}>{title}</div>
    <div style={{fontFamily: AR, fontWeight: 700, fontSize: 20, color: SOFT, direction: 'rtl', textAlign: 'center', padding: '0 28px'}}>{ar}</div>
  </div>
);

const Script: React.FC<Props> = (p) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  const L = p.lines as any[];
  // SOUND: current line (or the last one, dimmed) ; before the first line -> scene heading of p.97
  const HEAD0 = {t0: 0, t1: 7.4, r: [97, 40, 36, 556, 92], spk: '', scene: '55', diff: ''};
  const cur = at(L, t);
  const lst = last(L, t) ?? HEAD0;
  const tg = cur ?? lst;
  const idx = L.indexOf(tg);
  const prev = idx > 0 ? L[idx - 1] : HEAD0;
  const k = spring({frame: f - Math.round(tg.t0 * fps), fps, config: {damping: 200}, durationInFrames: 14});
  const sc = SC[tg.scene];
  const page = tg.r?.[0] ? `p.${tg.r[0]}` : '';
  const soundHead = <>
    <span style={{display: 'flex', gap: 8, alignItems: 'center'}}><Chip c={sc}>SOUND</Chip>
      <span style={{fontFamily: EN, fontWeight: 700, fontSize: 15, color: INK}}>{SCN[tg.scene]} {page && `· ${page}`}</span></span>
    <span style={{fontFamily: EN, fontWeight: 800, fontSize: 15, color: cur ? INK : DIM, letterSpacing: 1}}>{cur ? tg.spk : (t < 7.4 ? 'NO DIALOGUE YET' : '…')}</span>
  </>;
  const diffO = cur && tg.diff && tg.r?.[0] ? inOut(t, tg.t0, Math.max(tg.t1, tg.t0 + 2.6), 0.25) : 0;
  const foot = diffO > 0 ? (
    <div style={{position: 'absolute', left: 10, right: 10, bottom: 10, opacity: diffO, background: '#1B2129', border: `2px solid ${SC['56']}`, borderRadius: 8,
      padding: '6px 12px', display: 'flex', gap: 10, alignItems: 'center', direction: 'rtl'}}>
      <span style={{fontFamily: AR, fontWeight: 700, fontSize: 18, color: INK, lineHeight: 1.35}}>{tg.diff}</span>
      <span style={{direction: 'ltr', flex: 'none'}}><Chip c={SC['56']}>FILM ≠ SCRIPT</Chip></span>
    </div>) : null;
  const notIn = tg.r && !tg.r[0];
  // PICTURE
  const pic = at(p.pics as any[], t) ?? (p.pics as any[])[p.pics.length - 1];
  const pi = (p.pics as any[]).indexOf(pic);
  const pprev = pi > 0 ? (p.pics as any[])[pi - 1] : pic;
  const pk = interpolate(f - Math.round(pic.t0 * fps), [0, 6], [0, 1], clamp);
  const samePic = pprev && pprev.r && pic.r && pprev.r.join() === pic.r.join();
  const cross = pic.scene !== tg.scene && pic.scene !== 'x' && t > 92 && t < 191;
  return <>
    <Win y={SW.y} h={SW.h} color={sc} target={notIn ? null : tg} prev={notIn ? null : prev} k={k} dimHl={!cur} head={soundHead} foot={foot}
      empty={<Empty title="NOT IN SCRIPT (V10)" ar={tg.diff?.replace('مش مكتوبة في السيناريو: ', '') ?? ''} />} />
    <Win y={PW.y} h={PW.h} color={SC[pic.scene]} target={pic.r ? pic : null} prev={samePic ? pic : pprev?.r ? pprev : null} k={samePic ? 1 : pk}
      head={<>
        <span style={{display: 'flex', gap: 8, alignItems: 'center'}}><Chip c={SC[pic.scene]}>PICTURE</Chip>
          <span style={{fontFamily: EN, fontWeight: 700, fontSize: 15, color: INK}}>{SCN[pic.scene]}{pic.r ? ` · p.${pic.r[0]}` : ''}</span></span>
        {cross ? <span style={{fontFamily: EN, fontWeight: 900, fontSize: 13, letterSpacing: 1.5, color: '#0D1015', background: INK, borderRadius: 4, padding: '2px 8px'}}>SOUND ≠ PICTURE · CROSS-CUTTING</span>
          : <span style={{fontFamily: EN, fontWeight: 700, fontSize: 14, color: SOFT}}>SHOT {(p.shots as any[])[pi]?.n}</span>}
      </>}
      empty={<Empty title="NOT IN SCENE 55" ar="سطح بالليل وإبراهيم لوحده — مش مكتوب في مشهد 55" />} />
    {pic.scene === 'add' && <div style={{position: 'absolute', left: RC.x + 10, top: PW.y + PW.h - 52, width: RC.w - 20, direction: 'rtl', background: '#1B2129',
      border: `2px solid ${SC.add}`, borderRadius: 8, padding: '4px 12px', fontFamily: AR, fontWeight: 700, fontSize: 17, color: INK}}>
      مش مكتوبة كمشهد — تجسيد لـ «لسان آدمي» (ص 99)</div>}
  </>;
};

// ---------------- card strip (under the film) ----------------
const Cards: React.FC<Props> = (p) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  const c = at(p.cards as any[], t);
  const n = at(p.notes as any[], t);
  const bars = (p.shots as any[]).map((s) => ({d: s.e - s.s, sc: s.scene}));
  return <div style={{position: 'absolute', left: CARD.x, top: CARD.y, width: CARD.w, height: CARD.h}}>
    {c && (() => {
      const lf = f - Math.round(c.t0 * fps);
      const sp = spring({frame: lf, fps, config: {damping: 18, mass: 0.7}});
      const o = Math.min(sp, interpolate(t, [c.t1 - 0.3, c.t1], [1, 0], clamp));
      const col = KIND[c.kind as keyof typeof KIND];
      return <div style={{position: 'absolute', inset: 0, opacity: o, transform: `translateY(${(1 - sp) * 18}px)`, background: PANEL, borderRadius: 12,
        boxShadow: `0 0 0 1px ${LINE}`, display: 'flex', alignItems: 'center', overflow: 'hidden'}}>
        <div style={{width: 6, alignSelf: 'stretch', background: col}} />
        <div style={{width: 232, display: 'flex', justifyContent: 'center'}}>
          <div style={{width: 200, height: 116}}>
            <Sequence from={Math.round(c.t0 * fps)} layout="none"><Anim k={c.anim} c={col} lead={c.lead} bars={bars} /></Sequence>
          </div>
        </div>
        <div style={{flex: 1, paddingRight: 30, display: 'flex', flexDirection: 'column', gap: 8}}>
          <div style={{display: 'flex', alignItems: 'center', gap: 14}}>
            <span style={{display: 'flex', alignItems: 'center', gap: 4, fontFamily: EN, fontWeight: 800, fontSize: 14, letterSpacing: 2, color: col}}>
              <MiniIcon k={kindIcon(c.kind)} c={col} />{c.kind === 'edit' ? 'EDITING' : c.kind === 'sound' ? 'SOUND DESIGN' : 'CAMERA'}</span>
            <span style={{fontFamily: EN, fontWeight: 900, fontSize: 40, color: '#fff', letterSpacing: 0.5}}>{c.term}</span>
          </div>
          <div style={{fontFamily: AR, fontWeight: 700, fontSize: 25, color: '#D9DEE5', direction: 'rtl', textAlign: 'right', lineHeight: 1.3}}>{c.ar}</div>
        </div>
      </div>;
    })()}
    {!c && n && (() => {
      const o = inOut(t, n.t0, n.t1);
      return <div style={{position: 'absolute', left: 0, bottom: 0, height: 52, opacity: o, display: 'flex', alignItems: 'center', gap: 12, background: PANEL,
        borderRadius: 10, padding: '0 18px', boxShadow: `0 0 0 1px ${LINE}`}}>
        <span style={{fontFamily: EN, fontWeight: 800, fontSize: 14, letterSpacing: 2, color: SOFT}}>NOTE · {n.k}</span>
        <span style={{fontFamily: AR, fontWeight: 700, fontSize: 21, color: INK, direction: 'rtl'}}>{n.txt}</span>
      </div>;
    })()}
  </div>;
};

// ---------------- legend ----------------
const Legend: React.FC = () => {
  const row = (c: string, en: string, ar: string, sq = true) => (
    <div style={{display: 'flex', alignItems: 'center', gap: 8, height: 22}}>
      <span style={{width: sq ? 22 : 10, height: sq ? 12 : 16, borderRadius: 3, background: c, flex: 'none'}} />
      <span style={{fontFamily: EN, fontWeight: 700, fontSize: 13, color: INK, whiteSpace: 'nowrap'}}>{en}</span>
      <span style={{fontFamily: AR, fontWeight: 600, fontSize: 14, color: SOFT, direction: 'rtl', whiteSpace: 'nowrap'}}>{ar}</span>
    </div>
  );
  return <div style={{position: 'absolute', left: RC.x, top: CARD.y, width: RC.w, height: CARD.h, background: PANEL, borderRadius: 10, boxShadow: `0 0 0 1px ${LINE}`,
    padding: '10px 14px', display: 'flex', gap: 18, boxSizing: 'border-box'}}>
    <div style={{display: 'flex', flexDirection: 'column', gap: 2}}>
      <span style={{fontFamily: EN, fontWeight: 800, fontSize: 12, color: DIM, letterSpacing: 2}}>V1 · PICTURE</span>
      {row(SC['55'], 'Sc 55', 'بهو الجلوس')}
      {row(SC['56'], 'Sc 56', 'Photo Montage')}
      {row(SC.add, 'Film addition', 'مش مكتوبة كمشهد')}
      {row(SC.x, 'Not in script', 'مش في السيناريو')}
    </div>
    <div style={{display: 'flex', flexDirection: 'column', gap: 2}}>
      <span style={{fontFamily: EN, fontWeight: 800, fontSize: 12, color: DIM, letterSpacing: 2}}>A · SOUND / MARKERS</span>
      {row(AUD, 'Audio clip', 'صوت')}
      {row(KIND.edit, 'Editing', 'مونتاج', false)}
      {row(KIND.sound, 'Sound Design', 'صوت', false)}
      {row(KIND.camera, 'Camera', 'كاميرا', false)}
    </div>
  </div>;
};

// ---------------- Premiere-style timeline ----------------
const Timeline: React.FC<Props> = (p) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  const LBL = 112, X0 = LBL, CW = TL.w - LBL - 8;
  const WIN = 22;                           // seconds visible in the zoom window
  const pps = CW / WIN;
  const PH = 0.36;                          // playhead position in the window
  const v0 = Math.min(Math.max(0, t - WIN * PH), p.duration - WIN);
  const X = (s: number) => X0 + (s - v0) * pps;
  const phx = X(t);
  const R = {head: 0, ov: 28, ru: 54, mk: 78, v1: 106, a1: 162, a2: 202, a3: 236};
  const H = {v1: 50, a1: 34, a2: 28, a3: 28};
  const OW = TL.w - 16;
  const OX = (s: number) => 8 + (s / p.duration) * OW;
  const card = at(p.cards as any[], t);
  const hot = (name: string) => !!card && name.toLowerCase().includes(card.term.toLowerCase().slice(0, 6));
  const vis = (s: number, e: number) => e > v0 - 1 && s < v0 + WIN + 1;
  const track = (y: number, h: number, name: string, sub = '') => <g>
    <rect x={0} y={y} width={LBL - 6} height={h} rx={4} fill="#1A2029" />
    <text x={10} y={y + h / 2 + 5} fill={INK} fontFamily={EN} fontWeight={800} fontSize={14}>{name}</text>
    {sub && <text x={40} y={y + h / 2 + 5} fill={SOFT} fontFamily={EN} fontWeight={600} fontSize={11}>{sub}</text>}
    <rect x={X0} y={y} width={CW} height={h} fill="#12161C" />
  </g>;
  const clip = (s: number, e: number, y: number, h: number, c: string, label: string, key: string, o = 1, stripe = false) => {
    if (!vis(s, e)) return null;
    const x = Math.max(X0, X(s)), x2 = Math.min(X0 + CW, X(e));
    if (x2 - x < 1) return null;
    const w = x2 - x;
    return <g key={key} opacity={o}>
      <rect x={x + 0.5} y={y + 2} width={Math.max(0, w - 1)} height={h - 4} rx={3} fill={c} />
      {stripe && <rect x={x + 0.5} y={y + 2} width={Math.max(0, w - 1)} height={h - 4} rx={3} fill="url(#stripe)" />}
      {w > 26 && <text x={x + 6} y={y + h / 2 + 5} fill="#0D1015" fontFamily={EN} fontWeight={800} fontSize={13}
        clipPath={`inset(0 0 0 0)`}>{w > 96 ? label : w > 50 ? label.split(' ')[0] : label.split(' ')[0].slice(0, 3)}</text>}
    </g>;
  };
  // ruler ticks every 1 s, labels every 2 s (film TC)
  const ticks: React.ReactNode[] = [];
  for (let s = Math.floor(v0); s <= v0 + WIN; s++) {
    const x = X(s);
    if (x < X0) continue;
    ticks.push(<line key={'t' + s} x1={x} y1={R.ru + (s % 2 ? 14 : 8)} x2={x} y2={R.ru + 22} stroke={DIM} strokeWidth={1} />);
    if (s % 2 === 0) ticks.push(<text key={'l' + s} x={x + 3} y={R.ru + 12} fill={SOFT} fontFamily={EN} fontWeight={600} fontSize={11}>{tc(p.tc0 + s).replace('.0', '')}</text>);
  }
  const cross = (p.markers as any[]).find((m) => m.region);
  return <div style={{position: 'absolute', left: TL.x, top: TL.y, width: TL.w, height: TL.h, background: '#0F1318', borderRadius: 10, boxShadow: `0 0 0 1px ${LINE}`, overflow: 'hidden'}}>
    <svg width={TL.w} height={TL.h}>
      <defs>
        <pattern id="stripe" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="3" height="8" fill="rgba(0,0,0,0.25)" /></pattern>
      </defs>
      {/* header */}
      <text x={10} y={19} fill={SOFT} fontFamily={EN} fontWeight={700} fontSize={13}>SEQUENCE  Ibrahim_ElAbyad_Sc55-56</text>
      <text x={TL.w - 10} y={20} textAnchor="end" fill="#F2C94C" fontFamily={EN} fontWeight={800} fontSize={18}>{tc(p.tc0 + t)}</text>
      <text x={TL.w - 150} y={19} textAnchor="end" fill={DIM} fontFamily={EN} fontWeight={700} fontSize={12}>FILM TC ≈</text>
      {/* overview (whole scene) */}
      {(p.shots as any[]).map((s) => <rect key={'o' + s.n} x={OX(s.s)} y={R.ov} width={Math.max(1, OX(s.e) - OX(s.s) - 0.6)} height={14} fill={SC[s.scene]} opacity={0.85} />)}
      <rect x={OX(v0)} y={R.ov - 3} width={OX(v0 + WIN) - OX(v0)} height={20} rx={3} fill="none" stroke="#fff" strokeWidth={2} />
      <line x1={OX(t)} y1={R.ov - 4} x2={OX(t)} y2={R.ov + 18} stroke="#FF4D4D" strokeWidth={2} />
      {/* ruler */}
      <rect x={X0} y={R.ru} width={CW} height={22} fill="#161B22" />
      {ticks}
      {/* region: cross-cutting */}
      {cross && vis(cross.region[0], cross.region[1]) && <g>
        <rect x={Math.max(X0, X(cross.region[0]))} y={R.mk + 18} width={Math.min(X0 + CW, X(cross.region[1])) - Math.max(X0, X(cross.region[0]))} height={6} rx={3} fill={KIND.edit} opacity={0.5} />
      </g>}
      {/* tracks */}
      {track(R.v1, H.v1, 'V1', 'Shots')}
      {track(R.a1, H.a1, 'A1', 'Dialogue')}
      {track(R.a2, H.a2, 'A2', 'Music')}
      {track(R.a3, H.a3, 'A3', 'SFX')}
      {(p.shots as any[]).map((s) => clip(s.s, s.e, R.v1, H.v1, SC[s.scene], `${s.n} · ${s.size}`, 'v' + s.n))}
      {(p.a1 as any[]).map((a, i) => clip(a.s, a.e, R.a1, H.a1, AUD, a.name + (a.echo ? ' (echo)' : ''), 'a1' + i, 1, a.echo))}
      {(p.a2 as any[]).map((a, i) => <g key={'a2' + i}>{clip(a.s, a.e, R.a2, H.a2, '#3F7F68', a.name, 'a2c' + i)}
        {a.fadeOut && vis(a.fadeOut, a.e) && <path d={`M${X(a.fadeOut)} ${R.a2 + 3} L${X(a.e)} ${R.a2 + H.a2 - 3}`} stroke="#0D1015" strokeWidth={2.5} />}</g>)}
      {(p.a3 as any[]).map((a, i) => clip(a.s, a.e, R.a3, H.a3, '#5FBF8F', a.name, 'a3' + i))}
      {/* markers + lead-in spans */}
      {(p.markers as any[]).map((m, i) => {
        const c = KIND[m.kind as keyof typeof KIND];
        const on = hot(m.name);
        const els: React.ReactNode[] = [];
        if (m.span && vis(m.span[0], m.span[1])) {
          const xa = X(m.span[0]), xb = X(m.span[1]);
          const o = on ? 1 : 0.55;
          els.push(<g key={'sp' + i} opacity={o}>
            {xa >= X0 && <line x1={xa} y1={R.a1 - 2} x2={xa} y2={R.a3 + H.a3} stroke={c} strokeWidth={2} strokeDasharray="5 4" />}
            {xb >= X0 && <line x1={xb} y1={R.v1} x2={xb} y2={R.a3 + H.a3} stroke="#FF6B6B" strokeWidth={2} strokeDasharray="5 4" />}
            <rect x={Math.max(X0, xa)} y={R.a1 + H.a1 - 2} width={Math.max(0, Math.min(X0 + CW, xb) - Math.max(X0, xa))} height={4} fill={c} />
            {(xa + xb) / 2 > X0 + 30 && <g>
              <rect x={(xa + xb) / 2 - 34} y={R.a1 + H.a1 - 12} width={68} height={20} rx={4} fill="#0D1015" stroke={c} strokeWidth={1.5} />
              <text x={(xa + xb) / 2} y={R.a1 + H.a1 + 3} textAnchor="middle" fill={INK} fontFamily={EN} fontWeight={800} fontSize={13}>{`${(m.span[1] - m.span[0]).toFixed(1)} s`}</text>
            </g>}
          </g>);
        }
        if (vis(m.t, m.t)) {
          const x = X(m.t);
          if (x >= X0) els.push(<g key={'m' + i}>
            <path d={`M${x} ${R.mk} l7 0 l0 9 l-7 6 l-7 -6 l0 -9 z`} fill={c} opacity={on ? 1 : 0.8} />
            <text x={x + 10} y={R.mk + 12} fill={on ? '#fff' : c} fontFamily={EN} fontWeight={800} fontSize={13}>{m.name}</text>
          </g>);
        }
        return <g key={'mm' + i}>{els}</g>;
      })}
      {/* playhead */}
      <line x1={phx} y1={R.ru} x2={phx} y2={TL.h} stroke="#FF4D4D" strokeWidth={2} />
      <path d={`M${phx - 7} ${R.ru} l14 0 l0 8 l-7 7 l-7 -7 z`} fill="#FF4D4D" />
    </svg>
  </div>;
};

export const SceneAnalysis: React.FC<Props> = (p) => (
  <AbsoluteFill style={{background: BG}}>
    <style>{fontCss}</style>
    <Header />
    <Film {...p} />
    <Script {...p} />
    <Cards {...p} />
    <Legend />
    <Timeline {...p} />
  </AbsoluteFill>
);
