#!/usr/bin/env python3
"""Original score (calm arrangement) + SFX + voiceover mix for "Teach It Once", all synthesised in code.

Reads out/events.json (written by scripts/events.ts from the same timeline the picture uses) and
the VO takes in ../audio/vo/, and writes public/audio/soundtrack.wav (48 kHz, 24-bit stereo).

Music: 120 BPM, A minor, Am-F-C-G (one chord per 2 s bar). Structure (design_system.md):
pad from the enter key (3.5 s) -> filtered kick 10 s -> groove 22 s -> stripped 42 s ->
groove to S06 -> build S07-S08 -> riser (music out, riser on) -> DROP (S09) -> resolve from S11 ->
final Am(add9) rings out, silent by 114 s.
Mix: music ducked -12 dB under the voice (60 ms attack, 300 ms release), SFX ~6 dB under the
voice, master -14 LUFS integrated, true peak <= -1 dBTP.

No samples, loops or third-party audio: every sound below is generated from oscillators and noise.
"""
import json
import os
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy import signal

HERE = os.path.dirname(os.path.abspath(__file__))
FILM = os.path.dirname(HERE)
ROOT = os.path.dirname(FILM)
SR = 48000
BPM = 120
BEAT = 60 / BPM
BAR = 4 * BEAT
rng = np.random.default_rng(4431)

ev = json.load(open(os.path.join(FILM, 'out', 'events.json')))
TOTAL = ev['total']
N = int(round(TOTAL * SR))
CUE = ev['cue']
DROP = CUE["drop"]  # 80.0 (v2)
BLACK = CUE['s08Black']  # music drops out here, the riser carries on to the drop
SC = ev['scene']
S06, S07, S10, S11, S12 = (SC[k]['from'] for k in ('s06', 's07', 's10', 's11', 's12'))  # 50, 60, 86, 100, 108 s


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def t_(dur):
    return np.arange(int(dur * SR)) / SR


def place(buf, x, at, gain=1.0, pan=0.0):
    """Add mono or stereo x into stereo buf at time `at` (s) with equal-power pan."""
    i = int(round(at * SR))
    if i >= buf.shape[0] or len(x) == 0:
        return
    if i < 0:
        x = x[-i:]
        i = 0
    n = min(len(x), buf.shape[0] - i)
    if x.ndim == 1:
        a = (pan + 1) * np.pi / 4
        buf[i:i + n, 0] += x[:n] * gain * np.cos(a) * np.sqrt(2) * 0.7071
        buf[i:i + n, 1] += x[:n] * gain * np.sin(a) * np.sqrt(2) * 0.7071
    else:
        buf[i:i + n] += x[:n] * gain


def lp(x, fc, order=2):
    fc = min(fc, SR / 2 * 0.95)
    return signal.sosfilt(signal.butter(order, fc, 'low', fs=SR, output='sos'), x, axis=0)


def hp(x, fc, order=2):
    return signal.sosfilt(signal.butter(order, fc, 'high', fs=SR, output='sos'), x, axis=0)


def bp(x, lo, hi, order=2):
    return signal.sosfilt(signal.butter(order, [lo, hi], 'band', fs=SR, output='sos'), x, axis=0)


def env(n, a=0.005, d=0.2, s=0.0, r=0.0, total=None):
    """Attack / exponential decay envelope of n samples."""
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * (s + (1 - s) * np.exp(-np.maximum(0, t - a) / max(d, 1e-4)))
    if r > 0:
        rn = int(r * SR)
        e[-rn:] *= np.linspace(1, 0, rn)
    return e


def saw(f, t, detune=0.0):
    ph = (f * (1 + detune)) * t
    return 2 * (ph - np.floor(ph + 0.5))


# ---------------------------------------------------------------------------------------------
# Instruments
# ---------------------------------------------------------------------------------------------
def kick(gain=1.0):
    t = t_(0.45)
    f = 45 + 95 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * np.exp(-t / 0.13)
    return lp(x, 900) * gain


def clap():
    t = t_(0.25)
    n = rng.standard_normal(len(t))
    e = np.zeros(len(t))
    for k, off in enumerate([0, 0.011, 0.022]):
        i = int(off * SR)
        e[i:] += np.exp(-(t[: len(t) - i]) / (0.008 if k < 2 else 0.09))
    return bp(n * e, 900, 3500) * 0.9


