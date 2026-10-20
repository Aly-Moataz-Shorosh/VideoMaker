import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {z} from 'zod';
import {Base, Highlight} from '../blocks/Base';
import {C, theme} from '../blocks/theme';
import {enter, lerp} from '../blocks/anim';
import {MapPaths, Person, fillPoints, lonLat} from '../blocks/geo';

// Big full-screen scene (Aly 2026-10-07, figmaMake @0:15): map of Egypt (غطاء map look) fills with people
// (1 icon ≈ 1 million, Statistics-Easy-Learn style) -> each gets a laptop -> they jump & raise hands (competition)
// -> one grows and glows, everyone looks at him -> the map closes like a book and flies off (back to Aly).
// All *At props = frames from the cue start.
export const egyptCrowdSchema = z.object({
  count: z.number().default(120), // icons (and the counter value)
  unit: z.string().default('مليون'),
  label: z.string().default('مصري'),
  peopleAt: z.number().default(20),
  laptopAt: z.number().default(70),
  jumpAt: z.number().default(120),
  heroAt: z.number().default(180),
  closeAt: z.number().default(250),
  title1: z.string().default('*120 مليون* مصري'),
  title2: z.string().default('كلهم *مبرمجين*'),
  title3: z.string().default('المنافسة *عالية*'),
  title4: z.string().default('إيه اللي *يميزك*؟'),
  previewBg: z.string().default(''),
});

const io = Easing.inOut(Easing.cubic);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const NEAR = ['EGY', 'LBY', 'SDN', 'ISR', 'PSE', 'JOR', 'SAU', 'TCD', 'SYR', 'LBN', 'CYP', 'GRC', 'TUR', 'IRQ', 'ERI', 'YEM', 'TUN', 'NER', 'SSD', 'ETH', 'CAF'];

