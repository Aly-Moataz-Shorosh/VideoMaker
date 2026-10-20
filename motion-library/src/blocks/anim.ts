import {interpolate, spring, Easing} from 'remotion';
import {theme} from './theme';

// Enter progress 0..1 with a small overshoot (brand: fast in, soft out).
export const enter = (frame: number, fps: number, delay = 0) =>
  spring({frame: frame - delay, fps, config: {damping: 13, stiffness: 170, mass: 0.7}});

// Exit progress 1..0 over the last `outFrames` frames.
export const exit = (frame: number, duration: number, outFrames = theme.motion.outFrames) =>
  interpolate(frame, [duration - outFrames, duration], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.in(Easing.cubic),
  });

export const lerp = (p: number, a: number, b: number) => a + (b - a) * p;
