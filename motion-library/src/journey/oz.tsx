import React from 'react';
import {AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Pack3D} from './three';
import {AR, Bubble, BrickRoad, CornField, Dorothy, EmeraldCity, EN, grad, In, JY, lin, OzBadge, Pill, Sc, Scarecrow, spr} from './kit';

// "المجالات و ساحر مدينة أوز" — chapter 2 "صور" (ep 33): Dorothy meets the Scarecrow in the big farm where everyone
// works in pictures & graphic design; he tells her the fields. Everything DRAWN (Aly 2026-10-22: no film footage).
const C = JY.oz;
type B = Record<string, number>;
const at = (b: B, k: string, d = 0) => b[k] ?? d;

// sky + far hills (behind the road / the farm)
const Land: React.FC<{hills?: boolean}> = ({hills = true}) => {
  const f = useCurrentFrame();
  return (
    <svg width={1080} height={1920} style={{position: 'absolute'}}>
      {[[180, 420, 1.2], [760, 360, 1], [470, 520, 0.8]].map(([x, y, s], i) => (
        <g key={i} transform={`translate(${(x + f * 0.3 * (i + 1)) % 1300 - 110} ${y}) scale(${s})`} opacity={0.9}>
          <ellipse cx={0} cy={0} rx={70} ry={30} fill="#fff" /><ellipse cx={50} cy={-12} rx={50} ry={30} fill="#fff" /><ellipse cx={-50} cy={-8} rx={44} ry={24} fill="#fff" />
        </g>
      ))}
      {hills ? <>
        <path d="M0 860 Q 220 740 460 830 T 1080 800 L 1080 1100 L 0 1100 Z" fill="#7DBB55" />
        <path d="M0 900 Q 300 820 600 900 T 1080 880 L 1080 1100 L 0 1100 Z" fill="#5EA43E" />
      </> : null}
    </svg>
  );
};

// 1) Dorothy walks the yellow brick road toward the emerald city ("الفصل التاني: صور")
export const OzWalk: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const city = at(b, 'city', 100);
  return (
    <Sc>
      <Land />
      <EmeraldCity x={540} y={860} s={0.9} glow={0.3 + 0.7 * lin(f, city, city + 12)} />
      <BrickRoad vx={540} vy={860} walk />
      <Dorothy x={540} y={1100 - 20 * lin(f, 0, 200)} s={1.4 - 0.25 * lin(f, 0, 200)} walk />
      <In at={2} x={540} y={420}>
        <div style={{display: 'flex', alignItems: 'center', gap: 20, direction: 'rtl', background: C.card, padding: '14px 30px', borderRadius: 60, boxShadow: '0 12px 30px rgba(0,0,0,0.2)'}}>
          <OzBadge d={90} />
          <div style={{fontFamily: AR, fontWeight: 900, fontSize: 48, color: C.ink, whiteSpace: 'nowrap'}}>الفصل التاني: <span style={{color: C.a}}>صور</span></div>
        </div>
      </In>
      <In at={city} x={540} y={690}><Pill text="ساحر مدينة أوز ✨" bg={C.a} ink="#fff" size={42} /></In>
    </Sc>
  );
};

// 2) the big farm where everyone works in pictures & graphic design
export const OzFarm: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const work = at(b, 'work', 120);
  const icons = ['🖼️', '🎨', '✏️', '📐', '🖌️', '🖨️', '📷', '💻'];
  return (
    <Sc>
      <Land />
      <CornField y={1000} />
      <Dorothy x={460} y={1170} s={1.2} look={0.3} />
      <In at={4} x={540} y={760} rot={-3}>
        <div style={{background: '#9A6A3A', padding: '18px 40px', borderRadius: 12, border: '6px solid #6B4423', boxShadow: '0 14px 26px rgba(0,0,0,0.3)'}}>
          <div style={{fontFamily: AR, fontWeight: 900, fontSize: 64, color: '#FFF3D6'}}>مزرعة كبيرة قوي 🌽</div>
        </div>
        <div style={{position: 'absolute', left: '48%', top: '100%', width: 18, height: 180, background: '#6B4423'}} />
      </In>
      {icons.map((ic, i) => {
        const t0 = work + i * 4;
        if (f < t0) return null;
        const p = spr(f, 30, t0, 120, 10);
        const x = 90 + i * 128, y = 1000 - 260 * p - 20 * Math.sin(f / 9 + i);
        return <div key={i} style={{position: 'absolute', left: x - 50, top: y - 50, fontSize: 90, transform: `scale(${p}) rotate(${Math.sin(f / 12 + i) * 10}deg)`}}>{ic}</div>;
      })}
      <In at={work} x={540} y={420}><Pill text="كلهم شغالين في الصور والجرافيك ديزاين" bg={grad('oz')} ink={C.ink} size={40} /></In>
    </Sc>
  );
};

