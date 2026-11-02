# Claude Code Game Studios trong VAS / Claude Code Game Studios in VAS

## Tiếng Việt

Đã thêm **74 skill mới / 485 tệp**, không có bản trùng phải bỏ qua.
5 skill có tên trùng với catalog hiện có được phân tách bằng tiền tố namespace `gamestudio-` (`gamestudio-architecture-review`, `gamestudio-code-review`, `gamestudio-design-system`, `gamestudio-prototype`, `gamestudio-security-audit`).
Catalog: **3.429 skill / 119 danh mục**.

Đây là bộ quy trình studio phát triển game toàn diện (Game Development Studio Workflow) dành cho **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline** và **GitHub Copilot CLI** do tác giả **Donchitos ([@Donchitos](https://github.com/Donchitos))** phát triển:
biến một phiên làm việc AI thành cấu trúc studio làm game thực thụ với phân cấp trách nhiệm rõ ràng, cổng kiểm soát chất lượng (quality gates) và quy trình phối hợp khép kín giữa các bộ phận.

Bộ kỹ năng tương thích với các game engine phổ biến (**Godot 4**, **Unity**, **Unreal Engine 5**) và hỗ trợ toàn bộ vòng đời sản xuất game:
1. **Khởi tạo & Thiết kế**: `start`, `brainstorm`, `quick-design`, `art-bible`, `team-narrative`, `team-audio`, `team-combat`, `team-level`, `review-all-gdds`.
2. **Kiến trúc & Cấu hình Engine**: `setup-engine`, `create-architecture`, `map-systems`, `architecture-decision`, `gamestudio-architecture-review`, `gamestudio-design-system`.
3. **Quản lý Sản xuất & Pipeline**: `create-control-manifest`, `create-epics`, `create-stories`, `dev-story`, `story-readiness`, `story-done`, `vertical-slice`, `sprint-plan`, `sprint-status`.
4. **Kiểm thử & Đảm bảo chất lượng (QA)**: `test-setup`, `test-helpers`, `qa-plan`, `team-qa`, `test-evidence-review`, `test-flakiness`, `regression-suite`, `smoke-check`, `soak-test`, `gate-check`, `bug-report`, `bug-triage`.
5. **Đánh bóng & Phát hành**: `team-polish`, `team-release`, `localize`, `perf-profile`, `tech-debt`, `release-checklist`, `launch-checklist`, `patch-notes`, `changelog`, `day-one-patch`, `hotfix`, `retrospective`.

Mỗi skill được đóng gói độc lập kèm theo đầy đủ hợp đồng (`CONTRACT.md`), tài liệu tham chiếu (`references/`), script hỗ trợ (`scripts/`) và biểu mẫu (`templates/`) để có thể cài đặt và sử dụng riêng lẻ.

Skill được phát hành theo giấy phép **MIT License**, bản quyền thuộc về **Donchitos**.

### Hướng dẫn sử dụng không cần clone repo (Copy Agent Prompt)

Mở trang [Claude Code Game Studios trên VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&sources=gamestudios), chọn agent (Antigravity, Cursor, Claude Code, Codex...), bấm **Copy Agent Prompt** và dán vào cửa sổ chat của dự án.

Agent sẽ đọc manifest từ `install-manifests/<skill-id>.json`, xác thực SHA-256 từng tệp, tải trọn gói và lưu vào thư mục dự án cùng receipt `.vas-manifest.json` tương thích với CLI.

### Hướng dẫn sử dụng qua CLI (`./vas`)

Từ thư mục checkout VAS:

```bash
# Tìm kiếm các skill game studio
./vas search gamestudio

# Xem chi tiết runbook của một skill
./vas show setup-engine

# Cài đặt một skill vào dự án (chế độ copy độc lập)
./vas install setup-engine --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Cài đặt toàn bộ bộ sưu tập Game Studios
./vas install start brainstorm setup-engine gate-check dev-story --target antigravity --mode link

# Kiểm tra trạng thái cài đặt
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Gỡ bỏ skill khi hoàn thành
./vas uninstall setup-engine --target claude --dest "/path/to/project/.claude/skills"
```

### Bảng thư mục cài đặt mặc định theo Agent

| Agent | Thư mục cài đặt trong dự án |
|---|---|
| Google Antigravity | `.agents/skills/<skill-id>/` |
| OpenAI Codex | `.codex/skills/<skill-id>/` |
| Claude Code | `.claude/skills/<skill-id>/` |
| Cursor | `.cursor/skills/<skill-id>/` |
| Windsurf | `.windsurf/skills/<skill-id>/` |
| Cline / Roo Code | `.cline/skills/<skill-id>/` |
| GitHub Copilot CLI | `.github/skills/<skill-id>/` |

### Yêu cầu tiên quyết & Lưu ý an toàn

- **Môi trường hệ thống**:
  - Python 3 và môi trường Bash (macOS/Linux sẵn có; Windows dùng Git Bash).
  - Game Engine tương ứng cho dự án của bạn: Godot 4.x (GDScript/C#), Unity (C#) hoặc Unreal Engine 5.x (C++/Blueprint).
- **Quyền riêng tư & An toàn**: Quá trình cài đặt `./vas install` chỉ sao chép hoặc tạo liên kết tệp tin tĩnh và ghi receipt `.vas-manifest.json`. Không tự động chạy mã, không cài đặt runtime/MCP hay mở cổng dịch vụ trong lúc cài đặt.

---

## English

Added **74 new skills / 485 files**, zero duplicates skipped.
5 skills with colliding catalog names use the `gamestudio-` namespace prefix (`gamestudio-architecture-review`, `gamestudio-code-review`, `gamestudio-design-system`, `gamestudio-prototype`, `gamestudio-security-audit`).
Catalog total: **3,429 skills / 119 categories**.

This is the comprehensive Game Development Studio Workflow suite for **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline**, and **GitHub Copilot CLI**, authored by **Donchitos ([@Donchitos](https://github.com/Donchitos))**:
turns a single AI session into a disciplined game development studio with structured hierarchies, rigorous quality gates, and cross-functional coordination.

Compatible with major engines (**Godot 4**, **Unity**, **Unreal Engine 5**) across the entire production lifecycle:
1. **Design & Vision**: `start`, `brainstorm`, `quick-design`, `art-bible`, `team-narrative`, `team-audio`, `team-combat`, `team-level`, `review-all-gdds`.
2. **Architecture & Setup**: `setup-engine`, `create-architecture`, `map-systems`, `architecture-decision`, `gamestudio-architecture-review`, `gamestudio-design-system`.
3. **Production Pipeline**: `create-control-manifest`, `create-epics`, `create-stories`, `dev-story`, `story-readiness`, `story-done`, `vertical-slice`, `sprint-plan`, `sprint-status`.
4. **Quality Assurance & Testing**: `test-setup`, `test-helpers`, `qa-plan`, `team-qa`, `test-evidence-review`, `test-flakiness`, `regression-suite`, `smoke-check`, `soak-test`, `gate-check`, `bug-report`, `bug-triage`.
5. **Polish & Release**: `team-polish`, `team-release`, `localize`, `perf-profile`, `tech-debt`, `release-checklist`, `launch-checklist`, `patch-notes`, `changelog`, `day-one-patch`, `hotfix`, `retrospective`.

Every skill is self-contained with its own contracts (`CONTRACT.md`), reference documentation (`references/`), helper scripts (`scripts/`), and design templates (`templates/`).

The suite is released under the **MIT License**, Copyright (c) 2026 Donchitos.

### No-Clone Web Quickstart (Copy Agent Prompt)

Open [Claude Code Game Studios on VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=en&sources=gamestudios), pick your coding agent (Antigravity, Cursor, Claude Code, Codex, etc.), click **Copy Agent Prompt**, and paste it into your project chat window.

### CLI Instructions (`./vas`)

From your local VAS repository checkout:

```bash
# Search for game studio skills
./vas search gamestudio

# View skill runbook
./vas show setup-engine

# Install a skill in copy mode
./vas install setup-engine --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Check installation status
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Uninstall skill
./vas uninstall setup-engine --target claude --dest "/path/to/project/.claude/skills"
```

### Default Target Directory Mapping

| Agent | Project Install Location |
|---|---|
| Google Antigravity | `.agents/skills/<skill-id>/` |
| OpenAI Codex | `.codex/skills/<skill-id>/` |
| Claude Code | `.claude/skills/<skill-id>/` |
| Cursor | `.cursor/skills/<skill-id>/` |
| Windsurf | `.windsurf/skills/<skill-id>/` |
| Cline / Roo Code | `.cline/skills/<skill-id>/` |
| GitHub Copilot CLI | `.github/skills/<skill-id>/` |

### Prerequisites & Safety Notes

- **System Requirements**:
  - Python 3 and Bash environment.
  - Game Engine corresponding to your project: Godot 4.x, Unity, or Unreal Engine 5.x.
- **Safety**: Installation via `./vas install` only copies or symlinks static files and records `.vas-manifest.json`. No runtime/dependency is executed and no external services are contacted during installation.
