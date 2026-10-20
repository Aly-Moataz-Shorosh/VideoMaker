import React from 'react';
import {Easing, Img, staticFile, useCurrentFrame} from 'remotion';
import {useBeats} from '../film/kit';
import {AR, AuLogo, Chip, EN, G, GScene, Glass, In, Label, Mark, Pill, SKey, SMark, Screen, Sound, Top, Type, lin, spr} from './kit';

// Adobe Audition short (2026-10-15, style 10 glass-face): his face always on screen (talking head at the start, then the
// webcam corner of his screen recording), his REAL Audition recording big on the stage with a gold box on every click.
// Props from make_short.py: b = beats (s from scene start), cam = cam.mp4 path, camAt = timeline frame of the scene start,
// keys/marks = screen crop keys + click boxes (frames from scene start), env = voice bars for the sound cards.
type B = {b?: Record<string, number>; cam?: string; camAt?: number; keys?: SKey[]; marks?: SMark[]; env?: number[]; env2?: number[]};
const VIOLET = '#9999FF';

// the five effects = the backbone (a checklist that fills up chapter by chapter)
const FX = ['Noise Reduction', 'Normalize', 'Vocal Enhancer', 'Mastering', 'Parametric EQ'];
const Chain: React.FC<{done: number; cur?: number; y?: number}> = ({done, cur, y = 1180}) => (
  <div style={{position: 'absolute', top: y, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 10, direction: 'ltr'}}>
    {FX.map((n, i) => (
      <div key={n} style={{width: 18 + (i === cur ? 26 : 0), height: 18, borderRadius: 9, background: i < done ? G.gold : i === cur ? G.blue : 'rgba(255,255,255,0.22)',
        boxShadow: i === cur ? `0 0 16px ${G.blue}` : undefined}} />
    ))}
  </div>
);

const Stage: React.FC<{p: B; y?: number; w?: number; h?: number}> = ({p, y = 600, w = 1020, h = 880}) =>
  p.cam && p.keys ? (
    <In at={4} x={540} y={y}><Screen file={p.cam} startFrom={p.camAt ?? 0} keys={p.keys} marks={p.marks} w={w} h={h} /></In>
  ) : null;

// ---------- 0. hook: sound = 50% of the video; bad sound = nobody finishes it, even in HD ----------
export const AuHook: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const half = at('half', 3.5), audio = at('audio', 6), bad = at('bad', 9.5), hd = at('hd', 13);
  const fill = lin(f, half, half + 18, 0, 1, Easing.out(Easing.cubic));
  return (
    <GScene>
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 760, background: 'linear-gradient(180deg, rgba(5,8,14,0.9) 55%, transparent)', opacity: f < bad ? lin(f, 0, 10) : 1}} />
      {f < bad ? (
        <>
          <Top text="الصوت = *نص* الفيديو" at={2} y={110} size={84} out={bad - 8} />
          <In at={half} out={bad - 8} x={540} y={420}>
            <Glass w={900} h={190} pad={22} r={40}>
              <div style={{display: 'flex', height: '100%', gap: 12, direction: 'rtl'}}>
                <div style={{flex: 1, borderRadius: 26, background: `rgba(59,169,245,${0.25 + 0.55 * fill})`, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 14}}>
                  <span style={{fontSize: 60}}>🎥</span><Label text="الصورة 50%" size={44} />
                </div>
                <div style={{flex: f >= audio ? 1 : 0.0001, transition: 'none', borderRadius: 26, background: G.gold, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 14, overflow: 'hidden',
                  transform: `scaleX(${f >= audio ? spr(f, 30, audio, 160, 16) : 0})`, transformOrigin: 'left'}}>
                  <span style={{fontSize: 60}}>🎧</span><Label text="الصوت 50%" size={44} color="#14181F" />
                </div>
              </div>
            </Glass>
          </In>
        </>
      ) : (
        <>
          <Top text="صوت *وحش* = مش هتكمل" at={bad} y={110} size={80} />
          <In at={bad + 6} x={300} y={420}><Pill text="🤯 صداع" color={G.red} ink="#fff" size={56} /></In>
          <In at={bad + 12} x={760} y={420}><Mark ok={false} s={1.5} /></In>
          <In at={hd} x={540} y={600}><Pill text="حتى لو HD 📺" color="rgba(255,255,255,0.92)" size={54} /></In>
        </>
      )}
    </GScene>
  );
};

