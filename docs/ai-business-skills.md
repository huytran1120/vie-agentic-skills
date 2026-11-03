# AI Business Skills trong VAS / AI Business Skills in VAS

## Tiếng Việt

Đã thêm **147 skill mới / 744 tệp**, không có bản trùng nội dung phải bỏ qua.
1 skill có tên trùng với catalog hiện có được phân tách bằng tiền tố namespace `aibiz-` (`aibiz-product-marketing-context`).
Catalog: **3.576 skill / 119 danh mục**.

Đây là bộ quy trình thực chiến toàn diện về Tiếp thị & Kinh doanh ứng dụng AI (AI Marketing & Business Toolkit) dành cho **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline** và **GitHub Copilot CLI** do tác giả **Nguyễn Văn Minh ([@minhnv0807](https://github.com/minhnv0807))** và **Over Powers Agency** phát triển:
biến trợ lý AI lập trình thành dàn chuyên gia Marketing & Kinh doanh thực thụ dành cho solopreneur, nhà sáng lập, agency và doanh nghiệp SME.

Bộ kỹ năng gồm 2 phân hệ chuyên biệt (Cụm Việt Nam và Cụm Toàn Cầu) hỗ trợ toàn bộ vòng đời tiếp thị & bán hàng:
1. **Chiến lược & Lập kế hoạch**: `00-ke-hoach-mkt`, `00-marketing-plan-global`, `02-brief-chien-dich`, `02-campaign-brief-global`, `10-tinh-kpi-nguoc`, `10-reverse-kpi-global`, `58-positioning`, `58-positioning-global`, `59-go-to-market`, `59-go-to-market-global`, `61-budget-planning`, `61-budget-planning-global`, `aibiz-product-marketing-context`, `product-marketing-context-global`.
2. **Sản xuất Nội dung & Sáng tạo**: `01-lich-noi-dung`, `01-content-calendar-global`, `04-script-video`, `04-script-video-global`, `05-copy-quang-cao`, `05-ad-copy-global`, `35-brand-voice`, `35-brand-voice-global`, `36-content-brief`, `36-content-brief-global`, `37-caption-social`, `37-social-caption-global`, `74-copy-hai-lop`.
3. **Thiết kế & Đồ họa**: `30-thiet-ke-master`, `30-design-master-global`, `41-campaign-asset-list`, `42-brief-hinh-anh`, `43-brief-carousel`, `44-brief-video-editor`, `45-brief-canva`, `46-brand-guideline`, `47-design-review`, `48-quick-visual-brief`, `49-html-email-template`, `50-asset-resize`.
4. **Quảng cáo & Tối ưu chuyển đổi (Performance & Ads)**: `21-audit-ads-performance`, `21-ads-audit-global`, `52-account-structure`, `52-account-structure-global`, `53-tracking-setup`, `53-tracking-setup-global`, `54-media-plan`, `54-media-plan-global`, `55-scaling-ads`, `55-scaling-ads-global`, `56-retargeting-plan`, `56-retargeting-plan-global`, `57-next-ads-plan`, `57-next-ads-plan-global`, `68-cro-audit-trang`.
5. **Thương hiệu Cá nhân & AI Avatar**: `22-personal-brand-context`, `22-personal-brand-context-global`, `23-personal-brand-strategy`, `23-personal-brand-strategy-global`, `24-ai-avatar-production`, `24-ai-avatar-production-global`, `25-voice-clone-podcast`, `25-voice-clone-podcast-global`, `26-thought-leadership-content`, `26-thought-leadership-content-global`, `27-personal-brand-monetize`, `27-personal-brand-monetize-global`, `28-community-building`, `28-community-building-global`.
6. **Thương mại điện tử & Vận hành**: `29-dropshipping-mastery-global`, `29-xuat-khau-b2b`, `75-hop-tac-koc-affiliate`, `76-van-hanh-san-tmdt`, `77-kich-ban-sale-chatbot`, `71-sales-enablement`, `70-lead-magnet`, `69-giu-chan-khach-hang`.

Mỗi skill được đóng gói độc lập kèm theo đầy đủ hợp đồng trách nhiệm, tài liệu tham chiếu (`references/`), biến thể vùng miền (`variants/`), bộ đánh giá (`evals/`) và biểu mẫu (`templates/`) để có thể cài đặt và sử dụng riêng lẻ.

Skill được phát hành theo giấy phép **MIT License**, bản quyền thuộc về **Over Powers Agency**.

### Hướng dẫn sử dụng không cần clone repo (Copy Agent Prompt)

Mở trang [AI Business Skills trên VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&sources=aibusiness), chọn agent (Antigravity, Cursor, Claude Code, Codex...), bấm **Copy Agent Prompt** và dán vào cửa sổ chat của dự án.

Agent sẽ đọc manifest từ `install-manifests/<skill-id>.json`, xác thực SHA-256 từng tệp, tải trọn gói và lưu vào thư mục dự án cùng receipt `.vas-manifest.json` tương thích với CLI.

### Hướng dẫn sử dụng qua CLI (`./vas`)

Từ thư mục checkout VAS:

```bash
# Tìm kiếm các skill tiếp thị và kinh doanh AI
./vas search mkt
./vas search aibiz

# Xem chi tiết runbook của một skill
./vas show 00-ke-hoach-mkt

# Cài đặt một skill vào dự án (chế độ copy độc lập)
./vas install 00-ke-hoach-mkt --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Cài đặt bộ kỹ năng vào dự án Antigravity
./vas install 00-ke-hoach-mkt 04-script-video 05-copy-quang-cao 21-audit-ads-performance --target antigravity --mode link

# Kiểm tra trạng thái cài đặt
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Gỡ bỏ skill khi hoàn thành
./vas uninstall 00-ke-hoach-mkt --target claude --dest "/path/to/project/.claude/skills"
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
  - Tương thích với tất cả các agent AI hỗ trợ Open Agent Skills specification (`agentskills.io`).
  - Môi trường chạy chuẩn: Node.js hoặc Python 3 cho các công cụ tự động hóa tùy chọn.
- **Quyền riêng tư & An toàn**: Quá trình cài đặt `./vas install` chỉ sao chép hoặc tạo liên kết tệp tin tĩnh và ghi receipt `.vas-manifest.json`. Không tự động chạy mã, không cài đặt runtime/MCP hay mở kết nối mạng trong lúc cài đặt.

---

## English

Added **147 new skills / 744 files**, zero duplicates skipped.
1 skill with colliding catalog name uses the `aibiz-` namespace prefix (`aibiz-product-marketing-context`).
Catalog total: **3,576 skills / 119 categories**.

This is the comprehensive AI Marketing & Business workflow suite for **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline**, and **GitHub Copilot CLI**, authored by **Nguyễn Văn Minh ([@minhnv0807](https://github.com/minhnv0807))** and **Over Powers Agency**:
transforms general AI coding assistants into an end-to-end Marketing & Business operations squad for solopreneurs, founders, agencies, and SMBs.

Features two specialized clusters (Vietnam Edition and Global Edition) covering the complete business lifecycle:
1. **Strategy & Planning**: `00-ke-hoach-mkt`, `00-marketing-plan-global`, `02-brief-chien-dich`, `02-campaign-brief-global`, `10-tinh-kpi-nguoc`, `10-reverse-kpi-global`, `58-positioning`, `58-positioning-global`, `59-go-to-market`, `59-go-to-market-global`, `61-budget-planning`, `61-budget-planning-global`, `aibiz-product-marketing-context`, `product-marketing-context-global`.
2. **Content Production & Copywriting**: `01-lich-noi-dung`, `01-content-calendar-global`, `04-script-video`, `04-script-video-global`, `05-copy-quang-cao`, `05-ad-copy-global`, `35-brand-voice`, `35-brand-voice-global`, `36-content-brief`, `36-content-brief-global`, `37-caption-social`, `37-social-caption-global`, `74-copy-hai-lop`.
3. **Design & Visual Direction**: `30-thiet-ke-master`, `30-design-master-global`, `41-campaign-asset-list`, `42-brief-hinh-anh`, `43-brief-carousel`, `44-brief-video-editor`, `45-brief-canva`, `46-brand-guideline`, `47-design-review`, `48-quick-visual-brief`, `49-html-email-template`, `50-asset-resize`.
4. **Performance Marketing & CRO**: `21-audit-ads-performance`, `21-ads-audit-global`, `52-account-structure`, `52-account-structure-global`, `53-tracking-setup`, `53-tracking-setup-global`, `54-media-plan`, `54-media-plan-global`, `55-scaling-ads`, `55-scaling-ads-global`, `56-retargeting-plan`, `56-retargeting-plan-global`, `57-next-ads-plan`, `57-next-ads-plan-global`, `68-cro-audit-trang`.
5. **Personal Branding & AI Avatars**: `22-personal-brand-context`, `22-personal-brand-context-global`, `23-personal-brand-strategy`, `23-personal-brand-strategy-global`, `24-ai-avatar-production`, `24-ai-avatar-production-global`, `25-voice-clone-podcast`, `25-voice-clone-podcast-global`, `26-thought-leadership-content`, `26-thought-leadership-content-global`, `27-personal-brand-monetize`, `27-personal-brand-monetize-global`, `28-community-building`, `28-community-building-global`.
6. **E-Commerce & Operations**: `29-dropshipping-mastery-global`, `29-xuat-khau-b2b`, `75-hop-tac-koc-affiliate`, `76-van-hanh-san-tmdt`, `77-kich-ban-sale-chatbot`, `71-sales-enablement`, `70-lead-magnet`, `69-giu-chan-khach-hang`.

Every skill is self-contained with its own contracts, references (`references/`), regional variants (`variants/`), evaluations (`evals/`), and templates (`templates/`).

The suite is released under the **MIT License**, Copyright (c) 2025 Over Powers Agency.

### No-Clone Web Quickstart (Copy Agent Prompt)

Open [AI Business Skills on VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=en&sources=aibusiness), pick your coding agent (Antigravity, Cursor, Claude Code, Codex, etc.), click **Copy Agent Prompt**, and paste it into your project chat window.

### CLI Instructions (`./vas`)

From your local VAS repository checkout:

```bash
# Search marketing and AI business skills
./vas search mkt
./vas search aibiz

# Inspect skill runbook
./vas show 00-marketing-plan-global

# Install skill to project (copy mode)
./vas install 00-marketing-plan-global --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Install multiple skills to Antigravity (link mode)
./vas install 00-marketing-plan-global 04-script-video-global 05-ad-copy-global --target antigravity --mode link

# Check status
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Uninstall
./vas uninstall 00-marketing-plan-global --target claude --dest "/path/to/project/.claude/skills"
```

### Default Project Folders by Agent

| Agent | Project Destination |
|---|---|
| Google Antigravity | `.agents/skills/<skill-id>/` |
| OpenAI Codex | `.codex/skills/<skill-id>/` |
| Claude Code | `.claude/skills/<skill-id>/` |
| Cursor | `.cursor/skills/<skill-id>/` |
| Windsurf | `.windsurf/skills/<skill-id>/` |
| Cline / Roo Code | `.cline/skills/<skill-id>/` |
| GitHub Copilot CLI | `.github/skills/<skill-id>/` |
