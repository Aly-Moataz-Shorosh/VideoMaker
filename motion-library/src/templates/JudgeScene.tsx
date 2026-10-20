import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {z} from 'zod';
import {Base, Highlight} from '../blocks/Base';
import {C, theme} from '../blocks/theme';
import {enter, exit, lerp} from '../blocks/anim';
import {MapPaths, Person, lonLat} from '../blocks/geo';

// Big full-screen scene (Aly 2026-10-07, figmaMake @2:41): "objective vs subjective grading".
// World map: a cat and a dog photo; two people in China + one in the USA all point and agree (dog / cat) ->
// camera flies to Egypt, university pin + "same university / dept / subject" chips -> split screen: two doctors
// grade the SAME answer and give different marks. All *At = frames from the cue start.
export const judgeSceneSchema = z.object({
  cat: z.string().default('pics/cat.jpg'),
  dog: z.string().default('pics/dog.jpg'),
  photosAt: z.number().default(10),
  aiAt: z.number().default(40), // "any simple AI model knows" tag
  chinaAt: z.number().default(110),
  usaAt: z.number().default(150),
  pointAt: z.number().default(220),
  egyptAt: z.number().default(270),
  chips: z.array(z.object({text: z.string(), at: z.number()})).default([
    {text: 'نفس الجامعة', at: 320}, {text: 'نفس القسم', at: 355}, {text: 'نفس المادة', at: 390}]),
  uniLabel: z.string().default('جامعة'),
  splitAt: z.number().default(440),
  grade1: z.string().default('7/10'),
  grade1At: z.number().default(520),
  grade2: z.string().default('6/10'),
  grade2At: z.number().default(570),
  previewBg: z.string().default(''),
});

const io = Easing.inOut(Easing.cubic);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

const Flag: React.FC<{kind: 'cn' | 'us'; x: number; y: number}> = ({kind, x, y}) => (
  <g transform={`translate(${x},${y})`}>
    <line x1={0} y1={0} x2={0} y2={70} stroke="#C9D1DC" strokeWidth={4} />
    {kind === 'cn' ? (
      <>
        <rect x={2} y={0} width={66} height={44} fill="#DE2910" />
        <polygon points="16,8 19,17 28,17 21,22 24,31 16,26 8,31 11,22 4,17 13,17" fill="#FFDE00" />
      </>
    ) : (
      <>
        {Array.from({length: 7}).map((_, i) => <rect key={i} x={2} y={i * 6.3} width={66} height={3.2} fill="#B22234" />)}
        <rect x={2} y={3.2} width={66} height={3.1} fill="#fff" opacity={0} />
        <rect x={2} y={0} width={28} height={22} fill="#3C3B6E" />
      </>
    )}
  </g>
);

const Bubble: React.FC<{x: number; y: number; text: string; p: number; color: string}> = ({x, y, text, p, color}) => (
  <div style={{position: 'absolute', left: x - 150, top: y, width: 300, display: 'flex', justifyContent: 'center', opacity: p,
    transform: `scale(${lerp(p, 0.4, 1)})`, transformOrigin: '50% 100%'}}>
    <div style={{background: '#FFFFFF', color: '#14181F', borderRadius: 26, padding: '6px 26px', fontSize: 44, fontWeight: 900,
      boxShadow: theme.shadow, borderBottom: `6px solid ${color}`, whiteSpace: 'nowrap'}}>{text}</div>
  </div>
);