def hat(dec=0.035):
    t = t_(0.12)
    return hp(rng.standard_normal(len(t)), 7000) * np.exp(-t / dec) * 0.5


def snare():
    t = t_(0.2)
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05) * 0.5
    nz = bp(rng.standard_normal(len(t)), 1500, 8000) * np.exp(-t / 0.07)
    return body + nz * 0.8


def pluck(m, dur=0.35, bright=3500):
    t = t_(dur)
    f = midi(m)
    x = (saw(f, t) + 0.5 * saw(f, t, 0.004)) * np.exp(-t / 0.12)
    return lp(x, bright) * 0.35


def bass(m, dur, cutoff=500):
    t = t_(dur)
    f = midi(m)
    x = 0.7 * np.sin(2 * np.pi * f * t) + 0.35 * saw(f, t)
    x = lp(x, cutoff) * env(len(t), 0.004, dur * 0.8, 0.6, 0.02)
    return x * 0.55


def pad(notes, dur, cutoff=1400, att=0.6, rel=0.6):
    t = t_(dur)
    x = np.zeros(len(t))
    for m in notes:
        f = midi(m)
        for d in (-0.003, 0.0, 0.0035):
            x += saw(f, t, d) + 0.0 * t
    x = lp(x / (3 * len(notes)), cutoff, 2)
    e = np.minimum(1, t / att) * np.minimum(1, (dur - t) / rel)
    return x * np.clip(e, 0, 1) * 0.5


def lead(m, dur):
    t = t_(dur)
    f = midi(m)
    x = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.3) + 0.08 * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t / 0.15)
    return x * env(len(t), 0.02, 0.6, 0.0, 0.05) * 0.28


