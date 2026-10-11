"""Generate the voiceover lines with Kokoro (local, offline).

Usage: python3 scripts/make_vo.py <kokoro_model_dir>
Writes assets/vo/<id>.wav (24 kHz mono) and assets/vo/durations.json.
"""
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = Path(sys.argv[1])
OUT = ROOT / "assets" / "vo"
OUT.mkdir(parents=True, exist_ok=True)

# Default G2P misreads these acronyms; patch them in phoneme space.
PHONEME_FIXES = {
    "ˈʌsdk": "jˌuːˌɛsdˌiːsˈiː",  # USDC
    "jˈuːpi": "jˌuːpˌiːˈaɪ",  # UPI
    "fˈɔːɹks": "fˈɔːɹɛks",  # forex
}

cfg = json.loads((ROOT / "scripts" / "vo_lines.json").read_text())
kokoro = Kokoro(str(MODEL_DIR / "kokoro-v1.0.onnx"), str(MODEL_DIR / "voices-v1.0.bin"))

durations = {}
for line in cfg["lines"]:
    phonemes = kokoro.tokenizer.phonemize(line["text"], "en-us")
    for bad, good in PHONEME_FIXES.items():
        phonemes = phonemes.replace(bad, good)
    audio, sr = kokoro.create(
        phonemes, voice=cfg["voice"], speed=line.get("speed", cfg["speed"]), is_phonemes=True
    )
    # Short fades so clip edges never click.
    fade = int(sr * 0.012)
    audio[:fade] *= np.linspace(0, 1, fade)
    audio[-fade:] *= np.linspace(1, 0, fade)
    sf.write(OUT / f"{line['id']}.wav", audio, sr)
    durations[line["id"]] = round(len(audio) / sr, 3)
    print(f"{line['id']:14s} {durations[line['id']]:6.2f}s  {phonemes}")

(OUT / "durations.json").write_text(json.dumps(durations, indent=2))
print("total", round(sum(durations.values()), 2))