// ---------- 1. the tool + the worst mic on purpose (laptop mic) ----------
export const AuTool: React.FC<B> = ({b}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const au = at('au', 1), lap = at('lap', 4.5), all = at('all', 9);
  return (
    <GScene>
      {f < lap ? (
        <>
          <In at={au} x={540} y={300}><AuLogo s={1.3} /></In>
          <In at={au + 10} x={540} y={560}><Pill text="Adobe Audition" font={EN} dir="ltr" color={VIOLET} ink="#00005B" size={62} /></In>
        </>
      ) : (
        <>
          <Top text="هسجّل بـ *مايك_اللابتوب*" at={lap} y={110} size={74} />
          <In at={lap + 8} x={540} y={420}>
            <svg width={420} height={260} viewBox="0 0 420 260">
              <rect x={70} y={20} width={280} height={180} rx={16} fill="rgba(255,255,255,0.12)" stroke="#fff" strokeWidth={6} />
              <rect x={20} y={200} width={380} height={30} rx={12} fill="#fff" />
              <circle cx={210} cy={36} r={8} fill={G.red} style={{filter: `drop-shadow(0 0 10px ${G.red})`}} />
              <text x={210} y={130} textAnchor="middle" fontSize={70}>🎙️</text>
            </svg>
          </In>
          <In at={all} x={540} y={640}><Pill text="عشان أي حد يقدر يعملها ✅" color={G.blue} ink="#fff" size={48} /></In>
        </>
      )}
    </GScene>
  );
};

// ---------- 2. File > New > Audio File (real screen) ----------
export const AuNew: React.FC<B> = (p) => (
  <GScene>
    <Chip n="00" en="New Audio File" ar="ملف جديد" color={VIOLET} at={2} y={60} />
    <Stage p={p} />
  </GScene>
);

// ---------- 3 / 6 / 10. sound check (real voice bars) ----------
export const AuCheck: React.FC<B & {label?: string; noise?: number; color?: string; title?: string; label2?: string}> = ({b, env = [], env2, label = 'قبل', noise = 0.3, color = G.red, title = 'اسمع *قبل*', label2 = 'بعد'}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const ok = at('ok', 99);
  return (
    <GScene>
      <Top text={title} at={2} y={90} size={74} />
      <In at={6} x={540} y={env2 ? 360 : 470}><Sound env={env} noise={noise} label={label} color={color} at={8} h={env2 ? 200 : 300} /></In>
      {env2 ? <In at={at('two', 3)} x={540} y={700}><Sound env={env2} noise={0} label={label2} color={G.gold} at={at('two', 3) + 4} h={200} /></In> : null}
      {f >= ok ? <In at={ok} x={540} y={env2 ? 930 : 800}><Pill text="مفيش نقطة Noise واحدة ✓" color={G.green} ink="#fff" size={50} /></In> : null}
    </GScene>
  );
};

