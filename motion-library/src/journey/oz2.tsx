import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, Bubble, BrickRoad, CornField, Dorothy, EmeraldCity, EN, grad, In, JY, lin, logo, OzBadge, Pill, Sc, Scarecrow, spr} from './kit';
import {Lion, Princess, TinMan, Townie, Wizard} from './cast';
import {Field, Land} from './oz';
import {BouncingBall3D, Building3D, Cloner3D, Principles3D, Room3D} from './three';

// Oz chapters 1, 3, 4, 5 (shorts 32, 34, 35, 36, 37–40) — same approved recipe as chapter 2: drawn story + his circle +
// his WHOLE frame for the examples (Field) with the field's own motion under it. b = beats (scene frames).
const C = JY.oz;
type B = Record<string, number>;
const at = (b: B, k: string, d = 0) => b[k] ?? d;
const Sky: React.FC<{dark?: boolean}> = ({dark}) => (
  <AbsoluteFill style={{background: dark ? 'linear-gradient(180deg, #1F3A2A 0%, #2E5A3A 60%, #1E3A24 100%)' : 'linear-gradient(180deg, #CDEBF5 0%, #F4F1E4 60%, #F1E6C8 100%)'}} />
);
const Card: React.FC<{children: React.ReactNode; w?: number}> = ({children, w}) => (
  <div style={{background: C.card, borderRadius: 30, padding: '18px 34px', textAlign: 'center', boxShadow: '0 14px 30px rgba(0,0,0,0.2)', width: w, direction: 'rtl'}}>{children}</div>
);
const T: React.FC<{t: string; size?: number; color?: string}> = ({t, size = 48, color = C.ink}) => (
  <div style={{fontFamily: AR, fontWeight: 900, fontSize: size, color, lineHeight: 1.3, direction: 'rtl'}}>{t}</div>
);

// ---------------- chapter 1 ----------------
// a storybook opens: "an old story.. a girl called Dorothy.. a far place called Oz"
export const C1Book: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const open = lin(f, 4, 26);
  const d = at(b, 'dorothy', 60), oz = at(b, 'oz', 140);
  return (
    <Sc>
      <Sky />
      <div style={{position: 'absolute', left: 140, top: 520, width: 800, height: 620, perspective: 1600}}>
        <div style={{position: 'absolute', inset: 0, background: '#7A4A2A', borderRadius: 18, boxShadow: '0 30px 60px rgba(0,0,0,0.3)'}} />
        <div style={{position: 'absolute', left: 20, top: 20, right: 20, bottom: 20, background: '#FFF6DF', borderRadius: 10}} />
        <div style={{position: 'absolute', left: 20, top: 20, width: 380, bottom: 20, background: '#9A5B33', borderRadius: 10, transformOrigin: '100% 50%',
          transform: `rotateY(${-170 * open}deg)`, backfaceVisibility: 'hidden', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          <div style={{fontFamily: AR, fontWeight: 900, fontSize: 52, color: '#F2C230', textAlign: 'center', lineHeight: 1.4}}>حكاية<br />قديمة</div>
        </div>
      </div>
      {f > d ? <Dorothy x={330} y={980} s={1.0} look={0.5} /> : null}
      <In at={d} x={330} y={640}><Pill text="دورثي" bg={C.a} ink="#fff" size={44} /></In>
      <In at={oz} x={750} y={720}><EmeraldCityMini /><div style={{marginTop: 8}}><Pill text="مكان بعيد: أوز" size={38} /></div></In>
      <In at={0} x={540} y={400}><Card><T t="قصتك بتفكرني بقصة قديمة 📖" /></Card></In>
    </Sc>
  );
};
const EmeraldCityMini: React.FC = () => (
  <svg width={260} height={200} viewBox="-130 -190 260 200">
    {[[-80, 70, 16], [-45, 120, 20], [-10, 160, 24], [28, 130, 22], [62, 95, 18], [92, 60, 14]].map(([dx, h, w], i) => (
      <g key={i}><rect x={dx - w} y={-h} width={w * 2} height={h} fill={i % 2 ? '#1FA463' : '#2DBE6C'} /><polygon points={`${dx - w},${-h} ${dx},${-h - w * 1.8} ${dx + w},${-h}`} fill="#7CE0A0" /></g>
    ))}
  </svg>
);

// the girl is lost: which field? (pictures / video / 3D signposts spin)
export const C1Lost: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const signs = at(b, 'signs', 20);
  const items = [['🖼️ صور', -14, 760], ['🎬 فيديو', 12, 860], ['🧊 3D', -8, 960]] as const;
  return (
    <Sc>
      <Sky />
      <Land />
      <Dorothy x={330} y={1160} s={1.2} look={Math.sin(f / 12)} />
      <svg width={1080} height={1920} style={{position: 'absolute'}}><rect x={706} y={720} width={18} height={460} fill="#6B4423" /></svg>
      {items.map(([t, r, y], i) => (
        <In key={i} at={signs + i * 6} x={715 + (i % 2 ? 60 : -40)} y={y} rot={r + 6 * Math.sin(f / 10 + i)}>
          <div style={{background: '#9A6A3A', border: '5px solid #6B4423', borderRadius: 10, padding: '8px 26px', fontFamily: AR, fontWeight: 900, fontSize: 42, color: '#FFF3D6',
            whiteSpace: 'nowrap', clipPath: i % 2 ? 'polygon(0 0, 88% 0, 100% 50%, 88% 100%, 0 100%)' : 'polygon(12% 0, 100% 0, 100% 100%, 12% 100%, 0 50%)'}}>{t}</div>
        </In>
      ))}
      {[0, 1, 2].map((i) => <In key={i} at={8 + i * 10} x={250 + i * 90} y={640 - i * 40}><div style={{fontSize: 80, transform: `rotate(${Math.sin(f / 8 + i) * 12}deg)`}}>❓</div></In>)}
      <In at={0} x={540} y={420}><Card><T t="تايهة.. مش عارفة تتخصص في ايه 🤔" /></Card></In>
    </Sc>
  );
};

