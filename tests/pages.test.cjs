const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const catalog = require('../docs/catalog.js');
const i18n = require('../docs/i18n.js');
const skills = require('../docs/skills.min.json');
const root = path.resolve(__dirname, '..');

test('all real skills remain discoverable without filters', () => {
  assert.equal(catalog.filterSkills(skills).length, skills.length);
  assert.equal(new Set(catalog.filterSkills(skills).map(skill => skill.id)).size, skills.length);
});

test('recommendations are real skills, not fictional popularity rankings', () => {
  const sorted = catalog.filterSkills(skills);
  assert.equal(sorted[0].id, 'ui-ux-pro-max');
  assert.equal(sorted[1].id, 'code-review');
  const html = fs.readFileSync(path.join(root, 'docs/index.html'), 'utf8');
  assert.ok(html.includes('không phải xếp hạng lượt tải'));
  assert.ok(!html.includes('125K'));
});

test('source discovery finds all 35 Matt Pocock skills', () => {
  assert.equal(catalog.filterSkills(skills, { query: 'mattpocock/skills' }).length, 35);
  assert.ok(catalog.filterSkills(skills, { query: 'Matt Pocock' }).some(skill => skill.id === 'code-review'));
});

test('multi-token search matches across fields and ignores diacritics', () => {
  const fixtures = [{ id: 'web-test', category: 'testing', description: 'Kiểm thử giao diện', tags: ['browser'], author: 'Huy Trần' }];
  assert.equal(catalog.filterSkills(fixtures, { query: 'kiem thu browser' }).length, 1);
  assert.equal(catalog.filterSkills(fixtures, { query: 'huy tran' }).length, 1);
  assert.equal(catalog.filterSkills(fixtures, { query: 'browser absent' }).length, 0);
});

test('group filters use explicit categories and exact category remains available', () => {
  const security = catalog.filterSkills(skills, { group: 'security' });
  assert.equal(security.length, skills.filter(skill => skill.category === 'security').length);
  assert.ok(catalog.filterSkills(skills, { group: 'web' }).some(skill => skill.id === 'frontend-design'));
  for (const category of new Set(skills.map(skill => skill.category))) {
    assert.equal(catalog.filterSkills(skills, { category }).length, skills.filter(skill => skill.category === category).length);
  }
});

test('filter combinations can produce a recoverable empty state', () => {
  assert.equal(catalog.filterSkills(skills, { query: 'impossible-skill-name-8743' }).length, 0);
  assert.equal(catalog.filterSkills(skills, { category: 'security', query: 'mattpocock/skills' }).length, 0);
});

test('sorting is deterministic and does not mutate the catalog', () => {
  const before = skills.map(skill => skill.id);
  const az = catalog.filterSkills(skills, { sort: 'az' });
  const za = catalog.filterSkills(skills, { sort: 'za' });
  assert.deepEqual(az.map(skill => skill.id), za.map(skill => skill.id).reverse());
  assert.deepEqual(before, skills.map(skill => skill.id));
});

test('every agent generates the explicit target and link mode', () => {
  for (const [target] of catalog.agents) {
    assert.equal(catalog.installCommand('code-review', target), `./vas install code-review --target ${target} --mode link`);
  }
  assert.throws(() => catalog.installCommand('code-review', 'invalid'));
  assert.equal(catalog.installCommand("test'; whoami", 'codex'), "./vas install 'test'\\''; whoami' --target codex --mode link");
});

test('project installation points at each agent folder and quotes shell-sensitive paths', () => {
  for (const [target, folder] of Object.entries(catalog.targetFolders)) {
    assert.equal(catalog.installCommand('code-review', target, { scope: 'project', projectPath: '/Projects/my app' }),
      `./vas install code-review --target ${target} --mode link --dest '/Projects/my app/${folder}'`);
  }
  const all = catalog.installCommand('code-review', 'all', { scope: 'project', projectPath: '/Projects/app/' }).split('\n');
  assert.equal(all.length, 7);
  assert.ok(all.every(line => !line.includes('--target all') && line.includes('--dest /Projects/app/')));
  assert.equal(catalog.installCommand('code-review', 'codex', { scope: 'project', projectPath: 'C:\\Projects\\my-app' }),
    "./vas install code-review --target codex --mode link --dest 'C:/Projects/my-app/.codex/skills'");
  const quoted = catalog.installCommand('code-review', 'codex', { scope: 'project', projectPath: "/Projects/it's $(whoami)" });
  assert.ok(quoted.endsWith("--dest '/Projects/it'\\''s $(whoami)/.codex/skills'"));
  for (const projectPath of ['', 'relative/path', '~/app', '/app\nmalicious']) {
    assert.throws(() => catalog.installCommand('code-review', 'codex', { scope: 'project', projectPath }));
  }
});

test('global installation uses supported CLI semantics and rejects global all', () => {
  assert.equal(catalog.installCommand('code-review', 'codex', { scope: 'global' }), './vas install code-review --target codex --mode link --global');
  assert.throws(() => catalog.installCommand('code-review', 'all', { scope: 'global' }));
});

test('installation plans keep install, status, uninstall and prompts on the same destination', () => {
  for (const [target, folder] of Object.entries(catalog.targetFolders)) {
    for (const mode of ['link', 'copy']) {
      const plan = catalog.installationPlan('code-review', target, { scope: 'project', projectPath: '/Projects/my app', mode });
      assert.equal(plan.install, `./vas install code-review --target ${target} --mode ${mode} --dest '/Projects/my app/${folder}'`);
      assert.equal(plan.status, `./vas status --target ${target} --dest '/Projects/my app/${folder}'`);
      assert.equal(plan.uninstall, `./vas uninstall code-review --target ${target} --dest '/Projects/my app/${folder}'`);
      assert.deepEqual(plan.paths, [`/Projects/my app/${folder}/code-review/SKILL.md`]);
      assert.ok(plan.prompt.includes(plan.paths[0]));
    }
    const global = catalog.installationPlan('code-review', target, { scope: 'global', mode: 'copy' });
    assert.equal(global.install, `./vas install code-review --target ${target} --mode copy --global`);
    assert.equal(global.status, `./vas status --target ${target} --global`);
    assert.equal(global.uninstall, `./vas uninstall code-review --target ${target} --global`);
    assert.deepEqual(global.paths, [`${catalog.globalFolders[target]}/code-review/SKILL.md`]);
  }
  assert.throws(() => catalog.installationPlan('code-review', 'codex', { mode: 'invalid' }));
  assert.throws(() => catalog.installationPlan('code-review', 'codex', { scope: 'invalid' }));
});

test('all-agent plans preserve CLI scopes and namespaced skills use the actual installed folder', () => {
  const project = catalog.installationPlan('blender-skills/blender-director', 'all', { scope: 'project', projectPath: '/Projects/app', mode: 'copy' });
  assert.equal(project.install.split('\n').length, 7);
  assert.equal(project.status.split('\n').length, 7);
  assert.equal(project.uninstall.split('\n').length, 7);
  assert.equal(project.paths.length, 7);
  assert.ok(project.paths.every(path => path.endsWith('/blender-director/SKILL.md')));
  const repository = catalog.installationPlan('code-review', 'all');
  assert.equal(repository.install, './vas install code-review --target all --mode link');
  assert.equal(repository.status, './vas status --target all');
  assert.equal(repository.paths.length, 7);
  for (const skill of skills) {
    const plan = catalog.installationPlan(skill.id, 'codex');
    assert.equal(plan.paths[0], `.codex/skills/${path.basename(skill.path)}/SKILL.md`, skill.id);
  }
});

