/* Fast source checks for approved tokens, not a CSS cascade or pixel audit. */
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const contract = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures/ui-contract.json'), 'utf8'));
const stylesheet = fs.readFileSync(path.join(root, 'docs/catalog.css'), 'utf8');

function normalizeValue(value) {
  return String(value ?? '').trim().replace(/\s+/g, ' ').toLowerCase();
}

function normalizeFont(value) {
  return normalizeValue(value).replace(/["']/g, '').replace(/\s*,\s*/g, ',');
}

function rootDeclarations(source, theme) {
  const css = source.replace(/\/\*[\s\S]*?\*\//g, '');
  const selector = theme === 'light'
    ? /:root\s*\{([^{}]*)\}/g
    : /:root\s*\[\s*data-theme\s*=\s*(?:"dark"|'dark'|dark)\s*\]\s*\{([^{}]*)\}/g;
  const values = new Map();
  // Merge declarations from the matching root blocks in source order. Browser
  // layout checks cover rendered overrides and media rules separately.
  for (const match of css.matchAll(selector)) {
    for (const declaration of match[1].split(';')) {
      const colon = declaration.indexOf(':');
      if (colon < 0) continue;
      values.set(declaration.slice(0, colon).trim(), declaration.slice(colon + 1).trim());
    }
  }
  return values;
}

function validateDeclaredTokens(source, expected) {
  const violations = [];
  const light = rootDeclarations(source, 'light');
  for (const theme of ['light', 'dark']) {
    const palette = expected.themes?.[theme];
    assert.ok(palette && Object.keys(palette).length && palette['--accent'], `The contract needs an approved ${theme} palette`);
    const declarations = theme === 'light' ? light : rootDeclarations(source, theme);
    for (const [token, value] of Object.entries(palette)) {
      if (normalizeValue(declarations.get(token)) !== normalizeValue(value)) {
        violations.push(`${theme} ${token}: expected ${value}, got ${declarations.get(token) ?? '(missing)'}`);
      }
    }
  }
  for (const [name, property] of [['body', '--font'], ['mono', '--mono']]) {
    assert.ok(expected.fonts?.[name], `The contract needs an approved ${name} font stack`);
    if (normalizeFont(light.get(property)) !== normalizeFont(expected.fonts[name])) {
      violations.push(`font ${property}: expected ${expected.fonts[name]}, got ${light.get(property) ?? '(missing)'}`);
    }
    // A theme-specific font override must preserve the same approved family.
    const darkValue = rootDeclarations(source, 'dark').get(property);
    if (darkValue !== undefined && normalizeFont(darkValue) !== normalizeFont(expected.fonts[name])) {
      violations.push(`dark font ${property}: expected ${expected.fonts[name]}, got ${darkValue}`);
    }
  }
  return violations;
}

function changeLightDeclaration(source, property, value) {
  return source.replace(/(:root\s*\{)([^{}]*)(\})/, (_, opening, declarations, closing) => {
    const escaped = property.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const changed = declarations.replace(new RegExp(`(${escaped}\\s*:)\\s*[^;]+(?=;)`), `$1 ${value}`);
    return opening + changed + closing;
  });
}

test('VAS declares the approved light/dark palette and system font stacks', () => {
  assert.deepEqual(validateDeclaredTokens(stylesheet, contract), []);
});

test('the design contract detects an unintended accent change', () => {
  const changed = changeLightDeclaration(stylesheet, '--accent', '#00ff00');
  assert.notEqual(changed, stylesheet, 'The negative control must actually alter the stylesheet');
  assert.ok(validateDeclaredTokens(changed, contract).some(message => message.startsWith('light --accent:')));
});

test('the design contract detects an unintended body font replacement', () => {
  const changed = changeLightDeclaration(stylesheet, '--font', 'Georgia, serif');
  assert.notEqual(changed, stylesheet, 'The negative control must actually alter the stylesheet');
  assert.ok(validateDeclaredTokens(changed, contract).some(message => message.startsWith('font --font:')));
});

test('equivalent font quoting, whitespace and case do not change the contract', () => {
  let formatted = stylesheet;
  for (const [name, property] of [['body', '--font'], ['mono', '--mono']]) {
    const equivalent = contract.fonts[name].replace(/"/g, "'").replace(/,/g, '  ,  ').toUpperCase();
    formatted = changeLightDeclaration(formatted, property, equivalent);
  }
  assert.deepEqual(validateDeclaredTokens(formatted, contract), []);
});
