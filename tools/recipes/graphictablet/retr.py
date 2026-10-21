"""Re-transcribe one part (music under his voice) with a prompt of likely words. Usage: retr.py <wav> <offset s> <prompt>"""
import subprocess, sys
import numpy as np
from faster_whisper import WhisperModel
sys.stdout.reconfigure(encoding='utf-8')
wav, off, prompt = sys.argv[1], float(sys.argv[2]), sys.argv[3]
# decode with ffmpeg ourselves (PyAV inside faster-whisper breaks with this av version)
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', wav, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True, check=True).stdout
a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
m = WhisperModel('large-v3-turbo', device='cpu', compute_type='int8')
segs, _ = m.transcribe(a,language='ar', word_timestamps=True, initial_prompt=prompt, vad_filter=True, beam_size=5)
for s in segs:
    print(f"{s.start + off:7.1f}-{s.end + off:7.1f} {s.text}", flush=True)
    print('      ', ' '.join(f"{w.word.strip()}@{w.start + off:.1f}" for w in s.words), flush=True)
