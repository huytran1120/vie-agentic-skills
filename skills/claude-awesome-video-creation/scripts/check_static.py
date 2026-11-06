#!/usr/bin/env python3
"""Find frozen stretches in a rendered film (runs of identical frames >= --min seconds).

A viewer reads a held black/silent beat or a stuck frame as the video buffering ("it stutters at 1:17").
Usage: check_static.py film.mp4 [--min 0.1] [--fps 60]
"""
import argparse
import subprocess
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('video')
ap.add_argument('--min', type=float, default=0.1)
ap.add_argument('--fps', type=float, default=60)
a = ap.parse_args()
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', a.video, '-vf', 'scale=160:90,format=gray', '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
b = np.frombuffer(raw, np.uint8).reshape(-1, 90, 160).astype(float)
d = np.abs(np.diff(b, axis=0)).mean(axis=(1, 2))
runs, s = [], None
for i, x in enumerate(d):
    if x < 0.02:
        s = i if s is None else s
    else:
        if s is not None and (i - s) / a.fps >= a.min:
            runs.append((round((s + 1) / a.fps, 2), round((i + 1) / a.fps, 2)))
        s = None
print(f'{len(b)} frames; static runs >= {a.min}s: {runs if runs else "none"}')