// the city of Oz: happy people, then the story of the wizard who makes wishes come true
export const C1City: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const wiz = at(b, 'wizard', 120);
  const cols = ['#F26D5B', '#5E95D1', '#2DBE60', '#F2C230', '#B36BD1'];
  return (
    <Sc>
      <Sky />
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        {[[90, 760, '#F7A8C8'], [300, 720, '#9CC3EA'], [560, 740, '#F2C230'], [800, 730, '#7DBB55']].map(([x, y, c], i) => (
          <g key={i}><rect x={x as number} y={y as number} width={190} height={240} fill={c as string} stroke="#2B1D14" strokeWidth={5} /><path d={`M ${(x as number) - 14} ${y} L ${(x as number) + 95} ${(y as number) - 90} L ${(x as number) + 204} ${y} Z`} fill="#C8102E" stroke="#2B1D14" strokeWidth={5} />
            <rect x={(x as number) + 70} y={(y as number) + 140} width={50} height={100} fill="#6B4423" /></g>
        ))}
        <rect x={0} y={980} width={1080} height={500} fill="#F2C230" />
      </svg>
      {cols.map((c, i) => <Townie key={i} x={110 + i * 165} y={1130} s={1.1} c={c} hop={i} />)}
      <In at={0} x={540} y={420}><Card><T t="وصلت لمدينة اسمها أوز 🏘️" /></Card></In>
      {f >= wiz ? <In at={wiz} x={540} y={600}><Bubble w={760} h={170} tail="down"><span style={{fontSize: 44}}>فيه ساحر بيحقق الأمنيات ✨</span></Bubble></In> : null}
    </Sc>
  );
};

// the princess tells her the way: keep walking the yellow brick road, the wizard is at its end
export const C1Princess: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const road = at(b, 'road', 150), end = at(b, 'end', 260);
  return (
    <Sc>
      <Sky />
      <Land />
      {f >= road ? <div style={{position: 'absolute', inset: 0, opacity: lin(f, road, road + 14)}}><EmeraldCity x={600} y={860} s={0.7} glow={lin(f, end, end + 12)} /><BrickRoad vx={600} vy={860} /></div> : null}
      <Princess x={650} y={1110} s={1.2} talk={f < road + 60} point={lin(f, road - 10, road + 6)} look={-0.6} />
      <Dorothy x={230} y={1170} s={1.1} look={0.6} talk={f < 40} />
      <In at={4} out={road - 4} x={400} y={560}><Bubble w={560} h={170} tail="left"><span style={{fontSize: 42}}>قوليلي الطريق للساحر؟</span></Bubble></In>
      <In at={road} x={620} y={500}><Bubble w={700} h={210} tail="right"><span style={{fontSize: 42}}>امشي على الطريق الحجري الأصفر 🟨</span></Bubble></In>
      <In at={end} x={540} y={780}><Pill text="وفي آخره هتلاقي الساحر ✨" bg={C.a} ink="#fff" size={40} /></In>
    </Sc>
  );
};

// end of a chapter: keep walking the yellow brick road + what comes next (keeps them going to the playlist)
export const OzRoad: React.FC<{b?: B; chars?: string[]; next?: string; line?: string; room?: boolean}> = ({b = {}, chars = [], next = '', line = 'خليك ماشي على الطريق الأصفر 🟨', room}) => {
  const f = useCurrentFrame();
  const road = at(b, 'road', 60);
  const n = chars.length;
  // room = his face rectangle sits bottom-right (Aly 2026-10-23): the 4 friends a little smaller, all on the left
  const k = room ? 0.75 : 1, X = (a: number, r: number) => (room ? r : a);
  return (
    <Sc>
      <Land />
      <EmeraldCity x={540} y={860} s={0.9} glow={0.6} />
      <BrickRoad vx={540} vy={860} walk />
      {chars.includes('lion') ? <Lion x={X(690, 495)} y={1150} s={0.95 * k} walk /> : null}
      {chars.includes('tin') ? <TinMan x={X(chars.includes('lion') ? 130 : 250, 130)} y={1130} s={0.95 * k} walk /> : null}
      {chars.includes('scarecrow') ? <Scarecrow x={X(chars.includes('lion') ? 510 : 660, 375)} y={1120} s={1.05 * k} walk /> : null}
      <Dorothy x={X(chars.includes('lion') ? 320 : n ? 450 : 540, 255)} y={1130} s={1.2 * k} walk /> {/* 4 friends: all left of his face circle */}
      <In at={road} x={540} y={470}>
        <Card><T t="خليك فاكر.." size={44} /><T t={line} size={50} color="#C99A1E" /></Card>
      </In>
      {next ? <In at={road + 40} x={540} y={690}><Pill text={next} bg={C.ink} ink="#fff" size={36} /></In> : null}
    </Sc>
  );
};

