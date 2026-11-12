(function () {
  'use strict';

  const cards = window.SHOTCRAFT_CARDS || [];
  if (!cards.length) return;

  const state = {
    category: 'all',
    search: '',
    picked: new Set(),
    playing: !window.matchMedia('(prefers-reduced-motion: reduce)').matches,
    currentModalCard: null,
    modalProgress: 0,
    modalSpeed: 1,
    modalPlaying: true,
  };

  const elements = {
    grid: document.getElementById('sc-grid'),
    search: document.getElementById('sc-search'),
    count: document.getElementById('sc-count'),
    chips: document.getElementById('sc-chips'),
    tray: document.getElementById('sc-tray'),
    trayList: document.getElementById('sc-tray-list'),
    trayCount: document.getElementById('sc-tray-count'),
    trayClear: document.getElementById('sc-tray-clear'),
    trayCopy: document.getElementById('sc-tray-copy'),
    playToggle: document.getElementById('sc-play-toggle'),
    modal: document.getElementById('sc-modal'),
    modalTitle: document.getElementById('sc-modal-title'),
    modalCanvas: document.getElementById('sc-modal-canvas'),
    modalPlay: document.getElementById('sc-modal-play'),
    modalScrubber: document.getElementById('sc-modal-scrubber'),
    modalSpeed: document.getElementById('sc-modal-speed'),
    modalSpec: document.getElementById('sc-modal-spec'),
    modalCopy: document.getElementById('sc-modal-copy'),
    modalClose: document.getElementById('sc-modal-close'),
    toast: document.getElementById('sc-toast'),
  };

  const categoryNames = {
    all: { vi: 'Tất cả', en: 'All' },
    opening: { vi: 'Mở đầu & Brand', en: 'Opening & Brand' },
    camera: { vi: 'Camera & 3D', en: 'Camera & 3D' },
    'ui-entrance': { vi: 'Xuất hiện UI', en: 'UI Entrance' },
    typography: { vi: 'Chữ & Typography', en: 'Typography' },
    interaction: { vi: 'Tương tác UI', en: 'Interaction' },
    data: { vi: 'Biểu đồ & Số liệu', en: 'Data & Metrics' },
    transition: { vi: 'Chuyển cảnh', en: 'Transitions' },
    rhythm: { vi: 'Nhịp điệu & Cắt', en: 'Rhythm' },
    effects: { vi: 'Ánh sáng & Điểm nhấn', en: 'Light & Effects' },
    outro: { vi: 'Kết thúc & Outro', en: 'Outro' },
  };

  function showToast(msg) {
    if (!elements.toast) return;
    elements.toast.textContent = msg;
    elements.toast.classList.add('is-active');
    setTimeout(() => elements.toast.classList.remove('is-active'), 2500);
  }

  function getLang() {
    return document.documentElement.lang === 'en' ? 'en' : 'vi';
  }

  // Animation Archetypes Engine
  function drawArchetype(ctx, width, height, archetype, progress, themeDark) {
    ctx.clearRect(0, 0, width, height);

    // Background
    ctx.fillStyle = themeDark ? '#0d1117' : '#f6f8fa';
    ctx.fillRect(0, 0, width, height);

    const cx = width / 2;
    const cy = height / 2;
    const p = progress % 1;

    switch (archetype) {
      case 'spotlight': {
        // Spotlight cone sweeping and locking onto card
        const sweep = Math.sin(p * Math.PI * 2);
        const spotX = cx + sweep * (width * 0.25);
        const grad = ctx.createRadialGradient(spotX, cy * 0.6, 10, spotX, cy * 0.8, width * 0.5);
        grad.addColorStop(0, 'rgba(255, 220, 150, 0.45)');
        grad.addColorStop(0.5, 'rgba(255, 200, 100, 0.15)');
        grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, width, height);

        // Card lifting
        const lift = Math.sin(p * Math.PI) * 12;
        const cardW = width * 0.5;
        const cardH = height * 0.45;
        const cardX = cx - cardW / 2;
        const cardY = cy - cardH / 2 - lift;

        // Shadow
        ctx.fillStyle = themeDark ? 'rgba(0,0,0,0.6)' : 'rgba(0,0,0,0.15)';
        ctx.beginPath();
        ctx.roundRect(cardX, cardY + lift * 1.5, cardW, cardH, 8);
        ctx.fill();

        // Card body
        ctx.fillStyle = themeDark ? '#161b22' : '#ffffff';
        ctx.strokeStyle = '#d4af37';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.roundRect(cardX, cardY, cardW, cardH, 8);
        ctx.fill();
        ctx.stroke();

        // Outline beam
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.9)';
        ctx.lineWidth = 3;
        ctx.setLineDash([20, cardW * 2]);
        ctx.lineDashOffset = -p * cardW * 4;
        ctx.beginPath();
        ctx.roundRect(cardX, cardY, cardW, cardH, 8);
        ctx.stroke();
        ctx.setLineDash([]);
        break;
      }

      case 'camera3d': {
        // 3D perspective panels
        const angle = Math.sin(p * Math.PI * 2) * 0.25;
        ctx.save();
        ctx.translate(cx, cy);

        // Ground perspective grid
        ctx.strokeStyle = themeDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)';
        ctx.lineWidth = 1;
        for (let i = -4; i <= 4; i++) {
          ctx.beginPath();
          ctx.moveTo(i * 30, 20);
          ctx.lineTo(i * 70, height / 2);
          ctx.stroke();
        }

        // Panel 1, 2, 3
        [-1, 0, 1].forEach((idx) => {
          ctx.save();
          const offsetX = idx * 60 + Math.sin(p * Math.PI * 2 + idx) * 15;
          const offsetY = idx * 10 - 20;
          ctx.translate(offsetX, offsetY);
          ctx.rotate(angle);
          ctx.fillStyle = themeDark ? (idx === 0 ? '#1f6feb' : '#21262d') : (idx === 0 ? '#0969da' : '#eaeef2');
          ctx.beginPath();
          ctx.roundRect(-25, -35, 50, 70, 6);
          ctx.fill();
          ctx.restore();
        });
        ctx.restore();
        break;
      }

      case 'deck': {
        // Poker deal fly-in
        const count = 4;
        for (let i = 0; i < count; i++) {
          const delay = i * 0.2;
          const cardP = Math.max(0, Math.min(1, (p - delay) / 0.4));
          const ease = 1 - Math.pow(1 - cardP, 3);
          const startX = -60;
          const targetX = cx - 75 + i * 45;
          const x = startX + (targetX - startX) * ease;
          const y = cy - 25 + Math.sin(i + p * Math.PI) * 4;

          ctx.fillStyle = themeDark ? '#30363d' : '#d0d7de';
          ctx.beginPath();
          ctx.roundRect(x, y, 40, 55, 4);
          ctx.fill();
          ctx.strokeStyle = i === 2 ? '#2ea043' : (themeDark ? '#484f58' : '#8c959f');
          ctx.lineWidth = 1.5;
          ctx.stroke();
        }
        break;
      }

      case 'slam': {
        // Kinetic typography slam
        const slamP = Math.min(1, p / 0.4);
        const scale = 2.5 - 1.5 * (1 - Math.pow(1 - slamP, 4));
        const shake = p < 0.45 ? (Math.random() - 0.5) * 6 : 0;

        ctx.save();
        ctx.translate(cx + shake, cy + shake);
        ctx.scale(scale, scale);
        ctx.fillStyle = themeDark ? '#f0f6fc' : '#1f2328';
        ctx.font = 'bold 22px system-ui, -apple-system, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('CINEMATIC', 0, -8);
        ctx.fillStyle = '#0070f3';
        ctx.font = 'bold 12px system-ui, -apple-system, sans-serif';
        ctx.letterSpacing = `${(1 - slamP) * 10}px`;
        ctx.fillText('REMOTION SHOT', 0, 14);
        ctx.restore();
        break;
      }

      case 'counter': {
        // Rolling odometer & graph curve
        const val = Math.floor(p * 9999);
        ctx.fillStyle = themeDark ? '#58a6ff' : '#0969da';
        ctx.font = 'bold 28px monospace';
        ctx.textAlign = 'center';
        ctx.fillText(`+${val.toLocaleString()}`, cx, cy - 10);

        // Oscilloscope wave below
        ctx.strokeStyle = themeDark ? '#3fb950' : '#1a7f37';
        ctx.lineWidth = 2;
        ctx.beginPath();
        for (let x = 30; x < width - 30; x += 4) {
          const y = cy + 25 + Math.sin((x * 0.08) + p * Math.PI * 4) * 12 * Math.sin(p * Math.PI);
          if (x === 30) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
        break;
      }

      case 'click': {
        // Cursor movement, click, ripple
        const cursorP = Math.sin(p * Math.PI);
        const curX = cx - 40 + cursorP * 50;
        const curY = cy - 20 + cursorP * 30;

        // Target button
        const isClick = p > 0.45 && p < 0.65;
        ctx.fillStyle = isClick ? '#238636' : (themeDark ? '#21262d' : '#eaeef2');
        ctx.beginPath();
        ctx.roundRect(cx - 35, cy - 15, 70, 30, 6);
        ctx.fill();

        // Button text
        ctx.fillStyle = isClick ? '#fff' : (themeDark ? '#c9d1d9' : '#24292f');
        ctx.font = '10px system-ui';
        ctx.textAlign = 'center';
        ctx.fillText(isClick ? 'ACTIVE' : 'ACTION', cx, cy + 4);

        // Ripple
        if (p > 0.5) {
          const ripP = (p - 0.5) / 0.5;
          ctx.strokeStyle = `rgba(35, 134, 54, ${1 - ripP})`;
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.arc(cx, cy, ripP * 40, 0, Math.PI * 2);
          ctx.stroke();
        }

        // Mouse pointer arrow
        ctx.fillStyle = '#fff';
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(curX, curY);
        ctx.lineTo(curX, curY + 14);
        ctx.lineTo(curX + 4, curY + 10);
        ctx.lineTo(curX + 8, curY + 16);
        ctx.lineTo(curX + 11, curY + 15);
        ctx.lineTo(curX + 7, curY + 9);
        ctx.lineTo(curX + 12, curY + 9);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        break;
      }

      case 'flip': {
        // 3D Card flip 180 deg
        const flipAngle = p * Math.PI * 2;
        const cosA = Math.cos(flipAngle);
        const cardW = 90 * Math.abs(cosA);
        const cardH = 110;

        ctx.save();
        ctx.translate(cx, cy);

        // Specular gleam
        const isFront = cosA > 0;
        ctx.fillStyle = isFront ? (themeDark ? '#1f6feb' : '#0969da') : (themeDark ? '#238636' : '#1a7f37');
        ctx.beginPath();
        ctx.roundRect(-cardW / 2, -cardH / 2, cardW, cardH, 6);
        ctx.fill();

        if (cardW > 20) {
          ctx.fillStyle = '#fff';
          ctx.font = 'bold 12px system-ui';
          ctx.textAlign = 'center';
          ctx.fillText(isFront ? 'FRONT' : 'REVEAL', 0, 4);
        }

        // Edge shine
        if (Math.abs(cosA) < 0.2) {
          ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
          ctx.fillRect(-2, -cardH / 2, 4, cardH);
        }
        ctx.restore();
        break;
      }

      case 'beat': {
        // Rapid rhythm cuts and white freeze flash
        const beatIndex = Math.floor(p * 4);
        const flash = (p * 4) % 1 < 0.15;

        if (flash) {
          ctx.fillStyle = '#ffffff';
          ctx.fillRect(0, 0, width, height);
        } else {
          ctx.fillStyle = themeDark ? '#161b22' : '#ffffff';
          ctx.fillRect(10, 10, width - 20, height - 20);

          // Alternating visual composition per beat
          ctx.fillStyle = ['#f85149', '#a371f7', '#388bfd', '#3fb950'][beatIndex];
          ctx.font = 'bold 36px monospace';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(`BEAT ${beatIndex + 1}`, cx, cy);
        }
        break;
      }

      case 'aurora': {
        // Shifting aurora bloom
        const t = p * Math.PI * 2;
        const grad = ctx.createLinearGradient(0, height, width, 0);
        grad.addColorStop(0, `hsl(${(t * 50 + 260) % 360}, 85%, 55%)`);
        grad.addColorStop(0.5, `hsl(${(t * 50 + 320) % 360}, 80%, 50%)`);
        grad.addColorStop(1, `hsl(${(t * 50 + 40) % 360}, 90%, 60%)`);
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, width, height);

        // Dark overlay panel
        ctx.fillStyle = themeDark ? 'rgba(13, 17, 23, 0.85)' : 'rgba(255, 255, 255, 0.85)';
        ctx.beginPath();
        ctx.roundRect(cx - 90, cy - 45, 180, 90, 10);
        ctx.fill();
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.stroke();

        ctx.fillStyle = themeDark ? '#fff' : '#000';
        ctx.font = 'bold 13px system-ui';
        ctx.textAlign = 'center';
        ctx.fillText('AURORA BLOOM', cx, cy + 4);
        break;
      }

      case 'lockup':
      default: {
        // Logo lockup settle
        const lockP = Math.min(1, p / 0.5);
        const ease = 1 - Math.pow(1 - lockP, 3);
        const alpha = ease;

        ctx.save();
        ctx.globalAlpha = alpha;
        ctx.fillStyle = '#0070f3';
        ctx.beginPath();
        ctx.arc(cx, cy - 14, 18, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#fff';
        ctx.font = 'bold 14px monospace';
        ctx.textAlign = 'center';
        ctx.fillText('VS', cx, cy - 9);

        ctx.fillStyle = themeDark ? '#f0f6fc' : '#1f2328';
        ctx.font = 'bold 15px system-ui';
        ctx.fillText('video-shotcraft', cx, cy + 20);
        ctx.restore();
        break;
      }
    }
  }

  // Animation Loop for Active Cards
  let animationFrameId;
  let startTime = performance.now();

  function animate(now) {
    if (!state.playing) return;
    const elapsed = (now - startTime) / 1000;
    const isDark = document.documentElement.dataset.theme === 'dark';

    // Update small card previews
    const canvases = document.querySelectorAll('.sc-card-canvas');
    canvases.forEach((cvs) => {
      const archetype = cvs.dataset.archetype || 'spotlight';
      const ctx = cvs.getContext('2d');
      const progress = (elapsed * 0.4) % 1;
      drawArchetype(ctx, cvs.width, cvs.height, archetype, progress, isDark);
    });

    // Update modal stage if open
    if (state.currentModalCard && elements.modalCanvas && state.modalPlaying) {
      state.modalProgress = (state.modalProgress + 0.008 * state.modalSpeed) % 1;
      if (elements.modalScrubber) elements.modalScrubber.value = Math.floor(state.modalProgress * 100);
      const mCtx = elements.modalCanvas.getContext('2d');
      drawArchetype(mCtx, elements.modalCanvas.width, elements.modalCanvas.height, state.currentModalCard.archetype, state.modalProgress, isDark);
    }

    animationFrameId = requestAnimationFrame(animate);
  }

  function startAnimation() {
    state.playing = true;
    if (elements.playToggle) elements.playToggle.textContent = getLang() === 'vi' ? '⏸ Tạm dừng' : '⏸ Pause';
    animationFrameId = requestAnimationFrame(animate);
  }

  function stopAnimation() {
    state.playing = false;
    cancelAnimationFrame(animationFrameId);
    if (elements.playToggle) elements.playToggle.textContent = getLang() === 'vi' ? '▶ Tiếp tục' : '▶ Play';
  }

  // Filtering & Rendering
  function renderChips() {
    if (!elements.chips) return;
    const lang = getLang();
    const categories = ['all', 'opening', 'camera', 'ui-entrance', 'typography', 'interaction', 'data', 'transition', 'rhythm', 'effects', 'outro'];
    elements.chips.innerHTML = categories.map((cat) => {
      const count = cat === 'all' ? cards.length : cards.filter((c) => c.category === cat).length;
      const label = categoryNames[cat]?.[lang] || cat;
      const active = state.category === cat ? ' is-active' : '';
      return `<button type="button" class="sc-chip${active}" data-sc-cat="${cat}">
        <span>${label}</span>
        <span class="sc-chip-count">(${count})</span>
      </button>`;
    }).join('');

    elements.chips.querySelectorAll('.sc-chip').forEach((btn) => {
      btn.addEventListener('click', () => {
        state.category = btn.dataset.scCat;
        renderChips();
        renderGrid();
      });
    });
  }

  function filterCards() {
    const q = state.search.trim().toLowerCase();
    return cards.filter((card) => {
      if (state.category !== 'all' && card.category !== state.category) return false;
      if (!q) return true;
      return card.name.toLowerCase().includes(q) ||
        card.category.toLowerCase().includes(q) ||
        (card.summary_vi && card.summary_vi.toLowerCase().includes(q)) ||
        (card.summary_en && card.summary_en.toLowerCase().includes(q));
    });
  }

  function renderGrid() {
    if (!elements.grid) return;
    const lang = getLang();
    const filtered = filterCards();

    if (elements.count) {
      elements.count.textContent = lang === 'vi' ? `${filtered.length} shot card` : `${filtered.length} shot cards`;
    }

    if (!filtered.length) {
      elements.grid.innerHTML = `<p style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 3rem 1rem;">
        ${lang === 'vi' ? 'Không tìm thấy shot card phù hợp.' : 'No matching shot cards found.'}
      </p>`;
      return;
    }

    elements.grid.innerHTML = filtered.map((card) => {
      const isPicked = state.picked.has(card.id);
      const summary = lang === 'en' ? (card.summary_en || card.summary_zh) : (card.summary_vi || card.summary_zh);
      const catLabel = categoryNames[card.category]?.[lang] || card.category;
      const energyClass = card.energy === 'high' ? 'sc-badge-energy-high' : 'sc-badge-energy-med';

      return `<article class="sc-card${isPicked ? ' is-picked' : ''}" id="sc-card-${card.id}">
        <div class="sc-card-preview">
          <canvas class="sc-card-canvas" width="280" height="158" data-archetype="${card.archetype}"></canvas>
          <div class="sc-card-meta-bar">
            <span class="sc-badge sc-badge-cat">${catLabel}</span>
            <span class="sc-badge sc-badge-dur ${energyClass}">${card.duration.split('（')[0].trim()}</span>
          </div>
        </div>
        <div class="sc-card-body">
          <h3 class="sc-card-title">${card.name}</h3>
          <p class="sc-card-desc">${summary}</p>
          <div class="sc-card-actions">
            <button type="button" class="sc-btn sc-btn-sm sc-btn-pick" data-sc-pick="${card.id}">
              ${isPicked ? (lang === 'vi' ? '✓ Đã chọn' : '✓ Selected') : (lang === 'vi' ? '+ Chọn' : '+ Pick')}
            </button>
            <button type="button" class="sc-btn sc-btn-sm sc-btn-inspect" data-sc-inspect="${card.id}">
              ${lang === 'vi' ? 'Chi tiết' : 'Inspect'}
            </button>
            <button type="button" class="sc-btn sc-btn-sm sc-btn-copy" data-sc-copy="${card.id}">
              ${lang === 'vi' ? 'Prompt' : 'Prompt'}
            </button>
          </div>
        </div>
      </article>`;
    }).join('');

    // Attach card event listeners
    elements.grid.querySelectorAll('.sc-btn-pick').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        togglePick(btn.dataset.scPick);
      });
    });

    elements.grid.querySelectorAll('.sc-btn-inspect').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        openModal(btn.dataset.scInspect);
      });
    });

    elements.grid.querySelectorAll('.sc-btn-copy').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        copySinglePrompt(btn.dataset.scCopy);
      });
    });
  }

  // Tray management
  function togglePick(id) {
    if (state.picked.has(id)) {
      state.picked.delete(id);
    } else {
      state.picked.add(id);
    }
    updateTray();
    renderGrid();
  }

  function updateTray() {
    if (!elements.tray) return;
    const lang = getLang();
    const count = state.picked.size;
    elements.tray.hidden = count === 0;

    if (elements.trayCount) {
      elements.trayCount.textContent = lang === 'vi' ? `Kịch bản đã chọn: ${count} shot` : `Storyboard: ${count} shots selected`;
    }

    if (elements.trayList) {
      elements.trayList.innerHTML = Array.from(state.picked).map((id, index) => {
        return `<li class="sc-tray-item">
          <span><strong>#${index + 1}</strong> ${id}</span>
          <button type="button" data-sc-remove="${id}" aria-label="Remove ${id}">×</button>
        </li>`;
      }).join('');

      elements.trayList.querySelectorAll('[data-sc-remove]').forEach((btn) => {
        btn.addEventListener('click', () => togglePick(btn.dataset.scRemove));
      });
    }
  }

  function copySinglePrompt(id) {
    const card = cards.find((c) => c.id === id);
    if (!card) return;
    const lang = getLang();
    const summary = lang === 'en' ? (card.summary_en || card.summary_zh) : (card.summary_vi || card.summary_zh);

    const prompt = lang === 'vi'
      ? `Tôi muốn tạo một phân cảnh video sản phẩm điện ảnh bằng Remotion sử dụng skill video-shotcraft (cài đặt: ./vas install video-shotcraft --target workspace --mode link).
Hãy áp dụng shot card: "${card.name}" (${card.category}).
Thời lượng: ${card.duration}. Mức năng lượng: ${card.energy}.
Mô tả hiệu ứng: ${summary}.
Yêu cầu: Thiết lập PageCam 2.5D, căn nhịp theo âm thanh và đảm bảo render xác định.`
      : `I want to build a cinematic product video shot using Remotion with the video-shotcraft skill (install: ./vas install video-shotcraft --target workspace --mode link).
Please implement shot card: "${card.name}" (${card.category}).
Duration: ${card.duration}. Energy level: ${card.energy}.
Effect description: ${summary}.
Requirements: Setup 2.5D PageCam, synchronize with beat audio transients, and ensure deterministic rendering.`;

    navigator.clipboard.writeText(prompt).then(() => {
      showToast(lang === 'vi' ? `Đã sao chép prompt cho shot ${card.name}!` : `Copied prompt for ${card.name}!`);
    });
  }

  function copyStoryboardPrompt() {
    if (!state.picked.size) return;
    const lang = getLang();
    const pickedCards = Array.from(state.picked).map((id) => cards.find((c) => c.id === id)).filter(Boolean);

    let prompt = '';
    if (lang === 'vi') {
      prompt = `Tôi muốn tạo video quảng cáo sản phẩm hoàn chỉnh bằng Remotion với kịch bản đa phân cảnh từ skill video-shotcraft (cài đặt: ./vas install video-shotcraft --target workspace --mode link).\n\nDanh sách phân cảnh (Storyboard Sequence):\n`;
      pickedCards.forEach((c, idx) => {
        prompt += `${idx + 1}. [${c.name}] (${c.category}) - Thời lượng: ${c.duration} - Mô tả: ${c.summary_vi || c.summary_zh}\n`;
      });
      prompt += `\nHướng dẫn kỹ thuật:\n- Sử dụng kiến trúc 2.5D PageCam để điều hướng camera quanh giao diện thực tế.\n- Thiết lập BGM và căn nhịp cắt cảnh theo beat trống (librosa transients).\n- Cấu hình workbench.ts để hỗ trợ xem lại và tinh chỉnh visual timeline.\n- Render video hoàn chỉnh không dùng Math.random/Date.now.`;
    } else {
      prompt = `I want to build a complete cinematic product promo video using Remotion with a multi-shot sequence from the video-shotcraft skill (install: ./vas install video-shotcraft --target workspace --mode link).\n\nStoryboard Sequence:\n`;
      pickedCards.forEach((c, idx) => {
        prompt += `${idx + 1}. [${c.name}] (${c.category}) - Duration: ${c.duration} - Description: ${c.summary_en || c.summary_zh}\n`;
      });
      prompt += `\nTechnical Instructions:\n- Use 2.5D PageCam architecture to navigate the camera around the real product interface.\n- Align cut points and camera impacts to BGM drum transients.\n- Generate workbench.ts for visual timeline inspection and interactive polish.\n- Ensure deterministic Remotion rendering without Math.random or Date.now.`;
    }

    navigator.clipboard.writeText(prompt).then(() => {
      showToast(lang === 'vi' ? 'Đã sao chép prompt kịch bản toàn diện!' : 'Copied full storyboard prompt!');
    });
  }

  // Modal inspection
  function openModal(id) {
    const card = cards.find((c) => c.id === id);
    if (!card || !elements.modal) return;
    state.currentModalCard = card;
    state.modalProgress = 0;
    state.modalPlaying = true;

    const lang = getLang();
    const summary = lang === 'en' ? (card.summary_en || card.summary_zh) : (card.summary_vi || card.summary_zh);
    const catLabel = categoryNames[card.category]?.[lang] || card.category;

    if (elements.modalTitle) elements.modalTitle.textContent = `${card.name} (${catLabel})`;

    if (elements.modalSpec) {
      elements.modalSpec.innerHTML = `
        <table class="sc-spec-table">
          <tr><th>${lang === 'vi' ? 'Tên shot' : 'Shot ID'}</th><td><code>${card.name}</code></td></tr>
          <tr><th>${lang === 'vi' ? 'Chuyên mục' : 'Category'}</th><td>${catLabel}</td></tr>
          <tr><th>${lang === 'vi' ? 'Thời lượng' : 'Duration'}</th><td>${card.duration}</td></tr>
          <tr><th>${lang === 'vi' ? 'Mức năng lượng' : 'Energy'}</th><td>${card.energy.toUpperCase()}</td></tr>
          <tr><th>${lang === 'vi' ? 'Mô tả chi tiết' : 'Description'}</th><td>${summary}</td></tr>
          <tr><th>${lang === 'vi' ? 'Mã mẫu Remotion' : 'Remotion Demo'}</th><td><code>demos/${card.category}/${card.id}/</code></td></tr>
          <tr><th>${lang === 'vi' ? 'Cài đặt qua VAS' : 'VAS Command'}</th><td><code>./vas install video-shotcraft --target workspace --mode link</code></td></tr>
        </table>
      `;
    }

    elements.modal.showModal();
  }

  function closeModal() {
    if (elements.modal) {
      elements.modal.close();
      state.currentModalCard = null;
    }
  }

  // Initialization
  function init() {
    renderChips();
    renderGrid();
    startAnimation();

    if (elements.search) {
      elements.search.addEventListener('input', (e) => {
        state.search = e.target.value;
        renderGrid();
      });
      window.addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
          e.preventDefault();
          elements.search.focus();
        }
      });
    }

    if (elements.playToggle) {
      elements.playToggle.addEventListener('click', () => {
        if (state.playing) stopAnimation();
        else startAnimation();
      });
    }

    if (elements.trayClear) {
      elements.trayClear.addEventListener('click', () => {
        state.picked.clear();
        updateTray();
        renderGrid();
      });
    }

    if (elements.trayCopy) {
      elements.trayCopy.addEventListener('click', copyStoryboardPrompt);
    }

    if (elements.modalClose) {
      elements.modalClose.addEventListener('click', closeModal);
    }

    if (elements.modal) {
      elements.modal.addEventListener('click', (e) => {
        if (e.target === elements.modal) closeModal();
      });
    }

    if (elements.modalPlay) {
      elements.modalPlay.addEventListener('click', () => {
        state.modalPlaying = !state.modalPlaying;
        elements.modalPlay.textContent = state.modalPlaying ? '⏸' : '▶';
      });
    }

    if (elements.modalScrubber) {
      elements.modalScrubber.addEventListener('input', (e) => {
        state.modalProgress = parseInt(e.target.value, 10) / 100;
        state.modalPlaying = false;
        if (elements.modalPlay) elements.modalPlay.textContent = '▶';
      });
    }

    if (elements.modalSpeed) {
      elements.modalSpeed.addEventListener('change', (e) => {
        state.modalSpeed = parseFloat(e.target.value);
      });
    }

    if (elements.modalCopy) {
      elements.modalCopy.addEventListener('click', () => {
        if (state.currentModalCard) copySinglePrompt(state.currentModalCard.id);
      });
    }

    // Re-render strings when language changes via VAS blog.js
    const langBtn = document.getElementById('blog-language');
    if (langBtn) {
      langBtn.addEventListener('click', () => {
        setTimeout(() => {
          renderChips();
          renderGrid();
          updateTray();
        }, 50);
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
}());
