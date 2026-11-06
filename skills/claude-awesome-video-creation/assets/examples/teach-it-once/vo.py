#!/usr/bin/env python3
"""
vo.py: the voiceover stage of the build.

1. Parses ../script/voiceover.txt  ->  src/generated/vo_script.json (scene id, window, text).
2. For every scene whose ROOT/audio/vo/vo_SXX.wav is MISSING, generates a draft take with
   edge-tts (en-US-AndrewMultilingualNeural) and converts it to 48 kHz mono WAV.
   An existing file is NEVER overwritten: that is where the student's own recordings go.
   (--force-tts regenerates only files this script wrote itself, tagged in vo_tts.json.)
3. Analyses every take (draft or student): finds the speech onset/offset with an energy gate,
   so a take recorded with 1 s of silence either side still lands its first word on the cue.
   Word timings come from edge-tts word boundaries when the take is our own draft (hash match),
   otherwise they are spread over the detected speech by syllable weight.
4. Writes src/generated/vo.json (consumed by the captions in the picture and by soundtrack.py)
   and warns when a line overruns its scene.

Usage: python scripts/vo.py [--force-tts]
"""
import asyncio
import hashlib
import json
import os
import re
import subprocess
import sys

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
FILM = os.path.dirname(HERE)
ROOT = os.path.dirname(FILM)
VO_TXT = os.path.join(ROOT, 'script', 'voiceover.txt')
VO_DIR = os.path.join(ROOT, 'audio', 'vo')
GEN = os.path.join(FILM, 'src', 'generated')
TTS_LOG = os.path.join(VO_DIR, 'vo_tts.json')
VOICE = 'en-US-AndrewMultilingualNeural'
SR = 48000

# Scene ends (seconds) from the storyboard; a VO may run up to the end of its scene.
SCENE_START = {'S01': 0, 'S02': 6, 'S03': 13, 'S04': 22, 'S05': 33.5, 'S06': 46, 'S07': 58, 'S08': 70, 'S09': 76, 'S10': 81, 'S11': 93.5, 'S12': 99.5}
SCENE_END = {'S01': 6, 'S02': 13, 'S03': 22, 'S04': 33.5, 'S05': 46, 'S06': 58, 'S07': 70, 'S08': 76, 'S09': 81, 'S10': 93.5, 'S11': 99.5, 'S12': 116}

# Spoken forms for the synthetic voice only (captions keep the written text).
SPOKEN = [(r'claude-awesome-video-creation', 'Claude awesome video creation'), (r'SKILL\.md', 'skill dot M D'), (r'^…', ''), (r'…$', '...'), (r' — ', ', ')]


def ts(s):
    m, sec = s.split(':')
    return int(m) * 60 + float(sec)


def parse():
    out = []
    for line in open(VO_TXT, encoding='utf-8'):
        m = re.match(r'\[(S\d\d)\]\s*\(([\d:.]+)-([\d:.]+)\)\s*(.+?)\s*\|\s*\d+\s*$', line.strip())
        if m:
            sid, a, b, text = m.groups()
            out.append({'id': sid, 'start': ts(a), 'end': ts(b), 'sceneEnd': SCENE_END[sid], 'text': text.strip()})
    if len(out) != 12:
        sys.exit(f'vo.py: expected 12 VO lines in {VO_TXT}, found {len(out)}')
    return out


def sha(path):
    return hashlib.sha1(open(path, 'rb').read()).hexdigest()


# Draft-only pacing: the long lines are read a little faster so they sit inside their windows.
RATE = {}


async def tts(text, mp3, sid=''):
    import edge_tts
    spoken = text
    for a, b in SPOKEN:
        spoken = re.sub(a, b, spoken)
    com = edge_tts.Communicate(spoken.strip(), VOICE, rate=RATE.get(sid, '+11%'), pitch='-3Hz', boundary='WordBoundary')
    words = []
    with open(mp3, 'wb') as fh:
        async for ch in com.stream():
            if ch['type'] == 'audio':
                fh.write(ch['data'])
            elif ch['type'] == 'WordBoundary':
                words.append({'w': ch['text'], 't0': ch['offset'] / 1e7, 't1': (ch['offset'] + ch['duration']) / 1e7})
    return words


def speech_span(x, sr):
    """Onset/offset (s) of speech: 10 ms RMS frames, gate at max(-48 dBFS, peak-40 dB)."""
    if x.ndim > 1:
        x = x.mean(axis=1)
    hop = int(sr * 0.01)
    n = len(x) // hop
    if n == 0:
        return 0.0, len(x) / sr
    rms = np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    gate = max(-48.0, db.max() - 40.0)
    on = np.where(db > gate)[0]
    if len(on) == 0:
        return 0.0, len(x) / sr
    return max(0.0, on[0] * 0.01 - 0.02), min(len(x) / sr, (on[-1] + 1) * 0.01 + 0.05)


