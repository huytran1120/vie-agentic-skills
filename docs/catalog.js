/* Catalog logic is shared with the dependency-free Node regression tests. */
(function () {
  'use strict';
  const i18n = typeof module !== 'undefined' && module.exports ? require('./i18n.js') : globalThis.VASI18n;
  const agents = [
    ['antigravity', 'Antigravity', 'A'], ['codex', 'Codex', 'Co'],
    ['claude', 'Claude', 'Cl'], ['cursor', 'Cursor', 'Cu'],
    ['windsurf', 'Windsurf', 'W'], ['cline', 'Cline', 'C'],
    ['copilot', 'Copilot', 'Gh'], ['all', 'Tất cả', 'All']
  ];
  const groups = [
    { id: 'all', label: 'Tất cả', categories: [] },
    { id: 'blender', label: 'Blender Studio', categories: ['blender'] },
    { id: 'web', label: 'Frontend & Web', categories: ['front-end', 'frontend', 'web-development', 'full-stack', 'fullstack', 'web'] },
    { id: 'development', label: 'Development', categories: ['development'] },
    { id: 'devops', label: 'DevOps', categories: ['devops', 'ci-cd'] },
    { id: 'testing', label: 'Testing & QA', categories: ['testing', 'test-automation'] },
    { id: 'security', label: 'Security', categories: ['security'] },
    { id: 'data-ai', label: 'Data & AI', categories: ['ai-ml', 'data', 'data-science', 'database'] },
    { id: 'design', label: 'UI/UX & Design', categories: ['design', 'front-end', 'frontend', '3d', '3d-web'] },
    { id: 'cloud', label: 'Cloud', categories: ['cloud'] },
    { id: 'workflow', label: 'Quy trình & tiện ích', categories: ['workflow', 'productivity', 'automation'] }
  ];
  const recommended = ['ui-ux-pro-max', 'code-review', 'cloudflare-security-audit', 'webapp-testing', 'frontend-design', 'setup-pre-commit', 'impeccable', 'research', 'landing-page-design', 'writing-for-agents', 'web-performance-optimization'];


  function normalize(value) {
    return String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd').replace(/Đ/g, 'D').toLowerCase();
  }
  function matchesGroup(skill, groupId) {
    const group = groups.find(item => item.id === groupId);
    return groupId === 'all' || Boolean(group && group.categories.includes(skill.category));
  }
  function filterSkills(skills, { query = '', group = 'all', category = 'all', sort = 'recommended', sources = [] } = {}) {
    const words = normalize(query).trim().split(/\s+/).filter(Boolean);
    const matches = skills.filter(skill => {
      if (!matchesGroup(skill, group) || (category !== 'all' && skill.category !== category)) return false;
      if (sources.length && !sources.some(source => matchesSource(skill, source))) return false;
      const text = normalize([skill.id, skill.name, skill.description, skill.category, skill.source, skill.source_repo, skill.author, ...(skill.tags || [])].join(' '));
      return words.every(word => text.includes(word));
    });
    return matches.sort((a, b) => {
      if (sort === 'recommended') {
        if (words.length) {
          const relevance = skill => {
            const names = [normalize(skill.id), normalize(skill.name)];
            const phrase = normalize(query).trim();
            if (names.includes(phrase)) return 0;
            if (names.some(name => name.startsWith(phrase))) return 1;
            if (names.some(name => words.every(word => name.includes(word)))) return 2;
            const tags = normalize([skill.category, ...(skill.tags || [])].join(' '));
            if (words.every(word => tags.includes(word))) return 3;
            return 4;
          };
          const difference = relevance(a) - relevance(b);
          if (difference) return difference;
        }
        const aRank = recommended.indexOf(a.id);
        const bRank = recommended.indexOf(b.id);
        const difference = (aRank < 0 ? recommended.length : aRank) - (bRank < 0 ? recommended.length : bRank);
        if (difference) return difference;
      }
      return a.id.localeCompare(b.id, 'en') * (sort === 'za' ? -1 : 1);
    });
  }
  function shellQuote(value) {
    return /^[a-zA-Z0-9_./-]+$/.test(value) ? value : "'" + value.replace(/'/g, "'\\''") + "'";
  }
  const targetFolders = { antigravity: '.agents/skills', codex: '.codex/skills', claude: '.claude/skills', cursor: '.cursor/skills', windsurf: '.windsurf/skills', cline: '.cline/skills', copilot: '.github/skills' };
  const globalFolders = { antigravity: '~/.gemini/antigravity/skills', codex: '~/.codex/skills', claude: '~/.claude/skills', cursor: '~/.cursor/skills', windsurf: '~/.codeium/windsurf/skills', cline: '~/.cline/skills', copilot: '~/.copilot/skills' };
  const publishedSite = 'https://huytran1120.github.io/vie-agentic-skills';
  const encodePath = path => path.split('/').map(part => encodeURIComponent(part).replace(/[!'()*]/g, char => '%' + char.charCodeAt(0).toString(16).toUpperCase())).join('/');
  function installManifestUrl(skill, base = publishedSite) {
    if (typeof skill.id !== 'string' || /[\\\x00-\x20\x7f]/.test(skill.id) || skill.id.split('/').some(part => !part || part === '.' || part === '..')) {
      throw new Error('Invalid canonical skill ID');
    }
    return `${base}/install-manifests/${encodePath(skill.id)}.json`;
  }
  function agentInstallPrompt(skill, target, language = 'vi') {
    if (!agents.some(agent => agent[0] === target)) throw new Error(i18n.translate('install.invalidAgent', language));
    const leaf = skillUrl(skill).split('/').slice(-2, -1)[0];
    const targets = target === 'all' ? Object.keys(targetFolders) : [target];
    return i18n.translate('quick.prompt', language, {
      id: JSON.stringify(skill.id),
      agent: target === 'all' ? i18n.translate('quick.allAgents', language) : agents.find(agent => agent[0] === target)[1],
      paths: targets.map(agent => JSON.stringify(`${targetFolders[agent]}/${decodeURIComponent(leaf)}/`)).join('\n'),
      manifest: installManifestUrl(skill)
    });
  }
  function validateInstallManifest(manifest, skill) {
    if (!manifest || manifest.schema_version !== 1 || manifest.repository !== 'huytran1120/vie-agentic-skills'
        || manifest.skill_id !== skill.id || manifest.source_path !== String(skill.path || `skills/${skill.id}`).replace(/\/SKILL\.md$/, '')
        || manifest.target_name !== decodeURIComponent(skillUrl(skill).split('/').slice(-2, -1)[0])
        || !/^[0-9a-f]{40}$/.test(manifest.revision || '')) throw new Error('Invalid installation manifest');
    if (manifest.available !== true) throw new Error('Unpublished installation snapshot');
    if (!Array.isArray(manifest.files) || !manifest.files.length || !manifest.files.some(file => file.path === 'SKILL.md')) throw new Error('Missing installation files');
    const seen = new Set();
    for (const file of manifest.files) {
      if (typeof file.path !== 'string' || /[\\\x00-\x1f\x7f]/.test(file.path) || file.path.split('/').some(part => !part || part === '.' || part === '..')
          || seen.has(file.path) || !Number.isSafeInteger(file.bytes) || file.bytes < 0 || !/^[0-9a-f]{64}$/.test(file.sha256 || '')
          || typeof file.executable !== 'boolean'
          || file.url !== `https://raw.githubusercontent.com/${manifest.repository}/${manifest.revision}/${encodePath(`${manifest.source_path}/${file.path}`)}`) {
        throw new Error('Invalid installation file inventory');
      }
      seen.add(file.path);
    }
    if (manifest.receipt?.filename !== '.vas-manifest.json' || manifest.receipt.key !== skill.id
        || manifest.receipt.entry?.target_name !== manifest.target_name || manifest.receipt.entry?.mode !== 'copy') throw new Error('Invalid installation receipt');
    return manifest;
  }
  function installationPlan(id, target, { scope = 'repository', projectPath = '', mode = 'link', language = 'vi' } = {}) {
    const text = (key, values) => i18n.translate(key, language, values);
    if (!agents.some(agent => agent[0] === target)) throw new Error(text('install.invalidAgent'));
    if (!['link', 'copy'].includes(mode)) throw new Error(text('install.invalidMode'));
    if (!['repository', 'project', 'global'].includes(scope)) throw new Error(text('install.invalidScope'));
    if (scope === 'global' && target === 'all') throw new Error(text('install.globalAll'));
    let root = '';
    if (scope === 'project') {
      root = projectPath.trim();
      if (!root || /[\x00-\x1f\x7f]/.test(root) || !(/^(\/|[A-Za-z]:[\\/])/.test(root))) {
        throw new Error(text('install.invalidPath'));
      }
      if (/^[A-Za-z]:/.test(root)) root = root.replace(/\\/g, '/');
      root = root.replace(/\/+$/, '');
    }
    const targets = target === 'all' && scope === 'project' ? Object.keys(targetFolders) : [target];
    const location = agent => scope === 'global' ? ' --global' : scope === 'project' ? ' --dest ' + shellQuote(`${root}/${targetFolders[agent]}`) : '';
    const paths = (target === 'all' ? Object.keys(targetFolders) : [target]).map(agent => {
      const folder = scope === 'global' ? globalFolders[agent] : scope === 'project' ? `${root}/${targetFolders[agent]}` : targetFolders[agent];
      return `${folder}/${id.split('/').pop()}/SKILL.md`;
    });
    return {
      install: targets.map(agent => `./vas install ${shellQuote(id)} --target ${agent} --mode ${mode}${location(agent)}`).join('\n'),
      status: targets.map(agent => `./vas status --target ${agent}${location(agent)}`).join('\n'),
      uninstall: targets.map(agent => `./vas uninstall ${shellQuote(id)} --target ${agent}${location(agent)}`).join('\n'),
      paths,
      prompt: text('install.prompt', { id: JSON.stringify(id), paths: paths.map(path => JSON.stringify(path)).join('\n') })
    };
  }
  function installCommand(id, target, options) {
    return installationPlan(id, target, options).install;
  }
  function readCatalogState(search, preferredLanguage = 'vi') {
    const params = new URLSearchParams(search);
    return {
      query: params.get('q') || '', selected: params.get('skill') || null,
      language: i18n.resolveLanguage(search, preferredLanguage),
      target: agents.some(agent => agent[0] === params.get('agent')) ? params.get('agent') : 'antigravity',
      group: groups.some(group => group.id === params.get('group')) ? params.get('group') : 'all',
      category: params.get('category') || 'all',
      sort: ['az', 'za'].includes(params.get('sort')) ? params.get('sort') : 'recommended',
      view: params.get('view') === 'grid' ? 'grid' : 'list',
      sources: [...new Set((params.get('sources') || '').split(',').filter(key => Object.hasOwn(sourceNames, key)))]
    };
  }
  function catalogParams(value) {
    const params = new URLSearchParams();
    if (['vi', 'en'].includes(value.language)) params.set('lang', value.language);
    if (value.query) params.set('q', value.query);
    if (value.selected) params.set('skill', value.selected);
    if (value.target && value.target !== 'antigravity') params.set('agent', value.target);
    if (value.group && value.group !== 'all') params.set('group', value.group);
    if (value.category && value.category !== 'all') params.set('category', value.category);
    if (value.sort && value.sort !== 'recommended') params.set('sort', value.sort);
    if (value.sources?.length) params.set('sources', [...value.sources].filter(key => Object.hasOwn(sourceNames, key)).sort().join(','));
    if (value.view === 'grid') params.set('view', 'grid');
    return params.toString();
  }
  function skillUrl(skill, base = '..') {
    if (!['.', '..'].includes(base)) throw new Error('Gốc đường dẫn skill không hợp lệ');
    const path = String(skill.path || `skills/${skill.id}`).replace(/\/SKILL\.md$/, '');
    if (!path.startsWith('skills/') || path.split('/').some(part => !part || part === '.' || part === '..' || part.includes('\\'))) {
      throw new Error(`Đường dẫn skill không hợp lệ: ${skill.id}`);
    }
    return `${base}/${path.split('/').map(encodeURIComponent).join('/')}/SKILL.md`;
  }
  function sourceUrl(skill) {
    if (!/^[a-zA-Z0-9_.-]+\/[a-zA-Z0-9_.-]+$/.test(skill.source_repo || '')) return null;
    const root = `https://github.com/${skill.source_repo}`;
    return String(skill.source || '').startsWith(root + '/') ? skill.source : root;
  }
  function escapeHtml(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
  }
  const sourceNames = { mattpocock: 'Matt Pocock', addy: 'Addy Osmani', blender: 'Blender Skills', youtube: 'YouTube Skills', hallmark: 'Hallmark', typesafe: 'TypeSafe AI', android: 'Android Skills', gamedev: 'GameDev Skills', heydamir: 'UI Unslop · Damir Sokolovsky', videoeditor: 'Video Editor · DaVinci Resolve' };
  function matchesSource(skill, source) {
    if (source === 'mattpocock') return skill.source_repo === 'mattpocock/skills';
    if (source === 'addy') return normalize(skill.author).includes('addy osmani');
    if (source === 'blender') return skill.source_repo === 'arjun988/blender-skills';
    if (source === 'youtube') return skill.source_repo === 'Jakeschincariol/youtube-agent-skill';
    if (source === 'hallmark') return skill.source_repo === 'Nutlope/hallmark';
    if (source === 'typesafe') return skill.source_repo === 'typesafe-ai/skills';
    if (source === 'android') return skill.source_repo === 'android/skills';
    if (source === 'gamedev') return skill.source_repo === 'gamedev-skills/awesome-gamedev-agent-skills';
    if (source === 'heydamir') return skill.source_repo === 'heydamir/unslop';
    if (source === 'videoeditor') return skill.source_repo === 'appariciojunior/video-editor-skills';
    return false;
  }

  // Render repository Markdown as text and a small, explicit set of safe elements.
  // Raw HTML is always escaped; link destinations must use an approved protocol.
  function renderMarkdown(markdown, baseUrl = 'https://example.invalid/skills/', language = 'vi') {
    const lines = String(markdown).replace(/^\uFEFF/, '').replace(/^---\s*\r?\n[\s\S]*?\r?\n---\s*(?:\r?\n|$)/, '').replace(/\r\n?/g, '\n').split('\n');
    const headings = [], ids = new Map(), aliases = new Map(), sourceIds = new Map(), fragments = [];
    function inline(value) {
      const tokens = String(value).split(/(`[^`]+`|!?\[[^\]]*\]\([^\s)]+\)|\*\*[^*]+\*\*|__[^_]+__)/g);
      return tokens.map(token => {
        if (token.startsWith('`') && token.endsWith('`')) return `<code>${escapeHtml(token.slice(1, -1))}</code>`;
        if ((token.startsWith('**') && token.endsWith('**')) || (token.startsWith('__') && token.endsWith('__'))) return `<strong>${escapeHtml(token.slice(2, -2))}</strong>`;
        const link = token.match(/^!?\[([^\]]*)\]\(([^\s)]+)\)$/);
        if (link) {
          try {
            if (link[2].startsWith('#')) {
              const position = fragments.push(link[2].slice(1)) - 1;
              return `<a data-runbook-fragment="${position}" href="#">${escapeHtml(link[1] || link[2])}</a>`;
            }
            const url = new URL(link[2], baseUrl);
            if (['https:', 'http:', 'mailto:'].includes(url.protocol)) return `<a href="${escapeHtml(url.href)}" target="_blank" rel="noopener noreferrer">${escapeHtml(link[1] || link[2])}</a>`;
          } catch (_) { /* Invalid destinations remain plain text. */ }
        }
        return escapeHtml(token);
      }).join('');
    }
    const cells = line => line.trim().replace(/^\||\|$/g, '').split('|').map(cell => cell.trim());
    const tableRule = line => /^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(line || '');
    const indentation = line => line.match(/^[ \t]*/)[0].replace(/\t/g, '    ').length;
    function listItem(line) {
      const match = line.match(/^([ \t]*)([-+*]|\d{1,9}[.)])([ \t]+)(.*)$/);
      return match ? { indent: indentation(match[1]), ordered: /^\d/.test(match[2]), number: parseInt(match[2], 10), content: match[4], contentIndent: indentation(match[1]) + match[2].length + match[3].replace(/\t/g, '    ').length } : null;
    }
    const blockStart = line => /^(?:#{1,6}\s|`{3,}|~{3,}|>|(?:[-*_]\s*){3,}$)/.test(line.trim());
    function renderList(input, start) {
      const first = listItem(input[start]), items = [];
      let i = start;
      while (i < input.length) {
        const marker = listItem(input[i]);
        if (!marker || marker.indent !== first.indent || marker.ordered !== first.ordered) break;
        const body = [marker.content]; i++;
        while (i < input.length) {
          if (!input[i].trim()) {
            let next = i + 1;
            while (next < input.length && !input[next].trim()) next++;
            if (next === input.length || indentation(input[next]) <= first.indent) break;
            body.push(''); i++; continue;
          }
          const nested = listItem(input[i]), indent = indentation(input[i]);
          if (nested && nested.indent <= first.indent) break;
          if (indent <= first.indent && blockStart(input[i])) break;
          // Continuation text stays in the current item; deeper markers become nested lists.
          const expanded = input[i].replace(/\t/g, '    ');
          body.push(expanded.slice(Math.min(indent, marker.contentIndent))); i++;
        }
        let html = renderBlocks(body);
        if (html.startsWith('<p>') && html.indexOf('</p>') === html.length - 4) html = html.slice(3, -4);
        items.push(`<li>${html}</li>`);
        // A blank line between sibling markers makes one list, rather than restarting at 1.
        let next = i;
        while (next < input.length && !input[next].trim()) next++;
        const sibling = listItem(input[next] || '');
        if (!sibling || sibling.indent !== first.indent || sibling.ordered !== first.ordered) break;
        i = next;
      }
      const tag = first.ordered ? 'ol' : 'ul';
      return { html: `<${tag}${first.ordered && first.number !== 1 ? ` start="${first.number}"` : ''}>${items.join('')}</${tag}>`, next: i };
    }
    function renderBlocks(input) {
      const parts = [];
      for (let i = 0; i < input.length;) {
        const line = input[i];
        if (!line.trim()) { i++; continue; }
        const fence = line.match(/^\s*(`{3,}|~{3,})([^\s]*)/);
        if (fence) {
          const code = []; i++;
          while (i < input.length && !input[i].trim().startsWith(fence[1])) code.push(input[i++]);
          if (i < input.length) i++;
          parts.push(`<div class="code-block"><div class="code-heading"><span>${escapeHtml(fence[2] || 'TEXT')}</span><button class="text-button" data-copy-code>${i18n.translate('copy.codeButton', language)}</button></div><pre><code>${escapeHtml(code.join('\n'))}</code></pre></div>`); continue;
        }
        const heading = line.match(/^(#{1,6})\s+(.+?)\s*#*$/);
        if (heading) {
          const text = heading[2].replace(/[*`]/g, ''), slug = 'runbook-' + (normalize(text).replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'section');
          const suffix = ids.get(slug) || 0; ids.set(slug, suffix + 1); const id = slug + (suffix ? `-${suffix + 1}` : '');
          const sourceSlug = text.toLowerCase().replace(/[^\p{L}\p{N}_ -]/gu, '').replace(/ /g, '-');
          const sourceSuffix = sourceIds.get(sourceSlug) || 0; sourceIds.set(sourceSlug, sourceSuffix + 1);
          aliases.set(sourceSlug + (sourceSuffix ? `-${sourceSuffix}` : ''), id);
          const normalizedAlias = slug.slice('runbook-'.length) + (suffix ? `-${suffix}` : '');
          if (!aliases.has(normalizedAlias)) aliases.set(normalizedAlias, id);
          aliases.set(id, id);
          const level = Math.max(2, Math.min(6, heading[1].length + 1));
          parts.push(`<h${level} id="${id}">${inline(heading[2])}</h${level}>`); headings.push({ id, text, level }); i++; continue;
        }
        if (tableRule(input[i + 1])) {
          const header = cells(line); i += 2; const rows = [];
          while (i < input.length && input[i].includes('|') && input[i].trim()) rows.push(cells(input[i++]));
          parts.push(`<div class="table-scroll"><table><thead><tr>${header.map(cell => `<th>${inline(cell)}</th>`).join('')}</tr></thead><tbody>${rows.map(row => `<tr>${header.map((_, index) => `<td>${inline(row[index] || '')}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`); continue;
        }
        if (/^\s*(?:[-*_]\s*){3,}$/.test(line)) { parts.push('<hr>'); i++; continue; }
        if (/^\s*>/.test(line)) {
          const quote = []; while (i < input.length && /^\s*>/.test(input[i])) quote.push(input[i++].replace(/^\s*>\s?/, ''));
          parts.push(`<blockquote>${inline(quote.join(' '))}</blockquote>`); continue;
        }
        const list = listItem(line);
        if (list) {
          const rendered = renderList(input, i); parts.push(rendered.html); i = rendered.next; continue;
        }
        const paragraph = [line]; i++;
        while (i < input.length && input[i].trim() && !blockStart(input[i]) && !listItem(input[i]) && !tableRule(input[i + 1])) paragraph.push(input[i++]);
        parts.push(`<p>${inline(paragraph.join(' '))}</p>`);
      }
      return parts.join('\n');
    }
    const html = renderBlocks(lines).replace(/ data-runbook-fragment="(\d+)" href="#"/g, (_, index) => {
      const fragment = fragments[Number(index)];
      let decoded = fragment;
      try { decoded = decodeURIComponent(fragment); } catch (_) { /* Keep malformed escapes as a harmless local fragment. */ }
      return ` href="#${escapeHtml(aliases.get(decoded) || fragment)}"`;
    });
    return { html, headings };
  }

  const api = { normalize, matchesGroup, filterSkills, installCommand, installationPlan, skillUrl, sourceUrl, groups, agents, targetFolders, globalFolders, readCatalogState, catalogParams, matchesSource, renderMarkdown, agentInstallPrompt, installManifestUrl, validateInstallManifest };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof document === 'undefined') return;

  const skillBase = document.documentElement?.dataset.skillBase || '..';
  const state = { skills: [], query: '', group: 'all', category: 'all', sort: 'recommended', sources: [], target: 'antigravity', view: 'list', page: 1, selected: null, loaded: false, scope: 'project', projectPath: '', mode: 'link', language: 'vi' };
  let locationSearch = typeof window === 'undefined' ? '' : window.location.search;
  function preferredLanguage() {
    try { return typeof window === 'undefined' ? 'vi' : window.localStorage.getItem('vas-language'); }
    catch (error) { console.warn('Cannot read the saved VAS language preference:', error); return 'vi'; }
  }
  if (typeof window !== 'undefined') Object.assign(state, readCatalogState(window.location.search, preferredLanguage()));
  const pageSize = 6;
  const byId = id => document.getElementById(id);
  const icon = name => `<svg class="icon" aria-hidden="true"><use href="#i-${name}"/></svg>`;
  const t = (key, values) => i18n.translate(key, state.language, values);
  const count = number => number.toLocaleString(state.language === 'en' ? 'en-US' : 'vi-VN');
  const groupLabel = group => t(`group.${group.id}`);
  const agentLabel = ([id, label]) => id === 'all' ? t('all') : label;
  const runbookNoun = total => total === 1 ? 'runbook' : 'runbooks';
  let toastTimer, copyReturnFocus, loadingPromise, detailRendered = null, runbookRequest = 0, libraryScroll = 0, filterDraft;
  const runbookCache = new Map();
  const manifestCache = new Map();
  const skillIcon = skill => skill.id.includes('review') ? 'branch' : /security|pentest/.test(skill.category) ? 'shield' : /test/.test(skill.category) ? 'flask' : /design|front/.test(skill.category) ? (skill.id === 'ui-ux-pro-max' ? 'pen' : 'layout') : 'terminal';

  function toast(message) {
    clearTimeout(toastTimer); byId('toast').textContent = message; byId('toast').hidden = false;
    toastTimer = setTimeout(() => { byId('toast').hidden = true; }, 3500);
  }
  async function copy(text, button, message = t('copy.command')) {
    const pending = typeof text !== 'string';
    try {
      if (!navigator.clipboard) throw new Error('Clipboard không khả dụng');
      if (pending && navigator.clipboard.write && typeof ClipboardItem !== 'undefined') {
        // WebKit requires starting the write in the click, before the manifest fetch resolves.
        await navigator.clipboard.write([new ClipboardItem({
          'text/plain': Promise.resolve(text).then(value => new Blob([value], { type: 'text/plain' }))
        })]);
      } else await navigator.clipboard.writeText(pending ? await text : text);
      toast(message);
    } catch (_) {
      const value = pending ? await text : text;
      copyReturnFocus = button; byId('manual-copy').hidden = false; byId('manual-copy-text').value = value; byId('manual-copy-text').focus(); byId('manual-copy-text').select();
    }
  }
  async function copyInstallPrompt(skill, button) {
    button.disabled = true; button.setAttribute('aria-busy', 'true');
    try {
      if (!manifestCache.has(skill.id)) {
        const base = skillBase === '..' ? '../_site' : '.';
        manifestCache.set(skill.id, (async () => {
          const response = await fetch(installManifestUrl(skill, base));
          if (!response.ok) throw new Error(`Installation manifest: HTTP ${response.status}`);
          return validateInstallManifest(await response.json(), skill);
        })());
      }
      const text = manifestCache.get(skill.id).then(() => {
        if (button.isConnected === false) throw new Error('Installation prompt selection changed');
        return agentInstallPrompt(skill, state.target, state.language);
      });
      await copy(text, button, t('quick.copied'));
    } catch (error) {
      if (button.isConnected === false) return;
      manifestCache.delete(skill.id);
      console.error('Cannot prepare the VAS installation prompt:', error);
      toast(t(skillBase === '..' ? 'quick.localError' : 'quick.error'));
    } finally { button.disabled = false; button.setAttribute('aria-busy', 'false'); }
  }
  function closeManualCopy() { byId('manual-copy').hidden = true; if (copyReturnFocus?.isConnected) copyReturnFocus.focus(); }
  function applyLanguage() {
    const afterInstallationOpen = document.querySelector('#installation-after')?.open;
    const cliOpen = document.querySelector('#cli-installation')?.open;
    i18n.apply(document, state.language);
    const toggle = byId('language-toggle');
    toggle.textContent = state.language === 'vi' ? 'EN' : 'VI';
    toggle.setAttribute('lang', state.language === 'vi' ? 'en' : 'vi');
    toggle.setAttribute('aria-label', t('language.switch'));
    toggle.setAttribute('title', state.language === 'vi' ? 'English' : 'Tiếng Việt');
    byId('theme-toggle').setAttribute('aria-label', t(document.documentElement.dataset.theme === 'dark' ? 'theme.light' : 'theme.dark'));
    byId('home-link').setAttribute('href', `./?lang=${state.language}`);
    byId('readme-link').setAttribute('href', `${skillBase}/README${state.language === 'en' ? '_EN' : ''}.md`);
    if (state.loaded) {
      renderNavigation(); renderCategories(); renderResults();
      if (afterInstallationOpen && byId('installation-after')) byId('installation-after').open = true;
      if (cliOpen && byId('cli-installation')) byId('cli-installation').open = true;
    } else {
      byId('results-status').textContent = t(byId('error-state').hidden ? 'catalog.loading' : 'catalog.error');
    }
    if (byId('filters-dialog').open) renderMobileFilters();
    syncHeroAgent();
  }
  function changeLanguage() {
    clearTimeout(toastTimer); byId('toast').hidden = true;
    syncUrl(false, true);
    state.language = state.language === 'vi' ? 'en' : 'vi';
    applyLanguage(); syncUrl(true, true);
    try { window.localStorage.setItem('vas-language', state.language); }
    catch (error) { console.warn('Cannot save the VAS language preference:', error); toast(t('language.storage')); }
  }
  function syncSources() {
    document.querySelectorAll('input[name="source"]').forEach(input => { input.checked = state.sources.includes(input.value); });
  }
  function renderNavigation() {
    byId('quick-agent-select').innerHTML = agents.map(agent => `<option value="${agent[0]}">${agentLabel(agent)}</option>`).join('');
    byId('quick-agent-select').value = state.target;
    byId('category-navigation').innerHTML = groups.map(group => `<button type="button" data-group="${group.id}" aria-pressed="${state.group === group.id && state.category === 'all'}"><span>${escapeHtml(groupLabel(group))}</span><span>${count(state.skills.filter(skill => matchesGroup(skill, group.id)).length)}</span></button>`).join('');
    document.querySelectorAll('[data-source-count]').forEach(node => { node.textContent = count(state.skills.filter(skill => matchesSource(skill, node.dataset.sourceCount)).length); });
  }
  function updateNavigation() {
    document.querySelectorAll('[data-group]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.group === state.group && state.category === 'all')));
    byId('category-select').value = state.category; syncSources();
  }
  function renderCategories() {
    const counts = new Map();
    state.skills.forEach(skill => counts.set(skill.category || 'general', (counts.get(skill.category || 'general') || 0) + 1));
    byId('category-select').innerHTML = `<option value="all">${t('filters.categories', { count: count(counts.size) })}</option>` + [...counts].sort(([a], [b]) => a.localeCompare(b)).map(([category, total]) => `<option value="${escapeHtml(category)}">${escapeHtml(category)} (${count(total)})</option>`).join('');
  }
  function syncUrl(push = false, beforeLoad = false) {
    if (typeof window === 'undefined' || (!state.loaded && !beforeLoad)) return;
    const params = catalogParams(state), url = window.location.pathname + (params ? '?' + params : '') + window.location.hash;
    // Keep list navigation context in this tab's history, never in shared URLs.
    const context = { page: state.page, scroll: Number.isFinite(window.scrollY) ? window.scrollY : 0, libraryScroll };
    const history = { ...window.history.state, vas: context };
    const changedUrl = url !== window.location.pathname + window.location.search + window.location.hash;
    const previous = window.history.state?.vas;
    const changedContext = !previous || previous.page !== context.page || previous.scroll !== context.scroll || previous.libraryScroll !== context.libraryScroll;
    if (changedUrl || (!push && changedContext)) window.history[push ? 'pushState' : 'replaceState'](history, '', url);
    locationSearch = window.location.search;
  }
  function commandPreview(id) { try { const plan = installationPlan(id, state.target, state); return { command: plan.install, plan }; } catch (error) { return { error: error.message }; } }
  function syncInstallation() {
    if (!state.selected || !byId('agent-select')) return;
    const preview = commandPreview(state.selected);
    byId('agent-select').value = state.target; byId('install-scope').value = state.scope;
    byId('agent-install-prompt').textContent = agentInstallPrompt(state.skills.find(skill => skill.id === state.selected), state.target, state.language);
    byId('install-scope').setAttribute('aria-invalid', String(state.scope === 'global' && state.target === 'all'));
    byId('install-mode').value = state.mode;
    byId('project-path-field').hidden = state.scope !== 'project';
    byId('project-path').setAttribute('aria-invalid', String(state.scope === 'project' && Boolean(state.projectPath) && !preview.command));
    byId('installation-command').textContent = preview.command || preview.error;
    byId('install-location-help').textContent = preview.error || t(state.scope === 'global' ? 'install.globalHelp' : 'install.projectHelp');
    byId('install-mode-help').textContent = t(state.mode === 'copy' ? 'install.copyHelp' : 'install.linkHelp');
    byId('installed-paths').textContent = preview.plan ? preview.plan.paths.join('\n') : t('install.choosePath');
    for (const [id, key] of [['install-status', 'status'], ['install-uninstall', 'uninstall'], ['install-prompt', 'prompt']]) {
      byId(id).textContent = preview.plan ? preview.plan[key] : preview.error;
      document.querySelectorAll(`[data-copy-element="${id}"]`).forEach(button => { button.disabled = !preview.plan; });
    }
    document.querySelectorAll('[data-copy-skill]').forEach(button => { button.disabled = !preview.command; });
  }
  function installation(skill) {
    return `<aside class="detail-sidebar"><section class="install-panel"><h2>${icon('terminal')}${t('install.title')}</h2><p>${t('install.description')}</p>
      <label for="agent-select">Agent</label><select id="agent-select">${agents.map(agent => `<option value="${agent[0]}">${agentLabel(agent)}</option>`).join('')}</select>
      <section class="quick-install" aria-labelledby="quick-install-title"><h3 id="quick-install-title">${t('quick.title')}</h3><p class="field-help">${t('quick.description')}</p>
        <button class="button primary copy-install" data-copy-agent-prompt="${escapeHtml(skill.id)}">${icon('copy')}${t('quick.copy')}</button>
        <p class="field-help">${t('quick.requirements')}</p>${skillBase === '..' ? `<p class="field-help">${t('quick.preview')}</p>` : ''}
        <details><summary>${t('quick.previewPrompt')}</summary><pre class="installation-code"><code id="agent-install-prompt"></code></pre></details>
      </section><details id="cli-installation" class="cli-installation"><summary>${t('quick.cli')}</summary><p class="field-help">${t('quick.cliHelp')}</p>
      <label for="install-scope">${t('install.scope')}</label><select id="install-scope" aria-describedby="install-location-help"><option value="project">${t('install.project')}</option><option value="global">${t('install.global')}</option></select>
      <div id="project-path-field"><label for="project-path">${t('install.path')}</label><input id="project-path" type="text" placeholder="/Projects/my-app" value="${escapeHtml(state.projectPath)}" autocomplete="off" spellcheck="false" aria-describedby="install-location-help"></div>
      <p id="install-location-help" class="field-help" role="status"></p>
      <label for="install-mode">${t('install.mode')}</label><select id="install-mode" aria-describedby="install-mode-help"><option value="link">${t('install.link')}</option><option value="copy">${t('install.copy')}</option></select><p id="install-mode-help" class="field-help"></p>
      <div class="code-heading"><label for="installation-command">${t('install.command')}</label><span>BASH / ZSH</span></div><pre class="installation-code"><code id="installation-command"></code></pre><button class="button secondary copy-install" data-copy-skill="${escapeHtml(skill.id)}">${icon('copy')}${t('install.copyCommand')}</button>
      <p class="field-help">${t('install.missingRepo')}<a href="#quickstart" data-library-link>${t('install.setup')}</a>${t('install.windows')}</p>
      <details id="installation-after" class="quickstart-details"><summary>${t('install.after')}</summary><div class="quickstart-commands">
        <div><h3>${t('install.statusTitle')}</h3><pre class="installation-code"><code id="install-status"></code></pre><button class="button secondary" data-copy-element="install-status">${t('install.copyStatus')}</button></div>
        <div><h3>${t('install.openTitle')}</h3><p class="field-help">${t('install.reload')}</p><pre class="installation-code"><code id="installed-paths"></code></pre></div>
        <div><h3>${t('install.promptTitle')}</h3><pre class="installation-code"><code id="install-prompt"></code></pre><button class="button secondary" data-copy-element="install-prompt" data-copy-message="${t('copy.prompt')}">${t('install.copyPrompt')}</button></div>
        <div><h3>${t('install.uninstallTitle')}</h3><p class="field-help">${t('install.uninstallHelp')}</p><pre class="installation-code"><code id="install-uninstall"></code></pre><button class="button secondary" data-copy-element="install-uninstall">${t('install.copyUninstall')}</button></div>
      </div></details></details></section>
      <nav class="runbook-toc" aria-label="${t('runbook.toc')}"><h2>${t('runbook.toc')}</h2><div id="runbook-toc-links"><p>${t('runbook.structure')}</p></div></nav>
      <p class="detail-source-note">${icon('shield')}${escapeHtml(t('install.risk', { risk: skill.risk || 'unknown' }))}</p></aside>`;
  }
  function quickCopyButton(skill) {
    const agent = agentLabel(agents.find(agent => agent[0] === state.target));
    return `<button class="button secondary skill-open" data-copy-agent-prompt="${escapeHtml(skill.id)}" aria-label="${escapeHtml(t('quick.copyLabel', { id: skill.id, agent }))}">${icon('copy')}<span data-agent-install-label>${escapeHtml(t('quick.copyFor', { agent }))}</span></button>`;
  }
  function renderResults() {
    if (!state.loaded) return;
    byId('library-view').hidden = Boolean(state.selected); byId('detail-view').hidden = !state.selected;
    if (state.selected) { renderDetail(); return; }
    detailRendered = null; runbookRequest++;
    const filtered = filterSkills(state.skills, state), visible = filtered.slice(0, state.page * pageSize);
    const categoryLabel = state.category !== 'all' ? state.category : groupLabel(groups.find(group => group.id === state.group));
    byId('results-title').textContent = categoryLabel;
    byId('results-status').textContent = t('results.total', { count: count(filtered.length), noun: runbookNoun(filtered.length) }) + (state.query ? t('results.query', { query: state.query }) : '');
    byId('clear-search').hidden = !state.query;
    const chips = [];
    if (state.query) chips.push(['query', state.query]);
    if (state.group !== 'all') chips.push(['group', categoryLabel]);
    if (state.category !== 'all') chips.push(['category', state.category]);
    state.sources.forEach(source => chips.push([source, sourceNames[source]]));
    byId('filter-description').innerHTML = chips.length ? chips.map(([key, label]) => `<button class="filter-chip" data-remove-filter="${key}" aria-label="${escapeHtml(t('filters.remove', { label }))}">${escapeHtml(label)} <span aria-hidden="true">×</span></button>`).join('') : `<span class="filter-chip">${t('all')}</span><span>${t('filters.none')}</span>`;
    byId('reset-filters').disabled = !chips.length;
    byId('active-filter-count').hidden = !chips.length; byId('active-filter-count').textContent = chips.length;
    byId('empty-state').hidden = filtered.length !== 0;
    byId('skills-results').classList.toggle('is-grid', state.view === 'grid');
    byId('skills-results').innerHTML = visible.map(skill => `<article class="skill-row" data-skill="${escapeHtml(skill.id)}"><div class="skill-symbol">${icon(skillIcon(skill))}</div><div class="skill-info"><h3><button class="skill-name" data-open-skill="${escapeHtml(skill.id)}">${escapeHtml(skill.id)}</button></h3><p class="skill-description">${escapeHtml(Object.hasOwn(i18n.messages, `summary.${skill.id}`) ? t(`summary.${skill.id}`) : skill.description)}</p><div class="skill-metadata"><div class="skill-tags">${[skill.category, ...(skill.tags || []).filter(tag => tag !== skill.category)].slice(0, 3).map(tag => `<span>${escapeHtml(tag)}</span>`).join('')}</div>${skill.author ? `<span class="skill-author">${escapeHtml(t('skill.source', { author: skill.author }))}${skill.license === 'MIT' ? ' · MIT' : ''}</span>` : ''}</div></div><div class="skill-actions">${quickCopyButton(skill)}<button class="button secondary skill-open" data-open-skill="${escapeHtml(skill.id)}" aria-label="${escapeHtml(t('skill.openLabel', { id: skill.id }))}"><span aria-hidden="true">↗</span>${t('skill.open')}</button></div></article>`).join('');
    byId('pagination-controls').hidden = !visible.length; byId('pagination-status').textContent = t('results.pagination', { visible: count(visible.length), total: count(filtered.length), noun: runbookNoun(filtered.length) });
    byId('load-more').hidden = visible.length >= filtered.length;
    document.querySelectorAll('[data-view]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.view === state.view)));
    byId('sort-select').value = state.sort; updateNavigation(); syncInstallation();
  }
  function renderDetail() {
    const skill = state.skills.find(skill => skill.id === state.selected);
    if (!skill) { state.selected = null; renderResults(); return; }
    const detailKey = `${skill.id}:${state.language}`;
    if (detailRendered === detailKey) { syncInstallation(); return; }
    detailRendered = detailKey;
    const source = sourceUrl(skill);
    byId('skill-detail').innerHTML = `<nav class="breadcrumb" aria-label="${t('detail.breadcrumb')}"><button data-back-library>${t('library')}</button><span>›</span><code>${escapeHtml(skill.id)}</code></nav>
      <div class="detail-heading"><div class="detail-title-group"><div class="skill-symbol">${icon(skillIcon(skill))}</div><div><p class="eyebrow">Skill / Runbook</p><h1 tabindex="-1" id="detail-title">${escapeHtml(skill.id)}</h1></div></div><div class="detail-actions"><a class="button secondary" href="${escapeHtml(skillUrl(skill, skillBase))}" target="_blank" rel="noopener noreferrer">${icon('book')}${t('detail.read')}</a><button class="button secondary" data-share-skill="${escapeHtml(skill.id)}">${t('detail.share')}</button></div></div>
      <p class="detail-description">${escapeHtml(skill.description)}</p><div class="detail-provenance">${skill.author ? `<span>${escapeHtml(skill.author)}</span>` : ''}<span>${escapeHtml(skill.license || t('detail.license'))}</span><span class="skill-tag">${escapeHtml(skill.category)}</span>${source ? `<a href="${escapeHtml(source)}" target="_blank" rel="noopener noreferrer">${escapeHtml(skill.source_repo)} ↗</a>` : ''}</div>
      <div class="detail-layout"><div><section class="runbook-panel"><header>${icon('book')}<code>SKILL.md</code><span>${t('detail.reader')}</span></header><p class="runbook-language-note">${t('detail.original')}</p><div id="runbook-content" class="runbook-content" aria-busy="true"><p role="status">${t('runbook.loading')}</p></div></section><div class="next-skills"><div><h2>${t('detail.next')}</h2><p>${t('detail.nextDescription')}</p></div><button class="button secondary" data-back-library>${t('detail.back')}</button></div></div>${installation(skill)}</div>`;
    syncInstallation(); loadRunbook(skill);
  }
  async function loadRunbook(skill) {
    const request = ++runbookRequest;
    try {
      let text = runbookCache.get(skill.id);
      if (text === undefined) { const response = await fetch(skillUrl(skill, skillBase)); if (!response.ok) throw new Error(`HTTP ${response.status}`); text = await response.text(); if (text.length > 2000000) throw new Error(t('runbook.tooLarge')); runbookCache.set(skill.id, text); }
      if (request !== runbookRequest || state.selected !== skill.id) return;
      const parsed = renderMarkdown(text, new URL(skillUrl(skill, skillBase), window.location.href).href, state.language);
      byId('runbook-content').innerHTML = parsed.html;
      byId('runbook-toc-links').innerHTML = parsed.headings.slice(0, 8).map(heading => `<a href="#${heading.id}">${escapeHtml(heading.text)}</a>`).join('') || `<a href="#detail-title">${t('runbook.content')}</a>`;
    } catch (error) {
      if (request !== runbookRequest || state.selected !== skill.id) return;
      console.error('Cannot load the VAS runbook:', error);
      byId('runbook-content').innerHTML = `<div class="empty-state"><h2>${t('runbook.errorTitle')}</h2><p>${t('runbook.errorHelp')}</p><button class="button secondary" data-retry-runbook>${t('runbook.retry')}</button></div>`;
      byId('runbook-toc-links').textContent = t('runbook.error');
    } finally { if (request === runbookRequest && state.selected === skill.id) byId('runbook-content').setAttribute('aria-busy', 'false'); }
  }
  function applyFilters() { state.page = 1; state.selected = null; renderResults(); syncUrl(); }
  function resetFilters() { state.query = ''; state.group = 'all'; state.category = 'all'; state.sources = []; byId('search-input').value = ''; applyFilters(); byId('search-input').focus({ preventScroll: true }); }
  function focusSearch() {
    if (state.selected) { state.selected = null; renderResults(); syncUrl(); }
    byId('search-input').focus({ preventScroll: true }); byId('catalog').scrollIntoView({ block: 'start', behavior: 'instant' });
  }
  function openSkill(id) {
    if (!state.skills.some(skill => skill.id === id)) return;
    libraryScroll = typeof window !== 'undefined' ? window.scrollY : 0;
    syncUrl();
    // Leave the outgoing entry before hiding its content can clamp the browser's saved scroll.
    state.selected = id; syncUrl(true); renderResults();
    byId('detail-view').scrollIntoView({ block: 'start', behavior: 'instant' }); byId('detail-title').focus({ preventScroll: true });
    syncUrl();
  }
  function closeDetail() {
    syncUrl();
    state.selected = null; syncUrl(true); renderResults();
    window.scrollTo({ top: libraryScroll, behavior: 'instant' }); syncUrl();
  }
  function validateState() {
    if (!state.skills.some(skill => skill.category === state.category)) state.category = 'all';
    if (state.selected && !state.skills.some(skill => skill.id === state.selected)) { state.selected = null; toast(t('skill.missing')); }
  }
  function restoreLocation(event) {
    // Native fragment history belongs to the visible runbook, not a new catalog view.
    if (window.location.search === locationSearch) return;
    locationSearch = window.location.search;
    clearTimeout(toastTimer); byId('toast').hidden = true;
    Object.assign(state, readCatalogState(window.location.search, preferredLanguage()));
    if (state.loaded) validateState();
    byId('search-input').value = state.query; byId('sort-select').value = state.sort;
    const context = (event?.state || window.history.state)?.vas;
    const pages = Math.max(1, Math.ceil(filterSkills(state.skills, state).length / pageSize));
    state.page = Number.isSafeInteger(context?.page) && context.page > 0 ? Math.min(context.page, pages) : 1;
    if (Number.isFinite(context?.libraryScroll) && context.libraryScroll >= 0) libraryScroll = context.libraryScroll;
    applyLanguage();
    const scroll = Number.isFinite(context?.scroll) && context.scroll >= 0 ? context.scroll : null;
    const restoreScroll = () => {
      if (scroll !== null) window.scrollTo({ top: scroll, behavior: 'instant' });
      else if (state.selected && state.loaded) byId('detail-view').scrollIntoView({ block: 'start', behavior: 'instant' });
    };
    restoreScroll();
    if (scroll !== null) {
      const destination = window.location.href;
      // Browsers restore their own persisted scroll after popstate has finished.
      // Reapply this SPA entry's context afterward without intercepting fragment-only history.
      setTimeout(() => { if (window.location.href === destination) restoreScroll(); }, 0);
    }
  }
  async function loadCatalog() {
    if (loadingPromise) return loadingPromise;
    byId('loading-state').hidden = false; byId('error-state').hidden = true; byId('empty-state').hidden = true;
    byId('skills-results').setAttribute('aria-busy', 'true'); byId('results-status').textContent = t('catalog.loading');
    loadingPromise = (async () => {
      try {
        const response = await fetch('./skills.min.json'); if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        if (!Array.isArray(data) || !data.length || data.some(skill => !skill || typeof skill.id !== 'string' || !skill.id || typeof skill.category !== 'string' || (skill.tags && (!Array.isArray(skill.tags) || skill.tags.some(tag => typeof tag !== 'string'))))) throw new Error(t('catalog.invalid'));
        data.forEach(skill => skillUrl(skill, skillBase)); state.skills = data; state.loaded = true;
        renderNavigation(); renderCategories();
        validateState(); byId('search-input').value = state.query; renderResults();
        return true;
      } catch (error) { console.error('Cannot load the VAS catalog:', error); byId('error-state').hidden = false; byId('results-status').textContent = t('catalog.error'); return false; }
      finally { byId('loading-state').hidden = true; byId('skills-results').setAttribute('aria-busy', 'false'); loadingPromise = null; }
    })(); return loadingPromise;
  }
  async function discover(id) { if (!state.loaded && !(await loadCatalog())) return; openSkill(id); }
  function renderMobileFilters() {
    const options = byId('category-select').innerHTML;
    byId('mobile-filter-content').innerHTML = `<h3>${t('filters.specialty')}</h3><div class="category-navigation">${groups.map(group => `<button data-draft-group="${group.id}" aria-pressed="${filterDraft.group === group.id && filterDraft.category === 'all'}"><span>${escapeHtml(groupLabel(group))}</span><span>${count(state.skills.filter(skill => matchesGroup(skill, group.id)).length)}</span></button>`).join('')}</div><label for="mobile-category">${t('filters.category')}</label><select id="mobile-category">${options}</select><fieldset class="source-filters"><legend>${t('filters.source')}</legend>${Object.entries(sourceNames).map(([id, label]) => `<label><input type="checkbox" name="mobile-source" value="${id}"${filterDraft.sources.includes(id) ? ' checked' : ''}><span>${label}</span><span>${count(state.skills.filter(skill => matchesSource(skill, id)).length)}</span></label>`).join('')}</fieldset>`;
    byId('mobile-category').value = filterDraft.category;
  }
  byId('open-filters').addEventListener('click', () => { filterDraft = { group: state.group, category: state.category, sources: [...state.sources] }; renderMobileFilters(); byId('filters-dialog').showModal(); });
  byId('apply-mobile-filters').addEventListener('click', () => { Object.assign(state, filterDraft); applyFilters(); byId('filters-dialog').close(); });
  byId('mobile-reset').addEventListener('click', () => { filterDraft = { group: 'all', category: 'all', sources: [] }; renderMobileFilters(); });
  byId('filters-dialog').addEventListener('click', event => { if (event.target === byId('filters-dialog')) byId('filters-dialog').close(); });
  byId('search-form').addEventListener('submit', event => event.preventDefault());
  byId('search-input').addEventListener('input', event => { state.query = event.target.value; applyFilters(); });
  byId('clear-search').addEventListener('click', () => { state.query = ''; byId('search-input').value = ''; applyFilters(); byId('search-input').focus(); });
  byId('reset-filters').addEventListener('click', resetFilters); byId('empty-reset').addEventListener('click', resetFilters);
  byId('focus-search').addEventListener('click', focusSearch); byId('retry-load').addEventListener('click', loadCatalog);
  byId('sort-select').addEventListener('change', event => { state.sort = event.target.value; applyFilters(); });
  byId('category-select').addEventListener('change', event => { state.category = event.target.value; state.group = 'all'; applyFilters(); });
  document.addEventListener('change', event => {
    const target = event.target;
    if (target.id === 'agent-select' || target.id === 'quick-agent-select') { state.target = target.value; syncHeroAgent(); syncInstallation(); if (!state.selected) renderResults(); syncUrl(); }
    else if (target.id === 'install-scope') { state.scope = target.value; syncInstallation(); }
    else if (target.id === 'install-mode') { state.mode = target.value; syncInstallation(); }
    else if (target.matches('input[name="source"]')) { state.sources = [...document.querySelectorAll('input[name="source"]:checked')].map(input => input.value); applyFilters(); }
    else if (target.id === 'mobile-category') { filterDraft.category = target.value; filterDraft.group = 'all'; renderMobileFilters(); }
    else if (target.matches('input[name="mobile-source"]')) filterDraft.sources = [...document.querySelectorAll('input[name="mobile-source"]:checked')].map(input => input.value);
  });
  document.addEventListener('input', event => { if (event.target.id === 'project-path') { state.projectPath = event.target.value; syncInstallation(); } });
  if (typeof window !== 'undefined') window.addEventListener('popstate', restoreLocation);
  byId('load-more').addEventListener('click', () => { const firstNew = state.page * pageSize; state.page++; renderResults(); syncUrl(); const next = byId('skills-results').querySelectorAll('.skill-name')[firstNew]; if (next) next.focus({ preventScroll: true }); });
  function selectSource(source) { state.query = ''; state.group = 'all'; state.category = 'all'; state.sources = [source]; byId('search-input').value = ''; applyFilters(); focusSearch(); }
  byId('addy-collection').addEventListener('click', () => selectSource('addy')); byId('matt-collection').addEventListener('click', () => selectSource('mattpocock'));
  byId('youtube-collection').addEventListener('click', () => selectSource('youtube'));
  byId('typesafe-collection').addEventListener('click', () => selectSource('typesafe'));
  byId('android-collection').addEventListener('click', () => selectSource('android'));
  byId('gamedev-collection').addEventListener('click', () => selectSource('gamedev'));
  byId('unslop-collection').addEventListener('click', () => selectSource('heydamir'));
  byId('videoeditor-collection').addEventListener('click', () => selectSource('videoeditor'));
  byId('menu-toggle').addEventListener('click', () => { const menu = byId('mobile-menu'); menu.hidden = !menu.hidden; byId('menu-toggle').setAttribute('aria-expanded', String(!menu.hidden)); });
  byId('mobile-menu').addEventListener('click', event => { if (event.target.closest('a')) { byId('mobile-menu').hidden = true; byId('menu-toggle').setAttribute('aria-expanded', 'false'); } });
  byId('theme-toggle').addEventListener('click', event => {
    const apply = () => {
      const dark = document.documentElement.dataset.theme !== 'dark';
      document.documentElement.dataset.theme = dark ? 'dark' : 'light';
      byId('theme-toggle').setAttribute('aria-pressed', String(dark));
      byId('theme-toggle').setAttribute('aria-label', t(dark ? 'theme.light' : 'theme.dark'));
    };
    if (typeof window !== 'undefined' && window.VASMotion) window.VASMotion.changeTheme(apply, event.currentTarget);
    else apply();
  });
  byId('close-manual-copy').addEventListener('click', closeManualCopy);
  document.addEventListener('keydown', event => {
    const editing = event.target.closest('input, textarea, select, [contenteditable="true"]');
    if (byId('filters-dialog').open) return;
    if ((event.key.toLowerCase() === 'k' && (event.metaKey || event.ctrlKey)) || (event.key === '/' && !editing)) { event.preventDefault(); focusSearch(); }
    else if (event.key === 'Escape') {
      if (!byId('manual-copy').hidden) closeManualCopy();
      else if (!byId('mobile-menu').hidden) { byId('mobile-menu').hidden = true; byId('menu-toggle').setAttribute('aria-expanded', 'false'); byId('menu-toggle').focus(); }
      else if (event.target === byId('search-input')) { state.query = ''; byId('search-input').value = ''; applyFilters(); }
    }
  });
  document.addEventListener('click', event => {
    if (event.target.closest('a[href="#quickstart"]')) byId('cli-setup').open = true;
    const link = event.target.closest('[data-library-link]');
    if (link && state.selected) { state.selected = null; renderResults(); syncUrl(true); }
    const button = event.target.closest('button'); if (!button || button.disabled) return;
    if (button.hasAttribute('data-back-library')) closeDetail();
    else if (button.hasAttribute('data-query')) { state.query = button.dataset.query; state.group = 'all'; state.category = 'all'; state.sources = []; byId('search-input').value = state.query; applyFilters(); focusSearch(); }
    else if (button.hasAttribute('data-blender')) { state.query = ''; state.group = 'blender'; state.category = 'all'; state.sources = []; byId('search-input').value = ''; applyFilters(); focusSearch(); }
    else if (button.dataset.group) { state.group = button.dataset.group; state.category = 'all'; applyFilters(); }
    else if (button.dataset.draftGroup) { filterDraft.group = button.dataset.draftGroup; filterDraft.category = 'all'; renderMobileFilters(); }
    else if (button.dataset.view) { state.view = button.dataset.view; renderResults(); syncUrl(); }
    else if (button.dataset.openSkill) openSkill(button.dataset.openSkill);
    else if (button.dataset.installSkill) { openSkill(button.dataset.installSkill); byId('cli-installation').open = true; byId('agent-select').focus(); }
    else if (button.dataset.copySkill) { const preview = commandPreview(button.dataset.copySkill); if (preview.command) copy(preview.command, button); }
    else if (button.dataset.copyAgentPrompt) copyInstallPrompt(state.skills.find(skill => skill.id === button.dataset.copyAgentPrompt), button);
    else if (button.dataset.shareSkill) { const url = new URL(window.location.href); url.search = catalogParams({ selected: button.dataset.shareSkill, target: state.target, language: state.language }); url.hash = ''; copy(url.href, button, t('copy.link')); }
    else if (button.dataset.copyElement) copy(byId(button.dataset.copyElement).textContent, button, button.dataset.copyMessage);
    else if (button.dataset.discover) discover(button.dataset.discover);
    else if (button.hasAttribute('data-retry-runbook')) loadRunbook(state.skills.find(skill => skill.id === state.selected));
    else if (button.hasAttribute('data-copy-code')) copy(button.closest('.code-block').querySelector('code').textContent, button, t('copy.code'));
    else if (button.dataset.removeFilter) {
      const key = button.dataset.removeFilter;
      if (key === 'query') { state.query = ''; byId('search-input').value = ''; } else if (key === 'group') state.group = 'all'; else if (key === 'category') state.category = 'all'; else state.sources = state.sources.filter(source => source !== key);
      applyFilters();
    }
  });
  function syncHeroAgent() {
    const agent = agents.find(agent => agent[0] === state.target);
    const label = agent ? agentLabel(agent) : 'Antigravity';
    if (typeof window !== 'undefined' && window.VASMotion) window.VASMotion.setAgent(label, agents.map(agentLabel));
    else byId('hero-agent').textContent = label;
    byId('hero-agent').setAttribute('aria-label', t('hero.agent', { agent: label }));
    byId('quick-agent-select').value = state.target;
    document.querySelectorAll('[data-agent-install-label]').forEach(node => {
      node.textContent = t('quick.copyFor', { agent: label });
      const button = node.closest('button');
      button.setAttribute('aria-label', t('quick.copyLabel', { id: button.dataset.copyAgentPrompt, agent: label }));
    });
  }
  byId('hero-agent').addEventListener('click', () => {
    const options = agents.filter(agent => agent[0] !== 'all');
    const index = options.findIndex(agent => agent[0] === state.target);
    state.target = options[(index + 1) % options.length][0]; syncHeroAgent(); syncInstallation(); syncUrl();
  });
  byId('hero-explore').addEventListener('click', focusSearch);
  byId('language-toggle').addEventListener('click', changeLanguage);
  applyLanguage();
  byId('search-input').value = state.query; loadCatalog();
})();
