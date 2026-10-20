import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {fontCss, C} from './theme';

// Wraps every template: loads fonts, optional preview background (Aly's footage frame).
// For final overlay renders leave `previewBg` empty -> transparent.
export const Base: React.FC<{previewBg?: string; children: React.ReactNode}> = ({previewBg, children}) => (
  <AbsoluteFill style={{direction: 'rtl', fontFamily: 'Cairo', color: C.ink}}>
    <style>{fontCss}</style>
    {previewBg ? <Img src={staticFile(previewBg)} style={{width: '100%', height: '100%', objectFit: 'cover'}} /> : null}
    <AbsoluteFill>{children}</AbsoluteFill>
  </AbsoluteFill>
);

// Splits "text with *highlight*" into spans; highlighted part gets the accent color.
export const Highlight: React.FC<{text: string; accent: string}> = ({text, accent}) => (
  <>
    {text.split(/(\*[^*]+\*)/g).map((part, i) =>
      part.startsWith('*') ? (
        <span key={i} style={{color: accent}}>{part.slice(1, -1)}</span>
      ) : (
        <span key={i}>{part}</span>
      ),
    )}
  </>
);
