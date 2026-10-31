# Scenario Creative AI & DCC trong VAS / Scenario Creative AI & DCC in VAS

## Tiếng Việt

Đã thêm **167 skill mới / 1.717 tệp** từ [scenario-labs/skills](https://github.com/scenario-labs/skills) (commit `7f4b801c7248d51b093ec365aceb114bd06139e6`), không có bản trùng lặp trong toàn bộ catalog. Đã bỏ qua 7 skill nội bộ CI/dev repo (`.agents/skills/*`).
Catalog hiện tại: **3.353 skill / 119 danh mục**.

Bộ kỹ năng toàn diện dành cho sáng tạo nội dung số, tạo sinh AI và phát triển game trên **Claude Code**, **Cursor**, **OpenAI Codex**, **Google Antigravity**, **Windsurf**, **Cline / Roo Code** và **GitHub Copilot CLI** do **Scenario Inc. ([@scenario-labs](https://github.com/scenario-labs))** phát triển:
1. **Scenario AI Generative Suite** (78 skill, danh mục `media`): Tạo hình ảnh, video, audio, nhạc nền (ACE-Step), 3D Gaussian splatting (3D Worlds), character consistency, motion loop, video-to-motion, upscale và asset curation thông qua giao thức MCP Scenario.
2. **Blender Production Suite** (17 skill, danh mục `blender`): Hoạt hình 2D/3D, blockout, geometry nodes, grease pencil, hair groom, hard-surface modeling, lighting & rendering, previs/storyboarding, retopology, rigging, sculpting, texturing & shading, uv baking và điều phối tổng thể (`scenario-blender-expert`).
3. **Game Engines & DCC Suites** (72 skill, danh mục `game-development`):
   - **Autodesk Maya** (11 skill): Animation, deformation, FX, grooming, lighting, lookdev, modeling, pipeline scripting, retopology & UV, rigging và router `scenario-maya-expert`.
   - **Pixologic ZBrush** (9 skill): Automation, character/creature, hard-surface, polypaint & render, 3D printing pose, retopology export, sculpting, stylized modeling và router `scenario-zbrush-expert`.
   - **Godot Engine 4.x** (14 skill): 2D/3D gameplay, animation, architecture, audio, multiplayer, performance & export, pipeline automation, shaders, UI, VFX và router `scenario-godot-expert`.
   - **Roblox Studio / Luau** (14 skill): Animation, architecture, assets, data stores, environment, gameplay, monetization, networking, performance, tooling, UI, VFX & audio và router `scenario-roblox-expert`.
   - **Unity** (14 skill): 2D gameplay, animation, architecture, mobile, performance, pipeline automation, rendering & lighting, shaders, UI, VFX, WebGL, world building và router `scenario-unity-expert`.
   - **Unreal Engine 5** (10 skill): Animation, cinematics (Sequencer), gameplay (Blueprints/C++), lighting & Lumen rendering, materials, performance & profiling, pipeline automation, Niagara VFX, world building (Nanite/World Partition) và router `scenario-unreal-expert`.

Toàn bộ được phát hành theo giấy phép **MIT License**, bản quyền thuộc về **Scenario Inc.**. Các script thực thi (22 scripts) giữ nguyên cờ thực thi `0o755`, toàn bộ shader, template và tài liệu tham khảo được đóng gói độc lập.

### Hướng dẫn sử dụng không cần clone repo (Copy Agent Prompt)

Mở trang [Scenario trên VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&sources=scenario), chọn skill cần dùng (ví dụ: `scenario-blender-expert`, `scenario-godot-expert`, `scenario-unity-shaders`, `scenario-3d-worlds`...), chọn agent mục tiêu, bấm **Copy Agent Prompt** và dán vào cửa sổ chat của dự án.

Agent sẽ đọc manifest `install-manifests/<canonical-id>.json`, xác thực mã băm SHA-256 từng tệp, tải gói hoàn chỉnh và ghi nhận receipt `.vas-manifest.json` tương thích với CLI.

### Hướng dẫn sử dụng qua CLI (`./vas`)

Từ thư mục checkout VAS:

```bash
# Tìm kiếm các skill Scenario
./vas search scenario

# Xem chi tiết một skill
./vas show scenario-blender-expert
./vas show scenario-godot-architecture

# Cài đặt một skill vào dự án (chế độ copy độc lập)
./vas install scenario-blender-expert --target claude --mode copy --dest "/path/to/project/.claude/skills"
./vas install scenario-godot-2d --target cursor --mode link

# Cài đặt theo nhóm tag
./vas install --tag godot --target cursor --mode link

# Kiểm tra trạng thái cài đặt
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Gỡ bỏ skill khi xong việc
./vas uninstall scenario-blender-expert --target claude --dest "/path/to/project/.claude/skills"
```

### Bảng thư mục cài đặt mặc định theo Agent

| Agent | Thư mục cài đặt trong dự án |
|---|---|
| Claude Code | `.claude/skills/<canonical-id>/` |
| OpenAI Codex | `.codex/skills/<canonical-id>/` |
| Cursor | `.cursor/skills/<canonical-id>/` |
| Antigravity | `.agents/skills/<canonical-id>/` |
| Windsurf | `.windsurf/skills/<canonical-id>/` |
| Cline / Roo Code | `.cline/skills/<canonical-id>/` |
| GitHub Copilot CLI | `.github/skills/<canonical-id>/` |

### Yêu cầu tiên quyết & Lưu ý an toàn

- **Môi trường phần mềm**:
  - Với các skill AI tạo sinh (nhóm `scenario-*` media): Tài khoản Scenario và cấu hình MCP server (tùy chọn khi cần chạy tác vụ sinh ảnh/video trực tiếp).
  - Với các suite DCC & Game Engine: Cài đặt phần mềm tương ứng trên máy phát triển (Blender 5.x, Maya, ZBrush, Godot 4.x, Roblox Studio, Unity 2022/6, Unreal Engine 5.x).
- **Quyền riêng tư & An toàn**: Quá trình cài đặt `./vas install` chỉ sao chép hoặc tạo liên kết tệp tin, tuyệt đối không tự ý chạy script, không cài đặt runtime ngầm, không tự ý kết nối dịch vụ ngoài hay thu phí.

---

## English

Added **167 new skills / 1,717 files** from [scenario-labs/skills](https://github.com/scenario-labs/skills) (commit `7f4b801c7248d51b093ec365aceb114bd06139e6`), zero duplicates across the catalog. 7 internal CI/dev skills (`.agents/skills/*`) were skipped.
Catalog total: **3,353 skills / 119 categories**.

Comprehensive creative AI, DCC, and game engine mastery for **Claude Code**, **Cursor**, **OpenAI Codex**, **Google Antigravity**, **Windsurf**, **Cline / Roo Code**, and **GitHub Copilot CLI**, authored by **Scenario Inc. ([@scenario-labs](https://github.com/scenario-labs))**:
1. **Scenario AI Generative Suite** (78 skills, category `media`): Image, video, audio, lyric music (ACE-Step), 3D Gaussian splats (3D Worlds), character consistency, motion loops, video-to-motion, upscale, and asset pipeline workflows via Scenario MCP.
2. **Blender Production Suite** (17 skills, category `blender`): 2D/3D animation, blockout, geometry nodes, grease pencil, hair groom, hard-surface modeling, lighting & rendering, previs/storyboarding, retopology, rigging, sculpting, texturing & shading, UV baking, and the master router `scenario-blender-expert`.
3. **Game Engines & DCC Suites** (72 skills, category `game-development`):
   - **Autodesk Maya** (11 skills): Animation, deformation, FX, groom, lighting, lookdev, modeling, pipeline scripting, retopology & UV, rigging, and `scenario-maya-expert`.
   - **Pixologic ZBrush** (9 skills): Automation, character/creature, hard-surface, polypaint & render, 3D printing pose, retopology export, sculpting, stylized, and `scenario-zbrush-expert`.
   - **Godot Engine 4.x** (14 skills): 2D/3D gameplay, animation, architecture, audio, multiplayer, performance & export, pipeline automation, shaders, UI, VFX, and `scenario-godot-expert`.
   - **Roblox Studio / Luau** (14 skills): Animation, architecture, assets, data stores, environment, gameplay, monetization, networking, performance, tooling, UI, VFX & audio, and `scenario-roblox-expert`.
   - **Unity** (14 skills): 2D gameplay, animation, architecture, mobile, performance, pipeline automation, rendering & lighting, shaders, UI, VFX, WebGL, world building, and `scenario-unity-expert`.
   - **Unreal Engine 5** (10 skills): Animation, cinematics, gameplay, lighting & Lumen, materials, performance & profiling, pipeline automation, Niagara VFX, world building, and `scenario-unreal-expert`.

Released under the **MIT License**, Copyright (c) 2026 Scenario Inc. All 22 executable scripts preserve mode `0o755`, with independent shaders, templates, and references bundled per skill.

### No-Clone Setup (Copy Agent Prompt)

Visit [Scenario on VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=en&sources=scenario), select the desired skill (e.g. `scenario-blender-expert`, `scenario-godot-expert`, `scenario-unity-shaders`, `scenario-3d-worlds`), select your agent, click **Copy Agent Prompt**, and paste it into your project chat.

The agent fetches the verified file manifest at `install-manifests/<canonical-id>.json`, validates SHA-256 hashes, and installs the standalone payload with a CLI-compatible `.vas-manifest.json` receipt.

### CLI Workflow (`./vas`)

```bash
# Discover Scenario skills
./vas search scenario

# View runbook
./vas show scenario-blender-expert
./vas show scenario-godot-architecture

# Install into project in standalone copy mode
./vas install scenario-blender-expert --target claude --mode copy --dest "/path/to/project/.claude/skills"
./vas install scenario-godot-2d --target cursor --mode link

# Install by tag
./vas install --tag godot --target cursor --mode link

# Check status
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Uninstall cleanly
./vas uninstall scenario-blender-expert --target claude --dest "/path/to/project/.claude/skills"
```

### Default Agent Installation Directories

| AI Agent | Target Directory |
|---|---|
| Claude Code | `.claude/skills/<canonical-id>/` |
| OpenAI Codex | `.codex/skills/<canonical-id>/` |
| Cursor | `.cursor/skills/<canonical-id>/` |
| Google Antigravity | `.agents/skills/<canonical-id>/` |
| Windsurf | `.windsurf/skills/<canonical-id>/` |
| Cline / Roo Code | `.cline/skills/<canonical-id>/` |
| GitHub Copilot CLI | `.github/skills/<canonical-id>/` |

### Prerequisites & Safety Notes

- **Software Prerequisites**:
  - For generative AI skills (media): Scenario account and MCP server (optional, when executing generation workflows).
  - For DCC & Game Engine suites: Respective software installed locally (Blender 5.x, Maya, ZBrush, Godot 4.x, Roblox Studio, Unity 2022/6, Unreal Engine 5.x).
- **Safety & Privacy**: `./vas install` only copies or links verified files. No unapproved scripts are executed, no hidden runtimes are installed, and no paid third-party generation calls are made during installation.
