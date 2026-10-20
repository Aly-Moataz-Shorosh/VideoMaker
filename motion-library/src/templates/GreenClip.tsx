import React from 'react';
import {AbsoluteFill, OffthreadVideo, staticFile, useVideoConfig} from 'remotion';
import {z} from 'zod';

// Aly's own green-screen animations (`_branding/on video/youtube 1-3, instagram 1-3`), keyed once with FFmpeg into
// alpha .webm. Plays full-frame; dx/dy move it (fraction of width/height) so the animation lands in a free corner.
export const greenClipSchema = z.object({
  src: z.string().default('brand/greenscreen/gs_youtube_1.webm'),
  start: z.number().default(0), // seconds into the clip
  dx: z.number().default(0),
  dy: z.number().default(0),
  scale: z.number().default(1),
  volume: z.number().default(0.6),
  previewBg: z.string().default(''),
});

export const GreenClip: React.FC<z.infer<typeof greenClipSchema>> = (p) => {
  const {fps, width, height} = useVideoConfig();
  return (
    <AbsoluteFill style={{transform: `translate(${p.dx * width}px, ${p.dy * height}px) scale(${p.scale})`,
      transformOrigin: '100% 100%'}}>
      <OffthreadVideo transparent src={staticFile(p.src)} startFrom={Math.round(p.start * fps)} volume={p.volume}
        style={{width: '100%', height: '100%'}} />
    </AbsoluteFill>
  );
};
