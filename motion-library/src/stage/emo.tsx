import React from 'react';
import {Easing, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, bi, EN, L, lin, S, spr, W} from './kit';

// v3 scenes (Aly 2026-10-19: "الرسم بدائي اوي و هندسي اوي… عايز رسم انضف و اجمل"): Microsoft Fluent 3D emoji (MIT) as soft
// 3D actors on frosted cards — light from the top, contact shadow, slow float. Drawn in the stage box (y 430–1260), the tray
// scales them in. Every scene: props from the cue + b = beats (seconds from the cue start).
const bt = (b: Record<string, number> | undefined, k: string, fps: number, d = 0) => Math.round((b?.[k] ?? d) * fps);
export const fe = (n: string) => staticFile(`fluent/${n}.png`);

// swim fins (Fluent has none; Aly 2026-10-19: the snorkel mask was wrong — "الزعانف دي اللي بتتلبس في الرجل"): a pair of foot fins
// drawn in the same soft-3D style (gradient body, foot pocket, ribs, top highlight)
const Fin: React.FC<{x: number; rot: number; id: string}> = ({x, rot, id}) => (
  <g transform={`translate(${x} 0) rotate(${rot} 64 200)`}>
    <defs>
      <linearGradient id={`fb${id}`} x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#5FD3FF" /><stop offset="0.55" stopColor="#1E88E5" /><stop offset="1" stopColor="#0B4FA8" /></linearGradient>
      <linearGradient id={`fp${id}`} x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#3A3F55" /><stop offset="1" stopColor="#1C2033" /></linearGradient>
    </defs>
    {/* blade */}
    <path d="M40 120 Q8 150 6 200 L0 236 Q30 252 64 246 Q98 252 128 236 L122 200 Q120 150 88 120 Z" fill={`url(#fb${id})`} />
    <path d="M44 132 L30 236 M64 130 L64 244 M84 132 L98 236" stroke="#0A3E85" strokeOpacity={0.45} strokeWidth={5} strokeLinecap="round" fill="none" />
    <path d="M22 160 Q26 140 44 128" stroke="#fff" strokeOpacity={0.55} strokeWidth={6} strokeLinecap="round" fill="none" />
    {/* foot pocket */}
    <path d="M34 20 Q64 0 94 20 L98 122 Q64 140 30 122 Z" fill={`url(#fp${id})`} />
    <ellipse cx={64} cy={30} rx={24} ry={12} fill="#0E1120" />
    <path d="M42 40 Q44 80 40 112" stroke="#fff" strokeOpacity={0.25} strokeWidth={5} strokeLinecap="round" fill="none" />
  </g>
);
export const SwimFins: React.FC<{s: number}> = ({s}) => (
  <svg width={s} height={s} viewBox="0 0 256 256">
    <Fin x={30} rot={-12} id="a" />
    <Fin x={100} rot={10} id="b" />
  </svg>
);

// one 3D actor: float, contact shadow, entrance pop (at = frame), optional glow
export const Actor: React.FC<{e: string; s?: number; at?: number; glow?: string; flip?: boolean; dim?: number; rot?: number}> = ({e, s = 300, at = 0, glow, flip, dim = 0, rot = 0}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, at, 170, 12);
  const fl = Math.sin((f + at * 3) / 22) * s * 0.025;
  return (
    <div style={{position: 'relative', width: s, height: s * 1.1, opacity: Math.min(1, p * 2), transform: `scale(${0.3 + 0.7 * p}) rotate(${(1 - p) * -18 + rot}deg)`}}>
      {glow ? <div style={{position: 'absolute', left: -s * 0.2, top: -s * 0.2, width: s * 1.4, height: s * 1.4, borderRadius: '50%', background: `radial-gradient(circle, ${glow}55 0%, transparent 65%)`}} /> : null}
      <div style={{position: 'absolute', left: s * 0.18, top: s * 1.0, width: s * 0.64, height: s * 0.09, borderRadius: '50%', background: 'rgba(0,0,0,0.45)', filter: `blur(${s * 0.03}px)`,
        transform: `scaleX(${1 - fl / s * 4})`}} />
      {e.startsWith('logo:') ? (
        // real brand logo as it is (Aly 2026-10-19: "اللوجوهات استخدمها زي ما هي") on a white app-icon tile
        <div style={{position: 'absolute', left: s * 0.08, top: s * 0.08 - fl, width: s * 0.84, height: s * 0.84, borderRadius: s * 0.22, background: '#FFFFFF',
          boxShadow: `0 ${s * 0.06}px ${s * 0.12}px rgba(0,0,0,0.45), inset 0 -${s * 0.03}px 0 rgba(0,0,0,0.08)`, display: 'flex', alignItems: 'center', justifyContent: 'center',
          filter: dim ? `grayscale(${dim}) brightness(${1 - dim * 0.4})` : undefined}}>
          <Img src={staticFile(`logos/${e.slice(5)}.svg`)} style={{width: s * 0.74, height: s * 0.74, objectFit: 'contain'}} />
        </div>
      ) : e === 'swim_fins' ? <div style={{position: 'absolute', left: 0, top: -fl, filter: dim ? `grayscale(${dim}) brightness(${1 - dim * 0.4})` : undefined}}><SwimFins s={s} /></div>
        : <Img src={fe(e)} style={{position: 'absolute', left: 0, top: -fl, width: s, height: s, transform: flip ? 'scaleX(-1)' : undefined, filter: dim ? `grayscale(${dim}) brightness(${1 - dim * 0.4})` : undefined}} />}
    </div>
  );
};

