"""Premiere project for rough cut v8 (Aly v7 note 6): V1 = the video WITHOUT the handles, V2 = the handles layer (transparent PNG, the whole
length, easy to delete), A1 voice, A2 song, A3 sfx (separate stems). FCP7 XML -> Premiere: File > Import > the .xml.
Usage (project folder): python -X utf8 work/scripts/premiere_v8.py"""
import json, subprocess
from pathlib import Path
from urllib.parse import quote

P = Path.cwd(); OUT = P / "output" / "premiere_v8"; OUT.mkdir(parents=True, exist_ok=True)
FPS = 25
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout)
V1 = P / "output" / "rough_cut_v8_clean.mp4"; V2 = OUT / "handles_layer.png"
A = [P / "output/audio_stems_v8/voice_full_timeline.wav", P / "output/audio_stems_v8/music/song_C1_full_timeline.wav", P / "output/audio_stems_v8/sfx/sfx_timeline.wav"]
N = int(round(dur(V1) * FPS))
def url(p): return "file://localhost/" + quote(str(p).replace("\\", "/"), safe="/:")
def clip(i, name, path, kind, n, still=False):
    media = (f"<media><video><samplecharacteristics><width>1920</width><height>1080</height></samplecharacteristics></video></media>" if kind == "video"
             else "<media><audio><channelcount>2</channelcount></audio></media>")
    return f"""<clipitem id="c{i}"><name>{name}</name><duration>{n}</duration><rate><timebase>{FPS}</timebase></rate>
<start>0</start><end>{n}</end><in>0</in><out>{n}</out>
<file id="f{i}"><name>{name}</name><pathurl>{url(path)}</pathurl><rate><timebase>{FPS}</timebase></rate><duration>{n}</duration>{media}</file></clipitem>"""
xml = f"""<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE xmeml><xmeml version="4"><sequence id="seq"><name>عالم الـ AI كله - rough cut v8</name>
<duration>{N}</duration><rate><timebase>{FPS}</timebase></rate><media>
<video><format><samplecharacteristics><width>1920</width><height>1080</height><rate><timebase>{FPS}</timebase></rate></samplecharacteristics></format>
<track>{clip(1, V1.name, V1, "video", N)}</track><track>{clip(2, "handles_layer.png (delete = no handles)", V2, "video", N, still=True)}</track></video>
<audio>{''.join(f'<track>{clip(3 + k, a.name, a, "audio", N)}</track>' for k, a in enumerate(A))}</audio></media></sequence></xmeml>"""
(OUT / "rough_cut_v8.xml").write_text(xml, encoding="utf-8")
print("written", OUT / "rough_cut_v8.xml", N, "frames")
