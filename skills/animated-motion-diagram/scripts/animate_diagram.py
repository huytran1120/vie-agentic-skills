#!/usr/bin/env python3
"""
animate_diagram.py - Transforms or builds an Animated Motion Diagram.

Features:
- Animated flowing dashes on all SVG connectors (stroke-dasharray + stroke-dashoffset animation).
- Animated SVG particles (glowing beads) moving along data paths using <animateMotion>.
- Interactive Controls Bar: Play/Pause, Speed (0.5x, 1x, 2x), Flow Filter (All, Typing, MCP, etc.), Dark/Light toggle.
- Node hover elevation, halo glow, and interactive details tooltip.
"""

import sys
import re
import os

EXTRA_MOTION_CSS = """
/* ANIMATION & MOTION STYLES ==================================== */
@keyframes flowForward {
  from { stroke-dashoffset: 28; }
  to { stroke-dashoffset: 0; }
}

@keyframes pulseGlow {
  0%, 100% { opacity: 0.85; filter: drop-shadow(0 0 2px var(--color-accent)); }
  50% { opacity: 1; filter: drop-shadow(0 0 8px var(--color-accent)); }
}

/* Streaming dashes on edges */
.e {
  stroke: var(--color-accent);
  stroke-width: 1.8;
  stroke-dasharray: 8 6;
  animation: flowForward var(--flow-speed, 1.1s) linear infinite;
  stroke-linecap: round;
}

.n {
  stroke: var(--color-neutral);
  stroke-width: 1.5;
  stroke-dasharray: 6 6;
  animation: flowForward var(--flow-speed-slow, 1.6s) linear infinite;
  stroke-linecap: round;
}

.dash {
  stroke-dasharray: 5 6 !important;
  animation: flowForward var(--flow-speed-dash, 1.3s) linear infinite;
}

/* Suspended state when paused */
.paused .e,
.paused .n,
.paused .dash {
  animation-play-state: paused !important;
}

.paused .particle {
  display: none !important;
}

/* Glowing Particle dots along paths */
.particle {
  fill: var(--color-accent);
  filter: drop-shadow(0 0 5px var(--color-accent));
}

.particle.neutral {
  fill: var(--color-neutral);
  filter: drop-shadow(0 0 3px var(--color-neutral));
}

.particle.g1 {
  fill: var(--color-g1);
  filter: drop-shadow(0 0 5px var(--color-g1));
}

/* Node Hover Elevation & Motion */
.node {
  transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.2s ease;
  cursor: pointer;
}

.node:hover {
  transform: translateY(-4px) scale(1.03);
  z-index: 25;
}

.node:hover .tile {
  border-color: var(--color-accent);
  box-shadow: 0 6px 18px oklch(58% 0.20 256 / 0.25);
}

.node.dimmed {
  opacity: 0.25;
  filter: grayscale(80%);
}

.node.highlighted .tile {
  border-color: var(--color-accent);
  box-shadow: 0 0 16px var(--color-accent);
  transform: scale(1.05);
}

/* Interactive Floating Controls Bar */
.controls-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  background: var(--color-paper-2);
  border: 1px solid var(--color-rule-2);
  border-radius: var(--radius-card);
  padding: 8px 16px;
  margin-bottom: var(--space-md);
  font-family: var(--font-mono);
  font-size: 11px;
  flex-wrap: wrap;
}

.btn-group {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.control-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--color-paper);
  color: var(--color-ink);
  border: 1px solid var(--color-rule-2);
  border-radius: 6px;
  padding: 5px 12px;
  cursor: pointer;
  font-family: inherit;
  font-size: 11px;
  font-weight: 500;
  transition: all 0.15s ease;
}

.control-btn:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
  transform: translateY(-1px);
}

.control-btn.active {
  background: var(--color-accent);
  color: #fff;
  border-color: var(--color-accent);
  box-shadow: 0 2px 8px var(--color-accent-soft);
}

/* Interactive Floating Tooltip */
#nodeTooltip {
  position: absolute;
  z-index: 100;
  display: none;
  background: var(--color-paper);
  border: 1px solid var(--color-rule-2);
  border-radius: var(--radius-card);
  padding: 12px 16px;
  box-shadow: 0 10px 30px oklch(24% 0.02 258 / 0.18);
  max-width: 300px;
  pointer-events: none;
  font-family: var(--font-body);
  transition: opacity 0.15s ease;
}

#nodeTooltip h4 {
  font-family: var(--font-display);
  font-size: 13px;
  font-weight: 700;
  margin: 0 0 4px;
  color: var(--color-ink);
}

#nodeTooltip p {
  font-size: 11px;
  line-height: 1.5;
  color: var(--color-neutral);
  margin: 0;
}

#nodeTooltip .badge {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: 9.5px;
  background: var(--color-accent-tint);
  color: var(--color-accent);
  padding: 2px 6px;
  border-radius: 4px;
  margin-top: 6px;
  border: 1px solid var(--color-accent-soft);
}
"""

