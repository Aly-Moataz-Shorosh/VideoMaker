import React from 'react';
import {Easing, useCurrentFrame, useVideoConfig} from 'remotion';
import {Col} from './anims';
import {AR, bi, CC, EN, G, lin, spr} from './kit';

// Concept animations of the audio course (left column, side mode). Each one draws exactly what Aly says at that moment;
// numbers only from his words or plain math (2^16), nothing from outside.
type P = {dur: number; [k: string]: any};
const W = 640, H = 600;
const sine = (x0: number, w: number, y: number, amp: number, cycles: number, ph = 0, n = 240) => {
  let d = '';
  for (let i = 0; i <= n; i++) {
    const u = i / n;
    d += `${i ? 'L' : 'M'}${(x0 + u * w).toFixed(1)},${(y - Math.sin(u * cycles * 2 * Math.PI + ph) * amp).toFixed(1)}`;
  }
  return d;
};
const Pill: React.FC<{text: string; c?: string; on?: boolean}> = ({text, c = G.gold, on = true}) => (
  <div style={{padding: '6px 18px', borderRadius: 22, fontFamily: AR, fontWeight: 900, fontSize: 26, direction: 'rtl',
    background: on ? c : 'rgba(255,255,255,0.1)', color: on ? '#14181F' : G.soft}}>{bi(text)}</div>
);
const Row: React.FC<{y: number; children: React.ReactNode}> = ({y, children}) => (
  <div style={{position: 'absolute', left: 0, right: 0, top: y, display: 'flex', justifyContent: 'center', gap: 14}}>{children}</div>
);

// ch5: a picture = numbers; black & white = 2D array, colour = 3 layers R, G, B.
const PixelNums: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const n = 6, c = 64, ox = 128, oy = 30;
  const stage = f < 5 * fps ? 0 : 1;
  const vals = (i: number, j: number) => Math.round(128 + 120 * Math.sin(i * 0.9 + j * 0.6));
  const cells = [];
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
    const v = vals(i, j), p = spr(f, fps, 6 + (i + j) * 2, 160, 18);
    cells.push(<div key={i + '-' + j} style={{position: 'absolute', left: ox + i * c, top: oy + j * c, width: c - 3, height: c - 3, borderRadius: 4,
      background: `rgb(${v},${v},${v})`, opacity: p, display: 'flex', alignItems: 'center', justifyContent: 'center',
      fontFamily: EN, fontWeight: 800, fontSize: 18, color: v > 128 ? '#14181F' : '#fff'}}>{lin(f, 40, 52) > 0.5 ? v : ''}</div>);
  }
  const L = [{c: '#FF5A5F', t: 'R'}, {c: '#35D07F', t: 'G'}, {c: '#3BA9F5', t: 'B'}];
  const q = spr(f, fps, 5 * fps, 120, 16);
  return (
    <Col dur={dur} title={stage ? 'صورة ألوان = 3 طبقات أرقام' : 'الصورة = أرقام.. كل بيكسل رقم'} note={stage ? 'الطبقات: أحمر، أخضر، أزرق' : 'أبيض وأسود = 2D array'}>
      {stage === 0 ? cells : L.map((l, k) => (
        <div key={l.t} style={{position: 'absolute', left: 150 + k * 50 * q, top: 60 + k * 50 * q, width: 300, height: 300, borderRadius: 10,
          background: `${l.c}55`, border: `3px solid ${l.c}`, display: 'flex', alignItems: 'flex-start', justifyContent: 'flex-start', padding: 10,
          fontFamily: EN, fontWeight: 900, fontSize: 40, color: l.c}}>{l.t}</div>
      ))}
    </Col>
  );
};

