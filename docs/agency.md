# The Agency · AI Specialists trong VAS / The Agency · AI Specialists in VAS

## Tiếng Việt

Đã thêm **283 skill mới / 849 tệp**, không có bản trùng nội dung phải bỏ qua.
Tất cả các skill được định danh chuẩn với tiền tố `agency-` (theo quy chuẩn upstream Antigravity/Agent-Skills).
Catalog: **3.859 skill / 119 danh mục**.

Đây là bộ sưu tập 283 nhân sự AI chuyên môn hóa (Specialized AI Agent Personas) đến từ dự án **The Agency** ([`msitarzewski/agency-agents`](https://github.com/msitarzewski/agency-agents)), bản quyền thuộc về **AgentLand Contributors ([@msitarzewski](https://github.com/msitarzewski))** tại revision `b37b5bb33b78f2c1d6567d98e25ca818e3259219`, phát hành theo giấy phép **MIT License**.

Bộ kỹ năng này biến các trợ lý lập trình AI như **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline** và **GitHub Copilot CLI** thành một tổ chức Agency chuyên nghiệp, đầy đủ các phòng ban và chức danh:
- **Engineering (Kỹ thuật phần mềm)**: `agency-software-architect`, `agency-backend-developer`, `agency-frontend-developer`, `agency-fullstack-developer`, `agency-devops-engineer`, `agency-cloud-architect`, `agency-database-administrator`, `agency-site-reliability-engineer`, `agency-performance-engineer`, `agency-api-designer`...
- **Design & Creative (Thiết kế & Sáng tạo)**: `agency-ui-designer`, `agency-ux-researcher`, `agency-design-system-architect`, `agency-visual-designer`, `agency-motion-designer`, `agency-accessibility-specialist`...
- **Marketing & Paid Media (Tiếp thị & Truyền thông)**: `agency-growth-hacker`, `agency-content-strategist`, `agency-seo-specialist`, `agency-performance-marketer`, `agency-copywriter`, `agency-social-media-manager`, `agency-funnel-architect`...
- **Product & Project Management (Sản phẩm & Quản lý dự án)**: `agency-product-manager`, `agency-scrum-master`, `agency-technical-program-manager`, `agency-agile-coach`, `agency-release-manager`...
- **Security & Compliance (An ninh mạng & Tuân thủ)**: `agency-security-auditor`, `agency-application-security-engineer`, `agency-cloud-security-architect`, `agency-penetration-tester`, `agency-compliance-officer`...
- **Testing & Quality Assurance (Kiểm thử & Chất lượng)**: `agency-qa-engineer`, `agency-test-automation-architect`, `agency-performance-tester`, `agency-security-tester`...
- **Phòng ban chuyên sâu**: `academic` (học thuật), `finance` (tài chính & kế toán), `game-development` (phát triển game), `gis` (hệ thống thông tin địa lý & bản đồ 3D), `healthcare` (y tế & sức khỏe), `research` (nghiên cứu khoa học), `sales` (kinh doanh & bán hàng), `spatial-computing` (thực tế ảo & điện toán không gian), `support` (chăm sóc khách hàng & kỹ thuật).

Mỗi skill được đóng gói độc lập theo chuẩn Agent-Skills / Antigravity, chứa toàn bộ prompt định danh (`🧠 Your Identity & Memory`), nguyên tắc cốt lõi (`🎯 Your Core Principles`), danh mục sản phẩm bàn giao (`📋 Deliverables & Artifacts`), cùng quy trình làm việc chuẩn (`🔄 Your Workflow Loop`), kèm giấy phép MIT và thông báo bản quyền.

### Hướng dẫn sử dụng không cần clone repo (Copy Agent Prompt)

Mở trang [The Agency trên VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&sources=agency), chọn agent (Antigravity, Cursor, Claude Code, Codex...), bấm **Copy Agent Prompt** và dán vào cửa sổ chat của dự án.

Agent sẽ đọc manifest từ `install-manifests/<canonical-id>.json`, xác thực SHA-256 từng tệp, tải trọn gói và lưu vào thư mục dự án cùng receipt `.vas-manifest.json` tương thích với CLI.

### Hướng dẫn sử dụng qua CLI (`./vas`)

Từ thư mục checkout VAS:

```bash
# Tìm kiếm nhân sự AI theo chuyên môn
./vas search agency-architect
./vas search agency-frontend
./vas search agency-growth

# Xem chi tiết runbook và prompt của một nhân sự
./vas show agency-frontend-developer

# Cài đặt vào dự án (chế độ copy độc lập)
./vas install agency-frontend-developer --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Cài đặt dàn nhân sự nòng cốt vào dự án Antigravity
./vas install agency-software-architect agency-frontend-developer agency-backend-developer agency-qa-engineer --target antigravity --mode link

# Kiểm tra trạng thái cài đặt
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Gỡ bỏ skill khi hoàn thành
./vas uninstall agency-frontend-developer --target claude --dest "/path/to/project/.claude/skills"
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

- **Tương thích**: Chuẩn Open Agent Skills specification (`agentskills.io`), tương thích toàn diện với Antigravity, Claude Code, Cursor, Windsurf, Codex, Cline và GitHub Copilot CLI.
- **An toàn**: Quá trình cài đặt `./vas install` chỉ sao chép hoặc tạo liên kết tệp tin tĩnh và ghi receipt `.vas-manifest.json`. Không tự động chạy mã, không cài đặt runtime/MCP hay mở kết nối mạng trong lúc cài đặt.

---

## English

Added **283 new skills / 849 files**, zero duplicates skipped.
All skills are standardly identified with the `agency-` namespace prefix.
Catalog total: **3,859 skills / 119 categories**.

This is the collection of 283 specialized AI Agent Personas from **The Agency** ([`msitarzewski/agency-agents`](https://github.com/msitarzewski/agency-agents)), Copyright (c) 2025 **AgentLand Contributors ([@msitarzewski](https://github.com/msitarzewski))** at revision `b37b5bb33b78f2c1d6567d98e25ca818e3259219`, released under the **MIT License**.

The suite transforms AI coding assistants like **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline**, and **GitHub Copilot CLI** into an entire agency roster spanning 18 specialized divisions:
- **Engineering**: `agency-software-architect`, `agency-backend-developer`, `agency-frontend-developer`, `agency-fullstack-developer`, `agency-devops-engineer`, `agency-cloud-architect`, `agency-database-administrator`, `agency-site-reliability-engineer`, `agency-performance-engineer`, `agency-api-designer`...
- **Design & Creative**: `agency-ui-designer`, `agency-ux-researcher`, `agency-design-system-architect`, `agency-visual-designer`, `agency-motion-designer`, `agency-accessibility-specialist`...
- **Marketing & Paid Media**: `agency-growth-hacker`, `agency-content-strategist`, `agency-seo-specialist`, `agency-performance-marketer`, `agency-copywriter`, `agency-social-media-manager`, `agency-funnel-architect`...
- **Product & Project Management**: `agency-product-manager`, `agency-scrum-master`, `agency-technical-program-manager`, `agency-agile-coach`, `agency-release-manager`...
- **Security & Compliance**: `agency-security-auditor`, `agency-application-security-engineer`, `agency-cloud-security-architect`, `agency-penetration-tester`, `agency-compliance-officer`...
- **Testing & QA**: `agency-qa-engineer`, `agency-test-automation-architect`, `agency-performance-tester`, `agency-security-tester`...
- **Domain Specialists**: `academic`, `finance`, `game-development`, `gis`, `healthcare`, `research`, `sales`, `spatial-computing`, `support`.

Every skill is self-contained with its full identity persona, core operational principles, concrete deliverables, step-by-step workflow loop, bundled MIT license, and attribution notices.

### No-Clone Web Quickstart (Copy Agent Prompt)

Open [The Agency on VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=en&sources=agency), pick your coding agent (Antigravity, Cursor, Claude Code, Codex, etc.), click **Copy Agent Prompt**, and paste it into your project chat window.

### CLI Quickstart (`./vas`)

From your VAS checkout root:

```bash
# Search for specialized agents
./vas search agency-architect
./vas search agency-frontend

# Inspect an agent runbook
./vas show agency-frontend-developer

# Install standalone into Claude Code
./vas install agency-frontend-developer --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Install core squad into Google Antigravity
./vas install agency-software-architect agency-frontend-developer agency-backend-developer agency-qa-engineer --target antigravity --mode link

# Check installation status
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Clean uninstall
./vas uninstall agency-frontend-developer --target claude --dest "/path/to/project/.claude/skills"
```

### Safety & Prerequisites

- **Compatibility**: Standard Open Agent Skills specification (`agentskills.io`), supported across all modern AI coding agents.
- **Offline & Safe**: Installation strictly creates local symlinks or copies static files and writes `.vas-manifest.json`. No unapproved scripts are executed and no background services are connected.
