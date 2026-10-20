import React from 'react';
import * as v1 from './v1';
import * as v2 from './v2';
import * as v4 from './v4';
import * as v8 from './v8';

// Scene id (used in projects/<code>/work/scripts/make_shorts.py) -> component, look 'vhs' (vhstodigital 2026-10-09).
export const vhsScenes: Record<string, React.FC<any>> = {
  v1_hook: v1.V1Hook, v1_tapes: v1.V1Tapes, v1_idea: v1.V1Idea, v1_hours: v1.V1Hours, v1_convert: v1.V1Convert, v1_why: v1.V1Why,
  v1_chain: v1.V1Chain, v1_result: v1.V1Result, v1_end: v1.V1End, v1_soft: v1.V1Soft,
  v2_hook: v2.V2Hook, v2_shop: v2.V2Shop, v2_price: v2.V2Price, v2_privacy: v2.V2Privacy, v2_home: v2.V2Home,
  v4_hook: v4.V4Hook, v4_easy: v4.V4Easy, v4_problem: v4.V4Problem, v4_mine: v4.V4Mine, v4_versus: v4.V4Versus, v4_end: v4.V4End,
  v8_hook: v8.V8Hook, v8_real: v8.V8Real, vt: v1.VTitle, v8_box: v8.V8Box, v8_play: v8.V8Play, v8_save: v8.V8Save, v8_end: v8.V8End, v8_pray: v8.V8Pray,
};
