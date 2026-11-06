/* Read-only checks of the approved rendered design; shared by browser fixtures. */
(function () {
  const normalizeFont = value => value.replace(/["']/g, '').replace(/\s+/g, ' ').replace(/\s*,\s*/g, ',').trim().toLowerCase();
  const rgb = hex => `rgb(${[1, 3, 5].map(offset => parseInt(hex.slice(offset, offset + 2), 16)).join(', ')})`;
  function computedFont(doc, win, declaration) {
    // Chromium on macOS serializes BlinkMacSystemFont as system-ui. Ask the
    // same engine to normalize the independent baseline, without changing it.
    const probe = doc.createElement('span');
    probe.style.cssText = 'display:none';
    probe.style.setProperty('font-family', declaration, 'important');
    doc.body.append(probe);
    try { return normalizeFont(win.getComputedStyle(probe).fontFamily); }
    finally { probe.remove(); }
  }
  function violations(doc, win, contract) {
    const errors = [];
    const root = win.getComputedStyle(doc.documentElement);
    const theme = doc.documentElement.dataset.theme || 'light';
    for (const [token, expected] of Object.entries(contract.themes[theme])) {
      if (root.getPropertyValue(token).trim().toLowerCase() !== expected.toLowerCase()) errors.push(`palette:${theme}:${token}`);
    }
    const body = win.getComputedStyle(doc.body);
    if (normalizeFont(body.fontFamily) !== computedFont(doc, win, contract.fonts.body)) errors.push('font:body');
    const mark = doc.querySelector('.brand-mark');
    if (!mark || normalizeFont(win.getComputedStyle(mark).fontFamily) !== computedFont(doc, win, contract.fonts.mono)) errors.push('font:mono');
    if (body.backgroundColor !== rgb(contract.themes[theme]['--paper']) || body.color !== rgb(contract.themes[theme]['--ink'])) errors.push(`colors:body:${theme}`);
    const action = doc.getElementById('hero-explore');
    if (!action || win.getComputedStyle(action).backgroundColor !== rgb(contract.themes[theme]['--accent'])) errors.push(`colors:primary:${theme}`);
    let previous;
    for (const selector of contract.homepage_sections) {
      const section = doc.querySelector(`#library-view > ${selector}`);
      const box = section?.getBoundingClientRect();
      if (!box || box.height <= 0 || win.getComputedStyle(section).visibility === 'hidden' || win.getComputedStyle(section).opacity === '0') errors.push(`section:${selector}:hidden`);
      else {
        if (previous && box.top < previous.bottom - 2) errors.push(`section:${selector}:order-or-overlap`);
        previous = box;
      }
    }
    const search = doc.getElementById('search-input');
    if (!action || !search || search.getBoundingClientRect().top - action.getBoundingClientRect().bottom > contract.max_search_gap_px) errors.push('search:gap');
    const field = doc.querySelector('.hero-field');
    if (!field || field.getBoundingClientRect().width <= 0 || field.getBoundingClientRect().height <= 0 || win.getComputedStyle(field).opacity === '0' || win.getComputedStyle(field).visibility === 'hidden') errors.push('hero:field-hidden');
    const capsule = doc.querySelector('.hero-field .field-capsule');
    if (!capsule || win.getComputedStyle(capsule).display === 'none' || win.getComputedStyle(capsule).visibility === 'hidden') errors.push('hero:particles-missing');
    for (const selector of ['#intro-title', '#hero-explore']) {
      const node = doc.querySelector(selector);
      if (!node || node.getBoundingClientRect().height <= 0 || win.getComputedStyle(node).opacity === '0' || win.getComputedStyle(node).visibility === 'hidden') errors.push(`hero:${selector}:hidden`);
    }
    if (field?.getAttribute('aria-hidden') !== 'true') errors.push('hero:field-accessible-noise');
    const wordmark = doc.querySelector('#intro-title .sr-only');
    if (wordmark?.textContent !== 'Vie Agentic Skill') errors.push('hero:accessible-wordmark');
    if ([...doc.querySelectorAll('.hero-letter')].some(letter => letter.getAttribute('aria-hidden') !== 'true')) errors.push('hero:letters-accessible-noise');
    return errors;
  }
  window.VASUIContract = { violations, rgb };
}());
