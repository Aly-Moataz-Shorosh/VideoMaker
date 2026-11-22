import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {fontCss} from '../blocks/theme';
import {AR, EN, lin, spr} from '../film/kit';
import {Rewind, S, bi, groupLatin} from '../stage/kit';

// Garrett Warren @ UTH Festival 2026 (GEM) — vertical phone recording of a talk (Aly 2026-11-22, style 13 lecture-stage).
// Phone footage fills 9:16; hook -> rewind -> answer from "Hit me"; English captions (ElevenLabs Scribe, fixed) + Egyptian
// Arabic translation under them; a tray of real film pictures on every word over the empty stage floor; channel footer.
// Props: projects/<date> reel-h garrett warren/work/scripts/make_props.py
const W = 1080, H = 1920;
const Y = {tag: 104, head: 150, cap: 1110, tray: 1326, trayH: 450, foot: 1814};
const cue = z.object({t: z.number(), d: z.number(), k: z.string(), p: z.record(z.string(), z.any()).default({})});
const word = z.object({w: z.string(), s: z.number(), e: z.number()});
export const uthReelSchema = z.object({
  duration: z.number().default(5),
  cam: z.string().default(''),
  voice: z.string().default(''),
  hookEnd: z.number().default(0),
  rewind: z.object({t: z.number(), d: z.number(), from: z.string(), to: z.string()}).nullable().default(null),
  head: z.string().default(''),
  tag: z.string().default(''),
  tagAr: z.string().default(''),
  caps: z.array(z.object({t0: z.number(), t1: z.number(), en: z.array(word), ar: z.string()})).default([]),
  cues: z.array(cue).default([]),
  sfx: z.array(z.object({t: z.number(), file: z.string(), vol: z.number().default(0.3)})).default([]),
  zoom: z.array(z.array(z.number())).default([[0, 1]]),
});
type Props = z.infer<typeof uthReelSchema>;

const interp = (keys: number[][], t: number) => {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) if (t <= keys[i][0]) {
    const [t0, v0] = keys[i - 1], [t1, v1] = keys[i];
    const x = (t - t0) / Math.max(1e-6, t1 - t0);
    return v0 + (v1 - v0) * (x * x * (3 - 2 * x));
  }
  return keys[keys.length - 1][1];
};
const fluent = (n: string) => staticFile(`fluent/${n}.png`);
const ar = (size: number, color = S.white, w = 900): React.CSSProperties => ({fontFamily: AR, fontWeight: w, fontSize: size, color, direction: 'rtl', unicodeBidi: 'isolate', lineHeight: 1.3});
const en = (size: number, color = S.white, w = 800): React.CSSProperties => ({fontFamily: EN, fontWeight: w, fontSize: size, color, lineHeight: 1.15});

