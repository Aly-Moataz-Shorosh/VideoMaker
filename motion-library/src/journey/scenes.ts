import React from 'react';
import {vectorScenes} from './vectors';
import {ozScenes} from './oz';
import {progScenes} from './prog';
import {JourneyEnd} from './end';
import {JyReal} from './real';

// "رحلة إلى مركز الجرافيكس" series scenes (one file per short / section). Used by film-short with look 'journey'.
export const journeyScenes: Record<string, React.FC<any>> = {...vectorScenes, ...ozScenes, ...progScenes, jy_end: JourneyEnd, jy_real: JyReal};
