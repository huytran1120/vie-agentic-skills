/* Vercel Web Analytics bootstrap. Loaded only by Vercel publication builds. */
(function () {
  'use strict';
  window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
  window.va('beforeSend', function (event) {
    try {
      const url = new URL(event.url);
      if (!['http:', 'https:'].includes(url.protocol)) return null;
      url.search = '';
      url.hash = '';
      url.username = '';
      url.password = '';
      return { ...event, url: url.href };
    } catch (_) { return null; }
  });
}());