// soft frosted card
export const Soft: React.FC<{w: number; h: number; children?: React.ReactNode; glow?: string; style?: React.CSSProperties}> = ({w, h, children, glow = S.violet, style}) => (
  <div style={{width: w, height: h, borderRadius: 44, position: 'relative', boxSizing: 'border-box',
    background: 'linear-gradient(165deg, rgba(255,255,255,0.13) 0%, rgba(255,255,255,0.04) 60%, rgba(255,255,255,0.02) 100%)',
    border: '2px solid rgba(255,255,255,0.16)', boxShadow: `inset 0 2px 0 rgba(255,255,255,0.18), 0 30px 60px rgba(0,0,0,0.35), 0 0 60px ${glow}22`, ...style}}>{children}</div>
);

const Label: React.FC<{t: string; at: number; size?: number; color?: string; bg?: string}> = ({t, at, size = 54, color = S.white, bg}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spr(f, fps, at, 200, 14);
  return <div style={{opacity: p, transform: `translateY(${(1 - p) * 20}px)`, fontFamily: AR, fontWeight: 900, fontSize: size, color, direction: 'rtl', textAlign: 'center',
    background: bg, padding: bg ? '2px 22px 8px' : undefined, borderRadius: 18, lineHeight: 1.25, textShadow: bg ? undefined : '0 6px 20px rgba(0,0,0,0.5)'}}>{bi(t)}</div>;
};

const Tick: React.FC<{ok: boolean; at: number; s?: number}> = ({ok, at, s = 1}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (f < at) return null;
  return <div style={{position: 'absolute', right: -10, top: -10}}><Actor e={ok ? 'check_mark_button' : 'cross_mark'} s={110 * s} at={at} /></div>;
};

const wrapOut = (f: number, dur: number) => 1 - lin(f, dur - 7, dur);

// ---------- hero: one big actor + title (+ sub), optional second actor that joins ----------
export const Hero: React.FC<{dur: number; e: string; t?: string; sub?: string; e2?: string; b?: Record<string, number>; glow?: string}> = ({dur, e, t, sub, e2, b, glow = S.violet}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const k2 = bt(b, 'e2', fps, 0.6), kt = bt(b, 't', fps, 0.25);
  return (
    <div style={{position: 'absolute', left: 0, width: W, top: L.stageTop + 10, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10, opacity: wrapOut(f, dur)}}>
      <div style={{display: 'flex', gap: 20, alignItems: 'flex-end'}}>
        <Actor e={e} s={e2 ? 360 : 420} glow={glow} />
        {e2 ? <Actor e={e2} s={300} at={k2} /> : null}
      </div>
      {t ? <Label t={t} at={kt} size={76} /> : null}
      {sub ? <Label t={sub} at={kt + 8} size={46} color={S.soft} /> : null}
    </div>
  );
};

