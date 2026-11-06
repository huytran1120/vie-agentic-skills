// S10 write your own, S11 share it, S12 end card.
import React from 'react';
import { AbsoluteFill, OffthreadVideo, spring, staticFile, useCurrentFrame } from 'remotion';
import { a, C } from '../brand/tokens';
import { CLIPS, hasClip } from '../footage';
import { rnd, scramble, S10_ASK, S10_ASK_KEYS, S10_LINE_DUR, S10_LINES, S10_MKDIR, S10_MKDIR_KEYS, S10_RUN, S10_RUN_KEYS, typed } from '../schedule';
import { CUE, FPS, SCENE, SKILL_MD, VO_IS_DRAFT } from '../timeline';
import { Caret, Center, clamp, enter, EZ, FolderGlyph, glow, lmix, mix, mono, p, pulse, Recon, Rise, sans, serif, sheen, win3d, Win, Sh } from '../ui';

// ---------------------------------------------------------------------------------------------
// S10: make the folder, write SKILL.md (labelled), then check it with /skills and run it.
// ---------------------------------------------------------------------------------------------
const C_OUT: { t: number; text: string; tone?: string }[] = [
  { t: 0, text: '● Skill(lab-report)', tone: 'skill' },
  { t: 6, text: '  ⎿  Loaded .claude/skills/lab-report/SKILL.md', tone: 'muted' },
  { t: 22, text: '● Read(results/accuracy.csv)' },
  { t: 34, text: '● Bash(python scripts/plot.py)' },
  { t: 48, text: '● Write(report.md)' },
  { t: 64, text: '✓ report.md · Aim · Method · Results · Discussion', tone: 'ok' },
];
const SKILL_LIST: [string, string][] = [
  ['lab-report', 'Writes lab reports from my results.'],
  ['claude-awesome-video-creation', 'Tutorial videos from code.'],
];

const hl = (line: string) => {
  const m = line.match(/^(name|description):(.*)$/);
  if (m)
    return (
      <>
        <span style={{ color: m[1] === 'name' ? C.cyan : C.gold, fontWeight: 600 }}>{m[1]}:</span>
        <span style={{ color: m[1] === 'name' ? C.text : C.text }}>{m[2]}</span>
      </>
    );
  if (line === '---') return <span style={{ color: C.dim }}>{line}</span>;
  const n = line.match(/^(\d\.)(.*)$/);
  if (n)
    return (
      <>
        <span style={{ color: C.violet, fontWeight: 600 }}>{n[1]}</span>
        <span>{n[2]}</span>
      </>
    );
  return <span>{line}</span>;
};

/** A label that hangs off the end of an editor line. */
const Tag: React.FC<{ text: string; f: number; at: number; hue: string }> = ({ text, f, at, hue }) => {
  if (f < at) return null;
  const t = p(f, at, at + 18, EZ.out);
  return <span style={{ marginLeft: 26, ...mono(22, 600), color: C.ink, background: hue, padding: '2px 10px', borderRadius: 6, opacity: t, display: 'inline-block', transform: `translateX(${(1 - t) * 20}px)`, boxShadow: `0 0 24px ${a(hue, 0.4)}` }}>← {text}</span>;
};