test('getting started has usable CLI examples before a skill is selected', () => {
  const html = fs.readFileSync(path.join(root, 'docs/index.html'), 'utf8');
  assert.ok(html.includes('id="cli-setup"'));
  assert.ok(html.includes('chmod +x vas vas.py'));
  assert.ok(html.includes('./vas search code-review'));
  assert.ok(html.includes('./vas show code-review'));
  assert.ok(html.includes('data-install-skill="code-review"'));
  assert.ok(!html.includes('Chọn một skill trong catalog để tạo lệnh cài.'));
  assert.ok(!/data-copy-element="quickstart-command"[^>]*disabled/.test(html));
});

test('search ranks exact names, name prefixes and tags before description matches', () => {
  const fixtures = [
    { id: 'a-description', category: 'general', description: 'docker frontend' },
    { id: 'b-tags', category: 'general', tags: ['docker', 'front-end'] },
    { id: 'docker-expert', category: 'devops' },
    { id: 'docker', category: 'devops' }
  ];
  assert.deepEqual(catalog.filterSkills(fixtures, { query: 'docker' }).map(s => s.id), ['docker', 'docker-expert', 'b-tags', 'a-description']);
  assert.deepEqual(catalog.filterSkills(fixtures, { query: 'front-end' }).map(s => s.id), ['b-tags']);
  assert.deepEqual(catalog.filterSkills(fixtures, { query: 'frontend' }).map(s => s.id), ['a-description']);
  assert.deepEqual(catalog.filterSkills(fixtures, { query: 'docker', sort: 'az' }).map(s => s.id), ['a-description', 'b-tags', 'docker', 'docker-expert']);
});

test('catalog links restore filters and skills without sharing local project paths', () => {
  const state = { query: 'front-end design', selected: 'code-review', target: 'codex', group: 'web', category: 'frontend', sort: 'za', view: 'grid', projectPath: '/private/project', scope: 'project' };
  const params = catalog.catalogParams(state);
  assert.ok(!params.includes('private'));
  const restored = catalog.readCatalogState(params);
  for (const key of ['query', 'selected', 'target', 'group', 'category', 'sort', 'view']) assert.equal(restored[key], state[key]);
  const invalid = catalog.readCatalogState('?agent=oops&group=oops&sort=oops&view=oops');
  assert.equal(invalid.target, 'antigravity');
  assert.equal(invalid.group, 'all');
  assert.equal(invalid.sort, 'recommended');
  assert.equal(invalid.view, 'list');
});

test('all links use actual catalog paths, including nested skills', () => {
  for (const skill of skills) {
    const url = catalog.skillUrl(skill);
    assert.ok(url.startsWith('../skills/'));
    assert.ok(url.endsWith('/SKILL.md'));
    assert.ok(fs.existsSync(path.join(root, skill.path, 'SKILL.md')));
  }
  assert.equal(catalog.skillUrl({ id: 'x', path: 'skills/nested/x' }), '../skills/nested/x/SKILL.md');
  assert.throws(() => catalog.skillUrl({ id: 'x', path: 'skills/../outside' }));
});

test('upstream links cannot be replaced by unrelated or executable URLs', () => {
  assert.equal(catalog.sourceUrl({ source_repo: 'mattpocock/skills', source: 'javascript:alert(1)' }), 'https://github.com/mattpocock/skills');
  assert.equal(catalog.sourceUrl({ source_repo: 'mattpocock/skills', source: 'https://github.com/mattpocock/skills-evil/x' }), 'https://github.com/mattpocock/skills');
  assert.equal(catalog.sourceUrl({ source_repo: 'mattpocock/skills', source: 'https://github.com/mattpocock/skills/tree/main/pr' }), 'https://github.com/mattpocock/skills/tree/main/pr');
  assert.equal(catalog.sourceUrl({}), null);
});

test('local skill links encode filenames and cannot escape the skill tree', () => {
  const url = catalog.skillUrl({ id: 'example', path: 'skills/nested/a b#c' });
  assert.equal(url, '../skills/nested/a%20b%23c/SKILL.md');
  assert.equal(new URL(url, 'http://127.0.0.1:8765/docs/').pathname,
    '/skills/nested/a%20b%23c/SKILL.md');
  for (const path of ['skills/../outside', 'skills/./x', 'skills//x', 'outside/x', 'skills/a\\b']) {
    assert.throws(() => catalog.skillUrl({ id: 'x', path }));
  }
});

test('the public page has its own identity and supports both local and Pages builds', () => {
  const html = fs.readFileSync(path.join(root, 'docs/index.html'), 'utf8');
  assert.ok(html.includes('<title>Vie Agentic Skill'));
  assert.ok(html.includes('Nguồn upstream'));
  assert.ok(html.includes('href="../README.md"'));
  assert.ok(html.includes('href="../CATALOG.md"'));
  assert.ok(html.includes('https://huytran1120.github.io/vie-agentic-skills/'));
  assert.ok(html.includes('git clone https://github.com/huytran1120/vie-agentic-skills.git'));
  assert.ok(html.includes('data-skill-base=".."'));
  assert.ok(html.includes('data-theme="light"'));
  for (const setting of ['noindex', 'google-site-verification', '/_vercel/']) {
    assert.ok(!html.includes(setting), setting);
  }
  for (const id of ['pdf', 'docx', 'pptx', 'xlsx']) {
    const skill = skills.find(row => row.id === id);
    assert.equal(skill.source, 'local-original');
    assert.equal(skill.license, 'MIT');
    assert.equal(catalog.skillUrl(skill), `../skills/${id}/SKILL.md`);
    assert.equal(catalog.sourceUrl(skill), null);
  }
});

test('the Blender collection finds exactly the 94 namespaced skills and retains unrelated Blender skills', () => {
  const blender = catalog.filterSkills(skills, { group: 'blender' });
  assert.equal(blender.length, 94);
  assert.ok(blender.every(skill => skill.id.startsWith('blender-skills/')));
  assert.equal(catalog.readCatalogState('?group=blender').group, 'blender');
  assert.ok(catalog.filterSkills(skills, { query: 'blender-mcp' }).some(skill => skill.id === 'blender-mcp'));
  assert.equal(catalog.filterSkills(skills, { query: 'arjun988/blender-skills' }).length, 94);
  const html = fs.readFileSync(path.join(root, 'docs/index.html'), 'utf8');
  for (const match of html.matchAll(/data-discover="([^"]+)"/g)) {
    assert.ok(skills.some(skill => skill.id === match[1]), match[1]);
  }
});

test('published runbook URLs stay inside the repository prefix, including namespaced skills', () => {
  for (const skill of skills) {
    const url = catalog.skillUrl(skill, '.');
    const published = new URL(url, 'https://huytran1120.github.io/vie-agentic-skills/');
    assert.ok(published.pathname.startsWith('/vie-agentic-skills/skills/'));
  }
  assert.equal(catalog.skillUrl({ path: 'skills/blender-skills/blender-director' }, '.'),
    './skills/blender-skills/blender-director/SKILL.md');
  for (const base of ['../../', 'https://example.com', '/']) {
    assert.throws(() => catalog.skillUrl({ id: 'pdf' }, base));
  }
});

