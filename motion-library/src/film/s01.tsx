import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {MapPaths, lonLat, GEO} from '../blocks/geo';
import {AR, EN, K, Clip, Count, Halftone, Paper, Photo, Pop, Scene, Scribble, Stamp, Strip, Tag, Title, Beam, arrowPath, circlePath,
  img, lin, rnd, shake, spr, useBeats, Flash} from './kit';

// Short 1 — "Why Nolan says: watch The Odyssey only in IMAX 70" (theodesy). b = beats in seconds from scene start.
const PJ = 'projects/2026-10-08 shorts theodesy/';
type B = {b?: Record<string, number>};

// Series label shown on every hook.
export const SeriesTag: React.FC<{n: number; at?: number}> = ({n, at = 0}) => (
  <Pop at={at} x={540} y={150}>
    <div style={{display: 'flex', alignItems: 'center', gap: 14, background: K.ink, border: `3px solid ${K.yellow}`, borderRadius: 40, padding: '6px 26px',
      color: K.yellow, fontFamily: AR, fontWeight: 900, fontSize: 40}}>
      <span style={{width: 18, height: 18, borderRadius: 9, background: K.red}} /> حكاية الفيلم · {n}
    </div>
  </Pop>
);

// 1. Hook (behind Aly): big question + poster beside his head.
export const S1Hook: React.FC<B & {title: string}> = ({b, title}) => {
  const at = useBeats(b);
  return (
    <AbsoluteFill>
      <SeriesTag n={1} />
      <div style={{position: 'absolute', top: 230, left: 70, right: 70, display: 'flex', justifyContent: 'center'}}>
        <Title text={title} size={84} at={2} stagger={2} stroke />
      </div>
      <Pop at={at('poster', 0.6)} x={210} y={1010} rot={-9}>
        <Photo src={PJ + 'img/poster.jpg'} w={300} h={470} bw={false} seed={4} pos="50% 30%" />
      </Pop>
      <Pop at={at('imax', 1.2)} x={880} y={960} rot={8}>
        <Tag text="IMAX 70mm" font={EN} dir="ltr" bg={K.yellow} size={46} />
      </Pop>
    </AbsoluteFill>
  );
};

// 2. Nolan + his rule as a speech bubble, 70mm stamp, circle on the camera.
export const S1Nolan: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const say = at('say', 0.5), mm = at('mm', 3.5), all = at('all', 5);
  const text = 'ما تشوفوش الفيلم غير في سينما IMAX 70mm';
  const n = Math.round(lin(f, say, say + 40, 0, text.length, (x) => x));
  return (
    <Scene bg={K.paper2}>
      <Halftone color="#000" size={14} dot={0.18} opacity={0.12} />
      <Pop at={0} x={540} y={640} rot={-3} from={0.8}>
        <Photo src={PJ + 'img/nolan_cam.jpg'} w={1010} h={640} pos="70% 40%" seed={8} />
      </Pop>
      <Pop at={at('name', 0)} x={760} y={290} rot={4}>
        <Tag text="كريستوفر نولان" size={50} />
      </Pop>
      <Scribble width={1080} height={1920} p={lin(f, all, all + 14)} d={circlePath(330, 650, 250, 230)} w={12} />
      <Pop at={say} x={540} y={1180} from={0.6}>
        <div style={{position: 'relative', width: 900, background: K.white, border: `6px solid ${K.ink}`, borderRadius: 40, padding: '30px 40px',
          fontFamily: AR, fontWeight: 900, fontSize: 64, color: K.ink, textAlign: 'center', lineHeight: 1.3, boxShadow: '12px 14px 0 rgba(0,0,0,0.85)'}}>
          <span dir="rtl">{text.slice(0, n)}</span><span style={{opacity: f % 16 < 8 ? 1 : 0}}>|</span>
          <div style={{position: 'absolute', top: -46, right: 220, width: 0, height: 0, borderLeft: '30px solid transparent', borderRight: '30px solid transparent',
            borderBottom: `46px solid ${K.ink}`}} />
        </div>
      </Pop>
      <div style={{position: 'absolute', left: 90, top: 860}}>
        <Stamp text="70mm فقط" at={mm} size={96} rot={-8} />
      </div>
    </Scene>
  );
};