// ---------------- chapter 3 (3D) ----------------
export const C3Land: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const work = at(b, 'work', 100);
  const cubes = Array.from({length: 9}, (_, i) => ({x: 120 + (i % 5) * 210, y: 760 + Math.floor(i / 5) * 200, c: ['#F2C230', '#5E95D1', '#E8175D', '#2DBE60'][i % 4]}));
  return (
    <Sc>
      <Sky />
      <svg width={1080} height={1920} style={{position: 'absolute'}}><rect x={0} y={1000} width={1080} height={480} fill="#B9C4A4" /><path d="M0 1000 Q 540 940 1080 1000" fill="#C9D3B4" /></svg>
      {cubes.map((q, i) => {
        if (f < work + i * 3) return null;
        const p = spr(f, 30, work + i * 3, 120, 10);
        const ang = f / 30 + i;
        return (
          <svg key={i} width={160} height={160} viewBox="-60 -60 120 120" style={{position: 'absolute', left: q.x - 80, top: q.y - 80 - 20 * Math.sin(f / 15 + i), transform: `scale(${p})`}}>
            <g transform={`rotate(${Math.sin(ang) * 10})`}>
              <polygon points="0,-40 40,-20 0,0 -40,-20" fill={q.c} /><polygon points="-40,-20 0,0 0,44 -40,24" fill={q.c} opacity={0.7} /><polygon points="40,-20 0,0 0,44 40,24" fill={q.c} opacity={0.5} />
            </g>
          </svg>
        );
      })}
      <Dorothy x={330} y={1170} s={1.1} walk={f < 60} />
      <Scarecrow x={600} y={1160} s={1.0} walk={f < 60} />
      <In at={0} x={540} y={420}><Card><T t="أرض واسعة كبيرة قوي 🌄" /></Card></In>
      <In at={work} x={540} y={560}><Pill text="كلهم شغالين في الـ 3D 🧊" bg={grad('oz')} ink={C.ink} size={42} /></In>
    </Sc>
  );
};
export const C3Tin: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const oil = at(b, 'oil', 90), move = at(b, 'move', 200), ask = at(b, 'ask', 280);
  const rust = 1 - lin(f, oil, move);
  return (
    <Sc>
      <Sky />
      <svg width={1080} height={1920} style={{position: 'absolute'}}><rect x={0} y={1000} width={1080} height={480} fill="#B9C4A4" /></svg>
      <TinMan x={700} y={1110} s={1.35} rust={rust} stiff={f < move} walk={f >= move && f < ask} talk={f >= ask} look={-0.6} heart={0} />
      <Dorothy x={280} y={1160} s={1.15} look={0.6} talk={f >= ask - 30 && f < ask} />
      {f >= oil && f < move + 20 ? (
        <div style={{position: 'absolute', left: 440, top: 700, fontSize: 90, transform: `rotate(${-30 + 10 * Math.sin(f / 3)}deg)`}}>🛢️
          {[0, 1, 2].map((i) => <div key={i} style={{position: 'absolute', left: 110 + i * 22, top: 30 + ((f * 6 + i * 20) % 80), width: 14, height: 14, borderRadius: 7, background: '#C99A1E'}} />)}
        </div>
      ) : null}
      <In at={6} out={oil - 4} x={700} y={560}><Pill text="راجل حديدي.. مصدّي ومتيبّس 🥶" size={42} /></In>
      <In at={oil} out={move} x={540} y={560}><Pill text="زيّتته وساعدته 🛢️" bg={C.a} ink="#fff" size={42} /></In>
      <In at={move} out={ask - 4} x={540} y={560}><Pill text="رجع يتحرك تاني 🙌" bg={grad('oz')} ink={C.ink} size={42} /></In>
      <In at={ask} x={420} y={560}><Bubble w={620} h={200} tail="left"><span style={{fontSize: 42}}>كلّمني عن مجالات الـ 3D؟</span></Bubble></In>
    </Sc>
  );
};
// the tin man's wish: "I have no creativity.. no heart" -> heart
export const C3Wish: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const heart = at(b, 'heart', 300);
  return (
    <Sc>
      <Sky />
      <svg width={1080} height={1920} style={{position: 'absolute'}}><rect x={0} y={1000} width={1080} height={480} fill="#B9C4A4" /></svg>
      <TinMan x={620} y={1110} s={1.35} talk look={-0.5} heart={lin(f, heart, heart + 15)} />
      <Dorothy x={220} y={1160} s={1.1} look={0.6} />
      <Scarecrow x={900} y={1150} s={0.95} look={-0.8} />
      <In at={6} out={heart - 4} x={600} y={540}><Bubble w={720} h={220} tail="down"><span style={{fontSize: 42}}>حاسس إن معنديش إبداع.. ومعنديش قلب 💔</span></Bubble></In>
      <In at={heart} x={600} y={540}><Bubble w={560} h={180} tail="down"><span style={{fontSize: 50}}>يديني قلب ❤️</span></Bubble></In>
    </Sc>
  );
};
// the principles shared by all 3D programs (big 3D model + names)
export const C3Principles: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const {durationInFrames: dur} = useVideoConfig();
  const step = Math.max(8, (dur - 12) / 5);
  const stage = Math.min(4, Math.floor(Math.max(0, f - 6) / step));
  const names = ['Modeling', 'Materials', 'Lighting', 'Rigging', 'Animation'];
  return (
    <Sc>
      <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 45%, #33605F 0%, #2C5455 70%, #284D4E 100%)'}} />
      <In at={0} x={540} y={420}><Card><T t="مبادئ الـ 3D واحدة في أغلب البرامج" size={42} /></Card></In>
      <div style={{position: 'absolute', left: 90, top: 470}}><Principles3D w={900} h={560} stage={stage} sf={Math.max(0, f - 6) - stage * step} /></div>
      <div style={{position: 'absolute', top: 1060, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 12, direction: 'ltr'}}>
        {names.map((s2, i) => <div key={s2} style={{fontFamily: EN, fontWeight: 700, fontSize: 30, padding: '8px 16px', borderRadius: 24, color: i <= stage ? '#1E4243' : '#9CC3C0',
          background: i <= stage ? '#F7C531' : 'rgba(255,255,255,0.08)', transform: `scale(${i === stage ? 1.12 : 1})`}}>{s2}</div>)}
      </div>
    </Sc>
  );
};
const F3 = [{e: '🏛️', ar: 'عمارة'}, {e: '🛋️', ar: 'ديكور'}, {e: '🎮', ar: 'ألعاب'}, {e: '🖼️', ar: 'صور'}, {e: '🎬', ar: 'CGI'}, {e: '🧸', ar: 'أفلام 3D'}, {e: '📺', ar: 'إعلانات'}];
type FP = {b?: B; clip?: string; from?: number};
export const F3Arch: React.FC<FP> = ({clip, from}) => <Field i={0} list={F3} who="tin" title="العمارة" en="Architecture" clip={clip} from={from}><div style={{position: 'absolute', left: 90, top: 560}}><Building3D w={900} h={640} t0={4} /></div></Field>;
export const F3Interior: React.FC<FP> = ({clip, from}) => <Field i={1} list={F3} who="tin" title="التصميم الداخلي" en="Interior" clip={clip} from={from}><div style={{position: 'absolute', left: 90, top: 560}}><Room3D w={900} h={640} /></div></Field>;
export const F3Game: React.FC<FP> = ({clip, from}) => {
  const f = useCurrentFrame();
  return (
    <Field i={2} list={F3} who="tin" title="الألعاب" en="Gaming" clip={clip} from={from}>
      <In at={4} x={540} y={850}>
        <svg width={520} height={300} viewBox="0 0 520 300">
          <path d="M80 80 Q 260 40 440 80 Q 520 100 500 220 Q 480 290 400 260 L 330 200 L 190 200 L 120 260 Q 40 290 20 220 Q 0 100 80 80 Z" fill="#2B1D14" />
          <rect x={95} y={130} width={70} height={22} rx={6} fill="#F2C230" /><rect x={119} y={106} width={22} height={70} rx={6} fill="#F2C230" />
          {[[380, 110, '#E8175D'], [420, 145, '#2DBE60'], [380, 180, '#5E95D1'], [340, 145, '#F2C230']].map(([x, y, c], i) => <circle key={i} cx={x as number} cy={y as number} r={18 * (1 + 0.15 * (Math.floor(f / 8) % 4 === i ? 1 : 0))} fill={c as string} />)}
        </svg>
        <div style={{display: 'flex', gap: 18, justifyContent: 'center', marginTop: 16}}>{['🧍 الشخصيات', '⚔️ الأسلحة', '🏞️ المكان'].map((t) => <Pill key={t} text={t} size={34} />)}</div>
      </In>
    </Field>
  );
};
export const F3Pics: React.FC<FP> = ({clip, from}) => (
  <Field i={3} list={F3} who="tin" title="3D في الصور" en="3D in design" clip={clip} from={from}>
    <In at={4} x={540} y={860}><div style={{display: 'flex', gap: 30}}>{['🎬 بوسترات أفلام', '📲 سوشيال ميديا', '🧃 باكدجنج'].map((t, i) => (
      <div key={t} style={{width: 260, height: 330, borderRadius: 20, background: [`linear-gradient(160deg, #2B1D14, #C8102E)`, 'linear-gradient(160deg, #5E95D1, #B36BD1)', 'linear-gradient(160deg, #F7931E, #F2C230)'][i],
        display: 'flex', alignItems: 'flex-end', justifyContent: 'center', padding: 16, boxSizing: 'border-box', fontFamily: AR, fontWeight: 900, fontSize: 30, color: '#fff', boxShadow: '0 14px 30px rgba(0,0,0,0.3)',
        transform: `rotate(${(i - 1) * 4}deg)`}}>{t}</div>))}</div></In>
  </Field>
);
export const F3Cgi: React.FC<FP> = ({clip, from}) => {
  const f = useCurrentFrame();
  const {durationInFrames: dur} = useVideoConfig();
  const step = Math.max(8, (dur - 12) / 5);
  const stage = Math.min(4, Math.floor(Math.max(0, f - 6) / step));
  return <Field i={4} list={F3} who="tin" title="CGI و VFX" en="CGI" clip={clip} from={from}><div style={{position: 'absolute', left: 90, top: 560}}><Principles3D w={900} h={600} stage={stage} sf={Math.max(0, f - 6) - stage * step} /></div></Field>;
};
export const F3Film: React.FC<FP> = ({clip, from}) => <Field i={5} list={F3} who="tin" title="أفلام 3D أنيميشن" en="3D Animation" clip={clip} from={from}><div style={{position: 'absolute', left: 0, top: 560}}><BouncingBall3D w={1080} h={680} /></div></Field>;
export const F3Ads: React.FC<FP> = ({clip, from}) => <Field i={6} list={F3} who="tin" title="إعلانات وموشن 3D" en="3D Motion Graphics" clip={clip} from={from}><div style={{position: 'absolute', left: 90, top: 520}}><Cloner3D w={900} h={700} /></div></Field>;

