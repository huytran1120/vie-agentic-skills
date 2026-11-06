// The single source of truth for time in "Teach It Once". Picture (src/scenes), sound
// (src/sync.ts -> out/cues.json -> scripts/soundtrack.py), captions (src/captions.ts) and QA
// (scripts/grid-check.ts) all import this file, so a change here moves everything together.
// Keep it free of React and CSS imports: Node scripts load it directly.
//
// Grid: 120 BPM at 60 fps -> 1 beat = 30 f, 1 bar = 120 f = 2 s. Every scene boundary sits on a
// beat line. v2.3 (follow-along, for students): 114 s, the DROP lands on bar 38 = 74.000 s.
//
// The VO is data, not a constant: scripts/vo.py writes src/generated/vo.json from the takes in
// audio/vo/ (draft TTS or the student's own recordings). Picture beats that answer a spoken word
// read the word's onset from it and snap to the 8th-note grid, so a re-recorded line moves its
// kinetic type with it and every cut stays on the music.
import { holdFor, PACE, readingWindows, wordCount, type PaceName } from './lib/pace';
import VO from './generated/vo.json';

export { PACE } from './lib/pace';

export const FPS = 60;
export const BPM = 120;
export const W = 1920;
export const H = 1080;
export const PACE_NAME: PaceName = 'crisp';

export const BEAT = (60 / BPM) * FPS; // 30 f
export const BAR = BEAT * 4; // 120 f
/** Absolute frame of a grid position: bar is 1-based, beat 0-3, sub = 16ths within the beat. */
export const b = (bar: number, beat = 0, sub = 0) => Math.round(((bar - 1) * 4 + beat) * BEAT + sub * (BEAT / 4));
/** A choreography length written in 60 fps frames. */
export const f60 = (frames: number) => Math.round((frames * FPS) / 60);
/** Seconds -> frames. */
export const sec = (s: number) => Math.round(s * FPS);
/** Snap a frame to the nearest 8th note (15 f). */
export const q8 = (f: number) => Math.round(f / (BEAT / 2)) * (BEAT / 2);
/** Snap a frame to the nearest beat. */
export const q4 = (f: number) => Math.round(f / BEAT) * BEAT;

export const TAIL = 0; // the film ends on black at 1:56 exactly; the score's tail is inside S12
export const TOTAL = b(59); // 6960 f = 116.000 s

// ---------------------------------------------------------------------------------------------
// Scenes (storyboard.md): contiguous, bar-aligned, [from, from + dur).
// ---------------------------------------------------------------------------------------------
const sc = (fromS: number, toS: number) => ({ from: sec(fromS), dur: sec(toS) - sec(fromS) }); // seconds, on the beat grid
export const SCENE = {
  s01: sc(0, 6), // 0:00 cold open
  s02: sc(6, 13), // 0:06 title
  s03: sc(13, 22), // 0:13 the problem
  s04: sc(22, 33.5), // 0:22 anatomy of a skill + where it lives
  s05: sc(33.5, 46), // 0:33.5 the three loading stages
  s06: sc(46, 58), // 0:46 STEP 1 install Claude Code, STEP 2 add a skill (Clip A)
  s07: sc(58, 70), // 0:56 STEP 3 just ask (Clip B part 1)
  s08: sc(70, 76), // 1:08 render timelapse (Clip B part 2)
  s09: sc(76, 81), // 1:14 the reveal (DROP)
  s10: sc(81, 93.5), // 1:19 write your own (Clip C)
  s11: sc(93.5, 99.5), // 1:31.5 share it
  s12: sc(99.5, 116), // 1:37.5 cheat sheet, go deeper + contact, tagline, vote, end card
};
export type SceneId = keyof typeof SCENE;

