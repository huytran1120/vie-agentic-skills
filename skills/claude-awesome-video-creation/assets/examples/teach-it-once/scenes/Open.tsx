// S01 cold open, S02 title, S03 the problem.
import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { a, C } from '../brand/tokens';
import { S01_KEYS, S01_TEXT, scramble, typed } from '../schedule';
import { CUE, SCENE } from '../timeline';
import { Caret, Center, clamp, enter, EZ, glow, lmix, mix, mono, MONO_ADV, p, pulse, Rise, sans, serif, sheen, Win } from '../ui';

// ---------------------------------------------------------------------------------------------
// S01: a blinking ember caret, the prompt types itself, the return key, a 2-frame white flash.
// ---------------------------------------------------------------------------------------------
export const S01: React.FC = () => {
  const f = useCurrentFrame();
  const L = (x: number) => x - SCENE.s01.from;
  const enterAt = L(CUE.s01Enter);
  const n = typed(S01_KEYS.map(L), f);
  const size = 44;
  const full = ('> ' + S01_TEXT).length;
  const left = 960 - (full * size * MONO_ADV) / 2;
  const typing = f >= L(CUE.s01Type) && n < S01_TEXT.length;
  const caretOn = f < L(CUE.s01Caret) ? false : typing ? true : Math.floor((f - L(CUE.s01Caret)) / 30) % 2 === 0;
  const before = f < enterAt;
  // keycap
  const keyIn = p(f, L(CUE.s01Key), L(CUE.s01Key) + 18);
  const press = f >= enterAt ? 1 - 0.08 * pulse(f - enterAt, 3, 4) : 1;
  const flash = f >= enterAt && f < enterAt + 4;
  const glowK = f >= enterAt + 4 ? Math.exp(-(f - enterAt - 4) / 14) : 0;
  // after the flash: the lone caret returns and keeps breathing until the title
  const after = f >= enterAt + 30;
  const afterO = after ? p(f, enterAt + 30, enterAt + 48) * (1 - p(f, 330, 356, EZ.in)) : 0;
  const drift = 1 + 0.02 * (f / 360);
  return (
    <AbsoluteFill style={{ background: C.ink }}>
      <AbsoluteFill style={{ transform: `scale(${drift})` }}>
        {before && (
          <div style={{ position: 'absolute', left, top: 540 - size * 0.7, ...mono(size), color: C.text }}>
            <span style={{ color: C.muted }}>{'> '}</span>
            {S01_TEXT.slice(0, n)}
            <Caret on={caretOn} h={size * 1.05} w={size * MONO_ADV} style={{ marginLeft: 2, marginTop: -6 }} />
          </div>
        )}
        {before && keyIn > 0 && (
          <Center x={960} y={680} style={{ opacity: keyIn, transform: `translate(-50%, -50%) translateY(${(1 - keyIn) * 12}px) scale(${press})` }}>
            <div
              style={{
                width: 92,
                height: 80,
                borderRadius: 14,
                border: `1.5px solid ${C.line2}`,
                borderBottomWidth: 5,
                background: C.surface,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                ...mono(40, 600),
                color: C.text,
              }}
            >
              ↵
            </div>
          </Center>
        )}
        {after && (
          <Center y={540} style={{ opacity: afterO }}>
            <Caret on={Math.floor((f - enterAt) / 30) % 2 === 0} h={size * 1.05} w={size * MONO_ADV} />
          </Center>
        )}
      </AbsoluteFill>
      {glowK > 0 && <AbsoluteFill style={{ background: `radial-gradient(circle 600px at 960px 540px, ${a(C.ember, 0.35 * glowK)}, ${a(C.ember, 0)})` }} />}
      {flash && <AbsoluteFill style={{ background: C.flash }} />}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------------------------
// S02: "Claude Code" letter by letter, "Agent Skills" mask-revealed, ember underline, blur out.
// ---------------------------------------------------------------------------------------------
export const S02: React.FC = () => {
  const f = useCurrentFrame();
  const L = (x: number) => x - SCENE.s02.from;
  const sansAt = L(CUE.s02Sans);
  const serifAt = L(CUE.s02Serif);
  // exit: a zoom-through into the next scene (accelerating, log-space), not a fade
  const zt = p(f, L(CUE.s02Out) + 6, SCENE.s02.dur, EZ.in);
  const out = { o: 1 - p(f, SCENE.s02.dur - 14, SCENE.s02.dur, EZ.in), blur: 18 * zt };
  const push = mix(1, 1.04, f / SCENE.s02.dur) * lmix(1, 7, zt);
  const yaw = mix(-5, 3, p(f, 0, SCENE.s02.dur, EZ.cam));
  const reveal = p(f, serifAt, serifAt + 36);
  const under = p(f, serifAt + 36, serifAt + 84, EZ.cam);
  const word = 'Claude Code';
  return (
    <AbsoluteFill style={{ background: C.ink }}>
      <AbsoluteFill style={{ transform: `perspective(1800px) rotateY(${yaw}deg) scale(${push})`, transformOrigin: '50% 52%', opacity: out.o, filter: `blur(${out.blur}px)` }}>
        <Center y={390}>
          <div style={{ ...sans(56, 500), color: C.muted, display: 'flex' }}>
            {word.split('').map((ch, i) => (
              <span key={i} style={{ display: 'inline-block', ...enter(f, sansAt + i * 4, 36, 12, 8) }}>
                {ch === ' ' ? ' ' : ch}
              </span>
            ))}
          </div>
        </Center>
        <Center y={462}>
          <Rise text="Anthropic's AI agent · runs in your terminal · reads and writes your files" f={f} at={L(CUE.s02Sub)} stagger={3} style={{ ...sans(30, 400), color: C.dim }} />
        </Center>
        <Center y={600}>
          <div style={{ ...serif(180), clipPath: `inset(${mix(125, -20, reveal)}% -5% -20% -5%)`, opacity: reveal > 0 ? 1 : 0, transform: `translateY(${(1 - reveal) * 40}px)` }}>
            <span style={sheen(f, serifAt + 40, 60, C.text, C.emberGlow)}>Agent</span>{' '}
            <span style={{ position: 'relative', display: 'inline-block' }}>
              <span style={sheen(f, serifAt + 52, 60, C.text, C.emberGlow)}>Skills</span>
              <span
                style={{
                  position: 'absolute',
                  left: 0,
                  bottom: 6,
                  height: 2,
                  width: `${under * 100}%`,
                  background: C.ember,
                  boxShadow: glow(0.6),
                }}
              />
            </span>
          </div>
        </Center>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------------------------
// S03: a chat panel repeats itself; kinetic words on the beat; "Again." stutters; 12 panels.
// ---------------------------------------------------------------------------------------------
const ASK = 'Write my lab report. Sections: Aim, Method, Results.';

const ChatPanel: React.FC<{ count: number; typedN: number; w?: number; h?: number }> = ({ count, typedN, w = 960, h = 540 }) => {
  const bubbles = Math.min(3, count);
  return (
    <Win w={w} h={h} title="chat">
      <div style={{ position: 'absolute', right: 22, top: 16, ...mono(22, 600), color: C.ember }}>×{count}</div>
      {Array.from({ length: bubbles }).map((_, i) => {
        const last = i === bubbles - 1;
        const text = last ? ASK.slice(0, typedN) : ASK;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              right: 28,
              top: 70 + i * 120,
              maxWidth: w - 160,
              padding: '16px 22px',
              borderRadius: 16,
              background: C.surface2,
              border: `1px solid ${C.line}`,
              ...sans(26, 500),
              whiteSpace: 'normal',
              color: last ? C.text : C.muted,
              opacity: last ? 1 : 0.55,
            }}
          >
            {text}
            {last && typedN < ASK.length && <span style={{ color: C.ember }}>▍</span>}
          </div>
        );
      })}
      <div style={{ position: 'absolute', left: 28, bottom: 26, ...mono(18), color: C.dim, opacity: 0.8 }}>new chat · no memory of last time</div>
    </Win>
  );
};

export const S03: React.FC = () => {
  const f = useCurrentFrame();
  const L = (x: number) => x - SCENE.s03.from;
  const wordsAt = L(CUE.s03Words);
  const words: [string, number, number][] = [
    ['Lab reports.', wordsAt, L(CUE.s03Slides)],
    ['Slides.', L(CUE.s03Slides), L(CUE.s03Data)],
    ['Reference lists.', L(CUE.s03Data), L(CUE.s03Again)],
  ];
  const againAt = L(CUE.s03Again);
  const gridAt = L(CUE.s03Grid);
  const end = SCENE.s03.dur;
  // phase 1: the panel, the ask typed 3 times (counter climbs)
  const cycle = Math.max(1, Math.floor((wordsAt - 10) / 3));
  const k = Math.min(2, Math.floor(Math.max(0, f - 10) / cycle));
  const count = 1 + k;
  const typedN = Math.min(ASK.length, Math.floor(clamp((f - 10 - k * cycle) / (cycle * 0.6)) * ASK.length));
  const hand = p(f, 0, 30, EZ.out);
  const panelIn: React.CSSProperties = { opacity: clamp(hand * 2), filter: `blur(${12 * (1 - hand)}px)`, transform: `scale(${lmix(1.5, 1, hand)})` };
  // grid
  const g = p(f, gridAt, gridAt + 70, EZ.cam);
  const gridCount = 1 + Math.min(11, Math.floor(Math.max(0, f - gridAt) / 4));
  const dimGrid = 1 - 0.6 * p(f, gridAt + 40, gridAt + 70);
  const zeroLine = L(CUE.s03Grid) + 30;
  const zeroAt = L(CUE.s03Zero);
  const collapse = p(f, end - 26, end - 2, EZ.in);
  const outK = { o: 1 - p(f, end - 8, end, EZ.in), blur: 0 };
  const wall = p(f, gridAt + 10, gridAt + 90, EZ.cam);
  return (
    <AbsoluteFill style={{ background: C.ink }}>
      {f < wordsAt && (
        <Center y={520} style={{ ...panelIn, transform: `translate(-50%, -50%) ${panelIn.transform} scale(${1 + 0.02 * (f / wordsAt)})` }}>
          <div style={{ position: 'relative', width: 960, height: 540 }}>
            <ChatPanel count={count} typedN={typedN} />
          </div>
        </Center>
      )}
      {words.map(([w, from, to], i) =>
        f >= from && f < to ? (
          <Center key={i} y={520} style={{ transform: `translate(-50%, -50%) scale(${1 + 0.06 * (1 - p(f, from, from + 16))})` }}>
            {i === 0 ? (
              <div style={{ ...sans(120, 600), transform: `translateX(${(1 - p(f, from - 1, from + 20)) * -260}px)`, filter: `blur(${16 * (1 - p(f, from - 1, from + 14))}px)`, opacity: p(f, from - 1, from + 6) }}>{w}</div>
            ) : i === 1 ? (
              <div style={{ ...sans(120, 600), transform: `translateY(${(1 - p(f, from - 1, from + 20)) * -160}px) scale(${mix(1.25, 1, p(f, from - 1, from + 20))})`, opacity: p(f, from - 1, from + 6) }}>{w}</div>
            ) : (
              <div style={{ ...sans(120, 600) }}>{scramble(w, f, from - 1, 1.6, 6)}</div>
            )}
          </Center>
        ) : null,
      )}
      {f >= againAt && f < gridAt &&
        [0, 1, 2].map((i) => {
          const at = againAt + i * 30;
          if (f < at) return null;
          const fresh = f - at < 30;
          return (
            <Center key={i} x={960 + i * 8} y={520 + i * 8} style={{ opacity: fresh ? 1 : 0.22, transform: `translate(-50%, -50%) scale(${1 + 0.08 * (1 - p(f, at, at + 12))})` }}>
              <div style={{ ...sans(120, 600), color: i === 2 && fresh ? C.text : C.muted }}>Again.</div>
            </Center>
          );
        })}
      {f >= gridAt && (
        <AbsoluteFill style={{ opacity: outK.o }}>
          <AbsoluteFill style={{ transform: `perspective(1600px) rotateX(${14 * wall}deg) rotateY(${-16 * wall}deg) scale(${mix(1, 0.92, wall)})`, transformOrigin: '50% 50%' }}>
          {Array.from({ length: gridCount }).map((_, i) => {
            const col = i % 4;
            const row = Math.floor(i / 4);
            const tx = 240 + col * 480;
            const ty = 250 + row * 230;
            const x = i === 0 ? mix(960, tx, g) : tx;
            const y = i === 0 ? mix(520, ty, g) : ty;
            const s0 = i === 0 ? mix(1, 0.42, g) : 0.42 * p(f, gridAt + i * 4, gridAt + i * 4 + 18);
            const cd = clamp(collapse * 1.3 - (i % 4) * 0.05);
            const s = s0 * (1 - cd);
            const xx = mix(x, 960, cd);
            const yy = mix(y, 520, cd);
            return (
              <div key={i} style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${xx}px, ${yy}px) translate(-50%, -50%) scale(${Math.max(0.001, s)})`, opacity: dimGrid * (1 - cd * 0.6) }}>
                <div style={{ position: 'relative', width: 960, height: 540 }}>
                  <ChatPanel count={i + 3} typedN={ASK.length} />
                </div>
              </div>
            );
          })}
          </AbsoluteFill>
          <AbsoluteFill style={{ background: `radial-gradient(ellipse 900px 300px at 960px 540px, ${a(C.ink, 0.92 * p(f, zeroLine - 10, zeroLine + 20))}, ${a(C.ink, 0)})` }} />
          <Center y={540} style={{ opacity: 1 - collapse, transform: `translate(-50%, -50%) scale(${1 - 0.1 * collapse})` }}>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: 22 }}>
              <Rise text="Your AI starts from" f={f} at={zeroLine} style={{ ...sans(64, 500) }} />
              <Rise text="zero." f={f} at={zeroAt} dur={30} style={{ ...serif(104), color: C.ember, textShadow: glow() }} />
            </div>
          </Center>
          {collapse > 0.6 && <Center y={520} style={{ width: 16, height: 16, borderRadius: 8, background: C.ember, boxShadow: glow(1.5), opacity: p(f, end - 12, end - 4) }}>{null}</Center>}
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};
