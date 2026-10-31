import React from 'react';
import {AbsoluteFill, Easing, Img, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, EN, lin, rnd, spr} from '../film/kit';

// "Stage" look (New Stage 19 lecture shorts, 2026-10-18): a lecture turned into viral shorts.
// Learned from Aly's references: podcast clips (hook sentence first, then back to the start; big captions, one word lit),
// IG explainers (one headline that stays the whole short, a keyword boxed in yellow, one clean visual per sentence, big numbers,
// little actors that DO what he says). Colours = his slides (white-blue-violet-red ribbons) on a deep night stage.
export const S = {
  night: '#070912', night2: '#0E1222', ink: '#0B0D16', white: '#F6F7FB', soft: '#AEB4C8', dim: '#5E6680',
  blue: '#2F6BFF', violet: '#7B5CFF', red: '#FF3D6E', cyan: '#22D3EE', green: '#2BD17E', yellow: '#FFD43B',
};
export {AR, EN, lin, spr, rnd};
export const W = 1080, H = 1920;
// layout (IG/TikTok/YT safe zones: top 0–110 and bottom 1650+ and the right icon column are covered by the apps)
export const L = {tag: 118, head: 178, stageTop: 430, stageH: 830, cap: 1050, badge: 1452};
// v2 (Aly 2026-10-19: "اكون مالي الشاشة كاملة… موجود طول الفيديو"): his hall camera fills the whole 9:16 frame, following him;
// scenes are drawn in the old stage box (y 430–1260) and shown scaled into the TRAY over the seats under his feet.
export const TRAY = {y: 1150, h: 550, k: 0.66};