// ---------------------------------------------------------------------------------------------
// VO lookups (seconds in vo.json are absolute film time).
// ---------------------------------------------------------------------------------------------
type VoWord = { w: string; t0: number; t1: number };
type VoLine = { id: string; start: number; end: number; sceneEnd: number; text: string; file: string; source: string; at: number; onset: number; offset: number; dur: number; words: VoWord[] };
export const VO_LINES: VoLine[] = (VO as { lines: VoLine[] }).lines;
export const voLine = (id: string): VoLine => {
  const l = VO_LINES.find((x) => x.id === id);
  if (!l) throw new Error(`timeline: no VO line ${id}`);
  return l;
};
const norm = (s: string) => s.toLowerCase().replace(/[^a-z0-9]/g, '');
/** Frame of the onset of `word` (n-th occurrence) in VO line `id`; `fallback` seconds if the take's words differ. */
export const voAt = (id: string, word: string, fallback: number, n = 0): number => {
  const hits = voLine(id).words.filter((w) => norm(w.w) === norm(word));
  const h = hits[n];
  return h ? h.t0 * FPS : fallback * FPS;
};
/** Did the draft (TTS) voice produce any line? Then the credits say so honestly. */
export const VO_IS_DRAFT = VO_LINES.some((l) => l.source === 'tts-draft');

