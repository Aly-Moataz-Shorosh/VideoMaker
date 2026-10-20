#!/bin/sh
# Build edit_<name>.json for this project under the ASCII code 'enta00' (build_edit names the public folder after the
# project folder, and this one is Arabic). Usage (from video-maker): sh "projects/انت بتشتغل ايه/فيديو تعريفي/work/scripts/build.sh" review_01
name=${1:-review_01}
proj="projects/انت بتشتغل ايه/فيديو تعريفي"
python -X utf8 "$proj/work/scripts/make_plan.py" || exit 1
python -X utf8 tools/build_edit.py "$proj" --name "$name" || exit 1
pub=motion-library/public/projects
mv -f "$pub/فيديو تعريفي/edit_$name.json" "$pub/enta00/" && rm -rf "$pub/فيديو تعريفي"   # source.mp4 there is a hard link
python -X utf8 -c "
import sys; p=sys.argv[1]; s=open(p,encoding='utf8').read().replace('projects/فيديو تعريفي/','projects/enta00/'); open(p,'w',encoding='utf8').write(s)" "$pub/enta00/edit_$name.json"
echo "ok $pub/enta00/edit_$name.json"
