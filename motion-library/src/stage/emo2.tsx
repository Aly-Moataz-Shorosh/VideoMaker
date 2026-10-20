import React from 'react';
import {Easing, useCurrentFrame, useVideoConfig} from 'remotion';
import {AR, bi, EN, L, lin, S, spr, W} from './kit';
import {Actor, Soft} from './emo';

const bt = (b: Record<string, number> | undefined, k: string, fps: number, d = 0) => Math.round((b?.[k] ?? d) * fps);
const out = (f: number, dur: number) => 1 - lin(f, dur - 7, dur);

// ---------- steps: deleting an account = a phone that keeps throwing dialogs, the step counter runs to 16 ----------
const DIALOGS = ['متأكد إنك عايز تمشي؟', 'ليه؟ جاوب الاستبيان 📝', 'استنى! خصم خاص ليك 🎁', 'هتفقد كل حاجة 😢', 'اكتب الباسورد تاني', 'آخر فرصة…'];
export const Steps: React.FC<{dur: number; b?: Record<string, number>}> = ({dur, b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const ks = [bt(b, 's1', fps, 0.3), bt(b, 's2', fps, 1), bt(b, 's3', fps, 2), bt(b, 's4', fps, 3), bt(b, 's4', fps, 3) + 12, bt(b, 's4', fps, 3) + 24];
  const kEnd = bt(b, 'end', fps, 5);
  const n = Math.min(16, Math.max(1, Math.round(lin(f, ks[0], kEnd, 1, 16, Easing.linear))));
  const p = spr(f, fps, 0, 150, 15);
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: W, height: 1920, opacity: out(f, dur)}}>
      {/* phone */}
      <div style={{position: 'absolute', left: 120, top: L.stageTop + 10, width: 420, height: 800, borderRadius: 60, background: 'linear-gradient(160deg, #20263E, #0E1222)',
        border: '10px solid #2B3354', boxShadow: '0 40px 80px rgba(0,0,0,0.5)', transform: `scale(${0.85 + 0.15 * p})`, overflow: 'hidden'}}>
        <div style={{position: 'absolute', left: 150, top: 14, width: 100, height: 22, borderRadius: 11, background: '#05070D'}} />
        <div style={{position: 'absolute', left: 30, right: 30, top: 70, fontFamily: AR, fontWeight: 900, fontSize: 34, color: S.soft, direction: 'rtl'}}>الإعدادات › الحساب</div>
        {DIALOGS.map((t, i) => {
          const q = spr(f, fps, ks[i], 220, 15);
          return f < ks[i] ? null : (
            <div key={i} style={{position: 'absolute', left: 26 + i * 6, right: 26 - i * 6, top: 150 + i * 92, padding: '16px 18px', borderRadius: 24, background: '#F4F6FB',
              boxShadow: '0 14px 30px rgba(0,0,0,0.35)', fontFamily: AR, fontWeight: 900, fontSize: 30, color: '#1A1F33', direction: 'rtl',
              transform: `scale(${0.6 + 0.4 * q})`, opacity: q}}>{t}
              <div style={{display: 'flex', gap: 10, marginTop: 10}}>
                <span style={{flex: 1, textAlign: 'center', background: S.blue, color: '#fff', borderRadius: 14, padding: '4px 0', fontSize: 24}}>رجوع</span>
                <span style={{flex: 1, textAlign: 'center', background: '#E3E6EF', color: '#677', borderRadius: 14, padding: '4px 0', fontSize: 20}}>متابعة</span>
              </div>
            </div>
          );
        })}
      </div>
      {/* the counter */}
      <div style={{position: 'absolute', left: 590, top: L.stageTop + 120, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6}}>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 52, color: S.soft}}>خطوة</div>
        <div style={{fontFamily: EN, fontWeight: 900, fontSize: 230, lineHeight: 1, color: n >= 16 ? S.red : '#fff', textShadow: `0 0 50px ${n >= 16 ? S.red : S.violet}88`,
          transform: `scale(${1 + 0.08 * Math.max(0, Math.sin(f / 2)) * (n < 16 ? 1 : 0)})`}}>{n}</div>
        <div style={{fontFamily: AR, fontWeight: 900, fontSize: 44, color: '#fff'}}>علشان تمسح الأكاونت</div>
        {f > kEnd ? <div style={{marginTop: 20}}><Actor e="face_with_steam_from_nose" s={200} at={kEnd} /></div> : null}
      </div>
    </div>
  );
};