// ---------------- chapter 4 (video) ----------------
export const C4Forest: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const video = at(b, 'video', 200);
  return (
    <Sc>
      <Sky dark />
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        {Array.from({length: 9}, (_, i) => {
          const x = 40 + i * 125, h = 520 + (i % 3) * 90;
          return <g key={i}><rect x={x} y={1200 - h} width={34} height={h} fill="#3A2A1A" />
            <path d={`M ${x + 17} ${1200 - h + 60} Q ${x - 90} ${1200 - h - 40} ${x - 120} ${1200 - h + 120}`} stroke="#3A2A1A" strokeWidth={14} fill="none" />
            <path d={`M ${x + 17} ${1200 - h + 120} Q ${x + 120} ${1200 - h + 20} ${x + 150} ${1200 - h + 160}`} stroke="#3A2A1A" strokeWidth={12} fill="none" />
            <circle cx={x + 17} cy={1200 - h} r={110} fill={i % 2 ? '#2E6B3A' : '#3E7B44'} opacity={0.9} /></g>;
        })}
        <rect x={0} y={1200} width={1080} height={300} fill="#2E4A2A" />
      </svg>
      {f >= video ? ['🎥', '🎞️', '🎬', '📹'].map((e, i) => <div key={i} style={{position: 'absolute', left: 120 + i * 230, top: 700 + 40 * Math.sin(f / 12 + i), fontSize: 80, transform: `scale(${spr(f, 30, video + i * 4)})`}}>{e}</div>) : null}
      <Dorothy x={300} y={1180} s={1.05} walk={f < 120} />
      <Scarecrow x={520} y={1170} s={0.95} walk={f < 120} />
      <TinMan x={760} y={1170} s={0.95} walk={f < 120} />
      <In at={0} x={540} y={420}><Card><T t="غابة كبيرة.. أشجارها متشابكة 🌳" size={44} /></Card></In>
      <In at={video} x={540} y={560}><Pill text="كلهم شغالين في الفيديو 🎬" bg={grad('oz')} ink={C.ink} size={42} /></In>
    </Sc>
  );
};
export const C4Lion: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const roar = at(b, 'roar', 60), stop = at(b, 'stop', 200), scared = at(b, 'scared', 300);
  const jump = lin(f, roar - 20, roar);
  return (
    <Sc>
      <Sky dark />
      <svg width={1080} height={1920} style={{position: 'absolute'}}><rect x={0} y={1180} width={1080} height={300} fill="#2E4A2A" /></svg>
      <Lion x={760 - 200 * (1 - jump)} y={1160 - 80 * Math.sin(jump * Math.PI)} s={1.3} roar={f >= roar && f < stop} scared={f >= scared} talk={f >= scared} look={-0.6} />
      <Dorothy x={260} y={1170} s={1.15} look={0.6} talk={f >= stop && f < scared} />
      <In at={roar} out={stop - 4} x={700} y={560}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 130, color: '#F2C230', textShadow: '0 8px 0 #9A5B23', transform: `rotate(${-6 + 4 * Math.sin(f)}deg)`}}>ROAR!</div></In>
      <In at={stop} out={scared - 4} x={380} y={560}><Bubble w={520} h={170} tail="left"><span style={{fontSize: 46}}>كفاية كده! ✋</span></Bubble></In>
      <In at={scared} x={600} y={560}><Pill text="طلع خايف وجبان 😨" bg={C.a} ink="#fff" size={44} /></In>
    </Sc>
  );
};
export const C4Fear: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const up = at(b, 'upload', 40), port = at(b, 'portfolio', 120), ppl = at(b, 'people', 250);
  return (
    <Sc>
      <Sky dark />
      <svg width={1080} height={1920} style={{position: 'absolute'}}><rect x={0} y={1180} width={1080} height={300} fill="#2E4A2A" /></svg>
      <Lion x={300} y={1160} s={1.25} scared talk look={0.6} />
      <In at={4} x={700} y={900}>
        <div style={{width: 420, height: 270, background: '#2B1D14', borderRadius: 18, padding: 14, boxSizing: 'border-box'}}>
          <div style={{width: '100%', height: '100%', background: '#fff', borderRadius: 8, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 90}}>{f >= ppl ? '👎💬' : '🎬'}</div>
        </div>
        <div style={{width: 500, height: 24, background: '#5A4A3A', borderRadius: 12, margin: '0 auto'}} />
      </In>
      <In at={up} x={700} y={560}><Pill text="☁️ خايف يرفع شغله" size={40} /></In>
      <In at={port} x={700} y={660}><Pill text="📁 مش عارف يعمل بورتفوليو" bg={grad('oz')} ink={C.ink} size={38} /></In>
      <In at={ppl} x={700} y={1180}><Pill text="💬 خايف من كلام الناس" bg={C.red} ink="#fff" size={40} /></In>
      <In at={0} x={540} y={420}><Card><T t="مشكلته إنه مش لاقي شغل 🦁" size={44} /></Card></In>
    </Sc>
  );
};
export const C4Invite: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const yes = at(b, 'yes', 150);
  return (
    <Sc>
      <Sky dark />
      <svg width={1080} height={1920} style={{position: 'absolute'}}><rect x={0} y={1180} width={1080} height={300} fill="#2E4A2A" /></svg>
      <Lion x={760} y={1160} s={1.2} scared={f < yes} talk={f >= yes} look={-0.6} brave={lin(f, yes, yes + 15) * 0} />
      <Dorothy x={280} y={1170} s={1.15} look={0.6} talk={f < yes} />
      <In at={4} out={yes - 4} x={420} y={560}><Bubble w={700} h={200} tail="left"><span style={{fontSize: 40}}>تعالى معانا للساحر.. يمكن يحل مشكلتك ✨</span></Bubble></In>
      <In at={yes} x={700} y={560}><Bubble w={520} h={170} tail="right"><span style={{fontSize: 48}}>شكرًا جدًا! 🥺</span></Bubble></In>
    </Sc>
  );
};
const F4 = [{e: '✂️', ar: 'مونتاج'}, {e: '🎥', ar: 'صناعة الأفلام'}, {e: '✨', ar: 'VFX'}, {e: '✏️', ar: 'أنيميشن'}, {e: '🔷', ar: 'موشن جرافيك'}, {e: '🧸', ar: 'ستوب موشن'}];
export const F4Edit: React.FC<FP> = ({clip, from}) => {
  const f = useCurrentFrame();
  const clips = [[0, 180, '#5E95D1'], [190, 140, '#E8175D'], [340, 220, '#2DBE60'], [570, 160, '#F2C230']];
  return (
    <Field i={0} list={F4} who="lion" title="المونتاج" en="Video Editing" clip={clip} from={from}>
      <In at={4} x={540} y={860}>
        <div style={{width: 760, height: 260, background: '#2B1D14', borderRadius: 18, padding: 20, boxSizing: 'border-box', position: 'relative'}}>
          {[0, 1, 2].map((r) => <div key={r} style={{position: 'absolute', left: 20, right: 20, top: 24 + r * 74, height: 60, background: '#3A2E26', borderRadius: 8}}>
            {clips.map(([x, w, c], k) => (k + r) % 2 ? null : <div key={k} style={{position: 'absolute', left: (x as number) * 0.95 - ((f * 2) % 40), top: 6, width: (w as number) * 0.9, height: 48, background: c as string, borderRadius: 6}} />)}
          </div>)}
          <div style={{position: 'absolute', top: 10, bottom: 10, left: 20 + ((f * 4) % 720), width: 4, background: '#fff'}} />
        </div>
        <div style={{display: 'flex', gap: 14, justifyContent: 'center', marginTop: 14}}>{['🎬 أفلام', '📺 برامج', '📢 إعلانات', '🌍 وثائقي'].map((t) => <Pill key={t} text={t} size={30} />)}</div>
      </In>
    </Field>
  );
};
export const F4Film: React.FC<FP> = ({clip, from}) => (
  <Field i={1} list={F4} who="lion" title="صناعة الأفلام" en="Filmmaking" clip={clip} from={from}>
    <In at={4} x={540} y={880}><div style={{display: 'flex', gap: 26}}>{[['🎥', 'تصوير'], ['💡', 'إضاءة'], ['🎬', 'إخراج'], ['✂️', 'مونتاج']].map(([e, t], i) => (
      <div key={t} style={{width: 190, height: 230, borderRadius: 24, background: '#fff', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', boxShadow: '0 14px 30px rgba(0,0,0,0.2)'}}>
        <div style={{fontSize: 90}}>{e}</div><div style={{fontFamily: AR, fontWeight: 900, fontSize: 36, color: C.ink}}>{t}</div></div>))}</div></In>
  </Field>
);
export const F4Vfx: React.FC<FP> = ({clip, from}) => {
  const f = useCurrentFrame();
  const k = lin(f, 60, 90);
  return (
    <Field i={2} list={F4} who="lion" title="الفيجوال إفكتس" en="VFX" clip={clip} from={from}>
      <In at={4} x={540} y={880}>
        <div style={{width: 640, height: 360, borderRadius: 20, overflow: 'hidden', position: 'relative', boxShadow: '0 14px 30px rgba(0,0,0,0.3)'}}>
          <div style={{position: 'absolute', inset: 0, background: '#2DBE60', opacity: 1 - k}} />
          <div style={{position: 'absolute', inset: 0, opacity: k, background: 'linear-gradient(180deg, #1A1A40 0%, #6B3A8E 60%, #F7931E 100%)'}}>
            {[0, 1, 2, 3, 4].map((i) => <div key={i} style={{position: 'absolute', left: 60 + i * 120, top: 40 + (i % 2) * 30, width: 6, height: 6, borderRadius: 3, background: '#fff'}} />)}
            <div style={{position: 'absolute', left: 400, top: 60, width: 120, height: 120, borderRadius: 60, background: '#F2C230', boxShadow: '0 0 40px #F2C230'}} />
          </div>
          <svg width={640} height={360} style={{position: 'absolute'}}><circle cx={250} cy={150} r={36} fill="#F2C9A0" /><rect x={210} y={186} width={80} height={140} rx={30} fill="#2B1D14" /></svg>
          <div style={{position: 'absolute', left: 16, top: 12, fontFamily: EN, fontWeight: 900, fontSize: 28, color: '#fff', background: 'rgba(0,0,0,0.5)', padding: '2px 12px', borderRadius: 8}}>{k < 0.5 ? 'GREEN SCREEN' : 'VFX'}</div>
        </div>
        <div style={{display: 'flex', gap: 14, justifyContent: 'center', marginTop: 14}}>{['🧊 3D', '🧩 Compositing', '🏢 شركات كبيرة'].map((t) => <Pill key={t} text={t} size={30} />)}</div>
      </In>
    </Field>
  );
};
export const F4Trad: React.FC<FP> = ({clip, from}) => {
  const f = useCurrentFrame();
  const fr = Math.floor(f / 5) % 6;
  return (
    <Field i={3} list={F4} who="lion" title="أنيميشن تقليدي" en="Frame by frame" clip={clip} from={from}>
      <In at={4} x={540} y={880}><div style={{display: 'flex', gap: 10}}>{[0, 1, 2, 3, 4, 5].map((i) => (
        <div key={i} style={{width: 110, height: 150, background: '#FFF6DF', borderRadius: 8, border: `5px solid ${i === fr ? C.b : '#E3D9C2'}`, position: 'relative', transform: `translateY(${i === fr ? -16 : 0}px)`}}>
          <svg width={100} height={140}><circle cx={50} cy={40 + Math.abs(Math.sin(i / 5 * Math.PI)) * -20 + 30} r={16} fill="#E8175D" /><line x1={10} y1={120} x2={90} y2={120} stroke="#2B1D14" strokeWidth={3} /></svg>
        </div>))}</div>
        <div style={{marginTop: 14, textAlign: 'center'}}><Pill text="✏️ بيترسم فريم فريم" size={32} /></div></In>
    </Field>
  );
};
export const F42d: React.FC<FP> = ({clip, from}) => {
  const f = useCurrentFrame();
  return (
    <Field i={3} list={F4} who="lion" title="2D أنيميشن" en="2D Animation" clip={clip} from={from}>
      <In at={4} x={540} y={880}>
        <div style={{width: 560, height: 315, background: '#fff', borderRadius: 18, position: 'relative', overflow: 'hidden', boxShadow: '0 14px 30px rgba(0,0,0,0.25)'}}>
          <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 40, background: '#E53935'}} />
          <svg width={560} height={315} style={{position: 'absolute'}}><g transform={`translate(${280 + 60 * Math.sin(f / 10)} 200) rotate(${8 * Math.sin(f / 5)})`}><circle r={46} fill="#F2C230" /><circle cx={-15} cy={-8} r={6} fill="#2B1D14" /><circle cx={15} cy={-8} r={6} fill="#2B1D14" /><path d="M -16 14 Q 0 28 16 14" stroke="#2B1D14" strokeWidth={5} fill="none" /></g></svg>
        </div>
        <div style={{marginTop: 14, textAlign: 'center'}}><Pill text="📺 زي قنوات يوتيوب كتير" size={32} /></div></In>
    </Field>
  );
};
export const F43d: React.FC<FP> = ({clip, from}) => <Field i={3} list={F4} who="lion" title="3D أنيميشن" en="3D Animation" clip={clip} from={from}><div style={{position: 'absolute', left: 0, top: 560}}><BouncingBall3D w={1080} h={680} /></div></Field>;
export const F4Mg: React.FC<FP> = ({clip, from}) => (
  <Field i={4} list={F4} who="lion" title="موشن جرافيك" en="Motion Graphics" clip={clip} from={from}>
    <div style={{position: 'absolute', left: 90, top: 520}}><Cloner3D w={900} h={560} /></div>
    <In at={20} x={540} y={1180}><div style={{display: 'flex', gap: 12}}>{['✨ VFX', '📢 إعلانات', '📊 إنفوجرافيك', '🎬 إنتروز'].map((t) => <Pill key={t} text={t} size={30} />)}</div></In>
  </Field>
);
export const F4Stop: React.FC<FP> = ({clip, from}) => {
  const f = useCurrentFrame();
  const st = Math.floor(f / 8) % 4;
  return (
    <Field i={5} list={F4} who="lion" title="ستوب موشن" en="Stop Motion" clip={clip} from={from}>
      <In at={4} x={540} y={880}>
        <svg width={560} height={320} viewBox="0 0 560 320"><rect x={0} y={260} width={560} height={60} fill="#9A6A3A" />
          <g transform={`translate(${120 + st * 90} 0)`}><ellipse cx={0} cy={250} rx={40} ry={12} fill="rgba(0,0,0,0.2)" /><rect x={-30} y={150} width={60} height={100} rx={26} fill="#E8175D" /><circle cx={0} cy={120} r={38} fill="#F2C9A0" /><circle cx={-12} cy={114} r={6} fill="#2B1D14" /><circle cx={12} cy={114} r={6} fill="#2B1D14" /></g>
          <text x={500} y={60} fontSize={48}>📸</text></svg>
        <div style={{textAlign: 'center'}}><Pill text="📸 صورة.. تحريك سنة.. صورة" size={32} /></div></In>
    </Field>
  );
};
export const F4Jobs: React.FC<FP> = ({clip, from}) => (
  <Field i={5} list={F4} who="lion" title="تخصصات كتير" en="Roles" clip={clip} from={from}>
    <In at={4} x={540} y={880}><div style={{display: 'grid', gridTemplateColumns: 'repeat(2, 300px)', gap: 18}}>{['🧊 موديلز', '🦴 ريجنج', '🎬 أنيميشن', '💡 لايتنج'].map((t) => (
      <div key={t} style={{background: '#fff', borderRadius: 20, padding: '20px 0', textAlign: 'center', fontFamily: AR, fontWeight: 900, fontSize: 42, color: C.ink, boxShadow: '0 12px 24px rgba(0,0,0,0.2)'}}>{t}</div>))}</div></In>
  </Field>
);
// they get lazy and fall asleep in a poppy field -> "don't sleep, stay focused"
export const C4Sleep: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const sleep = at(b, 'sleep', 140), focus = at(b, 'focus', 300);
  return (
    <Sc>
      <Sky />
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <rect x={0} y={1000} width={1080} height={480} fill="#5EA43E" />
        {Array.from({length: 40}, (_, i) => <circle key={i} cx={(i * 97) % 1080} cy={1020 + ((i * 53) % 300)} r={14} fill="#E5232B" />)}
      </svg>
      <EmeraldCity x={540} y={820} s={0.7} glow={0.5} />
      {[[150, 'd'], [320, 's'], [490, 't'], [660, 'l']].map(([x, w], i) => { // right side kept free for his face circle
        const z = f >= sleep;
        const node = w === 'd' ? <Dorothy x={x as number} y={1160} s={1.0} /> : w === 's' ? <Scarecrow x={x as number} y={1150} s={0.9} /> : w === 't' ? <TinMan x={x as number} y={1150} s={0.9} /> : <Lion x={x as number} y={1150} s={0.9} />;
        const dx = z ? [340, 470, 600, 720][i] - (x as number) : 0; // asleep: all lie to the left, in a row that ends before his face circle
        return <div key={i} style={{position: 'absolute', inset: 0, transform: z ? `translateX(${dx}px) rotate(-80deg) scale(0.8)` : undefined, transformOrigin: `${x}px 1300px`, transition: 'none'}}>{node}</div>;
      })}
      {f >= sleep ? [0, 1, 2].map((i) => <div key={i} style={{position: 'absolute', left: 200 + i * 180, top: 980 - ((f * 2 + i * 40) % 160), fontFamily: EN, fontWeight: 900, fontSize: 60, color: '#fff', opacity: 0.9}}>Z</div>) : null}
      <In at={0} out={sleep - 4} x={540} y={420}><Card><T t="رايحين أخيرًا لقصر الساحر 🏰" size={44} /></Card></In>
      <In at={sleep} out={focus - 4} x={540} y={420}><Card><T t="كسلوا شوية.. وناموا 😴" size={44} /></Card></In>
      <In at={focus} x={540} y={420}><Card><T t="ما تنامش.. وخليك مركّز 👀" size={48} color={C.red} /></Card></In>
    </Sc>
  );
};
export const C4Intro2: React.FC<{b?: B}> = () => (
  <Sc>
    <Sky dark />
    <svg width={1080} height={1920} style={{position: 'absolute'}}><rect x={0} y={1180} width={1080} height={300} fill="#2E4A2A" /></svg>
    <Lion x={700} y={1160} s={1.25} talk look={-0.6} />
    <Dorothy x={280} y={1170} s={1.1} look={0.6} />
    <In at={0} x={540} y={420}><Card><T t="الأسد بيكمّل مجالات الفيديو 🦁" size={44} /></Card></In>
    <In at={10} x={540} y={560}><Pill text="الأنيميشن ليه أنواع كتير 🎬" bg={grad('oz')} ink={C.ink} size={42} /></In>
  </Sc>
);

