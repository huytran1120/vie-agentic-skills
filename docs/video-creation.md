# Claude Awesome Video Creation trong VAS / Claude Awesome Video Creation in VAS

## Tiếng Việt

Đã thêm **1 skill mới (`claude-awesome-video-creation`) / 194 tệp**, không có bản trùng phải bỏ qua.
Upstream: [`HaochenSHI66/claude-awesome-video-creation`](https://github.com/HaochenSHI66/claude-awesome-video-creation) tại revision `4b0f8d89d50046ac13003e95bcde081e328c2373`.
Catalog: **3.885 skill / 119 danh mục**.

Kỹ năng **`claude-awesome-video-creation`** do **SHI Haochen ([@HaochenSHI66](https://github.com/HaochenSHI66))** phát triển (dựa trên nền tảng **cinetic** của **Leonxlnx**) dành cho **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline** và **GitHub Copilot CLI**:
hướng dẫn AI coding agents xây dựng trọn gói video hướng dẫn (tutorial) và video giải thích sản phẩm (explainer) trực tiếp từ code với Remotion (React):
từ kịch bản và thu âm lồng tiếng (draft TTS hoặc giọng clone với timing từng từ), dòng thời gian khóa theo nhịp beat điều phối hình ảnh, phụ đề tự động và nhạc nền viết bằng code, giao diện terminal kính phong cách macOS với tô màu cú pháp, nhân vật mascot người dẫn hoạt họa có cử động khẩu hình (lip-sync), render phân đoạn tránh treo Chrome headless, và kiểm thử QA có đo lường (quét khung hình đóng băng, tạo contact sheet, chuẩn hóa âm lượng -14 LUFS).

Kỹ năng được phát hành theo giấy phép **MIT License**, bản quyền thuộc về **SHI Haochen** và **Leonxlnx**.

### Cấu trúc tệp đính kèm trong `skills/claude-awesome-video-creation/`

- `SKILL.md`: Runbook chính hướng dẫn cấu trúc video follow-along, quy tắc làm video học tập, quy trình lồng tiếng, thiết kế giao diện và các cổng kiểm thử QA.
- `references/` (25 tài liệu chuyên sâu):
  - `lessons.md`: Các quy tắc rút ra từ phản hồi thực tế của khán giả học viên.
  - `voiceover.md`: Định dạng kịch bản, timing từ, draft TTS và clone giọng nói.
  - `look-tutorial.md`: Bảng màu stage navy, aurora light, terminal kính Cobalt2 và tô màu cú pháp.
  - `mascot.md`: Quy trình tạo và điều khiển nhân vật mascot (19 sprite, cử động môi viseme, chuyển cảnh, nhảy, xoay).
  - `render-qa.md`: Kỹ thuật render phân đoạn (segmented render) và các bài kiểm tra QA bắt buộc.
  - `cinetic-core.md`, `craft-rules.md`, `finishing.md`, `technique-library.md` và các tài liệu kế thừa từ cinetic.
- `scripts/` (31 công cụ hỗ trợ):
  - `render_segments.sh`: Script render từng đoạn video rồi ghép lại, tránh deadlock GPU.
  - `check_static.py`: Quét phát hiện khung hình đứng/đóng băng bất thường.
  - `sheet.sh` & `sheet.py`: Xuất contact sheet kiểm tra toàn bộ nhịp độ video.
  - `key_magenta.py`: Tách nền magenta cho chuỗi sprite mascot.
  - `audio/`: Bộ script tổng hợp nhạc nền, kiểm tra âm lượng và phối khí.
  - `test/`: Bộ kiểm thử đơn vị cho các script hỗ trợ.
- `assets/`:
  - `examples/teach-it-once/`: Mã nguồn đầy đủ của video mẫu "Teach It Once" (1:54) kèm toàn bộ 19 sprite mascot.
  - `remotion-starter/`: Khung dự án Remotion mẫu sẵn sàng phát triển.
  - `hyperframes-starter/`: Khung dự án HyperFrames tương thích.
  - `critics/` & `library/`: Thư viện kỹ thuật chuyển động và checklist đánh giá.

### Hướng dẫn sử dụng không cần clone repo (Copy Agent Prompt)

Mở trang [Video Creation trên VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&sources=videocreation), chọn agent (Antigravity, Cursor, Claude Code, Codex...), bấm **Copy Agent Prompt** và dán vào cửa sổ chat của dự án.

Agent sẽ đọc manifest `install-manifests/claude-awesome-video-creation.json`, xác thực SHA-256 từng tệp (toàn bộ 194 tệp bao gồm references, scripts và assets), tải trọn gói và lưu vào thư mục dự án cùng receipt `.vas-manifest.json` tương thích với CLI.

### Hướng dẫn sử dụng qua CLI (`./vas`)

Từ thư mục checkout VAS:

```bash
# Tìm kiếm kỹ năng video creation
./vas search claude-awesome-video-creation
./vas search remotion

# Xem chi tiết runbook
./vas show claude-awesome-video-creation

# Cài đặt vào dự án (chế độ copy độc lập)
./vas install claude-awesome-video-creation --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Cài đặt liên kết (chế độ link symlink)
./vas install claude-awesome-video-creation --target antigravity --mode link

# Kiểm tra trạng thái cài đặt
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Gỡ bỏ kỹ năng khi hoàn thành dự án
./vas uninstall claude-awesome-video-creation --target claude --dest "/path/to/project/.claude/skills"
```

### Bảng thư mục cài đặt mặc định theo Agent

| Agent | Thư mục cài đặt trong dự án |
|---|---|
| Google Antigravity | `.agents/skills/claude-awesome-video-creation/` |
| OpenAI Codex | `.codex/skills/claude-awesome-video-creation/` |
| Claude Code | `.claude/skills/claude-awesome-video-creation/` |
| Cursor | `.cursor/skills/claude-awesome-video-creation/` |
| Windsurf | `.windsurf/skills/claude-awesome-video-creation/` |
| Cline / Roo Code | `.cline/skills/claude-awesome-video-creation/` |
| GitHub Copilot CLI | `.github/skills/claude-awesome-video-creation/` |

### Yêu cầu tiên quyết & Lưu ý an toàn

- **Môi trường khuyến nghị khi thực hiện video**:
  - Node.js 22+, Remotion 4+, ffmpeg 6+, Python 3.11+ (kèm `numpy`, `scipy`, `soundfile`, `pyloudnorm`, `pillow`).
  - Tùy chọn: `edge-tts` cho bản nháp voiceover; API key OpenAI/ElevenLabs nếu dùng giọng nhân bản; Codex CLI nếu tự sinh thêm sprite mascot.
- **An toàn**: Quá trình cài đặt `./vas install` chỉ sao chép hoặc liên kết tệp tin tĩnh và ghi receipt `.vas-manifest.json`. Không tự động chạy script, không render hay cài đặt gói npm trong lúc cài đặt.

---

## English

Added **1 new skill (`claude-awesome-video-creation`) / 194 files**, zero duplicates skipped.
Upstream: [`HaochenSHI66/claude-awesome-video-creation`](https://github.com/HaochenSHI66/claude-awesome-video-creation) at revision `4b0f8d89d50046ac13003e95bcde081e328c2373`.
Catalog: **3,885 skills / 119 categories**.

The **`claude-awesome-video-creation`** skill, authored by **SHI Haochen ([@HaochenSHI66](https://github.com/HaochenSHI66))** and built on **cinetic** by **Leonxlnx** for **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline**, and **GitHub Copilot CLI**, provides an end-to-end engineering playbook for producing follow-along coding tutorials and explainer videos from code using Remotion (React):
script & voiceover (draft TTS or cloned voice with word-level cues), a beat-locked timeline, macOS-style glass terminals with syntax highlights, an animated mascot presenter with 19 sprites and viseme lip-sync, segmented rendering to bypass headless Chrome GPU freezes, and rigorous automated QA (frozen frame detection, contact sheets, -14 LUFS loudness normalization).

Distributed under the **MIT License**, Copyright (c) 2026 SHI Haochen and Leonxlnx.

### Bundled Skill Structure

- `SKILL.md`: Main runbook outlining follow-along video structure, pacing rules, voiceover pipeline, glass terminal styling, mascot compositing, and QA gates.
- `references/` (25 guides): `lessons.md`, `voiceover.md`, `look-tutorial.md`, `mascot.md`, `render-qa.md`, `cinetic-core.md`, `technique-library.md`, and more.
- `scripts/` (31 tools): `render_segments.sh`, `check_static.py`, `sheet.sh`, `key_magenta.py`, audio mastering tools in `audio/`, and unit test suite in `test/`.
- `assets/`: Worked example project `teach-it-once` (full source and 19 mascot sprites), `remotion-starter`, and motion technique libraries.

### No-Clone Web Quickstart (Copy Agent Prompt)

Open [Video Creation on VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=en&sources=videocreation), pick your coding agent (Antigravity, Cursor, Claude Code, Codex, etc.), click **Copy Agent Prompt**, and paste it into your project chat window.

Your agent reads `install-manifests/claude-awesome-video-creation.json`, verifies every SHA-256 hash across all 194 files, downloads the payload, and saves the CLI-compatible `.vas-manifest.json` receipt.

### CLI Instructions (`./vas`)

From your local VAS repository checkout:

```bash
# Search for the skill
./vas search claude-awesome-video-creation
./vas search remotion

# View skill runbook
./vas show claude-awesome-video-creation

# Install in copy mode
./vas install claude-awesome-video-creation --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Install in symlink mode
./vas install claude-awesome-video-creation --target antigravity --mode link

# Check status
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Uninstall skill
./vas uninstall claude-awesome-video-creation --target claude --dest "/path/to/project/.claude/skills"
```

### Default Agent Installation Destinations

| Agent | Default Project Destination |
|---|---|
| Google Antigravity | `.agents/skills/claude-awesome-video-creation/` |
| OpenAI Codex | `.codex/skills/claude-awesome-video-creation/` |
| Claude Code | `.claude/skills/claude-awesome-video-creation/` |
| Cursor | `.cursor/skills/claude-awesome-video-creation/` |
| Windsurf | `.windsurf/skills/claude-awesome-video-creation/` |
| Cline / Roo Code | `.cline/skills/claude-awesome-video-creation/` |
| GitHub Copilot CLI | `.github/skills/claude-awesome-video-creation/` |