// ---------------------------------------------------------------------------------------------
// Acts for the motion-blur sampler (src/blur.ts): sub-frame samples never cross an act edge, so
// every designed hard cut is an act boundary here (scene starts plus the cuts inside scenes).
// ---------------------------------------------------------------------------------------------
const S = SCENE;
/** The onset of a VO word, snapped to the 8th grid and kept inside its scene. Throws if the word is missing. */
const vs = (sid: SceneId, word: string, n = 0, lead = 0): number => {
  const id = sid.toUpperCase();
  const t = voAt(id, word, -1, n);
  if (t < 0) throw new Error(`timeline: VO ${id} has no word "${word}" (#${n})`);
  const S0 = SCENE[sid];
  return Math.min(S0.from + S0.dur - 12, Math.max(S0.from + 8, q8(t) + lead));
};
export const CUE = {
  // S01 cold open
  s01Caret: S.s01.from + f60(6),
  s01Type: S.s01.from + b(1, 2) - b(1), // typing starts on beat 3 (1.0 s)
  s01Key: S.s01.from + b(2, 2) - b(1), // the return keycap appears (3.0 s) ...
  s01Enter: S.s01.from + b(2, 3) - b(1), // ... and is pressed on beat 4 of bar 2: 3.5 s
  // S02 title
  s02Sans: vs('s02', 'Claude'),
  s02Sub: vs('s02', "Anthropic's"),
  s02Serif: vs('s02', 'Agent'),
  s02Out: S.s02.from + S.s02.dur - 48, // zoom-through into S03
  // S03 the problem
  s03Words: vs('s03', 'Lab'),
  s03Slides: vs('s03', 'Slides.'),
  s03Data: vs('s03', 'Reference'),
  s03Again: vs('s03', 'And'), // "Again." x3 on three beats
  s03Grid: vs('s03', 'And') + 90, // the panel returns and multiplies
  s03Zero: Math.max(vs('s03', 'zero.'), vs('s03', 'And') + 130),
  // S04 anatomy + where it lives
  s04Collapse: S.s04.from,
  s04Folder: S.s04.from + 10,
  s04Tree: vs('s04', 'folder'),
  s04Skill: vs('s04', 'instruction'),
  s04Instr: vs('s04', 'name'), // label: name + description + steps
  s04Scripts: vs('s04', 'scripts'),
  s04Assets: vs('s04', 'scripts') + 24,
  s04Home: vs('s04', 'home'),
  s04Share: vs('s04', 'project', 1),
  // S05 the three stages (Discovery, Activation, Execution)
  s05Cards: S.s05.from,
  s05Bar: vs('s05', 'descriptions'),
  s05Ask: vs('s05', 'When'),
  s05Scan: vs('s05', 'matches'),
  s05Expand: vs('s05', 'loads'),
  s05Extra: vs('s05', 'opens'),
  s05Dozens: vs('s05', 'Install'),
  s05One: vs('s05', 'Context'),
  // S06 STEP 1 install Claude Code (left), STEP 2 add a skill (right, Clip A)
  s06Step1: vs('s06', 'Step'),
  s06Cmd1: vs('s06', 'install'),
  s06Cmd3: vs('s06', 'run'),
  s06Login: vs('s06', 'log'),
  s06Step2: vs('s06', 'two:'),
  s06Type: 0, // set below
  s06Fast: 0,
  s06Done: 0,
  // S07 STEP 3 just ask (Clip B part 1)
  s07Zoom: S.s07.from + 15,
  s07TypeAt: vs('s07', 'asked'),
  s07Freeze: Math.max(vs('s07', 'loaded'), vs('s07', 'asked') + 210), // freeze on the skill load (after the Skill line is on screen)
  s07FreezeEnd: 0, // set below
  s07Ramp8: 0, // set below
  s07Ramp16: 0, // set below
  s07Card0: vs('s07', 'storyboard,'),
  s07Card1: vs('s07', 'React'),
  s07Card2: vs('s07', 'captions,'),
  s07Card3: vs('s07', 'music,'),
  s07Card4: vs('s07', 'code.'),
  // S08 render timelapse (Clip B part 2)
  s08Strip: S.s08.from + 24,
  s08Ramp: S.s09.from - 120, // everything accelerates
  s08Black: S.s09.from - 30, // the suck-in to the drop (no dead air)
  // S09 the reveal
  drop: S.s09.from, // 76.000 s
  s09Settle: S.s09.from + 240,
  s09Line: vs('s09', 'is'),
  s09Now: vs('s09', 'right'),
  // S10 write your own
  s10Editor: S.s10.from,
  s10Mkdir: vs('s10', 'Make'),
  s10Line1: vs('s10', 'name,'), // frontmatter + name
  s10Desc: vs('s10', 'description'),
  s10Trigger: vs('s10', 'trigger.'),
  s10Steps: vs('s10', 'steps.'),
  s10Save: 0, // set below
  s10Ten: vs('s10', 'Type'), // /skills
  s10One: vs('s10', 'slash', 1), // /lab-report
  // S11 share it
  s11Fold: S.s11.from,
  s11Commit: S.s11.from + 16,
  s11Team: vs('s11', 'whole'),
  s11Ring2: vs('s11', 'other'),
  s11Open: vs('s11', 'open'),
  s11Portable: vs('s11', 'agents'),
  // S12 cheat sheet + end card
  s12Sheet: S.s12.from,
  s12Deep: vs('s12', 'This'), // just the basics
  s12Mail: vs('s12', 'Questions?'),
  s12Stop: vs('s12', 'Stop'),
  s12Once: vs('s12', 'Teach'),
  s12Vote: vs('s12', 'vote!'), // the vote card
  s12Lockup: vs('s12', 'vote!') + 70, // after the last caption
  s12Fade: S.s12.from + S.s12.dur - 80, // fade to black over 1 s
  end: TOTAL,
};
CUE.s07FreezeEnd = CUE.s07Freeze + 45; // 0.75 s freeze (held long enough to read the callout)
CUE.s07Ramp8 = CUE.s07FreezeEnd + 30;
CUE.s07Ramp16 = CUE.s07FreezeEnd + 120;
// S06 step 2: type the install command at 34 cps, then the output runs at 4x
export const SKILL_REPO = 'HaochenSHI66/claude-awesome-video-creation';
export const S06_CMD_TEXT = `npx skills add ${SKILL_REPO}`;
CUE.s06Type = CUE.s06Step2 + 14;
CUE.s06Fast = CUE.s06Type + Math.round((S06_CMD_TEXT.length / 34) * FPS) + 6;
CUE.s06Done = CUE.s06Fast + 8 + 4 * 9 + 2;
CUE.s10Save = CUE.s10Steps + 4 * 12 + 18;