// split into words but keep a run of English words together ("Install the app" stayed reversed in RTL flex rows, short 3 v3)
export const groupLatin = (t: string) => t.split(' ').reduce((acc: string[], w) => {
  const lat = /^[*_]*[A-Za-z0-9][A-Za-z0-9.\-+'_]*[*_.,؟?!:]*$/.test(w);
  const prev = acc[acc.length - 1];
  if (lat && prev !== undefined && /^[*_]*[A-Za-z0-9][A-Za-z0-9.\-+'_ ]*[*_.,؟?!:]*$/.test(prev) && !prev.endsWith('*') && !w.startsWith('*')) acc[acc.length - 1] = prev + ' ' + w;
  else acc.push(w);
  return acc;
}, []);
export const bi = (s: string) => (s ?? '').replace(/[A-Za-z0-9][A-Za-z0-9 .+:>&\/'-]*[A-Za-z0-9]|[A-Za-z0-9]/g, (m) => '⁦' + m + '⁩');

// ---------- background: night stage, his slide ribbons flowing slowly, a spotlight, fine grain ----------
const ribbon = (f: number, k: number, y0: number, amp: number) => {
  const pts: string[] = [];
  for (let i = 0; i <= 12; i++) {
    const x = -100 + i * 110;
    const y = y0 + amp * Math.sin(i * 0.55 + f / (70 + k * 13) + k) + 40 * Math.sin(i * 1.3 + f / 50 + k * 2);
    pts.push(`${x},${y}`);
  }
  return 'M' + pts.join(' L');
};
export const StageBg: React.FC<{hue?: number}> = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: `radial-gradient(120% 70% at 50% 30%, ${S.night2} 0%, ${S.night} 70%)`}}>
      <svg width={W} height={H} style={{position: 'absolute', inset: 0, filter: 'blur(26px)', opacity: 0.55}}>
        <defs>
          <linearGradient id="rb" x1="0" x2="1"><stop offset="0" stopColor={S.blue} /><stop offset="0.5" stopColor={S.violet} /><stop offset="1" stopColor={S.red} /></linearGradient>
        </defs>
        {[0, 1, 2, 3, 4].map((k) => <path key={k} d={ribbon(f, k, 1560 + k * 34, 70)} stroke="url(#rb)" strokeWidth={26 - k * 3} fill="none" opacity={0.75 - k * 0.1} />)}
        {[0, 1, 2].map((k) => <path key={'t' + k} d={ribbon(f + 300, k + 5, 360 + k * 40, 50)} stroke="url(#rb)" strokeWidth={14 - k * 3} fill="none" opacity={0.35} />)}
      </svg>
      <AbsoluteFill style={{background: `radial-gradient(40% 28% at ${50 + 6 * Math.sin(f / 80)}% 44%, rgba(120,140,255,0.13) 0%, transparent 70%)`}} />
      <Img src={staticFile(`bg/grain_${Math.floor(f / 2) % 3}.png`)} style={{position: 'absolute', width: W, height: H, opacity: 0.12, mixBlendMode: 'screen'}} />
    </AbsoluteFill>
  );
};

// ---------- the frame that stays: progress bar, series tag, the headline (hook question) with its key word boxed ----------
// pal / tag: other shows reuse the frame in their own colours (enta cs shorts 2026-10-21)
export type Pal = {box: string; boxInk: string; bar: string[]; now: string; hl: string};
export const STAGE_PAL: Pal = {box: S.yellow, boxInk: S.ink, bar: [S.blue, S.violet, S.red], now: S.yellow, hl: S.red};
export const Frame: React.FC<{no: number; total: number; head: string; dur: number; hookEnd: number; tag?: string; pal?: Pal; at?: string}> = ({no, total, head, dur, hookEnd, tag = 'NEW STAGE 19 · DIGITAL ART', pal = STAGE_PAL, at = ''}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = f / Math.max(1, dur);
  const q = spr(f, fps, 2, 150, 15);
  // headline words: *word* = yellow box (multi-word with _)
  const words = groupLatin(head);
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <div style={{position: 'absolute', left: 0, top: 0, height: 10, width: W * p, background: `linear-gradient(90deg, ${pal.bar.join(', ')})`, boxShadow: `0 0 20px ${pal.bar[1]}`}} />
      <div style={{position: 'absolute', left: 0, right: 0, top: L.tag, display: 'flex', justifyContent: 'center', gap: 14, alignItems: 'center', opacity: q}}>
        <span style={{fontWeight: 800, fontSize: 24, letterSpacing: /[A-Za-z]/.test(tag) ? 4 : 0, color: S.soft, fontFamily: /[A-Za-z]/.test(tag) ? EN : AR}}>{tag}</span>
        {at ? (  // show shorts (enta, Aly 2026-10-31): where it is in the episode instead of a post number
          <span style={{fontFamily: AR, fontWeight: 900, fontSize: 22, color: S.ink, background: S.white, borderRadius: 12, padding: '2px 12px', direction: 'rtl', unicodeBidi: 'isolate'}}>
            من الدقيقة <span style={{fontFamily: EN, direction: 'ltr', unicodeBidi: 'isolate'}}>{at}</span> في الحلقة</span>
        ) : <span style={{fontFamily: EN, fontWeight: 900, fontSize: 22, color: S.ink, background: S.white, borderRadius: 12, padding: '2px 10px'}}>{String(no).padStart(2, '0')}/{total}</span>}
      </div>
      <div style={{position: 'absolute', left: 50, right: 50, top: L.head, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', alignItems: 'center',
        gap: '6px 18px', direction: 'rtl'}}>
        {words.map((w, i) => {
          const t = 2 + i * 2;
          const a = spr(f, fps, t, 190, 14);
          const box = w.startsWith('*') && w.endsWith('*');
          const clean = bi(w.replace(/\*/g, '').replace(/_/g, ' '));
          // after the hook the box "re-stamps" once (draws attention back to the question)
          const re = f > hookEnd ? spr(f, fps, hookEnd + 4, 260, 10) : 1;
          return box ? (
            <span key={i} style={{display: 'inline-block', opacity: a, transform: `scale(${(0.6 + 0.4 * a) * (f > hookEnd ? 0.85 + 0.15 * re : 1)}) rotate(-2deg)`,
              background: pal.box, color: pal.boxInk, fontFamily: AR, fontWeight: 900, fontSize: 70, lineHeight: 1.18, padding: '0 18px 6px', borderRadius: 14,
              boxShadow: `0 10px 40px ${pal.box}55`}}>{clean}</span>
          ) : (
            <span key={i} style={{display: 'inline-block', opacity: a, transform: `translateY(${(1 - a) * 24}px)`, fontFamily: AR, fontWeight: 900, fontSize: 70,
              lineHeight: 1.18, color: S.white, textShadow: '0 6px 30px rgba(0,0,0,0.6)'}}>{clean}</span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ---------- captions: 2–4 words, big, the spoken word boxed (yellow) — words come pre-corrected per short ----------
type Wd = {w: string; start: number; end: number; hl?: boolean};
const chunks = (ws: Wd[], max = 4) => {
  const out: Wd[][] = [];
  let cur: Wd[] = [];
  ws.forEach((w, i) => {
    cur.push(w);
    const gap = i + 1 < ws.length ? ws[i + 1].start - w.end : 1;
    const len = cur.reduce((s, x) => s + x.w.length, 0);
    if (cur.length >= max || len > 18 || gap > 0.4 || /[.!?؟،]$/.test(w.w)) { out.push(cur); cur = []; }
  });
  if (cur.length) out.push(cur);
  return out;
};
export const Caps: React.FC<{words: Wd[]; hide?: [number, number][]; top?: number; pal?: Pal}> = ({words, hide = [], top = L.cap, pal = STAGE_PAL}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  if (hide.some(([a, b]) => t >= a && t < b)) return null;
  const cs = chunks(words);
  const c = cs.find((x, i) => t >= x[0].start - 0.05 && t < (cs[i + 1]?.[0].start ?? x[x.length - 1].end + 0.6));
  if (!c) return null;
  const k0 = Math.round((c[0].start - 0.05) * fps);
  const pop = spr(f, fps, k0, 260, 14);
  return (
    <div style={{position: 'absolute', left: 40, right: 40, top, display: 'flex', justifyContent: 'center', flexWrap: 'wrap', gap: '4px 16px', direction: 'rtl',
      transform: `scale(${0.86 + 0.14 * pop})`}}>
      {(() => {
        // consecutive English words = ONE left-to-right group, else the rtl row reverses them ("Engineering Software", 2026-10-31)
        const isLat = (w: Wd) => /^[A-Za-z0-9.\-]+[.،,:]*$/.test(w.w);
        const word = (w: Wd, i: number) => {
          const on = t >= w.start - 0.03;
          const now = on && t < w.end + 0.05;
          const latin = isLat(w);
          return (
            <span key={i} style={{display: 'inline-block', fontFamily: latin ? EN : AR, fontWeight: 900, fontSize: latin ? 60 : 68, lineHeight: 1.2, padding: '0 12px 4px', borderRadius: 14,
              color: now ? S.ink : w.hl ? pal.now : S.white, background: now ? (w.hl ? pal.hl : pal.now) : 'transparent', opacity: on ? 1 : 0.35,
              transform: now ? 'scale(1.07) rotate(-1.5deg)' : 'none',
              WebkitTextStroke: now ? undefined : '2px rgba(0,0,0,0.55)', textShadow: now ? undefined : '0 6px 22px rgba(0,0,0,0.85)'}}>{w.w.replace(/[.،,:]+$/, '')}</span>
          );
        };
        const out: React.ReactNode[] = [];
        for (let i = 0; i < c.length; ) {
          if (isLat(c[i]) && i + 1 < c.length && isLat(c[i + 1])) {
            let j = i;
            while (j < c.length && isLat(c[j])) j++;
            out.push(<span key={'g' + i} style={{display: 'inline-flex', direction: 'ltr', gap: '4px 16px'}}>{c.slice(i, j).map((w, q) => word(w, i + q))}</span>);
            i = j;
          } else {
            out.push(word(c[i], i));
            i++;
          }
        }
        return out;
      })()}
    </div>
  );
};

// ---------- side badge: the full lecture is on YouTube (thumb + QR). Small on the side; grows at the end ----------
export const Badge: React.FC<{thumb: string; qr: string; at: number; big: number; label?: string; sub?: string; len?: string; y0?: number; hide?: number}> = (
  {thumb, qr, at, big, label = 'المحاضرة كاملة', sub = 'على قناتي في يوتيوب', len = '52:07', y0 = 520, hide = 0}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (f < at) return null;
  const p = spr(f, fps, at, 150, 15);
  const g = f >= big ? spr(f, fps, big, 120, 15) : 0;
  const s = 1 + 1.3 * g, w = 250;
  const x = 34 + (540 - w * s / 2 - 34) * g, y = y0 + (700 - y0) * g;
  return (
    <>
    {g > 0 ? <div style={{position: 'absolute', inset: 0, background: `rgba(7,9,18,${0.7 * g})`}} /> : null}
    <div style={{position: 'absolute', left: x, top: y, transform: `scale(${s * (0.8 + 0.2 * p)})`, transformOrigin: '0 0', opacity: p * (g > 0 ? 1 : 1 - hide)}}>
      <div style={{width: w, padding: 10, borderRadius: 20, background: 'rgba(12,15,28,0.86)', border: '2px solid rgba(255,255,255,0.18)', boxSizing: 'border-box',
        boxShadow: '0 16px 40px rgba(0,0,0,0.5)', direction: 'rtl', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8}}>
        <div style={{position: 'relative'}}>
          <Img src={staticFile(thumb)} style={{width: w - 20, height: (w - 20) * 9 / 16, objectFit: 'cover', borderRadius: 10, display: 'block'}} />
          <div style={{position: 'absolute', left: 6, bottom: 6, background: '#FF0033', borderRadius: 6, padding: '0 7px', fontFamily: EN, fontWeight: 900, fontSize: 15, color: '#fff'}}>▶ {len}</div>
        </div>
        <div style={{display: 'flex', alignItems: 'center', gap: 8, width: '100%'}}>
          <div style={{flex: 1, fontFamily: AR, fontWeight: 900, fontSize: 24, color: S.white, lineHeight: 1.2}}>{label}<br /><span style={{color: S.soft, fontWeight: 700, fontSize: 18}}>{sub}</span></div>
          <div style={{background: '#fff', padding: 4, borderRadius: 8}}><Img src={staticFile(qr)} style={{width: 78, height: 78, display: 'block'}} /></div>
        </div>
      </div>
    </div>
    </>
  );
};

// ---------- card in the stage: rounded, soft glow, enters with a spring tilt ----------
export const Card: React.FC<{w: number; h: number; x?: number; y?: number; dur: number; glow?: string; children: React.ReactNode; tilt?: number; r?: number; bg?: string}> = (
  {w, h, x = (W - w) / 2, y = L.stageTop + (L.stageH - h) / 2, dur, glow = S.violet, children, tilt = 6, r = 30, bg = '#000'}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 150, 15), o = 1 - lin(f, dur - 7, dur);
  const drift = Math.sin(f / 40) * 0.6;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h, borderRadius: r, overflow: 'hidden', background: bg, opacity: Math.min(1, p * 1.5) * o,
      transform: `perspective(1600px) rotateY(${(1 - p) * tilt + drift}deg) rotateX(${(1 - p) * -tilt}deg) scale(${0.85 + 0.15 * p})`,
      boxShadow: `0 40px 80px rgba(0,0,0,0.55), 0 0 60px ${glow}44`, border: '2px solid rgba(255,255,255,0.14)'}}>
      {children}
    </div>
  );
};

// the real lecture (his hall camera) — proof that it was said on a stage
export const Hall: React.FC<{file: string; at: number; dur: number; zoom?: number; fx?: number; fy?: number; live?: boolean; h?: number; y?: number}> = (
  {file, at, dur, zoom = 1, fx = 0.5, fy = 0.4, live = true, h = 562, y}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const w = 1000, k = zoom * (1 + 0.04 * f / Math.max(1, dur));
  return (
    <Card w={w} h={h} dur={dur} y={y}>
      <OffthreadVideo muted src={staticFile(file)} startFrom={Math.round(at * fps)}
        style={{position: 'absolute', width: w * k, height: w * k * 9 / 16, left: (w - w * k) * fx, top: (h - w * k * 9 / 16) * fy}} />
      {live ? <div style={{position: 'absolute', right: 18, top: 16, display: 'flex', alignItems: 'center', gap: 8, padding: '4px 14px', borderRadius: 20, background: 'rgba(0,0,0,0.6)',
        fontFamily: AR, fontWeight: 900, fontSize: 26, color: '#fff', direction: 'rtl'}}>
        <span style={{width: 14, height: 14, borderRadius: 7, background: '#FF2D55', opacity: 0.5 + 0.5 * Math.sin(f / 5)}} />من المحاضرة</div> : null}
    </Card>
  );
};

// one of his slides (exported 1920x1080) — crop (sx, sy, sw) in slide px, slow push
export const Slide: React.FC<{n: number; dur: number; sx?: number; sy?: number; sw?: number; w?: number; h?: number; y?: number; label?: string}> = (
  {n, dur, sx = 0, sy = 0, sw = 1920, w = 1000, h, y, label}) => {
  const f = useCurrentFrame();
  const k = w / sw;
  const hh = h ?? Math.round(Math.min(1080 - sy, sw * 9 / 16) * k);
  const push = 1 + 0.05 * f / Math.max(1, dur);
  return (
    <Card w={w} h={hh} dur={dur} y={y} bg="#fff">
      <Img src={staticFile(`projects/newstage19/slides/slide_${String(n).padStart(3, '0')}.png`)}
        style={{position: 'absolute', width: 1920 * k, height: 1080 * k, left: -sx * k, top: -sy * k, transform: `scale(${push})`, transformOrigin: `${(sx + sw / 2) * k}px ${hh / 2 + sy * k}px`}} />
      {label ? <div style={{position: 'absolute', left: 16, bottom: 14, padding: '2px 14px', borderRadius: 12, background: 'rgba(0,0,0,0.65)', fontFamily: AR, fontWeight: 800, fontSize: 24,
        color: '#fff', direction: 'rtl'}}>{label}</div> : null}
    </Card>
  );
};

// big statement in the stage (typed in, optional emoji/number above)
export const Big: React.FC<{text: string; sub?: string; top?: string; dur: number; color?: string; y?: number; size?: number}> = ({text, sub, top, dur, color = S.white, y = 640, size = 92}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const o = 1 - lin(f, dur - 7, dur);
  const words = groupLatin(text);
  const q = spr(f, fps, 0, 170, 11);
  return (
    <div style={{position: 'absolute', left: 50, right: 50, top: y, opacity: o, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 20, direction: 'rtl'}}>
      {top ? (/^(logo:)?[a-z0-9_-]+$/.test(top)
        ? <Img src={staticFile(top.startsWith('logo:') ? `logos/${top.slice(5)}.svg` : `fluent/${top}.png`)} style={{width: 250, height: 250, transform: `scale(${q}) rotate(${(1 - q) * -20}deg) translateY(${Math.sin(f / 20) * 6}px)`, filter: 'drop-shadow(0 20px 30px rgba(0,0,0,0.45))'}} />
        : <div style={{fontSize: 170, lineHeight: 1, transform: `scale(${q}) rotate(${(1 - q) * -20}deg)`}}>{top}</div>) : null}
      <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '0 22px'}}>
        {words.map((w, i) => {
          const a = spr(f, fps, 3 + i * 3, 200, 13);
          const box = w.startsWith('*') && w.endsWith('*');
          const clean = bi(w.replace(/\*/g, '').replace(/_/g, ' '));
          return <span key={i} style={{display: 'inline-block', opacity: a, transform: `translateY(${(1 - a) * 30}px) ${box ? 'rotate(-2deg)' : ''}`, fontFamily: AR, fontWeight: 900,
            fontSize: size, lineHeight: 1.2, color: box ? S.ink : color, background: box ? S.yellow : undefined, padding: box ? '0 16px 6px' : undefined, borderRadius: 14,
            textShadow: box ? undefined : '0 8px 30px rgba(0,0,0,0.6)'}}>{clean}</span>;
        })}
      </div>
      {sub ? <div style={{fontFamily: AR, fontWeight: 700, fontSize: 44, color: S.soft, opacity: lin(f, 14, 24), textAlign: 'center'}}>{bi(sub)}</div> : null}
    </div>
  );
};

