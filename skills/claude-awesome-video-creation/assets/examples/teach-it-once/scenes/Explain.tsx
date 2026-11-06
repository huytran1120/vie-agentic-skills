// S04 anatomy of a skill, S05 progressive disclosure.
import React from 'react';
import { AbsoluteFill, spring, useCurrentFrame } from 'remotion';
import { a, C } from '../brand/tokens';
import { CUE, FPS, SCENE, SKILL_MD } from '../timeline';
import { clamp, enter, EZ, FolderGlyph, glow, HBlur, mix, mono, MONO_ADV, p, Rise, sans, serif, whipIn, whipOut } from '../ui';

// ---------------------------------------------------------------------------------------------
// S04: the folder glyph unfolds into the file tree; leader lines label each part.
// ---------------------------------------------------------------------------------------------
export const TREE = ['lab-report/', '├── SKILL.md', '├── scripts/plot.py', '└── template.md'];
const ROW_Y = (i: number) => 230 + i * 86;
const TREE_X = 330;
const T_SIZE = 40;
const LABEL_COLORS = [C.cyan, C.violet, C.gold];
export const S04_LABELS: { text: string; row: number; cue: number }[] = [
  { text: 'instructions: name · description · steps', row: 1, cue: CUE.s04Instr },
  { text: 'code it runs', row: 2, cue: CUE.s04Scripts },
  { text: 'files it reads', row: 3, cue: CUE.s04Assets },
];

