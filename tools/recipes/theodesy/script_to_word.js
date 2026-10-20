const fs = require('fs');
const {Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, BorderStyle, PageBreak} = require('docx');
const [src, out] = process.argv.slice(2);
const lines = fs.readFileSync(src, 'utf8').split(/\r?\n/);
const F = 'Arial';
const run = (t, o = {}) => new TextRun({text: t, rightToLeft: true, font: {name: F, cs: F}, size: o.size || 30, sizeComplexScript: o.size || 30,
  bold: o.bold, boldComplexScript: o.bold, color: o.color});
const kids = [];
let first = true;
for (const l of lines) {
  const s = l.trim();
  if (!s || s === '---') continue;
  if (s.startsWith('# ')) {
    kids.push(new Paragraph({bidirectional: true, alignment: AlignmentType.CENTER, spacing: {after: 240}, children: [run(s.slice(2), {size: 40, bold: true})]}));
  } else if (s.startsWith('## ')) {
    kids.push(new Paragraph({heading: HeadingLevel.HEADING_1, bidirectional: true, alignment: AlignmentType.RIGHT, pageBreakBefore: !first,
      spacing: {before: 120, after: 200}, border: {bottom: {style: BorderStyle.SINGLE, size: 8, color: 'E5232B', space: 4}},
      children: [run(s.slice(3), {size: 36, bold: true, color: '1A1917'})]}));
    first = false;
  } else if (s.startsWith('> ')) {
    kids.push(new Paragraph({bidirectional: true, alignment: AlignmentType.RIGHT, spacing: {after: 200}, indent: {right: 360},
      border: {right: {style: BorderStyle.SINGLE, size: 18, color: 'FFC21A', space: 8}}, children: [run(s.slice(2), {bold: true})]}));
  } else {
    kids.push(new Paragraph({bidirectional: true, alignment: AlignmentType.RIGHT, spacing: {after: 140, line: 360}, children: [run(s)]}));
  }
}
const doc = new Document({
  styles: {default: {document: {run: {font: F, size: 30}}},
    paragraphStyles: [{id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: {size: 36, bold: true, font: F}, paragraph: {spacing: {before: 120, after: 200}, outlineLevel: 0}}]},
  sections: [{properties: {page: {margin: {top: 1200, bottom: 1200, left: 1200, right: 1200}}}, children: kids}],
});
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(out, b); console.log('ok', out); });