// ---------- in/out of a tray scene ----------
const useIn = (dur: number, delay = 0) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return {f, fps, p: spr(f, fps, delay, 160, 15), o: 1 - lin(f, dur - 6, dur)};
};
const Pill: React.FC<{text: string; bg?: string; color?: string; size?: number}> = ({text, bg = S.yellow, color = S.ink, size = 30}) => (
  <span style={{...ar(size, color), background: bg, padding: '2px 18px 6px', borderRadius: 14, whiteSpace: 'nowrap'}}>{bi(text)}</span>
);
const Photo: React.FC<{file: string; w: number; h: number; x: number; y: number; dur: number; delay?: number; cut?: boolean; pos?: string; r?: number; z?: number}> = (
  {file, w, h, x, y, dur, delay = 0, cut, pos = 'center', r = 22, z = 1}) => {
  const {f, p, o} = useIn(dur, delay);
  const q = cut ? Math.min(1, (f - delay) / 3) : p;
  // trailer stills (tr_*) carry 2.35:1 letterbox bars inside a 16:9 frame -> zoom past them
  const push = z * (file.includes('/tr_') ? 1.34 : 1) * (1 + 0.06 * f / Math.max(1, dur));
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h, borderRadius: r, overflow: 'hidden', opacity: Math.max(0, Math.min(1, q * 1.4)) * o,
      transform: cut ? undefined : `perspective(1400px) rotateY(${(1 - q) * 8}deg) scale(${0.86 + 0.14 * q})`,
      boxShadow: '0 30px 60px rgba(0,0,0,0.55)', border: '3px solid rgba(255,255,255,0.85)', background: '#000'}}>
      <Img src={staticFile(file)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: pos, transform: `scale(${push})`}} />
    </div>
  );
};
const Under: React.FC<{text: string; y: number; dur: number; delay?: number; bg?: string; color?: string}> = ({text, y, dur, delay = 4, bg, color}) => {
  const {p, o} = useIn(dur, delay);
  return <div style={{position: 'absolute', left: 0, right: 0, top: y, display: 'flex', justifyContent: 'center', opacity: p * o, transform: `translateY(${(1 - p) * 16}px)`}}>
    <Pill text={text} bg={bg} color={color} /></div>;
};
const sec = (fps: number, s: number) => Math.round(s * fps);

