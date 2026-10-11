"""Synthesized SFX for the Zygo demo. Writes assets/sfx/*.wav (44.1 kHz stereo)."""
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy import signal

SR = 44100
rng = np.random.default_rng(11)
OUT = Path(__file__).resolve().parent.parent / "assets" / "sfx"
OUT.mkdir(parents=True, exist_ok=True)


def n_(sec):
    return int(round(sec * SR))


def bp(x, lo, hi, order=2):
    return signal.sosfilt(signal.butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def hp(x, fc, order=2):
    return signal.sosfilt(signal.butter(order, fc, "high", fs=SR, output="sos"), x)


def lp(x, fc, order=2):
    return signal.sosfilt(signal.butter(order, fc, "low", fs=SR, output="sos"), x)


def sweep_noise(dur, f0, f1, width=1.6):
    n = n_(dur)
    noise = rng.standard_normal(n)
    out = np.zeros(n)
    block = n_(0.015)
    for i in range(0, n, block):
        p = i / n
        fc = f0 * (f1 / f0) ** p
        seg = bp(noise[max(0, i - 4 * block) : i + block], fc / width, min(fc * width, 19000))
        out[i : i + block] = seg[-len(out[i : i + block]) :]
    return out


def stereo(y, spread=0.0, pan=0.0):
    l = np.cos((pan + 1) * np.pi / 4)
    r = np.sin((pan + 1) * np.pi / 4)
    if spread:
        d = n_(spread)
        y2 = np.concatenate([np.zeros(d), y[:-d]])
        return np.stack([y * l, y2 * r], axis=1)
    return np.stack([y * l, y * r], axis=1)


def write(name, y, peak=0.8):
    if y.ndim == 1:
        y = stereo(y)
    fade = n_(0.004)
    y[:fade] *= np.linspace(0, 1, fade)[:, None]
    y[-fade:] *= np.linspace(1, 0, fade)[:, None]
    y = y / (np.max(np.abs(y)) + 1e-9) * peak
    sf.write(OUT / f"{name}.wav", y.astype(np.float32), SR, subtype="PCM_16")
    print(f"{name:12s} {len(y) / SR:.2f}s")


def env_swell(n, peak_at=0.65, attack_pow=2.0, release_pow=1.4):
    t = np.linspace(0, 1, n)
    up = (t / peak_at) ** attack_pow
    down = ((1 - t) / (1 - peak_at)) ** release_pow
    return np.where(t < peak_at, up, down)


# Section wipe whoosh: band-passed noise sweeping up, then air tail
d = 0.75
y = sweep_noise(d, 350, 5200) * env_swell(n_(d), 0.6)
y += 0.25 * hp(rng.standard_normal(n_(d)), 6000) * env_swell(n_(d), 0.7, 3, 2)
write("whoosh", stereo(y, spread=0.012), 0.7)

# Soft whoosh for camera zooms
d = 0.5
y = sweep_noise(d, 500, 2600, 1.4) * env_swell(n_(d), 0.55, 1.6, 1.8)
write("whoosh-soft", stereo(y, spread=0.008), 0.5)

# UI click: tight transient + tiny body
d = 0.06
t = np.arange(n_(d)) / SR
y = hp(rng.standard_normal(n_(d)), 2500) * np.exp(-t / 0.0035) + 0.6 * np.sin(2 * np.pi * 1400 * t) * np.exp(-t / 0.012)
write("click", y, 0.55)

# Keypress tick for typing the amount
d = 0.05
t = np.arange(n_(d)) / SR
y = bp(rng.standard_normal(n_(d)), 1800, 7000) * np.exp(-t / 0.006) + 0.3 * np.sin(2 * np.pi * 900 * t) * np.exp(-t / 0.01)
write("key", y, 0.4)

# Pop for callouts appearing
d = 0.16
t = np.arange(n_(d)) / SR
f = 520 + 520 * (1 - np.exp(-t / 0.02))
y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.045)
write("pop", y, 0.5)


def bell(f, d, decay=2.5):
    t = np.arange(n_(d)) / SR
    return (
        np.sin(2 * np.pi * f * t) * np.exp(-decay * t)
        + 0.4 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-decay * 1.8 * t)
        + 0.18 * np.sin(2 * np.pi * f * 3.02 * t) * np.exp(-decay * 3 * t)
    )


def place(total, parts):
    out = np.zeros(n_(total))
    for start, y, g in parts:
        i = n_(start)
        out[i : i + len(y)] += g * y[: len(out) - i]
    return out


# Notification ping: two-tone (A5 -> E6)
y = place(1.0, [(0.0, bell(880.0, 0.9, 4.5), 0.8), (0.11, bell(1318.5, 0.85, 4.0), 0.9)])
write("ping", stereo(y, spread=0.01), 0.55)

# Success chime: rising major arpeggio E6 G#6 B6 + shimmer
y = place(
    1.6,
    [
        (0.0, bell(1318.5, 1.4, 3.0), 0.7),
        (0.08, bell(1661.2, 1.4, 3.0), 0.7),
        (0.16, bell(1975.5, 1.4, 2.6), 0.85),
    ],
)
y += 0.08 * hp(rng.standard_normal(len(y)), 9000) * np.exp(-np.arange(len(y)) / SR / 0.25)
write("success", stereo(y, spread=0.014), 0.6)

# Soft impact for stat reveals / stamps
d = 0.9
t = np.arange(n_(d)) / SR
f = 60 + 90 * np.exp(-t / 0.05)
y = np.tanh(1.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.25)) + 0.35 * lp(rng.standard_normal(n_(d)), 1500) * np.exp(-t / 0.05)
write("thud", y, 0.6)

# Count-up tick (for stat counters)
d = 0.035
t = np.arange(n_(d)) / SR
y = np.sin(2 * np.pi * 2400 * t) * np.exp(-t / 0.004)
write("tick", y, 0.3)