// ---------- 4. Noise Reduction (5 steps on the real screen) ----------
const Steps: React.FC<{items: string[]; ats: number[]; y?: number}> = ({items, ats, y = 1110}) => {
  const f = useCurrentFrame();
  let cur = 0;
  ats.forEach((t, i) => { if (f >= t) cur = i; });
  return (
    <In at={ats[0]} x={540} y={y}>
      <div style={{display: 'flex', alignItems: 'center', gap: 16, direction: 'rtl'}}>
        <div style={{width: 64, height: 64, borderRadius: '50%', background: G.gold, color: '#14181F', fontFamily: EN, fontWeight: 900, fontSize: 34,
          display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${spr(f, 30, ats[cur], 220, 12)})`}}>{cur + 1}</div>
        <span key={cur} style={{fontFamily: AR, fontWeight: 800, fontSize: 46, color: G.ink, opacity: lin(f, ats[cur], ats[cur] + 8), textShadow: '0 4px 20px rgba(0,0,0,0.6)'}}>{items[cur]}</span>
      </div>
    </In>
  );
};

export const AuStep: React.FC<B & {n: string; en: string; ar: string; steps?: string[]; done?: number; tip?: string}> = (p) => {
  const at = useBeats(p.b);
  const steps = p.steps ?? [];
  // (v2) tip pill sits on the screen card
  const ats = steps.map((_, i) => at('s' + (i + 1), 1 + i * 3));
  const f = useCurrentFrame();
  return (
    <GScene>
      <Chip n={p.n} en={p.en} ar={p.ar} color={G.gold} at={2} y={40} />
      <Stage p={p} />
      {steps.length ? <Steps items={steps} ats={ats} /> : null}
      {p.tip && f >= at('tip', 99) ? <In at={at('tip', 99)} x={540} y={600}><Pill text={p.tip} color={G.green} ink="#fff" size={54} /></In> : null}
      <Chain done={p.done ?? 0} cur={p.done} />
    </GScene>
  );
};

// ---------- 11. end: the 5 effects as one chain ----------
export const AuEnd: React.FC<B & {qr?: string}> = ({b, qr}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  return (
    <GScene>
      <Top text="الـ *5* إفكتات اللي بستخدمها" at={2} y={70} size={66} />
      <div style={{position: 'absolute', top: 190, left: 30, width: 640, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14}}>
        {FX.map((n, i) => {
          const t = 8 + i * 6;
          if (f < t) return null;
          const p = spr(f, 30, t, 160, 16);
          return (
            <div key={n} style={{opacity: Math.min(1, p * 1.4), transform: `translateX(${(1 - p) * 80}px)`}}>
              <Glass w={620} pad={16} r={30}>
                <div style={{display: 'flex', alignItems: 'center', gap: 22, direction: 'ltr'}}>
                  <div style={{width: 52, height: 52, borderRadius: '50%', background: G.gold, color: '#14181F', fontFamily: EN, fontWeight: 900, fontSize: 28, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{i + 1}</div>
                  <span style={{fontFamily: EN, fontWeight: 800, fontSize: 42, color: G.ink}}>{n}</span>
                </div>
              </Glass>
            </div>
          );
        })}
      </div>
      {f >= at('fast', 3) ? <In at={at('fast', 3)} x={540} y={935}><Pill text="⚡ لما أكون مستعجل" size={46} /></In> : null}
      {qr ? (
        <In at={14} x={870} y={450}>
          <div style={{background: '#fff', borderRadius: 30, padding: 18, border: `6px solid ${G.gold}`, boxShadow: `0 0 50px ${G.gold}66`, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8}}>
            <Img src={staticFile(qr)} style={{width: 270, height: 270, display: 'block'}} />
            <div style={{fontFamily: AR, fontWeight: 900, fontSize: 34, color: '#14181F'}}>الفيديو كامل 📲</div>
          </div>
        </In>
      ) : null}
    </GScene>
  );
};

export const AuHook2: React.FC<B> = ({b, env = [], env2 = []}) => {
  const f = useCurrentFrame();
  const at = useBeats(b);
  const two = at('two', 3), how = at('how', 6);
  const shake = f < two ? Math.sin(f * 1.3) * 3 : 0;
  return (
    <GScene>
      <Top text={f < two ? 'من *ده* 👎' : 'لـ *ده* 👍'} at={f < two ? 2 : two} y={190} size={96} />
      <In at={4} out={two - 6} x={540 + shake} y={480}><Sound env={env} noise={0.32} label="قبل" color={G.red} at={6} h={170} /></In>
      <In at={two} x={540} y={480}><Sound env={env2} noise={0} label="بعد" color={G.gold} at={two + 2} h={170} /></In>
      {f >= how ? <In at={how} x={540} y={1420}><Pill text="بـ 5 خطوات بس 🎧" color={G.blue} ink="#fff" size={60} /></In> : null}
    </GScene>
  );
};

export const auditionScenes: Record<string, React.FC<any>> = {
  au_hook: AuHook, au_hook2: AuHook2, au_tool: AuTool, au_new: AuNew, au_check: AuCheck, au_step: AuStep, au_end: AuEnd,
};
