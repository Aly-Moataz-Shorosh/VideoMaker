// Alpha overlays for Premiere: bundle ONCE, then one ProRes 4444 .mov per job (frame range of the comp).
// Usage (from motion-library): node overlays.mjs <comp> <props.json> <jobs.json>   jobs = [{out, a, b}]
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';

const [comp, propsFile, jobsFile] = process.argv.slice(2);
const inputProps = JSON.parse(fs.readFileSync(propsFile, 'utf8'));
const jobs = JSON.parse(fs.readFileSync(jobsFile, 'utf8'));
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts'), publicDir: path.resolve('public')});
const composition = await selectComposition({serveUrl, id: comp, inputProps});
for (const j of jobs) {
  await renderMedia({serveUrl, composition, inputProps, outputLocation: j.out, codec: 'prores', proResProfile: '4444',
    pixelFormat: 'yuva444p10le', imageFormat: 'png', frameRange: [j.a, j.b], muted: true});
  console.log('overlay', path.basename(j.out));
}