// ---------- T-shaped: the bar = a bit of everything, the stem = everything about one thing ----------
const BAR = ['mobile_phone', 'robot', 'globe_with_meridians', 'artist_palette', 'joystick', 'bar_chart'];
export const TShape: React.FC<{dur: number; b?: Record<string, number>}> = ({dur, b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const kTop = bt(b, 'top', fps, 0.5), kDeep = bt(b, 'deep', fps, 2.5);
  const x0 = 90, cell = 150;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: W, height: 1920, opacity: out(f, dur)}}>
      <div style={{position: 'absolute', left: 0, right: 0, top: L.stageTop - 10, textAlign: 'center', fontFamily: EN, fontWeight: 900, fontSize: 90, color: S.yellow,
        opacity: spr(f, fps, 0, 200, 14)}}>T-shaped</div>
      {BAR.map((e, i) => {
        const k = kTop + i * 3;
        const p = spr(f, fps, k, 200, 13);
        return <div key={i} style={{position: 'absolute', left: x0 + i * cell, top: L.stageTop + 110, width: cell - 12, height: cell - 12, borderRadius: 28, background: 'rgba(255,255,255,0.08)',
          border: '2px solid rgba(255,255,255,0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: p, transform: `scale(${0.5 + 0.5 * p})`}}>
          <Actor e={e} s={110} at={k} /></div>;
      })}
      <div style={{position: 'absolute', left: 0, right: 0, top: L.stageTop + 270, textAlign: 'center', fontFamily: AR, fontWeight: 900, fontSize: 46, color: '#fff',
        opacity: lin(f, kTop + 10, kTop + 20)}}>حاجة صغيرة من كل حاجة</div>
      {[0, 1, 2].map((j) => {
        const k = kDeep + j * 4;
        const p = spr(f, fps, k, 200, 13);
        return <div key={j} style={{position: 'absolute', left: x0 + 2.5 * cell - 6, top: L.stageTop + 340 + j * 150, width: cell + 12, height: cell - 12, borderRadius: 28,
          background: `linear-gradient(160deg, ${S.violet}, ${S.blue})`, opacity: p, transform: `scaleY(${p})`, boxShadow: `0 0 40px ${S.violet}66`,
          display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{j === 1 ? <Actor e="laptop" s={110} at={k} /> : null}</div>;
      })}
      <div style={{position: 'absolute', left: 620, top: L.stageTop + 520, width: 360, fontFamily: AR, fontWeight: 900, fontSize: 46, color: S.yellow, direction: 'rtl',
        opacity: lin(f, kDeep + 12, kDeep + 22)}}>وحاجة واحدة تعرف عنها كل حاجة</div>
    </div>
  );
};

// ---------- connect the dots (Steve Jobs): dots appear on beats, then a line links them looking BACK ----------
const DOTS = [{x: 820, y: 230, e: 'graduation_cap', t: 'كورس النهارده'}, {x: 520, y: 520, e: 'artist_palette', t: 'جرافيكس'}, {x: 220, y: 300, e: 'briefcase', t: 'شغلك بعدين'}];
export const Dots: React.FC<{dur: number; b?: Record<string, number>}> = ({dur, b}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const ks = [bt(b, 'd1', fps, 0.3), bt(b, 'd2', fps, 1.3), bt(b, 'd3', fps, 2.3)], kL = bt(b, 'link', fps, 4);
  const pl = lin(f, kL, kL + 30, 0, 1, Easing.inOut(Easing.cubic));
  const y0 = L.stageTop + 20;
  const path = `M ${DOTS[2].x} ${DOTS[2].y + y0} Q 380 ${y0 + 620} ${DOTS[1].x} ${DOTS[1].y + y0} T ${DOTS[0].x} ${DOTS[0].y + y0}`;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: W, height: 1920, opacity: out(f, dur)}}>
      <svg width={W} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
        <path d={path} stroke={S.yellow} strokeWidth={12} fill="none" strokeLinecap="round" strokeDasharray={1600} strokeDashoffset={1600 * (1 - pl)}
          style={{filter: `drop-shadow(0 0 14px ${S.yellow})`}} />
      </svg>
      {DOTS.map((d, i) => (
        <div key={i} style={{position: 'absolute', left: d.x - 110, top: y0 + d.y - 120, width: 220, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
          <Soft w={200} h={200} glow={S.yellow} style={{display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: spr(f, fps, ks[i], 200, 13)}}>
            <Actor e={d.e} s={150} at={ks[i]} /></Soft>
          <div style={{marginTop: 10, fontFamily: AR, fontWeight: 900, fontSize: 40, color: '#fff', direction: 'rtl', opacity: lin(f, ks[i] + 6, ks[i] + 14)}}>{bi(d.t)}</div>
        </div>
      ))}
      <div style={{position: 'absolute', left: 0, right: 0, top: y0 + 700, textAlign: 'center', fontFamily: AR, fontWeight: 900, fontSize: 52, color: S.yellow, direction: 'rtl',
        opacity: lin(f, kL + 20, kL + 32)}}>النقط بتتوصل وإنت باصص لورا</div>
    </div>
  );
};
