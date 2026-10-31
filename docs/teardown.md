# teardown trong VAS / teardown in VAS

## Tiếng Việt

Đã thêm **1 skill mới / 73 tệp**, không có bản trùng phải bỏ qua.
Catalog: **3.186 skill / 119 danh mục**.
Đây là công cụ xây dựng mô phỏng 3D cơ khí máy móc tương tác cho **Claude Code**, **Cursor**, **Codex** và **Antigravity** do tác giả **Elvar ([@elvarofficial](https://github.com/elvarofficial))** và **whaleyxbt ([@whaleyxbt](https://github.com/whaleyxbt))** phát triển:
biến bất kỳ cỗ máy hay cơ cấu cơ khí nào (động cơ V8, càng hạ cánh máy bay Cessna, cơ cấu bước đi Strandbeest, bơm thủy lực, hộp số) thành một trang HTML tương tác 3D ngoại tuyến có thể tháo rời từng bộ phận, bảng đồng hồ thông số hiển thị trực tiếp theo mô hình chuyển động, các góc nhìn mặt cắt (cutaway modes), chế độ tự động dẫn tour và khả năng xuất video 60 fps kèm nhạc nền tạo tự động (procedural score).

Skill được phát hành theo giấy phép **MIT License**, bản quyền thuộc về **elvarofficial** và **whaleyxbt**. 12 tệp âm thanh mẫu (SFX) được cấp phép theo **CC0 1.0 Public Domain** (ghi nguồn chi tiết tại `sfx/samples/SOURCES.md`).

### Hướng dẫn sử dụng không cần clone repo (Copy Agent Prompt)

Mở trang [teardown trên VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&sources=teardown), chọn agent (Claude Code, Cursor, Codex, Antigravity...), bấm **Copy Agent Prompt** và dán vào cửa sổ chat của dự án.

Agent sẽ đọc manifest `install-manifests/teardown.json`, xác thực SHA-256 từng tệp, tải trọn gói và lưu vào thư mục dự án cùng receipt `.vas-manifest.json` tương thích với CLI.

### Hướng dẫn sử dụng qua CLI (`./vas`)

Từ thư mục checkout VAS:

```bash
# Tìm kiếm skill
./vas search teardown

# Xem chi tiết runbook
./vas show teardown

# Cài đặt vào dự án (chế độ copy độc lập)
./vas install teardown --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Kiểm tra trạng thái cài đặt
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Gỡ bỏ skill khi hoàn thành dự án
./vas uninstall teardown --target claude --dest "/path/to/project/.claude/skills"
```

### Bảng thư mục cài đặt mặc định theo Agent

| Agent | Thư mục cài đặt trong dự án |
|---|---|
| Claude Code | `.claude/skills/teardown/` |
| OpenAI Codex | `.codex/skills/teardown/` |
| Cursor | `.cursor/skills/teardown/` |
| Antigravity | `.agents/skills/teardown/` |
| Windsurf | `.windsurf/skills/teardown/` |
| Cline / Roo Code | `.cline/skills/teardown/` |
| GitHub Copilot CLI | `.github/skills/teardown/` |

### Yêu cầu tiên quyết & Lưu ý an toàn

- **Môi trường hệ thống**:
  - Node.js 18+ (phục vụ `paths.mjs`, `sheet.mjs`, `wave.mjs` và các trình dựng mô phỏng `sims/build.mjs`).
  - Python 3.9+ (thư viện chuẩn, phục vụ bộ tổng hợp âm thanh `run_sfx.py` và `sfx/`).
  - Công cụ trên PATH để xuất video: `ffmpeg` và `playwright` (Chromium).
- **Quyền riêng tư & An toàn**: Tất cả mô hình 3D và thuật toán tính toán chuyển động chạy 100% ngoại tuyến trên trình duyệt chuẩn HTML/Three.js. Không tự động chạy mã tải về hay gọi API trả phí trong quá trình cài đặt `./vas install`.

---

## English

Added **1 new skill / 73 files**, zero duplicates skipped.
Catalog total: **3,186 skills / 119 categories**.
This is the interactive 3D machine and mechanism simulator skill for **Claude Code**, **Cursor**, **Codex**, and **Antigravity**, authored by **Elvar ([@elvarofficial](https://github.com/elvarofficial))** and **whaleyxbt ([@whaleyxbt](https://github.com/whaleyxbt))**:
turn any real machine or mechanism (V8 cross-plane engine, Cessna 337 landing gear, Theo Jansen Strandbeest, gearboxes, pumps) into a single offline 3D HTML simulator that users can inspect and take apart, with live telemetry panels, cutaways, camera angles, an interactive auto tour, and frame-by-frame 60 fps recording with a synchronized procedural score.

Distributed under the **MIT License**, Copyright (c) 2026 elvarofficial and whaleyxbt. 12 audio samples in `sfx/samples/` are licensed under **CC0 1.0 Public Domain** (attribution recorded in `sfx/samples/SOURCES.md`).

### No-Clone Setup (Copy Agent Prompt)

Open [teardown on VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=en&sources=teardown), pick your target coding agent (Claude Code, Cursor, Codex, Antigravity...), click **Copy Agent Prompt**, and paste it into your project chat.

The agent fetches the verified file manifest at `install-manifests/teardown.json`, validates each SHA-256 hash, and saves the standalone payload along with `.vas-manifest.json`.

### CLI Workflow (`./vas`)

```bash
# Discover skill
./vas search teardown

# View runbook
./vas show teardown

# Install into project in standalone copy mode
./vas install teardown --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Check installation receipt
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Uninstall cleanly
./vas uninstall teardown --target claude --dest "/path/to/project/.claude/skills"
```

### Default Agent Installation Directories

| AI Agent | Target Directory |
|---|---|
| Claude Code | `.claude/skills/teardown/` |
| OpenAI Codex | `.codex/skills/teardown/` |
| Cursor | `.cursor/skills/teardown/` |
| Google Antigravity | `.agents/skills/teardown/` |
| Windsurf | `.windsurf/skills/teardown/` |
| Cline / Roo Code | `.cline/skills/teardown/` |
| GitHub Copilot CLI | `.github/skills/teardown/` |

### Prerequisites & Safety Notes

- **Runtime & Tools**:
  - Node.js 18+ (for `paths.mjs`, `sheet.mjs`, `wave.mjs`, and `sims/build.mjs`).
  - Python 3.9+ (standard library only, for `run_sfx.py` and `sfx/`).
  - Tools on PATH for video recording: `ffmpeg` and `playwright` (Chromium).
- **Safety & Privacy**: All 3D simulations run offline in standard browser engines. Zero network calls or external API keys needed during simulation. No background process or downloaded runtime is executed during `./vas install`.