// 3. "Why not every cinema?" -> poster goes from grey to its real colors -> film strip.
export const S1Why: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const at = useBeats(b);
  const colors = at('colors', 3), strip = at('strip', 4.5);
  const q = spr(f, fps, 0, 120, 9);
  const wipe = lin(f, colors, colors + 18);
  return (
    <Scene bg={K.ink}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 120, textAlign: 'center', fontFamily: EN, fontWeight: 900, fontSize: 420, color: K.yellow,
        transform: `translateY(${(1 - q) * -400}px) rotate(${(1 - q) * 30}deg)`, opacity: 1 - lin(f, colors - 6, colors + 6) * 0.85}}>?</div>
      <div style={{position: 'absolute', top: 640, left: 70, right: 70, display: 'flex', justifyContent: 'center', opacity: 1 - lin(f, colors - 6, colors + 4)}}>
        <Title text="ليه مش في *أي* سينما؟" size={100} at={6} />
      </div>
      <Pop at={colors - 6} x={540} y={760} from={0.85}>
        <div style={{position: 'relative', width: 560, height: 880}}>
          <Photo src={PJ + 'img/poster.jpg'} w={560} h={880} bw={true} pos="50% 30%" seed={11} />
          <div style={{position: 'absolute', inset: 0, clipPath: `inset(${(1 - wipe) * 100}% 0 0 0)`}}>
            <Photo src={PJ + 'img/poster.jpg'} w={560} h={880} bw={false} pos="50% 30%" seed={11} />
          </div>
          <div style={{position: 'absolute', left: -20, right: -20, top: `${(1 - wipe) * 100}%`, height: 8, background: K.yellow, opacity: wipe > 0 && wipe < 1 ? 1 : 0,
            boxShadow: `0 0 30px ${K.yellow}`}} />
        </div>
      </Pop>
      <Pop at={colors + 10} x={540} y={250} rot={-3}>
        <Tag text="بألوانه الحقيقية" bg={K.yellow} size={64} />
      </Pop>
      {f >= strip ? (
        <div style={{position: 'absolute', top: 1260, left: 0, transform: `translateX(${lin(f, strip, strip + 60, 1100, -900, (x) => x)}px) rotate(-4deg)`}}>
          <Strip frames={Array(8).fill(PJ + 'img/poster.jpg')} fw={260} fh={190} />
        </div>
      ) : null}
    </Scene>
  );
};

// 4. Real footage: the IMAX 70 print on the platters (huge) + tags.
export const S1Projector: React.FC<B> = ({b}) => {
  const at = useBeats(b);
  return (
    <Scene bg={K.ink}>
      <Pop at={0} x={540} y={800} rot={2} from={0.85}>
        <Clip src={PJ + 'broll/b9_imax70.mp4'} start={4.6} w={900} h={1180} pos="50% 50%" seed={21} />
      </Pop>
      <Pop at={at('proj', 0.6)} x={330} y={250} rot={-5}><Tag text="بروجكتور مخصوص" size={58} /></Pop>
      <Pop at={at('huge', 2.6)} x={770} y={1300} rot={6}><Tag text="حجم ضخم جدًا" bg={K.yellow} size={62} /></Pop>
      <Pop at={at('special', 4.7)} x={420} y={1450} rot={-4}><Tag text="سينما متخصصة" bg={K.red} color={K.white} size={58} /></Pop>
    </Scene>
  );
};

