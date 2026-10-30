import os
"""Original synthesized background music for Everyday Cart reels (royalty free, made from scratch)."""
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100
rng = np.random.default_rng(7)
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def t_(d): return np.arange(int(d * SR)) / SR
def lp(x, fc, o=2): return sosfilt(butter(o, fc, "low", fs=SR, output="sos"), x)
def hp(x, fc, o=2): return sosfilt(butter(o, fc, "high", fs=SR, output="sos"), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], "band", fs=SR, output="sos"), x)

def add(buf, sig, at):
    i = int(at * SR); j = min(len(buf), i + len(sig))
    if i < len(buf): buf[i:j] += sig[: j - i]

# ---- instruments ----
def kick(soft=False):
    t = t_(0.45); f = 48 + (75 if not soft else 45) * np.exp(-t * 32)
    ph = 2 * np.pi * np.cumsum(f) / SR
    click = hp(rng.standard_normal(len(t)), 2000) * np.exp(-t * 300) * 0.15
    return (np.sin(ph) * np.exp(-t * (7 if not soft else 10)) + click)
def snare():
    t = t_(0.3); n = bp(rng.standard_normal(len(t)), 1200, 6000) * np.exp(-t * 22)
    return 0.7 * n + 0.35 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 28)
def clap():
    t = t_(0.25); n = bp(rng.standard_normal(len(t)), 900, 4000)
    e = np.exp(-t * 30) * (1 + 0.6 * (np.sin(2 * np.pi * 90 * t) > 0) * (t < 0.03))
    return n * e
def hat(open_=False):
    t = t_(0.12 if not open_ else 0.25); return hp(rng.standard_normal(len(t)), 7500) * np.exp(-t * (70 if not open_ else 18))
def shaker():
    t = t_(0.09); e = np.minimum(t / 0.015, 1) * np.exp(-t * 45); return hp(rng.standard_normal(len(t)), 5000) * e
def bass(m, d):
    t = t_(d); f = hz(m)
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t)
    e = np.minimum(t / 0.008, 1) * np.exp(-t * 3.2) * np.clip((d - t) / 0.02, 0, 1)
    return lp(s * e, 900)
def epiano(m, d):
    t = t_(d); f = hz(m)
    s = np.sin(2 * np.pi * f * t) + 0.45 * np.sin(4 * np.pi * f * t) * np.exp(-t * 4) + 0.12 * np.sin(6 * np.pi * f * t) * np.exp(-t * 7)
    e = np.minimum(t / 0.01, 1) * np.exp(-t * 1.1) * np.clip((d - t) / 0.08, 0, 1)
    return s * e
def pad(m, d):
    t = t_(d); f = hz(m); s = 0
    for det in (-0.12, 0, 0.12): s = s + np.sin(2 * np.pi * f * (1 + det / 100) * t) + 0.25 * np.sin(4 * np.pi * f * (1 + det / 100) * t)
    e = np.minimum(t / 0.35, 1) * np.clip((d - t) / 0.4, 0, 1)
    return lp(s * e / 3, 2500)
def pluck(m, d=0.6):
    t = t_(d); f = hz(m); s = 0
    for k in range(1, 7): s = s + np.sin(2 * np.pi * f * k * t) * np.exp(-t * (4 + 2.2 * k)) / k
    return s * np.minimum(t / 0.004, 1)
def bell(m, d=1.4):
    t = t_(d); f = hz(m)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 2.2) + 0.5 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 5) + 0.25 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 9)
    return s * np.minimum(t / 0.003, 1)

def reverb(x, secs=1.3, wet=0.25):
    t = t_(secs); ir = rng.standard_normal(len(t)) * np.exp(-t * 4.5); ir = lp(ir, 5000); ir /= np.sqrt(np.sum(ir ** 2))
    return x + wet * fftconvolve(x, ir)[: len(x)]

def master(mix, dur):
    mix = mix[: int(dur * SR)]
    fi = np.minimum(np.arange(len(mix)) / (0.05 * SR), 1)
    fo = np.clip((len(mix) - np.arange(len(mix))) / (1.2 * SR), 0, 1)
    mix = mix * fi * fo
    mix = mix / (np.max(np.abs(mix)) + 1e-9) * 1.25
    mix = np.tanh(mix) / np.tanh(1.25) * 0.89          # gentle soft-clip limiter
    return mix

