# Appllama Mobile App Design & Research trong VAS / Appllama Mobile App Design & Research in VAS

## Tiếng Việt

Đã thêm **2 skill mới / 15 tệp**, không có bản trùng phải bỏ qua.
Upstream: [`Appllama/appllama-skills`](https://github.com/Appllama/appllama-skills) tại revision `dd5caaec3d5d50ad7fc0324da238119c6b7c3707`.
Catalog: **3.875 skill / 119 danh mục**.

Bộ đôi kỹ năng thiết kế và nghiên cứu ứng dụng di động đỉnh cao (Mobile App Design & Top-Grossing Intelligence) dành cho **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline** và **GitHub Copilot CLI** do **Appllama ([appllama.io](https://appllama.io))** phát triển:
kết hợp phương pháp nghiên cứu mẫu giao diện thực chiến từ các ứng dụng đạt doanh thu hàng đầu (top-grossing apps) với chuẩn mực xây dựng giao diện native cao cấp (Expo / React Native) được kiểm chứng trực tiếp trên simulator.

Cả hai kỹ năng được phát hành theo giấy phép **MIT License**, bản quyền thuộc về **Antmind Ventures Private Limited (appllama.io)**.

### Danh sách 2 kỹ năng Appllama

1. **`appllama-app-design-skill`**:
   - **Xây dựng giao diện Expo / React Native chuẩn native**: Tuân thủ tuyệt đối Apple Human Interface Guidelines (HIG), màu sắc ngữ nghĩa (semantic colors), điều khiển native, và kỷ luật "anti-slop" (không tạo giao diện cẩu thả).
   - **Kiến trúc điều hướng & hoạt họa**: Phân biệt rành mạch push vs replace, modal vs sheet vs overlay, và các điểm chặn "one-way door" không được phép quay lại. Hoạt họa Reanimated mượt mà, lò xo (spring physics) theo sát vận tốc ngón tay, không block JS thread.
   - **Tài liệu tham khảo chuyên sâu đi kèm**:
     - `references/image-assets.md`: Quy chuẩn sinh tài nguyên đồ họa & icon đồng bộ phong cách.
     - `references/native-controls.md`: Lựa chọn và kết nối điều khiển chuẩn iOS & Android.
     - `references/motion.md`: Quy tắc hoạt họa Reanimated, gesture handling và physics.
     - `references/performance.md`: Triệt tiêu giật lag (jank), tối ưu TTI, giảm kích thước bundle.
     - `references/simulator-loop.md`: Danh mục kiểm tra từng frame trên iOS Simulator / Android Emulator.

2. **`appllama-usage`**:
   - **Động cơ nghiên cứu & phân tích**: Khai thác kho thư viện thiết kế của các app dẫn đầu doanh thu thị trường (real screens, onboarding flows, paywalls, UI patterns).
   - **Kịch bản thực chiến**:
     - `references/build-from-scratch.md`: Quy trình xây dựng app mới toanh từ nghiên cứu đối thủ top đầu.
     - `references/improve-a-screen.md`: Phân tích và nâng cấp một màn hình hiện có để tăng chuyển đổi.
     - `references/research-methods.md`: Phương pháp nghiên cứu luồng trải nghiệm và phần tử UI.
     - `agents/openai.yaml`: Định nghĩa tích hợp cho OpenAI Codex.

### Hướng dẫn sử dụng không cần clone repo (Copy Agent Prompt)

Mở trang [Appllama trên VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&sources=appllama), chọn agent (Antigravity, Cursor, Claude Code, Codex...), bấm **Copy Agent Prompt** và dán vào cửa sổ chat của dự án.

Agent sẽ đọc manifest `install-manifests/<canonical-id>.json`, xác thực SHA-256 từng tệp (bao gồm `SKILL.md`, `LICENSE`, `NOTICE.md` và toàn bộ thư mục `references/`), tải trọn gói và lưu vào thư mục dự án cùng receipt `.vas-manifest.json` tương thích với CLI.

### Hướng dẫn sử dụng qua CLI (`./vas`)

Từ thư mục checkout VAS:

```bash
# Tìm kiếm kỹ năng
./vas search appllama

# Xem chi tiết runbook
./vas show appllama-app-design-skill
./vas show appllama-usage

# Cài đặt chế độ copy độc lập vào dự án
./vas install appllama-app-design-skill --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Cài đặt chế độ link symlink
./vas install appllama-usage --target antigravity --mode link

# Kiểm tra trạng thái cài đặt
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Gỡ bỏ kỹ năng khi hoàn thành dự án
./vas uninstall appllama-app-design-skill --target claude --dest "/path/to/project/.claude/skills"
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

- **Môi trường & Dịch vụ**:
  - `appllama-app-design-skill` hoạt động độc lập 100% không yêu cầu bất kỳ tài khoản hay MCP server nào.
  - `appllama-usage` tùy chọn kết nối với Appllama MCP (`https://mcp.appllama.io/mcp`) để tìm kiếm dữ liệu màn hình trực tiếp; các tài liệu hướng dẫn nghiên cứu offline có sẵn không cần kết nối.
- **Quyền riêng tư & An toàn**: Quá trình cài đặt `./vas install` chỉ sao chép hoặc tạo liên kết tệp tin tĩnh và ghi receipt `.vas-manifest.json`. Không tự động chạy mã, không cài đặt runtime hay kết nối dịch vụ ngoài lúc cài đặt.

---

## English

Added **2 new skills / 15 files**, zero duplicates skipped.
Upstream: [`Appllama/appllama-skills`](https://github.com/Appllama/appllama-skills) at revision `dd5caaec3d5d50ad7fc0324da238119c6b7c3707`.
Catalog total: **3,875 skills / 119 categories**.

This is the mobile app design and top-grossing UI research skill suite for **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline**, and **GitHub Copilot CLI**, authored by **Appllama ([appllama.io](https://appllama.io))**:
turning the real screens, onboarding flows, and UI patterns of top-grossing mobile apps into an agent's working method, finished to an Apple HIG and simulator-verified native bar.

All skills are distributed under the **MIT License**, Copyright (c) 2026 Antmind Ventures Private Limited (appllama.io).

### 2 Appllama Skills

1. **`appllama-app-design-skill`**:
   - Native-feeling Expo / React Native mobile UI engineering: Apple HIG fidelity, semantic colors, native controls, anti-slop discipline, navigation semantics (push vs replace, sheets, one-way doors), Reanimated motion on UI thread, and full-motion simulator loop.
   - Complete bundled references:
     - `references/image-assets.md`: Cohesive asset & icon generation system.
     - `references/native-controls.md`: Platform-native iOS and Android controls.
     - `references/motion.md`: Reanimated gesture handling, spring physics, and frame budgets.
     - `references/performance.md`: Jank prevention, TTI optimization, bundle slimming.
     - `references/simulator-loop.md`: Frame-by-frame simulator verification checklist.

2. **`appllama-usage`**:
   - The research engine: querying real screens, paywalls, and UX flows from top-grossing apps via the Appllama MCP.
   - Comprehensive playbooks:
     - `references/build-from-scratch.md`: End-to-end workflow building an app from market research.
     - `references/improve-a-screen.md`: Auditing and elevating an existing screen against category leaders.
     - `references/research-methods.md`: Systematic flow and element research methodologies.
     - `agents/openai.yaml`: OpenAI Codex agent configuration.

### No-Clone Web Quickstart (Copy Agent Prompt)

Open [Appllama on VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=en&sources=appllama), pick your coding agent (Antigravity, Cursor, Claude Code, Codex, etc.), click **Copy Agent Prompt**, and paste it into your project chat window.

Your agent reads `install-manifests/<canonical-id>.json`, verifies every SHA-256 hash, downloads the complete payload, and saves the CLI-compatible `.vas-manifest.json` receipt.

### CLI Instructions (`./vas`)

From your local VAS repository checkout:

```bash
# Search for skills
./vas search appllama

# View skill runbook
./vas show appllama-app-design-skill
./vas show appllama-usage

# Install in copy mode
./vas install appllama-app-design-skill --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Install in symlink mode
./vas install appllama-usage --target antigravity --mode link

# Check status
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Uninstall skill
./vas uninstall appllama-app-design-skill --target claude --dest "/path/to/project/.claude/skills"
```

### Default Agent Installation Destinations

| Agent | Default Project Destination |
|---|---|
| Google Antigravity | `.agents/skills/<skill-id>/` |
| OpenAI Codex | `.codex/skills/<skill-id>/` |
| Claude Code | `.claude/skills/<skill-id>/` |
| Cursor | `.cursor/skills/<skill-id>/` |
| Windsurf | `.windsurf/skills/<skill-id>/` |
| Cline / Roo Code | `.cline/skills/<skill-id>/` |
| GitHub Copilot CLI | `.github/skills/<skill-id>/` |

### Prerequisites & Safety Notes

- **Environment Configuration**:
  - `appllama-app-design-skill` is completely standalone and operates with zero external network or account requirements.
  - `appllama-usage` optionally interfaces with the Appllama MCP (`https://mcp.appllama.io/mcp`) for live top-grossing app screen queries; offline design guidelines run safely without network dependencies.
- **Safe Operation**: Installation via `./vas install` only copies or symlinks static files and writes the `.vas-manifest.json` receipt. No executable scripts, runtimes, MCP servers, or background services are executed during installation.
