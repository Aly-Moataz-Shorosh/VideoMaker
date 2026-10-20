import React from 'react';
import world from '../data/world.json';

// World map from Natural Earth 1:50m (public domain), equirectangular: x = (lon+180)/360*3600, y = (90-lat)/180*1800.
// Keys = ISO A3 codes (EGY, CHN, USA ...). Built by a small script (see docs/17).
export const GEO = world as {w: number; h: number; c: Record<string, string>};
export const lonLat = (lon: number, lat: number): [number, number] => [((lon + 180) / 360) * GEO.w, ((90 - lat) / 180) * GEO.h];

type Ring = [number, number][];
const cache: Record<string, Ring[]> = {};
export const rings = (iso: string): Ring[] => {
  if (!cache[iso]) {
    cache[iso] = (GEO.c[iso] || '').split('M').filter(Boolean).map((r) =>
      r.replace('Z', '').split('L').map((p) => p.split(',').map(Number) as [number, number]));
  }
  return cache[iso];
};

const inRing = (x: number, y: number, r: Ring) => {
  let inside = false;
  for (let i = 0, j = r.length - 1; i < r.length; j = i++) {
    const [xi, yi] = r[i], [xj, yj] = r[j];
    if (yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) inside = !inside;
  }
  return inside;
};
export const inCountry = (iso: string, x: number, y: number) => rings(iso).some((r) => inRing(x, y, r));

// Grid points inside a country (map units), roughly `n` of them, shuffled with a fixed seed (stable renders).
export const fillPoints = (iso: string, n: number): [number, number][] => {
  const rs = rings(iso);
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
  rs.forEach((r) => r.forEach(([x, y]) => {x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y);}));
  let step = Math.sqrt(((x1 - x0) * (y1 - y0)) / n), pts: [number, number][] = [];
  for (let k = 0; k < 12; k++) {
    pts = [];
    for (let y = y0 + step / 2, row = 0; y < y1; y += step * 0.9, row++)
      for (let x = x0 + step / 2 + (row % 2) * step * 0.5; x < x1; x += step) if (inCountry(iso, x, y)) pts.push([x, y]);
    if (Math.abs(pts.length - n) <= n * 0.06) break;
    step *= Math.sqrt(pts.length / n);
  }
  let s = 7;
  const rnd = () => ((s = (s * 16807) % 2147483647) / 2147483647);
  return pts.map((p) => [p, rnd()] as const).sort((a, b) => a[1] - b[1]).map((a) => a[0]);
};

// Countries as SVG paths. fill/stroke per iso via `style(iso)`; default = muted land.
export const MapPaths: React.FC<{only?: string[]; style: (iso: string) => React.SVGProps<SVGPathElement>}> = ({only, style}) => (
  <>
    {Object.keys(GEO.c).filter((k) => !only || only.includes(k)).map((k) => <path key={k} d={GEO.c[k]} {...style(k)} />)}
  </>
);

// Statistics-Easy-Learn style pictogram person (map units). armsUp 0..1, look -1..1 (eyes turn), laptop 0..1.
export const Person: React.FC<{x: number; y: number; s: number; color: string; armsUp?: number; look?: number;
  laptop?: number; dim?: number; screen?: string}> = ({x, y, s, color, armsUp = 0, look = 0, laptop = 0, dim = 0, screen = '#3BA9F5'}) => {
  const a = (-30 + armsUp * 110) * (Math.PI / 180); // 0 = arms down, 1 = raised
  const arm = (side: number) => {
    const sx = x + side * s * 0.32, sy = y - s * 0.55;
    const ang = side > 0 ? a : Math.PI - a;
    return <line x1={sx} y1={sy} x2={sx + Math.cos(ang) * s * 0.55} y2={sy - Math.sin(ang) * s * 0.55}
      stroke={color} strokeWidth={s * 0.17} strokeLinecap="round" />;
  };
  return (
    <g opacity={1 - dim * 0.55}>
      {armsUp > 0.02 ? <>{arm(1)}{arm(-1)}</> : null}
      <path d={`M${x - s * 0.36},${y} L${x - s * 0.36},${y - s * 0.5} Q${x - s * 0.36},${y - s * 0.72} ${x - s * 0.14},${y - s * 0.72}
        L${x + s * 0.14},${y - s * 0.72} Q${x + s * 0.36},${y - s * 0.72} ${x + s * 0.36},${y - s * 0.5} L${x + s * 0.36},${y} Z`} fill={color} />
      <circle cx={x} cy={y - s * 0.98} r={s * 0.22} fill={color} />
      <circle cx={x - s * 0.08 + look * s * 0.08} cy={y - s * 1.0} r={s * 0.04} fill="#14181F" />
      <circle cx={x + s * 0.08 + look * s * 0.08} cy={y - s * 1.0} r={s * 0.04} fill="#14181F" />
      {laptop > 0.01 ? (
        <g transform={`translate(${x},${y - s * 0.12}) scale(${laptop})`}>
          <rect x={-s * 0.42} y={-s * 0.42} width={s * 0.84} height={s * 0.5} rx={s * 0.05} fill="#2B313C" stroke="#C9D1DC" strokeWidth={s * 0.04} />
          <rect x={-s * 0.34} y={-s * 0.35} width={s * 0.68} height={s * 0.36} fill={screen} opacity={0.9} />
          <rect x={-s * 0.55} y={s * 0.06} width={s * 1.1} height={s * 0.09} rx={s * 0.04} fill="#C9D1DC" />
        </g>
      ) : null}
    </g>
  );
};