// rewind between the hook and the start: VCR rewind look over the reversed hall frames (the mp4 already holds them)
export const Rewind: React.FC<{dur: number; from: string; to: string}> = ({dur, from, to}) => {
  const f = useCurrentFrame();
  const p = lin(f, 0, dur, 0, 1, Easing.inOut(Easing.cubic));
  const sec = (s: string) => s.split(':').reduce((a, b) => a * 60 + +b, 0);
  const t = sec(from) + (sec(to) - sec(from)) * p;
  const mm = Math.floor(t / 60), ss = Math.floor(t % 60);
  const jit = (rnd(f * 3.1) - 0.5) * 14;
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <AbsoluteFill style={{background: 'repeating-linear-gradient(0deg, rgba(0,0,0,0.28) 0 3px, transparent 3px 7px)', opacity: 0.8}} />
      <div style={{position: 'absolute', left: 0, right: 0, top: L.stageTop + 120 + ((f * 37) % 500), height: 60, background: 'rgba(255,255,255,0.10)', filter: 'blur(6px)'}} />
      <div style={{position: 'absolute', left: 0, right: 0, top: L.stageTop + L.stageH / 2 - 120, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6,
        transform: `translateX(${jit}px)`}}>
        <div style={{fontFamily: EN, fontWeight: 900, fontSize: 150, color: '#fff', textShadow: `4px 0 0 ${S.red}, -4px 0 0 ${S.cyan}`}}>◀◀</div>
        <div style={{fontFamily: EN, fontWeight: 800, fontSize: 64, color: '#fff', letterSpacing: 4, textShadow: `3px 0 0 ${S.red}, -3px 0 0 ${S.cyan}`}}>
          {String(mm).padStart(2, '0')}:{String(ss).padStart(2, '0')}</div>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 46, color: S.yellow, direction: 'rtl'}}>نرجع للأول</div>
      </div>
    </AbsoluteFill>
  );
};