// ch6: sound = air molecules pushing each other -> a wave that travels to you.
const MolWave: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const dots = [];
  for (let i = 0; i < 26; i++) for (let j = 0; j < 7; j++) {
    const x0 = 60 + i * 21;
    const dx = 9 * Math.sin(i * 0.55 - t * 4) * lin(f, 15, 30);
    dots.push(<circle key={i + '-' + j} cx={x0 + dx} cy={60 + j * 30} r={6} fill={G.blue} opacity={0.85} />);
  }
  return (
    <Col dur={dur} title="الصوت = جزيئات الهوا بتزق بعض" note="مش حاجة بتمسكها.. زي الموجة في المية">
      <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        <rect x={14} y={70} width={30} height={170} rx={8} fill={G.gold} transform={`translate(${Math.sin(t * 4) * 6} 0)`} />
        {dots}
        <path d={sine(60, 540, 400, 60 * lin(f, 30, 50), 3, -t * 4)} stroke={G.gold} strokeWidth={6} fill="none" strokeLinecap="round" />
        <text x={W / 2} y={520} textAnchor="middle" fontFamily={AR} fontWeight={800} fontSize={28} fill={G.soft} opacity={lin(f, 40, 55)}>قريبين من بعض = فوق · بعاد = تحت</text>
      </svg>
    </Col>
  );
};

// ch6: how the computer records and plays it: wave -> diaphragm -> numbers -> speaker -> the same wave.
const MicChain: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const S = [{t: 'موجة', c: G.blue}, {t: 'الدايافرام بيتهز', c: G.gold}, {t: 'أرقام في الكمبيوتر', c: CC.teal}, {t: 'السماعة بتعمل نفس الموجة', c: '#35D07F'}];
  return (
    <Col dur={dur} title="المايك بيسجل.. والسماعة بترجّع نفس الموجة">
      {S.map((s, i) => {
        const p = spr(f, fps, 8 + i * 22, 150, 16);
        return (
          <div key={i} style={{position: 'absolute', left: 60, top: 10 + i * 140, width: 520, height: 104, borderRadius: 22, border: `3px solid ${s.c}`,
            background: `${s.c}1f`, opacity: Math.min(1, p * 1.4), transform: `translateX(${(1 - p) * -60}px)`, display: 'flex', alignItems: 'center',
            justifyContent: 'center', fontFamily: AR, fontWeight: 900, fontSize: 34, color: G.ink, direction: 'rtl'}}>{bi(s.t)}
            {i < 3 ? <div style={{position: 'absolute', bottom: -40, left: 248, fontSize: 30, color: G.soft, opacity: lin(f, 20 + i * 22, 30 + i * 22)}}>▼</div> : null}
          </div>
        );
      })}
    </Col>
  );
};

// ch7: Hz = how many full waves (cycles) happen in ONE second.
const HzAnim: React.FC<P> = ({dur, hz = [2, 5]}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const k = f < (dur / 2) ? 0 : 1, n = hz[k], kf = f - k * dur / 2;
  const reveal = lin(kf, 6, 2.4 * fps);
  const counted = Math.min(n, Math.floor(reveal * n + 0.001));
  return (
    <Col dur={dur} title="Hz = كام موجة كاملة في الثانية" note="موجة كاملة = cycle: فوق وتحت">
      <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        <defs><clipPath id="hzc"><rect x={50} y={0} width={540 * reveal} height={400} /></clipPath></defs>
        <line x1={50} y1={200} x2={590} y2={200} stroke="rgba(255,255,255,0.2)" strokeWidth={2} />
        <path d={sine(50, 540, 200, 120, n)} stroke={G.gold} strokeWidth={7} fill="none" clipPath="url(#hzc)" strokeLinecap="round" />
        <line x1={50} y1={360} x2={590} y2={360} stroke={G.soft} strokeWidth={3} />
        <line x1={50} y1={345} x2={50} y2={375} stroke={G.soft} strokeWidth={3} /><line x1={590} y1={345} x2={590} y2={375} stroke={G.soft} strokeWidth={3} />
        <text x={320} y={405} textAnchor="middle" fontFamily={AR} fontWeight={800} fontSize={28} fill={G.soft}>ثانية واحدة</text>
        <text x={320} y={520} textAnchor="middle" fontFamily={EN} fontWeight={900} fontSize={84} fill="#fff">{counted} Hz</text>
      </svg>
    </Col>
  );
};