CONTROLS_HTML = """
  <!-- Interactive Motion Controls Bar -->
  <div class="controls-bar">
    <div class="btn-group">
      <span style="color:var(--color-neutral); font-weight:600; margin-right:4px;">✨ Chuyển động:</span>
      <button id="togglePlayBtn" class="control-btn active" onclick="togglePlay()">
        <span id="playIcon">⏸️</span> <span id="playText">Tạm dừng</span>
      </button>
      <button class="control-btn" onclick="setSpeed(0.5)">0.5x</button>
      <button class="control-btn active" id="spd1" onclick="setSpeed(1)">1x</button>
      <button class="control-btn" id="spd2" onclick="setSpeed(2)">2x</button>
    </div>

    <div class="btn-group">
      <span style="color:var(--color-neutral); font-weight:600; margin-right:4px;">🎯 Luồng dữ liệu:</span>
      <button class="control-btn active" id="filter-all" onclick="filterFlow('all')">Tất cả luồng</button>
      <button class="control-btn" id="filter-typing" onclick="filterFlow('typing')">⌨️ Gõ văn bản (1.4ms)</button>
      <button class="control-btn" id="filter-mcp" onclick="filterFlow('mcp')">🤖 AI Agent (MCP)</button>
      <button class="control-btn" id="filter-export" onclick="filterFlow('export')">📄 Xuất PDF/DOCX</button>
    </div>

    <div class="btn-group">
      <button class="control-btn" onclick="toggleTheme()">🌓 Sáng / Tối</button>
    </div>
  </div>

  <div id="nodeTooltip">
    <h4 id="ttTitle">Crate</h4>
    <p id="ttDesc">Mô tả chi tiết</p>
    <span id="ttBadge" class="badge">Layer L4</span>
  </div>
"""