# ---------------------------------------------------------------------------------------------
# SFX
# ---------------------------------------------------------------------------------------------
def sfx(kind, dur=None):
    if kind == 'key':
        t = t_(0.03)
        p = 2 ** (rng.uniform(-2, 2) / 12)
        x = bp(rng.standard_normal(len(t)), 2500 * p, 6500 * p) * np.exp(-t / 0.005)
        return x * 0.5 + np.sin(2 * np.pi * 1800 * p * t) * np.exp(-t / 0.004) * 0.2
    if kind == 'tick':
        t = t_(0.04)
        return np.sin(2 * np.pi * 3200 * t) * np.exp(-t / 0.006) * 0.5
    if kind == 'thock':
        t = t_(0.3)
        low = np.sin(2 * np.pi * (90 + 60 * np.exp(-t / 0.02)) * t) * np.exp(-t / 0.07)
        click = bp(rng.standard_normal(len(t)), 800, 3000) * np.exp(-t / 0.01)
        return low * 0.9 + click * 0.5
    if kind == 'burst':
        t = t_(0.07)
        return rng.standard_normal(len(t)) * np.exp(-t / 0.025) * 0.35
    if kind == 'sub':
        t = t_(1.6)
        return np.sin(2 * np.pi * (41 + 20 * np.exp(-t / 0.08)) * t) * np.exp(-t / 0.5) * 0.9
    if kind == 'whoosh':
        d = dur or 0.5
        t = t_(d)
        n = rng.standard_normal(len(t))
        e = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
        # sweep a band-pass up through the noise
        out = np.zeros(len(t))
        seg = 8
        for k in range(seg):
            a, b = k * len(t) // seg, (k + 1) * len(t) // seg
            fc = 400 * (12 ** (k / (seg - 1)))
            out[a:b] = bp(n, fc * 0.7, min(fc * 1.4, 20000))[a:b]
        return out * e * 0.6
    if kind == 'ting':
        t = t_(1.2)
        return (np.sin(2 * np.pi * 2400 * t) + 0.3 * np.sin(2 * np.pi * 4810 * t)) * np.exp(-t / 0.3) * 0.25
    if kind == 'rim':
        t = t_(0.08)
        return (np.sin(2 * np.pi * 1700 * t) * 0.5 + bp(rng.standard_normal(len(t)), 1500, 5000)) * np.exp(-t / 0.012) * 0.6
    if kind == 'stutter':
        t = t_(0.24)
        base = np.sin(2 * np.pi * 330 * t * (1 + 0.6 * t)) * np.exp(-t / 0.2)
        gate = (np.floor(t / 0.03) % 2 == 0).astype(float)
        return (base * gate + bp(rng.standard_normal(len(t)), 800, 3000) * gate * 0.2) * 0.4
    if kind == 'swell':
        d = dur or 1.4
        t = t_(d)
        return bp(rng.standard_normal(len(t)), 600, 4000) * (t / d) ** 2 * np.exp(-np.maximum(0, t - d * 0.85) / 0.05) * 0.3
    if kind == 'unfold':
        d = dur or 0.4
        t = t_(d)
        return lp(rng.standard_normal(len(t)), 1500) * np.sin(np.pi * t / d) * 0.5
    if kind == 'scratch':
        t = t_(0.22)
        return bp(rng.standard_normal(len(t)), 2500, 7000) * np.sin(np.pi * t / 0.22) * (0.6 + 0.4 * np.sin(2 * np.pi * 30 * t)) * 0.25
    if kind == 'ping':
        t = t_(0.8)
        return np.sin(2 * np.pi * 1320 * t) * np.exp(-t / 0.18) * 0.3
    if kind == 'latch':
        t = t_(0.12)
        a = np.sin(2 * np.pi * 700 * t) * np.exp(-t / 0.015)
        b = np.zeros(len(t))
        i = int(0.035 * SR)
        b[i:] = np.sin(2 * np.pi * 1100 * t[: len(t) - i]) * np.exp(-t[: len(t) - i] / 0.012)
        return (a + b) * 0.5
    if kind == 'bloop':
        t = t_(0.12)
        return np.sin(2 * np.pi * (500 + 500 * t / 0.12) * t) * np.exp(-t / 0.04) * 0.4
    if kind == 'ding':
        t = t_(1.0)
        return (np.sin(2 * np.pi * midi(88) * t) + 0.5 * np.sin(2 * np.pi * midi(95) * t)) * np.exp(-t / 0.25) * 0.22
    if kind == 'tapestop':
        t = t_(0.3)
        f = 600 * np.exp(-t / 0.08) + 40
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.15) * 0.4
    if kind == 'whirr':
        d = dur or 10
        t = t_(d)
        f = 80 * (1 + 4 * (t / d) ** 2)
        x = saw(1, np.cumsum(f) / SR) * 0.3 + bp(rng.standard_normal(len(t)), 300, 5000) * 0.4
        y = np.zeros(len(t))
        for k in range(12):
            a, b = k * len(t) // 12, (k + 1) * len(t) // 12
            y[a:b] = lp(x, 600 + 6000 * (k / 11) ** 2)[a:b]
        return y * (t / d) ** 1.5 * 0.4
    if kind == 'boom':
        t = t_(2.5)
        x = np.sin(2 * np.pi * (38 + 40 * np.exp(-t / 0.06)) * t) * np.exp(-t / 0.7)
        return x + lp(rng.standard_normal(len(t)), 600) * np.exp(-t / 0.05) * 0.4
    if kind == 'pluck':
        return pluck(rng.choice([69, 72, 76, 79]) + 12, 0.5, 5000) * 1.2
    if kind == 'shimmer':
        d = dur or 1.6
        t = t_(d)
        x = sum(np.sin(2 * np.pi * midi(m) * t + k) for k, m in enumerate([81, 84, 88, 91]))
        return x * np.sin(np.pi * t / d) ** 2 * 0.06
    raise ValueError(kind)


# ---------------------------------------------------------------------------------------------
# Score
# ---------------------------------------------------------------------------------------------
CHORDS = [  # (bass root, pad voicing) Am F C G
    (45, [57, 60, 64, 69]),
    (41, [57, 60, 65, 69]),
    (48, [55, 60, 64, 67]),
    (43, [55, 59, 62, 67]),
]
ARP = [[69, 72, 76, 72], [69, 72, 77, 72], [67, 72, 76, 72], [67, 71, 74, 71]]