// ---------- scenes (drawn in a 1000 x 450 box) ----------
const Pic: React.FC<{dur: number; file: string; label?: string; cut?: boolean; face?: string; faceAt?: number; faceLabel?: string}> = ({dur, file, label, cut, face, faceAt = 0, faceLabel}) => {
  const {fps} = useVideoConfig();
  const fa = sec(fps, faceAt);
  return (<>
    <Photo file={file} w={640} h={360} x={180} y={6} dur={dur} cut={cut} />
    {label ? <Under text={label} y={384} dur={dur} delay={cut ? 1 : 5} /> : null}
    {face ? <Sequence from={fa} layout="none"><FaceBubble file={face} label={faceLabel ?? ''} dur={dur - fa} x={760} y={190} /></Sequence> : null}
  </>);
};
const FaceBubble: React.FC<{file: string; label: string; dur: number; x: number; y: number}> = ({file, label, dur, x, y}) => {
  const {p, o} = useIn(dur);
  return (
    <div style={{position: 'absolute', left: x, top: y, width: 220, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6, opacity: o, transform: `scale(${p})`}}>
      <div style={{width: 170, height: 170, borderRadius: '50%', overflow: 'hidden', border: `5px solid ${S.yellow}`, boxShadow: '0 16px 40px rgba(0,0,0,0.6)'}}>
        <Img src={staticFile(file)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: '50% 18%'}} /></div>
      <span style={{...en(24, S.ink, 800), background: S.white, borderRadius: 10, padding: '2px 10px', whiteSpace: 'nowrap'}}>{label}</span>
    </div>
  );
};
const Vs: React.FC<{dur: number; a: string; al: string; b: string; bl: string; bAt?: number}> = ({dur, a, al, b, bl, bAt = 1}) => {
  const {fps} = useVideoConfig();
  const ba = sec(fps, bAt);
  return (<>
    <Photo file={a} w={470} h={264} x={10} y={50} dur={dur} />
    <div style={{position: 'absolute', left: 10, width: 470, top: 0}}><Under text={al} y={336} dur={dur} bg={S.white} /></div>
    <Sequence from={ba} layout="none">
      <Photo file={b} w={470} h={264} x={520} y={50} dur={dur - ba} />
      <div style={{position: 'absolute', left: 520, width: 470, top: 0}}><Under text={bl} y={336} dur={dur - ba} /></div>
    </Sequence>
    <Sequence from={ba} layout="none"><VsChip dur={dur - ba} /></Sequence>
  </>);
};
const VsChip: React.FC<{dur: number}> = ({dur}) => {
  const {p, o} = useIn(dur, 3);
  return <div style={{position: 'absolute', left: 452, top: 130, width: 96, height: 96, borderRadius: '50%', background: S.red, display: 'flex', alignItems: 'center',
    justifyContent: 'center', ...en(38, '#fff', 900), transform: `scale(${p}) rotate(${(1 - p) * 90}deg)`, opacity: o, boxShadow: `0 0 40px ${S.red}`}}>VS</div>;
};
const Event: React.FC<{dur: number}> = ({dur}) => {
  const {f, fps, o} = useIn(dur);
  const a = (d: number) => spr(f, fps, d, 180, 14);
  return (
    <div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 10, opacity: o}}>
      <Img src={fluent('classical_building')} style={{width: 120, height: 120, transform: `scale(${a(0)})`}} />
      <div style={{...en(64, S.yellow, 900), letterSpacing: 2, opacity: a(3), transform: `translateY(${(1 - a(3)) * 20}px)`}}>UTH FESTIVAL 2026</div>
      <div style={{...ar(48), opacity: a(7)}}>في المتحف المصري الكبير</div>
      <div style={{...ar(36, S.soft, 700), opacity: a(11)}}>{bi('الجمعة والسبت · 20 – 21 نوفمبر 2026')}</div>
    </div>
  );
};
const Who: React.FC<{dur: number; pic: string}> = ({dur, pic}) => {
  const {f, fps, o} = useIn(dur);
  const a = (d: number) => spr(f, fps, d, 180, 14);
  return (<>
    <Photo file={pic} w={330} h={420} x={8} y={14} dur={dur} pos="30% 50%" z={1.3} />
    <div style={{position: 'absolute', left: 370, right: 10, top: 30, display: 'flex', flexDirection: 'column', gap: 12, opacity: o}}>
      <div style={{...ar(30, S.soft, 800), opacity: a(4)}}>مين اللي بيتكلم؟</div>
      <div style={{...en(62, S.yellow, 900), opacity: a(7), transform: `translateX(${(1 - a(7)) * 30}px)`}}>Garrett Warren</div>
      <div style={{...en(27, S.white, 700), opacity: a(11)}}>Stunt Coordinator & Second Unit Director</div>
      <div style={{...ar(34), opacity: a(15)}}>{bi('مسؤول الأكشن والستانتس في أفلام Avatar التلاتة')}</div>
      <div style={{...ar(30, S.soft, 800), opacity: a(19)}}>{bi('واترشح 5 مرات لجايزة SAG للستانتس')}</div>
    </div>
  </>);
};
const Person: React.FC<{dur: number; file: string; name: string; sub: string; note?: string}> = ({dur, file, name, sub, note}) => {
  const {f, fps, o} = useIn(dur);
  const a = (d: number) => spr(f, fps, d, 180, 14);
  return (<>
    <Photo file={file} w={320} h={400} x={80} y={22} dur={dur} pos="50% 20%" />
    <div style={{position: 'absolute', left: 440, right: 20, top: 110, display: 'flex', flexDirection: 'column', gap: 14, opacity: o}}>
      <div style={{...en(58, S.yellow, 900), opacity: a(4)}}>{name}</div>
      <div style={{...ar(40), opacity: a(8)}}>{bi(sub)}</div>
      {note ? <div style={{...ar(32, S.soft, 800), opacity: a(12)}}>{bi(note)}</div> : null}
    </div>
  </>);
};
const Term: React.FC<{dur: number; file?: string; term: string; full?: string; def: string; at?: number}> = ({dur, file, term, full, def, at = 0.4}) => {
  const {f, fps, o} = useIn(dur);
  const a = (d: number) => spr(f, fps, d, 180, 14);
  const da = sec(fps, at);
  const x0 = file ? 470 : 40;
  return (<>
    {file ? <Photo file={file} w={430} h={242} x={10} y={100} dur={dur} /> : null}
    <div style={{position: 'absolute', left: x0, right: 30, top: file ? 70 : 60, display: 'flex', flexDirection: 'column', alignItems: file ? 'flex-start' : 'center', gap: 12, opacity: o}}>
      <div style={{...en(file ? 50 : 76, S.ink, 900), background: S.yellow, borderRadius: 14, padding: '4px 20px', transform: `scale(${a(0)}) rotate(-2deg)`}}>{term}</div>
      {full ? <div style={{...en(36, S.white, 700), opacity: a(6)}}>= {full}</div> : null}
      <div style={{...ar(file ? 38 : 42), opacity: a(da), transform: `translateY(${(1 - a(da)) * 16}px)`, textAlign: file ? 'right' : 'center', alignSelf: 'stretch'}}>{bi(def)}</div>
    </div>
  </>);
};
const Count: React.FC<{dur: number; file: string; n: number; unit: string; at: number}> = ({dur, file, n, unit, at}) => {
  const {f, fps, o} = useIn(dur);
  const a0 = sec(fps, at) - 18;
  const v = Math.round(n * lin(f, a0, a0 + 18));
  const pop = spr(f, fps, a0 + 18, 260, 10);
  return (<>
    <Photo file={file} w={560} h={315} x={10} y={60} dur={dur} />
    <div style={{position: 'absolute', left: 590, right: 10, top: 80, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6, opacity: o}}>
      <Img src={fluent('video_camera')} style={{width: 110, height: 110, transform: `rotate(${Math.sin(f / 8) * 6}deg)`}} />
      <div style={{...en(120, S.yellow, 900), transform: `scale(${0.9 + 0.1 * pop})`}}>{v}</div>
      <div style={{...ar(46)}}>{unit}</div>
    </div>
  </>);
};
const Emo: React.FC<{dur: number; items: string[][]; title?: string; beats?: number[]}> = ({dur, items, title, beats}) => {
  const {f, fps, o} = useIn(dur);
  const n = items.length;
  return (
    <div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 18, opacity: o}}>
      <div style={{display: 'flex', gap: n > 2 ? 60 : 120, alignItems: 'flex-end'}}>
        {items.map(([e, t], i) => {
          const d = beats ? sec(fps, beats[i] ?? 0) : i * 5;
          const a = spr(f, fps, d, 200, 11);
          return (
            <div key={i} style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10, opacity: Math.min(1, a * 1.5), transform: `scale(${a}) translateY(${Math.sin((f + i * 20) / 14) * 6}px)`}}>
              <Img src={fluent(e)} style={{width: 200, height: 200, filter: 'drop-shadow(0 20px 26px rgba(0,0,0,0.5))'}} />
              {t ? <Pill text={t} bg={S.white} /> : null}
            </div>
          );
        })}
      </div>
      {title ? <div style={{...ar(50, S.yellow), opacity: spr(f, fps, 8, 180, 14)}}>{bi(title)}</div> : null}
    </div>
  );
};
const Crown: React.FC<{dur: number; face: string; pic: string; name: string; at: number}> = ({dur, face, pic, name, at}) => {
  const {f, fps, o} = useIn(dur);
  const ca = sec(fps, at);
  const drop = spr(f, fps, ca, 200, 12);
  const a = spr(f, fps, 2, 170, 14);
  return (<>
    <Photo file={pic} w={980} h={430} x={10} y={10} dur={dur} />
    <div style={{position: 'absolute', inset: 10, borderRadius: 22, background: 'linear-gradient(90deg, rgba(5,7,14,0.1), rgba(5,7,14,0.75))', opacity: o}} />
    <div style={{position: 'absolute', left: 600, top: 100, width: 300, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10, opacity: o, transform: `scale(${a})`}}>
      <Img src={fluent('crown')} style={{width: 120, height: 120, position: 'absolute', top: -90 - (1 - drop) * 220, opacity: drop, transform: `rotate(${-8 + Math.sin(f / 10) * 4}deg)`}} />
      <div style={{width: 200, height: 200, borderRadius: '50%', overflow: 'hidden', border: `6px solid ${S.yellow}`}}>
        <Img src={staticFile(face)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: '50% 18%'}} /></div>
      <Pill text={name} />
      <div style={{...ar(34, S.white, 800), opacity: drop}}>بيكسب أي خيال</div>
    </div>
  </>);
};
const Versions: React.FC<{dur: number; at: number; c1: number; c2: number; riffs: number; bad: number; dislike: number; face: string}> = ({dur, at, c1, c2, riffs, bad, dislike, face}) => {
  const {f, fps, o} = useIn(dur);
  const s = (x: number) => sec(fps, x);
  const cols = [0, 1, 2, 3, 4];
  const lab = ['اللي هو عايزها', 'اللي أنا عايزها', 'تنويعة', 'تنويعة', 'تنويعة'];
  const labAt = [c1, c2, riffs, riffs, riffs];
  return (
    <div style={{position: 'absolute', inset: 0, opacity: o}}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 6, textAlign: 'center', ...ar(40, S.yellow), opacity: spr(f, fps, s(at), 180, 14)}}>{bi('4 أو 5 نسخ من المشهد')}</div>
      {cols.map((i) => {
        const a = spr(f, fps, s(at) + i * 4, 200, 12);
        const la = spr(f, fps, s(labAt[i]), 200, 13);
        const x = 20 + i * 194;
        const isBad = i >= 2 && f >= s(bad) + (i - 2) * 4;
        const dis = i >= 2 && f >= s(dislike);
        return (
          <div key={i} style={{position: 'absolute', left: x, top: 80, width: 176, height: 300, opacity: Math.min(1, a * 1.4), transform: `translateY(${(1 - a) * 60}px) rotate(${(i - 2) * 2}deg)`}}>
            <div style={{position: 'absolute', inset: 0, borderRadius: 18, background: 'linear-gradient(160deg, #1B2140, #0D1124)', border: `3px solid ${i < 2 && la > 0.5 ? S.yellow : 'rgba(255,255,255,0.4)'}`,
              display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 6, filter: isBad ? 'grayscale(0.8) brightness(0.6)' : undefined}}>
              <Img src={fluent('clapper_board')} style={{width: 80, height: 80}} />
              <div style={{...en(30, S.white, 900)}}>V{i + 1}</div>
              {i === 0 ? <div style={{width: 86, height: 86, borderRadius: '50%', overflow: 'hidden', border: `3px solid ${S.yellow}`, opacity: la, transform: `scale(${la})`}}>
                <Img src={staticFile(face)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: '50% 18%'}} /></div> : null}
              {i === 1 ? <Img src={fluent('man_bald')} style={{width: 86, height: 86, opacity: la, transform: `scale(${la})`}} /> : null}
            </div>
            <div style={{position: 'absolute', left: -10, right: -10, top: 312, textAlign: 'center', opacity: la, ...ar(i < 2 ? 25 : 24, i < 2 ? S.yellow : S.soft, 800)}}>{lab[i]}</div>
            {isBad ? <div style={{position: 'absolute', left: 38, top: 60, width: 100, height: 100, borderRadius: '50%', background: S.red, display: 'flex', alignItems: 'center',
              justifyContent: 'center', ...en(66, '#fff', 900), transform: `scale(${spr(f, fps, s(bad) + (i - 2) * 4, 260, 10)})`}}>✕</div> : null}
            {dis ? <Img src={fluent('thumbs_down')} style={{position: 'absolute', left: 104, top: -36, width: 84, height: 84, transform: `scale(${spr(f, fps, s(dislike) + (i - 2) * 3, 240, 11)})`}} /> : null}
          </div>
        );
      })}
    </div>
  );
};
const Gear: React.FC<{dur: number; beats: number[]}> = ({dur, beats}) => {
  const {f, fps, o} = useIn(dur);
  const a = (i: number) => spr(f, fps, sec(fps, beats[i]), 200, 12);
  const box = (i: number, top: React.ReactNode, label: string) => (
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14, opacity: Math.min(1, a(i) * 1.5), transform: `scale(${a(i)})`}}>
      {top}<span style={{...en(40, S.ink, 900), background: S.white, borderRadius: 14, padding: '2px 18px'}}>{label}</span></div>
  );
  return (
    <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 120, opacity: o}}>
      {box(0, <div style={{position: 'relative', width: 220, height: 220}}><Img src={fluent('mobile_phone')} style={{width: 220, height: 220}} />
        <Img src={staticFile('logos/apple.svg')} style={{position: 'absolute', right: -10, top: -10, width: 70, height: 70, background: '#fff', borderRadius: 18, padding: 10}} /></div>, 'iPhone')}
      <div style={{...ar(46, S.soft), opacity: a(1)}}>أو</div>
      {box(1, <Img src={fluent('camera')} style={{width: 220, height: 220}} />, 'Canon R5')}
    </div>
  );
};
const Logo: React.FC<{dur: number; file: string; label: string; emo?: string}> = ({dur, file, label, emo}) => {
  const {f, fps, o} = useIn(dur);
  const a = spr(f, fps, 0, 190, 12), b = spr(f, fps, 8, 190, 12);
  return (
    <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 70, opacity: o}}>
      {emo ? <Img src={fluent(emo)} style={{width: 230, height: 230, transform: `scale(${a})`}} /> : null}
      <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16, transform: `scale(${b})`}}>
        <Img src={staticFile(file)} style={{width: 200, height: 200, objectFit: 'contain', filter: 'drop-shadow(0 16px 30px rgba(0,0,0,0.5))'}} />
        <span style={{...en(42, S.white, 900)}}>{label}</span>
      </div>
    </div>
  );
};
const Hire: React.FC<{dur: number; at: number}> = ({dur, at}) => {
  const {f, fps, o} = useIn(dur);
  const a = spr(f, fps, 0, 180, 14);
  const st = spr(f, fps, sec(fps, at), 260, 9);
  return (
    <div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 16, opacity: o}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 26, opacity: a}}>
        <Img src={fluent('movie_camera')} style={{width: 130, height: 130}} />
        <div style={{...ar(50)}}>{bi('صوّر pre-vis وورّيه للعالم')}</div>
      </div>
      <div style={{display: 'flex', alignItems: 'center', gap: 24, opacity: Math.min(1, st * 2), transform: `scale(${0.6 + 0.4 * st}) rotate(-3deg)`}}>
        <Img src={fluent('handshake')} style={{width: 150, height: 150}} />
        <div style={{...en(72, S.ink, 900), background: S.yellow, borderRadius: 18, padding: '4px 26px', boxShadow: `0 0 50px ${S.yellow}88`}}>I'LL HIRE YOU</div>
      </div>
    </div>
  );
};
const SCENES: Record<string, React.FC<any>> = {pic: Pic, vs: Vs, event: Event, who: Who, person: Person, term: Term, count: Count, emo: Emo, crown: Crown,
  versions: Versions, gear: Gear, logo: Logo, hire: Hire};

