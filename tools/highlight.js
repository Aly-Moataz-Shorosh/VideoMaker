(q) => {
  const BS = String.fromCharCode(92);
  const esc = s => s.replace(/[-\/\^$*+?.()|[\]{}]/g, m => BS + m);
  const SEP = /(?:\s|\[[^\]]{0,12}\]|[\u200e\u200f\u00ad])*/.source;
  const root = document.querySelector('#mw-content-text') || document.querySelector('main') || document.body;
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  let nodes = [], full = '';
  while (w.nextNode()) { const n = w.currentNode; nodes.push([n, full.length]); full += n.nodeValue; }
  // Arabic diacritics (tashkeel, tatweel) are ignored on both sides, so a bare phrase matches a vocalised page
  const AR = /[\u064B-\u065F\u0670\u06D6-\u06ED\u0640]/;
  let norm = '', map = [];
  for (let k = 0; k < full.length; k++) { if (!AR.test(full[k])) { norm += full[k]; map.push(k); } }
  map.push(full.length);
  const parts = q.trim().split(/\s+/).map(p => esc(p.replace(new RegExp(AR.source, 'g'), '')));
  const m = norm.match(new RegExp(parts.join(SEP), 'i'));
  if (!m) return false;
  const i = map[m.index], end = map[m.index + m[0].length - 1] + 1;
  let sN, sO, eN, eO;
  for (const [n, off] of nodes) {
    const L = n.nodeValue.length;
    if (!sN && i < off + L) { sN = n; sO = i - off; }
    if (end <= off + L) { eN = n; eO = end - off; break; }
  }
  const r = document.createRange(); r.setStart(sN, sO); r.setEnd(eN, eO);
  const mk = document.createElement('mark'); mk.style.cssText = 'background:#ffe066;outline:3px solid #e8590c;';
  const c = r.extractContents(); mk.appendChild(c); r.insertNode(mk);
  mk.scrollIntoView({block: 'center'});
  return true;
}