// number chip / check / cross
export const Mark: React.FC<{ok: boolean; s?: number; at?: number}> = ({ok, s = 1, at = 0}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, at, 240, 11);
  return (
    <div style={{width: 120 * s, height: 120 * s, borderRadius: '50%', background: ok ? S.green : S.red, display: 'flex', alignItems: 'center', justifyContent: 'center',
      transform: `scale(${p}) rotate(${(1 - p) * 40}deg)`, boxShadow: `0 0 40px ${ok ? S.green : S.red}88`, fontFamily: EN, fontWeight: 900, fontSize: 80 * s, color: '#fff'}}>{ok ? '✓' : '✕'}</div>
  );
};

// ---------- his hall camera, full screen 9:16, following him (track = [[t, cx]] in 1280x720 px, zoom keys [[t, z]]) ----------
const interp = (keys: number[][], t: number) => {
  if (!keys.length) return 640;
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) if (t <= keys[i][0]) {
    const [t0, v0] = keys[i - 1], [t1, v1] = keys[i];
    return v0 + (v1 - v0) * (t - t0) / Math.max(1e-6, t1 - t0);
  }
  return keys[keys.length - 1][1];
};
// crop window for zoom z: 1 = 705 px tall (almost the whole camera height); his head (~y 170) always lands at y 430 of the short,
// under the headline (Aly 2026-10-19: his head was hidden behind the headline)
export const win = (z: number) => {
  const ch = 705 / z, cw = ch * 9 / 16;
  const top = Math.max(0, Math.min(720 - ch, 170 - 430 * ch / H));
  return {ch, cw, top};
};
export const Footage: React.FC<{file: string; track: number[][]; zoom: number[][]}> = ({file, track, zoom}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  const z = interp(zoom, t);
  const {ch, cw, top} = win(z);
  const cx = Math.max(cw / 2, Math.min(1280 - cw / 2, interp(track, t)));
  const cy = top + ch / 2;
  const k = H / ch;
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <OffthreadVideo muted src={staticFile(file)} style={{position: 'absolute', width: 1280 * k, height: 720 * k, left: -(cx - cw / 2) * k, top: -(cy - ch / 2) * k}} />
      {/* readability: dark top for the headline, dark bottom for the tray */}
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(5,7,14,0.85) 0%, rgba(5,7,14,0.35) 20%, transparent 30%, transparent 55%, rgba(5,7,14,0.55) 70%, rgba(5,7,14,0.8) 100%)'}} />
    </AbsoluteFill>
  );
};

