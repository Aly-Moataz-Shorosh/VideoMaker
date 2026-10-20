import React from 'react';
import {Img, staticFile, useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {z} from 'zod';
import {Base} from '../blocks/Base';
import {C} from '../blocks/theme';
import {enter, exit, lerp} from '../blocks/anim';

// Technique from Aly's "هو ايه" series: 3D keycap button pops in tilted, gets pressed
// (sinks into its edge) -> turns grey "SUBSCRIBED", bell keycap pops and rings, signature rises.
export const subscribePressSchema = z.object({
  pressAt: z.number().default(36),
  bellAt: z.number().default(50),
  signature: z.boolean().default(true),
  platform: z.enum(['youtube', 'instagram']).default('youtube'),
  y: z.number().default(0.45), // vertical center (0..1) of the button row — clear of captions
  x: z.number().default(0.2), // horizontal center (0..1); Aly is centered -> side by default
  previewBg: z.string().default(''),
});

const EDGE = 12;

const Keycap: React.FC<{w: number; face: string; edge: string; pressed: number; children: React.ReactNode}> = ({w, face, edge, pressed, children}) => {
  const e = lerp(pressed, EDGE, 3);
  return (
    <div style={{position: 'relative', width: w, height: 96 + EDGE}}>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 96, borderRadius: 20, background: edge, boxShadow: '0 16px 30px rgba(0,0,0,0.35)'}} />
      <div style={{position: 'absolute', left: 0, right: 0, top: EDGE - e, height: 96, borderRadius: 20, background: face,
        display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: 'inset 0 3px 0 rgba(255,255,255,0.35)'}}>
        {children}
      </div>
    </div>
  );
};

export const SubscribePress: React.FC<z.infer<typeof subscribePressSchema>> = ({pressAt, bellAt, signature, platform, y, x, previewBg}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const pIn = enter(frame, fps);
  const pOut = exit(frame, durationInFrames);
  const pressed = interpolate(frame, [pressAt, pressAt + 3, pressAt + 7], [0, 1, 0.55], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const done = frame >= pressAt + 2;
  const bell = enter(frame, fps, bellAt);
  const ring = frame >= bellAt + 6 ? Math.sin((frame - bellAt) * 1.1) * 14 * Math.max(0, 1 - (frame - bellAt - 6) / 25) : 0;
  const bellOn = frame >= bellAt + 6;
  const sig = enter(frame, fps, bellAt + 14);
  const scale = Math.min(width, height) / 1080;

  return (
    <Base previewBg={previewBg}>
      <div style={{position: 'absolute', left: width * x - 400, width: 800, top: height * y - 60 * scale, display: 'flex', flexDirection: 'column', alignItems: 'center',
        transform: `scale(${scale * lerp(Math.min(pIn, pOut), 0.5, 1)}) rotate(${lerp(pIn, -8, 0)}deg)`, opacity: Math.min(1, pIn * 2) * pOut}}>
        <div style={{display: 'flex', gap: 18, direction: 'ltr', alignItems: 'flex-end'}}>
          <Keycap w={360} pressed={pressed}
            face={done ? '#E9EBEE' : platform === 'instagram' ? 'linear-gradient(90deg, #F58529, #DD2A7B, #8134AF)' : `linear-gradient(180deg, #FF3B3B, ${C.red})`}
            edge={done ? '#8A9099' : platform === 'instagram' ? '#5B1F6E' : '#8E1A1A'}>
            <span style={{fontFamily: 'Montserrat', fontWeight: 800, fontSize: done ? 34 : 40, letterSpacing: 1, color: done ? '#6B717A' : '#fff'}}>
              {platform === 'instagram' ? (done ? 'FOLLOWING' : 'FOLLOW') : done ? 'SUBSCRIBED' : 'SUBSCRIBE'}
            </span>
          </Keycap>
          {frame >= bellAt ? (
            <div style={{transform: `scale(${bell})`}}>
              <Keycap w={110} pressed={bellOn ? 0.55 : 0} face="#E9EBEE" edge="#8A9099">
                <svg width="54" height="54" viewBox="0 0 24 24" style={{transform: `rotate(${ring}deg)`}}>
                  <defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#FF8A3D" /><stop offset="1" stopColor={C.red} /></linearGradient></defs>
                  <path d="M12 2a1.5 1.5 0 0 1 1.5 1.5v.6A6.5 6.5 0 0 1 18.5 10.5v4l2 2.5v1H3.5v-1l2-2.5v-4A6.5 6.5 0 0 1 10.5 4.1v-.6A1.5 1.5 0 0 1 12 2zm-2 18h4a2 2 0 0 1-4 0z"
                    fill={bellOn ? 'url(#bg)' : '#2B2F36'} />
                  {bellOn ? <path d="M3 7.5C3.6 5.4 4.8 3.8 6.3 2.8M21 7.5c-.6-2.1-1.8-3.7-3.3-4.7" stroke={C.red} strokeWidth="1.6" fill="none" strokeLinecap="round" /> : null}
                </svg>
              </Keycap>
            </div>
          ) : null}
        </div>
        {signature ? (
          <Img src={staticFile('brand/signature-calligraphy.png')} style={{width: 300, marginTop: 26, opacity: sig,
            transform: `translateY(${lerp(sig, 30, 0)}px)`, filter: 'invert(1) sepia(1) saturate(4) hue-rotate(-10deg) brightness(1.05) drop-shadow(0 3px 6px rgba(0,0,0,0.6))'}} />
        ) : null}
      </div>
    </Base>
  );
};