// ---------- English line (spoken word boxed) + Arabic translation ----------
const BiCaps: React.FC<{caps: Props['caps']}> = ({caps}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  const c = caps.find((x) => t >= x.t0 && t < x.t1);
  if (!c) return null;
  const k = Math.min(1, (t - c.t0) * 8, (c.t1 - t) * 8);
  const long = c.en.length > 9;
  return (
    <div style={{position: 'absolute', left: 50, right: 50, top: Y.cap, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6, opacity: k}}>
      <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '2px 10px', direction: 'ltr', maxWidth: 940}}>
        {c.en.map((w, i) => {
          const now = t >= w.s && t < (c.en[i + 1]?.s ?? c.t1);
          const said = t >= w.s;
          return <span key={i} style={{...en(long ? 38 : 44, now ? S.ink : said ? S.white : 'rgba(246,247,251,0.6)', 800), background: now ? S.yellow : undefined,
            borderRadius: 8, padding: '0 6px', textShadow: now ? undefined : '0 3px 12px rgba(0,0,0,0.9)'}}>{w.w}</span>;
        })}
      </div>
      <div style={{...ar(long ? 38 : 42, '#FFE7A3', 800), textAlign: 'center', textShadow: '0 3px 14px rgba(0,0,0,0.95)', maxWidth: 960}}>{bi(c.ar)}</div>
    </div>
  );
};