test('the static page ships local assets, structured data and accessible controls', () => {
  const html = fs.readFileSync(path.join(root, 'docs/index.html'), 'utf8');
  assert.ok(!html.includes('cdn.tailwindcss.com'));
  assert.ok(!html.includes('fonts.googleapis.com'));
  for (const match of html.matchAll(/(?:src|href)="\.\/([^"#]+)"/g)) {
    assert.ok(fs.existsSync(path.join(root, 'docs', match[1])), match[1]);
  }
  for (const match of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    assert.doesNotThrow(() => JSON.parse(match[1]));
  }
  assert.ok(html.includes('role="search"'));
  assert.ok(html.includes('aria-live="polite"'));
  assert.ok(html.includes('<noscript>'));
  assert.ok(html.includes('id="retry-load"'));
  assert.ok(html.includes('id="manual-copy"'));
});

function browserRuntime(fetch, window) {
  const elements = new Map();
  const errors = [];
  const warnings = [];
  const document = {
    listeners: new Map(),
    documentElement: { dataset: { theme: 'light' }, lang: 'vi' },
    querySelector: () => null,
    getElementById(id) {
      if (!elements.has(id)) {
        const classes = new Set();
        elements.set(id, {
          hidden: ['error-state', 'empty-state', 'manual-copy', 'toast'].includes(id),
          textContent: '',
          innerHTML: '',
          value: '',
          attributes: new Map(),
          listeners: new Map(),
          addEventListener(name, handler) { this.listeners.set(name, handler); },
          setAttribute(name, value) { this.attributes.set(name, value); },
          focus() { this.focused = true; },
          select() { this.selected = true; },
          scrollIntoView() {},
          querySelectorAll() { return []; },
          classList: {
            toggle(name, enabled) { if (enabled) classes.add(name); else classes.delete(name); }
          }
        });
      }
      return elements.get(id);
    },
    querySelectorAll: () => [],
    addEventListener(name, handler) { this.listeners.set(name, handler); }
  };
  vm.runInNewContext(fs.readFileSync(path.join(root, 'docs/catalog.js'), 'utf8'), {
    document, fetch, window, navigator: window?.navigator || {}, ClipboardItem: window?.ClipboardItem, Blob, VASI18n: i18n, URLSearchParams, URL,
    console: { error: (...args) => errors.push(args), warn: (...args) => warnings.push(args) },
    setTimeout, clearTimeout
  });
  return { document, elements, errors, warnings };
}

function manifestFixture(skill) {
  const revision = 'a'.repeat(40);
  return {
    schema_version: 1, available: true, repository: 'huytran1120/vie-agentic-skills',
    skill_id: skill.id, source_path: skill.path, revision,
    target_name: path.basename(skill.path),
    files: [{ path: 'SKILL.md', bytes: 3, sha256: 'b'.repeat(64), executable: false,
      url: `https://raw.githubusercontent.com/huytran1120/vie-agentic-skills/${revision}/${skill.path}/SKILL.md` }],
    receipt: { filename: '.vas-manifest.json', key: skill.id,
      entry: { mode: 'copy', target_name: path.basename(skill.path) } }
  };
}

function clickInstallPrompt(runtime, skill) {
  const button = {
    dataset: { copyAgentPrompt: skill.id }, disabled: false, attributes: new Map(),
    hasAttribute() { return false; },
    setAttribute(name, value) { this.attributes.set(name, value); }
  };
  runtime.document.listeners.get('click')({ target: { closest: selector => selector === 'button' ? button : null } });
  return button;
}

test('every skill has a short no-clone prompt using its real canonical identity and target folder', () => {
  for (const skill of skills) {
    const prompt = catalog.agentInstallPrompt(skill, 'codex', 'en');
    assert.ok(prompt.includes(`.codex/skills/${path.basename(skill.path)}/`), skill.id);
    assert.ok(prompt.includes(JSON.stringify(skill.id)), skill.id);
    assert.ok(prompt.includes(catalog.installManifestUrl(skill)), skill.id);
    assert.ok(prompt.length < 2300, skill.id);
    assert.ok(!/\{(?:id|agent|paths|manifest)\}/.test(prompt));
  }
  assert.throws(() => catalog.agentInstallPrompt(skills[0], 'invalid'));
  for (const id of ['../escape', '/absolute', 'x//y', 'x\\y', 'x\ncommand']) {
    assert.throws(() => catalog.installManifestUrl({ id }));
  }
});

test('localized chat installation always uses project copy destinations independently of CLI settings', () => {
  const skill = skills.find(skill => skill.id === 'youtube-agent-skill/yt-audit');
  for (const language of ['vi', 'en']) {
    for (const [agent] of catalog.agents) {
      const prompt = catalog.agentInstallPrompt(skill, agent, language);
      assert.ok(prompt.startsWith(language === 'vi' ? 'Hãy cài đặt skill' : 'Please install'));
      const targets = agent === 'all' ? Object.keys(catalog.targetFolders) : [agent];
      for (const target of targets) assert.ok(prompt.includes(`"${catalog.targetFolders[target]}/yt-audit/"`));
      for (const required of ['SHA-256', 'SKILL.md', 'LICENSE', 'scripts', 'templates', 'references', '.vas-manifest.json', 'receipt', 'available = true']) assert.ok(prompt.includes(required), required);
      for (const forbidden of ['--global', '--mode link', '/Projects/', '~/', 'npx ', 'python3 ']) assert.ok(!prompt.includes(forbidden));
      if (agent === 'all') assert.ok(prompt.includes('7 agent'));
    }
  }
});

test('manifest validation rejects mixed snapshots, unsafe paths, incomplete files and conflicting identities', () => {
  const skill = skills.find(skill => skill.id === 'youtube-agent-skill/yt-audit');
  assert.ok(catalog.validateInstallManifest(manifestFixture(skill), skill));
  for (const edit of [
    m => { m.skill_id = 'other'; }, m => { m.available = false; },
    m => { m.source_path = 'skills/other'; }, m => { m.target_name = '../outside'; },
    m => { m.files = []; }, m => { m.files[0].path = '../outside'; },
    m => { m.files[0].path = '/absolute'; }, m => { m.files[0].path = 'x\\y'; },
    m => { m.files[0].url = m.files[0].url.replace(m.revision, 'main'); },
    m => { m.files[0].url = m.files[0].url.replace('raw.githubusercontent.com', 'example.invalid'); },
    m => { m.files[0].sha256 = 'invalid'; }, m => { m.files[0].bytes = -1; },
    m => { m.files.push({ ...m.files[0] }); }, m => { m.receipt.key = 'other'; },
    m => { m.receipt.filename = '../.vas-manifest.json'; }
  ]) {
    const manifest = manifestFixture(skill);
    edit(manifest);
    assert.throws(() => catalog.validateInstallManifest(manifest, skill));
  }
});

test('copying an installation prompt uses the selected agent and reuses a validated file manifest', async () => {
  const skill = skills.find(skill => skill.id === 'code-review');
  const window = languageWindow('?lang=en&agent=cursor');
  let copied, requests = 0;
  window.navigator = { clipboard: { writeText: async text => { copied = text; } } };
  const runtime = browserRuntime(async url => {
    if (url === './skills.min.json') return { ok: true, json: async () => skills };
    assert.equal(url, '../_site/install-manifests/code-review.json');
    requests++;
    return { ok: true, json: async () => manifestFixture(skill) };
  }, window);
  await new Promise(setImmediate);
  const button = clickInstallPrompt(runtime, skill);
  await new Promise(setImmediate);
  assert.equal(copied, catalog.agentInstallPrompt(skill, 'cursor', 'en'));
  assert.equal(button.disabled, false);
  assert.equal(button.attributes.get('aria-busy'), 'false');
  assert.match(runtime.elements.get('toast').textContent, /Install prompt copied/);
  runtime.document.listeners.get('change')({ target: { id: 'quick-agent-select', value: 'claude' } });
  clickInstallPrompt(runtime, skill);
  await new Promise(setImmediate);
  assert.equal(copied, catalog.agentInstallPrompt(skill, 'claude', 'en'));
  assert.equal(requests, 1);
  assert.equal(runtime.errors.length, 0);
});

test('manifest failure does not copy an unsafe prompt and retry supports manual clipboard fallback', async () => {
  const skill = skills.find(skill => skill.id === 'code-review');
  const window = languageWindow('?lang=en&agent=codex');
  let fail = true;
  window.navigator = { clipboard: { writeText: async () => { throw new Error('Clipboard blocked'); } } };
  const runtime = browserRuntime(async url => {
    if (url === './skills.min.json') return { ok: true, json: async () => skills };
    if (fail) return { ok: false, status: 404 };
    return { ok: true, json: async () => manifestFixture(skill) };
  }, window);
  await new Promise(setImmediate);
  const button = clickInstallPrompt(runtime, skill);
  await new Promise(setImmediate);
  assert.equal(button.disabled, false);
  assert.equal(runtime.document.getElementById('manual-copy').hidden, true);
  assert.match(runtime.elements.get('toast').textContent, /No valid local manifest/);
  assert.equal(runtime.errors.length, 1);
  fail = false;
  clickInstallPrompt(runtime, skill);
  await new Promise(setImmediate);
  assert.equal(runtime.document.getElementById('manual-copy').hidden, false);
  const field = runtime.document.getElementById('manual-copy-text');
  assert.equal(field.value, catalog.agentInstallPrompt(skill, 'codex', 'en'));
  assert.ok(field.focused && field.selected);
});

test('WebKit clipboard writes begin in the click gesture and wait for validated manifest data', async () => {
  const skill = skills.find(skill => skill.id === 'code-review');
  const window = languageWindow('?lang=en&agent=cursor');
  let release, copied, started = false;
  window.ClipboardItem = class { constructor(data) { this.data = data; } };
  window.navigator = { clipboard: { write(items) {
    started = true;
    return items[0].data['text/plain'].then(blob => blob.text()).then(text => { copied = text; });
  } } };
  const runtime = browserRuntime(url => url === './skills.min.json'
    ? Promise.resolve({ ok: true, json: async () => skills })
    : new Promise(resolve => { release = resolve; }), window);
  await new Promise(setImmediate);
  const button = clickInstallPrompt(runtime, skill);
  assert.ok(started, 'Clipboard API must start before awaiting network, as required by WebKit');
  assert.equal(copied, undefined, 'Unverified contents must not be copied');
  release({ ok: true, json: async () => manifestFixture(skill) });
  await new Promise(setImmediate);
  assert.equal(copied, catalog.agentInstallPrompt(skill, 'cursor', 'en'));
  assert.equal(button.disabled, false);
  assert.equal(runtime.errors.length, 0);
});

test('an initial HTTP failure shows an explicit error and retry recovers', async () => {
  let requests = 0;
  const runtime = browserRuntime(async () => {
    requests++;
    return requests === 1 ? { ok: false, status: 503 } : { ok: true, json: async () => skills };
  });
  await new Promise(setImmediate);
  assert.equal(runtime.elements.get('error-state').hidden, false);
  assert.equal(runtime.elements.get('empty-state').hidden, true);
  assert.equal(runtime.elements.get('skills-results').attributes.get('aria-busy'), 'false');
  assert.equal(runtime.errors.length, 1);
  await runtime.elements.get('retry-load').listeners.get('click')();
  assert.equal(runtime.elements.get('error-state').hidden, true);
  assert.ok(runtime.elements.get('results-status').textContent.includes(skills.length.toLocaleString('vi-VN')));
});

test('search typed while loading is applied once the catalog arrives', async () => {
  let release;
  const runtime = browserRuntime(() => new Promise(resolve => { release = resolve; }));
  const input = runtime.elements.get('search-input');
  input.listeners.get('input')({ target: { value: 'mattpocock/skills' } });
  assert.equal(runtime.elements.get('empty-state').hidden, true);
  assert.equal(runtime.elements.get('skills-results').attributes.get('aria-busy'), 'true');
  release({ ok: true, json: async () => skills });
  await new Promise(setImmediate);
  assert.ok(runtime.elements.get('results-status').textContent.includes('35'));
  assert.equal(runtime.elements.get('loading-state').hidden, true);
});

test('malformed catalog data never turns into a success-shaped empty state', async () => {
  for (const data of [{ invalid: true }, [], [{ id: 'bad', category: 'test', tags: 'not-an-array' }]]) {
    const runtime = browserRuntime(async () => ({ ok: true, json: async () => data }));
    await new Promise(setImmediate);
    assert.equal(runtime.elements.get('error-state').hidden, false);
    assert.equal(runtime.elements.get('empty-state').hidden, true);
    assert.equal(runtime.errors.length, 1);
  }
});

test('source filters combine as a union and intersect with search and categories', () => {
  assert.equal(catalog.filterSkills(skills, { sources: ['mattpocock'] }).length, 35);
  assert.equal(catalog.filterSkills(skills, { sources: ['addy'] }).length, 25);
  assert.equal(catalog.filterSkills(skills, { sources: ['blender'] }).length, 94);
  assert.equal(catalog.filterSkills(skills, { sources: ['youtube'] }).length, 11);
  assert.equal(catalog.filterSkills(skills, { sources: ['hallmark'] }).length, 1);
  assert.equal(catalog.filterSkills(skills, { sources: ['typesafe'] }).length, 1);
  assert.equal(catalog.filterSkills(skills, { sources: ['android'] }).length, 35);
  assert.equal(catalog.filterSkills(skills, { sources: ['gamedev'] }).length, 78);
  assert.equal(catalog.filterSkills(skills, { sources: ['typesafe', 'hallmark'] }).length, 2);
  assert.equal(catalog.filterSkills(skills, { sources: ['hallmark', 'youtube'] }).length, 12);
  assert.equal(catalog.filterSkills(skills, { sources: ['youtube', 'blender'] }).length, 105);
  assert.equal(catalog.filterSkills(skills, { sources: ['mattpocock', 'blender'] }).length, 129);
  const filtered = catalog.filterSkills(skills, { sources: ['mattpocock'], query: 'review' });
  assert.ok(filtered.length > 0);
  assert.ok(filtered.every(skill => skill.source_repo === 'mattpocock/skills'));
  assert.equal(catalog.filterSkills(skills, { sources: ['blender'], category: 'security' }).length, 0);
});

test('YouTube collection retains its pinned source, standalone install paths and bilingual links', () => {
  const youtube = catalog.filterSkills(skills, { sources: ['youtube'] });
  assert.equal(youtube.length, 11);
  assert.equal(catalog.filterSkills(skills, { query: 'youtube-agent-skill' }).length, 11);
  assert.equal(skills.length, 3171);
  for (const skill of youtube) {
    assert.ok(skill.id.startsWith('youtube-agent-skill/'));
    assert.equal(skill.source_repo, 'Jakeschincariol/youtube-agent-skill');
    assert.ok(catalog.sourceUrl(skill).includes('/a2feb2104981a375ffd4f87ee04f4f5344ac43c6/'));
    const plan = catalog.installationPlan(skill.id, 'claude', { mode: 'copy' });
    assert.deepEqual(plan.paths, [`.claude/skills/${skill.name}/SKILL.md`]);
    assert.ok(plan.install.includes(`install ${skill.id} --target claude --mode copy`));
  }
  for (const language of ['vi', 'en']) {
    const state = catalog.readCatalogState(catalog.catalogParams({ language, sources: ['youtube'], selected: youtube[0].id }));
    assert.equal(state.language, language);
    assert.deepEqual(state.sources, ['youtube']);
    assert.equal(state.selected, youtube[0].id);
    assert.ok(i18n.translate('collections.youtube', language).startsWith('11 '));
    assert.ok(i18n.translate('stats.runbooks', language).includes(language === 'vi' ? '3.171' : '3,171'));
  }
  assert.equal(catalog.filterSkills(skills, { sources: ['youtube'], category: 'security' }).length, 0);
  const html = fs.readFileSync(path.join(root, 'docs/index.html'), 'utf8');
  assert.ok(html.includes('name="source" value="youtube"'));
  assert.ok(html.includes('id="youtube-collection"'));
});

test('Hallmark retains its pinned source and complete no-clone prompts for every agent and language', () => {
  const [skill] = catalog.filterSkills(skills, { sources: ['hallmark'] });
  assert.equal(skill.id, 'hallmark');
  assert.equal(skill.source_repo, 'Nutlope/hallmark');
  assert.equal(skill.license, 'MIT');
  assert.deepEqual(catalog.filterSkills(skills, { query: 'Nutlope' }).map(skill => skill.id), ['hallmark']);
  assert.ok(catalog.sourceUrl(skill).includes('/8f6969f8922caabde9de1784959eae11ddf68073/'));
  for (const language of ['vi', 'en']) {
    for (const [agent] of catalog.agents) {
      const state = catalog.readCatalogState(catalog.catalogParams({
        language, sources: ['hallmark'], selected: skill.id, target: agent
      }));
      assert.equal(state.language, language);
      assert.equal(state.target, agent);
      assert.equal(state.selected, 'hallmark');
      assert.deepEqual(state.sources, ['hallmark']);
      const prompt = catalog.agentInstallPrompt(skill, agent, language);
      assert.ok(prompt.startsWith(language === 'vi' ? 'Hãy cài đặt skill' : 'Please install'));
      assert.ok(prompt.includes('/install-manifests/hallmark.json'));
      assert.ok(prompt.includes('SHA-256') && prompt.includes('.vas-manifest.json'));
      assert.ok(!prompt.includes('8f6969f8922caabde9de1784959eae11ddf68073'));
      const targets = agent === 'all' ? Object.keys(catalog.targetFolders) : [agent];
      for (const target of targets) {
        assert.ok(prompt.includes(`"${catalog.targetFolders[target]}/hallmark/"`));
        const plan = catalog.installationPlan('hallmark', target, { mode: 'copy' });
        assert.deepEqual(plan.paths, [`${catalog.targetFolders[target]}/hallmark/SKILL.md`]);
      }
    }
  }
  const html = fs.readFileSync(path.join(root, 'docs/index.html'), 'utf8');
  assert.ok(html.includes('name="source" value="hallmark"'));
  assert.ok(html.includes('data-source-count="hallmark">1<'));
  assert.ok(html.includes('data-discover="hallmark"'));
});

test('TypeSafe source, search and localized install plans preserve its canonical identity', () => {
  const [skill] = catalog.filterSkills(skills, { sources: ['typesafe'] });
  assert.equal(skill.id, 'typesafe-ai');
  assert.equal(skill.license, 'MIT');
  assert.equal(skill.source_repo, 'typesafe-ai/skills');
  assert.ok(catalog.filterSkills(skills, { query: 'Jev' }).some(skill => skill.id === 'typesafe-ai'));
  assert.deepEqual(catalog.filterSkills(skills, { query: 'Jev', sources: ['typesafe'] }).map(skill => skill.id), ['typesafe-ai']);
  assert.deepEqual(catalog.filterSkills(skills, { sources: ['typesafe'], group: 'data-ai' }), [skill]);
  assert.equal(catalog.filterSkills(skills, { sources: ['typesafe'], category: 'security' }).length, 0);
  assert.ok(catalog.sourceUrl(skill).includes('/302eea662c54bca6730873fe245bec1d69ebc23d/'));
  for (const language of ['vi', 'en']) {
    assert.ok(i18n.translate('collections.typesafe', language).startsWith('1 skill'));
    for (const [agent] of catalog.agents) {
      const state = catalog.readCatalogState(catalog.catalogParams({
        language, sources: ['typesafe'], selected: skill.id, target: agent
      }));
      assert.equal(state.language, language);
      assert.equal(state.target, agent);
      assert.equal(state.selected, 'typesafe-ai');
      assert.deepEqual(state.sources, ['typesafe']);
      const prompt = catalog.agentInstallPrompt(skill, agent, language);
      assert.ok(prompt.startsWith(language === 'vi' ? 'Hãy cài đặt skill' : 'Please install'));
      for (const required of ['/install-manifests/typesafe-ai.json', 'SHA-256', 'LICENSE', '.vas-manifest.json']) assert.ok(prompt.includes(required));
      assert.ok(!prompt.includes('302eea662c54bca6730873fe245bec1d69ebc23d'));
      const targets = agent === 'all' ? Object.keys(catalog.targetFolders) : [agent];
      for (const target of targets) {
        assert.ok(prompt.includes(`"${catalog.targetFolders[target]}/typesafe-ai/"`));
        for (const mode of ['link', 'copy']) {
          const plan = catalog.installationPlan(skill.id, target, { mode });
          assert.deepEqual(plan.paths, [`${catalog.targetFolders[target]}/typesafe-ai/SKILL.md`]);
          assert.ok(plan.install.includes(`--target ${target} --mode ${mode}`));
          assert.ok(plan.status.includes(`--target ${target}`));
          assert.ok(plan.uninstall.includes(`uninstall typesafe-ai --target ${target}`));
        }
      }
    }
  }
  const html = fs.readFileSync(path.join(root, 'docs/index.html'), 'utf8');
  assert.ok(html.includes('name="source" value="typesafe"'));
  assert.ok(html.includes('data-source-count="typesafe">1<'));
  assert.ok(html.includes('id="typesafe-collection"'));
});

test('TypeSafe invalid snapshots never copy and clipboard rejection provides the localized manual prompt', async () => {
  const skill = skills.find(skill => skill.id === 'typesafe-ai');
  for (const language of ['vi', 'en']) {
    const window = languageWindow(`?lang=${language}&agent=copilot`);
    window.navigator = { clipboard: { writeText: async () => { throw new Error('Clipboard blocked'); } } };
    let available = false;
    const runtime = browserRuntime(async url => {
      if (url === './skills.min.json') return { ok: true, json: async () => skills };
      assert.equal(url, '../_site/install-manifests/typesafe-ai.json');
      return { ok: true, json: async () => ({ ...manifestFixture(skill), available }) };
    }, window);
    await new Promise(setImmediate);
    clickInstallPrompt(runtime, skill);
    await new Promise(setImmediate);
    assert.equal(runtime.document.getElementById('manual-copy').hidden, true);
    assert.equal(runtime.errors.length, 1);
    available = true;
    const button = clickInstallPrompt(runtime, skill);
    await new Promise(setImmediate);
    assert.equal(button.disabled, false);
    assert.equal(runtime.document.getElementById('manual-copy').hidden, false);
    const field = runtime.document.getElementById('manual-copy-text');
    assert.equal(field.value, catalog.agentInstallPrompt(skill, 'copilot', language));
    assert.ok(field.focused && field.selected);
  }
});

test('all 35 Android skills retain exact source filtering, Apache notices and every localized agent prompt', () => {
  const android = catalog.filterSkills(skills, { sources: ['android'] });
  assert.equal(android.length, 35);
  assert.ok(!android.some(skill => skill.id === 'android-cli'));
  assert.deepEqual(catalog.filterSkills(skills, { query: 'android/skills' }), android);
  assert.equal(catalog.filterSkills(skills, { sources: ['android'], category: 'mobile' }).length, 35);
  assert.equal(catalog.filterSkills(skills, { sources: ['android'], category: 'security' }).length, 0);
  for (const skill of android) {
    assert.equal(skill.source_repo, 'android/skills');
    assert.equal(skill.license, 'Apache-2.0');
    assert.equal(skill.id, path.basename(skill.path));
    assert.ok(catalog.sourceUrl(skill).includes('/6daa53ef27fa2aa87827d183a85c06cedceca833/'));
    for (const language of ['vi', 'en']) {
      assert.ok(i18n.translate('collections.android', language).startsWith('35 '));
      for (const [agent] of catalog.agents) {
        const state = catalog.readCatalogState(catalog.catalogParams({
          language, sources: ['android'], selected: skill.id, target: agent
        }));
        assert.equal(state.language, language);
        assert.equal(state.target, agent);
        assert.equal(state.selected, skill.id);
        assert.deepEqual(state.sources, ['android']);
        const prompt = catalog.agentInstallPrompt(skill, agent, language);
        assert.ok(prompt.startsWith(language === 'vi' ? 'Hãy cài đặt skill' : 'Please install'));
        for (const required of [`/install-manifests/${skill.id}.json`, 'SHA-256', 'LICENSE', '.vas-manifest.json']) assert.ok(prompt.includes(required));
        assert.ok(!prompt.includes('6daa53ef27fa2aa87827d183a85c06cedceca833'));
        const targets = agent === 'all' ? Object.keys(catalog.targetFolders) : [agent];
        for (const target of targets) {
          assert.ok(prompt.includes(`"${catalog.targetFolders[target]}/${skill.id}/"`));
          for (const mode of ['link', 'copy']) {
            const plan = catalog.installationPlan(skill.id, target, { mode });
            assert.deepEqual(plan.paths, [`${catalog.targetFolders[target]}/${skill.id}/SKILL.md`]);
            assert.ok(plan.install.includes(`--target ${target} --mode ${mode}`));
            assert.ok(plan.status.includes(`--target ${target}`));
            assert.ok(plan.uninstall.includes(`uninstall ${skill.id} --target ${target}`));
          }
        }
      }
    }
  }
  const html = fs.readFileSync(path.join(root, 'docs/index.html'), 'utf8');
  assert.ok(html.includes('name="source" value="android"'));
  assert.ok(html.includes('data-source-count="android">35<'));
  assert.ok(html.includes('id="android-collection"'));
});

test('Android snapshots must be available before copying and clipboard failure retains safe manual recovery', async () => {
  const skill = skills.find(skill => skill.id === 'play-policy-insights');
  for (const language of ['vi', 'en']) {
    const window = languageWindow(`?lang=${language}&agent=cursor`);
    window.navigator = { clipboard: { writeText: async () => { throw new Error('Clipboard blocked'); } } };
    let available = false;
    const runtime = browserRuntime(async url => {
      if (url === './skills.min.json') return { ok: true, json: async () => skills };
      assert.equal(url, '../_site/install-manifests/play-policy-insights.json');
      return { ok: true, json: async () => ({ ...manifestFixture(skill), available }) };
    }, window);
    await new Promise(setImmediate);
    clickInstallPrompt(runtime, skill);
    await new Promise(setImmediate);
    assert.equal(runtime.document.getElementById('manual-copy').hidden, true);
    assert.equal(runtime.errors.length, 1);
    available = true;
    const button = clickInstallPrompt(runtime, skill);
    await new Promise(setImmediate);
    assert.equal(button.disabled, false);
    assert.equal(runtime.document.getElementById('manual-copy').hidden, false);
    assert.equal(runtime.document.getElementById('manual-copy-text').value,
      catalog.agentInstallPrompt(skill, 'cursor', language));
  }
});

test('all GameDev workflows retain source identity, distinct names and every bilingual agent destination', () => {
  const gamedev = catalog.filterSkills(skills, { sources: ['gamedev'] });
  assert.equal(gamedev.length, 78);
  assert.deepEqual(catalog.filterSkills(skills, { query: 'gamedev-skills/awesome-gamedev-agent-skills' }), gamedev);
  assert.equal(catalog.filterSkills(skills, { sources: ['gamedev'], category: 'game-development' }).length, 78);
  assert.equal(catalog.filterSkills(skills, { sources: ['gamedev'], category: 'development' }).length, 0);
  for (const id of ['router', 'ebitengine-game', 'gamedev-performance-optimization', 'gamedev-godot-export']) assert.ok(gamedev.some(skill => skill.id === id));
  assert.ok(!gamedev.some(skill => skill.id === 'performance-optimization' || skill.id === 'blender-skills/godot-export'));
  for (const skill of gamedev) {
    assert.equal(skill.license, 'Apache-2.0');
    assert.equal(skill.id, path.basename(skill.path));
    assert.ok(catalog.sourceUrl(skill).includes('/19d93f97c9c1ea0f8b306e77aa81e0d3e352d3e9/'));
    for (const language of ['vi', 'en']) {
      assert.ok(i18n.translate('collections.gamedev', language).startsWith('78 '));
      for (const [agent] of catalog.agents) {
        const state = catalog.readCatalogState(catalog.catalogParams({ language, sources: ['gamedev'], selected: skill.id, target: agent }));
        assert.equal(state.language, language);
        assert.equal(state.selected, skill.id);
        assert.equal(state.target, agent);
        assert.deepEqual(state.sources, ['gamedev']);
        const prompt = catalog.agentInstallPrompt(skill, agent, language);
        assert.ok(prompt.startsWith(language === 'vi' ? 'Hãy cài đặt skill' : 'Please install'));
        for (const required of [`/install-manifests/${skill.id}.json`, 'SHA-256', 'LICENSE', '.vas-manifest.json']) assert.ok(prompt.includes(required));
        assert.ok(!prompt.includes('19d93f97c9c1ea0f8b306e77aa81e0d3e352d3e9'));
        for (const target of agent === 'all' ? Object.keys(catalog.targetFolders) : [agent]) {
          assert.ok(prompt.includes(`"${catalog.targetFolders[target]}/${skill.id}/"`));
          for (const mode of ['link', 'copy']) {
            const plan = catalog.installationPlan(skill.id, target, { mode });
            assert.deepEqual(plan.paths, [`${catalog.targetFolders[target]}/${skill.id}/SKILL.md`]);
            assert.ok(plan.install.includes(`--target ${target} --mode ${mode}`));
            assert.ok(plan.uninstall.includes(`uninstall ${skill.id} --target ${target}`));
          }
        }
      }
    }
  }
  const html = fs.readFileSync(path.join(root, 'docs/index.html'), 'utf8');
  for (const required of ['name="source" value="gamedev"', 'data-source-count="gamedev">78<', 'id="gamedev-collection"']) assert.ok(html.includes(required));
});

test('GameDev refuses unpublished manifests and recovers from clipboard errors in both languages', async () => {
  const skill = skills.find(skill => skill.id === 'router');
  for (const language of ['vi', 'en']) {
    const window = languageWindow(`?lang=${language}&agent=copilot`);
    window.navigator = { clipboard: { writeText: async () => { throw new Error('Clipboard blocked'); } } };
    let available = false;
    const runtime = browserRuntime(async url => {
      if (url === './skills.min.json') return { ok: true, json: async () => skills };
      assert.equal(url, '../_site/install-manifests/router.json');
      return { ok: true, json: async () => ({ ...manifestFixture(skill), available }) };
    }, window);
    await new Promise(setImmediate);
    clickInstallPrompt(runtime, skill);
    await new Promise(setImmediate);
    assert.equal(runtime.document.getElementById('manual-copy').hidden, true);
    assert.equal(runtime.errors.length, 1);
    available = true;
    clickInstallPrompt(runtime, skill);
    await new Promise(setImmediate);
    assert.equal(runtime.document.getElementById('manual-copy').hidden, false);
    assert.equal(runtime.document.getElementById('manual-copy-text').value, catalog.agentInstallPrompt(skill, 'copilot', language));
  }
});

test('shared links retain selected sources and reject unknown source keys', () => {
  const params = catalog.catalogParams({ sources: ['blender', 'mattpocock'], projectPath: '/private/project' });
  assert.deepEqual(catalog.readCatalogState(params).sources, ['blender', 'mattpocock']);
  assert.deepEqual(catalog.readCatalogState('?sources=blender,unknown,constructor,toString,blender').sources, ['blender']);
  assert.ok(!params.includes('private'));
});

test('runbook rendering preserves code verbatim and strips YAML frontmatter', () => {
  const md = '---\nname: example\ndescription: Hidden metadata\n---\n# Runbook\n\n```sh\n./vas install code-review --target codex\necho "<script>"\n```';
  const result = catalog.renderMarkdown(md);
  assert.ok(!result.html.includes('Hidden metadata'));
  assert.ok(result.html.includes('./vas install code-review --target codex'));
  assert.ok(result.html.includes('&lt;script&gt;'));
  assert.equal(result.headings[0].text, 'Runbook');
});

test('untrusted Markdown cannot inject HTML or executable link protocols', () => {
  const result = catalog.renderMarkdown('<img src=x onerror=alert(1)>\n\n[Bad](javascript:alert) [Data](data:text/html,test) [File](file:///etc/passwd)\n\n[Guide](references/guide.md)', 'https://example.com/skills/example/SKILL.md');
  assert.ok(!result.html.includes('<img'));
  assert.ok(!result.html.includes('href="javascript:'));
  assert.ok(!result.html.includes('href="data:'));
  assert.ok(!result.html.includes('href="file:'));
  assert.ok(result.html.includes('href="https://example.com/skills/example/references/guide.md"'));
});

test('runbook headings have stable unique anchors and tables remain structured', () => {
  const result = catalog.renderMarkdown('## Cài đặt\n\nFirst\n\n## Cài đặt\n\n| Tool | Required |\n| --- | --- |\n| Python | Yes |');
  assert.equal(new Set(result.headings.map(h => h.id)).size, 2);
  assert.ok(result.html.includes('<table>'));
  assert.ok(result.html.includes('<th>Tool</th>'));
  assert.ok(result.html.includes('<td>Python</td>'));
});

test('the PDF runbook retains all four extraction steps and their wrapped prerequisites', () => {
  const source = fs.readFileSync(path.join(root, 'skills/pdf/SKILL.md'), 'utf8');
  const extraction = source.split('## Extract selectable text')[1].split('```')[0];
  const result = catalog.renderMarkdown(extraction);
  const lists = [...result.html.matchAll(/<ol(?: [^>]*)?>[\s\S]*?<\/ol>/g)];
  assert.equal(lists.length, 1, 'Wrapped step text must not restart the list');
  assert.equal([...lists[0][0].matchAll(/<li>/g)].length, 4);
  assert.match(lists[0][0], /<li>Read the page count\.[\s\S]*workflow has been agreed; do not attempt password recovery\.<\/li>/);
  assert.match(lists[0][0], /<li>If pages contain no selectable text,[\s\S]*do not present empty extraction as successful document understanding\.<\/li>/);
});

test('ordered lists preserve their start and nested list/code content stays in its parent item', () => {
  const markdown = '3. Parent step\n   wrapped prerequisite\n   - Child task\n     1. Deep task\n     2. Another deep task\n   - Second child\n4. Next step\n\nOutside paragraph.\n\n7. Resumed step\n   ```sh\n   echo "<script>"\n     indented command\n   ```';
  const result = catalog.renderMarkdown(markdown);
  assert.match(result.html, /^<ol start="3"><li><p>Parent step wrapped prerequisite<\/p>\n<ul><li><p>Child task<\/p>\n<ol><li>Deep task<\/li><li>Another deep task<\/li><\/ol><\/li><li>Second child<\/li><\/ul><\/li><li>Next step<\/li><\/ol>/);
  assert.match(result.html, /<p>Outside paragraph\.<\/p>\n<ol start="7"><li>/);
  assert.ok(result.html.includes('echo &quot;&lt;script&gt;&quot;\n  indented command'));
  assert.ok(!result.html.includes('<script>'));
});

test('the senior-frontend table of contents navigates rendered headings in the same reader', () => {
  const source = fs.readFileSync(path.join(root, 'skills/senior-frontend/SKILL.md'), 'utf8');
  const base = 'https://huytran1120.github.io/vie-agentic-skills/skills/senior-frontend/SKILL.md';
  const result = catalog.renderMarkdown(source, base);
  assert.ok(result.headings.some(heading => heading.id === 'runbook-project-scaffolding'));
  assert.ok(result.html.includes('<a href="#runbook-project-scaffolding">Project Scaffolding</a>'));
  assert.ok(!result.html.includes(`${base}#project-scaffolding`));
  assert.ok(!result.html.includes('data-runbook-fragment='));
  const aliases = catalog.renderMarkdown('[First](#setup) [Second](#setup-1) [Unicode](#c%C3%A0i-%C4%91%E1%BA%B7t)\n\n## Setup\n\n## Setup\n\n## Cài đặt');
  for (const href of ['#runbook-setup', '#runbook-setup-2', '#runbook-cai-dat']) assert.ok(aliases.html.includes(`href="${href}"`), href);
  const unsafe = catalog.renderMarkdown('[Local](#%22onfocus=alert) [Unsafe](javascript:alert)');
  assert.ok(!unsafe.html.includes(' onfocus='));
  assert.ok(!unsafe.html.includes('href="javascript:'));
});

test('every interface message and static translation binding supports both languages', () => {
  for (const [key, pair] of Object.entries(i18n.messages)) {
    assert.equal(pair.length, 2, key);
    const values = Object.fromEntries([...pair.join('').matchAll(/\{(\w+)\}/g)].map(match => [match[1], 'example']));
    for (const language of ['vi', 'en']) {
      assert.ok(i18n.translate(key, language, values).trim(), `${language}: ${key}`);
    }
  }
  const html = fs.readFileSync(path.join(root, 'docs/index.html'), 'utf8');
  for (const [, key] of html.matchAll(/data-i18n(?:-(?:aria-label|title|placeholder|content|copy-message))?="([^"]+)"/g)) {
    assert.ok(Object.hasOwn(i18n.messages, key), key);
    assert.doesNotThrow(() => i18n.translate(key, 'en'), key);
  }
  assert.ok(html.indexOf('src="./i18n.js"') < html.indexOf('src="./catalog.js"'));
  assert.ok(html.includes('id="language-toggle"'));
  assert.throws(() => i18n.translate('missing'), /Missing translation/);
  assert.throws(() => i18n.translate('library', 'invalid'), /Unsupported interface language/);
  assert.throws(() => i18n.translate('hero.agent', 'en'), /Missing translation value/);
});