def chord_at(t):
    return int(t // BAR) % 4


def build_music():
    drums = np.zeros((N, 2))
    tonal = np.zeros((N, 2))
    padbus = np.zeros((N, 2))
    kicks = []
    enter = CUE['s01Enter']
    # 3.5 -> 10: one sustained A
    place(padbus, pad([45, 57], 10.0 - enter + 0.6, cutoff=700, att=0.8, rel=0.6), enter, 0.9)
    # pad chords 10 -> S06, S06 -> S07 (breakdown), S07 -> BLACK, DROP -> S12
    def pad_run(t0, t1, cutoff, g):
        b = np.floor(t0 / BAR) * BAR
        while b < t1 - 1e-6:
            s, e = max(b, t0), min(b + BAR, t1)
            notes = CHORDS[chord_at(b)][1]
            place(padbus, pad(notes, e - s + 0.25, cutoff=cutoff, att=0.15, rel=0.25), s, g)
            b += BAR
    pad_run(10.0, S06, 1100, 0.85)
    pad_run(S06, S07, 700, 0.8)
    pad_run(S07, BLACK, 1200, 0.85)
    pad_run(DROP, S12, 1500, 0.95)
    # kicks
    def kick_run(t0, t1, g=1.0):
        t = t0
        while t < t1 - 1e-6:
            kicks.append((t, g))
            t += 2 * BEAT  # half-time: a calmer pulse on beats 1 and 3
    kick_run(10.0, S06, 0.55)
    kick_run(S07, BLACK, 0.6)
    kick_run(DROP, S11, 0.75)
    kick_run(S11, S12 - 4.0, 0.4)
    kbuf = np.zeros((N, 2))
    for t, g in kicks:
        place(kbuf, kick(g), t, 0.9)
    # filtered kick 10-14 s: low-pass that opens 400 Hz -> 2 kHz across S03's first 2 s
    i0, i1, i2 = int(10 * SR), int(12 * SR), int(14 * SR)
    kbuf[i0:i1] = lp(kbuf[i0:i1], 400)
    seg = kbuf[i1:i2].copy()
    kbuf[i1:i2] = 0.5 * lp(seg, 700) + 0.5 * seg * np.linspace(0, 1, i2 - i1)[:, None]
    drums += kbuf
    # a soft shaker on 8ths in the drop only
    t, k = DROP, 0
    while t < S11:
        place(drums, hat(0.025), t, 0.1 if k % 2 else 0.14, 0.3 if k % 2 else -0.3)
        t += BEAT / 2
        k += 1
    # pluck arp (8ths) 12 -> S06, S07 -> BLACK, DROP -> S11
    for t0, t1, g in [(12.0, S06, 0.55), (S07, BLACK, 0.55), (DROP, S11, 0.5)]:
        t, k = t0, 0
        while t < t1 - 1e-6:
            notes = ARP[chord_at(t)]
            cut = 1200 if t < 14 else 2000
            place(tonal, pluck(notes[k % 4], 0.5, cut), t, g * 0.6, 0.3 if k % 2 else -0.3)
            t += BEAT / 2
            k += 1
    # bass: 22 -> S06, S07 -> BLACK, the drop, roots only in the resolve
    for t0, t1, step in [(22.0, S06, BAR), (S07, BLACK, BAR), (DROP, S11, BAR), (S11, S12, BAR)]:
        t = t0
        while t < t1 - 1e-6:
            root = CHORDS[chord_at(t)][0]
            d = min(step * 0.97, t1 - t)
            place(tonal, bass(root, d, 320), t, 0.9)
            t += step
    # riser: 7.5 s up to BLACK (noise, rising band)
    RISE = BLACK - 7.5
    d = BLACK - RISE
    tt = t_(d)
    nz = rng.standard_normal(len(tt))
    out = np.zeros(len(tt))
    for k in range(16):
        a, b = k * len(tt) // 16, (k + 1) * len(tt) // 16
        fc = 300 * (25 ** (k / 15))
        out[a:b] = bp(nz, fc * 0.6, min(fc * 1.6, 20000))[a:b]
    place(tonal, lp(out, 3000) * (tt / d) ** 2 * 0.12, RISE)
    # lead hook A-C-E-G in the drop: once per 2 bars, answered an octave up
    hook = [69, 72, 76, 79]
    t = DROP
    while t < S11 - 1e-6:
        bar_i = int(round((t - DROP) / BAR))
        if bar_i % 2 == 0:
            for k, m in enumerate(hook):
                place(tonal, lead(m + (12 if bar_i % 4 == 2 else 0), BEAT * 0.9), t + k * BEAT, 1.0, 0.1)
        t += BAR
    # the final chord: Am(add9), rings out from 106 s, silent before 114 s
    fin = pad([45, 57, 60, 64, 71, 69], TOTAL - S12 - 2.8, cutoff=1800, att=0.3, rel=4.5)
    place(padbus, fin, S12, 1.1)
    place(tonal, bass(45, 4.0, 300), S12, 0.8)

    # sidechain: pad ducks under every kick in the drop (and gently elsewhere)
    sc = np.ones(N)
    for t, g in kicks:
        i = int(t * SR)
        n = int(0.3 * SR)
        depth = 0.25 if DROP <= t < S11 else 0.1
        curve = 1 - depth * np.exp(-np.arange(n) / (0.08 * SR))
        j = min(N, i + n)
        sc[i:j] = np.minimum(sc[i:j], curve[: j - i])
    padbus *= sc[:, None]
    music = drums + tonal + padbus
    # simple stereo room
    music = music + 0.22 * reverb(music)
    # the music drops out for the last beat before the drop (the riser SFX carries on)
    a, b = int(BLACK * SR), int(DROP * SR)
    fade = int(0.012 * SR)
    music[a - fade:a] *= np.linspace(1, 0, fade)[:, None]
    music[a:b] = 0
    # end: silent by the last frame
    e0 = int((TOTAL - 0.6) * SR)
    music[e0:] *= np.linspace(1, 0, N - e0)[:, None] ** 2
    return music


def comb(x, k, g):
    """y[n] = x[n] + g * y[n - k], computed a block of k samples at a time."""
    y = np.copy(x)
    for i in range(k, len(x), k):
        j = min(len(x), i + k)
        y[i:j] += g * y[i - k:j - k]
    return y


def reverb(x):
    """Tiny feedback-comb reverb (decorrelated L/R)."""
    out = np.zeros_like(x)
    for ch, delays in enumerate([(0.029, 0.037, 0.041, 0.053), (0.031, 0.039, 0.047, 0.059)]):
        y = np.zeros(x.shape[0])
        for d in delays:
            y += comb(x[:, ch], int(d * SR), 0.72)
        out[:, ch] = lp(y / len(delays), 4500)
    return out


def build_sfx():
    buf = np.zeros((N, 2))
    for e in ev['events']:
        x = sfx(e['kind'], e.get('dur'))
        at = e['t']
        if e['kind'] == 'whoosh':
            at -= len(x) / SR * 0.6  # apex lands on the cue
        if e['kind'] == 'whirr':
            pass
        place(buf, x, at, e.get('gain', 1.0), e.get('pan', 0.0))
    return buf


def build_vo():
    buf = np.zeros((N, 2))
    env_ = np.zeros(N)
    for l in ev['vo']:
        x, sr = sf.read(os.path.join(ROOT, 'audio', 'vo', l['file']), always_2d=False)
        if x.ndim > 1:
            x = x.mean(axis=1)
        if sr != SR:
            x = signal.resample_poly(x, SR, sr)
        at = l['at'] - l['onset']
        place(buf, x, at, 1.0, 0.0)
        i = int(at * SR)
        a = np.abs(x)
        env_[i:i + len(a)] = np.maximum(env_[i:i + len(a)], a[: max(0, min(len(a), N - i))])
    return buf, env_


def duck_curve(vo_env, depth_db=-12.0, att=0.06, rel=0.3):
    """Gain curve for the music: depth_db while the voice speaks (60 ms attack, 300 ms release)."""
    hop = 240  # 5 ms
    frames = vo_env[: len(vo_env) // hop * hop].reshape(-1, hop).max(axis=1)
    active = (frames > 0.02).astype(float)
    # hold 120 ms so words don't pump between syllables
    holdn = int(0.12 / (hop / SR))
    active = np.convolve(active, np.ones(holdn), 'full')[: len(active)] > 0
    target = np.where(active, 10 ** (depth_db / 20), 1.0)
    g = np.ones(len(target))
    ka = 1 - np.exp(-(hop / SR) / att)
    kr = 1 - np.exp(-(hop / SR) / rel)
    for i in range(1, len(target)):
        k = ka if target[i] < g[i - 1] else kr
        g[i] = g[i - 1] + (target[i] - g[i - 1]) * k
    curve = np.repeat(g, hop)
    return np.concatenate([curve, np.full(N - len(curve), curve[-1])])


def limiter(x, ceiling_db=-1.2, look=0.004, release=0.08):
    ceil = 10 ** (ceiling_db / 20)
    # 4x oversampled peak estimate for true peak
    up = signal.resample_poly(np.abs(x).max(axis=1), 4, 1)
    peak = up.reshape(-1, 4).max(axis=1)[: x.shape[0]]
    peak = np.concatenate([peak, np.zeros(x.shape[0] - len(peak))])
    need = np.minimum(1.0, ceil / np.maximum(peak, 1e-9))
    lk = int(look * SR)
    # look-ahead minimum, then smooth release
    m = np.copy(need)
    for s_ in range(1, lk + 1):
        m[:-s_] = np.minimum(m[:-s_], need[s_:])
    g = np.empty_like(m)
    g[0] = m[0]
    kr = 1 - np.exp(-1 / (release * SR))
    for i in range(1, len(m)):
        g[i] = m[i] if m[i] < g[i - 1] else g[i - 1] + (m[i] - g[i - 1]) * kr
    return x * g[:, None]


def true_peak_db(x):
    up = signal.resample_poly(x, 4, 1, axis=0)
    return 20 * np.log10(np.abs(up).max() + 1e-12)


def main():
    print('music…', flush=True)
    music = build_music()
    print('sfx…', flush=True)
    fx = build_sfx()
    print('vo…', flush=True)
    vo, vo_env = build_vo()
    duck = duck_curve(vo_env)
    # balance: voice is the reference; music bed and sfx sit under it
    meter = pyln.Meter(SR)
    vo_l = meter.integrated_loudness(vo)
    mu_l = meter.integrated_loudness(music)
    fx_l = meter.integrated_loudness(fx)
    music *= 10 ** ((vo_l - 6 - mu_l) / 20)  # undocked music ~6 LU under the voice ...
    # the drop is the loudest moment of the film: +4 dB on the music from 78 s to the S10 voice
    boost = np.ones(N)
    a, b = int(DROP * SR), int((S10 + 0.4) * SR)
    boost[a:b] = 10 ** (2 / 20)
    r = int(0.4 * SR)
    boost[b:b + r] = np.linspace(10 ** (2 / 20), 1, r)
    music *= boost[:, None]
    music *= duck[:, None]  # ... and -12 dB more while it speaks
    fx *= 10 ** ((vo_l - 8 - fx_l) / 20)
    mix = vo + music + fx
    # master: -14 LUFS integrated, true peak <= -1 dBTP
    for _ in range(3):
        l = meter.integrated_loudness(mix)
        mix *= 10 ** ((-14.0 - l) / 20)
        mix = limiter(mix, -1.8)
    l = meter.integrated_loudness(mix)
    tp = true_peak_db(mix)
    out = os.path.join(FILM, 'public', 'audio', 'soundtrack.wav')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    sf.write(out, mix.astype(np.float32), SR, subtype='PCM_24')
    stems = os.path.join(FILM, 'out', 'stems')
    os.makedirs(stems, exist_ok=True)
    for name, x in [('music', music), ('sfx', fx), ('vo', vo)]:
        sf.write(os.path.join(stems, f'{name}.wav'), x.astype(np.float32), SR, subtype='FLOAT')
    print(f'{out}\n  {TOTAL:.3f} s, {l:.2f} LUFS integrated, true peak {tp:.2f} dBTP')
    if abs(l + 14) > 0.5 or tp > -1.0:
        print('  WARNING: loudness/peak outside target', file=sys.stderr)


if __name__ == '__main__':
    main()
