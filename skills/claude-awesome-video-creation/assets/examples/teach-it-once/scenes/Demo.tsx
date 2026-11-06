// S06 install, S07 the prompt, S08 render timelapse, S09 the reveal (drop).
// The terminals here are RECONSTRUCTED mockups unless the real clip exists in public/clips/.
import React from 'react';
import { AbsoluteFill, Freeze, OffthreadVideo, staticFile, useCurrentFrame } from 'remotion';
import { a, C } from '../brand/tokens';
import { CLIPS, hasClip, RENDER_SECONDS, type Clip } from '../footage';
import { PROMPT_FULL, rnd, S06_CMD, S06_KEYS, S07_CARDS, S07_ENTER, S07_FAST, S07_FILES, S07_KEYS, typed } from '../schedule';
import SOURCE_LINES from '../generated/source_lines.json';
import { CUE, FPS, SCENE, TOTAL, voAt } from '../timeline';
import { Badge, Caret, Center, clamp, enter, EZ, glow, HBlur, lmix, mix, mono, p, pulse, Recon, Rise, sans, serif, Sh, whipIn, whipOut, Win } from '../ui';
import { S03 } from './Open';
import { S02 } from './Open';
import { S04, S05 } from './Explain';
import { S10, S11, S12 } from './Close';

const ClipVideo: React.FC<{ clip: Clip }> = ({ clip }) => (
  <OffthreadVideo src={staticFile(clip.file)} startFrom={Math.round(clip.start * FPS)} playbackRate={clip.rate} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
);

/** Wrap text to `cols` characters, breaking at spaces. */
const wrap = (text: string, cols: number) => {
  const out: string[] = [];
  let line = '';
  for (const w of text.split(' ')) {
    if ((line + ' ' + w).trim().length > cols) {
      out.push(line);
      line = w;
    } else line = (line + ' ' + w).trim();
  }
  if (line) out.push(line);
  return out;
};

// ---------------------------------------------------------------------------------------------
// S06: install a community skill (Clip A slot).
// ---------------------------------------------------------------------------------------------
const S06_OUT = [
  'Cloning github.com/HaochenSHI66/claude-awesome-video-creation',
  'Found 1 skill: claude-awesome-video-creation',
  'Target agent: Claude Code',
  '→ .claude/skills/claude-awesome-video-creation',
  '✓ Installed 1 skill',
];
export const S06_OUT_AT = (i: number) => CUE.s06Fast + 8 + i * 9;
const S06_INSTALL: [string, string, number][] = [
  ['macOS · Linux · WSL', '% curl -fsSL https://claude.ai/install.sh | bash', 0],
  ['Windows PowerShell', 'PS> irm https://claude.ai/install.ps1 | iex', 18],
  ['then, in your project folder', '% cd my-project && claude', -1],
];

const StepHead: React.FC<{ n: string; title: string; f: number; at: number; hue?: string }> = ({ n, title, f, at, hue = C.ember }) => (
  <div style={{ display: 'flex', alignItems: 'baseline', gap: 20, ...enter(f, at, 26, 18, 0) }}>
    <span style={{ ...mono(26, 700), color: C.ink, padding: '6px 14px', borderRadius: 8, background: hue, boxShadow: `0 0 30px ${a(hue, 0.45)}`, letterSpacing: '0.08em' }}>STEP {n}</span>
    <Rise text={title} f={f} at={at + 4} style={{ ...sans(48, 600) }} />
  </div>
);

