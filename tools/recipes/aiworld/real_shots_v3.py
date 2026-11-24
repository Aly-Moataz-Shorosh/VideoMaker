"""Method 2 ('real face') for the avatar shots marked 'real' in work/avatar_methods_v3.json:
RVM cut-out of the HeyGen avatar clip (his real pixels) over the empty S4g plate, low feather, colours of how he looks in the
generated S4g still (same settings Aly saw in output/studio_example_real.mp4). Silent mp4 (voice = separate track).
Out: assets/ai/heygen/avatar_clips_v3_real/avatar_<n>_<ch>.mp4.  Usage (project folder): python -X utf8 work/scripts/real_shots_v3.py"""
import glob, json, shutil, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0, "work/scripts")
from studio_comp import comp, load_plate, _lab_stats

ROOT = Path(__file__).resolve().parents[4]          # video-maker
OUT = Path("assets/ai/heygen/avatar_clips_v3_real"); OUT.mkdir(parents=True, exist_ok=True)
TMP = Path("work/_tmp_real"); TMP.mkdir(exist_ok=True)
meth = json.load(open("work/avatar_methods_v3.json", encoding="utf-8"))["methods"]
clips = {x["n"]: x for x in json.load(open("assets/ai/heygen/avatar_clips_v1/avatar_clips_v1.json", encoding="utf-8"))}
W, H = 1920, 1080
plate = load_plate("assets/ai/higgsfield/studio_look_v2/plate_S4g_empty.png", W, H)
gen = np.asarray(Image.open("assets/ai/higgsfield/studio_look_v2/gen_S4g_nefertari_mashrabiya.png").convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.float32) / 255
ref_a = np.asarray(Image.open("assets/ai/higgsfield/studio_look_v1/matte_avatar001_2s.png").convert("RGBA")).astype(np.float32)[..., 3] / 255
target = _lab_stats(gen, ref_a)
for n, m in sorted(meth.items(), key=lambda kv: int(kv[0])):
    if m != "real":
        continue
    c = clips[int(n)]; src = Path("assets/ai/heygen/avatar_clips_v1") / c["file"]; out = OUT / c["file"]
    if out.exists():
        continue
    webm = TMP / f"m_{n}.webm"; fr = TMP / f"f_{n}"; fr.mkdir(exist_ok=True)
    subprocess.run([sys.executable, "-X", "utf8", str(ROOT / "tools/matte.py"), str(src.resolve()), "0", f"{c['dur']:.3f}", str(webm.resolve()), "--fps", "25"], check=True, cwd=ROOT)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-c:v", "libvpx-vp9", "-i", str(webm), "-pix_fmt", "rgba", str(fr / "%04d.png")], check=True)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "25", "-i", "-",
                          "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    for i, f in enumerate(sorted(glob.glob(str(fr / "*.png")))):
        fg = np.asarray(Image.open(f).convert("RGBA")).astype(np.float32) / 255
        p.stdin.write((comp(fg, plate, seed=i, feather=0.35, erode=0.35, wrap=0.12, rim=0.35, grade=0.7, target=target) * 255).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait()
    shutil.rmtree(fr); webm.unlink()
    print("ok", out, flush=True)
shutil.rmtree(TMP, ignore_errors=True)
print("ALL_REAL_DONE")