export const S04: React.FC = () => {
  const f = useCurrentFrame();
  const L = (x: number) => x - SCENE.s04.from;
  const treeAt = L(CUE.s04Tree);
  const folderAt = L(CUE.s04Folder);
  const end = SCENE.s04.dur;
  const wo = whipOut(f, end, 18);
  const tilt = mix(12, 0, p(f, treeAt - 20, treeAt + 100, EZ.cam));
  const drift = 1 + 0.03 * (f / end);
  // folder: pops at centre, then travels to the tree's first row and shrinks into its icon slot
  const fIn = p(f, folderAt, folderAt + 30);
  const fMove = p(f, treeAt - 30, treeAt + 10, EZ.cam);
  const fx = mix(960, TREE_X - 70, fMove);
  const fy = mix(520, ROW_Y(0), fMove);
  const fs = mix(220, 56, fMove);
  const skillAt = L(CUE.s04Skill);
  return (
    <AbsoluteFill style={{ background: C.ink }}>
      {f < folderAt + 20 && (
        <AbsoluteFill>
          <div style={{ position: 'absolute', left: 960, top: 520, width: 16, height: 16, marginLeft: -8, marginTop: -8, borderRadius: 8, background: C.ember, boxShadow: glow(1.5), transform: `scale(${1 + 2.5 * p(f, folderAt - 10, folderAt + 6)})`, opacity: 1 - p(f, folderAt, folderAt + 16) }} />
          <div style={{ position: 'absolute', left: 960, top: 520, width: 400, height: 400, marginLeft: -200, marginTop: -200, borderRadius: 200, border: `1.5px solid ${a(C.ember, 0.6)}`, transform: `scale(${p(f, folderAt - 6, folderAt + 30)})`, opacity: 1 - p(f, folderAt, folderAt + 30) }} />
        </AbsoluteFill>
      )}
      <HBlur px={70 * wo} id="s04w" style={{ transform: `translateX(${-700 * wo}px)`, opacity: 1 - p(f, end - 6, end) }}>
        {/* where it lives: the two real locations */}
        {[
          { path: '~/.claude/skills/lab-report/', tag: 'personal · every project', at: L(CUE.s04Home), lit: L(CUE.s04Home), hue: C.cyan },
          { path: '.claude/skills/lab-report/', tag: 'this project · commit to share', at: L(CUE.s04Home) + 14, lit: L(CUE.s04Share), hue: C.violet },
        ].map((r, i) => {
          const lit = p(f, r.lit, r.lit + 20);
          return (
            <div key={i} style={{ position: 'absolute', left: 250, top: 700 + i * 108, display: 'flex', alignItems: 'center', gap: 34, ...enter(f, r.at, 28, 18, 0) }}>
              <div style={{ ...mono(40, 600), padding: '12px 22px', borderRadius: 12, background: C.surface, border: `1.5px solid ${lit > 0 ? a(r.hue, 0.3 + 0.6 * lit) : C.line2}`, boxShadow: lit > 0 ? `0 0 40px ${a(r.hue, 0.22 * lit)}` : undefined, minWidth: 760, color: lit > 0.5 ? r.hue : C.text }}>{r.path}</div>
              <div style={{ ...sans(34, 500), color: lit > 0.5 ? r.hue : C.muted }}>← {r.tag}</div>
            </div>
          );
        })}
        {f >= L(CUE.s04Home) - 10 && <div style={{ position: 'absolute', left: 250, top: 650, ...mono(22, 600), color: C.dim, letterSpacing: '0.12em', ...enter(f, L(CUE.s04Home) - 10, 24) }}>WHERE IT LIVES</div>}
        <AbsoluteFill style={{ transform: `perspective(1600px) rotateX(${tilt}deg) scale(${drift})`, transformOrigin: '50% 50%' }}>
          {fIn > 0 && (
            <div style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${fx}px, ${fy}px) translate(-50%, -50%) scale(${0.6 + 0.4 * fIn})`, opacity: clamp(fIn * 2) }}>
              <FolderGlyph size={fs} draw={fIn} />
            </div>
          )}
          {TREE.map((row, i) => {
            const at = treeAt + i * 6;
            const t = p(f, at, at + 30);
            const isSkill = i === 1;
            const hl = isSkill ? p(f, skillAt, skillAt + 24) : 0;
            const head = row.match(/^[├└─ ]*/)?.[0] ?? '';
            return (
              <div key={i} style={{ position: 'absolute', left: TREE_X, top: ROW_Y(i) - T_SIZE * 0.7, opacity: t, transform: `translateX(${(1 - t) * -20}px)` }}>
                <span style={{ ...mono(T_SIZE), color: C.dim }}>{head}</span>
                <span
                  style={{
                    ...mono(T_SIZE, i === 0 ? 600 : 400),
                    color: isSkill ? (hl > 0.5 ? C.ember : C.text) : i === 0 ? C.text : C.text,
                    padding: '4px 12px',
                    marginLeft: -12,
                    borderRadius: 10,
                    background: isSkill ? a(C.ember, 0.14 * hl) : 'transparent',
                    boxShadow: isSkill ? `0 0 0 1.5px ${a(C.ember, 0.8 * hl)}, 0 0 40px ${a(C.ember, 0.25 * hl)}` : undefined,
                    textShadow: isSkill && hl > 0 ? glow(0.6 * hl) : undefined,
                  }}
                >
                  {row.slice(head.length)}
                </span>
              </div>
            );
          })}
          {S04_LABELS.map((lb, i) => {
            const at = L(lb.cue);
            const rowEnd = TREE_X + TREE[lb.row].length * T_SIZE * MONO_ADV + 30;
            const lx = 1040;
            const draw = p(f, at - 4, at + 22, EZ.cam);
            const y = ROW_Y(lb.row);
            return (
              <React.Fragment key={i}>
                <div style={{ position: 'absolute', left: rowEnd, top: y, width: (lx - 24 - rowEnd) * draw, height: 1.5, background: C.line2 }} />
                <div style={{ position: 'absolute', left: rowEnd - 4, top: y - 3.5, width: 8, height: 8, borderRadius: 4, background: C.muted, opacity: draw }} />
                <div style={{ position: 'absolute', left: lx, top: y - 28 }}>
                  <Rise text={lb.text} f={f} at={at + 8} style={{ ...sans(40, 500), color: LABEL_COLORS[i] }} />
                </div>
              </React.Fragment>
            );
          })}
        </AbsoluteFill>
      </HBlur>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------------------------
// S05: 8 collapsed skill cards; only name + description cost context; one card expands.
// ---------------------------------------------------------------------------------------------
export const CARDS: [string, string][] = [
  ['pptx', 'Build and edit slide decks.'],
  ['pdf', 'Read, fill and merge PDF files.'],
  ['citations', 'Format references in APA or IEEE.'],
  ['lab-report', 'Write up a lab or experiment report.'],
  ['remotion', 'Make videos with React code.'],
  ['docx', 'Create and edit Word documents.'],
  ['arxiv', 'Search and summarise papers.'],
  ['pr-review', 'Review a pull request.'],
];
export const S05_HIT = 3;
const STAGE_COLORS = [C.cyan, C.violet, C.lime];
const CARD_W = 700;
const CARD_H = 54;
const GAP = 10;
const EXPAND = 250;
const STACK_X = 110;
const STACK_Y = 150;
export const S05_SEG_AT = (i: number) => CUE.s05Bar + i * 6;

export const S05: React.FC = () => {
  const f = useCurrentFrame();
  const L = (x: number) => x - SCENE.s05.from;
  const end = SCENE.s05.dur;
  const wi = whipIn(f, 22);
  const push = p(f, end - 22, end, EZ.in);
  const scanAt = L(CUE.s05Scan);
  const expAt = L(CUE.s05Expand);
  const ex = spring({ frame: f - expAt, fps: FPS, config: { damping: 18, stiffness: 120 } });
  const exH = clamp(ex, 0, 1.06) * EXPAND;
  const dim = 1 - 0.7 * p(f, expAt, expAt + 24);
  // scan line travels the stack and parks on the hit card
  const scanY = mix(STACK_Y - 10, STACK_Y + S05_HIT * (CARD_H + GAP) + CARD_H / 2, p(f, scanAt - 30, scanAt + 6, EZ.cam));
  const scanO = p(f, scanAt - 30, scanAt - 20) * (1 - p(f, expAt + 4, expAt + 20));
  const hit = p(f, scanAt, scanAt + 10);
  // context bar
  const BAR_X = 900;
  const BAR_W = 900;
  const segW = BAR_W * 0.0075;
  const bigW = BAR_W * 0.11;
  const bigT = p(f, expAt + 10, expAt + 40);
  const body = SKILL_MD.slice(5);
  const extraAt = L(CUE.s05Extra);
  return (
    <AbsoluteFill style={{ background: C.ink }}>
      <HBlur px={60 * wi} id="s05w" style={{ transform: `translateX(${700 * wi}px) perspective(2000px) translateZ(${-500 * push}px) rotateX(${10 * push}deg)`, opacity: 1 - push }}>
      <AbsoluteFill style={{ transform: `scale(${1 + 0.025 * (f / end)})` }}>
        {CARDS.map(([name, desc], i) => {
          const isHit = i === S05_HIT;
          const y = STACK_Y + i * (CARD_H + GAP) + (i > S05_HIT ? exH : 0);
          const t = p(f, i * 4, i * 4 + 30);
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: STACK_X,
                top: 0,
                width: CARD_W,
                height: CARD_H + (isHit ? exH : 0),
                transform: `translate(${(1 - t) * -24}px, ${y}px)`,
                opacity: t * (isHit ? 1 : dim),
                filter: isHit ? undefined : `blur(${2 * (1 - dim) / 0.7}px)`,
                background: C.surface,
                borderRadius: 12,
                border: `1.5px solid ${isHit ? a(C.ember, hit) : C.line}`,
                boxShadow: isHit && hit > 0 ? `0 0 40px ${a(C.ember, 0.2 * hit)}` : undefined,
                overflow: 'hidden',
              }}
            >
              <div style={{ height: CARD_H, display: 'flex', alignItems: 'center', padding: '0 20px', gap: 16 }}>
                <span style={{ ...mono(22, 600), color: isHit && hit > 0.5 ? C.ember : C.text }}>{name}</span>
                <span style={{ ...mono(18), color: C.muted }}>{desc}</span>
              </div>
              {isHit && exH > 1 && (
                <div style={{ padding: '6px 22px', borderTop: `1px solid ${C.line}` }}>
                  {body.map((ln, k) => (
                    <div key={k} style={{ ...mono(20), color: k === 0 ? C.text : C.muted, opacity: p(f, expAt + 8 + k * 3, expAt + 24 + k * 3) }}>
                      {ln}
                    </div>
                  ))}
                  <div style={{ ...mono(20, 600), color: C.ember, marginTop: 8, opacity: p(f, extraAt, extraAt + 16) }}>→ opens template.md · runs scripts/plot.py</div>
                </div>
              )}
            </div>
          );
        })}
        {scanO > 0 && (
          <div style={{ position: 'absolute', left: STACK_X - 20, top: scanY, width: CARD_W + 40, height: 2, background: C.ember, opacity: scanO, boxShadow: glow(0.8) }} />
        )}
        {/* context window */}
        <div style={{ position: 'absolute', left: BAR_X, top: 200, ...mono(22, 600), color: C.muted, ...enter(f, L(CUE.s05Bar) - 20, 30) }}>context window</div>
        <div style={{ position: 'absolute', left: BAR_X, top: 246, width: BAR_W, height: 40, borderRadius: 8, border: `1.5px solid ${C.line2}`, ...enter(f, L(CUE.s05Bar) - 20, 30, 0, 0) }}>
          <div style={{ position: 'absolute', left: 4, top: 4, height: 32, display: 'flex', gap: 3 }}>
            {CARDS.map((_, i) => (
              <div key={i} style={{ width: segW * p(f, L(S05_SEG_AT(i)), L(S05_SEG_AT(i)) + 10), height: 32, borderRadius: 3, background: a(C.ember, 0.75) }} />
            ))}
            <div style={{ width: bigW * bigT, height: 32, borderRadius: 3, background: C.ember }} />
          </div>
        </div>
        <div style={{ position: 'absolute', left: BAR_X, top: 300, ...mono(18), color: C.dim, ...enter(f, L(CUE.s05Bar) + 50, 30) }}>
          {bigT > 0.5 ? 'names + descriptions · one skill in full' : 'names + descriptions only'}
        </div>
        {/* the ask */}
        <div
          style={{
            position: 'absolute',
            right: 120,
            top: 410,
            padding: '18px 26px',
            borderRadius: 18,
            background: C.surface2,
            border: `1px solid ${C.line}`,
            ...sans(32, 500),
            ...enter(f, L(CUE.s05Ask), 30, 16),
          }}
        >
          turn my results into a lab report.
        </div>
        {/* the three stages (agentskills.io: discovery, activation, execution) */}
        {[
          ['1', 'Discovery', 'every name + description, always', L(CUE.s05Bar)],
          ['2', 'Activation', "the matching skill's instructions load", expAt],
          ['3', 'Execution', 'extra files only if needed · scripts run, not read', extraAt],
        ].map(([n, h, d, at], i) => {
          const t0 = at as number;
          const nextAt = i === 0 ? expAt : i === 1 ? extraAt : 1e9;
          const on = p(f, t0, t0 + 14) * (1 - 0.55 * p(f, nextAt, nextAt + 14));
          return (
            <div key={i} style={{ position: 'absolute', left: BAR_X, top: 530 + i * 74, display: 'flex', alignItems: 'baseline', gap: 18, ...enter(f, t0 - 4, 24, 16, 0), opacity: f < t0 - 4 ? 0 : 0.35 + 0.65 * on }}>
              <span style={{ ...mono(30, 600), color: STAGE_COLORS[i], width: 30 }}>{n}</span>
              <span style={{ ...sans(38, 600), color: STAGE_COLORS[i], width: 230, textShadow: `0 0 24px ${a(STAGE_COLORS[i], 0.35 * on)}` }}>{h}</span>
              <span style={{ ...sans(26, 400), color: C.muted }}>{d}</span>
            </div>
          );
        })}
        <div style={{ position: 'absolute', left: BAR_X, top: 770, display: 'flex', alignItems: 'baseline', gap: 24 }}>
          <Rise text="Install dozens." f={f} at={L(CUE.s05Dozens)} style={{ ...sans(52, 600) }} />
          <Rise text="Context stays lean." f={f} at={L(CUE.s05One)} style={{ ...serif(70), color: C.ember, textShadow: glow() }} />
        </div>
      </AbsoluteFill>
      </HBlur>
    </AbsoluteFill>
  );
};

