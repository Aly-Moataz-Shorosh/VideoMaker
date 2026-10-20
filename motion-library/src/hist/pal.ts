// "History of communication" look (historyOfGraphics 2026-10-10). Aly's references: Ancient Egyptian Kit + Egyptian Stories
// opener (flat geometric shapes, warm ochre / plum / terracotta, paper grain, side-scrolling camera with blurred foreground),
// Mazepa (painted landscape pan), Tamim (one continuous travelling floor), Russia infographic (small round photo circles).
export const H = {
  ink: '#24151F', plum: '#3A2340', plum2: '#2A1830', plum3: '#55385A',
  terra: '#B4512F', terra2: '#8F3A22', rust: '#D06A3A',
  cream: '#F6E7C8', cream2: '#E9D3A6', paper: '#F1DEB6',
  gold: '#F2B531', yellow: '#FFD65A', red: '#C8372D',
  navy: '#2E3A6B', teal: '#2F8C88', teal2: '#1F6663', blue: '#5B8DB8',
  sand: '#E7B86F', sand2: '#D49A55', sand3: '#C4823F',
  soil1: '#7A4330', soil2: '#5E3324', soil3: '#46261C', soil4: '#2F1914',
  stone: '#D9C29A', stone2: '#B89D72', stone3: '#8E7552',
  skin: '#C98552', skin2: '#A9663A', skin3: '#E0A36E',
  wood: '#8A5530', wood2: '#6B3F22',
  green: '#5E8A4A', green2: '#3F6B38',
};

// Sky colours along the timeline (world x): dawn at the caves -> bright Egypt -> dusk Baghdad -> blue modern.
export const SKY: [number, string, string][] = [
  [0, '#F4C9A0', '#E89A72'],
  [2300, '#F5D3A0', '#E8A061'],
  [4500, '#F7DDA6', '#EBA85A'],
  [7600, '#F6D7A4', '#E59A5E'],
  [9900, '#EFB98E', '#B86C6A'],
  [11200, '#E9C9A0', '#C98A64'],
  [12400, '#BFD3DE', '#7FA2C2'],
  [14200, '#A9C6DE', '#5E86B6'],
];

const hex = (c: string) => [1, 3, 5].map((i) => parseInt(c.slice(i, i + 2), 16));
export const mix = (a: string, b: string, u: number) => {
  const A = hex(a), B = hex(b);
  return '#' + A.map((v, i) => Math.round(v + (B[i] - v) * u).toString(16).padStart(2, '0')).join('');
};
export const skyAt = (x: number) => {
  let i = 0;
  while (i < SKY.length - 1 && x > SKY[i + 1][0]) i++;
  const a = SKY[i], b = SKY[Math.min(i + 1, SKY.length - 1)];
  const u = a === b ? 0 : Math.max(0, Math.min(1, (x - a[0]) / (b[0] - a[0])));
  return [mix(a[1], b[1], u), mix(a[2], b[2], u)];
};

// Stations along the timeline (world x of their centre) + year label on the ruler.
export const ST: Record<string, {x: number; year: string; name: string}> = {
  weak: {x: -700, year: 'من 300,000 سنة', name: 'الإنسان'},
  speech: {x: 600, year: 'ما قبل التاريخ', name: 'الكلام'},
  village: {x: 1450, year: 'حضارات منطوقة', name: 'حضارات من غير كتابة'},
  cave: {x: 2350, year: '40,000 ق.م', name: 'رسومات الكهف'},
  sumer: {x: 3450, year: '3200 ق.م', name: 'الكتابة السومرية'},
  egypt: {x: 4550, year: '3100 ق.م', name: 'الهيروغليفي'},
  pyramids: {x: 5650, year: '2560 ق.م', name: 'الأهرامات'},
  china: {x: 6750, year: '1200 ق.م', name: 'الكتابة الصينية'},
  rome: {x: 7800, year: '100 م', name: 'اللاتيني'},
  paper: {x: 8900, year: '105 م', name: 'الورق'},
  baghdad: {x: 10050, year: '830 م', name: 'بيت الحكمة'},
  press: {x: 11250, year: '1450 م', name: 'الطباعة'},
  computer: {x: 12400, year: '1981 م', name: 'الكمبيوتر'},
  now: {x: 13600, year: '2026', name: 'الجرافيكس والفيديو'},
  future: {x: 14900, year: 'الأجازة الجاية', name: 'ولادك'},
};
export const WORLD_END = 15600;
