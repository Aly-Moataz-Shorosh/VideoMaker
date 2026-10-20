#!/bin/sh
# Build edit_<name>.json for this episode under the ASCII code 'entacs01' (build_edit names the public folder after the
# project folder). Usage (from video-maker): sh "projects/انت بتشتغل ايه/2026-10-20 ep01 cs quality control/work/scripts/build.sh" review_01
name=${1:-review_01}
proj="projects/انت بتشتغل ايه/2026-10-20 ep01 cs quality control"
code="2026-10-20 ep01 cs quality control"
python -X utf8 "$proj/work/scripts/make_plan.py" || exit 1
python -X utf8 tools/build_edit.py "$proj" --name "$name" || exit 1
pub=motion-library/public/projects
mv -f "$pub/$code/edit_$name.json" "$pub/entacs01/" && rm -rf "$pub/$code"   # source.mp4 there is a hard link
python -X utf8 -c "
import sys; p=sys.argv[1]; s=open(p,encoding='utf8').read().replace('projects/$code/','projects/entacs01/'); open(p,'w',encoding='utf8').write(s)" "$pub/entacs01/edit_$name.json"
echo "ok $pub/entacs01/edit_$name.json"
