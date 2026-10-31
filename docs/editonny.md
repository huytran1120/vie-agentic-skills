# editonny trong VAS / editonny in VAS

## Tiếng Việt

Đã thêm **1 skill mới / 2.108 tệp**, không có bản trùng phải bỏ qua.
Catalog: **3.185 skill / 119 danh mục**.
Đây là bộ công cụ biên tập video và motion scenes cục bộ chuyên sâu cho **Claude Code** và **Codex** do tác giả **Matheus Gomes ([@soumatheusgomes](https://github.com/soumatheusgomes))** phát triển:
cắt bỏ khoảng lặng và cảnh quay hỏng, tự động tạo phụ đề bám sát giọng nói, chuẩn hóa âm thanh (-14 LUFS, headroom -1.5 dBTP), căn chỉnh khung hình và chuyển đổi các đoạn lời thoại thành các cảnh chuyển động (145+ visual scenes có sẵn). Toàn bộ quá trình transcribe và render diễn ra cục bộ trên máy tính.

Skill được phát hành theo giấy phép **MIT License**, bản quyền thuộc về **Matheus Gomes**. Toàn bộ mã nguồn, kịch bản, bộ cảnh mẫu (HTML/Canvas), thư viện 3D, âm thanh, hiệu ứng và tài liệu hướng dẫn được đóng gói đầy đủ, giữ nguyên các thông cáo bên thứ ba tại `engine/THIRD_PARTY_NOTICES.md`.

### Hướng dẫn sử dụng không cần clone repo (Copy Agent Prompt)

Mở trang [editonny trên VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&sources=editonny), chọn agent (Claude Code, Cursor, Codex, Antigravity...), bấm **Copy Agent Prompt** và dán vào cửa sổ chat của dự án.

Agent sẽ kiểm tra manifest `install-manifests/editonny.json`, xác thực SHA-256 từng tệp, tải trọn gói và ghi receipt `.vas-manifest.json` tương thích với CLI.

### Hướng dẫn sử dụng qua CLI (`./vas`)

Từ thư mục checkout VAS:

```bash
# Tìm kiếm skill
./vas search editonny

# Xem chi tiết runbook
./vas show editonny

# Cài đặt vào dự án (chế độ copy độc lập)
./vas install editonny --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Kiểm tra trạng thái cài đặt
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Gỡ bỏ skill khi hoàn thành dự án
./vas uninstall editonny --target claude --dest "/path/to/project/.claude/skills"
```

### Bảng thư mục cài đặt mặc định theo Agent

| Agent | Thư mục cài đặt trong dự án |
|---|---|
| Claude Code | `.claude/skills/editonny/` |
| OpenAI Codex | `.codex/skills/editonny/` |
| Cursor | `.cursor/skills/editonny/` |
| Antigravity | `.agents/skills/editonny/` |
| Windsurf | `.windsurf/skills/editonny/` |
| Cline / Roo Code | `.cline/skills/editonny/` |
| GitHub Copilot CLI | `.github/skills/editonny/` |

### Yêu cầu tiên quyết & Lưu ý an toàn

- **Môi trường hệ thống**:
  - Python 3.9+ cho launcher; engine yêu cầu Python >=3.10,<3.14 thông qua `uv`.
  - Công cụ trên PATH: `ffmpeg`, `ffprobe`, Node.js (22.13+ hoặc 24+) kèm `npx`.
  - Trình đọc OCR cục bộ tùy chọn để xác thực phụ đề: Apple Vision (macOS) hoặc Tesseract.
- **Quyền riêng tư & API**: Quá trình transcribe và render chạy hoàn toàn offline trên máy tính, không yêu cầu API key LLM. Các dịch vụ tạo sinh bên thứ ba (ElevenLabs, v.v.) chỉ là tùy chọn và chỉ chạy khi có sự cấp phép rõ ràng từ người dùng.

---

## English

Added **1 new skill / 2,108 files**, zero duplicates skipped.
Catalog total: **3,185 skills / 119 categories**.
This is the complete local video editing and visual scenes suite for **Claude Code** and **Codex**, authored by **Matheus Gomes ([@soumatheusgomes](https://github.com/soumatheusgomes))**:
cut dead air and mistakes, generate faithful captions, balance voice audio (-14 LUFS with -1.5 dBTP headroom), reframe, and turn spoken points into animated motion scenes (145+ ready-to-use scenes) from natural language prompts. Transcription and rendering run entirely on your computer.

Distributed under the **MIT License**, Copyright (c) 2026 Matheus Gomes. Third-party notices for adapted helpers, bundled fonts, models, and recordings are preserved in `engine/THIRD_PARTY_NOTICES.md`.

### No-Clone Setup (Copy Agent Prompt)

Open [editonny in the VAS catalog](https://huytran1120.github.io/vie-agentic-skills/?lang=en&sources=editonny), select your target agent, click **Copy Agent Prompt**, and paste it into your agent's chat box.

Your agent verifies `install-manifests/editonny.json`, validates SHA-256 checksums, downloads the complete package, and writes a CLI-compatible `.vas-manifest.json` receipt.

### CLI Setup (`./vas`)

Run from your local VAS repository clone:

```bash
# Search for editonny
./vas search editonny

# Show runbook and details
./vas show editonny

# Install into your project directory (copy mode)
./vas install editonny --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Check installation status
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Cleanly uninstall
./vas uninstall editonny --target claude --dest "/path/to/project/.claude/skills"
```

### Agent Installation Directory Mapping

| Agent | Project Destination Path |
|---|---|
| Claude Code | `.claude/skills/editonny/` |
| OpenAI Codex | `.codex/skills/editonny/` |
| Cursor | `.cursor/skills/editonny/` |
| Antigravity | `.agents/skills/editonny/` |
| Windsurf | `.windsurf/skills/editonny/` |
| Cline / Roo Code | `.cline/skills/editonny/` |
| GitHub Copilot CLI | `.github/skills/editonny/` |

### Prerequisites & Safety Notes

- **System Requirements**:
  - Python 3.9+ for the launcher; engine requires Python >=3.10,<3.14 via `uv`.
  - Tools on PATH: `ffmpeg`, `ffprobe`, Node.js (22.13+ or 24+) with `npx`.
  - Optional local OCR for caption verification: Apple Vision (macOS) or Tesseract.
- **Privacy & Permissions**: Local transcription and rendering do not require an LLM API key. External generative services are strictly opt-in and require explicit user consent and separate API credentials.