// ---------- header: event tag + the question ----------
const Header: React.FC<{tag: string; tagAr: string; head: string}> = ({tag, tagAr, head}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const words = groupLatin(head);
  return (
    <div style={{position: 'absolute', left: 40, right: 40, top: Y.tag, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10}}>
      <div style={{display: 'flex', gap: 14, alignItems: 'center', opacity: spr(f, fps, 2, 150, 15)}}>
        <span style={{...en(24, S.ink, 900), background: S.yellow, borderRadius: 10, padding: '3px 12px', letterSpacing: 2}}>{tag}</span>
        <span style={{...ar(26, S.white, 800)}}>{tagAr}</span>
      </div>
      <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '4px 14px', direction: 'rtl'}}>
        {words.map((w, i) => {
          const a = spr(f, fps, 4 + i * 2, 190, 14);
          const box = w.startsWith('*') && w.endsWith('*');
          const clean = bi(w.replace(/\*/g, ''));
          return <span key={i} style={{display: 'inline-block', ...ar(52,box ? S.ink : S.white), opacity: a, transform: `translateY(${(1 - a) * 20}px) ${box ? 'rotate(-2deg)' : ''}`,
            background: box ? S.yellow : undefined, borderRadius: 12, padding: box ? '0 16px 4px' : undefined, textShadow: box ? undefined : '0 6px 24px rgba(0,0,0,0.7)'}}>{clean}</span>;
        })}
      </div>
    </div>
  );
};