export const S10: React.FC = () => {
  const f = useCurrentFrame();
  const L = (x: number) => x - SCENE.s10.from;
  const end = SCENE.s10.dur;
  const fold = p(f, end - 28, end, EZ.in);
  const shownLines = S10_LINES.filter((t) => f >= L(t)).length;
  const saveAt = L(CUE.s10Save);
  const saved = f >= saveAt;
  const nMk = typed(S10_MKDIR_KEYS.map(L), f);
  const nAsk = typed(S10_ASK_KEYS.map(L), f);
  const askDone = L(S10_ASK_KEYS[S10_ASK_KEYS.length - 1]) + 8;
  const nRun = typed(S10_RUN_KEYS.map(L), f);
  const runDone = L(S10_RUN_KEYS[S10_RUN_KEYS.length - 1]) + 8;
  const real = hasClip(CLIPS.C);
  const rel = f - runDone;
  const EW = 1150;
  const EH = 600;
  const FS = 26;
  const drift = 1 + 0.015 * (f / end);
  const saveFlash = saved ? pulse(f - saveAt, 2, 10) : 0;
  const ty = p(f, 14, 64);
  const lName = L(CUE.s10Line1) + 20;
  const lDesc = L(CUE.s10Trigger);
  const lSteps = L(CUE.s10Steps) + 20;
  return (
    <AbsoluteFill style={{ background: C.ink }}>
      <AbsoluteFill style={{ opacity: 1 - p(f, end - 10, end, EZ.in), transformOrigin: '960px 470px', transform: `scale(${drift * lmix(1, 0.12, fold)})`, filter: `blur(${6 * fold}px)` }}>
        {/* 1. the folder */}
        <div style={{ position: 'absolute', left: 60, top: 56, display: 'flex', alignItems: 'center', gap: 18, ...enter(f, L(CUE.s10Mkdir) - 6, 20, 10, 0) }}>
          <div style={{ ...mono(28, 500), padding: '12px 20px', borderRadius: 12, background: C.surface, border: `1.5px solid ${C.line2}`, minWidth: 700 }}>
            <Sh text={`% ${S10_MKDIR.slice(0, nMk)}`} />
            {nMk < S10_MKDIR.length && <Caret on h={30} w={15} />}
          </div>
          <div style={{ ...sans(26, 500), color: C.muted, opacity: p(f, L(CUE.s10Mkdir) + 50, L(CUE.s10Mkdir) + 66) }}>then write the instruction file inside it</div>
        </div>
        {/* 2. SKILL.md */}
        <div style={{ position: 'absolute', left: 60, top: 150, ...win3d(f, 0, 50) }}>
          <Win w={EW} h={EH} title={saved ? '.claude/skills/lab-report/SKILL.md' : '.claude/skills/lab-report/SKILL.md ●'} style={{ boxShadow: saveFlash > 0 ? `0 0 0 2px ${a(C.success, 0.6 * saveFlash)}, 0 40px 120px ${a(C.black, 0.6)}` : undefined }}>
            <div style={{ position: 'absolute', left: 0, top: 18 }}>
              {SKILL_MD.map((ln, i) => {
                const at = L(S10_LINES[i]);
                if (f < at) return null;
                const chars = Math.min(ln.length, Math.floor(((f - at) / S10_LINE_DUR[i]) * ln.length) + 1);
                const t = ln.slice(0, chars);
                const cur = i === shownLines - 1 && !saved;
                const flash = 1 - p(f, at, at + 24);
                return (
                  <div key={i} style={{ display: 'flex', ...mono(FS), height: 58, alignItems: 'center', background: cur ? a(C.ember, 0.07 + 0.1 * flash) : 'transparent', boxShadow: cur ? `inset 4px 0 0 ${C.ember}` : undefined, width: EW }}>
                    <span style={{ width: 56, textAlign: 'right', color: C.dim, paddingRight: 16 }}>{i + 1}</span>
                    <span style={{ whiteSpace: 'pre' }}>{hl(t)}</span>
                    {cur && <Caret on h={30} w={14} style={{ marginLeft: 2 }} />}
                    {i === 1 && <Tag text="becomes /lab-report" f={f} at={lName} hue={C.cyan} />}
                    {i === 3 && <Tag text="the trigger: say WHEN" f={f} at={lDesc} hue={C.gold} />}
                    {i === 5 && <Tag text="what you always repeat" f={f} at={lSteps} hue={C.violet} />}
                  </div>
                );
              })}
            </div>
            {saved && <div style={{ position: 'absolute', right: 24, bottom: 18, ...mono(24, 600), color: C.success, opacity: p(f, saveAt, saveAt + 8) }}>✓ saved</div>}
          </Win>
        </div>
        {/* 3. check it and run it (Clip C slot) */}
        <div
          style={{
            position: 'absolute',
            left: 1250,
            top: 150,
            opacity: clamp(ty * 2),
            transformOrigin: '100% 50%',
            transform: `perspective(1800px) translateX(${(1 - ty) * 400}px) rotateY(${mix(-30, -8, ty)}deg)`,
          }}
        >
          <Win w={620} h={EH} title="my-project — claude">
            {real ? (
              <OffthreadVideo src={staticFile(CLIPS.C.file)} startFrom={Math.round(CLIPS.C.start * FPS)} playbackRate={CLIPS.C.rate} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            ) : (
              <div style={{ position: 'absolute', left: 24, top: 22, width: 580, ...mono(22) }}>
                <div>
                  <span style={{ color: C.muted }}>{'> '}</span>
                  {S10_ASK.slice(0, nAsk)}
                  {f < askDone && nAsk > 0 && <Caret on h={24} w={12} />}
                  {nAsk === 0 && <Caret on={Math.floor(f / 20) % 2 === 0} h={24} w={12} />}
                </div>
                {f >= askDone && (
                  <div style={{ marginTop: 10, padding: '10px 14px', borderRadius: 10, border: `1px solid ${C.line2}`, ...enter(f, askDone, 14, 8, 0) }}>
                    <div style={{ color: C.muted, marginBottom: 6 }}>Skills</div>
                    {SKILL_LIST.map(([nm, d], i) => (
                      <div key={i} style={{ marginTop: 6, color: i === 0 ? C.text : C.muted }}>
                        <div style={{ color: i === 0 ? C.ember : C.violet, fontWeight: 600, whiteSpace: 'pre' }}>{i === 0 ? '✓ ' : '  '}{nm}</div>
                        <div style={{ ...mono(17), color: C.muted, marginLeft: 26 }}>{d}</div>
                      </div>
                    ))}
                  </div>
                )}
                {nRun > 0 && (
                  <div style={{ marginTop: 22 }}>
                    <span style={{ color: C.muted }}>{'> '}</span>
                    {S10_RUN.slice(0, nRun)}
                    {f < runDone && <Caret on h={24} w={12} />}
                  </div>
                )}
                {f >= runDone &&
                  C_OUT.filter((o) => rel >= o.t * 1.6).map((o, i) => (
                    <div key={i} style={{ marginTop: 6, color: o.tone === 'skill' ? C.ember : o.tone === 'ok' ? C.success : o.tone === 'muted' ? C.muted : C.text, whiteSpace: 'pre-wrap', ...mono(20) }}>
                      {o.text}
                    </div>
                  ))}
              </div>
            )}
            {!real && <Recon />}
          </Win>
          <div style={{ position: 'absolute', left: 0, top: EH + 18, whiteSpace: 'nowrap', ...sans(24, 400), color: C.muted, ...enter(f, L(CUE.s10One) + 20, 24, 10, 0) }}>
            or just ask: <span style={{ color: C.text }}>“write up my lab report”</span>
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------------------------
// S11: the skill folder duplicates out to the team; a second ring of agents that read SKILL.md.
// ---------------------------------------------------------------------------------------------
const TEAM = ['AL', 'JK', 'MR', 'SC', 'TW', 'YN'];
export const S11_NODE_AT = (i: number) => CUE.s11Team + i * 6;
export const S11: React.FC = () => {
  const f = useCurrentFrame();
  const L = (x: number) => x - SCENE.s11.from;
  const end = SCENE.s11.dur;
  const conv = p(f, end - 24, end, EZ.in);
  const CX = 960;
  const CY = 450;
  const R = 330;
  const fold = p(f, 0, 30, EZ.cam);
  const ring2 = L(CUE.s11Ring2);
  const tilt = mix(0, 64, p(f, 40, 200, EZ.cam)) * (Math.PI / 180);
  const spin = f * 0.55;
  const node = (i: number, rr = 1) => {
    const ang = ((i / TEAM.length) * 360 - 90 + spin) * (Math.PI / 180);
    const z = Math.sin(ang) * Math.sin(tilt); // -1 far .. +1 near
    return { x: CX + Math.cos(ang) * R * rr, y: CY + Math.sin(ang) * R * rr * Math.cos(tilt), z };
  };
  const openAt = L(CUE.s11Open);
  const portAt = L(CUE.s11Portable);
  return (
    <AbsoluteFill style={{ background: C.ink }}>
      <AbsoluteFill style={{ opacity: 1 - p(f, end - 8, end), transformOrigin: `960px 450px`, transform: `scale(${lmix(1, 0.4, conv)})`, filter: `blur(${8 * conv}px)` }}>
        <div style={{ position: 'absolute', left: 0, right: 0, top: 70, textAlign: 'center', ...mono(32), color: C.muted, ...enter(f, L(CUE.s11Commit), 30) }}>
          <Sh text={'% git add .claude/skills && git commit -m "add lab-report skill"'} />
        </div>
        <svg width={1920} height={1080} style={{ position: 'absolute', left: 0, top: 0 }}>
          {/* the orbit */}
          <ellipse cx={CX} cy={CY} rx={R} ry={R * Math.cos(tilt)} fill="none" stroke={C.line2} strokeWidth={1.5} strokeDasharray="4 10" opacity={p(f, 30, 60)} />
          {TEAM.map((_, i) => {
            const d = p(f, L(S11_NODE_AT(i)) - 12, L(S11_NODE_AT(i)) + 6, EZ.cam);
            const n = node(i, d);
            return <line key={i} x1={CX} y1={CY} x2={n.x} y2={n.y} stroke={a(C.ember, 0.35 + 0.3 * (n.z + 1) / 2)} strokeWidth={1.5} />;
          })}
          {TEAM.map((_, i) => {
            const at = L(S11_NODE_AT(i)) + 10;
            return [0, 1, 2].map((k) => {
              const u = ((f - at - k * 22) % 66) / 66;
              if (f < at + k * 22 || u < 0) return null;
              const n = node(i, u);
              return <circle key={`${i}-${k}`} cx={n.x} cy={n.y} r={4.5} fill={C.emberGlow} opacity={Math.sin(Math.PI * u)} />;
            });
          })}
          {[0, 1].map((i) => {
            const d = p(f, ring2 + i * 8 - 10, ring2 + i * 8 + 20, EZ.cam);
            const x = CX + (i === 0 ? -1 : 1) * 600 * d;
            return <line key={i} x1={CX + (i === 0 ? -1 : 1) * (R + 30)} y1={CY} x2={x} y2={CY} stroke={C.line2} strokeWidth={1.5} strokeDasharray="6 8" opacity={d > 0.6 ? 1 : 0} />;
          })}
        </svg>
        <Center x={CX} y={CY} style={{ transform: `translate(-50%, -50%) scale(${mix(2.2, 1, fold)})`, filter: `drop-shadow(0 0 ${18 + 10 * pulse(f % 30, 2, 8)}px ${a(C.ember, 0.5)})` }}>
          <FolderGlyph size={120} />
        </Center>
        <Center x={CX} y={CY + 84} style={{ opacity: fold }}>
          <div style={{ ...mono(24, 600), color: C.ember }}>lab-report</div>
        </Center>
        {TEAM.map((ini, i) => ({ ini, i, n: node(i, p(f, L(S11_NODE_AT(i)) - 12, L(S11_NODE_AT(i)) + 6, EZ.cam)) }))
          .sort((u, v) => u.n.z - v.n.z)
          .map(({ ini, i, n }) => {
            const at = L(S11_NODE_AT(i));
            const t = p(f, at - 12, at + 6, EZ.cam);
            const pop = 1 + 0.12 * pulse(f - at, 2, 6);
            const depth = 1 + 0.22 * n.z;
            return (
              <div
                key={i}
                style={{
                  position: 'absolute',
                  left: 0,
                  top: 0,
                  transform: `translate(${n.x}px, ${n.y}px) translate(-50%, -50%) scale(${pop * depth * clamp(t * 1.4)})`,
                  width: 84,
                  height: 84,
                  borderRadius: 42,
                  background: C.surface2,
                  border: `1.5px solid ${n.z > 0.3 ? a(C.ember, 0.7) : C.line2}`,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  ...sans(28, 600),
                  color: C.text,
                  opacity: 0.55 + 0.45 * (n.z + 1) / 2,
                  filter: `blur(${Math.max(0, -n.z) * 1.6}px)`,
                }}
              >
                {ini}
              </div>
            );
          })}
        <Center x={CX} y={CY + R * Math.cos(tilt) + 70} style={{ ...enter(f, L(CUE.s11Team) + 30, 30) }}>
          <div style={{ ...mono(26), color: C.muted, opacity: 1 - p(f, openAt - 20, openAt) }}>your group</div>
        </Center>
        {[0, 1].map((i) => {
          const t = p(f, ring2 + i * 8 + 8, ring2 + i * 8 + 30);
          const x = CX + (i === 0 ? -1 : 1) * 640;
          return (
            <Center key={i} x={x} y={CY} style={{ opacity: t, transform: `translate(-50%, -50%) translateX(${(1 - t) * (i ? -60 : 60)}px)` }}>
              <div style={{ padding: '16px 24px', borderRadius: 12, border: `1.5px solid ${C.line2}`, background: C.surface, ...mono(26, 600), color: C.text, whiteSpace: 'pre', textAlign: 'center' }}>
                {i === 0 ? 'Claude Code' : 'other AI agents\nthat support skills'}
              </div>
            </Center>
          );
        })}
        {/* "An open standard." decodes; agentskills.io drops in */}
        <div style={{ position: 'absolute', left: 0, right: 0, top: 800, display: 'flex', justifyContent: 'center', alignItems: 'baseline', gap: 30 }}>
          <span style={{ ...mono(58, 600), opacity: f >= openAt ? 1 : 0 }}>{scramble('An open standard.', f, openAt)}</span>
          <span style={{ display: 'inline-flex', gap: '0.25em', ...serif(96), color: C.ember, textShadow: glow() }}>
            {['agentskills.io'].map((w, i) => {
              const t = p(f, portAt + i * 6, portAt + i * 6 + 26, EZ.out);
              return (
                <span key={i} style={{ display: 'inline-block', opacity: clamp(t * 2), transform: `translateY(${(1 - t) * -70}px) rotate(${(1 - t) * -8}deg)`, filter: `blur(${6 * (1 - t)}px)` }}>
                  {w}
                </span>
              );
            })}
          </span>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------------------------
// S12: the cheat sheet (held so viewers can pause and copy), then "Teach it once." and the lockup.
// ---------------------------------------------------------------------------------------------
const SHEET_HUES = [C.cyan, C.violet, C.gold, C.pink, C.lime];
const SHEET: { n: string; label: string; cmd: string; sub?: string }[] = [
  { n: '1', label: 'Install', cmd: 'curl -fsSL https://claude.ai/install.sh | bash', sub: 'Windows PowerShell:  irm https://claude.ai/install.ps1 | iex' },
  { n: '2', label: 'Start', cmd: 'cd my-project && claude', sub: 'log in · Pro / Max / Team / Enterprise or API account' },
  { n: '3', label: 'Add a skill', cmd: 'npx skills add <owner/repo>', sub: 'mine:  npx skills add HaochenSHI66/claude-awesome-video-creation' },
  { n: '4', label: 'Write your own', cmd: '.claude/skills/<name>/SKILL.md', sub: 'the instruction file: name · description (say WHEN) · steps' },
  { n: '5', label: 'Use it', cmd: '/skills   /<name>', sub: 'or just ask: the description triggers it' },
];
/** The vote card: a burst, a colour-cycling frame, a check that draws itself, confetti. */
const CONFETTI = Array.from({ length: 70 }, (_, i) => ({
  ang: rnd(`ca${i}`) * Math.PI * 2,
  v: 9 + rnd(`cv${i}`) * 15,
  spin: (rnd(`cs${i}`) - 0.5) * 30,
  w: 8 + rnd(`cw${i}`) * 10,
  hue: [C.cyan, C.violet, C.gold, C.pink, C.lime, C.ember][i % 6],
}));
const VoteCard: React.FC<{ f: number; at: number }> = ({ f, at }) => {
  const t = f - at;
  if (t < -8) return null;
  const pop = spring({ frame: t, fps: FPS, config: { damping: 11, stiffness: 140 } });
  const o = clamp(p(f, at - 8, at + 6));
  const rot = f * 2.4;
  const check = p(f, at + 10, at + 34, EZ.out);
  const ring = p(f, at, at + 40, EZ.out);
  const grad = `linear-gradient(100deg, ${C.cyan}, ${C.violet} 40%, ${C.pink} 70%, ${C.gold})`;
  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      {/* light burst */}
      <AbsoluteFill style={{ background: `conic-gradient(from ${rot * 0.4}deg at 50% 46%, ${[C.cyan, C.violet, C.pink, C.gold, C.lime, C.cyan, C.violet, C.pink, C.gold, C.lime, C.cyan, C.violet].map((h, q) => `${a(h, 0.16)} ${q * 30}deg, ${a(h, 0)} ${q * 30 + 15}deg`).join(', ')})`, opacity: o, maskImage: 'radial-gradient(circle at 50% 46%, black 5%, transparent 62%)', WebkitMaskImage: 'radial-gradient(circle at 50% 46%, black 5%, transparent 62%)' }} />
      <div style={{ position: 'absolute', left: 960, top: 500, width: 20, height: 20, marginLeft: -10, marginTop: -10, borderRadius: '50%', border: `3px solid ${a(C.violet, 0.8 * (1 - ring))}`, transform: `scale(${1 + ring * 70})` }} />
      {/* confetti */}
      {CONFETTI.map((c, i) => {
        if (t < 0 || t > 140) return null;
        const x = 960 + Math.cos(c.ang) * c.v * t;
        const y = 500 + Math.sin(c.ang) * c.v * t * 0.8 + 0.09 * t * t;
        return <div key={i} style={{ position: 'absolute', left: x, top: y, width: c.w, height: c.w * 0.45, background: c.hue, borderRadius: 2, transform: `rotate(${c.spin * t}deg)`, opacity: 1 - p(f, at + 80, at + 140) }} />;
      })}
      {/* the card with a colour-cycling border */}
      <div style={{ position: 'absolute', left: 960, top: 500, transform: `translate(-50%, -50%) scale(${0.6 + 0.4 * pop})`, opacity: o, padding: 3, borderRadius: 30, background: `conic-gradient(from ${rot}deg, ${C.cyan}, ${C.violet}, ${C.pink}, ${C.gold}, ${C.lime}, ${C.cyan})`, boxShadow: `0 0 80px ${a(C.violet, 0.45)}, 0 0 160px ${a(C.cyan, 0.2)}` }}>
        <div style={{ borderRadius: 27, background: a(C.ink, 0.94), padding: '40px 70px 44px', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14 }}>
          <div style={{ ...mono(26, 600), color: C.muted, letterSpacing: '0.22em' }}>FOUND THIS USEFUL?</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 30 }}>
            <svg width={110} height={110} viewBox="0 0 110 110">
              <circle cx={55} cy={55} r={48} fill="none" stroke={C.lime} strokeWidth={7} strokeDasharray={302} strokeDashoffset={302 * (1 - ring)} transform="rotate(-90 55 55)" />
              <polyline points="32,57 49,73 79,40" fill="none" stroke={C.lime} strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={70} strokeDashoffset={70 * (1 - check)} />
            </svg>
            <div style={{ ...sans(132, 700), letterSpacing: '-0.03em', backgroundImage: grad, backgroundSize: '200% 100%', backgroundPosition: `${(f * 1.2) % 200}% 0`, WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent', filter: `drop-shadow(0 0 30px ${a(C.violet, 0.5)})` }}>Vote for it</div>
          </div>
          <div style={{ ...mono(32, 600), color: C.text }}>
            <span style={{ color: C.gold }}>24130819D</span> · Claude Code: Agent Skills
          </div>
          <div style={{ ...sans(24, 400), color: C.muted }}>COMP4431 peer voting · up to 5 picks · thank you!</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const DEEP_CAN: [string, string][] = [
  ['bundle scripts & templates', C.cyan],
  ['call tools and APIs', C.violet],
  ['chain into workflows', C.gold],
  ['run in other AI agents', C.lime],
];
const DEEP_USE: [string, string][] = [
  ['lab reports', C.pink],
  ['citations', C.cyan],
  ['exam revision', C.violet],
  ['thesis drafts', C.gold],
  ['code review', C.lime],
];
const Pill: React.FC<{ text: string; hue: string; f: number; at: number }> = ({ text, hue, f, at }) => {
  const t = p(f, at, at + 18, EZ.out);
  return (
    <span style={{ display: 'inline-block', ...sans(30, 600), color: hue, padding: '10px 22px', borderRadius: 999, background: a(hue, 0.12), border: `1.5px solid ${a(hue, 0.55)}`, boxShadow: `0 0 26px ${a(hue, 0.18)}`, opacity: t, transform: `translateY(${(1 - t) * 18}px) scale(${0.9 + 0.1 * t})` }}>
      {text}
    </span>
  );
};

export const S12: React.FC = () => {
  const f = useCurrentFrame();
  const L = (x: number) => x - SCENE.s12.from;
  const deep = L(CUE.s12Deep);
  const mail = L(CUE.s12Mail);
  const stop = L(CUE.s12Stop);
  const once = L(CUE.s12Once);
  const vote = L(CUE.s12Vote);
  const lock = L(CUE.s12Lockup);
  const fade = L(CUE.s12Fade);
  const fadeK = 1 - p(f, fade, fade + 60, EZ.smooth);
  const pulseK = 1 + 0.15 * Math.sin(((f - once) / 60) * Math.PI * 2);
  // phases: cheat sheet -> "just the basics" + contact -> tagline -> vote
  const sheetBack = p(f, deep - 6, deep + 20, EZ.cam);
  const deepIn = p(f, deep - 4, deep + 20, EZ.cam) * (1 - p(f, stop - 10, stop + 8, EZ.in));
  const tagIn = p(f, stop - 4, stop + 12) * (1 - p(f, vote - 8, vote + 14, EZ.in));
  return (
    <AbsoluteFill style={{ background: C.ink }}>
      {/* 1. the cheat sheet */}
      <AbsoluteFill style={{ opacity: fadeK * (1 - 0.8 * sheetBack), transform: `scale(${1 - 0.06 * sheetBack})`, filter: `blur(${8 * sheetBack}px)` }}>
        <div style={{ position: 'absolute', left: 150, top: 70, display: 'flex', alignItems: 'baseline', gap: 28, ...enter(f, 4, 26, 12, 0) }}>
          <span style={{ ...mono(24, 600), color: C.ember, letterSpacing: '0.16em' }}>CHEAT SHEET</span>
          <span style={{ ...sans(26, 400), color: C.muted }}>Claude Code · Agent Skills · pause, copy, try it</span>
        </div>
        <div style={{ position: 'absolute', left: 150, top: 140, width: 1620 }}>
          {SHEET.map((r, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: 26, padding: '18px 0', borderTop: `1px solid ${C.line}`, ...enter(f, 10 + i * 8, 24, 14, 0) }}>
              <span style={{ ...mono(32, 700), color: C.ink, background: SHEET_HUES[i], borderRadius: 8, width: 44, textAlign: 'center', boxShadow: `0 0 24px ${a(SHEET_HUES[i], 0.35)}` }}>{r.n}</span>
              <span style={{ ...sans(32, 600), color: C.text, width: 290 }}>{r.label}</span>
              <div>
                <div style={{ ...mono(32, 500), color: C.text, whiteSpace: 'pre' }}>{r.cmd.startsWith('/') || r.cmd.startsWith('.') ? <span style={{ color: C.violet }}>{r.cmd}</span> : <Sh text={r.cmd} />}</div>
                {r.sub && <div style={{ ...mono(22), color: C.muted, marginTop: 8, whiteSpace: 'pre' }}>{r.sub}</div>}
              </div>
            </div>
          ))}
          <div style={{ borderTop: `1px solid ${C.line}`, paddingTop: 16, ...mono(24), color: C.muted, ...enter(f, 60, 24, 10, 0) }}>
            docs: <span style={{ color: C.text }}>code.claude.com/docs/en/skills</span>   ·   format: <span style={{ color: C.text }}>agentskills.io</span>
          </div>
        </div>
      </AbsoluteFill>
      {/* 2. just the basics + contact */}
      {deepIn > 0 && (
        <AbsoluteFill style={{ opacity: deepIn * fadeK }}>
          <Center y={230}>
            <Rise text="This is just the basics." f={f} at={deep} stagger={5} style={{ ...sans(80, 700) }} word={(i) => (i >= 3 ? { color: C.gold, textShadow: `0 0 30px ${a(C.gold, 0.4)}` } : {})} />
          </Center>
          <div style={{ position: 'absolute', left: 0, right: 0, top: 330, display: 'flex', justifyContent: 'center', gap: 18, flexWrap: 'wrap' }}>
            <span style={{ ...mono(24, 600), color: C.muted, letterSpacing: '0.14em', alignSelf: 'center', marginRight: 6, opacity: p(f, deep + 30, deep + 44) }}>SKILLS CAN</span>
            {DEEP_CAN.map(([t, h], i) => <Pill key={i} text={t} hue={h} f={f} at={deep + 34 + i * 7} />)}
          </div>
          <div style={{ position: 'absolute', left: 0, right: 0, top: 430, display: 'flex', justifyContent: 'center', gap: 18, flexWrap: 'wrap' }}>
            <span style={{ ...mono(24, 600), color: C.muted, letterSpacing: '0.14em', alignSelf: 'center', marginRight: 6, opacity: p(f, deep + 58, deep + 72) }}>FOR STUDY</span>
            {DEEP_USE.map(([t, h], i) => <Pill key={i} text={t} hue={h} f={f} at={deep + 62 + i * 6} />)}
          </div>
          <div style={{ position: 'absolute', left: 0, right: 0, top: 530, textAlign: 'center', ...enter(f, deep + 90, 24, 12, 0) }}>
            <span style={{ ...sans(26, 600), color: C.gold }}>★ the workflow behind this video, as a skill:  </span>
            <span style={{ ...mono(28, 700), color: C.cyan }}>github.com/HaochenSHI66/claude-awesome-video-creation</span>
          </div>
          {/* contact card */}
          <div style={{ position: 'absolute', left: 960, top: 640, transform: `translate(-50%, 0) scale(${0.92 + 0.08 * p(f, mail, mail + 20, EZ.out)})`, opacity: p(f, mail - 4, mail + 14), padding: 2, borderRadius: 22, background: `linear-gradient(100deg, ${C.cyan}, ${C.violet}, ${C.pink})` }}>
            <div style={{ borderRadius: 20, background: a(C.ink, 0.92), padding: '22px 40px', display: 'flex', alignItems: 'center', gap: 26 }}>
              <svg width={58} height={44} viewBox="0 0 58 44">
                <rect x={2} y={2} width={54} height={40} rx={7} fill="none" stroke={C.cyan} strokeWidth={3.5} />
                <polyline points="5,6 29,25 53,6" fill="none" stroke={C.cyan} strokeWidth={3.5} strokeLinejoin="round" />
              </svg>
              <div>
                <div style={{ ...sans(26, 500), color: C.muted }}>Questions about skills? I've studied them a lot. Email me any time:</div>
                <div style={{ ...mono(44, 700), color: C.text, marginTop: 4, letterSpacing: '-0.01em' }}>24130819d@connect.polyu.hk</div>
              </div>
            </div>
          </div>
        </AbsoluteFill>
      )}
      {/* 3. the tagline */}
      {tagIn > 0 && (
        <AbsoluteFill style={{ opacity: tagIn * fadeK }}>
          <Center y={380}>
            <Rise text="Stop repeating yourself." f={f} at={stop} stagger={5} style={{ ...sans(88, 600) }} />
          </Center>
          <Center y={550}>
            <div style={{ textShadow: glow(f >= once ? pulseK : 1), position: 'relative' }}>
              <Rise text="Teach it once." f={f} at={once} stagger={7} dur={36} style={{ ...serif(150) }} word={(i) => sheen(f, once + 36 + i * 8, 60, C.ember, C.emberGlow)} />
              <div style={{ position: 'absolute', left: 0, top: '100%', height: 2, width: `${100 * p(f, once + 30, once + 80, EZ.cam)}%`, background: C.ember, boxShadow: glow(0.6) }} />
            </div>
          </Center>
        </AbsoluteFill>
      )}
      {/* 4. vote, then the lockup with the contact line */}
      <AbsoluteFill style={{ opacity: fadeK }}>
        <VoteCard f={f} at={vote} />
        <div style={{ position: 'absolute', left: 0, right: 0, bottom: 104, textAlign: 'center', ...mono(26, 600), color: C.cyan, ...enter(f, lock, 30) }}>
          ✉ 24130819d@connect.polyu.hk
        </div>
        <div style={{ position: 'absolute', left: 0, right: 0, bottom: 64, textAlign: 'center', ...sans(24, 500), color: C.muted, ...enter(f, lock + 6, 30) }}>
          Claude Code · Agent Skills · COMP4431 · SHI Haochen · 24130819D
        </div>
        <div style={{ position: 'absolute', left: 0, right: 0, bottom: 32, textAlign: 'center', ...mono(16), color: a(C.text, 0.4), ...enter(f, lock + 15, 30) }}>
          {VO_IS_DRAFT ? 'Made with Claude Code + my skill claude-awesome-video-creation (built on cinetic). Turtle mascot: original, generated with Codex. Voice: draft TTS, to be replaced.' : 'Made with Claude Code + my skill claude-awesome-video-creation (built on cinetic). Turtle mascot: original, generated with Codex. Voice: SHI Haochen.'}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