// 3) the scarecrow on his pole, Dorothy asks him; he agrees
export const OzMeet: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const ask = at(b, 'ask', 150), yes = at(b, 'yes', 300), years = at(b, 'years', 90);
  const talkS = f > yes - 4 || (f > 20 && f < ask - 10);
  return (
    <Sc>
      <Land />
      <CornField y={1080} sway={0.6} />
      <Scarecrow x={560} y={980} s={1.3} onPole talk={talkS} look={-0.6} />
      <Dorothy x={200} y={1170} s={1.15} talk={f > ask && f < yes - 6} look={0.6} />
      <In at={14} out={ask - 6} x={700} y={520}><Pill text="خيال مآتة.. بيتكلم! 😮" size={46} /></In>
      <In at={years} out={ask - 6} x={700} y={620}><Pill text="واقف هنا بقاله سنين ⏳" bg={C.a} ink="#fff" size={40} /></In>
      <In at={ask} out={yes - 4} x={360} y={560}><Bubble w={620} h={220} tail="left"><span style={{fontSize: 46}}>ممكن تكلّمني على مجالات الجرافيكس؟</span></Bubble></In>
      <In at={yes} x={600} y={520}><Bubble w={520} h={170} tail="right"><span style={{fontSize: 52}}>تعالي أقولك 😊</span></Bubble></In>
    </Sc>
  );
};

// 4) "many fields, full of specialities.. here are some" — tiles fly into a board
const FIELDS = [
  {e: '📱', ar: 'UI / UX'}, {e: '🏷️', ar: 'براندينج'}, {e: '🖨️', ar: 'مطبوعات'}, {e: '🧃', ar: 'باكدجنج'},
  {e: '📲', ar: 'سوشيال ميديا'}, {e: '📷', ar: 'تصوير وريتاتش'}, {e: '✒️', ar: 'إليستريشن'}, {e: '🖌️', ar: 'ديجيتال بينتنج'},
];
export const OzMany: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const some = at(b, 'some', 80);
  return (
    <Sc>
      <AbsoluteFill style={{background: `radial-gradient(circle at 50% 45%, ${C.card} 0%, ${C.bg0} 55%, ${C.bg1} 100%)`}} />
      <In at={0} x={540} y={400}><div style={{fontFamily: AR, fontWeight: 900, fontSize: 64, color: C.ink, direction: 'rtl', whiteSpace: 'nowrap'}}>مجالات <span style={{fontFamily: EN, color: C.a}}>Graphic Design</span></div></In>
      <In at={8} x={540} y={490}><Pill text="كتيرة قوي ومليانة تخصصات" bg={C.ink} ink="#fff" size={38} /></In>
      {FIELDS.map((x, i) => {
        const col = i % 2, row = Math.floor(i / 2);
        return (
          <In key={i} at={14 + i * 3} x={col ? 290 : 790} y={680 + row * 200} rot={(i % 3) - 1} slide={60}>
            <div style={{width: 440, height: 160, borderRadius: 26, background: '#fff', display: 'flex', alignItems: 'center', gap: 20, padding: '0 26px', direction: 'rtl',
              boxShadow: '0 14px 28px rgba(0,0,0,0.18)', border: `5px solid ${f >= some ? C.b : '#fff'}`, boxSizing: 'border-box'}}>
              <span style={{fontSize: 72}}>{x.e}</span><span style={{fontFamily: AR, fontWeight: 900, fontSize: 44, color: C.ink}}>{x.ar}</span>
            </div>
          </In>
        );
      })}
      <In at={some} x={540} y={1500}><Pill text="تعالي أقولك على شوية منهم 👇" bg={grad('oz')} ink={C.ink} size={40} /></In>
    </Sc>
  );
};

