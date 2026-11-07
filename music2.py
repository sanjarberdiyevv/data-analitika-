import numpy as np, wave, sys

SR = 44100
DUR = float(sys.argv[2])
N = int(SR * DUR)
out = np.zeros(N)
rng = np.random.default_rng(7)
BPM = 112
beat = 60 / BPM


def add(sig, t0, gain=1.0):
    i = int(t0 * SR)
    if i >= N:
        return
    j = min(N, i + len(sig))
    out[i:j] += sig[: j - i] * gain


def env(n, a=0.005, d=0.2):
    t = np.arange(n) / SR
    e = np.minimum(1, t / a) * np.exp(-t / d)
    return e


def kick():
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    f = 50 + 90 * np.exp(-t * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env(n, 0.002, 0.12)


def hat():
    n = int(0.06 * SR)
    s = rng.standard_normal(n)
    s = np.diff(np.concatenate([[0], s]))  # crude highpass
    return s * env(n, 0.001, 0.015) * 0.5


def pluck(freq, length=0.5):
    n = int(length * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * freq * t) + 0.4 * np.sin(4 * np.pi * freq * t) + 0.15 * np.sin(6 * np.pi * freq * t)
    return s * env(n, 0.004, 0.18)


def bass(freq, length):
    n = int(length * SR)
    t = np.arange(n) / SR
    s = np.tanh(2 * np.sin(2 * np.pi * freq * t))
    return s * env(n, 0.01, length * 0.6)


def whoosh(length=0.5):
    n = int(length * SR)
    s = rng.standard_normal(n)
    # moving lowpass via cumulative smoothing with changing alpha
    y = np.zeros(n)
    acc = 0
    for i in range(n):
        a = 0.02 + 0.3 * (i / n)
        acc += a * (s[i] - acc)
        y[i] = acc
    e = np.sin(np.pi * np.arange(n) / n) ** 2
    return y * e * 1.8


def pop():
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    f = 900 * np.exp(-t * 18) + 300
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.04)


def tick():
    n = int(0.03 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * 2400 * t) * env(n, 0.0005, 0.006)


def chaching():
    n = int(0.7 * SR)
    t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * 1567 * t) + np.sin(2 * np.pi * 2093 * t) * 0.8 + np.sin(2 * np.pi * 2637 * t) * 0.5)
    return s * env(n, 0.002, 0.25) * 0.5


# chord progression (Am - F - C - G), 2 beats each... 1 bar = 4 beats
roots = [110.0, 87.31, 130.81, 98.0]
chords = [[220, 261.63, 329.63], [174.61, 220, 261.63], [261.63, 329.63, 392], [196, 246.94, 293.66]]
bar = 4 * beat
t = 0.0
k = 0
while t < DUR - 0.5:
    ci = k % 4
    for b in range(4):
        tb = t + b * beat
        add(kick(), tb, 0.9)
        add(hat(), tb + beat / 2, 0.35)
        add(bass(roots[ci], beat * 0.9), tb, 0.28)
    for j, f in enumerate(chords[ci]):
        add(pluck(f * 2, 0.6), t + j * beat / 3, 0.12)
        add(pluck(f * 2, 0.6), t + 2 * beat + j * beat / 3, 0.10)
    t += bar
    k += 1

# SFX
for tc in [float(x) for x in sys.argv[3].split(',')]:
    add(whoosh(0.45), tc - 0.3, 0.35)
for tc in [float(x) for x in sys.argv[4].split(',')]:
    add(pop(), tc, 0.5)
# fade out last 1.2s, fade in 0.1s
fo = int(1.2 * SR)
out[-fo:] *= np.linspace(1, 0, fo)
out[: int(0.1 * SR)] *= np.linspace(0, 1, int(0.1 * SR))
out = out / np.max(np.abs(out)) * 0.85
pcm = (np.stack([out, out], axis=1) * 32767).astype(np.int16)
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