test('explicit language links override preferences and only known languages are accepted', () => {
  assert.equal(i18n.resolveLanguage('', null), 'vi');
  assert.equal(i18n.resolveLanguage('', 'en'), 'en');
  assert.equal(i18n.resolveLanguage('?lang=vi', 'en'), 'vi');
  assert.equal(i18n.resolveLanguage('?lang=en', 'vi'), 'en');
  for (const invalid of ['constructor', 'toString', 'fr', '<script>']) {
    assert.equal(i18n.resolveLanguage(`?lang=${encodeURIComponent(invalid)}`), 'vi');
  }
  const state = { language: 'en', selected: 'code-review', target: 'codex', query: 'docker', sources: ['blender'], view: 'grid', projectPath: '/private/project', scope: 'project', mode: 'copy' };
  const params = catalog.catalogParams(state);
  assert.equal(catalog.readCatalogState(params).language, 'en');
  assert.equal(catalog.readCatalogState('', 'en').language, 'en');
  assert.equal(catalog.readCatalogState('?lang=vi', 'en').language, 'vi');
  for (const forbidden of ['private', 'projectPath', 'scope', 'mode']) assert.ok(!params.includes(forbidden));
});

test('language changes prompts and validation, never executable commands or installed paths', () => {
  for (const [target] of catalog.agents) {
    for (const mode of ['link', 'copy']) {
      for (const scope of ['repository', 'project', ...(target === 'all' ? [] : ['global'])]) {
        const options = { scope, projectPath: '/Projects/my app', mode };
        const vi = catalog.installationPlan('blender-skills/blender-director', target, options);
        const en = catalog.installationPlan('blender-skills/blender-director', target, { ...options, language: 'en' });
        for (const key of ['install', 'status', 'uninstall', 'paths']) assert.deepEqual(en[key], vi[key]);
        assert.ok(en.prompt.startsWith('Read the runbook'));
        assert.ok(vi.prompt.startsWith('Hãy đọc runbook'));
        assert.ok(en.paths.every(path => en.prompt.includes(JSON.stringify(path))));
      }
    }
  }
  assert.throws(() => catalog.installationPlan('code-review', 'codex', { scope: 'project', language: 'en' }), /Enter an absolute project path/);
  assert.throws(() => catalog.installationPlan('code-review', 'all', { scope: 'global', language: 'en' }), /Choose one agent/);
});