// ---- field scenes: a cream "board" in the middle, the scarecrow presents from the bottom-left, a track of the 8 fields on top ----
const Track: React.FC<{i: number}> = ({i}) => (
  <div style={{position: 'absolute', top: 300, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 10, direction: 'rtl'}}>
    {FIELDS.map((x, k) => (
      <div key={k} style={{width: 92, height: 92, borderRadius: 22, background: k === i ? C.b : k < i ? '#FFF6DF' : 'rgba(255,255,255,0.45)', display: 'flex',
        alignItems: 'center', justifyContent: 'center', fontSize: 50, border: k === i ? `5px solid ${C.ink}` : '5px solid transparent', boxSizing: 'border-box',
        transform: `scale(${k === i ? 1.12 : 0.92})`, opacity: k <= i ? 1 : 0.6}}>{x.e}</div>
    ))}
  </div>
);
const Field: React.FC<{i: number; title: string; en?: string; children: React.ReactNode; clip?: string; from?: number}> = ({i, title, en, children, clip, from = 0}) => {
  const {fps} = useVideoConfig();
  const f = useCurrentFrame();
  return (
    <Sc>
      <AbsoluteFill style={{background: `radial-gradient(circle at 50% 50%, ${C.card} 0%, ${C.bg0} 60%, ${C.bg1} 100%)`}} />
      <Track i={i} />
      <In at={0} x={540} y={470}>
        <div style={{display: 'flex', alignItems: 'baseline', gap: 18, direction: 'rtl'}}>
          <span style={{fontFamily: AR, fontWeight: 900, fontSize: 64, color: C.ink, whiteSpace: 'nowrap'}}>{title}</span>
          {en ? <span style={{fontFamily: EN, fontWeight: 800, fontSize: 36, color: C.a, whiteSpace: 'nowrap'}}>{en}</span> : null}
        </div>
      </In>
      {clip ? (
        // his WHOLE chapter frame while he scrolls the examples (Aly v2 review: "حطها كاملة… من الفيديو و انا بعمل سكرول")
        <div style={{position: 'absolute', left: 150, top: 560, width: 780, height: 440, padding: 8, borderRadius: 26, background: grad('oz'), boxShadow: '0 22px 44px rgba(0,0,0,0.25)'}}>
          <div style={{width: 764, height: 424, borderRadius: 18, overflow: 'hidden', position: 'relative'}}>
            <OffthreadVideo muted src={staticFile(clip)} startFrom={Math.round(from * fps)} style={{width: 764, height: 430, maxWidth: 'none'}} />
          </div>
        </div>
      ) : null}
      {/* with his frame on top the small drawings only collided with the captions (v3) -> frame + scarecrow only */}
      {/* his frame on top, the field's motion right under it (compact, never under the captions) */}
      <AbsoluteFill style={{transform: clip ? 'translate(30px, 400px) scale(0.5)' : 'translate(-60px, 150px) scale(0.7)', transformOrigin: '540px 600px'}}>{children}</AbsoluteFill>
      <Scarecrow x={110} y={(clip ? 1180 : 1300) + 6 * Math.sin(f / 10)} s={clip ? 0.55 : 0.62} talk look={0.8} />
    </Sc>
  );
};

const Card: React.FC<{w: number; h: number; children?: React.ReactNode; bg?: string; r?: number}> = ({w, h, children, bg = '#fff', r = 20}) => (
  <div style={{width: w, height: h, background: bg, borderRadius: r, boxShadow: '0 16px 34px rgba(0,0,0,0.22)', position: 'relative', overflow: 'hidden'}}>{children}</div>
);
const Lbl: React.FC<{t: string; en?: boolean; size?: number}> = ({t, en, size = 34}) => (
  <div style={{textAlign: 'center', marginTop: 10, fontFamily: en ? EN : AR, fontWeight: 900, fontSize: size, color: C.ink, whiteSpace: 'nowrap'}}>{t}</div>
);
const bars = (n: number, w: number, c = '#E3D9C2') => Array.from({length: n}, (_, i) => <div key={i} style={{height: 14, width: `${w - (i % 3) * 18}%`, background: c, borderRadius: 7, margin: '10px 16px'}} />);

// 5) UI / UX: a phone app + a website being designed
export const FUiux: React.FC<{b?: B; clip?: string; from?: number}> = ({b = {}, clip, from}) => {
  const f = useCurrentFrame();
  const ux = at(b, 'ux', 30), web = at(b, 'web', 200), app = at(b, 'android', 250);
  const tap = (f - ux) % 40;
  return (
    <Field clip={clip} from={from} i={0} title="UI و UX">
      <In at={4} x={300} y={640}><Pill text="UI = شكل الواجهة" font={AR} size={36} /></In>
      <In at={ux} x={780} y={640}><Pill text="UX = تجربة المستخدم" bg={C.a} ink="#fff" size={36} /></In>
      <In at={Math.min(web, 20)} x={720} y={1020}>
        <Card w={520} h={340} r={18}>
          <div style={{height: 34, background: '#E9E2D0', display: 'flex', gap: 8, alignItems: 'center', paddingLeft: 12}}>{['#E5534B', '#F2C230', '#2DBE60'].map((c) => <div key={c} style={{width: 14, height: 14, borderRadius: 7, background: c}} />)}</div>
          <div style={{height: 110, margin: 14, borderRadius: 12, background: grad('oz')}} />
          <div style={{display: 'flex', gap: 12, margin: '0 14px'}}>{[0, 1, 2].map((k) => <div key={k} style={{flex: 1, height: 120, borderRadius: 10, background: '#F3EBD6', opacity: lin(f, 30 + k * 6, 40 + k * 6)}} />)}</div>
        </Card>
        <Lbl t="ويب" />
      </In>
      <In at={Math.min(app, 30)} x={350} y={1060}>
        <div style={{width: 230, height: 440, borderRadius: 40, background: '#2B1D14', padding: 12, boxShadow: '0 16px 34px rgba(0,0,0,0.3)'}}>
          <div style={{width: '100%', height: '100%', borderRadius: 30, background: '#fff', overflow: 'hidden', position: 'relative'}}>
            <div style={{height: 120, background: C.a}} />
            {bars(5, 80)}
            <div style={{position: 'absolute', left: 30, right: 30, bottom: 30, height: 56, borderRadius: 28, background: C.b, transform: `scale(${f > ux && tap < 6 ? 0.92 : 1})`}} />
            {f > ux ? <div style={{position: 'absolute', left: 100, bottom: 40, width: 40, height: 40, borderRadius: 20, border: '4px solid #2B1D14', opacity: tap < 12 ? 1 - tap / 12 : 0, transform: `scale(${1 + tap / 8})`}} /> : null}
          </div>
        </div>
        <Lbl t="أندرويد" />
      </In>
    </Field>
  );
};