// ---------- vs: two cards side by side (A then B), marks on beats ----------
type Side = {e: string; t: string; sub?: string; ok?: boolean; tag?: string};
export const Vs: React.FC<{dur: number; a: Side; b2: Side; b?: Record<string, number>}> = ({dur, a, b2, b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const ka = bt(b, 'a', fps, 0), kb = bt(b, 'b', fps, 0.5), kma = bt(b, 'ma', fps, 99), kmb = bt(b, 'mb', fps, 99);
  const card = (s: Side, k: number, km: number, glow: string) => {
    const p = spr(f, fps, k, 160, 15);
    return (
      <div style={{opacity: Math.min(1, p * 1.6), transform: `translateY(${(1 - p) * 60}px)`}}>
        <Soft w={450} h={700} glow={glow}>
          {s.tag ? <div style={{position: 'absolute', left: 0, right: 0, top: 26, textAlign: 'center', fontFamily: EN, fontWeight: 900, fontSize: 58, color: glow}}>{s.tag}</div> : null}
          <div style={{position: 'absolute', left: 45, top: s.tag ? 120 : 70}}><Actor e={s.e} s={360} at={k + 4} dim={s.ok === false && f > km ? 0.6 : 0} /></div>
          <div style={{position: 'absolute', left: 10, right: 10, top: s.tag ? 540 : 500}}><Label t={s.t} at={k + 8} size={48} />{s.sub ? <Label t={s.sub} at={k + 12} size={34} color={S.soft} /> : null}</div>
          {s.ok !== undefined ? <Tick ok={s.ok} at={km} /> : null}
        </Soft>
      </div>
    );
  };
  return (
    <div style={{position: 'absolute', left: 0, width: W, top: L.stageTop + 40, display: 'flex', justifyContent: 'center', gap: 40, direction: 'rtl', opacity: wrapOut(f, dur)}}>
      {card(a, ka, kma, S.cyan)}{card(b2, kb, kmb, S.yellow)}
    </div>
  );
};

// ---------- flow: actors in order with numbered arrows (step i appears on beat 's<i>') ----------
export const Flow: React.FC<{dur: number; items: {e: string; t: string; bad?: boolean}[]; b?: Record<string, number>; color?: string}> = ({dur, items, b, color = S.green}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const n = items.length, s = n > 3 ? 230 : 300;
  return (
    <div style={{position: 'absolute', left: 0, width: W, top: L.stageTop + 120, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 10, direction: 'rtl', opacity: wrapOut(f, dur)}}>
      {items.map((it, i) => {
        const k = bt(b, `s${i}`, fps, i * 0.6);
        const p = spr(f, fps, k, 200, 13);
        return (
          <React.Fragment key={i}>
            {i > 0 ? <div style={{fontFamily: EN, fontWeight: 900, fontSize: 80, color: S.soft, opacity: p, transform: `scaleX(-1) translateX(${(1 - p) * 30}px)`}}>➜</div> : null}
            <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6, position: 'relative'}}>
              <div style={{position: 'absolute', top: -20, right: 6, width: 64, height: 64, borderRadius: 32, background: it.bad ? S.red : color, color: '#fff', fontFamily: EN, fontWeight: 900,
                fontSize: 38, display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: p, zIndex: 2, boxShadow: '0 8px 20px rgba(0,0,0,0.4)'}}>{i + 1}</div>
              <Actor e={it.e} s={s} at={k} />
              <Label t={it.t} at={k + 4} size={46} />
            </div>
          </React.Fragment>
        );
      })}
    </div>
  );
};

