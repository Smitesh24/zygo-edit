"""Original music bed for the Zygo demo, synthesized offline.

100 BPM, 4/4, A major. 64 bars = 153.6 s, arranged to the storyboard sections so every
scene cut lands on a bar line. Writes assets/audio/music.wav (44.1 kHz stereo, 16-bit).
"""
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy import signal

SR = 44100
BPM = 100
BEAT = 60 / BPM
BAR = 4 * BEAT
N_BARS = 65
LENGTH = N_BARS * BAR + 3.0  # reverb tail
N = int(LENGTH * SR)
rng = np.random.default_rng(7)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "audio"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- harmony
VOICINGS = {
    "A": ([57, 61, 64, 69], 45),
    "E/G#": ([56, 59, 64, 68], 44),
    "F#m": ([57, 61, 66, 69], 42),
    "D": ([57, 62, 66, 69], 38),
    "Bm": ([59, 62, 66, 69], 47),
    "C#m": ([56, 61, 64, 68], 37),
    "E": ([56, 59, 64, 68], 40),
}
SECTIONS = [  # (name, first bar, chords) — hook first (app demo), then the explanation
    ("hook", 0, ["A", "E/G#", "F#m", "D", "E"]),
    ("demo", 5, (["A", "D", "F#m", "E"] * 7)[:27]),
    ("problem", 32, ["F#m", "D", "Bm", "C#m", "F#m", "D", "E"]),
    ("solution", 39, ["A", "E", "F#m", "D", "A", "E"]),
    ("impact", 45, ["D", "A", "E", "F#m", "D", "A", "E"]),
    ("traction", 52, ["F#m", "D", "A", "E", "F#m", "D", "A", "E", "E"]),
    ("outro", 61, ["D", "E", "A", "A"]),
]
CHORD_AT = {}
SECTION_AT = {}
SEC_START = {}
for name, start, chords in SECTIONS:
    SEC_START[name] = start
    for i, c in enumerate(chords):
        CHORD_AT[start + i] = c
        SECTION_AT[start + i] = name
assert len(CHORD_AT) == N_BARS


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def t_of(bar, beat=0.0):
    return bar * BAR + beat * BEAT


def idx(t):
    return int(round(t * SR))


# ---------------------------------------------------------------- oscillators
def saw_blep(freq, n, phase0=0.0):
    dt = freq / SR
    t = (phase0 + dt * np.arange(n)) % 1.0
    y = 2 * t - 1
    a = t < dt
    x = t[a] / dt
    y[a] -= x + x - x * x - 1
    b = t > 1 - dt
    x = (t[b] - 1) / dt
    y[b] -= x * x + x + x + 1
    return y


def adsr(n, a, d, s, r, sustain_len):
    """Envelope of n samples: attack a, decay d to level s, hold until sustain_len, release r."""
    env = np.zeros(n)
    A, D, S_end = idx(a), idx(d), idx(sustain_len)
    R = n - S_end
    A = max(A, 1)
    env[:A] = np.linspace(0, 1, A)
    d_end = min(A + D, n)
    env[A:d_end] = np.linspace(1, s, d_end - A)
    env[d_end:S_end] = s
    if R > 0:
        start = env[S_end - 1] if S_end > 0 else s
        env[S_end:] = start * np.exp(-np.arange(R) / (r * SR / 5))
    return env


def lowpass(x, fc, order=2):
    sos = signal.butter(order, fc, "low", fs=SR, output="sos")
    return signal.sosfilt(sos, x, axis=0)


def highpass(x, fc, order=2):
    sos = signal.butter(order, fc, "high", fs=SR, output="sos")
    return signal.sosfilt(sos, x, axis=0)


def bandpass(x, lo, hi, order=2):
    sos = signal.butter(order, [lo, hi], "band", fs=SR, output="sos")
    return signal.sosfilt(sos, x, axis=0)


def add(bus, start_t, clip, gain=1.0, pan=0.0):
    """Mix a mono clip into a stereo bus at start_t with constant-power pan (-1..1)."""
    i = idx(start_t)
    if i >= N:
        return
    clip = clip[: N - i]
    l = np.cos((pan + 1) * np.pi / 4) * gain
    r = np.sin((pan + 1) * np.pi / 4) * gain
    bus[i : i + len(clip), 0] += clip * l
    bus[i : i + len(clip), 1] += clip * r