// ---------- footer: channel face + name + handles (Aly 2026-11-22) ----------
const Footer: React.FC = () => {
  const P = 'projects/uth/';
  const h = (icon: string, text: string) => (
    <span style={{display: 'flex', alignItems: 'center', gap: 6}}>
      <Img src={staticFile(`logos/${icon}.svg`)} style={{width: 26, height: 26}} />
      <span style={{...en(21, S.white, 700)}}>{text}</span></span>
  );
  return (
    <div style={{position: 'absolute', left: 30, right: 30, top: Y.foot, height: 92, borderRadius: 24, background: 'rgba(7,9,18,0.78)', border: '1px solid rgba(255,255,255,0.14)',
      display: 'flex', alignItems: 'center', gap: 14, padding: '0 18px'}}>
      <Img src={staticFile(P + 'ch_face.png')} style={{height: 70}} />
      <div style={{display: 'flex', flexDirection: 'column', gap: 6}}>
        <Img src={staticFile(P + 'ch_name.png')} style={{height: 32, alignSelf: 'flex-start'}} />
        <div style={{display: 'flex', gap: 16, alignItems: 'center', flexWrap: 'nowrap'}}>
          <span style={{display: 'flex', alignItems: 'center', gap: 6}}>
            {['youtube-icon', 'instagram', 'tiktok'].map((i) => <Img key={i} src={staticFile(`logos/${i}.svg`)} style={{width: 26, height: 26}} />)}
            <span style={{...en(21, S.white, 700)}}>@alyshorosh</span></span>
          {h('facebook', 'aly.shorosh')}
          {h('linkedin', 'in/shorosh')}
          <span style={{...en(21, S.white, 700)}}><b style={{color: '#4F7BFF'}}>Bē</b> shorosh</span>
        </div>
      </div>
    </div>
  );
};