// 6) Branding: logo → its colours → its font → business card
export const FBrand: React.FC<{b?: B; clip?: string; from?: number}> = ({b = {}, clip, from}) => {
  const col = at(b, 'colors', 120), font = at(b, 'font', 250), card = at(b, 'card', 360);
  const Mark = ({s = 1}: {s?: number}) => (
    <svg width={160 * s} height={160 * s} viewBox="0 0 160 160"><circle cx={80} cy={80} r={74} fill={C.a} /><path d="M40 104 L80 40 L120 104 Z" fill={C.b} /><circle cx={80} cy={96} r={14} fill="#fff" /></svg>
  );
  return (
    <Field clip={clip} from={from} i={1} title="براندينج" en="Branding">
      <In at={6} x={540} y={760}><div style={{display: 'flex', alignItems: 'center', gap: 20, direction: 'ltr'}}><Mark /><span style={{fontFamily: EN, fontWeight: 900, fontSize: 70, color: C.ink}}>OZ.co</span></div><Lbl t="اللوجو" /></In>
      {[C.a, C.b, C.ink, '#FFF6DF'].map((c, k) => (
        <In key={c} at={col + k * 4} x={300 + k * 160} y={1000}><div style={{width: 130, height: 130, borderRadius: 24, background: c, boxShadow: '0 10px 20px rgba(0,0,0,0.2)', border: '4px solid #fff'}} /></In>
      ))}
      <In at={col} x={540} y={1110}><Lbl t="الألوان" /></In>
      <In at={font} x={330} y={1260}><div style={{fontFamily: EN, fontWeight: 900, fontSize: 110, color: C.ink}}>Aa</div><Lbl t="الفونت" /></In>
      <In at={card} x={760} y={1260} rot={-6}><Card w={330} h={190} bg={C.ink}><div style={{position: 'absolute', left: 20, top: 30}}><Mark s={0.6} /></div><div style={{position: 'absolute', right: 20, top: 60, width: 140}}>{bars(3, 90, '#6B4A2E')}</div></Card><Lbl t="كارت البيزنس" /></In>
    </Field>
  );
};