# ---------------------------------------------------------------- instruments
def pad_note(m, dur):
    n = idx(dur + 1.6)
    out = np.zeros((n, 2))
    for k, cents in enumerate((-8, 0, 8)):
        f = hz(m) * 2 ** (cents / 1200)
        osc = saw_blep(f, n, rng.random()) + 0.5 * saw_blep(f / 2, n, rng.random())
        pan = (-0.6, 0.0, 0.6)[k]
        out[:, 0] += osc * np.cos((pan + 1) * np.pi / 4)
        out[:, 1] += osc * np.sin((pan + 1) * np.pi / 4)
    env = adsr(n, 0.5, 0.8, 0.75, 1.4, dur)
    return out * env[:, None] / 3


def pluck(m, dur=0.55, bright=1.0):
    n = idx(dur)
    t = np.arange(n) / SR
    f = hz(m)
    y = np.zeros(n)
    for k in range(1, 9):
        if f * k > 9000:
            break
        decay = 7.0 * (1 + 0.55 * (k - 1)) / bright
        y += (1 / k**1.15) * np.sin(2 * np.pi * f * k * t + 0.3 * k) * np.exp(-decay * t)
    att = min(idx(0.004), n)
    y[:att] *= np.linspace(0, 1, att)
    return y * 0.5


def bell(m, dur=1.6):
    n = idx(dur)
    t = np.arange(n) / SR
    f = hz(m)
    y = (
        np.sin(2 * np.pi * f * t) * np.exp(-2.2 * t)
        + 0.45 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-3.5 * t)
        + 0.25 * np.sin(2 * np.pi * f * 3.01 * t) * np.exp(-6.0 * t)
        + 0.12 * np.sin(2 * np.pi * f * 4.2 * t) * np.exp(-9.0 * t)
    )
    y[: idx(0.003)] *= np.linspace(0, 1, idx(0.003))
    return y * 0.35


def bass_note(m, dur):
    n = idx(dur)
    t = np.arange(n) / SR
    f = hz(m)
    y = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) + 0.12 * saw_blep(f, n)
    y = np.tanh(1.6 * y) / 1.2
    env = np.ones(n)
    a, r = idx(0.006), idx(0.06)
    env[:a] = np.linspace(0, 1, a)
    env[-r:] *= np.linspace(1, 0, r)
    env *= 0.75 + 0.25 * np.exp(-t / 0.12)
    return y * env


def kick():
    n = idx(0.45)
    t = np.arange(n) / SR
    f = 46 + 120 * np.exp(-t / 0.032)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-t / 0.26)
    click = highpass(rng.standard_normal(idx(0.004)), 2500) * 0.25
    y[: len(click)] += click
    return np.tanh(1.4 * y)


def clap():
    n = idx(0.32)
    t = np.arange(n) / SR
    noise = bandpass(rng.standard_normal(n), 900, 5200)
    env = np.zeros(n)
    for off in (0.0, 0.011, 0.022):
        i0 = idx(off)
        env[i0:] += np.exp(-(t[: n - i0]) / (0.012 if off < 0.02 else 0.11))
    return noise * env * 0.35


def hat(open_=False):
    n = idx(0.3 if open_ else 0.07)
    t = np.arange(n) / SR
    y = highpass(rng.standard_normal(n), 7500, 4) * np.exp(-t / (0.11 if open_ else 0.018))
    return y * 0.22


def tick():
    n = idx(0.05)
    t = np.arange(n) / SR
    y = np.sin(2 * np.pi * 1850 * t) * np.exp(-t / 0.008) + 0.3 * highpass(rng.standard_normal(n), 3000) * np.exp(-t / 0.006)
    return y * 0.25


def riser(dur):
    n = idx(dur)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    y = np.zeros(n)
    block = idx(0.04)
    for i in range(0, n, block):
        p = i / n
        lo = 300 + 5000 * p**2
        seg = bandpass(noise[max(0, i - block) : i + block], lo, min(lo * 2.2, 18000))
        y[i : i + block] = seg[-min(block, n - i) :] if i else seg[: min(block, n - i)]
    sweep = np.sin(2 * np.pi * np.cumsum(220 + 900 * (t / dur) ** 2) / SR)
    env = (t / dur) ** 2.2
    return (y * 0.6 + sweep * 0.12) * env


