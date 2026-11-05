# n8n Self-Hosting (`n8n-mcp`) trong VAS / n8n Self-Hosting (`n8n-mcp`) in VAS

## Tiếng Việt

Đã thêm **1 skill mới (`n8n-self-hosting`) / 15 tệp** và bỏ qua **14 skill trùng đã tồn tại trong catalog**.
Upstream: [`czlonkowski/n8n-mcp`](https://github.com/czlonkowski/n8n-mcp) tại revision `1c755c5c8d99eb71faade17753a7f24138f4212c`.
Catalog: **3.873 skill / 119 danh mục**.

Kỹ năng **`n8n-self-hosting`** do **Romuald Czlonkowski ([@czlonkowski](https://github.com/czlonkowski))** phát triển dành cho **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline** và **GitHub Copilot CLI**:
hướng dẫn triển khai n8n tự host (self-hosted) hoàn chỉnh trên máy chủ Linux qua SSH với Docker Compose, reverse proxy Caddy tự động cấp chứng chỉ HTTPS (Let's Encrypt), hỗ trợ cả **Single Mode** (1 container + SQLite) lẫn **Queue Mode** (main + Redis + Postgres + N workers), cấu hình ghi đè thông tin xác thực OAuth (`CREDENTIAL_OVERWRITES`), gia cố bảo mật (`SECURITY`) và vận hành Ngày 2 (`DAY2`: sao lưu, khôi phục, nâng cấp phiên bản).

Kỹ năng được phát hành theo giấy phép **MIT License**, bản quyền thuộc về **Romuald Czlonkowski**.

### Kết quả kiểm tra trùng lặp trên kho nguồn `czlonkowski/n8n-mcp`

- **1 kỹ năng mới được nhập**:
  - `n8n-self-hosting` (`data/skills/n8n-self-hosting` → `skills/n8n-self-hosting`, danh mục `automation`, 15 tệp đi kèm gồm `SKILL.md`, `README.md`, `SINGLE_MODE.md`, `QUEUE_MODE.md`, `SECURITY.md`, `CREDENTIAL_OVERWRITES.md`, `DAY2.md`, `LICENSE`, `NOTICE.md` và 6 tệp cấu hình mẫu trong `assets/`).
- **14 kỹ năng được bỏ qua** vì đã tồn tại sẵn trong catalog VAS (giữ nguyên phiên bản hiện có, không tự ý ghi đè hay đổi tên):
  - `n8n-agents`, `n8n-binary-and-data`, `n8n-code-javascript`, `n8n-code-python`, `n8n-code-tool`, `n8n-error-handling`, `n8n-expression-syntax`, `n8n-mcp-tools-expert`, `n8n-multi-instance`, `n8n-node-configuration`, `n8n-subworkflows`, `n8n-validation-expert`, `n8n-workflow-patterns`, `using-n8n-mcp-skills`.

### Cấu trúc tệp đính kèm trong `skills/n8n-self-hosting/`

- `SKILL.md`: Runbook chính điều phối quy trình chọn kiến trúc (Single vs Queue), kiểm tra tiền điều kiện DNS/SSH, cài Docker, sinh khóa bí mật và khởi chạy HTTPS.
- `SINGLE_MODE.md` & `QUEUE_MODE.md`: Hướng dẫn chuyên sâu cho triển khai đơn lẻ (SQLite) và triển khai phân tán (Postgres + Redis + Workers).
- `SECURITY.md`: Quy chuẩn phân tách mạng Docker nội bộ, bảo vệ `N8N_ENCRYPTION_KEY`, cấu hình biến môi trường an toàn.
- `CREDENTIAL_OVERWRITES.md`: Cấu hình OAuth dùng chung toàn hệ thống (ẩn `client_secret` khỏi người dùng cuối, bật nút đăng nhập Google).
- `DAY2.md`: Quy trình nâng cấp phiên bản, sao lưu/khôi phục cơ sở dữ liệu và xử lý sự cố vận hành.
- `assets/`:
  - `docker-compose.single.yml` & `.env.single.example`
  - `docker-compose.queue.yml` & `.env.queue.example`
  - `Caddyfile` (cấu hình reverse proxy TLS tự động)
  - `init-data.sh` (script khởi tạo user Postgres không phải root cho Queue Mode, quyền thực thi `0755`)

### Hướng dẫn sử dụng không cần clone repo (Copy Agent Prompt)

Mở trang [n8n Self-Hosting trên VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&sources=n8nmcp), chọn agent (Antigravity, Cursor, Claude Code, Codex...), bấm **Copy Agent Prompt** và dán vào cửa sổ chat của dự án.

Agent sẽ đọc manifest `install-manifests/n8n-self-hosting.json`, xác thực SHA-256 từng tệp (bao gồm toàn bộ tài liệu tham khảo và thư mục `assets/`), tải trọn gói và lưu vào thư mục dự án cùng receipt `.vas-manifest.json` tương thích với CLI.

### Hướng dẫn sử dụng qua CLI (`./vas`)

Từ thư mục checkout VAS:

```bash
# Tìm kiếm kỹ năng n8n self-hosting
./vas search n8n-self-hosting

# Xem chi tiết runbook
./vas show n8n-self-hosting

# Cài đặt vào dự án (chế độ copy độc lập)
./vas install n8n-self-hosting --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Cài đặt liên kết (chế độ link symlink)
./vas install n8n-self-hosting --target antigravity --mode link

# Kiểm tra trạng thái cài đặt
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Gỡ bỏ kỹ năng khi hoàn thành dự án
./vas uninstall n8n-self-hosting --target claude --dest "/path/to/project/.claude/skills"
```

### Bảng thư mục cài đặt mặc định theo Agent

| Agent | Thư mục cài đặt trong dự án |
|---|---|
| Google Antigravity | `.agents/skills/n8n-self-hosting/` |
| OpenAI Codex | `.codex/skills/n8n-self-hosting/` |
| Claude Code | `.claude/skills/n8n-self-hosting/` |
| Cursor | `.cursor/skills/n8n-self-hosting/` |
| Windsurf | `.windsurf/skills/n8n-self-hosting/` |
| Cline / Roo Code | `.cline/skills/n8n-self-hosting/` |
| GitHub Copilot CLI | `.github/skills/n8n-self-hosting/` |

---

## English

Added **1 new skill (`n8n-self-hosting`) / 15 files** and skipped **14 duplicate skills already present in the catalog**.
Upstream: [`czlonkowski/n8n-mcp`](https://github.com/czlonkowski/n8n-mcp) at revision `1c755c5c8d99eb71faade17753a7f24138f4212c`.
Catalog total: **3,873 skills / 119 categories**.

The **`n8n-self-hosting`** skill, authored by **Romuald Czlonkowski ([@czlonkowski](https://github.com/czlonkowski))** for **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline**, and **GitHub Copilot CLI**, provides an end-to-end production runbook for deploying self-hosted n8n on a Linux VM over SSH using Docker Compose behind a Caddy reverse proxy with automatic Let's Encrypt HTTPS. It covers both **Single Mode** (single container + SQLite) and **Queue Mode** (main + Redis + Postgres + N workers), OAuth credential overwrites (`CREDENTIAL_OVERWRITES.md`), container/network security hardening (`SECURITY.md`), and Day-2 operations (`DAY2.md`: upgrades, backups, restores, and scaling).

Distributed under the **MIT License**, Copyright (c) 2024 Romuald Czlonkowski.

### Duplicate Check Summary for `czlonkowski/n8n-mcp`

- **1 genuinely new skill imported**:
  - `n8n-self-hosting` (`data/skills/n8n-self-hosting` → `skills/n8n-self-hosting`, category `automation`, 15 files including `SKILL.md`, 6 reference guides, `LICENSE`, `NOTICE.md`, and 6 production templates in `assets/`).
- **14 existing skills skipped** (preserved intact without overwriting or renaming):
  - `n8n-agents`, `n8n-binary-and-data`, `n8n-code-javascript`, `n8n-code-python`, `n8n-code-tool`, `n8n-error-handling`, `n8n-expression-syntax`, `n8n-mcp-tools-expert`, `n8n-multi-instance`, `n8n-node-configuration`, `n8n-subworkflows`, `n8n-validation-expert`, `n8n-workflow-patterns`, `using-n8n-mcp-skills`.

### No-Clone Web Quickstart (Copy Agent Prompt)

Open [n8n Self-Hosting on VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=en&sources=n8nmcp), select your coding agent (Antigravity, Cursor, Claude Code, Codex, etc.), click **Copy Agent Prompt**, and paste it into your project chat window.

Your agent reads `install-manifests/n8n-self-hosting.json`, verifies every SHA-256 hash across all 15 files, downloads the complete skill directory including `assets/`, and writes the CLI-compatible `.vas-manifest.json` receipt.

### CLI Instructions (`./vas`)

From your local VAS repository checkout:

```bash
# Search for the skill
./vas search n8n-self-hosting

# View skill runbook
./vas show n8n-self-hosting

# Install in copy mode
./vas install n8n-self-hosting --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Install in symlink mode
./vas install n8n-self-hosting --target antigravity --mode link

# Check status
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Uninstall skill
./vas uninstall n8n-self-hosting --target claude --dest "/path/to/project/.claude/skills"
```

### Default Agent Installation Destinations

| Agent | Default Project Destination |
|---|---|
| Google Antigravity | `.agents/skills/n8n-self-hosting/` |
| OpenAI Codex | `.codex/skills/n8n-self-hosting/` |
| Claude Code | `.claude/skills/n8n-self-hosting/` |
| Cursor | `.cursor/skills/n8n-self-hosting/` |
| Windsurf | `.windsurf/skills/n8n-self-hosting/` |
| Cline / Roo Code | `.cline/skills/n8n-self-hosting/` |
| GitHub Copilot CLI | `.github/skills/n8n-self-hosting/` |
