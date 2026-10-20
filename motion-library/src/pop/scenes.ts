import React from 'react';
import * as f1 from './f1';
import * as f2 from './f2';
import * as f3 from './f3';
import * as f4 from './f4';

// Scene id (projects/<code>/work/scripts/make_shorts.py) -> component, look 'pop' (ffmpeg shorts 2026-10-14).
export const popScenes: Record<string, React.FC<any>> = {
  f1_hook: f1.F1Hook, f1_google: f1.F1Google, f1_site: f1.F1Site, f1_bin: f1.F1Bin, f1_what: f1.F1What, f1_cmd: f1.F1Cmd,
  f1_line: f1.F1Line, f1_in: f1.F1In, f1_trick: f1.F1Trick, f1_enter: f1.F1Enter, f1_end: f1.F1End,
  f2_flash: f2.F2Flash, f2_why: f2.F2Why, f2_console: f2.F2Console, f2_input: f2.F2Input, f2_give: f2.F2Give, f2_i: f2.F2I,
  f3_hook: f3.F3Hook, f3_way1: f3.F3Way1, f3_way2: f3.F3Way2, f3_way3: f3.F3Way3, f3_end: f3.F3End,
  f4_github: f4.F4Github, f4_zip: f4.F4Zip, f4_folder: f4.F4Folder, f4_dragexe: f4.F4DragExe, f4_anatomy: f4.F4Anatomy, f4_rename: f4.F4Rename,
  f4_big: f4.F4Big, f4_done: f4.F4Done, f4_new: f4.F4New,
};
