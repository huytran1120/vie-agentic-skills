import os, glob, json, urllib.request, re

# Fetch English translations from the official github page
url = 'https://vincentwei1021.github.io/video-shotcraft/translations.js'
content = urllib.request.urlopen(url).read().decode('utf-8')
m_en = re.search(r'cardsEn:\s*(\{.*?\})\s*,\s*stylesZh:', content, re.DOTALL)
cards_en = {}
if m_en:
    for line in m_en.group(1).splitlines():
        line = line.strip()
        m_line = re.match(r'[\"\']?([a-zA-Z0-9_-]+)[\"\']?\s*:\s*[\"\'](.*)[\"\'],?', line)
        if m_line:
            cards_en[m_line.group(1)] = m_line.group(2).rstrip("',")

shots_dir = 'skills/video-shotcraft/references/shots'
files = glob.glob(f'{shots_dir}/**/*.md', recursive=True)

# Archetype mapping for canvas visualizer
archetype_map = {
    'opening': 'spotlight',
    'camera': 'camera3d',
    'ui-entrance': 'deck',
    'typography': 'slam',
    'interaction': 'click',
    'data': 'counter',
    'transition': 'flip',
    'rhythm': 'beat',
    'effects': 'aurora',
    'outro': 'lockup'
}

# Specific overrides for archetype to make previews diverse
specific_archetypes = {
    'spotlight-hero-card': 'spotlight',
    'brand-ink-open': 'lockup',
    'crane-rise-reveal': 'camera3d',
    'orbit-ring-title-open': 'camera3d',
    'basic-3d-scene': 'camera3d',
    'crash-zoom-punch': 'slam',
    'deck-deal-flyin': 'deck',
    'dock-fanout': 'deck',
    'kinetic-type-slam': 'slam',
    'lead-word-zoom-assemble': 'slam',
    'cursor-click-ripple': 'click',
    'before-after-slider-scrub': 'click',
    'split-counter-orbit': 'counter',
    'chart-live-moves': 'counter',
    'circle-match-iris': 'flip',
    'card-flip-reveal': 'flip',
    'beat-cut-moves': 'beat',
    'beat-step-list-theme-cycle': 'beat',
    'aurora-bloom-bg-flip': 'aurora',
    'laser-scan-reveal': 'aurora',
    'logo-lockup-settle': 'lockup'
}

cards = []

for f in sorted(files):
    if 'ATTRIBUTION.md' in f:
        continue
    rel = os.path.relpath(f, shots_dir)
    cat = rel.split('/')[0] if '/' in rel else 'general'
    text = open(f, encoding='utf-8').read()
    cid = os.path.splitext(os.path.basename(f))[0]
    
    fm = {}
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            for l in parts[1].splitlines():
                if ':' in l:
                    k, v = l.split(':', 1)
                    fm[k.strip()] = v.strip().strip('\"\'')
    
    zh_summary = fm.get('一句话', '')
    duration = fm.get('时长', '90f (~3s)')
    energy_raw = fm.get('能量', '中')
    energy = 'high' if '高' in energy_raw else ('low' if '低' in energy_raw else 'medium')
    en_summary = cards_en.get(cid, zh_summary)
    
    archetype = specific_archetypes.get(cid, archetype_map.get(cat, 'spotlight'))

    cards.append({
        'id': cid,
        'name': cid,
        'category': cat,
        'summary_zh': zh_summary,
        'summary_en': en_summary,
        'duration': duration,
        'energy': energy,
        'archetype': archetype
    })

print(f"Total cards: {len(cards)}")
out_dir = 'docs/blog/lam-video-quang-cao-san-pham-remotion-video-shotcraft'
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, 'cards-data.js')

with open(out_file, 'w', encoding='utf-8') as out:
    out.write('window.SHOTCRAFT_CARDS = ' + json.dumps(cards, ensure_ascii=False, indent=2) + ';\n')

print(f"Successfully generated {out_file} ({len(cards)} items)")
