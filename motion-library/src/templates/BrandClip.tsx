import React from 'react';
import {AbsoluteFill, OffthreadVideo, staticFile} from 'remotion';
import {z} from 'zod';

// Full-screen insert of Aly's real brand clips (copied from Genjutsu final, 2026-10-06):
// genjutsu_intro_sting (4.4 s), genjutsu_transition_a / _b (~1.7 s), genjutsu_outro (25.8 s). Long videos only.
export const brandClipSchema = z.object({
  clip: z.enum(['genjutsu_intro_sting', 'genjutsu_transition_a', 'genjutsu_transition_b', 'genjutsu_outro']).default('genjutsu_transition_a'),
  muted: z.boolean().default(false),
});

export const BrandClip: React.FC<z.infer<typeof brandClipSchema>> = ({clip, muted}) => (
  <AbsoluteFill style={{background: '#000'}}>
    <OffthreadVideo src={staticFile(`brand/clips/${clip}.mp4`)} muted={muted} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
  </AbsoluteFill>
);
