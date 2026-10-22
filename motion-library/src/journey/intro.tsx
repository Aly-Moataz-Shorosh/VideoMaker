import React from 'react';
import {AbsoluteFill, Img, useCurrentFrame} from 'remotion';
import {AR, grad, In, JY, lin, logo, Pill, Sc, spr} from './kit';

// Short 1 = the project's intro video (playlist 01): the "lost" phase, the map seen from above the planet, the 3 stages.
const C = JY.huwa;
type B = Record<string, number>;
const at = (b: B, k: string, d = 0) => b[k] ?? d;
const Card: React.FC<{t: string; size?: number}> = ({t, size = 46}) => (
  <div style={{background: '#fff', borderRadius: 30, padding: '16px 34px', fontFamily: AR, fontWeight: 900, fontSize: size, color: C.ink, boxShadow: '0 14px 30px rgba(0,0,0,0.15)', direction: 'rtl', textAlign: 'center'}}>{t}</div>
);

// the maze of the beginner: a little person tries paths, question chips pop
export const IMaze: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const qs = [['q1', '🖥️ أنهي برنامج؟'], ['q2', '💼 سوق العمل شغال ازاي؟'], ['q3', '📖 المصطلحات دي يعني ايه؟']];
  const walls = ['M100 0 V400', 'M200 100 V500', 'M300 0 V300', 'M400 200 V500', 'M0 200 H150', 'M250 400 H500', 'M300 300 H450', 'M100 100 H250'];
  const path = [[50, 450], [50, 250], [150, 250], [150, 450], [250, 450], [250, 150], [350, 150], [350, 50], [450, 50], [450, 150]];
  const u = (f / 18) % (path.length - 1); const i = Math.floor(u), k = u - i;
  const px = path[i][0] + (path[i + 1][0] - path[i][0]) * k, py = path[i][1] + (path[i + 1][1] - path[i][1]) * k;
  return (
    <Sc>
      <In at={0} x={540} y={400}><Card t="مرحلة «التطبيش» 🌀" size={54} /></In>
      <In at={4} x={540} y={830}>
        <svg width={620} height={620} viewBox="-10 -10 520 520" style={{background: '#fff', borderRadius: 30, boxShadow: '0 20px 40px rgba(0,0,0,0.15)'}}>
          <rect x={0} y={0} width={500} height={500} fill="none" stroke={C.ink} strokeWidth={10} />
          {walls.map((d, j) => <path key={j} d={d} stroke={C.ink} strokeWidth={10} strokeLinecap="round" />)}
          <circle cx={px} cy={py} r={22} fill={C.a} /><text x={px} y={py - 30} textAnchor="middle" fontSize={30}>❓</text>
        </svg>
      </In>
      {qs.map(([key, t], j) => <In key={key} at={at(b, key, 40 + j * 30)} x={540} y={1210 + j * 0} out={j < 2 ? at(b, qs[j + 1][0], 9999) : undefined}><Pill text={t} bg={grad('huwa')} ink="#fff" size={42} /></In>)}
      <In at={at(b, 'all', 9999)} x={540} y={1300}><Pill text="كلنا مرّينا بالمرحلة دي 🤝" size={40} /></In>
    </Sc>
  );
};