// 5. The map: 41 IMAX 70mm cinemas light up; Africa and Asia turn to empty desert with tumbleweeds.
const AFRICA = 'DZA AGO BEN BWA BFA BDI CMR CPV CAF TCD COM COD COG CIV DJI EGY GNQ ERI ETH GAB GMB GHA GIN GNB KEN LSO LBR LBY MDG MWI MLI MRT MUS MAR MOZ NAM NER NGA RWA STP SEN SYC SLE SOM ZAF SSD SDN SWZ TZA TGO TUN UGA ZMB ZWE ESH SOL'.split(' ');
const ASIA = 'AFG ARM AZE BHR BGD BTN BRN KHM CHN CYP GEO IND IDN IRN IRQ ISR JPN JOR KAZ KWT KGZ LAO LBN MYS MDV MNG MMR NPL PRK OMN PAK PSE PHL QAT SAU SGP KOR LKA SYR TWN TJK THA TLS TUR TKM ARE UZB VNM YEM HKG MAC KAS'.split(' ');
// Approximate cities with IMAX 70mm projection (Newsweek 2026: ~41 worldwide, ~25 in the US). No names shown.
const NA: [number, number][] = [[-73.98, 40.77], [-118.35, 34.14], [-118.34, 34.1], [-117.8, 33.68], [-117.6, 34.06], [-122.4, 37.78], [-121.93, 37.7],
  [-121.49, 38.58], [-122.35, 47.62], [-111.96, 33.4], [-104.99, 39.74], [-96.8, 32.78], [-95.37, 29.76], [-94.58, 39.1], [-93.2, 44.73], [-87.6, 41.89],
  [-86.16, 39.77], [-83.05, 42.33], [-84.39, 33.75], [-81.38, 28.54], [-77.03, 38.89], [-71.06, 42.36], [-75.17, 39.95], [-115.17, 36.11], [-80.84, 35.22],
  [-79.38, 43.65], [-79.5, 43.8], [-73.57, 45.5], [-123.12, 49.28], [-114.07, 51.05], [-75.69, 45.42], [-113.49, 53.55], [-97.14, 49.9]];
const UK: [number, number][] = [[-0.11, 51.5], [-0.175, 51.497], [-2.24, 53.48]];
const EU: [number, number][] = [[8.4, 49.0], [14.43, 50.08], [19.04, 47.5], [4.9, 52.37]];
const AU: [number, number][] = [[144.96, -37.81]];

const Tumbleweed: React.FC<{x: number; y: number; r: number; spin: number; seed?: number}> = ({x, y, r, spin, seed = 1}) => (
  <g transform={`translate(${x},${y}) rotate(${spin})`}>
    {Array.from({length: 26}, (_, i) => {
      const a = rnd(seed + i) * 6.28, rr = r * (0.35 + rnd(seed + i * 3) * 0.65);
      return <ellipse key={i} cx={Math.cos(a) * r * 0.15} cy={Math.sin(a) * r * 0.15} rx={rr} ry={rr * (0.4 + rnd(i + seed * 7) * 0.6)}
        transform={`rotate(${rnd(i * 5 + seed) * 180})`} fill="none" stroke="#C9A66B" strokeWidth={2.2} opacity={0.9} />;
    })}
  </g>
);