// the tray over the seats: scenes made for the old stage box, scaled in; a dark glass panel behind them
export const Tray: React.FC<{children: React.ReactNode; on: number}> = ({children, on}) => (
  <>
    <div style={{position: 'absolute', left: 40, right: 40, top: TRAY.y - 10, height: TRAY.h + 20, borderRadius: 36, opacity: on,
      background: 'linear-gradient(160deg, rgba(14,18,34,0.82), rgba(8,10,20,0.88))', border: '2px solid rgba(255,255,255,0.14)', backdropFilter: 'blur(18px)',
      boxShadow: `0 30px 60px rgba(0,0,0,0.5), 0 0 50px ${S.violet}33`}} />
    <div style={{position: 'absolute', left: 0, top: 0, width: W, height: H, transformOrigin: '540px 430px',
      transform: `translateY(${TRAY.y - L.stageTop + 8}px) scale(${TRAY.k})`}}>{children}</div>
  </>
);

// ---------- "pop-out": his video cropped into a square card, his cut-out (matte webm) on top so his head/body breaks out of it ----------
// crop window = the same one Footage uses (cx, z); matte webm = that window (540x960) with alpha, starting at the cue start.
export const Pop: React.FC<{file: string; matte: string; at: number; dur: number; cx: number; z?: number; tilt?: number}> = ({file, matte, at, dur, cx, z = 1, tilt = -3}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, 0, 150, 14), o = 1 - lin(f, dur - 6, dur);
  const {ch, cw, top} = win(z);
  const cy = top + ch / 2;
  const k = H / ch;
  const sq = {x: 175, y: 590, w: 730, h: 730};
  const vid = (src: string, start: number, alpha: boolean) => (
    <OffthreadVideo muted transparent={alpha} src={staticFile(src)} startFrom={start}
      style={alpha ? {position: 'absolute', left: 0, top: 0, width: W, height: H}
        : {position: 'absolute', width: 1280 * k, height: 720 * k, left: -(cx - cw / 2) * k, top: -(cy - ch / 2) * k}} />
  );
  return (
    <AbsoluteFill style={{opacity: Math.min(1, p * 1.5) * o}}>
      <div style={{position: 'absolute', left: sq.x, top: sq.y, width: sq.w, height: sq.h, borderRadius: 40, overflow: 'hidden', transform: `rotate(${tilt * p}deg) scale(${0.8 + 0.2 * p})`,
        boxShadow: `0 40px 90px rgba(0,0,0,0.6), 0 0 0 8px ${S.white}, 0 0 80px ${S.violet}66`}}>
        <div style={{position: 'absolute', left: -sq.x, top: -sq.y, width: W, height: H}}>{vid(file, Math.round(at * fps), false)}</div>
      </div>
      {/* his cut-out over the card: only what is outside the card shows a difference -> he "steps out" */}
      <div style={{position: 'absolute', inset: 0, transform: `scale(${0.8 + 0.2 * p})`, transformOrigin: `${sq.x + sq.w / 2}px ${sq.y + sq.h / 2}px`,
        clipPath: `polygon(0 0, 100% 0, 100% ${sq.y + 40}px, 0 ${sq.y + 40}px)`}}>{vid(matte, 0, true)}</div>
    </AbsoluteFill>
  );
};

