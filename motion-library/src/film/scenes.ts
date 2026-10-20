import React from 'react';
import * as s01 from './s01';
import * as s02 from './s02';
import * as s03 from './s03';
import * as s04 from './s04';
import * as s05 from './s05';
import * as s06 from './s06';
import * as s07 from './s07';
import * as s08 from './s08';
import * as s09 from './s09';
import * as s10 from './s10';

// Scene id (used in make_shorts.py plans) -> component. One file per short: s01.tsx, s02.tsx ...
export const filmScenes: Record<string, React.FC<any>> = {
  s1_hook: s01.S1Hook, s1_nolan: s01.S1Nolan, s1_why: s01.S1Why, s1_projector: s01.S1Projector, s1_map: s01.S1Map,
  s1_beam: s01.S1Beam, s1_egypt: s01.S1Egypt, s1_compare: s01.S1Compare, s1_aspect: s01.S1Aspect, s1_end: s01.S1End,
  s2_hook: s02.S2Hook, s2_emission: s02.S2Emission, s2_haytham: s02.S2Haytham, s2_light: s02.S2Light, s2_name: s02.S2Name,
  s2_obscura: s02.S2Obscura, s2_first: s02.S2First, s2_wall: s02.S2Wall,
  s3_hook: s03.S3Hook, s3_swap: s03.S3Swap, s3_keep: s03.S3Keep, s3_gens: s03.S3Gens, s3_miracle: s03.S3Miracle,
  s3_develop: s03.S3Develop, s3_born: s03.S3Born,
  s4_hook: s04.S4Hook, s4_silver: s04.S4Silver, s4_film: s04.S4Film, s4_camera: s04.S4Camera, s4_burn: s04.S4Burn,
  s4_develop: s04.S4Develop, s4_color: s04.S4Color, s4_past: s04.S4Past,
  s5_hook: s05.S5Hook, s5_count: s05.S5Count, s5_camera: s05.S5Camera, s5_fps: s05.S5Fps, s5_silent: s05.S5Silent,
  s5_band: s05.S5Band, s5_mic: s05.S5Mic, s5_sound: s05.S5Sound,
  s6_hook: s06.S6Hook, s6_gauge: s06.S6Gauge, s6_names: s06.S6Names, s6_shoot: s06.S6Shoot, s6_bigger: s06.S6Bigger, s6_clean: s06.S6Clean,
  s7_hook: s07.S7Hook, s7_digital: s07.S7Digital, s7_shock: s07.S7Shock, s7_colors: s07.S7Colors, s7_soul: s07.S7Soul, s7_grain: s07.S7Grain,
  s7_better: s07.S7Better,
  s8_hook: s08.S8Hook, s8_gauges: s08.S8Gauges, s8_biggest: s08.S8Biggest, s8_scenes: s08.S8Scenes, s8_noise: s08.S8Noise, s8_nolan: s08.S8Nolan,
  s8_blimp: s08.S8Blimp, s8_mirror: s08.S8Mirror, s8_first: s08.S8First,
  s9_hook: s09.S9Hook, s9_old: s09.S9Old, s9_how: s09.S9How, s9_robot: s09.S9Robot, s9_hand: s09.S9Hand, s9_prep: s09.S9Prep, s9_ready: s09.S9Ready,
  s10_hook: s10.S10Hook, s10_super8: s10.S10Super8, s10_16: s10.S1016, s10_35: s10.S1035, s10_day: s10.S10Day, s10_minute: s10.S10Minute,
  s10_receipt: s10.S10Receipt, s10_digital: s10.S10Digital,
};