export const S1Map: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const {fps, width: W, height: H} = useVideoConfig();
  const at = useBeats(b);
  const t41 = at('n41', 1.7), tNA = at('na', 5), tUK = at('uk', 6.8), tEU = at('eu', 7.6), tAU = at('au', 8.7), tNone = at('none', 9.2),
    tAF = at('africa', 10), tAS = at('asia', 11.4);
  // camera keyframes: [frame, lon, lat, zoom]
  const keys: [number, number, number, number][] = [[0, 10, 22, 0.42], [t41, 10, 22, 0.42], [tNA - 4, 10, 22, 0.5], [tNA + 10, -98, 42, 2.1],
    [tUK - 6, -98, 42, 2.1], [tUK + 8, 4, 50, 3.0], [tAU - 6, 6, 50, 3.0], [tAU + 8, 140, -30, 2.6], [tNone - 2, 140, -30, 2.6], [tNone + 14, 55, 18, 1.35]];
  let cam = keys[0];
  for (let i = 0; i < keys.length - 1; i++) {
    const [fa, ...a] = keys[i], [fb, ...bb] = keys[i + 1];
    if (f >= fa) {
      const k = interpolate(f, [fa, Math.max(fa + 1, fb)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
      cam = [f, a[0] + (bb[0] - a[0]) * k, a[1] + (bb[1] - a[1]) * k, a[2] + (bb[2] - a[2]) * k];
    }
  }
  const [cx, cy] = lonLat(cam[1], cam[2]);
  const base = W / 1500; // zoom 1 = 1500 map units across the screen
  const z = base * cam[3];
  const tx = W / 2 - cx * z, ty = 820 - cy * z;
  const scr = (lon: number, lat: number) => {const [x, y] = lonLat(lon, lat); return [tx + x * z, ty + y * z];};
  const desert = lin(f, tNone, tNone + 16);
  const pin = (p: [number, number], i: number, start: number, col = K.yellow) => {
    const k = spr(f, fps, start + i * 0.6, 260, 12);
    if (f < start) return null;
    const [x, y] = lonLat(p[0], p[1]);
    return (
      <g key={i} transform={`translate(${x},${y}) scale(${(1.7 * k) / Math.sqrt(cam[3])})`}>
        <circle r={22} fill={col} opacity={0.25 + 0.15 * Math.sin((f + i * 5) / 4)} />
        <circle r={9} fill={col} stroke={K.ink} strokeWidth={3} />
        <polygon points="-7,-10 7,-10 22,-110 -22,-110" fill={col} opacity={0.18} />
      </g>
    );
  };
  const count = Math.round(lin(f, t41, t41 + 30, 0, 41, (x) => x));
  const label = (txt: string, n: string, a: number, x: number, y: number, bg = K.yellow, col = K.ink, out?: number) => (
    <Pop at={a} out={out} x={x} y={y} rot={rnd(a) * 8 - 4}>
      <div style={{display: 'flex', alignItems: 'center', gap: 16}}>
        <Tag text={txt} bg={bg} color={col} size={54} />
        <div style={{fontFamily: EN, fontWeight: 900, fontSize: 92, color: bg === K.paper ? K.paper : bg, textShadow: '0 6px 0 #000'}}>{n}</div>
      </div>
    </Pop>
  );
  const twX = (a: number, from: number, to: number) => from + (to - from) * lin(f, a, a + 50, 0, 1, (x) => x);
  return (
    <Scene bg="#0B1013">
      <Halftone color="#2A3A40" size={12} dot={0.25} opacity={0.5} />
      <svg width={W} height={H} style={{position: 'absolute'}}>
        <g transform={`translate(${tx},${ty}) scale(${z})`}>
          <MapPaths style={(iso) => {
            const dead = AFRICA.includes(iso) || ASIA.includes(iso);
            const fill = dead ? interpolate(desert, [0, 1], [0, 1]) > 0.5 ? '#8A6E45' : '#3B3934' : '#4A4741';
            return {fill, stroke: '#0B1013', strokeWidth: 1.2 / cam[3], opacity: dead ? 0.55 + 0.45 * desert : 1};
          }} />
          {desert > 0 ? <MapPaths only={['EGY']} style={() => ({fill: '#A8854F', stroke: K.red, strokeWidth: 5 / cam[3]})} /> : null}
          {NA.map((p, i) => pin(p, i, t41))}
          {UK.map((p, i) => pin(p, i, t41 + 20))}
          {EU.map((p, i) => pin(p, i, t41 + 23))}
          {AU.map((p, i) => pin(p, i, t41 + 27))}
        </g>
        {desert > 0 ? (
          <>
            {Array.from({length: 9}, (_, i) => {
              const y = 640 + i * 70, x = ((f * (14 + i * 2) + i * 300) % 1500) - 300;
              return <line key={i} x1={x} y1={y} x2={x + 160 + i * 10} y2={y} stroke="#D8C49A" strokeWidth={3} strokeLinecap="round" opacity={0.35 * desert} />;
            })}
            {f >= tAF ? (() => {const [, y] = scr(20, 8); const x = twX(tAF, -120, 760); return <Tumbleweed x={x} y={y - Math.abs(Math.sin(f / 5)) * 50} r={62} spin={f * 9} seed={3} />;})() : null}
            {f >= tAS ? (() => {const [, y] = scr(90, 40); const x = twX(tAS, 300, 1180); return <Tumbleweed x={x} y={y - Math.abs(Math.sin(f / 4.5)) * 45} r={54} spin={f * 10} seed={9} />;})() : null}
          </>
        ) : null}
      </svg>
      <div style={{position: 'absolute', top: 140, left: 0, right: 0, display: 'flex', flexDirection: 'column', alignItems: 'center',
        opacity: f >= t41 ? 1 : 0, transform: `scale(${f < tNA ? 1 : 0.62}) translateY(${f < tNA ? 0 : -110}px)`, transition: 'none'}}>
        <div style={{fontFamily: EN, fontWeight: 900, fontSize: 260, color: K.yellow, lineHeight: 1, textShadow: '0 12px 0 #000'}}>{count}</div>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 64, color: K.white}}>قاعة بس في العالم كله</div>
      </div>
      {label('أمريكا وكندا', 'أغلبهم', tNA + 6, 540, 1360, K.yellow, K.ink, tUK)}
      {label('بريطانيا', '3', tUK + 4, 330, 1300, K.yellow, K.ink, tAU)}
      {label('أوروبا', '4', tEU + 2, 740, 1420, K.yellow, K.ink, tAU)}
      {label('أستراليا', '1', tAU + 6, 540, 1360, K.yellow, K.ink, tNone)}
      {f >= tAF ? <Pop at={tAF} x={scr(30, 26)[0]} y={scr(30, 26)[1]}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 130, color: K.red, textShadow: '0 6px 0 #000'}}>✕</div></Pop> : null}
      {label('أفريقيا', '0', tAF + 4, 300, 1380, K.red, K.white)}
      {label('آسيا', '0', tAS, 780, 1380, K.red, K.white)}
    </Scene>
  );
};