// ---------- list: rows (actor + text) popping on beats 'r<i>' ----------
export const List: React.FC<{dur: number; items: {e: string; t: string; ok?: boolean}[]; title?: string; b?: Record<string, number>}> = ({dur, items, title, b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const rowH = Math.min(170, 700 / items.length);
  return (
    <div style={{position: 'absolute', left: 90, right: 90, top: L.stageTop + 20, display: 'flex', flexDirection: 'column', gap: 14, direction: 'rtl', opacity: wrapOut(f, dur)}}>
      {title ? <Label t={title} at={0} size={60} color={S.yellow} /> : null}
      {items.map((it, i) => {
        const k = bt(b, `r${i}`, fps, 0.3 + i * 0.5);
        const p = spr(f, fps, k, 190, 14);
        return (
          <div key={i} style={{display: 'flex', alignItems: 'center', gap: 22, height: rowH, opacity: Math.min(1, p * 1.5), transform: `translateX(${(1 - p) * 120}px)`,
            background: 'rgba(255,255,255,0.06)', borderRadius: 30, padding: '0 22px', border: '1.5px solid rgba(255,255,255,0.12)'}}>
            <Actor e={it.e} s={rowH * 0.85} at={k} />
            <div style={{flex: 1, fontFamily: AR, fontWeight: 900, fontSize: Math.min(56, rowH * 0.36), color: '#fff'}}>{bi(it.t)}</div>
            {it.ok !== undefined ? <Actor e={it.ok ? 'check_mark_button' : 'cross_mark'} s={rowH * 0.55} at={k + 6} /> : null}
          </div>
        );
      })}
    </div>
  );
};

// ---------- count: big number that counts up (+ actor) ----------
export const Count: React.FC<{dur: number; e?: string; to: number; from?: number; pre?: string; suf?: string; t?: string; b?: Record<string, number>; e2?: string; to2?: number; t2?: string}> = (
  {dur, e, to, from = 0, pre = '', suf = '', t, b, e2, to2, t2}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const k0 = bt(b, 'go', fps, 0.2), k2 = bt(b, 'go2', fps, 99);
  const v = Math.round(from + (to - from) * lin(f, k0, k0 + 24, 0, 1, Easing.out(Easing.cubic)));
  const v2 = to2 === undefined ? 0 : Math.round(to2 * lin(f, k2, k2 + 24, 0, 1, Easing.out(Easing.cubic)));
  const big = (val: number, color: string, at: number) => {
    const p = spr(f, fps, at, 220, 12);
    return <div style={{fontFamily: EN, fontWeight: 900, fontSize: 190, color, lineHeight: 1, transform: `scale(${0.6 + 0.4 * p})`, opacity: p, textShadow: `0 0 50px ${color}66`, direction: 'ltr'}}>
      {pre}{val.toLocaleString('en-US')}{suf}</div>;
  };
  return (
    <div style={{position: 'absolute', left: 0, width: W, top: L.stageTop + 20, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6, opacity: wrapOut(f, dur)}}>
      {e ? <Actor e={e} s={260} /> : null}
      {big(v, S.white, k0)}
      {t ? <Label t={t} at={k0 + 6} size={52} color={S.soft} /> : null}
      {to2 !== undefined && f >= k2 ? <>{big(v2, S.yellow, k2)}{t2 ? <Label t={t2} at={k2 + 6} size={52} color={S.yellow} /> : null}</> : null}
      {e2 && f >= k2 ? <Actor e={e2} s={200} at={k2} /> : null}
    </div>
  );
};

// ---------- ATM story (3D): card first (right) / cash first -> the old man walks off with the cash, the card blinks alone ----------
export const AtmStory: React.FC<{dur: number; mode: 'ask' | 'right' | 'wrong'; b?: Record<string, number>}> = ({dur, mode, b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const kC = bt(b, 'card', fps, 0.5), kM = bt(b, 'cash', fps, 1.5), kW = bt(b, 'walk', fps, 99);
  const walk = lin(f, kW, kW + 36, 0, 1, Easing.inOut(Easing.quad));
  const out = (k: number) => lin(f, k, k + 12, 0, 1, Easing.out(Easing.back(1.7)));
  const y0 = L.stageTop + 60;
  const first = mode === 'right' ? [['credit_card', kC], ['dollar_banknote', kM]] : [['dollar_banknote', kM], ['credit_card', kW + 30]];
  const blink = mode === 'wrong' && f > kW + 30 ? 0.5 + 0.5 * Math.sin(f / 3) : 1;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: W, height: 1920, opacity: wrapOut(f, dur)}}>
      {/* the machine */}
      <div style={{position: 'absolute', left: 560, top: y0}}><Actor e="atm_sign" s={420} glow={S.blue} /></div>
      {mode === 'ask' ? <div style={{position: 'absolute', left: 140, top: y0 + 40}}><Actor e="red_question_mark" s={300} at={6} /></div> : null}
      {/* what comes out, in order */}
      {mode !== 'ask' ? first.map(([e, k], i) => {
        const o = out(k as number);
        const taken = mode === 'wrong' && e === 'dollar_banknote' ? walk : 0;
        return f < (k as number) ? null : (
          <div key={i} style={{position: 'absolute', left: 620 - o * 120 - taken * 700, top: y0 + 380 + i * 10 - o * 40 * (i + 1), opacity: (e === 'credit_card' ? blink : 1)}}>
            <div style={{position: 'absolute', left: -46, top: -30, width: 60, height: 60, borderRadius: 30, background: mode === 'right' ? S.green : S.red, color: '#fff',
              fontFamily: EN, fontWeight: 900, fontSize: 36, display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 2}}>{i + 1}</div>
            <Actor e={e as string} s={220} at={k as number} />
          </div>
        );
      }) : null}
      {/* the old man */}
      {mode !== 'ask' ? <div style={{position: 'absolute', left: 120 - walk * 600, top: y0 + 120, opacity: 1 - lin(f, kW + 24, kW + 36)}}><Actor e="old_man" s={360} at={4} flip={walk > 0} /></div> : null}
      {mode === 'wrong' && f > kW + 34 ? <div style={{position: 'absolute', left: 130, top: y0 + 160, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10}}>
        <Actor e="cross_mark" s={150} at={kW + 34} /><Label t="نسي الكارت!" at={kW + 38} size={60} bg={S.red} /></div> : null}
      {mode === 'right' && f > kM + 14 ? <div style={{position: 'absolute', left: 170, top: y0 + 520}}><Actor e="check_mark_button" s={140} at={kM + 14} /></div> : null}
    </div>
  );
};
