import React from 'react';
import {AtmScene, KetchupScene, Shield} from './ux';
import {AtmStory, Count, Flow, Hero, List, Vs} from './emo';
import {Dots, Steps, TShape} from './emo2';
import {Flipbook, MapTour, Pic, Pics, PixVec, Thumbs} from './extra';
import {Looks3D, Mat3D, Rot3D} from './three';

// cue k -> scene component (props: dur in frames + cue p)
export const stageScenes: Record<string, React.FC<any>> = {
  atm: AtmScene,
  ketchup: KetchupScene,
  shield: Shield,
  hero: Hero, vs: Vs, flow: Flow, list: List, count: Count, atm3d: AtmStory,
  steps: Steps, tshape: TShape, dots: Dots,
  pic: Pic, pics: Pics, thumbs: Thumbs, map: MapTour, pixvec: PixVec, flipbook: Flipbook, mat3d: Mat3D, looks3d: Looks3D, rot3d: Rot3D,
};
