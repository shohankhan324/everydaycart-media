"""Original 124 BPM dance-pop track: build-up intro, drop on the first product, whooshes on every cut."""
import os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)); _T = _os.path.dirname(_R)

import sys
import numpy as np
sys.path.insert(0, _T)
from make_music import (SR, hz, t_, lp, hp, add, kick, snare, clap, hat, bass, pluck, pad, bell, reverb, master, rng)

BPM = 124; B = 60 / BPM; BAR = 4 * B

def stab(m, d=0.22):
    t = t_(d); env = np.exp(-t * 9) * np.minimum(t / 0.004, 1)
    x = sum(np.sign(np.sin(2 * np.pi * hz(m) * (1 + det) * t)) for det in (-0.006, 0, 0.006)) / 3
    return lp(x * env, 3200)

def riser(d):
    t = t_(d); n = rng.standard_normal(len(t)) * (t / d) ** 2
    return hp(n, 1500) * 0.6

def whoosh(d=0.45):
    t = t_(d); n = rng.standard_normal(len(t)); env = np.sin(np.pi * t / d) ** 2
    return hp(lp(n, 6000), 900) * env * 0.5

def impact():
    t = t_(1.6); return (np.sin(2 * np.pi * 48 * t * (1 + 2 * np.exp(-t * 18))) * np.exp(-t * 3.2)
                         + lp(rng.standard_normal(len(t)), 2500) * np.exp(-t * 7) * 0.4)

def drive(dur, drop, cuts, end_hit, key=0):
    L = int((dur + 3) * SR)
    drums = np.zeros(L); bs = np.zeros(L); keys = np.zeros(L); lead = np.zeros(L); fx = np.zeros(L); env = np.zeros(L)
    # Am F C G
    prog = [(r + key, [c + key for c in ch]) for r, ch in [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [55, 60, 64]), (43, [55, 59, 62])]]
    # intro: filtered stabs + snare roll + riser
    nb_in = int(round(drop / B))
    for q in range(nb_in):
        for c in prog[0][1]: add(keys, 0.12 * stab(c + 12, 0.18), q * B)
    roll = np.linspace(0, drop, 13)[:-1]
    for i, s in enumerate(roll): add(drums, (0.12 + 0.35 * i / len(roll)) * snare(), s)
    add(fx, riser(drop), 0)
    # main groove
    nbar = int(np.ceil((dur - drop) / BAR)) + 1
    hook = [0, 2, 1, 2, 0, 1, 2, 1]
    for i in range(nbar):
        s0 = drop + i * BAR; root, ch = prog[i % 4]
        for q in range(4):
            add(drums, 0.95 * kick(), s0 + q * B); add(env, np.exp(-t_(0.3) * 10), s0 + q * B)
            add(drums, 0.26 * hat(open_=True), s0 + q * B + B / 2)
            add(bs, 0.6 * bass(root, B / 2 * 0.9), s0 + q * B + B / 2)
            for c in ch: add(keys, 0.09 * stab(c + 12), s0 + q * B + B / 2)
        for q in (1, 3): add(drums, 0.45 * clap(), s0 + q * B); add(drums, 0.3 * snare(), s0 + q * B)
        for e in range(16): add(drums, 0.08 * hat(), s0 + e * B / 4)
        for e in range(8):
            if e in (3, 7) and i % 2 == 0: continue
            add(lead, 0.17 * pluck(ch[hook[e]] + 24 - (12 if i % 4 == 3 and e > 4 else 0)), s0 + e * B / 2)
    for c in cuts: add(fx, whoosh(), c - 0.3)
    add(fx, impact() * 0.9, drop); add(fx, impact() * 0.7, end_hit)
    duck = 1 - 0.55 * np.clip(env, 0, 1)
    mix = drums + lp(bs, 900) * duck + reverb(keys * duck, 1.0, 0.22) + reverb(lead * duck, 1.3, 0.3) + fx
    return master(mix, dur)
