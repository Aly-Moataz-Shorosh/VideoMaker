import {staticFile} from 'remotion';
import raw from '../theme.json';

import packs from '../packs.json';

export const theme = raw;
// Mutable on purpose: a whole render uses ONE pack (set once by Edit via applyPack before children render).
export const C: Record<string, string> = {...raw.colors};
export const applyPack = (name?: string) => {
  const p = (packs as Record<string, any>)[name || 'charcoal'];
  if (p && typeof p === 'object') Object.assign(C, p);
};

// Fonts are local files in public/fonts (copied from Aly's installed fonts).
export const fontCss = `
@font-face{font-family:'Cairo';src:url('${staticFile('fonts/Cairo.ttf')}') format('truetype');font-weight:200 1000;}
@font-face{font-family:'Montserrat';src:url('${staticFile('fonts/Montserrat.ttf')}') format('truetype');font-weight:100 900;}
@font-face{font-family:'Amiri';src:url('${staticFile('fonts/Amiri.ttf')}') format('truetype');}
`;

export const isVertical = (w: number, h: number) => h > w;

export const accentColor = (a: 'gold' | 'blue' | 'red' | 'green') => C[a];
