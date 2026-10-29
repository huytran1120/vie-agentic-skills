const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const catalog = require('../docs/catalog.js');
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

function browserRuntime(fetch) {
  const elements = new Map();
  const errors = [];
  const document = {
    getElementById(id) {
      if (!elements.has(id)) {
        const classes = new Set();
        elements.set(id, {
          hidden: ['error-state', 'empty-state'].includes(id),
          textContent: '',
          innerHTML: '',
          value: '',
          attributes: new Map(),
          listeners: new Map(),
          addEventListener(name, handler) { this.listeners.set(name, handler); },
          setAttribute(name, value) { this.attributes.set(name, value); },
          classList: {
            toggle(name, enabled) { if (enabled) classes.add(name); else classes.delete(name); }
          }
        });
      }
      return elements.get(id);
    },
    querySelectorAll: () => [],
    addEventListener() {}
  };
  vm.runInNewContext(fs.readFileSync(path.join(root, 'docs/catalog.js'), 'utf8'), {
    document, fetch, console: { error: (...args) => errors.push(args) },
    setTimeout, clearTimeout
  });
  return { document, elements, errors };
}

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
  assert.ok(runtime.elements.get('results-status').textContent.includes(skills.length.toLocaleString('en-US')));
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
  assert.equal(catalog.filterSkills(skills, { sources: ['mattpocock', 'blender'] }).length, 129);
  const filtered = catalog.filterSkills(skills, { sources: ['mattpocock'], query: 'review' });
  assert.ok(filtered.length > 0);
  assert.ok(filtered.every(skill => skill.source_repo === 'mattpocock/skills'));
  assert.equal(catalog.filterSkills(skills, { sources: ['blender'], category: 'security' }).length, 0);
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