def boom():
    n = idx(2.4)
    t = np.arange(n) / SR
    f = 32 + 70 * np.exp(-t / 0.09)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.7)
    hit = lowpass(rng.standard_normal(n), 900) * np.exp(-t / 0.18) * 0.5
    return np.tanh(1.3 * (sub + hit))


# ---------------------------------------------------------------- arrangement
pad = np.zeros((N, 2))
arp = np.zeros((N, 2))
lead = np.zeros((N, 2))
bass = np.zeros((N, 2))
drums = np.zeros((N, 2))
fx = np.zeros((N, 2))
shaker = np.zeros((N, 2))

KICK, CLAP, HAT, HAT_O, TICK = kick(), clap(), hat(), hat(True), tick()
kick_times = []

ARP_PATTERN = [0, 2, 1, 3, 2, 1, 3, 2]  # indices into the voicing, 8ths

for bar in range(N_BARS):
    sec = SECTION_AT[bar]
    rel = bar - SEC_START[sec]
    chord, bass_m = VOICINGS[CHORD_AT[bar]]
    t0 = t_of(bar)
    last = bar == N_BARS - 1

    pad_gain = {"hook": 0.42, "problem": 0.5, "solution": 0.42, "demo": 0.36, "impact": 0.42, "traction": 0.42, "outro": 0.55}[sec]
    for m in chord:
        add(pad, t0, pad_note(m, BAR * (2.0 if last else 1.0)).sum(axis=1) * 0.5, pad_gain / len(chord) * 2.2)

    # Arp
    arp_on = sec in ("hook", "solution", "impact", "traction", "outro") or (sec == "demo" and rel >= 8) or (sec == "problem" and rel >= 2)
    if arp_on and not (sec == "outro" and rel >= 2):
        bright = {"hook": 1.2, "problem": 0.55, "solution": 1.1, "demo": 0.75, "impact": 1.1, "traction": 1.25, "outro": 0.8}[sec]
        g = {"hook": 0.34, "problem": 0.22, "solution": 0.34, "demo": 0.22, "impact": 0.33, "traction": 0.36, "outro": 0.3}[sec]
        for s_, k in enumerate(ARP_PATTERN):
            m = chord[k % len(chord)] + 12
            add(arp, t0 + s_ * BEAT / 2, pluck(m, 0.5, bright), g, pan=(-0.35 if s_ % 2 else 0.35))

    # Lead bell counter-melody: hook, traction and the back half of impact
    if sec in ("hook", "traction") or (sec == "impact" and rel >= 3):
        tones = [chord[3] + 12, chord[2] + 12, chord[1] + 12, chord[2] + 12]
        for q, m in enumerate(tones):
            if q in (0, 2) or sec != "impact":
                add(lead, t0 + q * BEAT, bell(m), 0.2 if sec != "impact" else 0.16, pan=0.15)

    # Bass
    if sec == "problem":
        for e in range(8):
            add(bass, t0 + e * BEAT / 2, bass_note(bass_m, BEAT / 2 * 0.8), 0.32 if e % 2 == 0 else 0.2)
    elif sec != "outro" or rel < 2:
        pattern = [0, 1.5, 2, 3.5] if sec == "demo" else [0, 0.5, 1.5, 2, 2.5, 3.5]
        for b_ in pattern:
            add(bass, t0 + b_ * BEAT, bass_note(bass_m, BEAT * 0.45), 0.42)

    # Drums
    four_floor = sec in ("hook", "solution", "impact", "traction") or (sec == "demo" and rel < 26) or (sec == "outro" and rel < 2)
    if four_floor:
        kg = 0.38 if sec == "demo" else 0.48
        for b_ in range(4):
            add(drums, t0 + b_ * BEAT, KICK, kg)
            kick_times.append(t0 + b_ * BEAT)
        hats_on = sec != "demo" or rel >= 4
        if hats_on:
            for e in range(8):
                if e % 2 == 1:
                    add(drums, t0 + e * BEAT / 2, HAT_O if (sec in ("traction", "impact", "hook") and e == 7) else HAT, 1.5 if sec != "demo" else 1.1, pan=0.25)
                elif sec in ("impact", "traction", "hook"):
                    add(drums, t0 + e * BEAT / 2, HAT, 0.7, pan=-0.25)
        clap_on = sec in ("hook", "solution", "impact", "traction") or (sec == "demo" and 16 <= rel < 24)
        if clap_on:
            for b_ in (1, 3):
                add(drums, t0 + b_ * BEAT, CLAP, 0.6 if sec != "demo" else 0.4, pan=-0.05)
    if sec in ("demo", "impact", "traction", "hook") and not (sec == "demo" and rel >= 26):
        for e in range(16):
            n_ = idx(0.06)
            sh = highpass(rng.standard_normal(n_), 5000, 2) * np.exp(-np.arange(n_) / SR / 0.02)
            add(shaker, t0 + e * BEAT / 4, sh, (0.09 if e % 4 == 2 else 0.05) * (0.8 if sec == "demo" else 1.0), pan=0.45)
    if sec == "problem":
        for e in range(8):
            add(drums, t0 + e * BEAT / 2, TICK, 0.5 if e % 2 else 0.3, pan=0.3)
        if rel >= 5:
            for b_ in (0, 2):
                add(drums, t0 + b_ * BEAT, KICK, 0.45)
                kick_times.append(t0 + b_ * BEAT)