# ---- songs ----
def upbeat(dur, key=0):
    bpm = 116; b = 60 / bpm; bar = 4 * b
    nb = int(np.ceil(dur / bar)) + 1; L = int((nb * bar + 2) * SR)
    drums = np.zeros(L); bassb = np.zeros(L); keys = np.zeros(L); lead = np.zeros(L); kickenv = np.zeros(L)
    # C G Am F
    prog = [(48, [60, 64, 67]), (43, [59, 62, 67]), (45, [57, 60, 64]), (41, [57, 60, 65])]
    motif = [0, 2, 1, 2, 0, 2, 1, 2]
    for i in range(nb):
        root, ch = prog[i % 4]; root += key; ch = [c + key for c in ch]; s = i * bar
        for q in range(4):
            k = kick(); add(drums, 0.9 * k, s + q * b)
            add(kickenv, np.exp(-t_(0.35) * 9), s + q * b)
        for q in (1, 3):
            add(drums, 0.55 * snare(), s + q * b); add(drums, 0.35 * clap(), s + q * b)
        for e in range(8): add(drums, (0.22 if e % 2 else 0.14) * hat(open_=(e == 7)), s + e * b / 2)
        for e in range(8): add(bassb, 0.55 * bass(root + (12 if e in (3, 7) else 0), b / 2 * 0.95), s + e * b / 2)
        for c in ch: add(keys, 0.16 * epiano(c, bar), s)
        for e in range(8):
            if i == 0 and e < 2: continue
            m = ch[motif[e]] + 12 + (12 if (i % 2 and e >= 6) else 0)
            add(lead, 0.20 * pluck(m), s + e * b / 2)
    duck = 1 - 0.45 * np.clip(kickenv, 0, 1)
    mix = drums + lp(bassb, 1000) + reverb(keys * duck, 1.0, 0.25) + reverb(lead * duck, 1.4, 0.3)
    return master(mix, dur)

def gentle(dur, key=5):
    bpm = 92; b = 60 / bpm; bar = 4 * b
    nb = int(np.ceil(dur / bar)) + 1; L = int((nb * bar + 3) * SR)
    perc = np.zeros(L); bassb = np.zeros(L); pads = np.zeros(L); mel = np.zeros(L)
    # C Am F G (transposed)
    prog = [(36, [60, 64, 67]), (33, [57, 60, 64]), (29, [57, 60, 65]), (31, [59, 62, 67])]
    tune = [[4, 7, 12, 7], [9, 7, 4, 2], [5, 9, 12, 9], [7, 11, 14, 12]]
    for i in range(nb):
        root, ch = prog[i % 4]; root += key; ch = [c + key for c in ch]; s = i * bar
        add(perc, 0.45 * kick(soft=True), s); add(perc, 0.25 * kick(soft=True), s + 2.5 * b)
        for e in range(8): add(perc, (0.10 if e % 2 else 0.06) * shaker(), s + e * b / 2)
        for q in (1, 3): add(perc, 0.10 * clap(), s + q * b)
        add(bassb, 0.5 * bass(root + 12, 2 * b * 0.95), s); add(bassb, 0.4 * bass(root + 12, 2 * b * 0.95), s + 2 * b)
        for c in ch: add(pads, 0.12 * pad(c, bar + 0.3), s)
        if i == 0: continue
        for q, n in enumerate(tune[i % 4]):
            add(mel, 0.22 * bell(60 + key + n + 12), s + q * b)
            if q % 2: add(mel, 0.10 * bell(60 + key + n + 7 + 12), s + q * b + b / 2)
    mix = perc + lp(bassb, 700) + reverb(pads, 1.6, 0.3) + reverb(mel, 1.8, 0.35)
    return master(mix, dur)

if __name__ == "__main__":
    out = "/tmp/claude-0/-home-claude/da0f4f16-de8b-599c-9c43-7f614620f3dd/scratchpad/music/"
    import os; os.makedirs(out, exist_ok=True)
    for name, fn, dur, key in [("gadget", upbeat, 13.9, 0), ("watch", upbeat, 9.0, 2), ("baby", gentle, 12.1, 5)]:
        x = fn(dur, key)
        st = np.stack([x, x], 1)
        # light stereo width: delay right channel a touch
        st[:, 1] = np.concatenate([np.zeros(int(0.012 * SR)), x[: len(x) - int(0.012 * SR)]]) * 0.15 + x * 0.85
        wavfile.write(out + name + ".wav", SR, (st * 32767).astype(np.int16))
        rms = 20 * np.log10(np.sqrt(np.mean(x ** 2)))
        print(name, f"{len(x)/SR:.1f}s peak={20*np.log10(np.max(np.abs(x))):.1f}dBFS rms={rms:.1f}dBFS", flush=True)