test('localized Markdown controls preserve source text, code and safe links', () => {
  const md = '# Hướng dẫn\n\nGiữ nguyên nội dung.\n\n```sh\necho \"Tiếng Việt & English\"\n```\n\n[Guide](references/guide.md)';
  const vi = catalog.renderMarkdown(md);
  const en = catalog.renderMarkdown(md, 'https://example.invalid/skills/', 'en');
  assert.deepEqual(en.headings, vi.headings);
  assert.equal(en.html.replace('Copy code', 'Sao chép mã'), vi.html);
});

function languageWindow(search = '', saved = null, blocked = false) {
  const location = new URL(`https://example.com/docs/${search}`);
  const storage = new Map(saved ? [['vas-language', saved]] : []);
  const listeners = new Map();
  return {
    location, storage, listeners,
    scrollY: 0,
    scrollTo({ top }) { this.scrollY = top; },
    localStorage: {
      getItem(key) { if (blocked) throw new Error('Storage blocked'); return storage.get(key) || null; },
      setItem(key, value) { if (blocked) throw new Error('Storage blocked'); storage.set(key, value); }
    },
    history: {
      state: null,
      replaceState(state, _title, url) { this.state = state; location.href = new URL(url, location).href; },
      pushState(state, _title, url) { this.state = state; location.href = new URL(url, location).href; }
    },
    addEventListener(name, handler) { listeners.set(name, handler); }
  };
}