// 6. Projection: a beam from the projection window carries film frames up to the giant screen.
export const S1Beam: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const {width: W, height: H} = useVideoConfig();
  const at = useBeats(b);
  const lit = lin(f, 4, 24);
  return (
    <Scene bg="#070605">
      <div style={{position: 'absolute', left: 50, right: 50, top: 170, height: 640, background: '#222', borderRadius: 10, overflow: 'hidden',
        boxShadow: `0 0 ${120 * lit}px rgba(255,240,200,${0.35 * lit})`}}>
        <Img src={img(PJ + 'img/poster.jpg')} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: '50% 35%', opacity: lit * (0.85 + 0.15 * rnd(f)),
          filter: 'contrast(1.1)'}} />
      </div>
      <Beam x={540} y={1330} ang={-90} len={1200} spread={56} op={0.35 * lit} width={W} height={H} />
      {Array.from({length: 6}, (_, i) => {
        const k = ((f - 6 - i * 9) % 54) / 54;
        if (f < 6 + i * 9) return null;
        const y = 1300 - k * 900, s = 0.25 + k * 1.1;
        return (
          <div key={i} style={{position: 'absolute', left: 540, top: y, transform: `translate(-50%,-50%) scale(${s}) rotate(${(rnd(i) - 0.5) * 20}deg)`, opacity: 1 - k}}>
            <Strip frames={[PJ + 'img/poster.jpg']} fw={120} fh={88} holes={3} />
          </div>
        );
      })}
      {/* audience silhouettes */}
      <svg width={W} height={H} style={{position: 'absolute'}}>
        {Array.from({length: 3}, (_, r) => Array.from({length: 7}, (_, i) => {
          const x = 60 + i * 160 + (r % 2) * 80, y = 1420 + r * 110;
          return <g key={`${r}${i}`} fill="#000"><circle cx={x} cy={y - 60} r={34} /><rect x={x - 55} y={y - 30} width={110} height={120} rx={40} /></g>;
        }))}
        <rect x={470} y={1300} width={140} height={60} rx={8} fill="#1d1a16" stroke="#3a352d" strokeWidth={4} />
      </svg>
      <Pop at={at('raw', 2)} x={540} y={900} rot={-3}><Tag text="IMAX خام 70mm" bg={K.yellow} size={64} /></Pop>
      <Pop at={at('proj', 5)} x={540} y={1010} rot={3}><Tag text="بروجكشن من الشريط نفسه" size={50} /></Pop>
    </Scene>
  );
};

