#!/bin/sh
# Build edit_<name>.json for this episode under the ASCII code 'entabiz01' (build_edit names the public folder after the
# project folder). Usage (from video-maker): sh "projects/انت بتشتغل ايه/2026-10-27 ep01 biz karim tamer/work/scripts/build.sh" review_01
name=${1:-review_01}
proj="projects/انت بتشتغل ايه/2026-10-27 ep01 biz karim tamer"
code="2026-10-27 ep01 biz karim tamer"
python -X utf8 "$proj/work/scripts/make_plan.py" || exit 1
python -X utf8 tools/build_edit.py "$proj" --name "$name" || exit 1
pub=motion-library/public/projects
mv -f "$pub/$code/edit_$name.json" "$pub/entabiz01/" && rm -rf "${pub:?}/${code:?}"   # source.mp4 there is a hard link
python -X utf8 -c "
import sys; p=sys.argv[1]; s=open(p,encoding='utf8').read().replace('projects/$code/','projects/entabiz01/').replace('entabiz01/source.mp4','entabiz01/source30.mp4'); open(p,'w',encoding='utf8').write(s)" "$pub/entabiz01/edit_$name.json"
echo "ok $pub/entabiz01/edit_$name.json"
