# stageshow trong VAS / stageshow in VAS

## Tiếng Việt

Đã thêm **1 skill mới / 358 tệp**, không có bản trùng phải bỏ qua.
Catalog: **3.354 skill / 119 danh mục**.
Đây là bộ công cụ thiết kế và hoạt họa giao diện sản phẩm (faux product UI, miniature UI, interactive demo và cursor walkthroughs) dành cho **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline** và **GitHub Copilot CLI** do tác giả **Benji Taylor ([@benjitaylor](https://github.com/benjitaylor))** phát triển:
giúp bạn tạo ra các khung minh họa sản phẩm thực tế và đáng tin cậy (browser windows, macOS app chrome, dashboards, phones, dynamic island notifications, bento grids, terminals) với hoạt họa con trỏ tương tác di chuyển và nhấp chuột có chủ đích (`a.click()`, `a.set()`) phục vụ trang landing page, feature cards hoặc docs hero.

Skill được phát hành theo giấy phép **MIT License**, bản quyền thuộc về **Benji Taylor**. Các biểu tượng ứng dụng và nhãn hiệu minh họa của bên thứ ba tuân thủ giấy phép riêng và được ghi nguồn chi tiết trong `NOTICE.md` và `kit/brands/SOURCES.md`.

### Hướng dẫn sử dụng không cần clone repo (Copy Agent Prompt)

Mở trang [stageshow trên VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&sources=stageshow), chọn agent (Antigravity, Cursor, Claude Code, Codex...), bấm **Copy Agent Prompt** và dán vào cửa sổ chat của dự án.

Agent sẽ đọc manifest `install-manifests/stageshow.json`, xác thực SHA-256 từng tệp, tải trọn gói và lưu vào thư mục dự án cùng receipt `.vas-manifest.json` tương thích với CLI.

### Hướng dẫn sử dụng qua CLI (`./vas`)

Từ thư mục checkout VAS:

```bash
# Tìm kiếm skill
./vas search stageshow

# Xem chi tiết runbook
./vas show stageshow

# Cài đặt vào dự án (chế độ copy độc lập)
./vas install stageshow --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Cài đặt liên kết (chế độ link symlink)
./vas install stageshow --target antigravity --mode link

# Kiểm tra trạng thái cài đặt
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Gỡ bỏ skill khi hoàn thành dự án
./vas uninstall stageshow --target claude --dest "/path/to/project/.claude/skills"
```

### Bảng thư mục cài đặt mặc định theo Agent

| Agent | Thư mục cài đặt trong dự án |
|---|---|
| Google Antigravity | `.agents/skills/stageshow/` |
| OpenAI Codex | `.codex/skills/stageshow/` |
| Claude Code | `.claude/skills/stageshow/` |
| Cursor | `.cursor/skills/stageshow/` |
| Windsurf | `.windsurf/skills/stageshow/` |
| Cline / Roo Code | `.cline/skills/stageshow/` |
| GitHub Copilot CLI | `.github/skills/stageshow/` |

### Yêu cầu tiên quyết & Lưu ý an toàn

- **Môi trường hệ thống**:
  - React 18+ và CSS thuần trong ứng dụng của bạn.
  - Node.js 20.19+ (nếu muốn chạy thử Vite playground cục bộ qua `npm run dev` hoặc kiểm tra CSS qua `npm run check:css`).
  - Tùy chọn kiểm tra filming: `playwright-core` và Google Chrome có sẵn trên máy (hoặc cấu hình `CHROME_PATH`).
- **Quyền riêng tư & An toàn**: Toàn bộ kit React và mã nguồn minh họa chạy 100% offline. Không có tiến trình chạy ngầm, không tự động cài đặt runtime hay kết nối dịch vụ bên ngoài trong quá trình cài đặt `./vas install`.

---

## English

Added **1 new skill / 358 files**, zero duplicates skipped.
Catalog total: **3,354 skills / 119 categories**.
This is the miniature product UI, interactive demo, and cursor motion design skill for **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline**, and **GitHub Copilot CLI**, authored by **Benji Taylor ([@benjitaylor](https://github.com/benjitaylor))**:
build believable faux product interfaces (browser windows, app frames, phones, notifications, terminals, bento grids, and cursor walkthroughs) framed and cropped with intent for marketing pages, feature cards, and documentation hero sections.

Distributed under the **MIT License**, Copyright (c) 2026 Benji Taylor. Third-party brand marks, example app artwork, and vector icons remain with their respective owners and are documented in `NOTICE.md` and `kit/brands/SOURCES.md`.

### No-Clone Setup (Copy Agent Prompt)

Open [stageshow on VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=en&sources=stageshow), pick your target coding agent (Antigravity, Cursor, Claude Code, Codex...), click **Copy Agent Prompt**, and paste it into your project chat.

The agent fetches the verified file manifest at `install-manifests/stageshow.json`, validates each SHA-256 hash, and saves the standalone payload along with `.vas-manifest.json`.

### CLI Workflow (`./vas`)

```bash
# Discover skill
./vas search stageshow

# View runbook
./vas show stageshow

# Install into project in standalone copy mode
./vas install stageshow --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Install in symlink mode
./vas install stageshow --target antigravity --mode link

# Check installation receipt
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Uninstall cleanly
./vas uninstall stageshow --target claude --dest "/path/to/project/.claude/skills"
```

### Default Agent Installation Directories

| AI Agent | Target Directory |
|---|---|
| Google Antigravity | `.agents/skills/stageshow/` |
| OpenAI Codex | `.codex/skills/stageshow/` |
| Claude Code | `.claude/skills/stageshow/` |
| Cursor | `.cursor/skills/stageshow/` |
| Windsurf | `.windsurf/skills/stageshow/` |
| Cline / Roo Code | `.cline/skills/stageshow/` |
| GitHub Copilot CLI | `.github/skills/stageshow/` |

### Prerequisites & Safety Notes

- **Runtime & Tools**:
  - React 18+ and plain CSS in your target project.
  - Node.js 20.19+ (for running the optional local Vite playground or CSS clash checks).
  - Optional filming & verification: `playwright-core` and an installed Chrome browser (or `CHROME_PATH`).
- **Safety & Privacy**: The React kit and example scenes run entirely offline in standard web environments. Zero network calls or external API keys needed. No background process or downloaded runtime is executed during `./vas install`.
