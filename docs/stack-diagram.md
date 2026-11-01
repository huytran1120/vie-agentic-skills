# stack-diagram trong VAS / stack-diagram in VAS

## Tiếng Việt

Đã thêm **1 skill mới / 20 tệp**, không có bản trùng phải bỏ qua.
Catalog: **3.355 skill / 119 danh mục**.
Đây là công cụ tạo sơ đồ kiến trúc hệ thống, đám mây và hạ tầng công nghệ (cloud architecture diagrams, system architectures, infra layouts, service topologies) dành cho **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline** và **GitHub Copilot CLI** do tác giả **caru-ini ([@caru-ini](https://github.com/caru-ini))** phát triển:
giúp bạn chuyển đổi mô tả hệ thống thành sơ đồ kỹ thuật đẹp mắt với logo thương hiệu chính thức (tự động tải từ SVGL, devicon, gilbarbara/logos, AWS Architecture Icons), các hộp phân nhóm chuẩn mực (cloud provider, runtime, monorepo), mũi tên trực giao không cắt chữ và nền lưới kỹ thuật (graph-paper background). Kết quả xuất ra dưới dạng một tệp HTML tự chứa hoàn chỉnh, ảnh PNG (cả light và dark mode), React/TSX component hoặc Claude Artifact.

Skill được phát hành theo giấy phép **MIT License**, bản quyền thuộc về **caru-ini**. Phông chữ đi kèm trong `assets/fonts/` (Geist và JetBrains Mono) được cấp phép theo **SIL Open Font License 1.1**. Các biểu tượng logo và nhãn hiệu tải về thuộc quyền sở hữu của các thương hiệu tương ứng.

### Hướng dẫn sử dụng không cần clone repo (Copy Agent Prompt)

Mở trang [stack-diagram trên VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&sources=stackdiagram), chọn agent (Antigravity, Cursor, Claude Code, Codex...), bấm **Copy Agent Prompt** và dán vào cửa sổ chat của dự án.

Agent sẽ đọc manifest `install-manifests/stack-diagram.json`, xác thực SHA-256 từng tệp, tải trọn gói và lưu vào thư mục dự án cùng receipt `.vas-manifest.json` tương thích với CLI.

### Hướng dẫn sử dụng qua CLI (`./vas`)

Từ thư mục checkout VAS:

```bash
# Tìm kiếm skill
./vas search stack-diagram

# Xem chi tiết runbook
./vas show stack-diagram

# Cài đặt vào dự án (chế độ copy độc lập)
./vas install stack-diagram --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Cài đặt liên kết (chế độ link symlink)
./vas install stack-diagram --target antigravity --mode link

# Kiểm tra trạng thái cài đặt
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Gỡ bỏ skill khi hoàn thành dự án
./vas uninstall stack-diagram --target claude --dest "/path/to/project/.claude/skills"
```

### Bảng thư mục cài đặt mặc định theo Agent

| Agent | Thư mục cài đặt trong dự án |
|---|---|
| Google Antigravity | `.agents/skills/stack-diagram/` |
| OpenAI Codex | `.codex/skills/stack-diagram/` |
| Claude Code | `.claude/skills/stack-diagram/` |
| Cursor | `.cursor/skills/stack-diagram/` |
| Windsurf | `.windsurf/skills/stack-diagram/` |
| Cline / Roo Code | `.cline/skills/stack-diagram/` |
| GitHub Copilot CLI | `.github/skills/stack-diagram/` |

### Yêu cầu tiên quyết & Lưu ý an toàn

- **Môi trường hệ thống**:
  - Python 3.9+ (chỉ sử dụng thư viện chuẩn standard library cho `scripts/build.py` và `scripts/fetch_icons.py`).
  - Kết nối mạng khi tải icon thương hiệu (svgl.app, raw.githubusercontent.com, cdn.jsdelivr.net, aws.amazon.com).
  - Tùy chọn xuất ảnh PNG: Cần Playwright và Chromium (`pip install playwright && python3 -m playwright install --with-deps chromium`).
- **Quyền riêng tư & An toàn**: Quá trình cài đặt `./vas install` chỉ sao chép hoặc tạo liên kết tệp tin tĩnh và ghi receipt `.vas-manifest.json`. Không tự động chạy mã, không cài đặt runtime/MCP hay mở cổng dịch vụ trong lúc cài đặt.

---

## English

Added **1 new skill / 20 files**, zero duplicates skipped.
Catalog total: **3,355 skills / 119 categories**.
This is the cloud-architecture and system topology diagramming skill for **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline**, and **GitHub Copilot CLI**, authored by **caru-ini ([@caru-ini](https://github.com/caru-ini))**:
describe your stack in a sentence and get engineering-drawing-style architecture diagrams with official logos on white tiles, labeled group boxes (VPCs, runtimes, monorepos), and clean orthogonal routed arrows on a graph-paper canvas. Delivers self-contained standalone HTML, high-resolution PNG images (both light and dark mode), zero-dependency React/TSX components, or Claude Artifacts.

The skill source is licensed under the **MIT License**, Copyright (c) 2026 caru-ini. Bundled fonts in `assets/fonts/` (Geist, JetBrains Mono) are licensed under the **SIL Open Font License 1.1**. Downloaded brand logos and trademarks remain the property of their respective owners.

### No-Clone Web Quickstart (Copy Agent Prompt)

Open [stack-diagram on VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=en&sources=stackdiagram), pick your coding agent (Antigravity, Cursor, Claude Code, Codex, etc.), click **Copy Agent Prompt**, and paste it into your project chat window.

Your agent reads `install-manifests/stack-diagram.json`, verifies every SHA-256 hash, downloads the complete payload, and saves the CLI-compatible `.vas-manifest.json` receipt.

### CLI Instructions (`./vas`)

From your local VAS repository checkout:

```bash
# Search for skill
./vas search stack-diagram

# View skill runbook
./vas show stack-diagram

# Install in copy mode
./vas install stack-diagram --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Install in symlink mode
./vas install stack-diagram --target antigravity --mode link

# Check status
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Uninstall skill
./vas uninstall stack-diagram --target claude --dest "/path/to/project/.claude/skills"
```

### Default Target Directory Mapping

| Agent | Project Install Location |
|---|---|
| Google Antigravity | `.agents/skills/stack-diagram/` |
| OpenAI Codex | `.codex/skills/stack-diagram/` |
| Claude Code | `.claude/skills/stack-diagram/` |
| Cursor | `.cursor/skills/stack-diagram/` |
| Windsurf | `.windsurf/skills/stack-diagram/` |
| Cline / Roo Code | `.cline/skills/stack-diagram/` |
| GitHub Copilot CLI | `.github/skills/stack-diagram/` |

### Prerequisites & Safety Notes

- **System Requirements**:
  - Python 3.9+ (standard library only for `scripts/build.py` and `scripts/fetch_icons.py`).
  - Network access for downloading brand logos on demand.
  - Optional PNG export: Playwright + Chromium (`pip install playwright && python3 -m playwright install --with-deps chromium`).
- **Safety**: Installation via `./vas install` only copies or symlinks static files and records `.vas-manifest.json`. No unapproved runtime is installed and no external account or daemon process is started during installation.