export const ACT = {
  s01a: { from: S.s01.from, dur: CUE.s01Enter - S.s01.from },
  s01b: { from: CUE.s01Enter, dur: S.s02.from - CUE.s01Enter },
  s02: S.s02,
  s03a: { from: S.s03.from, dur: CUE.s03Words - S.s03.from },
  s03b: { from: CUE.s03Words, dur: CUE.s03Slides - CUE.s03Words },
  s03c: { from: CUE.s03Slides, dur: CUE.s03Data - CUE.s03Slides },
  s03d: { from: CUE.s03Data, dur: CUE.s03Again - CUE.s03Data },
  s03e: { from: CUE.s03Again, dur: 30 },
  s03f: { from: CUE.s03Again + 30, dur: 30 },
  s03g: { from: CUE.s03Again + 60, dur: CUE.s03Grid - CUE.s03Again - 60 },
  s03h: { from: CUE.s03Grid, dur: S.s04.from - CUE.s03Grid },
  s04: S.s04,
  s05: S.s05,
  s06: S.s06,
  s07: S.s07,
  s08a: { from: S.s08.from, dur: CUE.s08Black - S.s08.from },
  s08b: { from: CUE.s08Black, dur: S.s09.from - CUE.s08Black },
  s09: S.s09,
  s10: S.s10,
  s11: S.s11,
  s12: S.s12,
};

// ---------------------------------------------------------------------------------------------
// COPY: every on-screen string. kind 'ui' = a string the product shows (code, a command, a label).
// ---------------------------------------------------------------------------------------------
export type Copy = {
  id: string;
  text: string;
  in: number;
  resolved: number;
  out: number;
  kind?: 'copy' | 'ui';
  chain?: string;
  mode?: 'build' | 'replace';
};
const pace = PACE[PACE_NAME];
const cp = (id: string, text: string, inF: number, resolved: number, out: number, kind: 'copy' | 'ui' = 'copy'): Copy => ({ id, text, in: inF, resolved, out, kind });
const ui = (id: string, text: string, inF: number, out: number, resolved = inF + 12): Copy => cp(id, text, inF, resolved, out, 'ui');

/** The exact first line of the student's prompt (shotlist_for_student.md, Clip B). */
export const PROMPT_SHORT = '> make a launch video about agent skills.';

export const SKILL_MD = [
  '---',
  'name: lab-report',
  'description: Writes lab reports from my results.',
  '  Use when I ask for a lab report.',
  '---',
  '1. Read results/*.csv and notes.md',
  '2. Follow template.md: Aim, Method, Results, Discussion',
  '3. One figure per table (run scripts/plot.py)',
  '4. Under 1,500 words, APA citations',
];