export const UthReel: React.FC<Props> = ({duration, cam, voice, hookEnd, rewind, head, tag, tagAr, caps, cues, sfx, zoom}) => {
  const {fps} = useVideoConfig();
  const now = useCurrentFrame();
  const fr = (s: number) => Math.round(s * fps);
  const t = now / fps;
  const zz = interp(zoom, t);
  const near = (c: {t: number; d: number}) => Math.min(1, Math.max(0, Math.min((now - fr(c.t)) / 6 + 1, (fr(c.t + c.d) - now) / 6)));
  const trayOn = cues.reduce((m, c) => Math.max(m, near(c)), 0);
  const inRew = rewind && t >= rewind.t && t < rewind.t + rewind.d;
  return (
    <AbsoluteFill style={{background: S.night}}>
      <style>{fontCss}</style>
      {cam ? <AbsoluteFill style={{overflow: 'hidden'}}>
        <OffthreadVideo muted src={staticFile(cam)} style={{position: 'absolute', left: 0, top: 0, width: W, height: H, transform: `scale(${zz})`, transformOrigin: '56% 36%'}} />
      </AbsoluteFill> : null}
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(5,7,14,0.88) 0%, rgba(5,7,14,0.35) 15%, transparent 22%, transparent 52%, rgba(5,7,14,0.55) 60%, rgba(5,7,14,0.88) 72%, rgba(5,7,14,0.95) 100%)'}} />
      {/* tray over the stage floor */}
      <div style={{position: 'absolute', left: 30, right: 30, top: Y.tray - 14, height: Y.trayH + 26, borderRadius: 34, opacity: trayOn,
        background: 'linear-gradient(160deg, rgba(14,18,34,0.80), rgba(8,10,20,0.90))', border: '2px solid rgba(255,255,255,0.14)', boxShadow: `0 30px 60px rgba(0,0,0,0.5), 0 0 50px ${S.violet}33`}} />
      <div style={{position: 'absolute', left: 40, top: Y.tray, width: 1000, height: Y.trayH}}>
        {cues.map((c, i) => {
          if (now < fr(c.t) - 2 || now >= fr(c.t + c.d) + 2) return null;
          const C = SCENES[c.k];
          return C ? <Sequence key={i} from={fr(c.t)} durationInFrames={fr(c.d)} layout="none"><C dur={fr(c.d)} {...(c.p as any)} /></Sequence> : null;
        })}
      </div>
      {/* picture credits, once for the whole tray (film stills = official Avatar videos; portraits = Commons CC BY 2.0) */}
      <div style={{position: 'absolute', left: 0, right: 0, top: Y.tray + Y.trayH + 16, textAlign: 'center', opacity: trayOn * 0.75, ...en(15, S.soft, 600)}}>
        Avatar stills © 20th Century Studios (official featurette & trailer) · Portraits: Dick Thomas Johnson, CC BY 2.0</div>
      {rewind ? <Sequence from={fr(rewind.t)} durationInFrames={fr(rewind.d)} layout="none"><Rewind dur={fr(rewind.d)} from={rewind.from} to={rewind.to} /></Sequence> : null}
      {inRew ? null : <BiCaps caps={caps} />}
      <Header tag={tag} tagAr={tagAr} head={head} />
      <div style={{position: 'absolute', left: 0, top: 0, height: 8, width: W * now / Math.max(1, fr(duration)), background: `linear-gradient(90deg, ${S.blue}, ${S.violet}, ${S.red})`}} />
      <Footer />
      {voice ? <Audio src={staticFile(voice)} /> : null}
      {sfx.map((s, i) => <Sequence key={'x' + i} from={fr(s.t)} durationInFrames={fr(2.5)} layout="none"><Audio src={staticFile(s.file)} volume={s.vol} /></Sequence>)}
      {hookEnd > 0 && now < fr(hookEnd) ? null : null}
    </AbsoluteFill>
  );
};
