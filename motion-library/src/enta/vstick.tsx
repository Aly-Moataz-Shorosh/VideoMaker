import React from 'react';

// VECTOR stickers for the show (Aly 2026-10-13: the PNG stickers = 3x upscales of tiny crops -> pixelated; "no pixelated graphics").
// Same look as his styles sheet: flat muted fill, dark ink outline, thick white sticker border, soft shadow. 100x100 viewBox.
// Sticker() in kit.tsx uses these first and falls back to the PNG only for names that have no vector yet.
const O = '#E0642E', B = '#5C8BC0', G = '#8E9A5B', Y = '#E8B54A', INK = '#1C2030', W = '#FBF7EE';

type Shape = {d: string; fill: string; ink?: number};
const star = (cx: number, cy: number, r1: number, r2: number, n: number, rot = -90) => {
  let d = '';
  for (let i = 0; i < n * 2; i++) {
    const r = i % 2 ? r2 : r1, a = ((rot + (i * 180) / n) * Math.PI) / 180;
    d += `${i ? 'L' : 'M'}${(cx + r * Math.cos(a)).toFixed(1)} ${(cy + r * Math.sin(a)).toFixed(1)} `;
  }
  return d + 'Z';
};
const spark = (c: string): Shape[] => [{d: 'M50 6 C54 36 64 46 94 50 C64 54 54 64 50 94 C46 64 36 54 6 50 C36 46 46 36 50 6Z', fill: c}];

export const VEC: Record<string, Shape[]> = {
  bug: [
    {d: 'M30 30 L18 18 M70 30 L82 18 M22 52 L6 50 M78 52 L94 50 M24 70 L10 82 M76 70 L90 82', fill: 'none', ink: 6},
    {d: 'M50 26 C72 26 80 46 80 62 C80 80 66 92 50 92 C34 92 20 80 20 62 C20 46 28 26 50 26Z', fill: O},
    {d: 'M50 12 C62 12 68 20 68 30 L32 30 C32 20 38 12 50 12Z', fill: INK},
    {d: 'M50 32 L50 90', fill: 'none', ink: 4},
    {d: 'M34 50 a5 5 0 1 0 0.1 0Z M64 46 a6 6 0 1 0 0.1 0Z M38 72 a4 4 0 1 0 0.1 0Z M64 72 a5 5 0 1 0 0.1 0Z', fill: INK},
  ],
  brace_l: [{d: 'M66 8 C44 8 40 16 40 30 L40 40 C40 46 34 50 24 50 C34 50 40 54 40 60 L40 70 C40 84 44 92 66 92 L66 80 C56 80 54 78 54 68 L54 58 C54 54 50 50 46 50 C50 50 54 46 54 42 L54 32 C54 22 56 20 66 20Z', fill: B}],
  brace_r: [{d: 'M34 8 C56 8 60 16 60 30 L60 40 C60 46 66 50 76 50 C66 50 60 54 60 60 L60 70 C60 84 56 92 34 92 L34 80 C44 80 46 78 46 68 L46 58 C46 54 50 50 54 50 C50 50 46 46 46 42 L46 32 C46 22 44 20 34 20Z', fill: B}],
  zero: [{d: 'M50 8 C74 8 84 28 84 50 C84 72 74 92 50 92 C26 92 16 72 16 50 C16 28 26 8 50 8Z M50 24 C38 24 32 34 32 50 C32 66 38 76 50 76 C62 76 68 66 68 50 C68 34 62 24 50 24Z', fill: G}],
  one: [{d: 'M44 8 L60 8 L60 78 L74 78 L74 92 L28 92 L28 78 L44 78 L44 30 L30 36 L26 24Z', fill: Y}],
  floppy: [
    {d: 'M12 12 L76 12 L90 26 L90 88 L12 88Z', fill: B},
    {d: 'M28 12 L68 12 L68 38 L28 38Z', fill: W},
    {d: 'M56 17 L63 17 L63 33 L56 33Z', fill: INK},
    {d: 'M24 54 L78 54 L78 88 L24 88Z', fill: W},
    {d: 'M32 64 L70 64 M32 74 L62 74', fill: 'none', ink: 4},
  ],
  qmark: [
    {d: 'M24 34 C24 16 38 6 52 6 C70 6 80 18 80 32 C80 46 70 52 62 58 C58 61 58 64 58 70 L42 70 C42 60 44 54 52 48 C60 42 64 38 64 32 C64 26 60 20 52 20 C44 20 40 26 40 34Z', fill: O},
    {d: 'M50 76 a9 9 0 1 0 0.1 0Z', fill: O},
  ],
  burst: [{d: star(50, 50, 46, 26, 12), fill: Y}],
  star_y: [{d: star(50, 52, 46, 20, 5), fill: Y}],
  star8_b: [{d: star(50, 50, 46, 24, 8, -90), fill: B}],
  star_line: [{d: star(50, 52, 44, 19, 5), fill: G}],
  spark_o: spark(O), spark_b: spark(B), spark_g: spark(G), spark_y: spark(Y), spark_g2: spark(G),
  check: [{d: 'M10 54 L26 38 L42 54 L76 16 L92 32 L42 86Z', fill: G}],
  cross: [{d: 'M14 30 L30 14 L50 34 L70 14 L86 30 L66 50 L86 70 L70 86 L50 66 L30 86 L14 70 L34 50Z', fill: O}],
  arrow_y: [{d: 'M6 44 L62 44 L62 24 L96 52 L62 80 L62 60 L6 60Z', fill: Y}],
  arrow_b: [{d: 'M6 44 L62 44 L62 24 L96 52 L62 80 L62 60 L6 60Z', fill: B}],
  arrow_g: [{d: 'M6 44 L62 44 L62 24 L96 52 L62 80 L62 60 L6 60Z', fill: G}],
  onair: [
    {d: 'M6 26 Q6 18 14 18 L86 18 Q94 18 94 26 L94 74 Q94 82 86 82 L14 82 Q6 82 6 74Z', fill: O},
  ],
};

export const VSticker: React.FC<{name: string; size: number; style?: React.CSSProperties}> = ({name, size, style}) => {
  const sh = VEC[name];
  return (
    <svg width={size} height={name === 'onair' ? size * 0.7 : size} viewBox={name === 'onair' ? '-10 8 120 84' : '-10 -10 120 120'} style={{overflow: 'visible', filter: 'drop-shadow(0 6px 10px rgba(0,0,0,.45))', ...style}}>
      {/* white sticker border: every shape stroked wide in white, under everything */}
      {sh.map((s, i) => <path key={'w' + i} d={s.d} fill={s.fill === 'none' ? 'none' : W} stroke={W} strokeWidth={(s.ink ?? 0) + 14} strokeLinejoin="round" strokeLinecap="round" />)}
      {sh.map((s, i) => s.fill === 'none'
        ? <path key={i} d={s.d} fill="none" stroke={INK} strokeWidth={s.ink ?? 4} strokeLinecap="round" />
        : <path key={i} d={s.d} fill={s.fill} stroke={INK} strokeWidth={3} strokeLinejoin="round" fillRule="evenodd" />)}
      {name === 'onair' ? <text x={50} y={60} textAnchor="middle" fontSize={26} fontWeight={900} fill={W} fontFamily="Montserrat">ON AIR</text> : null}
    </svg>
  );
};