// 7) Print: roll-up, banners, street signs + layouts of books, flyers, brochures
export const FPrint: React.FC<{b?: B; clip?: string; from?: number}> = ({b = {}, clip, from}) => {
  const f = useCurrentFrame();
  const roll = at(b, 'rollup', 120), ban = at(b, 'banner', 150), sign = at(b, 'sign', 170), lay = at(b, 'layout', 300), fly = at(b, 'flyer', 330), bro = at(b, 'brochure', 360);
  const second = f >= lay - 6;
  return (
    <Field clip={clip} from={from} i={2} title="مطبوعات" en="Print">
      {!second ? <>
        <In at={roll} x={260} y={1000}><div style={{width: 200, height: 460, background: '#fff', borderTop: `20px solid ${C.ink}`, boxShadow: '0 14px 30px rgba(0,0,0,0.2)', position: 'relative'}}>
          <div style={{height: 160, margin: 14, background: grad('oz'), borderRadius: 8}} />{bars(4, 80)}<div style={{position: 'absolute', bottom: -30, left: -20, right: -20, height: 30, background: C.ink, borderRadius: 6}} /></div><Lbl t="رول أب" /></In>
        <In at={ban} x={720} y={760}><div style={{width: 460, height: 150, background: C.a, borderRadius: 6, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 12px 24px rgba(0,0,0,0.2)'}}><span style={{fontFamily: AR, fontWeight: 900, fontSize: 56, color: '#fff'}}>تخفيضات 50%</span></div><Lbl t="بانر" /></In>
        <In at={sign} x={720} y={1150}><div style={{width: 420, height: 230, background: '#FFF6DF', border: `10px solid ${C.ink}`, display: 'flex', alignItems: 'center', justifyContent: 'center'}}><span style={{fontFamily: AR, fontWeight: 900, fontSize: 52, color: C.ink}}>مطعم أوز 🍔</span></div>
          <div style={{display: 'flex', justifyContent: 'space-between', padding: '0 80px'}}><div style={{width: 16, height: 110, background: C.ink}} /><div style={{width: 16, height: 110, background: C.ink}} /></div><Lbl t="يافطة في الشارع" /></In>
      </> : <>
        <In at={lay} x={300} y={980} rot={-4}><div style={{display: 'flex', boxShadow: '0 14px 30px rgba(0,0,0,0.25)'}}>{[0, 1].map((k) => <div key={k} style={{width: 190, height: 270, background: '#fff', borderRight: k ? undefined : '3px solid #E3D9C2'}}>{k ? <div style={{height: 110, margin: 14, background: C.a, borderRadius: 6}} /> : null}{bars(k ? 4 : 9, 85)}</div>)}</div><Lbl t="كتاب" /></In>
        <In at={fly} x={780} y={860} rot={5}><Card w={250} h={340} r={8}><div style={{height: 150, background: grad('oz')}} /><div style={{fontFamily: AR, fontWeight: 900, fontSize: 40, textAlign: 'center', marginTop: 8}}>عرض!</div>{bars(3, 80)}</Card><Lbl t="فلاير" /></In>
        <In at={bro} x={720} y={1290}><div style={{display: 'flex', transform: 'perspective(800px) rotateY(-10deg)'}}>{[0, 1, 2].map((k) => <div key={k} style={{width: 130, height: 230, background: k === 1 ? '#FFF6DF' : '#fff', boxShadow: '0 10px 20px rgba(0,0,0,0.18)'}}><div style={{height: 70, margin: 10, background: [C.a, C.b, C.ink][k], borderRadius: 6}} />{bars(3, 80)}</div>)}</div><Lbl t="بروشور" /></In>
      </>}
    </Field>
  );
};

// 8) Packaging: juice box, chips bag, carton
export const FPack: React.FC<{b?: B; clip?: string; from?: number}> = ({b = {}, clip, from}) => {
  const j = at(b, 'juice', 100), c = at(b, 'chips', 120), k = at(b, 'carton', 140);
  return (
    <Field clip={clip} from={from} i={3} title="باكدجنج" en="Packaging">
      <In at={4} x={540} y={640}><Pill text="أي حاجة متعلبة 📦" size={40} /></In>
      <div style={{position: 'absolute', left: 40, top: 700}}><Pack3D w={1000} h={560} at={[Math.min(j, 20), Math.min(c, 30), Math.min(k, 40)]} /></div>
      <In at={Math.min(j, 20)} x={240} y={1240}><Lbl t="عصير" /></In>
      <In at={Math.min(c, 30)} x={540} y={1240}><Lbl t="شيبسي" /></In>
      <In at={Math.min(k, 40)} x={840} y={1240}><Lbl t="كرتونة" /></In>
    </Field>
  );
};

// 9) Social media designs + movie posters
export const FSocial: React.FC<{b?: B; clip?: string; from?: number}> = ({b = {}, clip, from}) => {
  const f = useCurrentFrame();
  const poster = at(b, 'poster', 100);
  const scroll = (f * 3) % 300;
  return (
    <Field clip={clip} from={from} i={4} title="سوشيال ميديا" en="Social Media">
      <In at={4} x={400} y={1000}>
        <div style={{width: 300, height: 560, borderRadius: 44, background: '#2B1D14', padding: 12}}>
          <div style={{width: '100%', height: '100%', borderRadius: 34, background: '#fff', overflow: 'hidden'}}>
            <div style={{transform: `translateY(${-scroll}px)`}}>
              {[C.a, C.b, '#5E95D1', C.a, C.b, '#5E95D1'].map((c, k) => (
                <div key={k} style={{margin: 12}}><div style={{display: 'flex', gap: 8, alignItems: 'center', marginBottom: 8}}><div style={{width: 30, height: 30, borderRadius: 15, background: '#ddd'}} /><div style={{width: 120, height: 12, borderRadius: 6, background: '#ddd'}} /></div>
                  <div style={{height: 230, borderRadius: 12, background: `linear-gradient(135deg, ${c}, ${C.b})`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: AR, fontWeight: 900, fontSize: 40, color: '#fff'}}>بوست</div>
                  <div style={{fontSize: 26, marginTop: 6}}>❤️ 💬 ↗️</div></div>
              ))}
            </div>
          </div>
        </div>
      </In>
      <In at={poster} x={770} y={1010} rot={4}>
        <div style={{width: 320, height: 470, background: '#1B1410', borderRadius: 8, boxShadow: '0 18px 36px rgba(0,0,0,0.35)', position: 'relative', overflow: 'hidden'}}>
          <div style={{position: 'absolute', inset: 0, background: `radial-gradient(circle at 50% 35%, ${C.a} 0%, transparent 60%)`}} />
          <svg width={320} height={300} style={{position: 'absolute', top: 60}}><path d="M60 300 L160 40 L260 300 Z" fill="#14804A" /><path d="M120 300 L160 120 L200 300 Z" fill="#2DBE6C" /></svg>
          <div style={{position: 'absolute', bottom: 70, width: '100%', textAlign: 'center', fontFamily: AR, fontWeight: 900, fontSize: 52, color: C.b}}>المدينة الخضرا</div>
          <div style={{position: 'absolute', bottom: 30, width: '100%', textAlign: 'center', fontFamily: EN, fontWeight: 700, fontSize: 18, letterSpacing: 4, color: '#fff'}}>COMING SOON</div>
        </div>
        <Lbl t="بوستر فيلم" />
      </In>
    </Field>
  );
};

// 10) Photographers + retouching: camera flash, then a before/after slider over a portrait
export const FPhoto: React.FC<{b?: B; clip?: string; from?: number}> = ({b = {}, clip, from}) => {
  const f = useCurrentFrame();
  const shot = at(b, 'shot', 60), ret = at(b, 'retouch', 200);
  const flash = f > shot && f < shot + 8 ? 1 - (f - shot) / 8 : 0;
  const slider = 0.15 + 0.7 * (0.5 + 0.5 * Math.sin((f - ret) / 14));
  const face = (clean: boolean) => (
    <svg width={460} height={460} viewBox="0 0 460 460">
      <rect width={460} height={460} fill={clean ? '#F7E7CF' : '#C9B9A0'} />
      <ellipse cx={230} cy={420} rx={170} ry={110} fill="#5E95D1" />
      <ellipse cx={230} cy={210} rx={110} ry={130} fill={clean ? '#F2CBA6' : '#C99C78'} />
      <path d="M120 180 Q 130 70 230 70 Q 330 70 340 180 Q 300 120 230 120 Q 160 120 120 180 Z" fill="#6B3A1E" />
      <circle cx={190} cy={210} r={10} fill="#2A1A10" /><circle cx={270} cy={210} r={10} fill="#2A1A10" />
      <path d="M195 270 Q 230 295 265 270" stroke="#9B3B3B" strokeWidth={8} fill="none" strokeLinecap="round" />
      {!clean ? [[170, 250], [290, 250], [250, 170], [200, 290], [300, 220]].map(([x, y], k) => <circle key={k} cx={x} cy={y} r={7} fill="#A0522D" opacity={0.7} />) : null}
    </svg>
  );
  return (
    <Field clip={clip} from={from} i={5} title="تصوير وريتاتش" en="Retouching">
      {f < ret ? (
        <In at={4} x={600} y={1000}>
          <div style={{width: 420, height: 290, background: '#2B1D14', borderRadius: 50, position: 'relative', boxShadow: '0 20px 40px rgba(0,0,0,0.3)'}}>
            <div style={{position: 'absolute', left: 120, top: 55, width: 180, height: 180, borderRadius: '50%', background: '#111', border: '16px solid #6B4A2E'}} />
            <div style={{position: 'absolute', left: 40, top: -34, width: 110, height: 44, background: '#2B1D14', borderRadius: 10}} />
          </div>
          <Lbl t="الناس اللي بتصوّر 📷" />
        </In>
      ) : (
        <In at={ret} x={600} y={1000}>
          <div style={{width: 460, height: 460, position: 'relative', borderRadius: 20, overflow: 'hidden', boxShadow: '0 20px 40px rgba(0,0,0,0.3)'}}>
            <div style={{position: 'absolute', inset: 0}}>{face(true)}</div>
            <div style={{position: 'absolute', inset: 0, clipPath: `inset(0 ${(1 - slider) * 100}% 0 0)`}}>{face(false)}</div>
            <div style={{position: 'absolute', top: 0, bottom: 0, left: `${slider * 100}%`, width: 6, background: '#fff', transform: 'translateX(-3px)'}} />
            <div style={{position: 'absolute', top: 14, left: 14, fontFamily: EN, fontWeight: 800, fontSize: 24, color: '#fff', background: 'rgba(0,0,0,0.5)', padding: '2px 10px', borderRadius: 6}}>BEFORE</div>
            <div style={{position: 'absolute', top: 14, right: 14, fontFamily: EN, fontWeight: 800, fontSize: 24, color: '#fff', background: 'rgba(0,0,0,0.5)', padding: '2px 10px', borderRadius: 6}}>AFTER</div>
          </div>
          <Lbl t="ريتاتش بعد التصوير ✨" />
        </In>
      )}
      <AbsoluteFill style={{background: '#fff', opacity: flash}} />
    </Field>
  );
};

// 11) Illustration: a vector character drawn, then used in a magazine, a newspaper, a video, a design
export const FIllus: React.FC<{b?: B; clip?: string; from?: number}> = ({b = {}, clip, from}) => {
  const f = useCurrentFrame();
  const use = at(b, 'mag', 150);
  const d = lin(f, 6, 90);
  const lion = (s: number) => (
    <svg width={220 * s} height={220 * s} viewBox="0 0 220 220">
      <circle cx={110} cy={110} r={100} fill="#D9822B" /><circle cx={110} cy={118} r={64} fill="#F2C230" />
      <circle cx={88} cy={108} r={8} fill="#2B1D14" /><circle cx={132} cy={108} r={8} fill="#2B1D14" />
      <path d="M100 136 L120 136 L110 148 Z" fill="#6B3A1E" /><path d="M92 156 Q 110 168 128 156" stroke="#6B3A1E" strokeWidth={5} fill="none" />
    </svg>
  );
  const uses = [{t: 'مجلة', x: 250, y: 1230}, {t: 'جريدة', x: 540, y: 1260}, {t: 'فيديو', x: 830, y: 1230}];
  return (
    <Field clip={clip} from={from} i={6} title="إليستريشن" en="Illustration">
      <In at={2} x={540} y={850}>
        <div style={{position: 'relative', width: 340, height: 340}}>
          <svg width={340} height={340} viewBox="0 0 220 220" style={{position: 'absolute'}}>
            <circle cx={110} cy={110} r={100} fill="none" stroke={C.ink} strokeWidth={3} pathLength={1} strokeDasharray={`${d} 1`} />
            <circle cx={110} cy={118} r={64} fill="none" stroke={C.ink} strokeWidth={3} pathLength={1} strokeDasharray={`${lin(f, 30, 90)} 1`} />
          </svg>
          <div style={{position: 'absolute', inset: 0, opacity: lin(f, 90, 104)}}>{lion(340 / 220)}</div>
          {f < 104 ? <div style={{position: 'absolute', left: 170 + 150 * Math.cos(d * 6.28), top: 120 + 150 * Math.sin(d * 6.28), fontSize: 60}}>🖊️</div> : null}
        </div>
      </In>
      {uses.map((u, k) => (
        <In key={u.t} at={use + k * 22} x={u.x} y={u.y} rot={(k - 1) * 4}>
          <Card w={230} h={260} r={10} bg={k === 2 ? '#2B1D14' : '#fff'}>
            <div style={{position: 'absolute', top: 16, left: 16, right: 16, height: 20, background: k === 1 ? '#555' : C.a, borderRadius: 4}} />
            <div style={{position: 'absolute', top: 50, left: 45}}>{lion(0.65)}</div>
            {k === 2 ? <div style={{position: 'absolute', bottom: 16, left: 16, right: 16, height: 8, background: '#555', borderRadius: 4}}><div style={{width: `${(f * 2) % 100}%`, height: '100%', background: C.red, borderRadius: 4}} /></div> : <div style={{position: 'absolute', bottom: 10, left: 0, right: 0}}>{bars(2, 80)}</div>}
          </Card>
          <Lbl t={u.t} />
        </In>
      ))}
    </Field>
  );
};

// 12) Digital painting: painting on a tablet (Photoshop) vs on paper with a pen — a different feeling
export const FPaint: React.FC<{b?: B; clip?: string; from?: number}> = ({b = {}, clip, from}) => {
  const f = useCurrentFrame();
  const paper = at(b, 'paper', 250);
  const strokes = [
    {d: 'M40 300 Q 180 120 360 260', c: '#5E95D1', t: 20}, {d: 'M60 330 Q 220 200 380 320', c: '#7DBB55', t: 40}, {d: 'M260 90 m -40 0 a 40 40 0 1 0 80 0 a 40 40 0 1 0 -80 0', c: '#F2C230', t: 60},
    {d: 'M30 360 L 400 360', c: '#5EA43E', t: 80}, {d: 'M120 340 L 160 200 L 200 340', c: '#14804A', t: 100},
  ];
  return (
    <Field clip={clip} from={from} i={7} title="ديجيتال بينتنج" en="Digital Painting">
      <In at={4} x={540} y={940}>
        <div style={{width: 560, height: 420, borderRadius: 34, background: '#2B1D14', padding: 18, boxShadow: '0 20px 40px rgba(0,0,0,0.3)'}}>
          <svg width={524} height={384} viewBox="0 0 430 400" style={{background: '#FFF6DF', borderRadius: 18}}>
            {strokes.map((s, k) => <path key={k} d={s.d} stroke={s.c} strokeWidth={24} fill="none" strokeLinecap="round" pathLength={1} strokeDasharray={`${lin(f, s.t, s.t + 26)} 1`} />)}
          </svg>
        </div>
        <Lbl t="بيترسم على برامج زي فوتوشوب 🖌️" />
      </In>
      <In at={paper} x={790} y={1180} rot={6}>
        <div style={{width: 240, height: 180, background: '#fff', boxShadow: '0 10px 24px rgba(0,0,0,0.2)', position: 'relative'}}>
          <svg width={240} height={180}><path d="M30 140 Q 90 40 200 110" stroke="#555" strokeWidth={4} fill="none" /></svg>
          <div style={{position: 'absolute', right: -20, top: -30, fontSize: 70}}>✏️</div>
        </div>
        <Lbl t="غير الورقة والقلم" size={30} />
      </In>
    </Field>
  );
};

// 13) the scarecrow's wish: "take me to the wizard.. I stood here for years, I don't learn.. he'll give me a BRAIN"
export const OzWish: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const years = at(b, 'years', 150), brain = at(b, 'brain', 380);
  return (
    <Sc>
      <Land />
      <CornField y={1080} sway={0.4} />
      <Scarecrow x={560} y={980} s={1.3} onPole talk sad={f < brain} look={-0.6} />
      <Dorothy x={200} y={1170} s={1.15} look={0.6} />
      <In at={6} out={years - 4} x={600} y={520}><Bubble w={620} h={200} tail="right"><span style={{fontSize: 46}}>ممكن تاخديني معاكي للساحر؟</span></Bubble></In>
      <In at={years} out={brain - 4} x={600} y={520}><Bubble w={680} h={220} tail="right"><span style={{fontSize: 42}}>بقالي سنين واقف.. مش بتعلّم ومش بطوّر نفسي ⏳</span></Bubble></In>
      <In at={brain} x={600} y={520}><Bubble w={560} h={200} tail="right"><span style={{fontSize: 52}}>يديني عقل 🧠</span></Bubble></In>
      <In at={brain + 8} x={700} y={780} from={0.1}><div style={{fontSize: 150, transform: `rotate(${Math.sin(f / 8) * 8}deg)`}}>🧠</div></In>
    </Sc>
  );
};

// 14) Dorothy agrees: both walk the road together; "keep walking the yellow brick road"
export const OzTogether: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const road = at(b, 'road', 220);
  return (
    <Sc>
      <Land />
      <EmeraldCity x={540} y={860} s={0.9} glow={0.6} />
      <BrickRoad vx={540} vy={860} walk />
      <Dorothy x={420} y={1120} s={1.2} walk />
      <Scarecrow x={660} y={1110} s={1.12} walk />
      <In at={6} out={road - 6} x={540} y={520}><Pill text="وكمّلوا الرحلة سوا 🤝" bg={C.a} ink="#fff" size={46} /></In>
      <In at={road} x={540} y={470}>
        <div style={{background: C.card, borderRadius: 30, padding: '20px 36px', textAlign: 'center', boxShadow: '0 14px 30px rgba(0,0,0,0.2)'}}>
          <div style={{fontFamily: AR, fontWeight: 900, fontSize: 46, color: C.ink}}>خليك فاكر..</div>
          <div style={{fontFamily: AR, fontWeight: 900, fontSize: 54, color: '#C99A1E'}}>خليك ماشي على الطريق الأصفر 🟨</div>
        </div>
      </In>
      <In at={road + 40} x={540} y={680}><Pill text="الفصل الجاي: الراجل الحديدي و الـ 3D 🤖" bg={C.ink} ink="#fff" size={36} /></In>
    </Sc>
  );
};

export const ozScenes: Record<string, React.FC<any>> = {
  oz_walk: OzWalk, oz_farm: OzFarm, oz_meet: OzMeet, oz_many: OzMany, f_uiux: FUiux, f_brand: FBrand, f_print: FPrint, f_pack: FPack,
  f_social: FSocial, f_photo: FPhoto, f_illus: FIllus, f_paint: FPaint, oz_wish: OzWish, oz_together: OzTogether,
};