test('Back restores the loaded result pages and list scroll without sharing installation settings', async () => {
  const window = languageWindow('?lang=en&agent=codex');
  window.scrollY = 1800;
  window.scrollTo = ({ top }) => { window.scrollY = top; };
  const runtime = browserRuntime(async url => url === './skills.min.json'
    ? { ok: true, json: async () => skills } : { ok: true, text: async () => '# Runbook' }, window);
  await new Promise(setImmediate);
  const result = catalog.filterSkills(skills)[8];
  assert.ok(!runtime.elements.get('skills-results').innerHTML.includes(`data-skill="${result.id}"`));
  runtime.elements.get('load-more').listeners.get('click')();
  assert.equal(runtime.elements.get('pagination-status').textContent, `Showing 12 / ${skills.length.toLocaleString('en-US')} runbooks`);
  runtime.document.listeners.get('input')({ target: { id: 'project-path', value: '/private/project' } });
  let previous;
  const push = window.history.pushState.bind(window.history);
  window.history.pushState = (state, title, url) => {
    previous = { state: window.history.state, href: window.location.href };
    push(state, title, url);
  };
  const button = { dataset: { openSkill: result.id }, disabled: false, hasAttribute: () => false };
  runtime.document.listeners.get('click')({ target: { closest: selector => selector === 'button' ? button : null } });
  assert.equal(new URL(window.location.href).searchParams.get('skill'), result.id);
  assert.ok(!JSON.stringify(previous.state).includes('private'));
  assert.ok(!previous.href.includes('page=') && !previous.href.includes('scroll='));
  window.scrollY = 0;
  window.location.href = previous.href;
  window.listeners.get('popstate')({ state: previous.state });
  assert.equal(runtime.elements.get('pagination-status').textContent, `Showing 12 / ${skills.length.toLocaleString('en-US')} runbooks`);
  assert.ok(runtime.elements.get('skills-results').innerHTML.includes(`data-skill="${result.id}"`));
  assert.equal(window.scrollY, 1800);
  assert.equal(runtime.elements.get('library-view').hidden, false);
});

