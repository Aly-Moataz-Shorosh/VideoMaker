import React from 'react';
import {Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {Base} from '../blocks/Base';
import {enter, lerp} from '../blocks/anim';
import {E, Grain, Hi, Sticker, stickerBorder, Tape} from './kit';
import {Backdrop, clamp, Title} from './Board';

// Show intro video (2026-10-16): full-screen boards for Aly's "about the show" talk.

// ---------------- 1) flavours: the kinds of guests (cs / fnon / business owners) ----------------
const flavour = z.object({pic: z.string(), label: z.string(), sub: z.string().default(''), at: z.number(), fit: z.enum(['cover', 'contain']).default('cover'),
  accent: z.enum(['orange', 'blue', 'olive', 'mustard']).default('orange'),
  chips: z.array(z.object({text: z.string(), at: z.number()})).default([])});
export const entaFlavoursSchema = z.object({
  title: z.string().default('انت بتشتغل ايه؟ *3 أنواع* ضيوف'),
  items: z.array(flavour).default([
    {pic: 'enta/fx_bokeh.jpg', label: 'حاسبات', sub: 'Computer Science', at: 10, fit: 'cover', accent: 'blue', chips: []},
    {pic: 'enta/fx_bokeh.jpg', label: 'فنون', sub: 'كل مجالات الفن', at: 40, fit: 'cover', accent: 'orange', chips: []},
    {pic: 'enta/fx_bokeh.jpg', label: 'أصحاب أعمال', sub: '', at: 70, fit: 'cover', accent: 'olive', chips: [{text: 'شركة', at: 90}, {text: 'ورشة', at: 100}, {text: 'مصنع', at: 110}]},
  ]),
  previewBg: z.string().default(''),
});
export const EntaFlavours: React.FC<z.infer<typeof entaFlavoursSchema>> = ({title, items, previewBg}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const n = items.length, cw = 470, gap = (width - 2 * 120 - n * cw) / Math.max(1, n - 1);
  const xOf = (i: number) => width - 120 - cw - i * (cw + gap); // RTL: first on the right
  const y = height * 0.25;
  return (
    <Base previewBg={previewBg}>
      <Backdrop>
        <Title text={title} />
        {items.map((it, i) => {
          if (frame < it.at) return null;
          const p = enter(frame, fps, it.at);
          const acc = (E as Record<string, string>)[it.accent];
          const bob = Math.sin((frame - it.at) / 22 + i) * 4;
          return (
            <div key={i} style={{position: 'absolute', left: xOf(i), top: y + bob, width: cw, opacity: Math.min(1, p * 1.5),
              transform: `translateY(${lerp(p, -260, 0)}px) rotate(${lerp(p, (i - 1) * 14, (i - 1) * 2.5)}deg) scale(${lerp(p, 0.8, 1)})`}}>
              <div style={{position: 'relative', height: 380, overflow: 'hidden', background: it.fit === 'contain' ? acc : '#222', ...stickerBorder(10)}}>
                {it.fit === 'contain' ? <Grain opacity={0.35} seed={60 + i} /> : null}
                <Img src={staticFile(it.pic)} style={{position: 'absolute', inset: it.fit === 'contain' ? 18 : 0, width: it.fit === 'contain' ? 'calc(100% - 36px)' : '100%',
                  height: it.fit === 'contain' ? 'calc(100% - 36px)' : '100%', objectFit: it.fit, filter: it.fit === 'contain' ? 'drop-shadow(0 10px 16px rgba(0,0,0,.4))' : 'none',
                  transform: `scale(${1.04 + (frame - it.at) * 0.0006})`}} />
                {it.fit === 'cover' ? <Grain opacity={0.18} seed={70 + i} /> : null}
              </div>
              <Tape w={150} rot={-6} olive={i % 2 === 1} style={{top: -24, left: cw / 2 - 75}} />
              <div style={{position: 'absolute', top: -46, right: -34, width: 92, height: 92, borderRadius: 46, background: acc, color: E.ink,
                border: `6px solid ${E.white}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 52, fontWeight: 900, fontFamily: 'Montserrat',
                transform: `scale(${enter(frame, fps, it.at + 6)}) rotate(${-8 + bob}deg)`, boxShadow: '0 8px 16px rgba(0,0,0,.45)'}}>{i + 1}</div>
              <div style={{marginTop: 26, textAlign: 'center', color: E.white, fontSize: 64, fontWeight: 900}}>{it.label}</div>
              {it.sub ? <div style={{textAlign: 'center', color: acc, fontSize: 36, fontWeight: 800}}>{it.sub}</div> : null}
              <div style={{display: 'flex', justifyContent: 'center', gap: 14, marginTop: 10}}>
                {it.chips.map((c, k) => frame < c.at ? null : (
                  <div key={k} style={{transform: `scale(${enter(frame, fps, c.at)}) rotate(${k % 2 ? 4 : -4}deg)`, background: [E.mustard, E.blue, E.orange][k % 3],
                    color: E.ink, fontWeight: 900, fontSize: 38, padding: '4px 22px', borderRadius: 30, border: `4px solid ${E.white}`, boxShadow: '0 8px 16px rgba(0,0,0,.4)'}}>{c.text}</div>
                ))}
              </div>
            </div>
          );
        })}
      </Backdrop>
    </Base>
  );
};

// ---------------- 2) drawer: the show waited in the drawer 2023 -> today, then jumps out ----------------
// Front view of a desk drawer. Open = the tray slides toward us (front panel goes down, dark inside shows) with the
// show things standing in it; closed = they sink in, years tick by with dust; open again = the logo jumps out.
export const entaDrawerSchema = z.object({
  items: z.array(z.string()).default(['enta/reel.png', 'enta/masks.png', 'enta/onair.png']), // things in the drawer (2023)
  hero: z.string().default('enta/onair.png'), // jumps out at the end
  closeAt: z.number().default(70), years: z.array(z.object({y: z.number(), at: z.number()})).default([{y: 2023, at: 0}, {y: 2024, at: 90}, {y: 2025, at: 110}, {y: 2026, at: 130}]),
  openAt: z.number().default(170), jumpAt: z.number().default(185),
  text1: z.string().default('اللوجو + الانترو *جاهزين*'), text2: z.string().default('في *الدرج*… 3-4 سنين'), text3: z.string().default('أول حلقة *النهاردة*'), text4: z.string().default(''), t4At: z.number().default(9999),
  previewBg: z.string().default(''),
});
export const EntaDrawer: React.FC<z.infer<typeof entaDrawerSchema>> = ({items, hero, closeAt, years, openAt, jumpAt, text1, text2, text3, text4, t4At, previewBg}) => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const ease = (a: number, b: number) => {const x = interpolate(frame, [a, b], [0, 1], clamp); return x * x * (3 - 2 * x);};
  const o = frame < openAt ? 1 - ease(closeAt, closeAt + 14) : ease(openAt, openAt + 12); // drawer opening 0..1
  const cx = width / 2, deskY = 640, fw = 640, fh = 210;
  const frontY = deskY + 18 + 190 * o, fs = 1 + 0.1 * o;
  const shake = frame >= openAt - 10 && frame < openAt ? Math.sin(frame * 2.4) * 6 : 0; // rattles before it opens
  const yr = [...years].reverse().find((v) => frame >= v.at) ?? years[0];
  const yrAt = yr.at;
  const phase = frame < closeAt + 10 ? 0 : frame < openAt + 8 ? 1 : text4 && frame >= t4At ? 3 : 2;
  const txt = [text1, text2, text3, text4][phase];
  const tAt = [6, closeAt + 10, openAt + 8, t4At][phase];
  const jp = enter(frame, fps, jumpAt);
  const dust = frame >= closeAt + 12 && frame < openAt + 20;
  const wood = '#8A5A35', woodD = '#6B4428', woodL = '#A8744A';
  return (
    <Base previewBg={previewBg}>
      <Backdrop>
        {/* year counter */}
        <div style={{position: 'absolute', top: 70, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
          <div style={{position: 'relative', background: E.paper, color: E.ink, fontFamily: 'Montserrat', fontWeight: 900, fontSize: 120, padding: '0 50px', borderRadius: 14,
            ...stickerBorder(8), transform: `rotate(-2deg) scale(${lerp(enter(frame, fps, yrAt), 1.25, 1)})`, overflow: 'hidden'}}>
            <Grain opacity={0.3} seed={81} />
            <span style={{position: 'relative', color: phase === 2 ? E.orange : E.ink}}>{yr.y}</span>
          </div>
        </div>
        {/* phase text */}
        <div style={{position: 'absolute', top: 270, left: 0, right: 0, textAlign: 'center', color: E.white, fontSize: 64, fontWeight: 900,
          transform: `scale(${enter(frame, fps, tAt)})`, textShadow: '0 6px 14px rgba(0,0,0,.6)'}}>
          <Hi text={txt} color={E.mustard} />
        </div>
        {/* desk top */}
        <div style={{position: 'absolute', left: cx - 620, width: 1240, top: deskY - 40, height: 58, background: woodL, borderRadius: 8,
          boxShadow: '0 16px 30px rgba(0,0,0,.5)', overflow: 'hidden'}}><Grain opacity={0.4} seed={82} /></div>
        <div style={{position: 'absolute', left: cx - 600, width: 1200, top: deskY + 18, height: 420, background: woodD}}><Grain opacity={0.35} seed={83} /></div>
        {/* tray interior (visible when open) */}
        <div style={{position: 'absolute', left: cx - (fw * fs) / 2, width: fw * fs, top: deskY + 18, height: frontY - deskY - 18, background: '#2A1A10',
          clipPath: `polygon(${(fs - 1) / fs * 50}% 0, ${100 - (fs - 1) / fs * 50}% 0, 100% 100%, 0 100%)`}} />
        {/* things in the drawer: stand on the tray floor, clipped to the open part */}
        <div style={{position: 'absolute', left: cx - 420, width: 840, top: deskY - 330, height: frontY - (deskY - 330) + 6, overflow: 'hidden'}}>
          {items.map((src, i) => {
            const n = items.length, x = (i - (n - 1) / 2) * 250;
            const hide = frame >= jumpAt && src === hero;
            return hide ? null : (
              <Img key={i} src={staticFile(src)} style={{position: 'absolute', left: 420 + x - 115, bottom: 10 - (1 - o) * 260, width: 230,
                transform: `rotate(${(i - 1) * 8 + Math.sin(frame / 15 + i) * 2}deg)`, filter: 'drop-shadow(0 8px 12px rgba(0,0,0,.5))'}} />
            );
          })}
        </div>
        {/* drawer front */}
        <div style={{position: 'absolute', left: cx - (fw * fs) / 2 + shake, width: fw * fs, top: frontY, height: fh * fs, background: wood, borderRadius: 10,
          border: `5px solid ${woodD}`, boxShadow: '0 18px 30px rgba(0,0,0,.55)', overflow: 'hidden'}}>
          <Grain opacity={0.45} seed={84} />
          <div style={{position: 'absolute', left: '50%', top: '42%', width: 200, height: 34, marginLeft: -100, borderRadius: 17, background: E.mustard,
            border: `4px solid ${woodD}`, boxShadow: '0 6px 10px rgba(0,0,0,.4)'}} />
        </div>
        {/* dust while it waits */}
        {dust ? Array.from({length: 26}, (_, i) => {
          const t = (frame - closeAt) / 30, ph = (i * 0.37) % 1;
          const yy = ((t * (18 + (i % 5) * 6) + ph * 300) % 300);
          return <div key={i} style={{position: 'absolute', left: cx - 600 + ((i * 137) % 1200), top: deskY - 300 + yy, width: 6 + (i % 3) * 3, height: 6 + (i % 3) * 3,
            borderRadius: 10, background: 'rgba(239,230,210,.45)'}} />;
        }) : null}
        {/* the logo jumps out of the drawer and lands on the desk (left) */}
        {frame >= jumpAt ? (
          <div style={{position: 'absolute', left: lerp(jp, cx - 190, cx - 750), top: lerp(jp, frontY - 200, deskY - 40 - 384) - Math.sin(Math.min(1, jp) * Math.PI) * 160, width: 380,
            transform: `scale(${lerp(jp, 0.5, 1)}) rotate(${lerp(jp, 30, -4)}deg)`, filter: 'drop-shadow(0 18px 26px rgba(0,0,0,.55))'}}>
            <Img src={staticFile(hero)} style={{width: '100%'}} />
          </div>
        ) : null}
        {frame >= jumpAt + 8 ? [['star_y', -800, 250, 110], ['spark_o', -330, 260, 100], ['onair', 470, 480, 210], ['star8_b', -820, 520, 90]].map(([s, dx, yy, sz], i) => (
          <div key={i} style={{position: 'absolute', left: cx + (dx as number) - (sz as number) / 2, top: yy as number,
            transform: `scale(${enter(frame, fps, jumpAt + 8 + i * 4)}) rotate(${Math.sin(frame / 9 + i) * 8}deg)`}}>
            <Sticker name={s as string} size={sz as number} />
          </div>
        )) : null}
      </Backdrop>
    </Base>
  );
};