// ch8: sample rate = how many snapshots of the wave per second (like frames of a video); min. 2 per wave (top + bottom).
const SampleAnim: React.FC<P> = ({dur, mode = 'rate'}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const rates = mode === 'min' ? [2] : [8, 32];
  const k = mode === 'min' ? 0 : f < dur / 2 ? 0 : 1, n = rates[k];
  const cyc = mode === 'min' ? 3 : 2, total = n * cyc;
  const kf = f - (mode === 'min' ? 0 : k * dur / 2);
  const bars = [];
  for (let i = 0; i < total; i++) {
    const u = (i + (mode === 'min' ? 0.25 : 0.5)) / total, x = 50 + u * 540, y = 230 - Math.sin(u * cyc * 2 * Math.PI) * 140;
    const p = lin(kf, 10 + i * (40 / total), 14 + i * (40 / total));
    bars.push(<g key={i} opacity={p}><line x1={x} y1={230} x2={x} y2={y} stroke={G.blue} strokeWidth={mode === 'min' ? 10 : n > 16 ? 7 : 12} strokeLinecap="round" />
      <circle cx={x} cy={y} r={8} fill="#fff" /></g>);
  }
  return (
    <Col dur={dur} title={mode === 'min' ? 'أقل حاجة: لقطتين لكل موجة' : 'Sample rate = عدد اللقطات من الموجة في الثانية'}
      note={mode === 'min' ? 'واحدة فوق.. وواحدة تحت' : 'زي الـ frame rate في الفيديو: لقطات أكتر = دقة أكتر'}>
      <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        <path d={sine(50, 540, 230, 140, cyc)} stroke="rgba(255,255,255,0.35)" strokeWidth={4} fill="none" strokeDasharray="10 8" />
        <line x1={50} y1={230} x2={590} y2={230} stroke="rgba(255,255,255,0.15)" strokeWidth={2} />
        {bars}
      </svg>
      {mode === 'min' ? null : <Row y={430}>{rates.map((r, i) => <Pill key={r} text={`${r} لقطة`} on={i === k} c={G.blue} />)}</Row>}
    </Col>
  );
};

// ch9: bit depth = how many steps ONE sample can choose from (like the colours of one pixel). 2^bits.
const BitAnim: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const B = [1, 2, 4];
  const k = Math.min(2, Math.floor(f / (dur / 3)));
  const bits = B[k], steps = 2 ** bits;
  const v = 0.72, lvl = Math.round(v * (steps - 1)) / (steps - 1);
  const Hh = 380;
  return (
    <Col dur={dur} title="Bit depth = كام درجة ممكن تختار منها لكل لقطة" note="16 bit = 65,536 درجة · 24 bit = 16,777,216 درجة">
      <div style={{position: 'absolute', left: 150, top: 20, width: 120, height: Hh, borderRadius: 12, border: '3px solid rgba(255,255,255,0.3)', overflow: 'hidden'}}>
        {Array.from({length: steps}).map((_, i) => (
          <div key={i} style={{position: 'absolute', left: 0, right: 0, bottom: (i * Hh) / steps, height: Hh / steps, borderTop: '2px solid rgba(255,255,255,0.18)',
            background: i / (steps - 1 || 1) <= lvl + 1e-6 ? `${G.gold}cc` : 'transparent'}} />
        ))}
      </div>
      <div style={{position: 'absolute', left: 310, top: 20 + Hh * (1 - v) - 2, width: 200, borderTop: `3px dashed ${G.blue}`}} />
      <div style={{position: 'absolute', left: 320, top: 20 + Hh * (1 - v) - 44, fontFamily: AR, fontWeight: 800, fontSize: 24, color: G.blue, direction: 'rtl'}}>الصوت الحقيقي</div>
      <div style={{position: 'absolute', left: 320, top: 190, fontFamily: EN, fontWeight: 900, fontSize: 64, color: '#fff'}}>{steps}</div>
      <div style={{position: 'absolute', left: 320, top: 270, fontFamily: AR, fontWeight: 800, fontSize: 28, color: G.soft, direction: 'rtl'}}>درجة</div>
      <Row y={440}>{B.map((b, i) => <Pill key={b} text={`${b} bit`} on={i === k} />)}</Row>
    </Col>
  );
};