// 7. Behind Aly (middle): IMAX in Egypt = digital.
export const S1Egypt: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const at = useBeats(b);
  const e = spr(f, fps, at('egypt', 0.8), 120, 14);
  const [x0, y0] = lonLat(24.5, 32), [x1, y1] = lonLat(37.5, 21.5);
  const s = 520 / (x1 - x0);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: 60, top: 120, width: 560, height: 520, transform: `scale(${e}) rotate(${(1 - e) * -20}deg)`, opacity: e}}>
        <svg width={560} height={520}>
          <g transform={`translate(${20 - x0 * s},${10 - y0 * s}) scale(${s})`}>
            <MapPaths only={['EGY']} style={() => ({fill: K.paper, stroke: K.ink, strokeWidth: 3 / s})} />
          </g>
          <circle cx={300} cy={200} r={18} fill={K.red} stroke={K.ink} strokeWidth={4} />
        </svg>
        <Halftone color="#000" size={9} dot={0.2} opacity={0.15} />
      </div>
      <Pop at={at('egypt', 0.8) + 6} x={760} y={200} rot={-4}><Tag text="IMAX في مصر" size={60} /></Pop>
      <div style={{position: 'absolute', left: 640, top: 330}}>
        <Stamp text="= ديجيتال" at={at('digital', 4)} size={88} rot={10} />
      </div>
      {f >= at('digital', 4) ? (
        <div style={{position: 'absolute', left: 700, top: 500, display: 'grid', gridTemplateColumns: 'repeat(6, 44px)', gap: 4}}>
          {Array.from({length: 24}, (_, i) => (
            <div key={i} style={{width: 44, height: 44, background: [K.cyan, K.yellow, K.red, K.paper][Math.floor(rnd(i) * 4)],
              opacity: lin(f, at('digital', 4) + i, at('digital', 4) + i + 6)}} />
          ))}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// 8. Raw film grain vs digital pixels (same picture, zoom in).
export const S1Compare: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const tRaw = at('raw', 2.2), tDig = at('digital', 3), tZoom = at('zoom', 4.6), tNe = at('notsame', 5.4);
  const z = 1 + 1.6 * lin(f, tZoom, tZoom + 40);
  const half = (top: boolean) => (
    <div style={{position: 'absolute', left: 50, right: 50, top: top ? 150 : 850, height: 640, overflow: 'hidden', borderRadius: 12, border: `5px solid ${top ? K.yellow : K.cyan}`,
      opacity: lin(f, top ? tRaw - 8 : tDig - 8, top ? tRaw : tDig), background: '#000'}}>
      <Img src={img(PJ + (top ? 'img/poster_grain.jpg' : 'img/poster_px.png'))} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${z})`,
        transformOrigin: '50% 30%', imageRendering: top ? 'auto' : 'pixelated'}} />
      {top ? <Img src={img(`bg/grain_${Math.floor(f / 2) % 3}.png`)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: 0.5, mixBlendMode: 'overlay'}} /> : null}
      <div style={{position: 'absolute', top: 24, right: 24}}><Tag text={top ? 'خام 70mm' : 'ديجيتال'} bg={top ? K.yellow : K.cyan} size={56} /></div>
    </div>
  );
  return (
    <Scene bg={K.ink}>
      {half(true)}
      {half(false)}
      <Pop at={tNe} x={540} y={820}>
        <div style={{width: 150, height: 150, borderRadius: 75, background: K.red, color: K.white, fontFamily: EN, fontWeight: 900, fontSize: 130, lineHeight: '140px',
          textAlign: 'center', border: `6px solid ${K.ink}`}}>≠</div>
      </Pop>
    </Scene>
  );
};

// Odyssey-like illustration (ship on the sea at sunset) used as "the picture" for aspect-ratio crops.
export const ShipScene: React.FC<{w: number; h: number}> = ({w, h}) => {
  const f = useCurrentFrame();
  return (
    <svg width={w} height={h} viewBox="0 0 1000 700" preserveAspectRatio="xMidYMid slice">
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#1B1A2E" /><stop offset="0.55" stopColor="#B4432A" /><stop offset="1" stopColor="#F2B04A" /></linearGradient>
      </defs>
      <rect width={1000} height={700} fill="url(#sky)" />
      <circle cx={500} cy={420} r={130} fill="#FFD27A" />
      {Array.from({length: 7}, (_, i) => <path key={i} d={`M${i * 160 - 80},${470 + i * 4} q40,-14 80,0 t80,0`} stroke="#000" strokeWidth={3} fill="none" opacity={0.25} transform={`translate(${(f * 0.6) % 160},0)`} />)}
      <rect y={440} width={1000} height={260} fill="#14223A" />
      {Array.from({length: 9}, (_, i) => <path key={'w' + i} d={`M-100,${470 + i * 28} ${Array.from({length: 14}, (_, k) => `q35,${i % 2 ? -10 : 10} 80,0`).join(' ')}`}
        stroke="#F2B04A" strokeOpacity={0.35 - i * 0.03} strokeWidth={4} fill="none" transform={`translate(${((f * (1 + i * 0.2)) % 80) - 80},0)`} />)}
      <g transform={`translate(380,${400 + Math.sin(f / 10) * 6}) rotate(${Math.sin(f / 14) * 2})`}>
        <path d="M0,60 L260,60 L230,95 L30,95 Z" fill="#0A0A0A" />
        <line x1={130} y1={60} x2={130} y2={-120} stroke="#0A0A0A" strokeWidth={8} />
        <path d="M60,-110 Q130,-60 200,-110 L200,30 Q130,50 60,30 Z" fill="#E9E1CF" stroke="#0A0A0A" strokeWidth={5} />
        {Array.from({length: 8}, (_, i) => <line key={i} x1={40 + i * 26} y1={95} x2={20 + i * 26} y2={135} stroke="#0A0A0A" strokeWidth={5} />)}
      </g>
      {Array.from({length: 4}, (_, i) => <path key={'b' + i} d={`M${200 + i * 140 + (f % 300) * 0.4},${150 + i * 20} q12,-12 24,0 q12,-12 24,0`} stroke="#000" strokeWidth={4} fill="none" />)}
    </svg>
  );
};

// 9. Aspect ratio: full IMAX frame -> cropped a bit (digital IMAX) -> cropped a lot (normal cinema). Cut strips fall away.
export const S1Aspect: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const c1 = at('cut1', 5), c2 = at('cut2', 9);
  const W = 1000, H0 = W / 1.43, H1 = W / 1.9, H2 = W / 2.39;
  const h = H0 + (H1 - H0) * lin(f, c1, c1 + 12) + (H2 - H1) * lin(f, c2, c2 + 12);
  const top = 780 - H0 / 2;
  const cut = (k: number, a: number, hh: number) => {
    if (f < a) return null;
    const fall = lin(f, a + 10, a + 40, 0, 1, Easing.in(Easing.quad));
    return [0, 1].map((side) => (
      <div key={side + '' + k} style={{position: 'absolute', left: 40, width: W, height: hh, top: side ? top + H0 - hh : top, overflow: 'hidden', opacity: 1 - fall * 0.6,
        transform: `translateY(${(side ? 1 : -1) * fall * 900}px) rotate(${(side ? 1 : -1) * fall * 25}deg)`, border: `4px dashed ${K.red}`}}>
        <div style={{position: 'absolute', left: 0, top: side ? -(H0 - hh) : 0}}><ShipScene w={W} h={H0} /></div>
      </div>
    ));
  };
  const lab = f < c1 ? 'IMAX خام 70mm = الصورة كاملة' : f < c2 ? 'IMAX ديجيتال: مقصوص حتة' : 'سينما عادية: مقصوص كتير';
  return (
    <Scene bg={K.ink}>
      <div style={{position: 'absolute', left: 40, top: top + (H0 - h) / 2, width: W, height: h, overflow: 'hidden', boxShadow: '0 30px 60px rgba(0,0,0,0.6)'}}>
        <div style={{position: 'absolute', top: -(H0 - h) / 2}}><ShipScene w={W} h={H0} /></div>
      </div>
      {cut(1, c1, (H0 - H1) / 2)}
      {cut(2, c2, (H1 - H2) / 2 + (H0 - H1) / 2)}
      <div style={{position: 'absolute', top: 210, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
        <Tag key={lab} text={lab} bg={f < c1 ? K.yellow : K.red} color={f < c1 ? K.ink : K.white} size={58} />
      </div>
      <div style={{position: 'absolute', top: 1230, left: 0, right: 0, textAlign: 'center', fontFamily: EN, fontWeight: 900, fontSize: 110, color: K.white}}>
        {f < c1 ? '1.43 : 1' : f < c2 ? '1.90 : 1' : '2.39 : 1'}
      </div>
      {[c1, c2].map((a, i) => f >= a - 4 && f < a + 16 ? (
        <div key={i} style={{position: 'absolute', left: lin(f, a - 4, a + 14, -150, 1100, (x) => x), top: top + (i ? (H0 - H1) / 2 : 0) - 60, fontSize: 110}}>✂️</div>
      ) : null)}
    </Scene>
  );
};

// 10. Front overlay on Aly at the end: "don't watch it in a normal cinema".
export const S1End: React.FC<B> = ({b}) => {
  const at = useBeats(b);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: 0, right: 0, top: 380, display: 'flex', justifyContent: 'center'}}>
        <Stamp text="✕ سينما عادية" at={at('stamp', 0.3)} size={110} rot={-8} />
      </div>
    </AbsoluteFill>
  );
};