// ---------------- chapter 5 (the end: the wizard is just a man; 4 lessons) ----------------
const Hall: React.FC = () => (
  <>
    <AbsoluteFill style={{background: 'linear-gradient(180deg, #0E3B27 0%, #1F7A45 55%, #14532F 100%)'}} />
    <svg width={1080} height={1920} style={{position: 'absolute'}}>{[120, 360, 720, 960].map((x) => <rect key={x} x={x - 30} y={300} width={60} height={900} fill="#2DBE6C" opacity={0.5} />)}
      <rect x={0} y={1200} width={1080} height={300} fill="#0B2E1E" /></svg>
  </>
);
export const C5Castle: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const meet = at(b, 'meet', 200);
  return (
    <Sc>
      <Sky />
      <EmeraldCity x={540} y={1000} s={2.2} glow={0.8} />
      <svg width={1080} height={1920} style={{position: 'absolute'}}><rect x={0} y={1000} width={1080} height={500} fill="#F2C230" /></svg>
      <Dorothy x={260} y={1160} s={1.0} walk={f < meet} /><Scarecrow x={460} y={1150} s={0.9} walk={f < meet} /><TinMan x={650} y={1150} s={0.9} walk={f < meet} /><Lion x={850} y={1150} s={0.9} walk={f < meet} />
      <In at={0} x={540} y={420}><Card><T t="وصلوا لقصر الساحر 🏰" size={46} /></Card></In>
      <In at={meet} x={540} y={560}><Pill text="وقدروا يقابلوه ✨" bg={C.a} ink="#fff" size={42} /></In>
    </Sc>
  );
};
export const C5Reveal: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const man = at(b, 'man', 60), sad = at(b, 'sad', 180), good = at(b, 'good', 300), help = at(b, 'help', 600);
  const curtain = lin(f, man - 20, man);
  return (
    <Sc>
      <Hall />
      <Wizard x={540} y={1100} s={1.3} talk={f >= good} />
      <div style={{position: 'absolute', left: 0, top: 300, width: 540 * (1 - curtain), height: 960, background: 'linear-gradient(90deg, #6B0F1A, #A3192A)'}} />
      <div style={{position: 'absolute', right: 0, top: 300, width: 540 * (1 - curtain), height: 960, background: 'linear-gradient(270deg, #6B0F1A, #A3192A)'}} />
      <In at={man} out={good - 4} x={540} y={420}><Card><T t="الساحر طلع.. راجل عادي! 😮" size={46} /></Card></In>
      <In at={sad} out={good - 4} x={540} y={560}><Pill text="اتضايقوا.. وحسّوا بإحباط 😞" bg={C.red} ink="#fff" size={40} /></In>
      <In at={good} out={help - 4} x={540} y={520}><Bubble w={760} h={210} tail="down"><span style={{fontSize: 42}}>أنا راجل طيب جدًا.. بس ساحر سيئ جدًا 😅</span></Bubble></In>
      <In at={help} x={540} y={520}><Bubble w={700} h={200} tail="down"><span style={{fontSize: 42}}>بس أقدر أساعدكم وأحل مشاكلكم 💪</span></Bubble></In>
    </Sc>
  );
};
// a lesson: the wizard talks to one of them; `lines` = [beat, text, kind] pop one after another
export const C5Lesson: React.FC<{b?: B; who: string; lines: [string, string, string?][]; head: string; room?: boolean}> = ({b = {}, who, lines, head, room}) => {
  const cx = room ? 430 : 640, wx = room ? 170 : 250; // room = his face rectangle sits on the right (Aly 2026-10-23)
  const f = useCurrentFrame();
  const shown = lines.filter(([k]) => f >= at(b, k, 9999)).slice(-3);
  const node = who === 'scarecrow' ? <Scarecrow x={cx} y={1120} s={1.05} look={-0.7} /> : who === 'lion' ? <Lion x={cx} y={1130} s={1.05} look={-0.7} brave={lin(f, at(b, 'brave', 9999), at(b, 'brave', 9999) + 15)} />
    : who === 'tin' ? <TinMan x={cx} y={1120} s={1.05} look={-0.7} heart={lin(f, at(b, 'heart', 9999), at(b, 'heart', 9999) + 15)} /> : <Dorothy x={cx} y={1130} s={1.05} look={-0.7} />;
  return (
    <Sc>
      <Hall />
      <Wizard x={wx} y={1110} s={1.1} talk look={0.7} point={f % 120 < 60} />
      {node}
      <In at={0} x={540} y={410}><Card><T t={head} size={42} /></Card></In>
      <div style={{position: 'absolute', left: 60, right: 60, top: 520, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16}}>
        {shown.map(([k, t, kind]) => {
          const p = spr(f, 30, at(b, k), 190, 13);
          return <div key={k} style={{transform: `scale(${0.5 + 0.5 * p})`, opacity: Math.min(1, p * 1.5)}}><Pill text={t} bg={kind === 'gold' ? grad('oz') : kind === 'red' ? C.red : '#fff'} ink={kind === 'red' ? '#fff' : C.ink} size={40} /></div>;
        })}
      </div>
    </Sc>
  );
};
// typing "What is graphic design" in a search bar -> a playlist of results
export const C5Search: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const q = 'What is graphic design';
  const n = Math.min(q.length, Math.max(0, Math.floor((f - 10) / 2)));
  const res = at(b, 'results', 120), vis = at(b, 'visual', 400), sol = at(b, 'solve', 600);
  return (
    <Sc>
      <Hall />
      <In at={0} x={540} y={420}><Card><T t="أي حد يقدر يتعلم أي حاجة 🧠" size={44} /></Card></In>
      <In at={4} x={540} y={560}>
        <div style={{width: 860, height: 96, background: '#fff', borderRadius: 48, display: 'flex', alignItems: 'center', padding: '0 30px', gap: 18, boxShadow: '0 12px 26px rgba(0,0,0,0.3)', direction: 'ltr'}}>
          <Img src={staticFile('logos/youtube-icon.svg')} style={{height: 50}} />
          <span style={{fontFamily: EN, fontWeight: 600, fontSize: 40, color: '#1E1E24'}}>{q.slice(0, n)}<span style={{opacity: f % 20 < 10 ? 1 : 0}}>|</span></span>
        </div>
      </In>
      {f >= res ? [0, 1, 2].map((i) => (
        <In key={i} at={res + i * 6} x={540} y={720 + i * 150}>
          <div style={{width: 860, height: 130, background: 'rgba(255,255,255,0.95)', borderRadius: 16, display: 'flex', gap: 20, alignItems: 'center', padding: 12, boxSizing: 'border-box', direction: 'ltr'}}>
            <div style={{width: 180, height: 104, borderRadius: 10, background: ['#E8175D', '#5E95D1', '#F2C230'][i]}} />
            <div><div style={{width: 420, height: 18, borderRadius: 9, background: '#555'}} /><div style={{width: 260, height: 14, borderRadius: 7, background: '#AAA', marginTop: 12}} /></div>
          </div>
        </In>
      )) : null}
      <In at={vis} out={sol - 4} x={540} y={1180}><Pill text="Graphics = خطوط • أشكال • ألوان • ملمس • فراغ" size={34} /></In>
      <In at={sol} x={540} y={1180}><Pill text="Design = حل المشكلات 💡" bg={grad('oz')} ink={C.ink} size={40} /></In>
    </Sc>
  );
};
// the sites where they watched a lot of work (logos he names)
export const C5Sites: React.FC<{b?: B; room?: boolean}> = ({b = {}, room}) => {
  const items = ['Behance', 'ArtStation', 'YouTube', 'Vimeo'];
  return (
    <Sc>
      <Hall />
      <TinMan x={room ? 430 : 640} y={1120} s={1.0} heart={1} look={-0.7} />
      <Wizard x={room ? 170 : 260} y={1110} s={1.05} talk look={0.7} />
      <In at={0} x={540} y={410}><Card><T t="كانوا بيتفرجوا على شغل كتير 👀" size={42} /></Card></In>
      {items.map((t, i) => (
        <In key={t} at={at(b, 'sites', 10) + i * 8} x={240 + (i % 2) * 600} y={600 + Math.floor(i / 2) * 140}>
          <div style={{display: 'flex', alignItems: 'center', gap: 12, background: '#fff', borderRadius: 40, padding: '12px 28px', boxShadow: '0 12px 24px rgba(0,0,0,0.3)'}}>
            {t === 'Behance' ? <Img src={staticFile(`projects/2026-10-22 shorts Journey to the center of computer graphics/logos/behance.png`)} style={{height: 46}} /> : t === 'YouTube' ? <Img src={staticFile('logos/youtube-icon.svg')} style={{height: 46}} /> : null}
            <span style={{fontFamily: EN, fontWeight: 800, fontSize: 40, color: '#1E1E24'}}>{t}</span>
          </div>
        </In>
      ))}
      <In at={at(b, 'groups', 200)} x={540} y={900}><Pill text="👥 جروبات فيسبوك" size={40} /></In>
    </Sc>
  );
};

export const oz2Scenes: Record<string, React.FC<any>> = {
  c1_book: C1Book, c1_lost: C1Lost, c1_city: C1City, c1_princess: C1Princess, oz_road: OzRoad,
  c3_land: C3Land, c3_tin: C3Tin, c3_wish: C3Wish, c3_principles: C3Principles,
  f3_arch: F3Arch, f3_interior: F3Interior, f3_game: F3Game, f3_pics: F3Pics, f3_cgi: F3Cgi, f3_film: F3Film, f3_ads: F3Ads,
  c4_forest: C4Forest, c4_lion: C4Lion, c4_fear: C4Fear, c4_invite: C4Invite, c4_intro2: C4Intro2, c4_sleep: C4Sleep,
  f4_edit: F4Edit, f4_film: F4Film, f4_vfx: F4Vfx, f4_trad: F4Trad, f4_2d: F42d, f4_3d: F43d, f4_mg: F4Mg, f4_stop: F4Stop, f4_jobs: F4Jobs,
  c5_castle: C5Castle, c5_reveal: C5Reveal, c5_lesson: C5Lesson, c5_search: C5Search, c5_sites: C5Sites,
};
export {logo, OzBadge, CornField, EN};