// ch10: the three mic technologies as HE describes them (strength / sensitivity / price), no outside specs.
const MicTypes: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const M = [
    {n: 'Dynamic', c: G.gold, rows: ['قوي يستحمل الخبط', 'حساسيته ضعيفة', 'رخيص']},
    {n: 'Condenser', c: G.blue, rows: ['حساس جدا', 'صوت نقي قوي', 'الأنسب لأغلب التصوير']},
    {n: 'Ribbon', c: CC.coral, rows: ['غالي جدا', 'غالبا مش هتلاقيه']},
  ];
  return (
    <Col dur={dur} title="3 أنواع أساسية للمايكات">
      {M.map((m, i) => {
        const p = spr(f, fps, 8 + i * 26, 140, 16);
        return (
          <div key={m.n} style={{position: 'absolute', left: 20, top: i * 205, width: 600, height: 192, borderRadius: 24, border: `3px solid ${m.c}`, background: `${m.c}16`,
            opacity: Math.min(1, p * 1.4), transform: `translateX(${(1 - p) * -60}px)`, padding: '14px 24px', boxSizing: 'border-box', direction: 'rtl'}}>
            <div style={{fontFamily: EN, fontWeight: 900, fontSize: 34, color: m.c, direction: 'ltr', textAlign: 'right'}}>{m.n}</div>
            <div style={{display: 'flex', flexWrap: 'wrap', gap: 8, marginTop: 6}}>
              {m.rows.map((r) => <span key={r} style={{padding: '3px 12px', borderRadius: 14, background: 'rgba(255,255,255,0.08)', fontFamily: AR, fontWeight: 800, fontSize: 22, color: G.ink}}>{bi(r)}</span>)}
            </div>
          </div>
        );
      })}
    </Col>
  );
};

// ch11: polar patterns from the top: where the mic hears from (omni / cardioid / shotgun).
const PolarAnim: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const K = [
    {n: 'Omni', ar: 'من كل الاتجاهات', r: (a: number) => 1},
    {n: 'Cardioid', ar: 'من قدام وشوية من الجناب.. مش من ورا', r: (a: number) => 0.5 + 0.5 * Math.cos(a)},
    {n: 'Shotgun', ar: 'من قدام بس.. ولمسافة أبعد', r: (a: number) => Math.max(0.04, Math.cos(a)) ** 6},
  ];
  const k = Math.min(2, Math.floor(f / (dur / 3)));
  const kf = f - k * dur / 3, g = lin(kf, 0, 16, 0, 1, Easing.out(Easing.cubic));
  const cx = 320, cy = 260, R = 190;
  let d = '';
  for (let i = 0; i <= 180; i++) {
    const a = (i / 180) * 2 * Math.PI, r = R * K[k].r(a) * g;
    d += `${i ? 'L' : 'M'}${(cx + Math.sin(a) * r).toFixed(1)},${(cy - Math.cos(a) * r).toFixed(1)}`;
  }
  return (
    <Col dur={dur} title={`${K[k].n}: ${K[k].ar}`} note="شكل المكان اللي المايك بيسمع منه = Polar pattern">
      <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        {[1, 0.66, 0.33].map((s) => <circle key={s} cx={cx} cy={cy} r={R * s} fill="none" stroke="rgba(255,255,255,0.12)" strokeWidth={2} />)}
        <path d={d + 'Z'} fill={`${G.gold}33`} stroke={G.gold} strokeWidth={5} />
        <rect x={cx - 14} y={cy - 30} width={28} height={60} rx={12} fill="#fff" />
        <text x={cx} y={cy - R - 24} textAnchor="middle" fontFamily={AR} fontWeight={800} fontSize={26} fill={G.soft}>قدام ▲</text>
      </svg>
      <Row y={510}>{K.map((x, i) => <Pill key={x.n} text={x.n} on={i === k} />)}</Row>
    </Col>
  );
};