export const S06: React.FC = () => {
  const f = useCurrentFrame();
  const L = (x: number) => x - SCENE.s06.from;
  const end = SCENE.s06.dur;
  const pushIn = p(f, end - 26, end, EZ.in);
  const step2 = L(CUE.s06Step2);
  const swing = p(f, step2 - 6, step2 + 34, EZ.cam);
  const n = typed(S06_KEYS.map(L), f);
  const fast = f >= L(CUE.s06Fast) && f < L(CUE.s06Done);
  const real = hasClip(CLIPS.A);
  const leftDim = 1 - 0.45 * p(f, step2, step2 + 20);
  const TW = 840;
  const TH = 470;
  return (
    <AbsoluteFill style={{ background: C.ink }}>
      <AbsoluteFill style={{ transformOrigin: '1410px 520px', transform: `scale(${lmix(1, 1.3, pushIn)})` }}>
        {/* STEP 1: install Claude Code */}
        <div style={{ position: 'absolute', left: 96, top: 120, width: 820, opacity: leftDim }}>
          <StepHead n="1/3" title="Install Claude Code" f={f} at={L(CUE.s06Step1)} hue={C.cyan} />
          {S06_INSTALL.map(([label, cmd, off], i) => {
            const at = off >= 0 ? L(CUE.s06Cmd1) + off : L(CUE.s06Cmd3);
            const lit = p(f, at, at + 14) * (1 - 0.6 * p(f, at + 90, at + 110));
            return (
              <div key={i} style={{ marginTop: i === 2 ? 44 : 30, ...enter(f, at, 24, 16, 0) }}>
                <div style={{ ...sans(24, 500), color: C.muted, marginBottom: 10 }}>{label}</div>
                <div style={{ ...mono(26, 500), color: C.text, padding: '16px 20px', borderRadius: 12, background: C.surface, border: `1.5px solid ${lit > 0.05 ? a(C.cyan, 0.25 + 0.6 * lit) : C.line2}`, boxShadow: lit > 0.05 ? `0 0 30px ${a(C.cyan, 0.15 * lit)}` : undefined, whiteSpace: 'pre' }}>
                  <Sh text={cmd} />
                </div>
              </div>
            );
          })}
          <div style={{ marginTop: 30, width: 800, ...sans(23, 400), whiteSpace: 'normal', lineHeight: 1.45, color: C.muted, ...enter(f, L(CUE.s06Login), 26, 12, 0) }}>
            Log in in the browser. Needs a Claude <span style={{ color: C.text }}>Pro, Max, Team, Enterprise</span> or <span style={{ color: C.text }}>API (Console)</span> account. The free plan has no Claude Code.
          </div>
        </div>
        {/* STEP 2: add a skill (Clip A slot) */}
        <div style={{ position: 'absolute', left: 990, top: 120, width: TW }}>
          <StepHead n="2/3" title="Add a skill" f={f} at={step2 - 10} hue={C.violet} />
          <div
            style={{
              marginTop: 30,
              width: TW,
              height: TH,
              opacity: clamp(swing * 2.2),
              transformOrigin: '50% 60%',
              transform: `perspective(2000px) translateZ(${(1 - swing) * -300}px) translateY(${(1 - swing) * 90}px) rotateX(${(1 - swing) * 20}deg)`,
            }}
          >
            <Win w={TW} h={TH} title="my-project — zsh — 96×24">
              {real ? (
                <ClipVideo clip={CLIPS.A} />
              ) : (
                <div style={{ position: 'absolute', left: 26, top: 26, ...mono(21) }}>
                  <div>
                    <Sh text={`% ${S06_CMD.slice(0, n)}`} />
                    {f < L(CUE.s06Fast) && <Caret on={Math.floor(f / 20) % 2 === 0 || n < S06_CMD.length} h={30} w={15} />}
                  </div>
                  {S06_OUT.map((ln, i) =>
                    f >= L(S06_OUT_AT(i)) ? (
                      <div key={i} style={{ color: ln.startsWith('✓') ? C.success : C.muted, marginTop: 8 }}>
                        {ln}
                      </div>
                    ) : null,
                  )}
                  {f >= L(CUE.s06Done) + 10 && (
                    <div style={{ marginTop: 26, ...enter(f, L(CUE.s06Done) + 10, 20, 10, 0) }}>
                      <Sh text="% ls .claude/skills" />
                      <div style={{ color: C.violet, marginTop: 6 }}>claude-awesome-video-creation/</div>
                    </div>
                  )}
                </div>
              )}
              {!real && <Recon />}
            </Win>
          </div>
          <div style={{ marginTop: 22, padding: 2, borderRadius: 16, background: `linear-gradient(100deg, ${C.cyan}, ${C.violet}, ${C.pink})`, ...enter(f, L(CUE.s06Type) + 10, 24, 12, 0) }}>
            <div style={{ borderRadius: 14, background: a(C.ink, 0.92), padding: '12px 18px' }}>
              <div style={{ ...sans(22, 600), color: C.gold }}>★ my own skill · a reusable video workflow</div>
              <div style={{ ...mono(21, 600), color: C.text, marginTop: 4 }}>github.com/HaochenSHI66/claude-awesome-video-creation</div>
            </div>
          </div>
        </div>
        {fast && <Badge text="4×" style={{ left: 'auto', right: 96, top: 52 }} />}
      </AbsoluteFill>
      <AbsoluteFill style={{ background: C.term, opacity: p(f, end - 10, end, EZ.in) }} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------------------------
// S07: the prompt is typed, the skill loads (freeze + callout), then 8x / 16x with file cards.
// ---------------------------------------------------------------------------------------------
type TL = { t: number; text: string; tone?: 'muted' | 'text' | 'tool' | 'ok' | 'skill' };
const RESP: TL[] = [
  { t: 18, text: '● Read(script/storyboard.md)', tone: 'tool' },
  { t: 34, text: '● Read(script/design_system.md)', tone: 'tool' },
  { t: 52, text: '● Skill(claude-awesome-video-creation)', tone: 'skill' },
  { t: 58, text: '  ⎿  Loaded .claude/skills/claude-awesome-video-creation/SKILL.md', tone: 'muted' },
  { t: 140, text: 'Plan: 12 scenes, 120 BPM grid, drop at 1:20.', tone: 'text' },
  { t: 190, text: '● Write(src/timeline.ts)', tone: 'tool' },
  { t: 260, text: '● Write(src/scenes/Open.tsx)', tone: 'tool' },
  { t: 340, text: '● Write(src/scenes/Explain.tsx)', tone: 'tool' },
  { t: 420, text: '● Write(src/scenes/Demo.tsx)', tone: 'tool' },
  { t: 520, text: '● Write(src/scenes/Close.tsx)', tone: 'tool' },
  { t: 640, text: '● Write(src/Captions.tsx)', tone: 'tool' },
  { t: 820, text: '● Write(scripts/soundtrack.py)', tone: 'tool' },
  { t: 1100, text: '● Bash(npx tsc --noEmit)', tone: 'tool' },
  { t: 1300, text: '  ⎿  ok', tone: 'ok' },
  { t: 1600, text: '● Bash(python scripts/soundtrack.py)', tone: 'tool' },
  { t: 2100, text: '● Bash(npx remotion still Film --frame=2400)', tone: 'tool' },
  { t: 2600, text: '● Read(out/stills/f2400.png)', tone: 'tool' },
  { t: 3200, text: '● Edit(src/scenes/Demo.tsx)', tone: 'tool' },
  { t: 3900, text: '● Bash(npx remotion render Film)', tone: 'tool' },
];
/** Claude Code transcript line: the verb of a tool call gets its own colour. */
const VERB: Record<string, string> = { Read: C.cyan, Write: C.violet, Edit: C.pink, Bash: C.gold, Skill: C.ember };
const ToolLine: React.FC<{ text: string }> = ({ text }) => {
  const m = text.match(/^● (\w+)\((.*)\)$/);
  if (!m) return <>{text}</>;
  const hue = VERB[m[1]] ?? C.text;
  return (
    <>
      <span style={{ color: hue }}>● </span>
      <span style={{ color: hue, fontWeight: 600 }}>{m[1]}</span>
      <span style={{ color: C.muted }}>(</span>
      <span style={{ color: m[1] === 'Skill' ? C.ember : C.text }}>{m[2]}</span>
      <span style={{ color: C.muted }}>)</span>
    </>
  );
};
const toneColor = (t?: TL['tone']) => (t === 'tool' ? C.text : t === 'ok' ? C.success : t === 'skill' ? C.ember : t === 'text' ? C.text : C.muted);

export const S07: React.FC = () => {
  const f = useCurrentFrame();
  const L = (x: number) => x - SCENE.s07.from;
  const end = SCENE.s07.dur;
  const fz = L(CUE.s07Freeze);
  const fzEnd = L(CUE.s07FreezeEnd);
  const r8 = L(CUE.s07Ramp8);
  const r16 = L(CUE.s07Ramp16);
  // content time: real until the freeze, held through it, then 1x -> 8x -> 16x
  const ct = f < fz ? f : f < fzEnd ? fz : f < r8 ? f - (fzEnd - fz) : f < r16 ? r8 - (fzEnd - fz) + (f - r8) * 8 : r8 - (fzEnd - fz) + (r16 - r8) * 8 + (f - r16) * 16;
  const enterAt = L(S07_ENTER);
  const n = typed(S07_KEYS.map(L), Math.min(f, enterAt));
  const submitted = f >= enterAt;
  const real = hasClip(CLIPS.B1);
  // camera: push to 1.6 on the input line while typing, back out once it is sent
  const zIn = p(f, 10, 70, EZ.cam);
  const zOut = p(f, L(S07_FAST), L(S07_FAST) + 40, EZ.cam);
  const zk = zIn * (1 - zOut);
  const k = lmix(1, 1.6, zk);
  const inputY = 800;
  const camY = mix(inputY, 560, zk);
  const SIZE = 34;
  const COLS = 84;
  const promptLines = wrap(PROMPT_FULL.slice(0, n), COLS);
  // transcript: echoed prompt + response lines that have appeared
  const rel = ct - enterAt;
  const shown = submitted ? RESP.filter((r) => rel >= r.t) : [];
  const echo = submitted ? wrap('> ' + PROMPT_FULL, COLS) : [];
  const all: TL[] = [...echo.map((e) => ({ t: 0, text: e, tone: 'muted' as const })), { t: 0, text: '' }, ...shown];
  const maxRows = 12;
  const rows = all.slice(Math.max(0, all.length - maxRows));
  const skillIdx = rows.findIndex((r) => r.tone === 'skill');
  const freezeOn = f >= fz && f < fzEnd + 50;
  const fzK = p(f, fz, fz + 8) * (1 - p(f, fzEnd + 40, fzEnd + 56, EZ.in));
  const badge = f >= L(S07_FAST) && f < enterAt ? '16×' : f >= r16 ? '16×' : f >= r8 ? '8×' : null;
  const wo = whipOut(f, end, 16);
  return (
    <AbsoluteFill style={{ background: C.ink }}>
      <HBlur px={80 * wo} id="s07w" style={{ transform: `translateX(${-800 * wo}px)` }}>
        <AbsoluteFill style={{ transformOrigin: '0 0', transform: `translate(120px, ${camY}px) scale(${k}) translate(-120px, ${-inputY}px)` }}>
          {real ? (
            <Freeze frame={Math.round(ct)} active={freezeOn}>
              <ClipVideo clip={CLIPS.B1} />
            </Freeze>
          ) : (
            <AbsoluteFill style={{ background: `linear-gradient(135deg, ${a(C.flash, 0.07)} 0%, ${a(C.flash, 0)} 40%), ${C.term}` }}>
              <div style={{ position: 'absolute', left: 80, top: 130, ...mono(SIZE) }}>
                {rows.map((r, i) => (
                  <div key={i} style={{ height: SIZE * 1.45, color: toneColor(r.tone), position: 'relative' }}>
                    <ToolLine text={r.text} />
                    {i === skillIdx && fzK > 0 && (
                      <div style={{ position: 'absolute', left: -16, top: -8, width: 1400, height: SIZE * 2.9 + 16, border: `2px solid ${a(C.ember, fzK)}`, borderRadius: 10, boxShadow: `0 0 40px ${a(C.ember, 0.25 * fzK)}` }} />
                    )}
                    {i === skillIdx && fzK > 0 && (
                      <div style={{ position: 'absolute', left: 1424, top: 2, opacity: fzK }}>
                        <div style={{ ...mono(32, 600), color: C.ember, textShadow: glow(0.5) }}>← skill loaded</div>
                        <div style={{ ...mono(22), color: C.text, marginTop: 6 }}>matched by its description</div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
              {/* input box */}
              <div style={{ position: 'absolute', left: 60, right: 60, top: inputY - 50, minHeight: 100, borderRadius: 12, border: `1.5px solid ${submitted ? C.line : C.line2}`, padding: '20px 24px', ...mono(SIZE) }}>
                {submitted ? (
                  <span style={{ color: C.dim }}>{'> '}</span>
                ) : (
                  promptLines.slice(-2).map((ln, i, arr) => (
                    <div key={i}>
                      <span style={{ color: C.muted }}>{i === 0 && promptLines.length <= 2 ? '> ' : '  '}</span>
                      {ln}
                      {i === arr.length - 1 && <Caret on h={SIZE * 1.1} w={SIZE * 0.6} />}
                    </div>
                  ))
                )}
              </div>
              {submitted && f < fz + 2 && rel > 0 && rel < 60 && <div style={{ position: 'absolute', left: 80, top: inputY + 80, ...mono(28), color: C.ember }}>✻ Working…</div>}
            </AbsoluteFill>
          )}
        </AbsoluteFill>
        {!real && <Recon />}
        {freezeOn && <AbsoluteFill style={{ boxShadow: `inset 0 0 0 6px ${a(C.ember, 0.25 * fzK)}` }} />}
        <div style={{ position: 'absolute', left: 80, top: 34, padding: '10px 18px 10px 10px', borderRadius: 14, background: a(C.surface, 0.92) }}>
          <StepHead n="3/3" title="Just ask" f={f} at={10} hue={C.lime} />
        </div>
        {f >= fzEnd + 10 && (
          <div style={{ position: 'absolute', left: 620, top: 52, ...mono(30, 500), color: C.muted, padding: '8px 18px', borderRadius: 10, background: C.surface2, border: `1px solid ${C.line2}`, ...enter(f, fzEnd + 10, 24, 10, 0) }}>
            or call it directly: <span style={{ color: C.ember, fontWeight: 600 }}>/claude-awesome-video-creation</span>
          </div>
        )}
        {S07_CARDS.map((at, i) => {
          const t0 = L(at);
          if (f < t0 || f > t0 + 120) return null;
          const tt = p(f, t0, t0 + 60, EZ.out);
          const side = i % 2 === 0 ? -1 : 1;
          const x = 960 + side * mix(80, 420 + i * 40, tt);
          const y = mix(560, 260 + i * 70, tt);
          const z = mix(-400, 0, tt);
          const o = clamp(tt * 3) * (1 - p(f, t0 + 90, t0 + 120, EZ.in));
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: 0,
                top: 0,
                transform: `perspective(1200px) translate3d(${x}px, ${y}px, ${z}px) translate(-50%, -50%) rotateY(${side * -8 * (1 - tt)}deg)`,
                opacity: o,
                filter: `blur(${(1 - tt) * 10}px)`,
                borderLeft: `3px solid ${C.ember}`,
                padding: '18px 28px',
                borderRadius: 14,
                background: C.surface2,
                border: `1px solid ${C.line2}`,
                boxShadow: `0 30px 80px ${a(C.black, 0.6)}`,
                ...mono(30, 600),
              }}
            >
              {S07_FILES[i]}
            </div>
          );
        })}
        {badge && <Badge text={badge} style={{ left: 'auto', right: 96, top: 52 }} />}
      </HBlur>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------------------------
// S08: render timelapse. Left: render progress. Right: a filmstrip of this film's own frames.
// ---------------------------------------------------------------------------------------------
/** A frame of the film (outside S06-S09), drawn live from the scene components. */
const Thumb: React.FC<{ at: number }> = ({ at }) => {
  const map: [keyof typeof SCENE, React.FC][] = [
    ['s02', S02],
    ['s03', S03],
    ['s04', S04],
    ['s05', S05],
    ['s10', S10],
    ['s11', S11],
    ['s12', S12],
  ];
  const hit = map.find(([id]) => at >= SCENE[id].from && at < SCENE[id].from + SCENE[id].dur) ?? map[0];
  const [id, Comp] = hit;
  return (
    <Freeze frame={Math.max(0, at - SCENE[id].from)}>
      <Comp />
    </Freeze>
  );
};
export const THUMB_FRAMES = [700, 1000, 1250, 1500, 1800, 2300, 2600, 4900, 5200, 5500, 5650, 5900, 6100];

export const S08: React.FC = () => {
  const f = useCurrentFrame();
  const L = (x: number) => x - SCENE.s08.from;
  const blackAt = L(CUE.s08Black);
  const rampAt = L(CUE.s08Ramp);
  const real = hasClip(CLIPS.B2);
  // last 0.9 s: no dead air, the frame is sucked toward the drop
  const suck = p(f, blackAt - 24, SCENE.s08.dur, (t) => t ** 1.4);
  const prog = p(f, 20, blackAt - 10, (t) => t * t * 0.4 + t * 0.6);
  const frames = Math.min(TOTAL, Math.round(prog * TOTAL));
  const pct = Math.round(prog * 100);
  const ramp = p(f, rampAt, blackAt, EZ.in);
  // filmstrip scroll: accelerates, and accelerates hard in the ramp
  const scroll = f * 3 + f * f * 0.004 + ramp * 2600;
  const TH = 0.25;
  const tw = 1920 * TH;
  const th = 1080 * TH;
  const gap = 22;
  const stripBlur = 40 * ramp;
  const realCount = RENDER_SECONDS === null ? null : Math.round(RENDER_SECONDS * p(f, 30, blackAt - 60, EZ.out));
  const mmss = (x: number) => `${Math.floor(x / 60)}:${String(x % 60).padStart(2, '0')}`;
  const lines = [
    `> npx remotion render Film out/film.mp4`,
    `Bundling… done`,
    `Rendering frames ${String(frames).padStart(4, ' ')}/${TOTAL}`,
    `[${'█'.repeat(Math.round(pct / 4))}${'░'.repeat(25 - Math.round(pct / 4))}] ${pct}%`,
    ...(pct >= 100 ? ['Muxing soundtrack.wav', '✓ out/film.mp4'] : []),
  ];
  const timerIn = enter(f, 20, 30);
  return (
    <AbsoluteFill style={{ background: C.ink, transform: `scale(${1 + 1.8 * suck})`, filter: `brightness(${1 + 0.35 * ramp + 1.6 * suck}) blur(${18 * suck}px)` }}>
      <HBlur px={80 * whipIn(f, 22)} id="s08w" style={{ transform: `translateX(${800 * whipIn(f, 22)}px)` }}>
      <div style={{ position: 'absolute', left: 96, top: 250, width: 1060, height: 700, ...enter(f, 0, 24, 20, 0) }}>
        <Win w={1060} h={700} title="teach-it-once — node — 110×32">
          {real ? (
            <ClipVideo clip={CLIPS.B2} />
          ) : (
            <div style={{ position: 'absolute', left: 40, top: 34, ...mono(32) }}>
              {lines.map((ln, i) => (
                <div key={i} style={{ color: ln.startsWith('✓') ? C.success : i === 0 ? C.text : C.muted, marginBottom: 4 }}>
                  {ln}
                </div>
              ))}
            </div>
          )}
          {!real && <Recon />}
        </Win>
      </div>
      {/* filmstrip of real frames */}
      <div style={{ position: 'absolute', left: 1230, top: -140, width: tw + 40, height: 1360, overflow: 'hidden', filter: `blur(${stripBlur * 0.15}px)`, transform: `perspective(1600px) rotateY(-26deg) rotateZ(3deg)`, transformOrigin: '0 50%', maskImage: 'linear-gradient(transparent, black 18%, black 82%, transparent)', WebkitMaskImage: 'linear-gradient(transparent, black 18%, black 82%, transparent)' }}>
        {THUMB_FRAMES.concat(THUMB_FRAMES).map((fr, i) => {
          const y = 1360 - ((scroll + i * (th + gap)) % ((th + gap) * THUMB_FRAMES.length * 2)) + 100;
          if (y < -th - 10 || y > 1370) return null;
          return (
            <div key={i} style={{ position: 'absolute', left: 20, top: 0, transform: `translateY(${y}px)`, width: tw, height: th, borderRadius: 8, overflow: 'hidden', border: `1px solid ${C.line2}` }}>
              <div style={{ width: 1920, height: 1080, transform: `scale(${TH})`, transformOrigin: '0 0', position: 'relative', background: C.ink }}>
                <Thumb at={fr} />
              </div>
            </div>
          );
        })}
      </div>
      {/* timer */}
      <div style={{ position: 'absolute', left: 96, top: 72, width: 1060, ...timerIn }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: 36 }}>
          <div>
            <div style={{ ...mono(96, 600), lineHeight: 1.05 }}>{realCount === null ? '—' : mmss(realCount)}</div>
            <div style={{ ...mono(20), color: C.muted }}>real time</div>
          </div>
          <div style={{ ...mono(56), color: C.muted, marginTop: 22 }}>→</div>
          <div>
            <div style={{ ...mono(96, 600), lineHeight: 1.05, color: C.ember, textShadow: glow(0.6) }}>{Math.round(SCENE.s08.dur / FPS)} s</div>
            <div style={{ ...mono(20), color: C.muted }}>on screen</div>
          </div>
        </div>
        <div style={{ marginTop: 18, width: 1060, height: 4, background: C.line }}>
          <div style={{ width: `${pct}%`, height: 4, background: C.ember }} />
        </div>
      </div>
      </HBlur>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------------------------
// S09: the drop. This film's own title plays in a player, inside a terminal, inside a window,
// five levels deep, each turned 7 degrees: a Droste spiral the camera pulls out of on the beat,
// until the window floats in a space made of this film's own source code.
// ---------------------------------------------------------------------------------------------
const PLAYER = { x: 480, y: 330, w: 960, h: 540 };
const PS = PLAYER.w / 1920; // 0.5
const ROT = 7; // degrees each level turns inside its parent
const DEPTH = 5;
const PC = { x: PLAYER.x + PLAYER.w / 2, y: PLAYER.y + PLAYER.h / 2 };
/** An S02 frame with the full title on screen (after the serif reveal, before the zoom-out). */
const S02_HERO = CUE.s02Serif - SCENE.s02.from + 84;

const Level: React.FC<{ d: number; t: number }> = ({ d, t }) => (
  <div style={{ position: 'absolute', left: 0, top: 0, width: 1920, height: 1080 }}>
    <Win w={1920} h={1080} title={d === DEPTH ? 'teach-it-once — zsh' : `level ${d}`} style={{ borderRadius: 22, border: `2px solid ${C.line2}` }}>
      <div style={{ position: 'absolute', left: 70, top: 46, ...mono(40) }}>
        <div style={{ color: C.muted }}>{'> npx remotion render Film'}</div>
        <div style={{ color: C.success }}>✓ out/film_final.mp4</div>
        <div style={{ color: C.muted }}>{'> open out/film_final.mp4'}</div>
      </div>
    </Win>
    <div
      style={{
        position: 'absolute',
        left: PLAYER.x,
        top: PLAYER.y,
        width: PLAYER.w,
        height: PLAYER.h,
        transform: `rotate(${ROT}deg)`,
        borderRadius: 12,
        overflow: 'hidden',
        outline: `3px solid ${a(C.ember, 0.55)}`,
        boxShadow: `0 0 60px ${a(C.ember, 0.25)}`,
        background: C.ink,
      }}
    >
      <div style={{ width: 1920, height: 1080, transform: `scale(${PS})`, transformOrigin: '0 0', position: 'relative' }}>
        {d > 0 ? (
          <Level d={d - 1} t={t} />
        ) : (
          <Freeze frame={Math.min(S02_HERO + 24, S02_HERO + Math.round(t * 0.08))}>
            <S02 />
          </Freeze>
        )}
      </div>
    </div>
  </div>
);

/** Camera stops: stop j frames level (DEPTH - j)... j = 0 is the innermost picture, DEPTH the outer window. */
const STOPS = (() => {
  const rad = (ROT * Math.PI) / 180;
  const cos = Math.cos(rad);
  const sin = Math.sin(rad);
  // A maps a point of level j into world (= level DEPTH) coordinates
  type Aff = { sc: number; rot: number; f: (x: number, y: number) => [number, number] };
  const levels: Aff[] = [];
  let A: Aff = { sc: 1, rot: 0, f: (x, y) => [x, y] };
  levels[DEPTH] = A;
  for (let j = DEPTH - 1; j >= 0; j--) {
    const parent = A;
    const child = (x: number, y: number): [number, number] => {
      const px = PLAYER.x + PS * x - PC.x;
      const py = PLAYER.y + PS * y - PC.y;
      return parent.f(PC.x + cos * px - sin * py, PC.y + sin * px + cos * py);
    };
    A = { sc: parent.sc * PS, rot: parent.rot + ROT, f: child };
    levels[j] = A;
  }
  // the innermost frame is the S02 picture inside level 0's player
  const inner = { sc: levels[0].sc * PS, rot: levels[0].rot + ROT, c: (() => {
    const px = PLAYER.x + PS * 960 - PC.x;
    const py = PLAYER.y + PS * 540 - PC.y;
    return levels[0].f(PC.x + cos * px - sin * py, PC.y + sin * px + cos * py);
  })() };
  const stops = [{ k: 1 / inner.sc, rot: -inner.rot, c: inner.c }];
  for (let j = 0; j <= DEPTH; j++) stops.push({ k: 0.94 / levels[j].sc, rot: -levels[j].rot, c: levels[j].f(960, 540) });
  stops.push({ k: 0.46, rot: 0, c: [960, 560] as [number, number] });
  return stops;
})();

const SRC = SOURCE_LINES as { file: string; text: string }[];

/** Real lines of this film's own source, flying past in depth around the window. */
const CodeSpace: React.FC<{ f: number; o: number }> = ({ f, o }) => {
  if (o <= 0) return null;
  return (
    <AbsoluteFill style={{ perspective: 1100, opacity: o }}>
      {SRC.slice(0, 64).map((l, i) => {
        const ang = rnd(`a${i}`) * Math.PI * 2;
        const rad = 520 + rnd(`r${i}`) * 900;
        const speed = 7 + rnd(`s${i}`) * 6;
        const z = ((rnd(`z${i}`) * 2600 + f * speed) % 2600) - 2200; // -2200 .. 400, toward camera
        const x = 960 + Math.cos(ang) * rad;
        const y = 540 + Math.sin(ang) * rad * 0.62;
        const near = clamp((z + 2200) / 2600);
        const fade = clamp(near * 3) * clamp((400 - z) / 300);
        const hot = i % 7 === 0;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: 0,
              top: 0,
              transform: `translate3d(${x}px, ${y}px, ${z}px) translate(-50%, -50%)`,
              ...mono(26, hot ? 600 : 400),
              color: hot ? C.ember : C.muted,
              opacity: fade * (hot ? 0.95 : 0.55),
              filter: `blur(${Math.abs(z + 600) / 260}px)`,
              textShadow: hot ? glow(0.5) : undefined,
            }}
          >
            {l.text}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

export const S09_WORDS = ['is', 'the', 'video', 'you’re', 'watching'];
export const S09: React.FC = () => {
  const f = useCurrentFrame();
  const L = (x: number) => x - SCENE.s09.from;
  const end = SCENE.s09.dur;
  // camera: through the stops, one level about every 60 f, on a smooth in-out
  const zStart = 18;
  const zEnd = 220;
  const d = p(f, zStart, zEnd, EZ.cam) * (STOPS.length - 1);
  const j = Math.min(STOPS.length - 2, Math.floor(d));
  const u = d - j;
  const A = STOPS[j];
  const B = STOPS[j + 1];
  const beatT = f % 30;
  const punch = 1 + 0.03 * pulse(beatT, 2, 7) * (f < 420 ? 1 : 0);
  const k = lmix(A.k, B.k, u) * punch;
  const rot = mix(A.rot, B.rot, u);
  const cx = mix(A.c[0], B.c[0], u);
  const cy = mix(A.c[1], B.c[1], u);
  // VO-synced words
  const at = (w: string, fb: number, n = 0) => L(voAt('S09', w, fb, n));
  const wordAt = [at('…is', 82.97), at('the', 83.07), at('video', 83.13), at('you’re', 83.42), at('watching', 83.55)];
  const rightAt = at('right', 83.87);
  const nowAt = at('now.', 84.06);
  const settle = p(f, nowAt + 24, nowAt + 64, EZ.cam);
  const wordsK = p(f, wordAt[0] - 24, wordAt[0]); // the spiral blurs back only while the words land
  const exitZ = p(f, end - 20, end, EZ.in);
  const chroma = 2 + 6 * pulse(beatT, 2, 6);
  const codeO = p(f, 120, 220, EZ.smooth);
  return (
    <AbsoluteFill style={{ background: C.ink }}>
      <AbsoluteFill style={{ transform: `scale(${lmix(1, 4, exitZ)})`, filter: `blur(${14 * exitZ}px)`, opacity: 1 - p(f, end - 8, end) }}>
        {/* light rays and beat rings behind everything */}
        <AbsoluteFill style={{ background: `conic-gradient(from ${f * 0.6}deg at 50% 52%, ${[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11].map((q) => `${a(C.ember, q % 2 ? 0 : 0.07)} ${q * 30}deg ${q * 30 + 30}deg`).join(', ')})`, opacity: codeO, maskImage: 'radial-gradient(circle at 50% 52%, black 10%, transparent 70%)', WebkitMaskImage: 'radial-gradient(circle at 50% 52%, black 10%, transparent 70%)' }} />
        <CodeSpace f={f} o={codeO} />
        {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15].map((b) => {
          const t0 = b * 30;
          if (f < t0 || f > t0 + 50 || t0 > 420) return null;
          const q = p(f, t0, t0 + 50, EZ.out);
          return <div key={b} style={{ position: 'absolute', left: 960, top: 560, width: 10, height: 10, marginLeft: -5, marginTop: -5, borderRadius: '50%', border: `${b % 4 === 0 ? 3 : 1.5}px solid ${a(C.ember, (b % 4 === 0 ? 0.7 : 0.35) * (1 - q))}`, transform: `scale(${1 + q * (b % 4 === 0 ? 220 : 150)})` }} />;
        })}
        {/* the spiral */}
        <AbsoluteFill style={{ filter: f < 12 ? `drop-shadow(${(12 - f) / 2}px 0 0 ${a('#FF2A2A', 0.6)}) drop-shadow(${-(12 - f) / 2}px 0 0 ${a('#2AFFFF', 0.6)})` : `blur(${12 * wordsK * (1 - settle)}px) brightness(${1 - 0.45 * wordsK * (1 - settle)})` }}>
          <div style={{ position: 'absolute', left: 0, top: 0, transformOrigin: '0 0', transform: `translate(960px, 540px) rotate(${rot}deg) scale(${k}) translate(${-cx}px, ${-cy}px)` }}>
            <Level d={DEPTH} t={f} />
          </div>
        </AbsoluteFill>
        {/* scrim while the words land */}
        <AbsoluteFill style={{ background: `radial-gradient(ellipse 1100px 520px at 50% 50%, ${a(C.ink, 0.78 * wordsK * (1 - settle))}, ${a(C.ink, 0.25 * wordsK * (1 - settle))})` }} />
        {/* the line: slams in word by word with the voice, then settles to the lower third */}
        <AbsoluteFill style={{ transform: `translateY(${mix(0, 400, settle)}px) scale(${mix(1, 0.5, settle)})`, transformOrigin: '50% 50%' }}>
          <Center y={430}>
            <div style={{ display: 'flex', gap: 30, alignItems: 'baseline', ...serif(118) }}>
              {S09_WORDS.map((w, i) => {
                const t = p(f, wordAt[i] - 1, wordAt[i] + 14, EZ.out);
                return (
                  <span key={i} style={{ display: 'inline-block', opacity: clamp(t * 3), transform: `scale(${mix(1.6, 1, t)})`, filter: `blur(${10 * (1 - t)}px)`, textShadow: `0 0 30px ${a(C.black, 0.8)}` }}>
                    {w}
                  </span>
                );
              })}
            </div>
          </Center>
          <Center y={640}>
            <div style={{ display: 'flex', gap: 40, alignItems: 'baseline' }}>
              {[
                ['right', rightAt],
                ['now.', nowAt],
              ].map(([w, t0], i) => {
                const t = p(f, (t0 as number) - 1, (t0 as number) + 16, EZ.out);
                return (
                  <span
                    key={i}
                    style={{
                      display: 'inline-block',
                      ...serif(230),
                      color: C.ember,
                      opacity: clamp(t * 3),
                      transform: `scale(${mix(2.2, 1, t)}) rotate(${(1 - t) * (i ? 6 : -6)}deg)`,
                      filter: `blur(${14 * (1 - t)}px)`,
                      textShadow: `${chroma}px 0 0 ${a('#FF2A2A', 0.45)}, ${-chroma}px 0 0 ${a('#2AFFFF', 0.45)}, ${glow(1.4)}`,
                    }}
                  >
                    {w as string}
                  </span>
                );
              })}
            </div>
          </Center>
        </AbsoluteFill>
      </AbsoluteFill>
      {f < 4 && <AbsoluteFill style={{ background: C.flash }} />}
    </AbsoluteFill>
  );
};