SCRIPT_JS = """
<script>
  let isPlaying = true;
  let currentSpeed = 1;

  function togglePlay() {
    isPlaying = !isPlaying;
    const scroller = document.querySelector('.scroller');
    const btn = document.getElementById('togglePlayBtn');
    const icon = document.getElementById('playIcon');
    const text = document.getElementById('playText');
    
    if (isPlaying) {
      scroller.classList.remove('paused');
      btn.classList.add('active');
      icon.innerText = '⏸️';
      text.innerText = 'Tạm dừng';
      document.querySelectorAll('#flowParticles animateMotion').forEach(a => {
        try { a.ownerSVGElement.unpauseAnimations(); } catch(e){}
      });
    } else {
      scroller.classList.add('paused');
      btn.classList.remove('active');
      icon.innerText = '▶️';
      text.innerText = 'Tiếp tục';
      document.querySelectorAll('#flowParticles animateMotion').forEach(a => {
        try { a.ownerSVGElement.pauseAnimations(); } catch(e){}
      });
    }
  }

  function setSpeed(spd) {
    currentSpeed = spd;
    const root = document.documentElement;
    root.style.setProperty('--flow-speed', (1.1 / spd) + 's');
    root.style.setProperty('--flow-speed-slow', (1.6 / spd) + 's');
    root.style.setProperty('--flow-speed-dash', (1.3 / spd) + 's');

    document.querySelectorAll('#spd1, #spd2').forEach(b => b.classList.remove('active'));
    if (spd === 1 && document.getElementById('spd1')) document.getElementById('spd1').classList.add('active');
    if (spd === 2 && document.getElementById('spd2')) document.getElementById('spd2').classList.add('active');
  }

  function toggleTheme() {
    const html = document.documentElement;
    const isDark = html.getAttribute('data-theme') === 'dark';
    if (isDark) {
      html.removeAttribute('data-theme');
    } else {
      html.setAttribute('data-theme', 'dark');
    }
  }

  function filterFlow(flow) {
    document.querySelectorAll('[id^="filter-"]').forEach(b => b.classList.remove('active'));
    const activeBtn = document.getElementById('filter-' + flow);
    if (activeBtn) activeBtn.classList.add('active');

    const particles = document.querySelectorAll('#flowParticles circle');
    if (flow === 'all') {
      particles.forEach(p => p.style.display = 'block');
      document.querySelectorAll('.node').forEach(n => n.classList.remove('dimmed', 'highlighted'));
      return;
    }

    particles.forEach(p => {
      if (p.classList.contains('flow-p-' + flow)) {
        p.style.display = 'block';
      } else {
        p.style.display = 'none';
      }
    });

    const nodeMaps = {
      'typing': ['vforge-word', 'ui-egui', 'vforge-engine', 'vforge-layout', 'vforge-render', 'vforge-doc'],
      'mcp': ['mcp-cli', 'claude-desktop', 'vforge-mcp', 'vforge-control-key', 'vforge-engine', 'vforge-doc'],
      'export': ['vforge-engine', 'vforge-layout', 'vforge-pdf', 'vforge-docx', 'vforge-doc']
    };

    const targetList = nodeMaps[flow] || [];
    document.querySelectorAll('.node').forEach(node => {
      const nameEl = node.querySelector('.name span');
      const name = nameEl ? nameEl.innerText.trim() : '';
      if (targetList.includes(name)) {
        node.classList.remove('dimmed');
        node.classList.add('highlighted');
      } else {
        node.classList.add('dimmed');
        node.classList.remove('highlighted');
      }
    });
  }

  // Interactive Tooltip on Node Hover
  const tooltip = document.getElementById('nodeTooltip');
  const ttTitle = document.getElementById('ttTitle');
  const ttDesc = document.getElementById('ttDesc');
  const ttBadge = document.getElementById('ttBadge');

  const crateDetails = {
    'vforge-word': { desc: 'Ứng dụng Desktop native trên macOS, Windows & Linux (eframe + wgpu).', badge: 'Apps · 3,740 dòng' },
    'vforge-word-web': { desc: 'Bản phân phối trình duyệt WebAssembly hỗ trợ WebGPU/WebGL2.', badge: 'Apps · 1,159 dòng' },
    'mcp-cli': { desc: 'Công cụ CLI đa năng kiêm chế độ máy chủ AI Agent MCP.', badge: 'Apps · 1,901 dòng' },
    'claude-desktop': { desc: 'AI Assistant (Claude Desktop / Antigravity) tương tác qua JSON-RPC.', badge: 'Client Ngoài' },
    'ui-egui': { desc: 'Thanh Ribbon, Canvas vẽ trang GPU, bộ gõ phím, thước kẻ và Việt hoá.', badge: 'Layer 6 · 81,759 dòng' },
    'vforge-control-key': { desc: 'Cơ chế xác thực cổng Socket per-window bảo mật TCP 7981.', badge: 'Layer 0 · 87 dòng' },
    'vforge-mcp': { desc: 'Máy chủ MCP ánh xạ 420+ lệnh thành JSON tools cho AI Agent.', badge: 'Layer 5 · 1,822 dòng' },
    'zotero-api': { desc: 'Tích hợp giao thức trích dẫn tài liệu học thuật Zotero.', badge: 'Layer 5 · 2,372 dòng' },
    'vforge-engine': { desc: 'Session, Command Registry (420+ lệnh), Undo Snapshot Arc và bảo vệ panic.', badge: 'Layer 4 · 72,851 dòng' },
    'xtask': { desc: 'Công cụ CI, kiểm tra phân tầng layers và kiểm định chất lượng mã.', badge: 'Tooling · 1,488 dòng' },
    'vforge-render': { desc: 'vello_cpu rasterizer vẽ trang CPU có bộ đệm thumbnail cache.', badge: 'Layer 3 · 4,499 dòng' },
    'vforge-layout': { desc: 'Dàn trang cực nhanh (1.4 ms/200 trang), chia cột báo và ngắt dòng.', badge: 'Layer 2 · 35,990 dòng' },
    'vforge-pdf': { desc: 'Xuất PDF vector chuẩn xác với krilla, selectable text và mục lục.', badge: 'Layer 3 · 4,513 dòng' },
    'vforge-doc': { desc: 'Cây AST mô hình văn bản cốt lõi: Paragraph, Run, Table, Revision.', badge: 'Layer 1 · 23,719 dòng' },
    'vforge-docx': { desc: 'Bộ đọc/ghi ECMA-376 OOXML (.docx), công thức toán OMML và VBA.', badge: 'Layer 2 · 37,376 dòng' },
    'vforge-docbin': { desc: 'Đọc tệp nhị phân Microsoft Word 97–2003 (.doc) qua cấu trúc CFB.', badge: 'Layer 2 · 8,815 dòng' },
    'vforge-formats': { desc: 'Nhập/xuất tài liệu đa định dạng: Markdown, RTF, ODT, HTML, LaTeX.', badge: 'Layer 2 · 23,058 dòng' },
    'vforge-fonts': { desc: 'Font DB, HarfRust text shaping và thay thế font tương thích Word.', badge: 'Layer 1 · 7,088 dòng' },
    'vforge-proof': { desc: '15 bộ từ điển ngôn ngữ kiểm tra chính tả và ngữ pháp offline.', badge: 'Layer 1 · 16,326 dòng' },
    'vforge-metafile': { desc: 'Phân tích và vẽ đồ hoạ vector Windows Metafile (WMF/EMF).', badge: 'Layer 1 · 3,614 dòng' },
    'vforge-geom': { desc: 'Đơn vị đo chuẩn Word: Points, Twips (1/20 pt), EMU, Inch, Centimet.', badge: 'Layer 0 · 1,271 dòng' }
  };

  document.querySelectorAll('.node').forEach(node => {
    node.addEventListener('mouseenter', (e) => {
      const nameEl = node.querySelector('.name span');
      const name = nameEl ? nameEl.innerText.trim() : '';
      const info = crateDetails[name] || { desc: 'Thành phần kiến trúc hệ thống', badge: 'Module' };

      ttTitle.innerText = name;
      ttDesc.innerText = info.desc;
      ttBadge.innerText = info.badge;

      const rect = node.getBoundingClientRect();
      const scrollerRect = document.querySelector('.scroller').getBoundingClientRect();
      
      const left = node.offsetLeft + 140;
      const top = node.offsetTop;

      tooltip.style.left = left + 'px';
      tooltip.style.top = top + 'px';
      tooltip.style.display = 'block';
    });

    node.addEventListener('mouseleave', () => {
      tooltip.style.display = 'none';
    });
  });
</script>
"""