// ch15: the four kinds of sound in a video, with HIS examples.
const FourSounds: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const S = [
    {n: 'Dialogue', ar: 'الحوار: كلام اللي بيتكلم', c: G.gold},
    {n: 'Ambience', ar: 'الصوت المحيط: عصافير، شجر', c: '#35D07F'},
    {n: 'Music', ar: 'الموسيقى التصويرية', c: G.blue},
    {n: 'SFX', ar: 'المؤثرات: خبطة، زرار كيبورد', c: CC.coral},
  ];
  return (
    <Col dur={dur} title="4 أنواع صوت في أي فيديو">
      {S.map((s, i) => {
        const p = spr(f, fps, 8 + i * 16, 150, 16);
        return (
          <div key={s.n} style={{position: 'absolute', left: (i % 2) * 320, top: Math.floor(i / 2) * 290, width: 300, height: 270, borderRadius: 26,
            border: `3px solid ${s.c}`, background: `${s.c}18`, opacity: Math.min(1, p * 1.4), transform: `scale(${0.85 + 0.15 * p})`,
            display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 14, padding: 16, boxSizing: 'border-box'}}>
            <div style={{fontFamily: EN, fontWeight: 900, fontSize: 40, color: s.c}}>{s.n}</div>
            <div style={{fontFamily: AR, fontWeight: 800, fontSize: 26, color: G.ink, textAlign: 'center', direction: 'rtl', lineHeight: 1.4}}>{bi(s.ar)}</div>
          </div>
        );
      })}
    </Col>
  );
};

// ch19 / Premiere: sync = the camera's sound and the mic's sound line up on the clap.
const SyncAnim: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const off = 120 * (1 - lin(f, 50, 90, 0, 1, Easing.inOut(Easing.cubic)));
  const tr = (y: number, x: number, c: string, label: string) => {
    let d = '';
    for (let i = 0; i <= 200; i++) {
      const u = i / 200, X = 40 + u * 560, peak = Math.exp(-(((u - 0.45) * 40) ** 2)) * 70;
      const a = peak + 10 * Math.abs(Math.sin(i * 1.7) * Math.sin(i * 0.31));
      d += `M${(X + x).toFixed(1)},${y - a}L${(X + x).toFixed(1)},${y + a}`;
    }
    return <g><text x={600} y={y - 90} textAnchor="end" fontFamily={AR} fontWeight={800} fontSize={26} fill={G.soft}>{label}</text><path d={d} stroke={c} strokeWidth={2} /></g>;
  };
  const ok = lin(f, 90, 100);
  return (
    <Col dur={dur} title="Sync = الصوت ماشي مع الصورة بالظبط" note="التسقيفة بتعمل موجة عالية في الاتنين.. نحطهم فوق بعض">
      <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        {tr(150, 0, G.blue, 'صوت الكاميرا')}
        {tr(390, off, G.gold, 'صوت المايك')}
        <line x1={40 + 0.45 * 560} y1={40} x2={40 + 0.45 * 560} y2={500} stroke="#35D07F" strokeWidth={4} strokeDasharray="10 8" opacity={ok} />
      </svg>
    </Col>
  );
};

