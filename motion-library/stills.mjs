// Check a render without making a video: a few still frames -> ONE contact sheet PNG.
// Usage (from motion-library): node stills.mjs <comp> <props.json> <out.png> <frame> [<frame> ...]
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import {execFileSync} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const [comp, propsFile, out, ...frames] = process.argv.slice(2);
const inputProps = JSON.parse(fs.readFileSync(propsFile, 'utf8'));
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts'), publicDir: path.resolve('public')});
const composition = await selectComposition({serveUrl, id: comp, inputProps});
const tmp = fs.mkdtempSync(path.join(path.dirname(path.resolve(out)), 'stills-'));
for (const [i, f] of frames.entries()) {
  await renderStill({serveUrl, composition, inputProps, frame: Number(f), output: path.join(tmp, `${String(i).padStart(2, '0')}.png`), scale: 0.4});
  console.log('frame', f);
}
const cols = Math.min(frames.length, 5), rows = Math.ceil(frames.length / cols);
execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', '1', '-i', path.join(tmp, '%02d.png'), '-vf', `tile=${cols}x${rows}:padding=6`, '-frames:v', '1', out]);
for (const f of fs.readdirSync(tmp)) fs.unlinkSync(path.join(tmp, f));
fs.rmdirSync(tmp);
console.log('sheet', out);
