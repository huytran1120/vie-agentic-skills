/* Catalog logic is shared with the dependency-free Node regression tests. */
(function () {
  'use strict';
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
  function installCommand(id, target, { scope = 'repository', projectPath = '' } = {}) {
    if (!agents.some(agent => agent[0] === target)) throw new Error('Agent không được hỗ trợ');
    const command = agent => `./vas install ${shellQuote(id)} --target ${agent} --mode link`;
    if (scope === 'repository') return command(target);
    if (scope === 'global') {
      if (target === 'all') throw new Error('Chọn một agent để cài toàn máy.');
      return command(target) + ' --global';
    }
    if (scope !== 'project') throw new Error('Nơi cài không được hỗ trợ.');
    let root = projectPath.trim();
    if (!root || /[\x00-\x1f\x7f]/.test(root) || !(/^(\/|[A-Za-z]:[\\/])/.test(root))) {
      throw new Error('Nhập đường dẫn tuyệt đối đến dự án, ví dụ /Users/ban/my-project hoặc C:/Projects/my-app.');
    }
    if (/^[A-Za-z]:/.test(root)) root = root.replace(/\\/g, '/');
    root = root.replace(/\/+$/, '');
    const targets = target === 'all' ? Object.keys(targetFolders) : [target];
    return targets.map(agent => command(agent) + ' --dest ' + shellQuote(`${root}/${targetFolders[agent]}`)).join('\n');
  }
  function readCatalogState(search) {
    const params = new URLSearchParams(search);
    return {
      query: params.get('q') || '', selected: params.get('skill') || null,
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
  const sourceNames = { mattpocock: 'Matt Pocock', addy: 'Addy Osmani', blender: 'Blender Skills' };
  function matchesSource(skill, source) {
    if (source === 'mattpocock') return skill.source_repo === 'mattpocock/skills';
    if (source === 'addy') return normalize(skill.author).includes('addy osmani');
    if (source === 'blender') return skill.source_repo === 'arjun988/blender-skills';
    return false;
  }

  // Render repository Markdown as text and a small, explicit set of safe elements.
  // Raw HTML is always escaped; link destinations must use an approved protocol.
  function renderMarkdown(markdown, baseUrl = 'https://example.invalid/skills/') {
    const lines = String(markdown).replace(/^\uFEFF/, '').replace(/^---\s*\r?\n[\s\S]*?\r?\n---\s*(?:\r?\n|$)/, '').replace(/\r\n?/g, '\n').split('\n');
    const headings = [], parts = [], ids = new Map();
    function inline(value) {
      const tokens = String(value).split(/(`[^`]+`|!?\[[^\]]*\]\([^\s)]+\)|\*\*[^*]+\*\*|__[^_]+__)/g);
      return tokens.map(token => {
        if (token.startsWith('`') && token.endsWith('`')) return `<code>${escapeHtml(token.slice(1, -1))}</code>`;
        if ((token.startsWith('**') && token.endsWith('**')) || (token.startsWith('__') && token.endsWith('__'))) return `<strong>${escapeHtml(token.slice(2, -2))}</strong>`;
        const link = token.match(/^!?\[([^\]]*)\]\(([^\s)]+)\)$/);
        if (link) {
          try {
            const url = new URL(link[2], baseUrl);
            if (['https:', 'http:', 'mailto:'].includes(url.protocol)) return `<a href="${escapeHtml(url.href)}" target="_blank" rel="noopener noreferrer">${escapeHtml(link[1] || link[2])}</a>`;
          } catch (_) { /* Invalid destinations remain plain text. */ }
        }
        return escapeHtml(token);
      }).join('');
    }
    const cells = line => line.trim().replace(/^\||\|$/g, '').split('|').map(cell => cell.trim());
    const tableRule = line => /^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(line || '');
    for (let i = 0; i < lines.length;) {
      const line = lines[i];
      if (!line.trim()) { i++; continue; }
      const fence = line.match(/^\s*(`{3,}|~{3,})([^\s]*)/);
      if (fence) {
        const code = []; i++;
        while (i < lines.length && !lines[i].trim().startsWith(fence[1])) code.push(lines[i++]);
        if (i < lines.length) i++;
        parts.push(`<div class="code-block"><div class="code-heading"><span>${escapeHtml(fence[2] || 'TEXT')}</span><button class="text-button" data-copy-code>Sao chép mã</button></div><pre><code>${escapeHtml(code.join('\n'))}</code></pre></div>`); continue;
      }
      const heading = line.match(/^(#{1,6})\s+(.+?)\s*#*$/);
      if (heading) {
        const text = heading[2].replace(/[*`]/g, ''), slug = 'runbook-' + (normalize(text).replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'section');
        const suffix = ids.get(slug) || 0; ids.set(slug, suffix + 1); const id = slug + (suffix ? `-${suffix + 1}` : '');
        const level = Math.max(2, Math.min(6, heading[1].length + 1));
        parts.push(`<h${level} id="${id}">${inline(heading[2])}</h${level}>`); headings.push({ id, text, level }); i++; continue;
      }
      if (tableRule(lines[i + 1])) {
        const header = cells(line); i += 2; const rows = [];
        while (i < lines.length && lines[i].includes('|') && lines[i].trim()) rows.push(cells(lines[i++]));
        parts.push(`<div class="table-scroll"><table><thead><tr>${header.map(cell => `<th>${inline(cell)}</th>`).join('')}</tr></thead><tbody>${rows.map(row => `<tr>${header.map((_, index) => `<td>${inline(row[index] || '')}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`); continue;
      }
      if (/^\s*(?:[-*_]\s*){3,}$/.test(line)) { parts.push('<hr>'); i++; continue; }
      if (/^\s*>/.test(line)) {
        const quote = []; while (i < lines.length && /^\s*>/.test(lines[i])) quote.push(lines[i++].replace(/^\s*>\s?/, ''));
        parts.push(`<blockquote>${inline(quote.join(' '))}</blockquote>`); continue;
      }
      const list = line.match(/^\s*(?:([-+*])|(\d+)[.)])\s+(.+)/);
      if (list) {
        const ordered = Boolean(list[2]), items = [];
        while (i < lines.length) {
          const item = lines[i].match(/^\s*(?:([-+*])|(\d+)[.)])\s+(.+)/);
          if (!item || Boolean(item[2]) !== ordered) break;
          items.push(inline(item[3])); i++;
        }
        const tag = ordered ? 'ol' : 'ul'; parts.push(`<${tag}>${items.map(item => `<li>${item}</li>`).join('')}</${tag}>`); continue;
      }
      const paragraph = [line]; i++;
      while (i < lines.length && lines[i].trim() && !/^\s*(?:#{1,6}\s|`{3,}|~{3,}|>|[-+*]\s|\d+[.)]\s)/.test(lines[i]) && !tableRule(lines[i + 1])) paragraph.push(lines[i++]);
      parts.push(`<p>${inline(paragraph.join(' '))}</p>`);
    }
    return { html: parts.join('\n'), headings };
  }

  const api = { normalize, matchesGroup, filterSkills, installCommand, skillUrl, sourceUrl, groups, agents, targetFolders, readCatalogState, catalogParams, matchesSource, renderMarkdown };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof document === 'undefined') return;

  const skillBase = document.documentElement?.dataset.skillBase || '..';
  const state = { skills: [], query: '', group: 'all', category: 'all', sort: 'recommended', sources: [], target: 'antigravity', view: 'list', page: 1, selected: null, loaded: false, scope: 'project', projectPath: '' };
  if (typeof window !== 'undefined') Object.assign(state, readCatalogState(window.location.search));
  const pageSize = 6;
  const byId = id => document.getElementById(id);
  const icon = name => `<svg class="icon" aria-hidden="true"><use href="#i-${name}"/></svg>`;
  const count = number => number.toLocaleString('en-US');
  const summaries = {
    'ui-ux-pro-max': 'Thiết kế UI/UX, typography và design systems cho web, mobile và desktop.',
    'code-review': 'Review thay đổi theo coding standards và specification. Báo lỗi có bằng chứng và hướng sửa cụ thể.',
    'cloudflare-security-audit': 'Rà soát access control, luồng dữ liệu và bề mặt tấn công theo quy trình security review.',
    'webapp-testing': 'Kiểm thử luồng người dùng bằng Playwright; kiểm tra giao diện, chụp màn hình và đọc browser logs.',
    'frontend-design': 'Xây dựng giao diện frontend có chủ đích: bố cục, typography và phân cấp thị giác.',
    'setup-pre-commit': 'Thiết lập Husky và lint-staged để chạy format, type checking và kiểm tra trước commit.'
  };
  let toastTimer, copyReturnFocus, loadingPromise, detailRendered = null, runbookRequest = 0, libraryScroll = 0, filterDraft;
  const runbookCache = new Map();
  const skillIcon = skill => skill.id.includes('review') ? 'branch' : /security|pentest/.test(skill.category) ? 'shield' : /test/.test(skill.category) ? 'flask' : /design|front/.test(skill.category) ? (skill.id === 'ui-ux-pro-max' ? 'pen' : 'layout') : 'terminal';

  function toast(message) {
    clearTimeout(toastTimer); byId('toast').textContent = message; byId('toast').hidden = false;
    toastTimer = setTimeout(() => { byId('toast').hidden = true; }, 3500);
  }
  async function copy(text, button, message = 'Đã sao chép. Chạy lệnh từ thư mục gốc VAS.') {
    try { if (!navigator.clipboard) throw new Error('Clipboard không khả dụng'); await navigator.clipboard.writeText(text); toast(message); }
    catch (_) { copyReturnFocus = button; byId('manual-copy').hidden = false; byId('manual-copy-text').value = text; byId('manual-copy-text').focus(); byId('manual-copy-text').select(); }
  }
  function closeManualCopy() { byId('manual-copy').hidden = true; if (copyReturnFocus?.isConnected) copyReturnFocus.focus(); }
  function syncSources() {
    document.querySelectorAll('input[name="source"]').forEach(input => { input.checked = state.sources.includes(input.value); });
  }
  function renderNavigation() {
    byId('category-navigation').innerHTML = groups.map(group => `<button type="button" data-group="${group.id}" aria-pressed="${state.group === group.id && state.category === 'all'}"><span>${group.label}</span><span>${count(state.skills.filter(skill => matchesGroup(skill, group.id)).length)}</span></button>`).join('');
    document.querySelectorAll('[data-source-count]').forEach(node => { node.textContent = count(state.skills.filter(skill => matchesSource(skill, node.dataset.sourceCount)).length); });
  }
  function updateNavigation() {
    document.querySelectorAll('[data-group]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.group === state.group && state.category === 'all')));
    byId('category-select').value = state.category; syncSources();
  }
  function renderCategories() {
    const counts = new Map();
    state.skills.forEach(skill => counts.set(skill.category || 'general', (counts.get(skill.category || 'general') || 0) + 1));
    byId('category-select').innerHTML = `<option value="all">Tất cả ${counts.size} danh mục</option>` + [...counts].sort(([a], [b]) => a.localeCompare(b)).map(([category, total]) => `<option value="${escapeHtml(category)}">${escapeHtml(category)} (${count(total)})</option>`).join('');
  }
  function syncUrl(push = false) {
    if (typeof window === 'undefined' || !state.loaded) return;
    const params = catalogParams(state), url = window.location.pathname + (params ? '?' + params : '') + window.location.hash;
    if (url !== window.location.pathname + window.location.search + window.location.hash) window.history[push ? 'pushState' : 'replaceState'](null, '', url);
  }
  function commandPreview(id) { try { return { command: installCommand(id, state.target, state) }; } catch (error) { return { error: error.message }; } }
  function syncInstallation() {
    const preview = commandPreview(state.selected || 'ui-ux-pro-max');
    byId('quickstart-command').textContent = state.selected ? preview.command || preview.error : 'Chọn một skill trong catalog để tạo lệnh cài.';
    document.querySelectorAll('[data-copy-element="quickstart-command"]').forEach(button => { button.disabled = !state.selected || !preview.command; });
    if (!state.selected || !byId('agent-select')) return;
    byId('agent-select').value = state.target; byId('install-scope').value = state.scope;
    byId('project-path-field').hidden = state.scope !== 'project';
    byId('project-path').setAttribute('aria-invalid', String(state.scope === 'project' && Boolean(state.projectPath) && !preview.command));
    byId('installation-command').textContent = preview.command || preview.error;
    byId('install-location-help').textContent = state.scope === 'global' ? (state.target === 'all' ? preview.error : 'Cài vào thư mục skill toàn máy của agent đã chọn.') : 'Đường dẫn chỉ dùng trong phiên này, không xuất hiện trong liên kết chia sẻ.';
    document.querySelectorAll('[data-copy-skill]').forEach(button => { button.disabled = !preview.command; });
  }
  function installation(skill) {
    return `<aside class="detail-sidebar"><section class="install-panel"><h2>${icon('terminal')}Cài skill</h2><p>Chọn môi trường, sao chép lệnh và chạy từ thư mục gốc VAS. Yêu cầu Python 3.</p>
      <label for="agent-select">Agent</label><select id="agent-select">${agents.map(([id, label]) => `<option value="${id}">${label}</option>`).join('')}</select>
      <label for="install-scope">Phạm vi cài đặt</label><select id="install-scope"><option value="project">Dự án cụ thể</option><option value="global">Toàn máy</option></select>
      <div id="project-path-field"><label for="project-path">Đường dẫn tuyệt đối đến dự án</label><input id="project-path" type="text" placeholder="/Projects/my-app" value="${escapeHtml(state.projectPath)}" autocomplete="off" spellcheck="false" aria-describedby="install-location-help"></div>
      <p id="install-location-help" class="field-help" role="status"></p><p class="mode-note"><code>mode: link</code> Liên kết skill vào thư mục đích</p>
      <div class="code-heading"><label for="installation-command">Lệnh cài đặt</label><span>SHELL</span></div><pre class="installation-code"><code id="installation-command"></code></pre><button class="button primary copy-install" data-copy-skill="${escapeHtml(skill.id)}">${icon('copy')}Sao chép lệnh</button>
      <p class="field-help">Giữ nguyên vị trí kho nguồn khi dùng link. Kiểm tra đường dẫn trước khi chạy. <a href="#quickstart" data-library-link>Hướng dẫn CLI</a>.</p></section>
      <nav class="runbook-toc" aria-label="Trong runbook này"><h2>Trong runbook này</h2><div id="runbook-toc-links"><p>Đang đọc cấu trúc tài liệu…</p></div></nav>
      <p class="detail-source-note">${icon('shield')}Nhãn risk: ${escapeHtml(skill.risk || 'unknown')}. Đây là metadata nguồn, không thay thế việc kiểm tra script và quyền truy cập.</p></aside>`;
  }
  function renderResults() {
    if (!state.loaded) return;
    byId('library-view').hidden = Boolean(state.selected); byId('detail-view').hidden = !state.selected;
    if (state.selected) { renderDetail(); return; }
    detailRendered = null; runbookRequest++;
    const filtered = filterSkills(state.skills, state), visible = filtered.slice(0, state.page * pageSize);
    const categoryLabel = state.category !== 'all' ? state.category : groups.find(group => group.id === state.group).label;
    byId('results-title').textContent = categoryLabel;
    byId('results-status').textContent = `${count(filtered.length)} runbook${state.query ? ` cho “${state.query}”` : ''}`;
    byId('clear-search').hidden = !state.query;
    const chips = [];
    if (state.query) chips.push(['query', state.query]);
    if (state.group !== 'all') chips.push(['group', categoryLabel]);
    if (state.category !== 'all') chips.push(['category', state.category]);
    state.sources.forEach(source => chips.push([source, sourceNames[source]]));
    byId('filter-description').innerHTML = chips.length ? chips.map(([key, label]) => `<button class="filter-chip" data-remove-filter="${key}" aria-label="Bỏ bộ lọc ${escapeHtml(label)}">${escapeHtml(label)} <span aria-hidden="true">×</span></button>`).join('') : '<span class="filter-chip">Tất cả</span><span>Chưa áp dụng bộ lọc</span>';
    byId('reset-filters').disabled = !chips.length;
    byId('active-filter-count').hidden = !chips.length; byId('active-filter-count').textContent = chips.length;
    byId('empty-state').hidden = filtered.length !== 0;
    byId('skills-results').classList.toggle('is-grid', state.view === 'grid');
    byId('skills-results').innerHTML = visible.map(skill => `<article class="skill-row" data-skill="${escapeHtml(skill.id)}"><div class="skill-symbol">${icon(skillIcon(skill))}</div><div class="skill-info"><h3><button class="skill-name" data-open-skill="${escapeHtml(skill.id)}">${escapeHtml(skill.id)}</button></h3><p class="skill-description">${escapeHtml(summaries[skill.id] || skill.description)}</p><div class="skill-metadata"><div class="skill-tags">${[skill.category, ...(skill.tags || []).filter(tag => tag !== skill.category)].slice(0, 3).map(tag => `<span>${escapeHtml(tag)}</span>`).join('')}</div>${skill.author ? `<span class="skill-author">Nguồn: ${escapeHtml(skill.author)}${skill.license === 'MIT' ? ' · MIT' : ''}</span>` : ''}</div></div><button class="button secondary skill-open" data-open-skill="${escapeHtml(skill.id)}" aria-label="Xem runbook ${escapeHtml(skill.id)}"><span aria-hidden="true">↗</span>Xem runbook</button></article>`).join('');
    byId('pagination-controls').hidden = !visible.length; byId('pagination-status').textContent = `Đang hiển thị ${count(visible.length)} / ${count(filtered.length)} runbook`;
    byId('load-more').hidden = visible.length >= filtered.length;
    document.querySelectorAll('[data-view]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.view === state.view)));
    byId('sort-select').value = state.sort; updateNavigation(); syncInstallation();
  }
  function renderDetail() {
    const skill = state.skills.find(skill => skill.id === state.selected);
    if (!skill) { state.selected = null; renderResults(); return; }
    if (detailRendered === skill.id) { syncInstallation(); return; }
    detailRendered = skill.id;
    const source = sourceUrl(skill);
    byId('skill-detail').innerHTML = `<nav class="breadcrumb" aria-label="Đường dẫn thư viện"><button data-back-library>Thư viện</button><span>›</span><code>${escapeHtml(skill.id)}</code></nav>
      <div class="detail-heading"><div class="detail-title-group"><div class="skill-symbol">${icon(skillIcon(skill))}</div><div><p class="eyebrow">Skill / Runbook</p><h1 tabindex="-1" id="detail-title">${escapeHtml(skill.id)}</h1></div></div><div class="detail-actions"><a class="button secondary" href="${escapeHtml(skillUrl(skill, skillBase))}" target="_blank" rel="noopener noreferrer">${icon('book')}Đọc SKILL.md</a><button class="button secondary" data-share-skill="${escapeHtml(skill.id)}">Chia sẻ ↗</button></div></div>
      <p class="detail-description">${escapeHtml(skill.description)}</p><div class="detail-provenance">${skill.author ? `<span>${escapeHtml(skill.author)}</span>` : ''}<span>${escapeHtml(skill.license || 'Giấy phép: xem trong skill')}</span><span class="skill-tag">${escapeHtml(skill.category)}</span>${source ? `<a href="${escapeHtml(source)}" target="_blank" rel="noopener noreferrer">${escapeHtml(skill.source_repo)} ↗</a>` : ''}</div>
      <div class="detail-layout"><div><section class="runbook-panel"><header>${icon('book')}<code>SKILL.md</code><span>Bản đọc runbook</span></header><div id="runbook-content" class="runbook-content" aria-busy="true"><p role="status">Đang tải nội dung SKILL.md…</p></div></section><div class="next-skills"><div><h2>Tìm skill cho bước tiếp theo</h2><p>Khám phá kiểm thử, frontend và bảo mật.</p></div><button class="button secondary" data-back-library>Về thư viện →</button></div></div>${installation(skill)}</div>`;
    syncInstallation(); loadRunbook(skill);
  }
  async function loadRunbook(skill) {
    const request = ++runbookRequest;
    try {
      let text = runbookCache.get(skill.id);
      if (text === undefined) { const response = await fetch(skillUrl(skill, skillBase)); if (!response.ok) throw new Error(`HTTP ${response.status}`); text = await response.text(); if (text.length > 2000000) throw new Error('Runbook vượt giới hạn đọc'); runbookCache.set(skill.id, text); }
      if (request !== runbookRequest || state.selected !== skill.id) return;
      const parsed = renderMarkdown(text, new URL(skillUrl(skill, skillBase), window.location.href).href);
      byId('runbook-content').innerHTML = parsed.html;
      byId('runbook-toc-links').innerHTML = parsed.headings.slice(0, 8).map(heading => `<a href="#${heading.id}">${escapeHtml(heading.text)}</a>`).join('') || '<a href="#detail-title">Nội dung runbook</a>';
    } catch (error) {
      if (request !== runbookRequest || state.selected !== skill.id) return;
      byId('runbook-content').innerHTML = `<div class="empty-state"><h2>Chưa tải được nội dung runbook</h2><p>Bạn vẫn có thể mở file SKILL.md hoặc thử tải lại.</p><button class="button secondary" data-retry-runbook>Thử lại</button></div>`;
      byId('runbook-toc-links').textContent = 'Nội dung chưa tải được.';
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
    state.selected = id; renderResults(); syncUrl(true);
    byId('detail-view').scrollIntoView({ block: 'start', behavior: 'instant' }); byId('detail-title').focus({ preventScroll: true });
  }
  function closeDetail() { state.selected = null; renderResults(); syncUrl(true); window.scrollTo({ top: libraryScroll, behavior: 'instant' }); }
  function validateState() {
    if (!state.skills.some(skill => skill.category === state.category)) state.category = 'all';
    if (state.selected && !state.skills.some(skill => skill.id === state.selected)) { state.selected = null; toast('Skill không còn trong catalog. Bạn có thể tìm lại bên dưới.'); }
  }
  function restoreLocation() {
    Object.assign(state, readCatalogState(window.location.search)); validateState();
    byId('search-input').value = state.query; byId('sort-select').value = state.sort;
    state.page = 1; renderResults(); syncHeroAgent();
    if (state.selected) byId('detail-view').scrollIntoView({ block: 'start', behavior: 'instant' });
  }
  async function loadCatalog() {
    if (loadingPromise) return loadingPromise;
    byId('loading-state').hidden = false; byId('error-state').hidden = true; byId('empty-state').hidden = true;
    byId('skills-results').setAttribute('aria-busy', 'true'); byId('results-status').textContent = 'Đang tải danh mục…';
    loadingPromise = (async () => {
      try {
        const response = await fetch('./skills.min.json'); if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        if (!Array.isArray(data) || !data.length || data.some(skill => !skill || typeof skill.id !== 'string' || !skill.id || typeof skill.category !== 'string' || (skill.tags && (!Array.isArray(skill.tags) || skill.tags.some(tag => typeof tag !== 'string'))))) throw new Error('Dữ liệu catalog không hợp lệ');
        data.forEach(skill => skillUrl(skill, skillBase)); state.skills = data; state.loaded = true;
        renderNavigation(); renderCategories();
        validateState(); byId('search-input').value = state.query; renderResults();
        return true;
      } catch (error) { console.error('Lỗi tải danh mục:', error); byId('error-state').hidden = false; byId('results-status').textContent = 'Không thể tải danh mục. Vui lòng thử lại.'; return false; }
      finally { byId('loading-state').hidden = true; byId('skills-results').setAttribute('aria-busy', 'false'); loadingPromise = null; }
    })(); return loadingPromise;
  }
  async function discover(id) { if (!state.loaded && !(await loadCatalog())) return; openSkill(id); }
  function renderMobileFilters() {
    const options = byId('category-select').innerHTML;
    byId('mobile-filter-content').innerHTML = `<h3>Chuyên môn</h3><div class="category-navigation">${groups.map(group => `<button data-draft-group="${group.id}" aria-pressed="${filterDraft.group === group.id && filterDraft.category === 'all'}"><span>${group.label}</span><span>${count(state.skills.filter(skill => matchesGroup(skill, group.id)).length)}</span></button>`).join('')}</div><label for="mobile-category">Danh mục chi tiết</label><select id="mobile-category">${options}</select><fieldset class="source-filters"><legend>Nguồn</legend>${Object.entries(sourceNames).map(([id, label]) => `<label><input type="checkbox" name="mobile-source" value="${id}"${filterDraft.sources.includes(id) ? ' checked' : ''}><span>${label}</span><span>${count(state.skills.filter(skill => matchesSource(skill, id)).length)}</span></label>`).join('')}</fieldset>`;
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
    if (target.id === 'agent-select') { state.target = target.value; syncHeroAgent(); syncInstallation(); syncUrl(); }
    else if (target.id === 'install-scope') { state.scope = target.value; syncInstallation(); }
    else if (target.matches('input[name="source"]')) { state.sources = [...document.querySelectorAll('input[name="source"]:checked')].map(input => input.value); applyFilters(); }
    else if (target.id === 'mobile-category') { filterDraft.category = target.value; filterDraft.group = 'all'; renderMobileFilters(); }
    else if (target.matches('input[name="mobile-source"]')) filterDraft.sources = [...document.querySelectorAll('input[name="mobile-source"]:checked')].map(input => input.value);
  });
  document.addEventListener('input', event => { if (event.target.id === 'project-path') { state.projectPath = event.target.value; syncInstallation(); } });
  if (typeof window !== 'undefined') window.addEventListener('popstate', () => { if (state.loaded) restoreLocation(); });
  byId('load-more').addEventListener('click', () => { const firstNew = state.page * pageSize; state.page++; renderResults(); const next = byId('skills-results').querySelectorAll('.skill-name')[firstNew]; if (next) next.focus({ preventScroll: true }); });
  function selectSource(source) { state.query = ''; state.group = 'all'; state.category = 'all'; state.sources = [source]; byId('search-input').value = ''; applyFilters(); focusSearch(); }
  byId('addy-collection').addEventListener('click', () => selectSource('addy')); byId('matt-collection').addEventListener('click', () => selectSource('mattpocock'));
  byId('menu-toggle').addEventListener('click', () => { const menu = byId('mobile-menu'); menu.hidden = !menu.hidden; byId('menu-toggle').setAttribute('aria-expanded', String(!menu.hidden)); });
  byId('mobile-menu').addEventListener('click', event => { if (event.target.closest('a')) { byId('mobile-menu').hidden = true; byId('menu-toggle').setAttribute('aria-expanded', 'false'); } });
  byId('theme-toggle').addEventListener('click', event => {
    const apply = () => {
      const dark = document.documentElement.dataset.theme !== 'dark';
      document.documentElement.dataset.theme = dark ? 'dark' : 'light';
      byId('theme-toggle').setAttribute('aria-pressed', String(dark));
      byId('theme-toggle').setAttribute('aria-label', dark ? 'Bật giao diện sáng' : 'Bật giao diện tối');
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
    const link = event.target.closest('[data-library-link]');
    if (link && state.selected) { state.selected = null; renderResults(); syncUrl(true); }
    const button = event.target.closest('button'); if (!button) return;
    if (button.hasAttribute('data-back-library')) closeDetail();
    else if (button.hasAttribute('data-query')) { state.query = button.dataset.query; state.group = 'all'; state.category = 'all'; state.sources = []; byId('search-input').value = state.query; applyFilters(); focusSearch(); }
    else if (button.hasAttribute('data-blender')) { state.query = ''; state.group = 'blender'; state.category = 'all'; state.sources = []; byId('search-input').value = ''; applyFilters(); focusSearch(); }
    else if (button.dataset.group) { state.group = button.dataset.group; state.category = 'all'; applyFilters(); }
    else if (button.dataset.draftGroup) { filterDraft.group = button.dataset.draftGroup; filterDraft.category = 'all'; renderMobileFilters(); }
    else if (button.dataset.view) { state.view = button.dataset.view; renderResults(); syncUrl(); }
    else if (button.dataset.openSkill) openSkill(button.dataset.openSkill);
    else if (button.dataset.copySkill) { const preview = commandPreview(button.dataset.copySkill); if (preview.command) copy(preview.command, button); }
    else if (button.dataset.shareSkill) { const url = new URL(window.location.href); url.search = catalogParams({ selected: button.dataset.shareSkill, target: state.target }); url.hash = ''; copy(url.href, button, 'Đã sao chép liên kết đến skill.'); }
    else if (button.dataset.copyElement) copy(byId(button.dataset.copyElement).textContent, button);
    else if (button.dataset.discover) discover(button.dataset.discover);
    else if (button.hasAttribute('data-retry-runbook')) loadRunbook(state.skills.find(skill => skill.id === state.selected));
    else if (button.hasAttribute('data-copy-code')) copy(button.closest('.code-block').querySelector('code').textContent, button, 'Đã sao chép đoạn mã.');
    else if (button.dataset.removeFilter) {
      const key = button.dataset.removeFilter;
      if (key === 'query') { state.query = ''; byId('search-input').value = ''; } else if (key === 'group') state.group = 'all'; else if (key === 'category') state.category = 'all'; else state.sources = state.sources.filter(source => source !== key);
      applyFilters();
    }
  });
  function syncHeroAgent() {
    const agent = agents.find(agent => agent[0] === state.target);
    const label = agent ? agent[1] : 'Antigravity';
    if (typeof window !== 'undefined' && window.VASMotion) window.VASMotion.setAgent(label, agents.map(agent => agent[1]));
    else byId('hero-agent').textContent = label;
    byId('hero-agent').setAttribute('aria-label', `Đổi agent mục tiêu. Hiện tại: ${label}`);
  }
  byId('hero-agent').addEventListener('click', () => {
    const options = agents.filter(agent => agent[0] !== 'all');
    const index = options.findIndex(agent => agent[0] === state.target);
    state.target = options[(index + 1) % options.length][0]; syncHeroAgent(); syncInstallation(); syncUrl();
  });
  byId('hero-explore').addEventListener('click', focusSearch);
  syncHeroAgent();
  byId('search-input').value = state.query; loadCatalog();
})();
