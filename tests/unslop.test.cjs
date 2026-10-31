const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const catalog = require('../docs/catalog.js');
const i18n = require('../docs/i18n.js');
const root = path.resolve(__dirname, '..');
const skills = JSON.parse(fs.readFileSync(path.join(root, 'skills_index.json'), 'utf8'));
const skill = skills.find(row => row.id === 'heydamir-unslop');

test('UI Unslop has exact source identity and does not replace the prose workflow', () => {
  assert.deepEqual(catalog.filterSkills(skills, { sources: ['heydamir'] }), [skill]);
  assert.deepEqual(catalog.filterSkills(skills, { query: 'heydamir/unslop' }), [skill]);
  assert.deepEqual(catalog.filterSkills(skills, { sources: ['heydamir'], category: 'front-end' }), [skill]);
  assert.deepEqual(catalog.filterSkills(skills, { sources: ['heydamir'], category: 'writing' }), []);
  assert.equal(skill.license, 'CC-BY-4.0');
  assert.equal(skill.author, 'Damir Sokolovsky');
  assert.ok(catalog.sourceUrl(skill).includes('/4652254daff586ff4739849395a127b56f7f8cc7/'));
  assert.equal(skills.find(row => row.id === 'unslop').source_repo, 'MohamedAbdallah-14/unslop');
  const html = fs.readFileSync(path.join(root, 'docs/index.html'), 'utf8');
  for (const required of ['name="source" value="heydamir"', 'data-source-count="heydamir">1<', 'id="unslop-collection"']) assert.ok(html.includes(required));
});

test('every bilingual agent prompt and CLI plan uses the unique UI Unslop folder', () => {
  for (const language of ['vi', 'en']) {
    assert.ok(i18n.translate('collections.unslop', language).startsWith('1 skill'));
    for (const [agent] of catalog.agents) {
      const state = catalog.readCatalogState(catalog.catalogParams({
        language, sources: ['heydamir'], selected: skill.id, target: agent
      }));
      assert.equal(state.language, language);
      assert.equal(state.target, agent);
      assert.equal(state.selected, skill.id);
      assert.deepEqual(state.sources, ['heydamir']);
      const prompt = catalog.agentInstallPrompt(skill, agent, language);
      assert.ok(prompt.startsWith(language === 'vi' ? 'Hãy cài đặt skill' : 'Please install'));
      for (const required of ['/install-manifests/heydamir-unslop.json', 'SHA-256', 'LICENSE', '.vas-manifest.json']) assert.ok(prompt.includes(required));
      assert.ok(!prompt.includes('4652254daff586ff4739849395a127b56f7f8cc7'));
      assert.ok(!prompt.includes('/skills/unslop/'));
      for (const target of agent === 'all' ? Object.keys(catalog.targetFolders) : [agent]) {
        assert.ok(prompt.includes(`"${catalog.targetFolders[target]}/heydamir-unslop/"`));
        for (const mode of ['link', 'copy']) {
          const plan = catalog.installationPlan(skill.id, target, { mode });
          assert.deepEqual(plan.paths, [`${catalog.targetFolders[target]}/heydamir-unslop/SKILL.md`]);
          assert.ok(plan.install.includes(`install heydamir-unslop --target ${target} --mode ${mode}`));
          assert.ok(plan.status.includes(`--target ${target}`));
          assert.ok(plan.uninstall.includes(`uninstall heydamir-unslop --target ${target}`));
        }
      }
    }
  }
});

test('UI Unslop renders author credit and links every reference/helper without executing it', () => {
  const markdown = fs.readFileSync(path.join(root, skill.path, 'SKILL.md'), 'utf8');
  for (const language of ['vi', 'en']) {
    const result = catalog.renderMarkdown(markdown, `https://example.invalid/${skill.path}/SKILL.md`, language);
    assert.ok(result.html.includes('Damir Sokolovsky'));
    assert.ok(result.html.includes('CC BY 4.0'));
    assert.ok(result.html.includes('references/visuals.md'));
    assert.ok(result.html.includes('scripts/story.mjs'));
    assert.ok(result.html.includes('separate authorization'));
    assert.ok(!result.html.includes('<script'));
  }
  for (const name of ['snapshot.mjs', 'story.mjs']) {
    const script = fs.readFileSync(path.join(root, skill.path, 'scripts', name), 'utf8');
    assert.ok(!script.includes('npx '));
    assert.ok(script.includes('Obtain approval'));
  }
});