test('runbook fragment history leaves native anchor scrolling and the current reader intact', async () => {
  const window = languageWindow('?lang=en&skill=code-review');
  const runtime = browserRuntime(async url => url === './skills.min.json'
    ? { ok: true, json: async () => skills } : { ok: true, text: async () => '# Runbook' }, window);
  await new Promise(setImmediate);
  let scrolled = false;
  runtime.elements.get('detail-view').scrollIntoView = () => { scrolled = true; };
  const content = runtime.elements.get('skill-detail').innerHTML;
  window.location.hash = '#runbook-runbook';
  window.listeners.get('popstate')({ state: null });
  assert.equal(scrolled, false, 'A hash history entry must not jump back to the detail header');
  assert.equal(runtime.elements.get('skill-detail').innerHTML, content);
});

test('language switching works during loading and preserves query, agent and privacy', async () => {
  let release;
  const window = languageWindow('?q=docker&agent=codex&sources=blender');
  const runtime = browserRuntime(() => new Promise(resolve => { release = resolve; }), window);
  runtime.elements.get('language-toggle').listeners.get('click')();
  assert.equal(runtime.document.documentElement.lang, 'en');
  assert.equal(window.storage.get('vas-language'), 'en');
  assert.deepEqual([...window.storage.keys()], ['vas-language']);
  assert.equal(window.location.search, '?lang=en&q=docker&agent=codex&sources=blender');
  release({ ok: true, json: async () => skills });
  await new Promise(setImmediate);
  assert.ok(runtime.elements.get('results-status').textContent.endsWith(' for “docker”'));
  assert.equal(runtime.elements.get('search-input').value, 'docker');
  assert.equal(runtime.elements.get('language-toggle').textContent, 'VI');
});

