const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const source = fs.readFileSync(path.join(__dirname, '../docs/analytics.js'), 'utf8');

function bootstrap(initial = {}, forbiddenAccesses) {
  const window = { ...initial };
  const sandbox = { window, URL };
  if (forbiddenAccesses) {
    const deny = name => ({
      configurable: true,
      get() {
        forbiddenAccesses.push(name);
        throw new Error(`Analytics must not access ${name}`);
      },
      set() {
        forbiddenAccesses.push(name);
        throw new Error(`Analytics must not replace ${name}`);
      },
    });
    for (const name of ['document', 'localStorage', 'sessionStorage', 'history', 'fetch', 'XMLHttpRequest', 'navigator', 'location']) {
      Object.defineProperty(window, name, deny(`window.${name}`));
      Object.defineProperty(sandbox, name, deny(name));
    }
  }
  vm.runInNewContext(source, sandbox, { filename: 'docs/analytics.js', timeout: 1000 });
  return window;
}

function middleware(window) {
  const registrations = window.vaq.filter(entry => entry[0] === 'beforeSend');
  assert.equal(registrations.length, 1, 'The sanitizer must be queued before tracking starts');
  assert.equal(typeof registrations[0][1], 'function');
  return registrations[0][1];
}

test('analytics initializes the official queue and registers its sanitizer', () => {
  const window = bootstrap();
  assert.equal(typeof window.va, 'function');
  assert.ok(Array.isArray(window.vaq));
  middleware(window);
  window.va('event', { name: 'queued-example' });
  const queued = window.vaq[window.vaq.length - 1];
  assert.equal(queued[0], 'event');
  assert.equal(queued[1].name, 'queued-example');
});

test('analytics preserves an existing Vercel handler and pending queue', () => {
  const calls = [];
  const handler = (...args) => calls.push(args);
  const pending = [['pageview', { path: '/already-queued/' }]];
  const window = bootstrap({ va: handler, vaq: pending });
  assert.equal(window.va, handler);
  assert.equal(window.vaq, pending);
  assert.equal(pending.length, 1, 'Existing queued events must not be discarded or replayed');
  assert.equal(calls.length, 1);
  assert.equal(calls[0][0], 'beforeSend');
  assert.equal(typeof calls[0][1], 'function');
});

test('pageviews discard private URL fields without changing the input event', () => {
  const beforeSend = middleware(bootstrap());
  const input = Object.freeze({
    type: 'pageview',
    url: 'https://alice:private-password@vie-agentic-skills.vercel.app/blog/agent-skills-la-gi/?q=private-search&lang=vi#private-fragment',
    marker: 'keep-event-metadata',
  });
  const output = beforeSend(input);
  assert.notEqual(output, input, 'The sanitizer must return a fresh event');
  assert.deepEqual(JSON.parse(JSON.stringify(output)), {
    type: 'pageview',
    url: 'https://vie-agentic-skills.vercel.app/blog/agent-skills-la-gi/',
    marker: 'keep-event-metadata',
  });
  assert.ok(input.url.includes('private-password'));
  assert.ok(input.url.includes('private-search'));
  assert.ok(input.url.endsWith('#private-fragment'));
});

test('sanitized URLs retain their origin and exact public pathname', () => {
  const beforeSend = middleware(bootstrap());
  for (const [url, expected] of [
    ['https://vie-agentic-skills.vercel.app/?skill=webapp-testing&agent=codex', 'https://vie-agentic-skills.vercel.app/'],
    ['https://preview.vercel.app/blog/a%20b/?lang=en#reading-position', 'https://preview.vercel.app/blog/a%20b/'],
    ['http://localhost:8765/blog/guide/?q=secret', 'http://localhost:8765/blog/guide/'],
    ['https://example.com/blog/guide/', 'https://example.com/blog/guide/'],
  ]) {
    assert.equal(beforeSend({ type: 'pageview', url }).url, expected, url);
  }
});

test('the sanitizer preserves the event type and does not add custom tracking data', () => {
  const beforeSend = middleware(bootstrap());
  const output = beforeSend({ type: 'event', url: 'https://example.com/blog/?token=secret#private' });
  assert.deepEqual(JSON.parse(JSON.stringify(output)), { type: 'event', url: 'https://example.com/blog/' });
});

test('malformed URLs and unsupported protocols suppress the event safely', () => {
  const beforeSend = middleware(bootstrap());
  for (const input of [null, undefined, {}, { url: null }, { url: 17 },
    ...['', 'not a URL', '/relative?secret=1', 'https://', 'javascript:alert(1)', 'data:text/plain,secret', 'ftp://example.com/private']
      .map(url => ({ type: 'pageview', url })),
  ]) {
    assert.equal(beforeSend(input), null, JSON.stringify(input));
  }
});

test('bootstrap and sanitization do not read forms/storage or alter navigation/network APIs', () => {
  const accesses = [];
  const window = bootstrap({}, accesses);
  const beforeSend = middleware(window);
  assert.equal(beforeSend({ type: 'pageview', url: 'https://example.com/blog/?q=private' }).url, 'https://example.com/blog/');
  assert.equal(beforeSend({ type: 'pageview', url: 'invalid' }), null);
  assert.deepEqual(accesses, []);
});