def extract_paths_and_make_particles(html):
    """Finds <path class="e" d="..." /> and <path class="n" d="..." /> and generates particles."""
    path_matches = re.findall(r'<path\s+class="([^"]+)"\s+d="([^"]+)"', html)
    particles = ['      <!-- AUTO-GENERATED PARTICLES -->', '      <g id="flowParticles">']
    
    seen = set()
    for cls, d in path_matches:
        if d in seen:
            continue
        seen.add(d)
        
        # Determine particle class & speed
        if "e" in cls:
            p_class = "particle flow-p-typing"
            dur = "1.6s"
            r = "4.2"
        elif "g1" in cls or "mcp" in d:
            p_class = "particle g1 flow-p-mcp"
            dur = "1.8s"
            r = "4"
        else:
            p_class = "particle neutral flow-p-export"
            dur = "2.2s"
            r = "3.5"
            
        particles.append(f'        <circle r="{r}" class="{p_class}">')
        particles.append(f'          <animateMotion path="{d}" dur="{dur}" repeatCount="indefinite" />')
        particles.append('        </circle>')
        
    particles.append('      </g>')
    return "\n".join(particles)

def animate_html(input_html):
    out = input_html
    
    # 1. Title update
    if "<title>" in out:
        out = re.sub(r'<title>(.*?)</title>', r'<title>\1 (Animated Motion Diagram)</title>', out, count=1)
        
    # 2. Inject CSS
    if "</style>" in out:
        out = out.replace("</style>", EXTRA_MOTION_CSS + "\n</style>", 1)
        
    # 3. Inject Controls Bar
    if "</header>" in out:
        out = out.replace("</header>", "</header>\n" + CONTROLS_HTML, 1)
        
    # 4. Inject Particles
    particles_svg = extract_paths_and_make_particles(out)
    if "</svg>" in out:
        out = out.replace("</svg>", particles_svg + "\n</svg>", 1)
        
    # 5. Inject Script
    if "</body>" in out:
        out = out.replace("</body>", SCRIPT_JS + "\n</body>", 1)
        
    return out

def main():
    if len(sys.argv) < 2:
        print("Usage: animate_diagram.py <input.html> [output.html]")
        sys.exit(1)
        
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else inp
    
    with open(inp, "r", encoding="utf-8") as f:
        content = f.read()
        
    animated = animate_html(content)
    
    with open(out, "w", encoding="utf-8") as f:
        f.write(animated)
        
    print(f"Successfully generated Animated Motion Diagram: {out}")

if __name__ == "__main__":
    main()