test('English loading failures remain actionable and unavailable storage is reported', async () => {
  const window = languageWindow('?lang=en', 'vi', true);
  const runtime = browserRuntime(async () => ({ ok: false, status: 503 }), window);
  await new Promise(setImmediate);
  assert.equal(runtime.elements.get('error-state').hidden, false);
  assert.equal(runtime.elements.get('results-status').textContent, 'Unable to load the catalog. Please try again.');
  assert.equal(runtime.warnings.length, 1);
  runtime.elements.get('language-toggle').listeners.get('click')();
  assert.equal(runtime.document.documentElement.lang, 'vi');
  assert.ok(window.location.search.includes('lang=vi'));
  assert.equal(runtime.elements.get('toast').hidden, false);
  assert.equal(runtime.warnings.length, 2);
});

test('language changes retain theme state and history still reports missing skills', async () => {
  const window = languageWindow('?lang=en');
  const runtime = browserRuntime(async () => ({ ok: true, json: async () => skills }), window);
  await new Promise(setImmediate);
  runtime.elements.get('theme-toggle').listeners.get('click')({});
  assert.equal(runtime.document.documentElement.dataset.theme, 'dark');
  assert.equal(runtime.elements.get('theme-toggle').attributes.get('aria-label'), 'Switch to light theme');
  runtime.elements.get('language-toggle').listeners.get('click')();
  assert.equal(runtime.document.documentElement.dataset.theme, 'dark');
  assert.equal(runtime.elements.get('theme-toggle').attributes.get('aria-label'), 'Bật giao diện sáng');
  window.location.search = '?lang=en&skill=missing-skill';
  window.listeners.get('popstate')();
  assert.equal(runtime.elements.get('toast').hidden, false);
  assert.equal(runtime.elements.get('toast').textContent, 'This skill is no longer in the catalog. Search for another one below.');
});
