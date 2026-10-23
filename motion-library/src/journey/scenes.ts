import React from 'react';
import {vectorScenes} from './vectors';
import {ozScenes} from './oz';
import {oz2Scenes} from './oz2';
import {introScenes} from './intro';
import {peditScenes} from './pedit';
import {progScenes} from './prog';
import {JourneyEnd} from './end';
import {JyReal} from './real';
import {JyClip, JyZoom} from './clip';

// "رحلة إلى مركز الجرافيكس" series scenes (one file per short / section). Used by film-short with look 'journey'.
export const journeyScenes: Record<string, React.FC<any>> = {...vectorScenes, ...ozScenes, ...oz2Scenes, ...introScenes, ...peditScenes, ...progScenes, jy_end: JourneyEnd, jy_real: JyReal, jy_clip: JyClip, jy_zoom: JyZoom};
