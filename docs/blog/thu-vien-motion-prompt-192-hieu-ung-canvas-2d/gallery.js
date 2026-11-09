/* Interactive Motion Prompt Gallery for VAS Blog — dependency-free Canvas 2D engine. */
(function () {
  'use strict';
  const CAT = window.MP_CATALOG;
  const PROMPT = window.MP_PROMPT;
  const MP = window.MotionPrompt;
  if (!CAT || !PROMPT || !MP) return;

  const $ = (sel, root) => (root || document).querySelector(sel);
  const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));

  const PACK_VI = {
    motion: 'Chuyển động Motion Graphics (Phần 1)',
    camera: 'Chuyển động Camera & Chuyển cảnh (Phần 1)',
    ui: 'Thành phần Giao diện UI',
    lp: 'Hiệu ứng Landing Page & Web (Phần 1)',
    photo: 'Phong cách Nhiếp ảnh, Ánh sáng & Màu sắc',
    motion2: 'Chuyển động Motion Graphics (Phần 2)',
    lp2: 'Hiệu ứng Landing Page & Web (Phần 2)',
    camera2: 'Chuyển động Camera & Chuyển cảnh (Phần 2)',
  };

  const CAT_VI = {
    'entrances-text': 'Xuất hiện & Chữ',
    'motion-polish': 'Tinh chỉnh nhịp điệu',
    'transitions-highlights': 'Chuyển cảnh & Điểm nhấn',
    'camera-movement': 'Di chuyển máy quay',
    'shooting-style-time': 'Cách quay & Thời gian',
    'transitions': 'Chuyển cảnh (Transitions)',
    'open-overlay': 'Mở & Lớp phủ (Overlay)',
    'select-switch': 'Chọn & Chuyển đổi',
    'navigate-status': 'Điều hướng & Trạng thái',
    'scroll': 'Hiệu ứng cuộn trang (Scroll)',
    'hover-click': 'Tương tác rê chuột & nhấp',
    'loading-loops': 'Tải trang & Vòng lặp nền',
    'lighting': 'Ánh sáng & Thời điểm',
    'lens-camera': 'Hiệu ứng ống kính & máy ảnh',
    'tone-finish': 'Tông màu & Hoàn thiện',
    'techniques': 'Kỹ thuật chuyển động',
    'text-shapes': 'Chữ & Hình khối',
    'mouse-input': 'Tương tác chuột & biểu mẫu',
    'showcase': 'Hiệu ứng trình diễn (Showcase)',
    'angles-framing': 'Góc máy & Bố cục khung hình',
    'transitions-editing': 'Chuyển cảnh & Dựng phim',
  };

  const TEXT = {
    vi: {
      all: 'Tất cả 192 mẫu',
      allInPack: 'Tất cả trong nhóm này',
      searchPh: 'Tìm theo tên, mã #001–#192 hoặc tag (vd: spring,parallax, #012)…',
      pause: 'Tạm dừng',
      play: 'Phát chuyển động',
      pauseAria: 'Tạm dừng tất cả hiệu ứng Canvas 2D',
      playAria: 'Phát tất cả hiệu ứng Canvas 2D',
      count: '{n} hiệu ứng',
      countOf: 'Đang hiển thị {n} / {total} hiệu ứng',
      openLabel: 'Mở chi tiết #{id} {name}',
      pick: '+ Chọn',
      picked: '✓ Đã chọn',
      pickLabel: 'Chọn #{id} {name}',
      trayTitle: 'Đã chọn {n} hiệu ứng để gửi cho AI agent',
      notePh: 'Ghi chú ngữ cảnh (tùy chọn, vd: dùng cho tiêu đề mở đầu video)…',
      copyPicks: 'Sao chép Prompt các mẫu đã chọn',
      clearPicks: 'Bỏ chọn tất cả',
      copied: 'Đã sao chép!',
      copyFailed: 'Không thể sao chép',
      size: '{w}×{h} px · Chu kỳ {c}s',
      copyPrompt: 'Sao chép Prompt',
      copyCode: 'Sao chép mã Canvas 2D',
      prev: '← Trước',
      next: 'Tiếp →',
      close: 'Đóng ×',
      outIntro: 'Tôi đã chọn {n} hiệu ứng từ thư viện motion-prompt. Hãy áp dụng đúng thông số chuyển động và hàm mẫu Canvas 2D cho tác vụ này:',
      outDemo: 'Mẫu trực quan',
      outSpec: 'Thông số & mã chuẩn',
      outNote: 'Ghi chú',
      outEnd: 'Bạn có thể lấy đầy đủ thông số bằng lệnh `node scripts/motion-prompt.mjs get <id>` trong skill motion-prompt.',
    },
    en: {
      all: 'All 192 moves',
      allInPack: 'All in this pack',
      searchPh: 'Search by name, #001–#192 or tag (e.g. spring, parallax, #012)…',
      pause: 'Pause all',
      play: 'Play all',
      pauseAria: 'Pause all Canvas 2D previews',
      playAria: 'Play all Canvas 2D previews',
      count: '{n} moves',
      countOf: 'Showing {n} of {total} moves',
      openLabel: 'Open details for #{id} {name}',
      pick: '+ Pick',
      picked: '✓ Picked',
      pickLabel: 'Pick #{id} {name}',
      trayTitle: '{n} move(s) picked for your AI agent',
      notePh: 'Optional context note (e.g. use for the hero section or opening title)…',
      copyPicks: 'Copy combined prompt for picked moves',
      clearPicks: 'Clear all',
      copied: 'Copied!',
      copyFailed: 'Copy failed',
      size: '{w}×{h} px · {c}s loop',
      copyPrompt: 'Copy Prompt',
      copyCode: 'Copy Canvas 2D Code',
      prev: '← Prev',
      next: 'Next →',
      close: 'Close ×',
      outIntro: 'I picked these {n} effect(s) from the motion-prompt library. Please apply their motion specs and Canvas 2D reference timing:',
      outDemo: 'Live demo',
      outSpec: 'Spec and code',
      outNote: 'Note',
      outEnd: 'Use `node scripts/motion-prompt.mjs get <id>` from the motion-prompt skill to inspect full specifications.',
    },
  };

  const reduceMotion = window.matchMedia
    ? window.matchMedia('(prefers-reduced-motion: reduce)')
    : { matches: false };

  const state = {
    lang: document.documentElement.lang === 'en' ? 'en' : 'vi',
    pack: 'all',
    cat: 'all',
    q: '',
    playing: !reduceMotion.matches,
    openId: null,
    picks: [],
    note: '',
  };

  const packBy = {};
  const elBy = {};
  const order = [];
  CAT.packs.forEach(p => { packBy[p.pack] = p; });
  CAT.elements.forEach((e, i) => {
    elBy[e.id] = e;
    e._i = i;
    order.push(e.id);
  });

  function t(key, vars) {
    const dict = TEXT[state.lang] || TEXT.vi;
    let s = dict[key] || TEXT.en[key] || key;
    if (vars) {
      Object.keys(vars).forEach(k => {
        s = s.split('{' + k + '}').join(vars[k]);
      });
    }
    return s;
  }

  function packTitle(p, lang) {
    if ((lang || state.lang) === 'vi' && PACK_VI[p.pack]) return PACK_VI[p.pack];
    return p.title.en;
  }

  function catTitle(c, lang) {
    if ((lang || state.lang) === 'vi' && CAT_VI[c.slug]) return CAT_VI[c.slug];
    return c.en;
  }

  function h(tag, attrs, kids) {
    const node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(k => {
        if (k === 'class') node.className = attrs[k];
        else if (k === 'text') node.textContent = attrs[k];
        else node.setAttribute(k, attrs[k]);
      });
    }
    (kids || []).forEach(c => { if (c) node.appendChild(c); });
    return node;
  }

  // Parse pack.js function source on // @kit and // @element NN markers
  const parsedPacks = {};
  function extractElementCode(el) {
    const reg = MP.packs[el.pack];
    if (!reg || !reg.source) return '// Source unavailable';
    if (!parsedPacks[el.pack]) {
      const lines = reg.source.replace(/\r\n/g, '\n').split('\n');
      const blocks = [];
      let cur = null;
      const markRe = /^\s*\/\/ @(kit|shared|end|element (\d{2}))\s*$/;
      lines.forEach(line => {
        const m = markRe.exec(line);
        if (!m) {
          if (cur) cur.lines.push(line);
          return;
        }
        cur = null;
        if (m[1] === 'end') return;
        cur = { type: m[2] ? 'element' : m[1], no: m[2] || null, lines: [line] };
        blocks.push(cur);
      });
      const dedent = arr => arr.map(l => (l.startsWith('  ') ? l.slice(2) : l)).join('\n').trim();
      const kitText = blocks.filter(b => b.type !== 'element').map(b => dedent(b.lines)).join('\n\n');
      const byNo = {};
      blocks.filter(b => b.type === 'element').forEach(b => {
        byNo[b.no] = dedent(b.lines);
      });
      parsedPacks[el.pack] = { kit: kitText, elements: byNo };
    }
    const pData = parsedPacks[el.pack];
    const elCode = pData.elements[el.no] || '';
    return [
      `// Motion Prompt #${el.id} (${el.name.en} / ${el.name.ja}) · pack "${el.pack}" #${el.no}`,
      `// Size: ${el.width}x${el.height} px · Cycle: ${el.cycle}s · Pure Canvas 2D function of time u in [0, ${el.cycle})`,
      '',
      elCode,
      '',
      '// ---------------- Shared pack kit helpers (@kit) ----------------',
      pData.kit,
    ].join('\n');
  }

  // Canvas 2D rendering
  const STILL = 0.4;
  let tiles = [];
  let shown = order.slice();
  let clock = 0;
  let lastNow = 0;
  let rafId = 0;

  const detail = {
    dialog: $('#mp-detail'),
    canvas: $('#mp-d-canvas'),
    ctx: null,
    scale: 1,
    el: null,
    u: 0,
    dirty: false,
  };

  function paintCell(ctx, el, u, scale) {
    const reg = MP.packs[el.pack];
    const cell = reg && reg.cells && reg.cells[Number(el.no) - 1];
    if (!cell || !ctx) return false;
    const w = el.width;
    const hgt = el.height;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.globalAlpha = 1;
    ctx.filter = 'none';
    ctx.globalCompositeOperation = 'source-over';
    ctx.clearRect(0, 0, w * scale, hgt * scale);
    ctx.save();
    if (scale !== 1) ctx.scale(scale, scale);
    try {
      cell(ctx, w, hgt, u);
    } catch (_) {
      ctx.restore();
      return false;
    }
    ctx.restore();
    return true;
  }

  function timeFor(el, offset) {
    const u = (clock + offset * el.cycle) % el.cycle;
    return u < 0 ? u + el.cycle : u;
  }

  function paintDirtySnapshot() {
    if (state.openId && detail.el && detail.dirty) {
      detail.dirty = false;
      paintCell(detail.ctx, detail.el, detail.u, detail.scale);
      return;
    }
    for (let i = 0; i < tiles.length; i++) {
      const tl = tiles[i];
      if (!tl.visible || !tl.dirty || tl.box.hidden) continue;
      tl.dirty = false;
      paintCell(tl.ctx, tl.el, timeFor(tl.el, tl.offset), 1);
    }
  }

  function tick(now) {
    rafId = 0;
    const dt = lastNow ? Math.min((now - lastNow) / 1000, 0.1) : 0;
    lastNow = now;
    if (state.playing) clock += dt;

    if (state.openId && detail.el) {
      if (state.playing || detail.dirty) {
        detail.dirty = false;
        if (state.playing) detail.u = (detail.u + dt) % detail.el.cycle;
        paintCell(detail.ctx, detail.el, detail.u, detail.scale);
      }
    } else {
      for (let i = 0; i < tiles.length; i++) {
        const tl = tiles[i];
        if (!tl.visible || tl.box.hidden) continue;
        if (!state.playing && !tl.dirty) continue;
        tl.dirty = false;
        paintCell(tl.ctx, tl.el, timeFor(tl.el, tl.offset), 1);
      }
    }

    if (state.playing) {
      rafId = requestAnimationFrame(tick);
    }
  }

  function ensureLoop() {
    if (state.playing) {
      if (!rafId) {
        lastNow = 0;
        rafId = requestAnimationFrame(tick);
      }
    } else {
      if (rafId) {
        cancelAnimationFrame(rafId);
        rafId = 0;
      }
      paintDirtySnapshot();
    }
  }

  function markAllDirty() {
    tiles.forEach(tl => { tl.dirty = true; });
    detail.dirty = true;
    ensureLoop();
  }

  const io = 'IntersectionObserver' in window
    ? new IntersectionObserver(entries => {
        entries.forEach(en => {
          const tl = en.target._tile;
          if (!tl) return;
          tl.visible = en.isIntersecting;
          if (tl.visible) {
            tl.dirty = false;
            paintCell(tl.ctx, tl.el, timeFor(tl.el, tl.offset), 1);
          }
        });
      }, { rootMargin: '160px 0px' })
    : null;

  // Build Gallery DOM
  const grid = $('#mp-grid');
  function buildGrid() {
    if (!grid) return;
    if (io) io.disconnect();
    tiles = [];
    grid.textContent = '';

    CAT.packs.forEach(p => {
      const list = h('div', { class: 'mp-tiles' });
      CAT.elements.forEach(el => {
        if (el.pack !== p.pack) return;
        const canvas = h('canvas', { width: el.width, height: el.height, 'aria-hidden': 'true' });
        const stage = h('span', { class: 'mp-tile-stage', style: `aspect-ratio:${el.width}/${el.height}` }, [canvas]);
        const nameEl = h('span', { class: 'mp-tile-name', text: el.name.en });
        const subEl = h('span', {
          class: 'mp-tile-sub',
          text: el.meaning ? el.meaning.en : el.name.ja,
        });
        const btn = h('button', {
          type: 'button',
          class: 'mp-tile',
          'data-id': el.id,
          'aria-label': t('openLabel', { id: el.id, name: el.name.en }),
        }, [
          stage,
          h('span', { class: 'mp-tile-cap' }, [
            h('span', { class: 'mp-tile-id', text: '#' + el.id }),
            nameEl,
            subEl,
          ]),
        ]);

        const pickBtn = h('button', {
          type: 'button',
          class: 'mp-tile-pick',
          'aria-pressed': 'false',
          'data-pick': el.id,
          text: t('pick'),
        });

        const box = h('div', { class: 'mp-tile-box' }, [btn, pickBtn]);
        const tl = {
          el,
          btn,
          box,
          pickBtn,
          nameEl,
          subEl,
          canvas,
          ctx: canvas.getContext('2d'),
          visible: !io,
          dirty: true,
          offset: reduceMotion.matches ? STILL : ((el._i + 1) * 0.6180339887) % 1,
        };
        btn._tile = tl;
        btn.addEventListener('click', () => openDetail(el.id));
        pickBtn.addEventListener('click', ev => {
          ev.stopPropagation();
          togglePick(el.id);
        });
        syncTilePick(tl);
        tiles.push(tl);
        list.appendChild(box);
        if (io) io.observe(btn);
      });

      const titleH3 = h('h3', { id: 'mp-pack-' + p.pack, text: packTitle(p) });
      const sec = h('section', { class: 'mp-pack-section', 'data-pack': p.pack, 'aria-labelledby': 'mp-pack-' + p.pack }, [
        h('div', { class: 'mp-pack-header' }, [
          titleH3,
          h('span', { class: 'mp-pack-range', text: `#${p.first}–#${p.last} · ${p.width}×${p.height}px · ${p.cycle}s` }),
        ]),
        list,
      ]);
      grid.appendChild(sec);
    });

    applyFilter();
    // Paint the first 12 tiles immediately so top-of-gallery previews are visible before scroll
    for (let i = 0; i < Math.min(12, tiles.length); i++) {
      tiles[i].visible = true;
      tiles[i].dirty = false;
      paintCell(tiles[i].ctx, tiles[i].el, timeFor(tiles[i].el, tiles[i].offset), 1);
    }
    ensureLoop();
  }

  function haystack(el) {
    const p = packBy[el.pack];
    const c = p.categories.find(x => x.slug === el.category) || {};
    return [
      '#' + el.id, el.id, String(Number(el.id)), el.slug, el.pack,
      el.name.en, el.name.ja,
      el.meaning ? el.meaning.en + ' ' + el.meaning.ja : '',
      el.summary.en, el.summary.ja,
      el.tags.join(' '),
      p.title.en, PACK_VI[p.pack] || '',
      c.en || '', CAT_VI[el.category] || '',
    ].join(' ').toLowerCase();
  }

  function matches(el) {
    if (state.pack !== 'all' && state.pack.split(',').indexOf(el.pack) < 0) return false;
    if (state.cat !== 'all' && el.category !== state.cat) return false;
    if (!state.q) return true;
    if (!el._hay) el._hay = haystack(el);
    const terms = state.q.toLowerCase().replace(/＃/g, '#').split(/[\s　]+/).filter(Boolean);
    return terms.every(term => {
      if (/^#?\d{1,3}$/.test(term)) {
        const d = term.replace('#', '');
        return el.id === ('000' + d).slice(-3) || (d.length === 3 && el.id === d);
      }
      return el._hay.indexOf(term) >= 0;
    });
  }

  function applyFilter() {
    shown = [];
    tiles.forEach(tl => {
      const ok = matches(tl.el);
      tl.box.hidden = !ok;
      if (ok) shown.push(tl.el.id);
    });
    $$('.mp-pack-section', grid).forEach(sec => {
      sec.hidden = !$('.mp-tile-box:not([hidden])', sec);
    });
    const emptyEl = $('#mp-empty');
    if (emptyEl) emptyEl.hidden = shown.length > 0;
    const countEl = $('#mp-count');
    if (countEl) {
      countEl.textContent = shown.length === CAT.count
        ? t('count', { n: CAT.count })
        : t('countOf', { n: shown.length, total: CAT.count });
    }
    if (!state.playing) paintDirtySnapshot();
  }

  function makeChip(label, pressed, countText, onClick) {
    const b = h('button', {
      type: 'button',
      class: 'mp-chip',
      'aria-pressed': pressed ? 'true' : 'false',
      text: label,
    });
    if (countText) b.appendChild(h('small', { text: countText }));
    b.addEventListener('click', onClick);
    return b;
  }

  function buildChips() {
    const packsWrap = $('#mp-packs');
    const catsWrap = $('#mp-cats');
    if (!packsWrap || !catsWrap) return;
    packsWrap.textContent = '';
    catsWrap.textContent = '';

    packsWrap.appendChild(makeChip(t('all'), state.pack === 'all', String(CAT.count), () => setFilter('all', 'all')));
    CAT.packs.forEach(p => {
      packsWrap.appendChild(makeChip(packTitle(p), state.pack === p.pack, String(p.count), () => setFilter(p.pack, 'all')));
    });

    const p = packBy[state.pack];
    catsWrap.hidden = !p;
    if (!p) return;
    catsWrap.appendChild(makeChip(t('allInPack'), state.cat === 'all', '', () => setFilter(state.pack, 'all')));
    p.categories.forEach(c => {
      catsWrap.appendChild(makeChip(catTitle(c), state.cat === c.slug, '', () => setFilter(state.pack, c.slug)));
    });
  }

  function setFilter(pack, cat) {
    state.pack = pack;
    state.cat = cat;
    buildChips();
    applyFilter();
  }

  // Copy helper
  function copyText(text, btn) {
    const done = ok => {
      if (!btn) return;
      if (!btn._orig) btn._orig = btn.textContent;
      clearTimeout(btn._timer);
      btn.textContent = t(ok ? 'copied' : 'copyFailed');
      btn._timer = setTimeout(() => {
        btn.textContent = btn._orig;
        btn._orig = null;
      }, 1500);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(() => done(true), () => done(false));
    } else {
      const ta = h('textarea', { style: 'position:fixed;opacity:0;pointer-events:none' });
      ta.value = text;
      (detail.dialog && detail.dialog.open ? detail.dialog : document.body).appendChild(ta);
      ta.select();
      let ok = false;
      try { ok = document.execCommand('copy'); } catch (_) { ok = false; }
      ta.remove();
      done(ok);
    }
  }

  // Picks & Tray
  function isPicked(id) {
    return state.picks.indexOf(id) >= 0;
  }

  function syncTilePick(tl) {
    const on = isPicked(tl.el.id);
    tl.box.classList.toggle('is-picked', on);
    tl.pickBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
    tl.pickBtn.setAttribute('aria-label', t('pickLabel', { id: tl.el.id, name: tl.el.name.en }));
    tl.pickBtn.textContent = t(on ? 'picked' : 'pick');
  }

  function syncDetailPick() {
    const btn = $('#mp-d-pick');
    if (!btn || !detail.el) return;
    const on = isPicked(detail.el.id);
    btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    btn.textContent = t(on ? 'picked' : 'pick');
  }

  function togglePick(id) {
    const idx = state.picks.indexOf(id);
    if (idx >= 0) state.picks.splice(idx, 1);
    else state.picks.push(id);
    tiles.forEach(tl => { if (tl.el.id === id) syncTilePick(tl); });
    syncDetailPick();
    renderTray();
  }

  function renderTray() {
    const tray = $('#mp-tray');
    const list = $('#mp-tray-list');
    const title = $('#mp-tray-title');
    if (!tray || !list || !title) return;
    const n = state.picks.length;
    tray.hidden = n === 0;
    title.textContent = t('trayTitle', { n });
    list.textContent = '';
    state.picks.forEach(id => {
      const el = elBy[id];
      if (!el) return;
      const item = h('li', { class: 'mp-tray-item' }, [
        h('strong', { text: '#' + id }),
        h('span', { text: el.name.en }),
      ]);
      const rm = h('button', { type: 'button', 'aria-label': 'Remove #' + id, text: '×' });
      rm.addEventListener('click', () => togglePick(id));
      item.appendChild(rm);
      list.appendChild(item);
    });
  }

  function buildPickedPrompt() {
    const lines = [t('outIntro', { n: state.picks.length }), ''];
    state.picks.forEach((id, i) => {
      const el = elBy[id];
      const p = packBy[el.pack];
      lines.push(`${i + 1}. #${id} ${el.name.en} (${el.name.ja}) — ${p.title.en}`);
      lines.push(`   Summary: ${el.summary.en}`);
      lines.push(`   Spec: ${el.spec.en.join(' | ')}`);
      lines.push(`   ${t('outSpec')}: https://showheyohtaki.github.io/motion-prompt/api/v1/en/e/${id}.txt`);
    });
    if (state.note.trim()) {
      lines.push('', `${t('outNote')}: ${state.note.trim()}`);
    }
    lines.push('', t('outEnd'));
    return lines.join('\n');
  }

  // Detail Modal
  let lastFocus = null;
  function sizeDetailCanvas() {
    const el = detail.el;
    if (!el || !detail.canvas) return;
    const cssW = detail.canvas.parentNode.clientWidth || el.width;
    const want = Math.ceil(cssW * (window.devicePixelRatio || 1) / el.width);
    const scale = packBy[el.pack].scalable ? Math.max(1, Math.min(2, want)) : 1;
    detail.canvas.width = el.width * scale;
    detail.canvas.height = el.height * scale;
    detail.scale = scale;
    detail.dirty = true;
    paintCell(detail.ctx, detail.el, detail.u, detail.scale);
    ensureLoop();
  }

  function fillDetail(el) {
    const p = packBy[el.pack];
    const c = p.categories.find(x => x.slug === el.category);
    detail.el = el;
    detail.u = STILL * el.cycle;
    detail.ctx = detail.canvas.getContext('2d');
    detail.canvas.style.aspectRatio = `${el.width}/${el.height}`;

    $('#mp-d-id').textContent = '#' + el.id;
    $('#mp-d-where').textContent = packTitle(p) + (c ? ' / ' + catTitle(c) : '');
    $('#mp-d-name').textContent = `${el.name.en} (${el.name.ja})`;
    $('#mp-d-sub').textContent = `${el.slug} · ` + t('size', { w: el.width, h: el.height, c: el.cycle });
    $('#mp-d-meaning').textContent = el.meaning ? el.meaning.en : '';
    $('#mp-d-summary').textContent = el.summary.en;
    $('#mp-d-ask').textContent = el.ask ? el.ask.en : '';

    const specList = $('#mp-d-spec');
    specList.textContent = '';
    el.spec.en.forEach(s => specList.appendChild(h('li', { text: s })));

    $('#mp-d-use').textContent = el.use.en;

    const tagsList = $('#mp-d-tags');
    tagsList.textContent = '';
    el.tags.forEach(tag => tagsList.appendChild(h('li', { text: tag })));

    $('#mp-d-prompt').textContent = PROMPT(el, p.title.en, 'en');
    $('#mp-d-code').textContent = extractElementCode(el);

    const list = shown.indexOf(el.id) >= 0 ? shown : order;
    const idx = list.indexOf(el.id);
    const prevBtn = $('#mp-d-prev');
    const nextBtn = $('#mp-d-next');
    prevBtn.disabled = idx <= 0;
    nextBtn.disabled = idx >= list.length - 1;
    prevBtn._to = list[idx - 1];
    nextBtn._to = list[idx + 1];

    syncDetailPick();
    sizeDetailCanvas();
  }

  function openDetail(id) {
    const el = elBy[id];
    if (!el || !detail.dialog) return;
    const first = !detail.dialog.open;
    state.openId = id;
    fillDetail(el);
    if (first) {
      lastFocus = document.activeElement;
      if (detail.dialog.showModal) detail.dialog.showModal();
      else detail.dialog.setAttribute('open', '');
    }
    sizeDetailCanvas();
  }

  function closeDetail() {
    if (!state.openId && (!detail.dialog || !detail.dialog.open)) return;
    state.openId = null;
    detail.el = null;
    if (detail.dialog && detail.dialog.open) {
      if (detail.dialog.close) detail.dialog.close();
      else detail.dialog.removeAttribute('open');
    }
    markAllDirty();
    if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
  }

  function syncPlayButtons() {
    const playBtn = $('#mp-play-toggle');
    if (!playBtn) return;
    playBtn.setAttribute('aria-pressed', state.playing ? 'true' : 'false');
    playBtn.setAttribute('aria-label', t(state.playing ? 'pauseAria' : 'playAria'));
    playBtn.textContent = state.playing ? '⏸ ' + t('pause') : '▶ ' + t('play');
  }

  function syncLanguageUI() {
    state.lang = document.documentElement.lang === 'en' ? 'en' : 'vi';
    const searchInput = $('#mp-q');
    if (searchInput) searchInput.placeholder = t('searchPh');
    const noteInput = $('#mp-tray-note');
    if (noteInput) noteInput.placeholder = t('notePh');
    const copyPicksBtn = $('#mp-tray-copy');
    if (copyPicksBtn) copyPicksBtn.textContent = t('copyPicks');
    const clearPicksBtn = $('#mp-tray-clear');
    if (clearPicksBtn) clearPicksBtn.textContent = t('clearPicks');
    const copyPromptBtn = $('#mp-d-copy-prompt');
    if (copyPromptBtn) copyPromptBtn.textContent = t('copyPrompt');
    const copyCodeBtn = $('#mp-d-copy-code');
    if (copyCodeBtn) copyCodeBtn.textContent = t('copyCode');
    const prevBtn = $('#mp-d-prev');
    if (prevBtn) prevBtn.textContent = t('prev');
    const nextBtn = $('#mp-d-next');
    if (nextBtn) nextBtn.textContent = t('next');
    const closeBtn = $('#mp-d-close');
    if (closeBtn) closeBtn.textContent = t('close');

    CAT.packs.forEach(p => {
      const h3 = $('#mp-pack-' + p.pack);
      if (h3) h3.textContent = packTitle(p);
    });
    tiles.forEach(syncTilePick);
    buildChips();
    applyFilter();
    syncPlayButtons();
    renderTray();
    if (state.openId && elBy[state.openId]) fillDetail(elBy[state.openId]);
  }

  // Event Listeners
  const searchInput = $('#mp-q');
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      state.q = searchInput.value.trim();
      applyFilter();
    });
  }

  const playToggle = $('#mp-play-toggle');
  if (playToggle) {
    playToggle.addEventListener('click', () => {
      state.playing = !state.playing;
      syncPlayButtons();
      ensureLoop();
    });
  }

  const trayCopy = $('#mp-tray-copy');
  if (trayCopy) {
    trayCopy.addEventListener('click', function () {
      if (state.picks.length) copyText(buildPickedPrompt(), this);
    });
  }

  const trayClear = $('#mp-tray-clear');
  if (trayClear) {
    trayClear.addEventListener('click', () => {
      state.picks = [];
      tiles.forEach(syncTilePick);
      syncDetailPick();
      renderTray();
    });
  }

  const trayNote = $('#mp-tray-note');
  if (trayNote) {
    trayNote.addEventListener('input', () => {
      state.note = trayNote.value;
    });
  }

  if (detail.dialog) {
    detail.dialog.addEventListener('cancel', ev => {
      ev.preventDefault();
      closeDetail();
    });
    detail.dialog.addEventListener('click', ev => {
      if (ev.target === detail.dialog) closeDetail();
    });
    $('#mp-d-close')?.addEventListener('click', closeDetail);
    $('#mp-d-prev')?.addEventListener('click', function () {
      if (this._to) openDetail(this._to);
    });
    $('#mp-d-next')?.addEventListener('click', function () {
      if (this._to) openDetail(this._to);
    });
    $('#mp-d-pick')?.addEventListener('click', () => {
      if (detail.el) togglePick(detail.el.id);
    });
    $('#mp-d-copy-prompt')?.addEventListener('click', function () {
      copyText($('#mp-d-prompt').textContent, this);
    });
    $('#mp-d-copy-code')?.addEventListener('click', function () {
      copyText($('#mp-d-code').textContent, this);
    });
  }

  window.addEventListener('resize', () => {
    if (state.openId) sizeDetailCanvas();
  });

  // Observe <html lang="..."> changes triggered by #blog-language
  if ('MutationObserver' in window) {
    new MutationObserver(() => {
      const newLang = document.documentElement.lang === 'en' ? 'en' : 'vi';
      if (newLang !== state.lang) syncLanguageUI();
    }).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
  }

  buildGrid();
  syncLanguageUI();
})();