export const EgyptCrowd: React.FC<z.infer<typeof egyptCrowdSchema>> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const vert = height > width;
  const pts = React.useMemo(() => fillPoints('EGY', p.count), [p.count]);
  const [cx, cy] = lonLat(30.4, 26.9);
  const hero = React.useMemo(() => {
    let best = 0, d = 1e9;
    pts.forEach(([x, y], i) => {const k = (x - cx) ** 2 + (y - cy - 6) ** 2; if (k < d) {d = k; best = i;}});
    return best;
  }, [pts, cx, cy]);

  // camera: wide region -> Egypt fills the screen (slow push all the time)
  const zoomIn = interpolate(frame, [0, 40], [0, 1], {...clamp, easing: io});
  const scale = lerp(zoomIn, 2.2, 8.6) * interpolate(frame, [40, p.closeAt], [1, 1.06], clamp);
  const camX = vert ? cx : cx + 9, camY = vert ? cy + 8 : cy; // 16:9: Egypt left of center -> titles right; 9:16: centered, titles on top
  const s = 6.2; // person size (map units)
  const appear = (i: number) => enter(frame, fps, p.peopleAt + (i / pts.length) * 30);
  const lap = (i: number) => enter(frame, fps, p.laptopAt + (i / pts.length) * 24);
  const jumping = frame >= p.jumpAt && frame < p.heroAt + 10;
  const heroP = enter(frame, fps, p.heroAt);
  const [hx, hy] = pts[hero] || [cx, cy];

  const scene = (
    <AbsoluteFill style={{background: '#0E1A26'}}>
      <svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
        <defs>
          <radialGradient id="ec-sea" cx="50%" cy="45%" r="70%">
            <stop offset="0%" stopColor="#173149" /><stop offset="100%" stopColor="#0A131C" />
          </radialGradient>
          <filter id="ec-glow"><feGaussianBlur stdDeviation="1.6" /></filter>
        </defs>
        <rect width={width} height={height} fill="url(#ec-sea)" />
        <g transform={`translate(${width / 2},${height / 2}) scale(${scale}) translate(${-camX},${-camY})`}>
          <MapPaths only={NEAR} style={(k) => k === 'EGY'
            ? {fill: '#E9D3A1', stroke: C.gold, strokeWidth: 0.9, strokeLinejoin: 'round'}
            : {fill: '#2A3644', stroke: '#3E4C5C', strokeWidth: 0.4}} />
          <MapPaths only={['EGY']} style={() => ({fill: 'none', stroke: C.gold, strokeWidth: 2.4, opacity: 0.35, filter: 'url(#ec-glow)'})} />
          {/* Nile (approximate) */}
          <path d={[[31.2, 21.9], [31.6, 23.8], [32.9, 24.1], [32.6, 25.7], [32.7, 26.2], [31.6, 27.2], [30.8, 28.6], [31.2, 30.05], [30.4, 31.4]]
            .map(([lo, la], i) => (i ? 'L' : 'M') + lonLat(lo, la).join(',')).join('')}
            fill="none" stroke="#3BA9F5" strokeWidth={1.3} strokeLinecap="round" strokeLinejoin="round" opacity={0.85}
            strokeDasharray="400" strokeDashoffset={interpolate(frame, [8, 40], [400, 0], clamp)} />
          {pts.map(([x, y], i) => {
            const a = appear(i);
            if (a <= 0.01) return null;
            const isHero = i === hero;
            const ph = (i * 2.399) % (Math.PI * 2);
            const j = jumping ? Math.abs(Math.sin((frame - p.jumpAt) / 3.2 + ph)) : 0;
            const ramp = interpolate(frame, [p.jumpAt, p.jumpAt + 8, p.heroAt, p.heroAt + 10], [0, 1, 1, 0], clamp);
            const look = Math.max(-1, Math.min(1, (hx - x) / 12)) * heroP;
            const grow = isHero ? lerp(heroP, 1, 3.4) : 1;
            const yy = y + s * 0.6 - j * s * 0.7 * ramp - (isHero ? heroP * s * 0.8 : 0);
            return (
              <g key={i} transform={`translate(${x},${yy}) scale(${a * grow}) translate(${-x},${-yy})`}>
                {isHero && heroP > 0.05 ? <circle cx={x} cy={yy - s * 0.6} r={s * 1.1} fill={C.gold} opacity={0.35 * heroP} filter="url(#ec-glow)" /> : null}
                <Person x={x} y={yy} s={s} color={isHero && heroP > 0.05 ? C.gold : '#FFFFFF'} armsUp={isHero ? heroP : ramp * (0.5 + 0.5 * j)}
                  look={isHero ? 0 : look} laptop={lap(i)} dim={isHero ? 0 : heroP} screen={isHero && heroP > 0.05 ? C.gold : C.blue} />
              </g>
            );
          })}
        </g>
      </svg>
      {/* calligraphy-like place name + pin (map videos / غطاء) */}
      <div style={{position: 'absolute', left: width * 0.07, top: vert ? height * 0.74 : height * 0.1, opacity: interpolate(frame, [20, 32], [0, 1], clamp) * (1 - heroP * 0.6),
        fontFamily: 'Amiri', fontSize: 120, color: '#F2E9D8', textShadow: '0 6px 24px #000', transform: `translateY(${lerp(enter(frame, fps, 20), 30, 0)}px)`}}>
        مصر
      </div>
      {[p.title1, p.title2, p.title3, p.title4].map((t, k) => {
        const at = [p.peopleAt, p.laptopAt, p.jumpAt, p.heroAt][k];
        const nx = [p.laptopAt, p.jumpAt, p.heroAt, p.closeAt][k];
        const a = Math.min(enter(frame, fps, at + 4), interpolate(frame, [nx - 4, nx + 2], [1, 0], clamp));
        if (a <= 0.01) return null;
        return (
          <div key={k} style={{position: 'absolute', right: width * 0.05, top: vert ? height * 0.12 : height * 0.36, width: vert ? width * 0.9 : width * 0.34, display: 'flex', justifyContent: 'center',
            opacity: a, transform: `scale(${lerp(a, 0.7, 1)}) rotate(-2deg)`}}>
            <div style={{background: C.panel, borderRadius: theme.radius, padding: '18px 40px', fontSize: 92, fontWeight: 900, lineHeight: 1.2,
              textAlign: 'center', boxShadow: theme.shadow, borderBottom: `8px solid ${C.gold}`}}>
              <Highlight text={t} accent={C.gold} />
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );

  // book close: right half folds over the left (rotateY), then the closed book shrinks and flies off.
  const fold = interpolate(frame, [p.closeAt, p.closeAt + 16], [0, 1], {...clamp, easing: io});
  const fly = interpolate(frame, [p.closeAt + 16, durationInFrames], [0, 1], {...clamp, easing: Easing.in(Easing.cubic)});
  const inP = interpolate(frame, [0, 8], [0, 1], clamp);
  const k = Math.cos(fold * Math.PI); // flap width factor: 1 -> -1 (2D fold, reliable in headless renders)
  const half = (side: 'l' | 'r') => ({clipPath: side === 'l' ? 'inset(0 50% 0 0)' : 'inset(0 0 0 50%)'});
  return (
    <Base previewBg={p.previewBg}>
      <AbsoluteFill style={{opacity: inP * (1 - fly), transform: `translate(${-fly * width * 0.25}px, ${fly * height * 0.1}px) scale(${lerp(fly, 1, 0.25)}) rotate(${fly * -8}deg) scale(${lerp(inP, 1.15, 1)})`}}>
        {fold <= 0 ? scene : (
          <>
            <AbsoluteFill style={half('l')}>{scene}</AbsoluteFill>
            <AbsoluteFill style={{transform: `scaleX(${k})`, transformOrigin: '50% 50%', filter: `brightness(${1 - 0.4 * Math.abs(Math.sin(fold * Math.PI))})`}}>
              {k > 0 ? <AbsoluteFill style={half('r')}>{scene}</AbsoluteFill> : (
                <AbsoluteFill style={{...half('r'), background: `linear-gradient(135deg, ${C.panel}, #0B0E13)`}}>
                  <div style={{position: 'absolute', left: '50%', width: '50%', height: '100%', boxSizing: 'border-box', borderLeft: `14px solid ${C.gold}`,
                    display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'Amiri', fontSize: 160, color: C.gold, transform: 'scaleX(-1)'}}>مصر</div>
                </AbsoluteFill>
              )}
            </AbsoluteFill>
          </>
        )}
      </AbsoluteFill>
    </Base>
  );
};