# Risers into the big moments and impacts on them
add(fx, t_of(4), riser(BAR), 0.35)  # hook -> demo
add(fx, t_of(37), riser(2 * BAR), 0.5)  # into "Zygo flips that"
add(fx, t_of(44), riser(BAR), 0.35)  # into impact
add(fx, t_of(51), riser(BAR), 0.4)  # into traction
add(fx, t_of(60), riser(BAR), 0.4)  # into outro
for bar, g in ((0, 0.7), (5, 0.35), (39, 0.55), (45, 0.5), (52, 0.55), (61, 0.6)):
    add(fx, t_of(bar), boom(), g)

# ---------------------------------------------------------------- mix
# Sidechain the pad and bass to the kick
duck = np.ones(N)
tt = np.arange(idx(0.35)) / SR
shape = 1 - 0.55 * np.exp(-tt / 0.09)
for kt in kick_times:
    i = idx(kt)
    j = min(N, i + len(shape))
    duck[i:j] = np.minimum(duck[i:j], shape[: j - i])

pad = lowpass(pad, 4200) * duck[:, None]
# Darker pad during the problem section: crossfade a lowpassed copy in
dark = lowpass(pad, 900, 2)
w = np.zeros(N)
a, b = idx(t_of(32)), idx(t_of(39))
w[a:b] = 1
w = np.convolve(w, np.ones(idx(0.6)) / idx(0.6), mode="same")
pad = pad * (1 - w[:, None]) + dark * w[:, None]
bass = lowpass(bass, 1800) * duck[:, None]
arp = highpass(arp, 220)

# Feedback-free dotted-eighth echo on the arp
delay = np.zeros_like(arp)
d = idx(BEAT * 0.75)
delay[d:, 0] += arp[:-d, 1] * 0.32
delay[2 * d :, 1] += arp[: -2 * d, 0] * 0.18
arp = arp + lowpass(delay, 4000)

# Reverb send: decaying stereo noise IR
ir_len = idx(2.6)
ti = np.arange(ir_len) / SR
ir = rng.standard_normal((ir_len, 2)) * np.exp(-ti / 0.55)[:, None]
ir = lowpass(ir, 5500)
ir /= np.sqrt((ir**2).sum(axis=0))
send = pad * 0.35 + arp * 0.5 + lead * 0.6 + drums * 0.08 + fx * 0.3
wet = np.stack([signal.fftconvolve(send[:, c], ir[:, c])[:N] for c in range(2)], axis=1)

mix = pad * 0.9 + arp * 1.0 + lead * 1.0 + bass * 0.5 + drums * 0.9 + shaker * 0.9 + fx * 0.8 + wet * 0.55
mix = mix - 0.35 * lowpass(mix, 90)  # tame the sub build-up
mix = highpass(mix, 28)

# Gentle glue: soft clip then normalize
mix = np.tanh(mix * 1.1)
mix /= np.max(np.abs(mix)) / 0.89

# Fade in/out
fi = idx(0.05)
mix[:fi] *= np.linspace(0, 1, fi)[:, None]
fo_start = idx(N_BARS * BAR - 1.2)
mix[fo_start:] *= np.linspace(1, 0, N - fo_start)[:, None] ** 1.5

sf.write(OUT / "music.wav", mix.astype(np.float32), SR, subtype="PCM_16")
rms = np.sqrt(np.mean(mix**2))
print(f"wrote {OUT / 'music.wav'}  {N / SR:.1f}s  rms {20 * np.log10(rms):.1f} dBFS")
