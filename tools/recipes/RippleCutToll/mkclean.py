import json,subprocess
SRC=r"F:/_root/output/Youtube/Aly Shorosh - From 2026/5- delete silence/20261001_192249f.mp4"
m=json.load(open('his_edit_v1.json'))
lst=[]
for i,c in enumerate(m):
    n=round((c['end']-c['tl'])*30)
    o=f'clean/p{i:03d}.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f"{c['src']:.4f}",'-i',SRC,'-frames:v',str(n),'-an','-c:v','libx264','-crf','16','-preset','veryfast','-pix_fmt','yuv420p','-r','30',o],check=True)
    lst.append(f"file 'p{i:03d}.mp4'")
open('clean/list.txt','w').write('\n'.join(lst))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','clean/list.txt','-i','../input/delete_silence_edit.mp4','-map','0:v','-map','1:a','-c:v','copy','-c:a','copy','clean.mp4'],check=True)
print('ok')
