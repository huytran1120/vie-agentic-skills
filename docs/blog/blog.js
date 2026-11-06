(function () {
  'use strict';
  const main = document.getElementById('guide-main');
  const toggle = document.getElementById('blog-language');
  const theme = document.getElementById('blog-theme');
  let saved;
  try { saved = localStorage.getItem('vas-language'); } catch (_) { /* Private storage can be unavailable. */ }
  let language = new URLSearchParams(location.search).get('lang') || saved;
  language = language === 'en' ? 'en' : 'vi';
  function applyLanguage() {
    document.documentElement.lang = language;
    document.querySelectorAll('[data-language]').forEach(node => { node.hidden = node.dataset.language !== language; });
    const titles = JSON.parse(main.dataset.pageTitles);
    const descriptions = JSON.parse(main.dataset.pageDescriptions);
    document.title = titles[language];
    for (const selector of ['meta[name="description"]', 'meta[property="og:description"]', 'meta[name="twitter:description"]']) document.querySelector(selector).content = descriptions[language];
    for (const selector of ['meta[property="og:title"]', 'meta[name="twitter:title"]']) document.querySelector(selector).content = titles[language].replace(/ — VAS$/, '');
    toggle.textContent = language === 'vi' ? 'EN' : 'VI';
    toggle.lang = language === 'vi' ? 'en' : 'vi';
    toggle.setAttribute('aria-label', language === 'vi' ? 'Switch to English' : 'Chuyển sang tiếng Việt');
    document.querySelector('.guide-nav').setAttribute('aria-label', language === 'vi' ? 'Điều hướng' : 'Navigation');
    const companion = document.querySelector('.guide-companion');
    if (companion) companion.setAttribute('aria-label', language === 'vi' ? 'Skill liên quan' : 'Related skill');
    theme.setAttribute('aria-label', language === 'vi' ? (document.documentElement.dataset.theme === 'dark' ? 'Bật giao diện sáng' : 'Bật giao diện tối') : (document.documentElement.dataset.theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'));
    const agent = new URLSearchParams(location.search).get('agent');
    const validAgent = ['antigravity', 'codex', 'claude', 'cursor', 'windsurf', 'cline', 'copilot', 'all'].includes(agent);
    document.querySelectorAll('[data-home], [data-catalog-skill], [data-blog], [data-guide-link]').forEach(link => {
      const url = new URL(link.getAttribute('href'), location.href);
      url.searchParams.set('lang', language);
      if (validAgent) url.searchParams.set('agent', agent);
      link.href = url.href;
    });
  }
  toggle.addEventListener('click', () => {
    language = language === 'vi' ? 'en' : 'vi';
    try { localStorage.setItem('vas-language', language); } catch (_) { /* Keep in-page switching available. */ }
    const url = new URL(location.href);
    url.searchParams.set('lang', language);
    history.replaceState(null, '', url);
    applyLanguage();
  });
  theme.addEventListener('click', () => {
    const dark = document.documentElement.dataset.theme !== 'dark';
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
    theme.setAttribute('aria-pressed', String(dark));
    applyLanguage();
  });
  applyLanguage();
}());
