# Store Screenshots trong VAS / Store Screenshots in VAS

## Tiếng Việt

Đã thêm **1 skill mới / 1.699 tệp**, không có bản trùng phải bỏ qua.
Upstream: [`thearkxd/store-screenshots-skill`](https://github.com/thearkxd/store-screenshots-skill) tại revision `c25bf66faa7396818c0f7b267e6add4d441573a8` (phiên bản `v2.2.41`).
Catalog: **3.876 skill / 119 danh mục**.

Kỹ năng lên kế hoạch, viết nội dung và thiết kế ảnh chụp màn hình chợ ứng dụng (App Store & Google Play Screenshots) chuyên nghiệp dành cho **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline** và **GitHub Copilot CLI** do **thearkxd (Alpiworks)** phát triển:
biến ảnh chụp màn hình thực tế của ứng dụng thành chiến dịch quảng cáo chuyển đổi cao trong 2 giây lướt xem đầu tiên của người dùng, trích xuất mã gen thị giác (Visual DNA), bố cục tự do đa lớp (layers scene) với góc phối cảnh 3D thiết bị, kiểm tra xác minh tuyên bố tính năng và xuất ảnh pixel-exact PNG kèm SVG có thể chỉnh sửa cho mọi kích thước store.

Mã nguồn và tài liệu kỹ năng phát hành theo giấy phép **MIT License**, bản quyền thuộc về **Alpiworks**. Kho ảnh tham chiếu App Store bên thứ ba trong `assets/library/img/` được lưu chi tiết trong `NOTICE.md` phục vụ nghiên cứu và học thuật.

### Chi tiết kỹ năng `store-screenshots`

- **Tên kỹ năng**: `store-screenshots`
- **Mục tiêu**: Lên kế hoạch, viết headline/copy, trích xuất visual DNA, kết xuất bố cục đa lớp (multi-layer scene), và kiểm tra độ tuân thủ tiêu chuẩn cửa hàng cho ảnh App Store và Google Play.
- **7 Nguyên tắc bất khả xâm phạm**:
  1. **Giao diện thật, không chỉnh sửa cẩu thả**: Sử dụng ảnh raw từ ứng dụng, cắt ghép trung thực, không bao giờ tự vẽ lại thành phần UI hay bịa đặt số liệu đánh giá.
  2. **Một ý tưởng cho mỗi bức ảnh**: Một thông điệp duy nhất, tối đa một dòng phụ ngắn gọn.
  3. **Vượt qua bài kiểm tra hoán đổi (Swap test)**: Đổi tên app thành tên đối thủ; nếu headline vẫn đúng, viết lại cho đến khi chỉ duy nhất ứng dụng này sở hữu lời hứa đó.
  4. **Bức ảnh đầu tiên luôn là Lời hứa (The Promise)**: Không dùng logo, màn hình chờ splash hay "chúng tôi vừa cập nhật".
  5. **Chỉ dùng ảnh raw từ máy thật/simulator**: Không cắt UI từ ảnh marketing đã qua chỉnh sửa của đối thủ.
  6. **Thiết kế riêng cho ứng dụng này**: Phong cách bắt nguồn từ chính DNA của ứng dụng, không dùng template rập khuôn.
  7. **Kiểm tra ở cả kích thước thật và kích thước thumbnail kết quả tìm kiếm** trước khi xuất bản.
- **Tài liệu tham khảo chuyên sâu đi kèm**:
  - `references/storytelling.md`: Nghệ thuật kể chuyện và xây dựng câu chuyện sản phẩm qua từng shot.
  - `references/copy-rules.md`: Quy tắc viết headline, sub-headline, cấu trúc câu tiếng Anh và đa ngôn ngữ.
  - `references/design-process.md`: Quy trình thiết kế 4 giai đoạn từ intake, storyboard đến DNA board và final render.
  - `references/scene-format.md`: Định dạng đặc tả scene dạng JSON cho từng layer (device3d, text, crop, lift, brand).
  - `references/layouts.md`: Các kiểu bố cục bố trí thiết bị (portrait, landscape, tilted, layered, duo).
  - `references/store-specs.md`: Thông số kích thước ảnh, tỉ lệ, định dạng và giới hạn của Apple App Store & Google Play.
  - `references/categories.md`: Playbook thiết kế theo từng ngành (Fitness, Finance, Productivity, Travel, Social...).
  - `references/critique.md`: Bảng chấm điểm và phương pháp đánh giá bộ ảnh chụp hiện có.
  - `references/localization.md`: Chiến lược địa phương hóa ảnh chụp màn hình cho từng thị trường.
- **Bộ công cụ & Thư viện đi kèm**:
  - `scripts/`: 19 công cụ Python hỗ trợ đo đạc visual DNA (`dna.py`), bố cục scene tự do (`compose.py`), dựng thiết bị 3D (`device3d.py`), kiểm tra lỗi hiển thị (`check_set.py`), phân tích danh sách App Store live (`fetch_listing.py`), tìm kiếm thư viện mẫu (`search_library.py`).
  - `assets/library/`: Thư viện phân tích hơn 1.700 ảnh chụp màn hình top bảng xếp hạng kèm OCR headline và đánh giá chất lượng (`catalog.json`, `classifications.json`, `stats.json`).
  - `assets/fonts/`: Bộ phông chữ typography chuyên nghiệp tương thích giấy phép OFL.

### Hướng dẫn sử dụng không cần clone repo (Copy Agent Prompt)

Mở trang [Store Screenshots trên VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&sources=storescreenshots), chọn agent (Antigravity, Cursor, Claude Code, Codex...), bấm **Copy Agent Prompt** và dán vào cửa sổ chat của dự án.

Agent sẽ đọc manifest `install-manifests/store-screenshots.json`, xác thực SHA-256 từng tệp (bao gồm `SKILL.md`, `LICENSE`, `NOTICE.md`, `references/`, `scripts/`, `templates/` và `assets/`), tải trọn gói và lưu vào thư mục dự án cùng receipt `.vas-manifest.json` tương thích với CLI.

### Hướng dẫn sử dụng qua CLI (`./vas`)

Từ thư mục checkout VAS:

```bash
# Tìm kiếm kỹ năng
./vas search store-screenshots

# Xem chi tiết runbook
./vas show store-screenshots

# Cài đặt chế độ copy độc lập vào dự án
./vas install store-screenshots --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Cài đặt chế độ link symlink
./vas install store-screenshots --target antigravity --mode link

# Kiểm tra trạng thái cài đặt
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Gỡ bỏ an toàn
./vas uninstall store-screenshots --target claude --dest "/path/to/project/.claude/skills"
```

---

## English

Added **1 new skill / 1,699 files**, 0 duplicates skipped.
Upstream: [`thearkxd/store-screenshots-skill`](https://github.com/thearkxd/store-screenshots-skill) at revision `c25bf66faa7396818c0f7b267e6add4d441573a8` (release `v2.2.41`).
Catalog: **3,876 skills / 119 categories**.

Production-grade App Store and Google Play screenshot planning, copywriting, and multi-layer scene design skill for **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline**, and **GitHub Copilot CLI** created by **thearkxd (Alpiworks)**:
turns raw app screens into an ad that works in a 2-second scroll, extracts the app's visual DNA (palette, typography, signature elements), composes free multi-layer scenes with 3D device perspectives, verifies claims against real UI, and exports pixel-exact PNGs and editable SVGs for all store sizes.

Released under the **MIT License**, Copyright (c) 2026 Alpiworks. Third-party App Store reference screenshots in `assets/library/img/` are documented under `NOTICE.md` for study and reference.

### Skill Details: `store-screenshots`

- **Skill ID**: `store-screenshots`
- **Core Mission**: Plans, writes copy, measures visual DNA, composes free multi-layer scenes (text, crops, lifts, 3D devices, glass/glow shapes, callouts), and performs store-spec and legibility checks.
- **The 7 Non-Negotiables**:
  1. **Real UI only, unaltered**: Never stretch, recolor, filter, redraw, or fake UI numbers or reviews.
  2. **One idea per screenshot**: One headline, optionally one short sub-line.
  3. **The promise passes the swap test**: If a competitor's name can replace yours, rewrite until unique.
  4. **First shot = The Promise**: Never waste shot 1 on a splash screen or login page.
  5. **Raw screens only**: No cutting UI out of competitor marketing screenshots.
  6. **Designed for this app, nothing by default**: Concepts derive strictly from the app's visual DNA.
  7. **Look at your work at real and search-result sizes** before publishing.
- **Reference Playbooks**:
  - `references/storytelling.md`: Visual storytelling across screenshot sequences.
  - `references/copy-rules.md`: Headline length limits, word choice, and localization rules.
  - `references/design-process.md`: Four-phase design loop from intake to final export.
  - `references/scene-format.md`: Layer-based JSON scene specifications.
  - `references/layouts.md`: Portrait, landscape, tilted, and duo device framing layouts.
  - `references/store-specs.md`: Apple App Store and Google Play dimension, ratio, and policy specs.
  - `references/categories.md`: Category playbooks across major mobile verticals.
  - `references/critique.md`: Structured audit rubric for existing store listings.
  - `references/localization.md`: Multi-locale translation and layout adaptation guidelines.
- **Bundled Tooling & Reference Assets**:
  - `scripts/`: 19 Python utilities for visual DNA (`dna.py`), scene composition (`compose.py`), 3D device projection (`device3d.py`), store spec checks (`check_set.py`), live store listing scraping (`fetch_listing.py`), and library search (`search_library.py`).
  - `assets/library/`: Classified reference dataset of 1,700+ top-chart screenshots with OCR headlines and critique verdicts (`catalog.json`, `classifications.json`, `stats.json`).
  - `assets/fonts/`: Open Font License (OFL) typefaces curated for app screenshot typography.

### Usage Without Cloning (Copy Agent Prompt)

Visit [Store Screenshots on VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=en&sources=storescreenshots), select your coding agent, click **Copy Agent Prompt**, and paste it directly into your AI chat window.

Your agent validates `install-manifests/store-screenshots.json`, verifies every SHA-256 hash, downloads files directly from the pinned commit, and saves `.vas-manifest.json` for CLI compatibility.

### CLI Usage (`./vas`)

From your local VAS clone:

```bash
# Search for store-screenshots
./vas search store-screenshots

# View runbook
./vas show store-screenshots

# Copy install into project
./vas install store-screenshots --target cursor --mode copy --dest "/path/to/project/.cursor/skills"

# Symlink install into global Antigravity
./vas install store-screenshots --target antigravity --mode link

# Check installation status
./vas status --target cursor --dest "/path/to/project/.cursor/skills"

# Clean uninstall
./vas uninstall store-screenshots --target cursor --dest "/path/to/project/.cursor/skills"
```