export const JudgeScene: React.FC<z.infer<typeof judgeSceneSchema>> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const inP = interpolate(frame, [0, 10], [0, 1], clamp);
  const outP = exit(frame, durationInFrames, 10);

  const vert = height > width; // 9:16: smaller world, photos left/right on top, doctors split top/bottom
  // camera: world view -> Egypt
  const fly = interpolate(frame, [p.egyptAt, p.egyptAt + 40], [0, 1], {...clamp, easing: io});
  const [ex, ey] = lonLat(31.3, 29.85); // Helwan / Cairo
  const camX = lerp(fly, vert ? 1850 : 1900, ex), camY = lerp(fly, vert ? 640 : 600, ey);
  const sc = Math.exp(lerp(fly, Math.log(vert ? 0.37 : 0.72), Math.log(9)));
  const proj = (lon: number, lat: number) => {
    const [x, y] = lonLat(lon, lat);
    return [(x - camX) * sc + width / 2, (y - camY) * sc + height / 2];
  };
  const worldFade = 1 - fly;
  const split = interpolate(frame, [p.splitAt, p.splitAt + 18], [0, 1], {...clamp, easing: io});

  const photoP = enter(frame, fps, p.photosAt) * worldFade;
  const aiP = Math.min(enter(frame, fps, p.aiAt), interpolate(frame, [p.chinaAt - 6, p.chinaAt], [1, 0], clamp));
  const point = enter(frame, fps, p.pointAt);
  const [cnx, cny] = proj(104, 33), [usx, usy] = proj(-98, 38);
  const people = [
    {x: cnx - (vert ? 70 : 130), y: cny + 40, at: p.chinaAt, flag: 'cn' as const, say: 'ده الكلب', c: C.blue},
    {x: cnx + (vert ? 70 : 130), y: cny + 40, at: p.chinaAt + 8, flag: 'cn' as const, say: 'ودي القطة', c: C.gold},
    {x: usx, y: usy + 40, at: p.usaAt, flag: 'us' as const, say: 'ده الكلب', c: C.blue},
  ];
  const ps = vert ? 0.6 : 1; // people scale
  const [ux, uy] = proj(31.3, 29.85);
  const pin = enter(frame, fps, p.egyptAt + 34);

  const world = (
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 40%, #173149, #0A131C)'}}>
      <svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
        <g transform={`translate(${width / 2},${height / 2}) scale(${sc}) translate(${-camX},${-camY})`}>
          <MapPaths style={(k) => ({
            fill: k === 'EGY' ? lerp(fly, 0, 1) > 0.5 ? '#E9D3A1' : '#3A4757' : k === 'CHN' || k === 'USA' ? '#3A5068' : '#26313E',
            stroke: k === 'EGY' && fly > 0.5 ? C.gold : '#3E4C5C', strokeWidth: (k === 'EGY' && fly > 0.5 ? 2.2 : 0.8) / sc * 0.9,
          })} />
        </g>
        {people.map((q, i) => {
          const a = enter(frame, fps, q.at) * worldFade;
          if (a <= 0.01) return null;
          return (
            <g key={i} opacity={a} transform={`translate(${q.x},${q.y + lerp(a, 60, 0)}) scale(${ps})`}>
              <Flag kind={q.flag} x={70} y={-230} />
              <Person x={0} y={0} s={170} color="#FFFFFF" armsUp={point * (i % 2 ? 0.8 : 1)} look={i === 2 ? 1 : -0.6} />
            </g>
          );
        })}
      </svg>
      {/* cat & dog photos */}
      {[{src: p.dog, x: vert ? 0.27 : 0.4, label: 'كلب', c: C.blue}, {src: p.cat, x: vert ? 0.73 : 0.6, label: 'قطة', c: C.gold}].map((ph, i) => {
        const a = enter(frame, fps, p.photosAt + i * 6) * worldFade;
        if (a <= 0.01) return null;
        const w = 300;
        return (
          <div key={i} style={{position: 'absolute', left: width * ph.x - w / 2, top: height * (vert ? 0.08 : 0.1), width: w, opacity: Math.min(1, a * 1.4),
            transform: `translateY(${lerp(a, -80, 0)}px) rotate(${(i ? 4 : -4) * a}deg)`}}>
            <div style={{width: w, height: w, borderRadius: 18, overflow: 'hidden', border: '8px solid #fff', boxShadow: theme.shadow}}>
              <Img src={staticFile(ph.src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
            </div>
            <div style={{position: 'absolute', bottom: -30, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: point}}>
              <div style={{background: ph.c, color: '#0B0E13', fontSize: 46, fontWeight: 900, padding: '0 30px', borderRadius: 999,
                transform: `scale(${lerp(point, 0.3, 1)})`}}>{ph.label} ✓</div>
            </div>
          </div>
        );
      })}
      {aiP > 0.01 ? (
        <div style={{position: 'absolute', left: 0, right: 0, top: height * (vert ? 0.3 : 0.47), display: 'flex', justifyContent: 'center', opacity: aiP * worldFade}}>
          <div style={{background: C.panel, borderRadius: 999, padding: '10px 40px', fontSize: 56, fontWeight: 900, boxShadow: theme.shadow,
            borderBottom: `6px solid ${C.blue}`, transform: `scale(${lerp(aiP, 0.6, 1)})`}}>
            <Highlight text="أي موديل *AI* بسيط يعرفهم" accent={C.blue} />
          </div>
        </div>
      ) : null}
      {people.map((q, i) => (
        <Bubble key={i} x={q.x} y={q.y - 330 * ps - (i === 1 ? 70 * ps : 0) - (vert ? 40 : 0)} text={q.say} p={Math.min(enter(frame, fps, p.pointAt + 6 + i * 6), worldFade)} color={q.c} />
      ))}
      {point > 0.05 && worldFade > 0.05 ? (
        <div style={{position: 'absolute', left: 0, right: 0, bottom: height * 0.07, display: 'flex', justifyContent: 'center',
          opacity: Math.min(enter(frame, fps, p.pointAt + 24), worldFade)}}>
          <div style={{background: C.green, color: '#0B0E13', borderRadius: 999, padding: '6px 40px', fontSize: 54, fontWeight: 900}}>
            <Highlight text="كل الناس متفقين ✓" accent="#0B0E13" />
          </div>
        </div>
      ) : null}
      {/* university pin in Egypt */}
      {pin > 0.01 ? (
        <>
          <div style={{position: 'absolute', left: ux - 60, top: uy - 150 + lerp(pin, -200, 0), width: 120, height: 150, opacity: Math.min(1, pin * 2)}}>
            <svg viewBox="0 0 120 150" width={120} height={150}>
              <path d="M60 146 C60 146 10 86 10 56 A50 50 0 1 1 110 56 C110 86 60 146 60 146Z" fill={C.red} stroke="#fff" strokeWidth={5} />
              <path d="M60 24 L92 40 L28 40 Z M34 44 h52 v6 h-52z M38 52 h8 v24 h-8z M56 52 h8 v24 h-8z M74 52 h8 v24 h-8z M32 78 h56 v8 h-56z" fill="#fff" />
            </svg>
          </div>
          <div style={{position: 'absolute', left: ux - 300, width: 600, top: uy + 20, textAlign: 'center', fontFamily: 'Amiri', fontSize: 92,
            color: '#F2E9D8', textShadow: '0 4px 18px #000', opacity: pin}}>{p.uniLabel}</div>
        </>
      ) : null}
      <div style={{position: 'absolute', right: width * 0.05, top: height * (vert ? 0.62 : 0.2), display: 'flex', flexDirection: 'column', gap: 26, alignItems: 'flex-start'}}>
        {p.chips.map((c, i) => {
          const a = enter(frame, fps, c.at);
          if (a <= 0.01) return null;
          return (
            <div key={i} style={{background: C.panel, borderRadius: 999, padding: '8px 36px', fontSize: 58, fontWeight: 900, boxShadow: theme.shadow,
              borderRight: `10px solid ${C.gold}`, opacity: a, transform: `translateX(${lerp(a, 200, 0)}px)`}}>{c.text}</div>
          );
        })}
      </div>
    </AbsoluteFill>
  );

  // split screen: two doctors, same answer sheet, different marks
  const doctor = (k: number, bw: number, bh: number) => {
    const u = bh / 1080;
    const g = k ? p.grade2 : p.grade1, at = k ? p.grade2At : p.grade1At;
    const stamp = enter(frame, fps, at);
    const col = k ? C.red : C.gold;
    return (
      <AbsoluteFill style={{background: k ? '#1A2230' : '#202838'}}>
        <svg width={bw} height={bh} style={{position: 'absolute', left: 0, top: 0}}>
          <Person x={bw * 0.26} y={bh * 0.86} s={300 * u} color="#F2F4F7" look={1} armsUp={0} />
        </svg>
        <div style={{position: 'absolute', left: bw * 0.08, top: bh * 0.08, fontSize: 64 * u, fontWeight: 900}}>
          {k ? 'دكتور ٢' : 'دكتور ١'}
        </div>
        {/* answer sheet */}
        <div style={{position: 'absolute', left: bw * 0.48, top: bh * 0.2, width: bw * 0.44, height: bh * 0.62, background: '#F7F3EA',
          borderRadius: 14, boxShadow: theme.shadow, transform: `rotate(${k ? 3 : -3}deg)`, padding: 34 * u, boxSizing: 'border-box'}}>
          <div style={{color: '#14181F', fontSize: 38 * u, fontWeight: 900, marginBottom: 18 * u}}>سؤال مقالي</div>
          {Array.from({length: 8}).map((_, i) => (
            <div key={i} style={{height: 12 * u, borderRadius: 6, background: '#B9B2A2', margin: `${22 * u}px 0`, width: `${[96, 88, 92, 70, 94, 84, 90, 60][i]}%`}} />
          ))}
          <div style={{position: 'absolute', right: -40 * u, bottom: -30 * u, width: 210 * u, height: 210 * u, borderRadius: 105 * u, border: `${10 * u}px solid ${col}`,
            display: 'flex', alignItems: 'center', justifyContent: 'center', color: col, fontSize: 84 * u, fontWeight: 900, direction: 'ltr',
            fontFamily: 'Montserrat', opacity: stamp, transform: `scale(${lerp(stamp, 2.2, 1)}) rotate(-12deg)`, background: '#F7F3EAcc'}}>{g}</div>
        </div>
      </AbsoluteFill>
    );
  };

  return (
    <Base previewBg={p.previewBg}>
      <AbsoluteFill style={{opacity: inP * outP, transform: `scale(${lerp(inP, 1.1, 1)})`}}>
        {world}
        {split > 0 ? (
          <>
            {vert ? (
              <>
                <div style={{position: 'absolute', left: 0, top: 0, width, height: height / 2, overflow: 'hidden', transform: `translateX(${(split - 1) * width}px)`}}>{doctor(0, width, height / 2)}</div>
                <div style={{position: 'absolute', left: 0, top: height / 2, width, height: height / 2, overflow: 'hidden', transform: `translateX(${(1 - split) * width}px)`}}>{doctor(1, width, height / 2)}</div>
                <div style={{position: 'absolute', left: 0, top: height / 2 - 5, width: '100%', height: 10, background: C.gold, opacity: split}} />
              </>
            ) : (
              <>
                <AbsoluteFill style={{clipPath: `inset(0 ${lerp(split, 100, 50)}% 0 0)`}}>{doctor(1, width / 2, height)}</AbsoluteFill>
                <AbsoluteFill style={{left: width / 2, width: width / 2, clipPath: `inset(0 0 0 ${lerp(split, 100, 0)}%)`}}>{doctor(0, width / 2, height)}</AbsoluteFill>
                <div style={{position: 'absolute', left: width / 2 - 5, top: 0, width: 10, height: '100%', background: C.gold, opacity: split}} />
              </>
            )}
            <div style={{position: 'absolute', left: 0, right: 0, top: height * (vert ? 0.465 : 0.86), display: 'flex', justifyContent: 'center',
              opacity: enter(frame, fps, p.grade2At + 12)}}>
              <div style={{background: C.panel, borderRadius: 999, padding: '8px 44px', fontSize: 60, fontWeight: 900, boxShadow: theme.shadow,
                borderBottom: `6px solid ${C.gold}`}}>
                <Highlight text="نفس الإجابة.. *درجة مختلفة*" accent={C.gold} />
              </div>
            </div>
          </>
        ) : null}
      </AbsoluteFill>
    </Base>
  );
};