def syllables(w):
    w = re.sub(r'[^a-z]', '', w.lower())
    return max(1, len(re.findall(r'[aeiouy]+', w)))


def spread(text, a, b):
    """Fallback word timing over [a, b]: syllable-weighted, with small gaps after punctuation."""
    toks = text.split()
    wts = [syllables(t) + (0.8 if re.search(r'[.,:;!?…—]$', t) else 0) for t in toks]
    tot = sum(wts)
    t, out = a, []
    for tok, wgt in zip(toks, wts):
        d = (b - a) * wgt / tot
        out.append({'w': tok, 't0': round(t, 3), 't1': round(t + d * 0.85, 3)})
        t += d
    return out


def align_written(text, spoken_words, a, b):
    """Map edge-tts boundaries (spoken tokens) back onto the written tokens shown in captions."""
    toks = text.split()
    if not spoken_words:
        return spread(text, a, b)
    # SKILL.md is spoken as 3 tokens; greedy match by normalised prefix, else proportional fallback
    norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
    out, j = [], 0
    for tok in toks:
        nt = norm(tok)
        if not nt:  # a bare dash or ellipsis
            continue
        if j >= len(spoken_words):
            return spread(text, a, b)
        start = spoken_words[j]
        if nt == 'skillmd':
            end = spoken_words[min(j + 3, len(spoken_words)) - 1]
            j += 4 if j + 3 < len(spoken_words) and norm(spoken_words[j + 3]['w']) == 'd' else 3
            # "skill dot M D" -> 4 boundaries
        else:
            end = start
            j += 1
        out.append({'w': tok, 't0': round(start['t0'], 3), 't1': round(end['t1'], 3)})
    return out


def main():
    force = '--force-tts' in sys.argv
    os.makedirs(VO_DIR, exist_ok=True)
    os.makedirs(GEN, exist_ok=True)
    lines = parse()
    json.dump(lines, open(os.path.join(GEN, 'vo_script.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    log = json.load(open(TTS_LOG)) if os.path.exists(TTS_LOG) else {}
    warnings = []
    result = []
    for L in lines:
        wav = os.path.join(VO_DIR, f"vo_{L['id']}.wav")
        ours = L['id'] in log and os.path.exists(wav) and log[L['id']].get('sha') == sha(wav)
        if not os.path.exists(wav) or (force and ours):
            mp3 = wav[:-4] + '.tts.mp3'
            print(f"vo.py: generating draft TTS for {L['id']} ({VOICE})")
            words = asyncio.run(tts(L['text'], mp3, L['id']))
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp3, '-ac', '1', '-ar', str(SR), '-c:a', 'pcm_s24le', wav], check=True)
            os.remove(mp3)
            log[L['id']] = {'sha': sha(wav), 'voice': VOICE, 'words': words}
            json.dump(log, open(TTS_LOG, 'w'), indent=1)
            ours = True
        x, sr = sf.read(wav, always_2d=False)
        dur = len(x) / sr
        on, off = speech_span(x, sr)
        source = 'tts-draft' if ours else 'recorded'
        if ours:
            words = align_written(L['text'], log[L['id']]['words'], on, off)
        else:
            words = spread(L['text'], on, off)
        speech = off - on
        # S08 must be done before the suck-in to the drop (75.1 s)
        limit = 75.05 if L['id'] == 'S08' else L['sceneEnd'] - 0.15
        land_end = L['start'] + speech
        at = L['start']
        if land_end > limit:
            at = max(SCENE_START[L['id']] + 0.1, limit - speech)
        if land_end > limit:
            warnings.append(f"{L['id']}: speech is {speech:.2f}s and would end at {land_end:.2f}s, past its scene end {L['sceneEnd']}s; "
                            f"it will be started earlier (fit) - consider a shorter take")
        elif land_end > L['end'] + 0.6:
            warnings.append(f"{L['id']}: speech ends at {land_end:.2f}s, after its planned window end {L['end']}s (still inside the scene)")
        result.append({**L, 'file': f"vo_{L['id']}.wav", 'source': source, 'sr': sr, 'dur': round(dur, 3),
                       'onset': round(on, 3), 'offset': round(off, 3), 'at': round(at, 3),
                       'words': [{'w': w['w'], 't0': round(at + w['t0'] - on, 3), 't1': round(at + w['t1'] - on, 3)} for w in words]})
    json.dump({'voice': VOICE, 'lines': result}, open(os.path.join(GEN, 'vo.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    for w in warnings:
        print('vo.py: WARNING ' + w)
    print(f"vo.py: {sum(r['source'] == 'recorded' for r in result)} recorded + {sum(r['source'] == 'tts-draft' for r in result)} draft takes -> src/generated/vo.json")


if __name__ == '__main__':
    main()