export const COPY: Copy[] = [
  // S01
  ui('s01.prompt', PROMPT_SHORT, CUE.s01Type, CUE.s01Enter, CUE.s01Type + Math.ceil((PROMPT_SHORT.length / 28) * FPS)),
  // S02
  cp('s02.sans', 'Claude Code', CUE.s02Sans, CUE.s02Sans + 70, CUE.s02Out),
  cp('s02.sub', "Anthropic's AI agent · runs in your terminal · reads and writes your files", CUE.s02Sub, CUE.s02Sub + 40, CUE.s02Out),
  cp('s02.serif', 'Agent Skills', CUE.s02Serif, CUE.s02Serif + 36, CUE.s02Out),
  // S03
  ui('s03.ask', 'Write my lab report. Sections: Aim, Method, Results.', S.s03.from + 20, CUE.s03Words),
  cp('s03.w1', 'Lab reports.', CUE.s03Words, CUE.s03Words + 6, CUE.s03Slides),
  cp('s03.w2', 'Slides.', CUE.s03Slides, CUE.s03Slides + 6, CUE.s03Data),
  cp('s03.w3', 'Reference lists.', CUE.s03Data, CUE.s03Data + 6, CUE.s03Again),
  cp('s03.w4', 'Again.', CUE.s03Again, CUE.s03Again + 6, CUE.s03Grid),
  cp('s03.zero1', 'Your AI starts from', CUE.s03Grid + 30, CUE.s03Grid + 56, S.s04.from),
  cp('s03.zero2', 'zero.', CUE.s03Zero, CUE.s03Zero + 24, S.s04.from),
  // S04
  ui('s04.t0', 'lab-report/', CUE.s04Tree, S.s05.from - 18),
  ui('s04.t1', '├── SKILL.md', CUE.s04Tree + 6, S.s05.from - 18),
  ui('s04.t2', '├── scripts/plot.py', CUE.s04Tree + 12, S.s05.from - 18),
  ui('s04.t3', '└── template.md', CUE.s04Tree + 18, S.s05.from - 18),
  cp('s04.l1', 'name · description · steps', CUE.s04Instr, CUE.s04Instr + 24, S.s05.from - 18),
  cp('s04.l2', 'code it runs', CUE.s04Scripts, CUE.s04Scripts + 24, S.s05.from - 18),
  cp('s04.l3', 'files it reads', CUE.s04Assets, CUE.s04Assets + 24, S.s05.from - 18),
  ui('s04.home', '~/.claude/skills/lab-report/', CUE.s04Home, S.s05.from - 18),
  cp('s04.homeTag', 'personal · every project', CUE.s04Home + 10, CUE.s04Home + 40, S.s05.from - 18),
  ui('s04.proj', '.claude/skills/lab-report/', CUE.s04Home + 14, S.s05.from - 18),
  cp('s04.projTag', 'this project · commit to share', CUE.s04Share, CUE.s04Share + 30, S.s05.from - 18),
  // S05
  ui('s05.ctx', 'context window', CUE.s05Bar - 20, S.s06.from - 12),
  cp('s05.st1', '1 Discovery · every name + description', CUE.s05Bar, CUE.s05Bar + 30, S.s06.from - 12),
  ui('s05.ask', 'turn my results into a lab report.', CUE.s05Ask, S.s06.from - 12),
  cp('s05.st2', "2 Activation · the matching skill's instructions load", CUE.s05Expand, CUE.s05Expand + 30, S.s06.from - 12),
  cp('s05.st3', '3 Execution · extra files only if needed', CUE.s05Extra, CUE.s05Extra + 30, S.s06.from - 12),
  cp('s05.dozens', 'Install dozens.', CUE.s05Dozens, CUE.s05Dozens + 24, S.s06.from - 12),
  cp('s05.one', 'Context stays lean.', CUE.s05One, CUE.s05One + 24, S.s06.from - 12),
  // S06
  cp('s06.step1', 'STEP 1/3 · Install Claude Code', CUE.s06Step1, CUE.s06Step1 + 24, S.s07.from),
  ui('s06.mac', 'curl -fsSL https://claude.ai/install.sh | bash', CUE.s06Cmd1, S.s07.from),
  ui('s06.win', 'irm https://claude.ai/install.ps1 | iex', CUE.s06Cmd1 + 18, S.s07.from),
  ui('s06.run', 'cd my-project && claude', CUE.s06Cmd3, S.s07.from),
  cp('s06.login', 'Log in in the browser. Needs Claude Pro, Max, Team, Enterprise or an API (Console) account; the free plan has no Claude Code.', CUE.s06Login, CUE.s06Login + 60, S.s07.from),
  cp('s06.step2', 'STEP 2/3 · Add a skill', CUE.s06Step2 - 10, CUE.s06Step2 + 14, S.s07.from),
  ui('s06.cmd', 'npx skills add HaochenSHI66/claude-awesome-video-creation', CUE.s06Type, S.s07.from),
  ui('s06.ok', '✓ Installed 1 skill', CUE.s06Done, S.s07.from - 12),
  // S07
  cp('s07.step3', 'STEP 3/3 · Just ask', S.s07.from + 10, S.s07.from + 34, S.s08.from),
  ui('s07.callout', '← skill loaded: matched by its description', CUE.s07Freeze + 6, CUE.s07FreezeEnd + 60),
  ui('s07.direct', 'or call it directly:  /claude-awesome-video-creation', CUE.s07FreezeEnd + 10, S.s08.from - 10),
  // S08
  ui('s08.real', 'real time', CUE.s08Strip, CUE.s08Black),
  ui('s08.screen', 'on screen', CUE.s08Strip, CUE.s08Black),
  // S09
  cp('s09.line', "is the video you're watching", CUE.s09Line, CUE.s09Line + 40, S.s10.from - 12),
  cp('s09.now', 'right now.', CUE.s09Now, CUE.s09Now + 30, S.s10.from - 12),
  // S10
  ui('s10.mkdir', 'mkdir -p .claude/skills/lab-report', CUE.s10Mkdir, S.s11.from),
  ...SKILL_MD.map((t, i) => ui(`s10.code${i}`, t, CUE.s10Line1, S.s11.from)),
  cp('s10.lName', 'name → becomes /lab-report', CUE.s10Line1 + 20, CUE.s10Line1 + 50, S.s11.from),
  cp('s10.lDesc', 'description → the trigger: say WHEN', CUE.s10Trigger, CUE.s10Trigger + 30, S.s11.from),
  cp('s10.lSteps', 'steps → what you always repeat', CUE.s10Steps + 20, CUE.s10Steps + 50, S.s11.from),
  ui('s10.skills', '/skills', CUE.s10Ten, S.s11.from),
  ui('s10.run', '/lab-report', CUE.s10One, S.s11.from),
  // S11
  ui('s11.commit', 'git add .claude/skills && git commit -m "add lab-report skill"', CUE.s11Commit, S.s12.from - 12),
  ui('s11.team', 'your group', CUE.s11Team + 30, CUE.s11Open),
  ui('s11.cc', 'Claude Code', CUE.s11Ring2, S.s12.from - 12),
  ui('s11.other', 'other AI agents that support skills', CUE.s11Ring2 + 8, S.s12.from - 12),
  cp('s11.open', 'An open standard.', CUE.s11Open, CUE.s11Open + 24, S.s12.from - 12),
  ui('s11.portable', 'agentskills.io', CUE.s11Portable, S.s12.from - 12),
  // S12
  cp('s12.title', 'Cheat sheet', CUE.s12Sheet + 10, CUE.s12Sheet + 40, CUE.s12Fade + 50),
  cp('s12.deep', 'This is just the basics.', CUE.s12Deep, CUE.s12Deep + 30, CUE.s12Stop),
  ui('s12.mail', '24130819d@connect.polyu.hk', CUE.s12Mail, CUE.s12Fade + 50),
  cp('s12.stop', 'Stop repeating yourself.', CUE.s12Stop, CUE.s12Stop + 30, CUE.s12Fade),
  cp('s12.once', 'Teach it once.', CUE.s12Once, CUE.s12Once + 36, CUE.s12Fade + 50),
  ui('s12.lockup', 'Claude Code · Agent Skills · COMP4431 · SHI Haochen · 24130819D', CUE.s12Lockup, CUE.s12Fade + 50),
  ui('s12.credit', VO_IS_DRAFT ? 'Made with Claude Code + my skill claude-awesome-video-creation (built on cinetic). Voice: draft TTS, to be replaced.' : 'Made with Claude Code + my skill claude-awesome-video-creation (built on cinetic). Voice: SHI Haochen.', CUE.s12Lockup + 15, CUE.s12Fade + 50),
];

/** One COPY entry by id. */
export const copy = (id: string): Copy => {
  const c = COPY.find((x) => x.id === id);
  if (!c) throw new Error(`timeline: no COPY entry "${id}"`);
  return c;
};
export const chainOf = (id: string): Copy[] => COPY.filter((x) => x.chain === id).sort((p, q) => p.in - q.in);
export const READ = readingWindows(COPY, pace, FPS, TOTAL);
void holdFor;
void wordCount;