// ch28: noise reduction in Audition: select a quiet part -> Capture Noise Print -> remove it from the whole file.
const NoisePrint: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const sel = lin(f, 15, 30), clean = lin(f, 3.2 * fps, 4.4 * fps);
  let d = '';
  for (let i = 0; i <= 260; i++) {
    const u = i / 260, X = 30 + u * 580;
    const voice = (u > 0.3 && u < 0.55) || u > 0.7 ? 60 * Math.abs(Math.sin(i * 0.7) * Math.sin(i * 0.13)) + 15 : 0;
    const noise = 14 * (1 - clean) * (0.6 + 0.4 * Math.abs(Math.sin(i * 2.3)));
    const a = voice + noise;
    d += `M${X.toFixed(1)},${200 - a}L${X.toFixed(1)},${200 + a}`;
  }
  const steps = ['علّم على حتة دوشة بس', 'Capture Noise Print', 'Noise Reduction على الملف كله'];
  const st = f < 1.6 * fps ? 0 : f < 3.2 * fps ? 1 : 2;
  return (
    <Col dur={dur} title="تشيل الدوشة: البرنامج بيحفظ بصمتها" note="بصمة الدوشة = noise print">
      <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        <rect x={30} y={90} width={0.27 * 580 * sel} height={220} fill={`${G.gold}2a`} stroke={G.gold} strokeWidth={st === 0 ? 3 : 0} opacity={1 - clean} />
        <path d={d} stroke={clean > 0.5 ? '#35D07F' : G.blue} strokeWidth={2} />
      </svg>
      <div style={{position: 'absolute', left: 0, right: 0, top: 360, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12}}>
        {steps.map((s, i) => <Pill key={s} text={`${i + 1}. ${s}`} on={i === st} c={i === 2 ? '#35D07F' : G.gold} />)}
      </div>
    </Col>
  );
};

// ch30: stereo = two channels (left + right speaker), mono = one.
const StereoAnim: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const k = f < dur / 2 ? 0 : 1;
  const spk = (x: number, on: boolean) => (
    <g opacity={on ? 1 : 0.25}>
      <rect x={x - 50} y={150} width={100} height={150} rx={18} fill="#1C2433" stroke={on ? G.gold : G.dim} strokeWidth={4} />
      <circle cx={x} cy={240} r={32} fill="none" stroke={on ? G.gold : G.dim} strokeWidth={5} />
      {on ? [0, 1, 2].map((i) => <circle key={i} cx={x} cy={240} r={50 + ((t * 60 + i * 30) % 90)} fill="none" stroke={G.gold} strokeWidth={3} opacity={1 - ((t * 60 + i * 30) % 90) / 90} />) : null}
    </g>
  );
  return (
    <Col dur={dur} title={k ? 'Mono = قناة واحدة.. سماعة واحدة' : 'Stereo = قناتين: يمين وشمال'}>
      <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>{spk(150, true)}{spk(490, k === 0)}</svg>
      <Row y={430}><Pill text="Stereo" on={k === 0} /><Pill text="Mono" on={k === 1} /></Row>
    </Col>
  );
};

// ch31 (Q&A): why podcasters wear headphones: mic -> recorder / laptop -> headphones = he hears himself while recording.
const HeadMonitor: React.FC<P> = ({dur}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const S = [{t: 'المايك', c: G.gold}, {t: 'مسجل الصوت أو اللابتوب', c: G.blue}, {t: 'السماعة على ودنه', c: '#35D07F'}];
  return (
    <Col dur={dur} title="ليه السماعة في البودكاست؟" note="بيسمع صوته وهو بيسجل.. يعرف صوته واضح ولا لأ">
      {S.map((s, i) => {
        const p = spr(f, fps, 8 + i * 22, 150, 16);
        return (
          <div key={i} style={{position: 'absolute', left: 70, top: 20 + i * 165, width: 500, height: 110, borderRadius: 24, border: `3px solid ${s.c}`, background: `${s.c}1c`,
            opacity: Math.min(1, p * 1.4), display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: AR, fontWeight: 900, fontSize: 34, color: G.ink, direction: 'rtl'}}>
            {s.t}
            {i < 2 ? <div style={{position: 'absolute', bottom: -48, left: 236, fontSize: 32, color: G.soft, opacity: lin(f, 20 + i * 22, 30 + i * 22)}}>▼</div> : null}
          </div>
        );
      })}
    </Col>
  );
};

export const audioAnims: Record<string, React.FC<P>> = {PixelNums, MolWave, MicChain, HzAnim, SampleAnim, BitAnim, MicTypes, PolarAnim, FourSounds, SyncAnim, NoisePrint, StereoAnim, HeadMonitor};
