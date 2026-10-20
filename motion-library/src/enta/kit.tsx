import React from 'react';
import {Img, staticFile} from 'remotion';

// Show "انت بتشتغل ايه" kit (docs/22): Aly's styles.png look — flat hand-drawn stickers with a white outline,
// muted orange / blue / olive / mustard on dark, blue paper speech bubbles, cut-out photos with a white border,
// masking tape, film grain. Stickers = real crops of his sheet (public/enta/<name>.png, 3x upscaled).
export const E = {
  orange: '#E0642E', blue: '#5C8BC0', olive: '#8E9A5B', mustard: '#E8B54A',
  ink: '#1C2030', paper: '#EFE6D2', bluePaper: '#A9C6E4', white: '#FBF7EE',
};
export const accentOf = (a: string) => (E as Record<string, string>)[a] ?? E.orange;

// Sticker from Aly's sheet. size = width px.
export const Sticker: React.FC<{name: string; size: number; style?: React.CSSProperties}> = ({name, size, style}) => (
  <Img src={staticFile(`enta/${name}.png`)} style={{width: size, height: 'auto', filter: 'drop-shadow(0 6px 10px rgba(0,0,0,.45))', ...style}} />
);

// Paper grain (SVG noise) laid over cards so they never look flat/digital.
export const Grain: React.FC<{opacity?: number; seed?: number}> = ({opacity = 0.35, seed = 3}) => (
  <svg style={{position: 'absolute', inset: 0, width: '100%', height: '100%', mixBlendMode: 'multiply', opacity, pointerEvents: 'none'}}>
    <filter id={`g${seed}`}>
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={seed} />
      <feColorMatrix values="0 0 0 0 0.35  0 0 0 0 0.3  0 0 0 0 0.25  0 0 0 1.4 -0.35" />
    </filter>
    <rect width="100%" height="100%" filter={`url(#g${seed})`} />
  </svg>
);

// Masking tape strip (his sheet: cream / olive).
export const Tape: React.FC<{w: number; rot?: number; olive?: boolean; style?: React.CSSProperties}> = ({w, rot = -4, olive, style}) => (
  <Img src={staticFile(`enta/${olive ? 'tape_olive' : 'tape_cream'}.png`)}
    style={{position: 'absolute', width: w, transform: `rotate(${rot}deg)`, opacity: 0.95, ...style}} />
);

// "text with *highlight*" -> highlighted part in the accent color.
export const Hi: React.FC<{text: string; color: string}> = ({text, color}) => (
  <>
    {text.split(/(\*[^*]+\*)/g).map((p, i) =>
      p.startsWith('*') ? <span key={i} style={{color}}>{p.slice(1, -1)}</span> : <span key={i}>{p}</span>)}
  </>
);

// Sticker outline used on cards/photos: white border + dark hairline + soft shadow (like his sheet).
export const stickerBorder = (px = 8): React.CSSProperties => ({
  border: `${px}px solid ${E.white}`, outline: `2px solid rgba(20,20,30,.55)`,
  boxShadow: '0 14px 30px rgba(0,0,0,.5)',
});