// get above the planet of graphics and look at the map
export const IPlanet: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const map = at(b, 'map', 90), me = at(b, 'me', 300);
  const r = 230, rot = f * 1.2;
  const conts = [[-60, -40, 70, 40], [50, 10, 60, 90], [-20, 90, 50, 30], [80, -90, 40, 30]];
  return (
    <Sc>
      <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 45%, #2A2F4A 0%, #121528 70%)'}} />
      {Array.from({length: 40}, (_, i) => <div key={i} style={{position: 'absolute', left: (i * 263) % 1080, top: 300 + (i * 151) % 1200, width: 4, height: 4, borderRadius: 2, background: '#fff', opacity: 0.4 + 0.6 * Math.abs(Math.sin(f / 20 + i))}} />)}
      <In at={0} x={540} y={400}><div style={{fontFamily: AR, fontWeight: 900, fontSize: 52, color: '#fff', direction: 'rtl'}}>اطلع فوق كوكب الجرافيكس 🪐</div></In>
      <div style={{position: 'absolute', left: 540 - r, top: 720 - r, width: 2 * r, height: 2 * r, borderRadius: '50%', overflow: 'hidden', background: 'radial-gradient(circle at 35% 30%, #5AB0F0, #1E5BD8 70%)', boxShadow: '0 0 60px rgba(90,176,240,0.5)', transform: `scale(${1 - 0.35 * lin(f, map, map + 20)})`}}>
        {conts.map(([x, y, w, h], i) => <div key={i} style={{position: 'absolute', left: r + ((x + rot) % 520 + 520) % 520 - 260 - w / 2, top: r + y - h / 2, width: w * 1.6, height: h * 1.6, borderRadius: '45%', background: '#3FAE5A'}} />)}
      </div>
      {f >= map ? (
        <In at={map} x={540} y={1080}>
          <svg width={760} height={360} viewBox="0 0 760 360" style={{background: '#F3EEE2', borderRadius: 16, boxShadow: '0 20px 40px rgba(0,0,0,0.4)'}}>
            <path d="M40 300 Q 200 80 380 200 T 720 80" stroke="#C99A1E" strokeWidth={10} fill="none" strokeDasharray="20 14" pathLength={1} strokeDashoffset={1 - lin(f, map, map + 60)} />
            {[[80, 280, '🏙️'], [380, 200, '🏔️'], [700, 90, '🏝️']].map(([x, y, e], i) => <text key={i} x={x as number} y={y as number} fontSize={50} textAnchor="middle">{e}</text>)}
            <text x={380} y={340} textAnchor="middle" fontFamily="Cairo" fontWeight={900} fontSize={34} fill="#2B1D14">الطرق • البلاد • القارات • البحار</text>
          </svg>
        </In>
      ) : null}
      <In at={me} x={540} y={1320}><Pill text="وأنا رسمت لك الخريطة دي 🗺️" bg={grad('huwa')} ink="#fff" size={44} /></In>
    </Sc>
  );
};

// the 3 stages of the map, his three logos light up on his words, then the project's name
export const IStages: React.FC<{b?: B}> = ({b = {}}) => {
  const f = useCurrentFrame();
  const st = [{k: 'one', logo: 'huwa.png', t: 'المصطلحات', sub: '30 فيديو • "هو ايه"', h: 130}, {k: 'two', logo: 'oz.png', t: 'المجالات', sub: '5 فيديوهات • ساحر أوز', h: 170},
              {k: 'three', logo: 'prog.png', t: 'البرامج', sub: 'فيديو واحد • شجرة البرامج', h: 120}];
  const name = at(b, 'name', 9999);
  return (
    <Sc>
      <In at={0} x={540} y={400}><Card t="الخريطة = 3 مراحل 🗺️" size={54} /></In>
      {st.map((x, i) => {
        const a = at(b, x.k, 30 + i * 90), on = f >= a;
        return (
          <div key={x.k} style={{position: 'absolute', left: 90, right: 90, top: 520 + i * 250, height: 220, borderRadius: 30, background: on ? '#fff' : 'rgba(255,255,255,0.4)', display: 'flex', alignItems: 'center', gap: 30,
            padding: '0 34px', direction: 'rtl', boxShadow: on ? '0 16px 34px rgba(0,0,0,0.15)' : undefined, border: on ? `6px solid ${C.a}` : '6px solid transparent', boxSizing: 'border-box',
            transform: `scale(${on ? 0.92 + 0.08 * spr(f, 30, a) : 0.92})`}}>
            <div style={{fontFamily: 'Montserrat', fontWeight: 900, fontSize: 80, color: on ? C.a : '#999'}}>{i + 1}</div>
            <Img src={logo(x.logo)} style={{height: x.h * 0.8, filter: on ? undefined : 'grayscale(1)', opacity: on ? 1 : 0.5}} />
            <div><div style={{fontFamily: AR, fontWeight: 900, fontSize: 50, color: C.ink}}>{x.t}</div><div style={{fontFamily: AR, fontWeight: 800, fontSize: 30, color: C.soft}}>{x.sub}</div></div>
          </div>
        );
      })}
      <In at={name} x={540} y={1320}><Pill text="مشروع: رحلة إلى مركز الجرافيكس 🚀" bg={grad('huwa')} ink="#fff" size={42} /></In>
    </Sc>
  );
};

export const introScenes: Record<string, React.FC<any>> = {i_maze: IMaze, i_planet: IPlanet, i_stages: IStages};