// v3: the camera is pre-cut at 1080x1920 from the RAW file (no browser upscaling) -> just play it, plus the readability shades
export const CamFull: React.FC<{file: string}> = ({file}) => (
  <AbsoluteFill>
    <OffthreadVideo muted src={staticFile(file)} style={{position: 'absolute', left: 0, top: 0, width: W, height: H}} />
    <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(5,7,14,0.85) 0%, rgba(5,7,14,0.35) 20%, transparent 30%, transparent 55%, rgba(5,7,14,0.55) 70%, rgba(5,7,14,0.8) 100%)'}} />
  </AbsoluteFill>
);

// one of the videos inside his slides (work/slide_media -> public/projects/newstage19/media), muted, in a card
export const Clip: React.FC<{file: string; dur: number; from?: number; w?: number; h?: number; y?: number; label?: string; fit?: 'cover' | 'contain'; note?: string; rate?: number; qr?: string}> = (
  {file, dur, from = 0, w = 1000, h = 562, y, label, fit = 'cover', note, rate = 1, qr}) => {
  const {fps} = useVideoConfig();
  const f = useCurrentFrame();
  return (
    <>
    {note ? <div style={{position: 'absolute', left: 60, right: 60, top: (y ?? L.stageTop + (L.stageH - h) / 2) + h + 18, textAlign: 'center', fontFamily: AR, fontWeight: 900, fontSize: 40,
      color: '#fff', direction: 'rtl', lineHeight: 1.35, opacity: lin(f, 8, 18) * (1 - lin(f, dur - 7, dur))}}>{note}</div> : null}
    <Card w={w} h={h} dur={dur} y={y} bg="#000">
      <OffthreadVideo muted playbackRate={rate} src={staticFile(`projects/newstage19/media/${file}`)} startFrom={Math.round(from * fps)} style={{width: w, height: h, objectFit: fit}} />
      {label ? <div style={{position: 'absolute', left: 16, bottom: 14, padding: '2px 14px', borderRadius: 12, background: 'rgba(0,0,0,0.65)', fontFamily: AR, fontWeight: 800, fontSize: 26,
        color: '#fff', direction: 'rtl'}}>{bi(label)}</div> : null}
      {qr ? <div style={{position: 'absolute', right: 14, top: 14, background: '#fff', padding: 6, borderRadius: 10}}>
        <Img src={staticFile(`projects/newstage19/media/${qr}`)} style={{width: 150, height: 150, display: 'block'}} /></div> : null}
    </Card>
    </>
  );
};
