/* VAS motion layer. Decorative effects never control catalog or installation state. */
(function () {
  'use strict';
  const root = document.documentElement;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  const spring = 'cubic-bezier(.2,.85,.25,1.12)';
  const byId = id => document.getElementById(id);
  const animate = (node, frames, options = {}) => {
    if (reduce.matches || !node?.animate) return null;
    return node.animate(frames, { duration: 650, easing: spring, ...options });
  };

  // A rolling display only: the catalog owns the selected agent and its command.
  const reel = byId('hero-agent');
  let track, labels = [], index = 0, selectedLabel, reelTimer, introFrame, reelGeneration = 0;
  function fitReel(duration) {
    const word = track?.children[index];
    if (!word || !reel.getBoundingClientRect().width) return;
    const height = word.getBoundingClientRect().height;
    const width = word.getBoundingClientRect().width;
    if (duration !== undefined) {
      track.style.transition = duration ? `transform ${duration}ms ${spring}` : 'none';
      reel.style.transition = duration ? `width ${duration}ms ${spring}, border-color .2s` : 'none';
    }
    track.style.transform = `translateY(${-index * height}px)`;
    reel.style.width = `${width}px`;
  }
  function settleReel() {
    clearTimeout(reelTimer);
    if (!labels.length) return;
    index = labels.length + labels.indexOf(selectedLabel);
    fitReel(0);
  }
  function rollReel(label, introduction = false) {
    cancelAnimationFrame(introFrame); clearTimeout(reelTimer);
    const generation = ++reelGeneration;
    const next = labels.indexOf(label);
    const steps = (next - index % labels.length + labels.length) % labels.length;
    if (!introduction && !steps) return;
    if (index + steps + (introduction ? labels.length : 0) >= labels.length * 3) { index %= labels.length; fitReel(0); }
    // Commit the current transform before starting another roll, including rapid clicks.
    void track.offsetHeight;
    index += steps + (introduction ? labels.length : 0);
    const duration = introduction ? 1650 : 720;
    fitReel(reduce.matches ? 0 : duration);
    if (reduce.matches) settleReel();
    else reelTimer = setTimeout(() => { if (generation === reelGeneration) settleReel(); }, duration + 40);
  }
  function setAgent(label, options) {
    const first = !track;
    if (first) {
      labels = options;
      track = document.createElement('span'); track.className = 'agent-track'; track.setAttribute('aria-hidden', 'true');
      for (let cycle = 0; cycle < 3; cycle++) for (const text of labels) {
        const word = document.createElement('span'); word.textContent = text; track.append(word);
      }
      reel.replaceChildren(track); reel.classList.add('agent-reel');
      selectedLabel = label; index = labels.indexOf(label); fitReel(0);
      if (!reduce.matches) introFrame = requestAnimationFrame(() => rollReel(selectedLabel, true));
    } else if (selectedLabel !== label) {
      selectedLabel = label; rollReel(label); fieldSurge();
    } else fitReel();
  }

  // Independent capsule particles move in short, elastic diagonal steps.
  // Collision fading keeps the moving field clear of headings and controls.
  const field = document.querySelector('.hero-field');
  const intro = document.querySelector('.intro');
  const palette = ['#ddd2c3', '#b4a9c7', '#c29fa9', '#a6b59e', '#829db3', '#8e86b5'];
  let particles = [], width = 0, height = 0, blockers = [], pointer = null;
  let fieldFrame = 0, lastTime = 0, onScreen = true, energy = 0;
  function measureField() {
    const rect = field.getBoundingClientRect();
    if (!rect.width || !rect.height) return;
    width = rect.width; height = rect.height;
    blockers = [...document.querySelectorAll('.release-badge, #intro-title > span, .intro-description, .hero-actions, .library-stats')].map(node => {
      let left = 0, top = 0, parent = node;
      // Layout offsets stay stable during the entrance's translated keyframes.
      while (parent && parent !== field.offsetParent) { left += parent.offsetLeft; top += parent.offsetTop; parent = parent.offsetParent; }
      return { left: left - 14, top: top - 14, right: left + node.offsetWidth + 14, bottom: top + node.offsetHeight + 14 };
    });
    const total = width < 600 ? 12 : 26;
    if (particles.length !== total) {
      particles = Array.from({ length: total }, (_, i) => {
        const node = document.createElement('span'); node.className = 'field-capsule';
        node.style.background = palette[i % palette.length];
        return { node, x: 0, y: 0, phase: Math.random(), rate: .18 + Math.random() * .22, length: 0, size: 0, ox: 0, oy: 0, vx: 0, vy: 0, opacity: 0 };
      });
      field.replaceChildren(...particles.map(particle => particle.node));
    }
    particles.forEach((p, i) => {
      p.x = ((i * .618034 + .23) % 1) * width;
      p.y = ((i * .754878 + .07) % 1) * height;
      p.size = Math.max(20, Math.min(42, width * .034));
      p.length = p.size * [1, 2.4, 3.8, 1.6][i % 4];
      p.node.style.width = `${p.length}px`; p.node.style.height = `${p.size}px`;
    });
    drawField(0); wakeField();
  }
  function drawField(dt) {
    energy *= Math.exp(-dt * 1.8);
    const distance = Math.max(56, width * .07);
    for (const p of particles) {
      if (dt) {
        p.phase += dt * p.rate * (1 + energy * 2.5);
        if (p.phase >= 1) { p.phase %= 1; p.x += distance * .866; p.y -= distance * .5; }
        if (p.x > width + p.length) p.x = -p.length;
        if (p.y < -p.length) p.y = height + p.length;
      }
      const phase = reduce.matches ? 0 : p.phase;
      const ease = phase * phase * (3 - 2 * phase);
      const x = p.x + distance * .866 * ease, y = p.y - distance * .5 * ease;
      let tx = 0, ty = 0;
      if (pointer) {
        const dx = x - pointer.x, dy = y - pointer.y, radius = Math.hypot(dx, dy);
        if (radius < 170) { const force = (1 - radius / 170) * 60; tx = dx / Math.max(radius, 1) * force; ty = dy / Math.max(radius, 1) * force; }
      }
      p.vx = (p.vx + (tx - p.ox) * 34 * dt) * Math.exp(-8 * dt);
      p.vy = (p.vy + (ty - p.oy) * 34 * dt) * Math.exp(-8 * dt);
      p.ox += p.vx * dt; p.oy += p.vy * dt;
      const px = x + p.ox, py = y + p.oy;
      const stretch = 1 + Math.sin(phase * Math.PI) * .32;
      const halfWidth = (p.length * stretch * .866 + p.size * .5) * .5;
      const halfHeight = (p.length * stretch * .5 + p.size * .866) * .5;
      const obscuresText = blockers.some(box => px + halfWidth > box.left && px - halfWidth < box.right && py + halfHeight > box.top && py - halfHeight < box.bottom);
      p.opacity = obscuresText ? 0 : p.opacity + (.75 - p.opacity) * (dt ? Math.min(1, dt * 8) : 1);
      p.node.style.opacity = p.opacity.toFixed(3);
      p.node.style.transform = `translate3d(${(px - p.length / 2).toFixed(2)}px,${(py - p.size / 2).toFixed(2)}px,0) rotate(-30deg) scaleX(${stretch})`;
    }
  }
  function tick(now) {
    fieldFrame = 0;
    const dt = lastTime ? Math.min((now - lastTime) / 1000, .04) : 0;
    lastTime = now; drawField(dt); wakeField();
  }
  function wakeField() {
    if (!fieldFrame && onScreen && !document.hidden && !reduce.matches) fieldFrame = requestAnimationFrame(tick);
  }
  function stopField() { cancelAnimationFrame(fieldFrame); fieldFrame = 0; lastTime = 0; }
  function fieldSurge() { if (!reduce.matches) { energy = 1.8; wakeField(); } }
  intro.addEventListener('pointermove', event => {
    if (!finePointer.matches || reduce.matches) return;
    const rect = field.getBoundingClientRect(); pointer = { x: event.clientX - rect.left, y: event.clientY - rect.top };
  }, { passive: true });
  intro.addEventListener('pointerleave', () => { pointer = null; });
  byId('hero-explore').addEventListener('click', fieldSurge);
  document.addEventListener('visibilitychange', () => { stopField(); if (!document.hidden) wakeField(); });
  if ('IntersectionObserver' in window) new IntersectionObserver(([entry]) => {
    onScreen = entry.isIntersecting; if (onScreen) { measureField(); wakeField(); } else stopField();
  }).observe(intro);

  // Wordmark entrance and individual letter hover, with an unchanged accessible name.
  const wordmark = document.querySelector('#intro-title > span:first-child');
  const wordmarkText = wordmark.textContent;
  wordmark.textContent = ''; wordmark.classList.add('hero-wordmark');
  const accessibleWordmark = document.createElement('span'); accessibleWordmark.className = 'sr-only'; accessibleWordmark.textContent = wordmarkText; wordmark.append(accessibleWordmark);
  Array.from(wordmarkText).forEach((text, i) => {
    const letter = document.createElement('span'); letter.textContent = text === ' ' ? '\u00a0' : text;
    letter.className = 'hero-letter'; letter.style.setProperty('--letter', i); letter.setAttribute('aria-hidden', 'true'); wordmark.append(letter);
  });

  // Observe once; no content is hidden until a working observer is installed.
  let revealObserver;
  function stage(nodes) {
    if (!revealObserver || reduce.matches) return;
    nodes.forEach((node, i) => {
      if (node.dataset.reveal) return;
      node.dataset.reveal = 'pending'; node.style.setProperty('--reveal-delay', `${Math.min(i % 6, 4) * 55}ms`); revealObserver.observe(node);
    });
  }
  if ('IntersectionObserver' in window) {
    revealObserver = new IntersectionObserver(entries => {
      for (const entry of entries) if (entry.isIntersecting) {
        entry.target.dataset.reveal = 'shown'; revealObserver.unobserve(entry.target);
      }
    }, { threshold: .08, rootMargin: '0px 0px -24px 0px' });
    stage([...document.querySelectorAll('.library-stats > div, .section-heading, .collection-card, .blender-note, .steps > li, .site-footer')]);
  }
  const results = byId('skills-results');
  const cardsObserver = new MutationObserver(records => {
    for (const record of records) for (const node of record.removedNodes) if (node.nodeType === 1) revealObserver?.unobserve(node);
    stage([...results.children]); syncScroll();
  });
  cardsObserver.observe(results, { childList: true });
  stage([...results.children]);

  // Sliding navigation highlight works with both pointer and keyboard focus.
  const navigation = document.querySelector('.desktop-nav');
  const ink = document.createElement('span'); ink.className = 'nav-ink'; ink.setAttribute('aria-hidden', 'true'); navigation.prepend(ink);
  function moveInk(link) {
    if (!link || !navigation.contains(link)) return;
    const box = link.getBoundingClientRect(), parent = navigation.getBoundingClientRect();
    ink.style.width = `${box.width + 18}px`; ink.style.height = `${box.height - 8}px`;
    ink.style.transform = `translate(${box.left - parent.left - 9}px,${box.top - parent.top + 4}px)`; ink.classList.add('is-visible');
  }
  navigation.addEventListener('pointerover', event => { if (finePointer.matches) moveInk(event.target.closest('a')); });
  navigation.addEventListener('pointerleave', () => ink.classList.remove('is-visible'));
  navigation.addEventListener('focusin', event => moveInk(event.target.closest('a')));
  navigation.addEventListener('focusout', event => { if (!navigation.contains(event.relatedTarget)) ink.classList.remove('is-visible'); });
  const cta = byId('hero-explore');
  cta.addEventListener('pointermove', event => {
    if (reduce.matches || !finePointer.matches) return;
    const rect = cta.getBoundingClientRect();
    cta.style.translate = `${((event.clientX - rect.left) / rect.width - .5) * 10}px ${((event.clientY - rect.top) / rect.height - .5) * 8}px`;
  });
  cta.addEventListener('pointerleave', () => { cta.style.translate = ''; });

  const progress = document.createElement('div'); progress.className = 'reading-progress'; progress.setAttribute('aria-hidden', 'true'); document.body.append(progress);
  let scrollFrame = 0, resizeFrame = 0, lastScrollY = window.scrollY, lastScrollTime = performance.now();
  function syncScroll() {
    scrollFrame = 0;
    const range = root.scrollHeight - window.innerHeight;
    progress.style.transform = `scaleX(${range > 0 ? Math.min(1, Math.max(0, window.scrollY / range)) : 0})`;
    document.querySelector('.site-header').classList.toggle('is-scrolled', window.scrollY > 8);
  }
  window.addEventListener('scroll', () => {
    const now = performance.now(), speed = Math.abs(window.scrollY - lastScrollY) / Math.max(16, now - lastScrollTime);
    lastScrollY = window.scrollY; lastScrollTime = now;
    if (onScreen && !reduce.matches) energy = Math.max(energy, Math.min(.8, speed / 2));
    if (!scrollFrame) scrollFrame = requestAnimationFrame(syncScroll);
  }, { passive: true });
  window.addEventListener('resize', () => {
    cancelAnimationFrame(resizeFrame); resizeFrame = requestAnimationFrame(() => { settleReel(); measureField(); syncScroll(); ink.classList.remove('is-visible'); });
  }, { passive: true });
  if ('ResizeObserver' in window) new ResizeObserver(() => { measureField(); fitReel(); syncScroll(); }).observe(intro);
  // Re-measure when the library returns from a skill detail view.
  new MutationObserver(() => { measureField(); fitReel(); syncScroll(); }).observe(byId('library-view'), { attributes: true, attributeFilter: ['hidden'] });

  let themeTransition;
  function changeTheme(apply) {
    if (!document.startViewTransition || reduce.matches) { apply(); return; }
    themeTransition?.skipTransition();
    const edge = window.innerWidth + window.innerHeight * .58;
    const polygon = offset => `polygon(${offset}px 0,${edge}px 0,${edge}px 100%,${offset + window.innerHeight * .58}px 100%)`;
    try {
      themeTransition = document.startViewTransition(apply);
      themeTransition.ready.then(() => {
        if (reduce.matches) { themeTransition.skipTransition(); return; }
        root.animate([{ clipPath: polygon(window.innerWidth + 8) }, { clipPath: polygon(-window.innerHeight * .58 - 10) }], { duration: 760, easing: 'cubic-bezier(.4,0,.2,1)', pseudoElement: '::view-transition-new(root)', fill: 'both' });
      }).catch(() => {});
    } catch (_) { apply(); }
  }
  reduce.addEventListener('change', () => {
    stopField(); pointer = null; energy = 0; cancelAnimationFrame(introFrame); settleReel();
    if (reduce.matches) {
      document.getAnimations().forEach(animation => animation.cancel());
      document.querySelectorAll('[data-reveal="pending"]').forEach(node => { node.dataset.reveal = 'shown'; revealObserver?.unobserve(node); });
      particles.forEach(p => { p.ox = 0; p.oy = 0; p.vx = 0; p.vy = 0; }); drawField(0);
    } else wakeField();
    cta.style.translate = '';
  });
  window.VASMotion = { setAgent, changeTheme };
  measureField(); syncScroll();
  document.fonts?.ready.then(() => { fitReel(); measureField(); });
})();
