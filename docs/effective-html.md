# Effective HTML trong VAS / Effective HTML in VAS

## Tiếng Việt

Đã thêm **8 skill mới / 37 tệp**, không có bản trùng phải bỏ qua.
Upstream: [`plannotator/effective-html`](https://github.com/plannotator/effective-html) tại revision `5ce160a3e76dc1c0f9301f8a1903704ec607636a`.
Catalog: **3.884 skill / 119 danh mục**.

Bộ kỹ năng trực quan hóa và thiết kế tài liệu HTML độc lập (self-contained HTML artifacts) dành cho **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline** và **GitHub Copilot CLI** do **Plannotator ([plannotator.ai](https://docs.plannotator.ai/))** phát triển:
biến mọi quyết định sản phẩm, ý tưởng, kế hoạch và kiến trúc hệ thống thành các file HTML đơn lẻ, hoàn chỉnh, tương tác trực tiếp trong trình duyệt thay vì những văn bản chữ nhàm chán.

Toàn bộ 8 kỹ năng được phát hành theo giấy phép **MIT License**, bản quyền thuộc về **Plannotator**.

### Danh sách 8 kỹ năng Effective HTML

1. **`html`**:
   - **Kỹ năng điều hướng (Router) và tạo tài liệu HTML tổng quát**: Xây dựng các trang báo cáo, bản thuyết trình, công cụ mini hoặc landing page độc lập theo yêu cầu dự án.
   - Tự động nhận diện và chuyển hướng các yêu cầu chuyên sâu về wireframe, prototype, diagram hoặc roadmap đến các kỹ năng chuyên biệt tương ứng.
   - Đi kèm 5 tài liệu tham khảo cốt lõi trong thư mục `references/`:
     - `creative-direction.md`: Định hướng phong cách thiết kế, typography và phối màu.
     - `charts-and-data.md`: Kỹ thuật dựng biểu đồ và bảng số liệu tương tác.
     - `diagrams.md`: Mô hình trực quan hóa quan hệ và luồng dữ liệu.
     - `documents-and-presentations.md`: Bố cục văn bản, memo và slide deck.
     - `interfaces.md`: Thiết kế giao diện công cụ và ứng dụng mini.

2. **`big-pics-little-words`**:
   - **Giải thích trực quan bằng hình ảnh lớn và cô đọng chữ**: Trình bày các chủ đề phức tạp bằng đồ họa, sơ đồ và hình ảnh trực quan rõ nét, tối thiểu hóa văn bản nhưng vẫn giữ trọn vẹn thông điệp quan trọng.

3. **`one-pager`**:
   - **Tài liệu tóm tắt ý tưởng 1 trang duy nhất**: Tạo trang HTML một trang duy nhất để chia sẻ ý tưởng ban đầu với đồng đội hoặc tổng kết kết quả công việc một cách nhanh gọn, súc tích và dễ hiểu.

4. **`design-artifact`**:
   - **Định hướng sáng tạo và phong cách thiết kế chuyên nghiệp**: Cung cấp nguyên lý thiết kế, lựa chọn bảng màu, ghép cặp phông chữ (type pairing), căn chỉnh khoảng cách và chọn đúng tông điệu (register) cho tài liệu HTML mà không bị rập khuôn hay mang vẻ "AI-generated".

5. **`html-wireframe`**:
   - **Dựng khung giao diện độ trung thực thấp (Low-Fidelity)**: Kiểm thử cấu trúc nội dung, phân cấp thông tin (information hierarchy), luồng tác vụ và bố cục responsive trước khi đi vào thiết kế chi tiết.

6. **`html-prototype`**:
   - **Nguyên mẫu tương tác chân thực và mockup sắc nét**: Xây dựng luồng trải nghiệm hoạt động được với đầy đủ các trạng thái (loading, empty, error, recovery), hỗ trợ bàn phím và giao diện responsive bám sát ngữ cảnh sản phẩm.

7. **`html-plan`**:
   - **Kế hoạch hành động, lộ trình và chuỗi triển khai**: Chuyển hóa kế hoạch kỹ thuật, roadmap hoặc kịch bản rollout thành tài liệu HTML rõ ràng, minh bạch quyền sở hữu và phụ thuộc, dễ dàng kiểm tra đối soát.

8. **`html-diagram`**:
   - **Sơ đồ cấu trúc, topo và chuỗi tin nhắn**: Lựa chọn mô hình biểu diễn phù hợp nhất (topology, sequence diagram, state machine, phân cấp định lượng) để làm sáng tỏ các mối liên kết và tương tác hệ thống.

### Hướng dẫn sử dụng không cần clone repo (Copy Agent Prompt)

Mở trang [Effective HTML trên VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&sources=effectivehtml), chọn agent (Antigravity, Cursor, Claude Code, Codex...), bấm **Copy Agent Prompt** và dán vào cửa sổ chat của dự án.

Agent sẽ đọc manifest `install-manifests/<canonical-id>.json`, xác thực SHA-256 từng tệp (bao gồm `SKILL.md`, `LICENSE`, `NOTICE.md`, các references và agent configs), tải trọn gói và lưu vào thư mục dự án cùng receipt `.vas-manifest.json` tương thích với CLI.

### Hướng dẫn sử dụng qua CLI (`./vas`)

Từ thư mục checkout VAS:

```bash
# Tìm kiếm kỹ năng
./vas search effective-html
./vas search html

# Xem chi tiết runbook của từng kỹ năng
./vas show html
./vas show design-artifact
./vas show html-wireframe
./vas show html-prototype
./vas show html-plan
./vas show html-diagram
./vas show one-pager
./vas show big-pics-little-words

# Cài đặt chế độ copy độc lập vào dự án
./vas install html --target claude --mode copy --dest "/path/to/project/.claude/skills"
./vas install design-artifact --target cursor --mode copy --dest "/path/to/project/.cursor/skills"

# Cài đặt chế độ link symlink
./vas install html-prototype --target antigravity --mode link

# Kiểm tra trạng thái cài đặt
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Gỡ bỏ kỹ năng an toàn
./vas uninstall html --target claude --dest "/path/to/project/.claude/skills"
```

---

## English

Added **8 new skills / 37 files**, 0 duplicates skipped.
Upstream: [`plannotator/effective-html`](https://github.com/plannotator/effective-html) at revision `5ce160a3e76dc1c0f9301f8a1903704ec607636a`.
Catalog: **3,884 skills / 119 categories**.

Focused agent skills for creating pragmatic, self-contained HTML artifacts for **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline**, and **GitHub Copilot CLI** by **Plannotator ([plannotator.ai](https://docs.plannotator.ai/))**:
turn product decisions, architectural sequences, rollouts, wireframes, and prototypes into standalone, interactive HTML deliverables verified directly in browser viewports.

All 8 skills are published under the **MIT License**, Copyright (c) 2026 Plannotator.

### The 8 Effective HTML Skills

1. **`html`**:
   - **Collection router and general HTML deliverable creator**: Build standalone single-file HTML reports, landing pages, explainers, and tools.
   - Routes explicit wireframe, prototype, plan, or diagram requests to the corresponding specialist skill.
   - Ships with 5 core references in `references/`:
     - `creative-direction.md`: Principles for register, typography pairing, and palette selection.
     - `charts-and-data.md`: Interactive data visualizers, sparklines, and metric tables.
     - `diagrams.md`: Visual relationship representations and system flows.
     - `documents-and-presentations.md`: Structured layouts, memos, and slide decks.
     - `interfaces.md`: Interactive widgets, dashboards, and mini tools.

2. **`big-pics-little-words`**:
   - **Visual explanations with rich graphics and concise prose**: Explain complex subjects in HTML with large visuals and minimal text while keeping essential details intact.

3. **`one-pager`**:
   - **Executive one-page visual briefs**: Create a single HTML page to pitch an early idea to teammates or summarize a milestone clearly in minutes.

4. **`design-artifact`**:
   - **Creative direction and craftsmanship**: Choose palettes, typography pairings, layout hierarchies, and appropriate tonal registers for any HTML deliverable without falling into generic AI aesthetics.

5. **`html-wireframe`**:
   - **Low-fidelity information hierarchy validation**: Test content models, navigation flows, and responsive layouts before committing to visual polish.

6. **`html-prototype`**:
   - **Interactive prototypes and polished mockups**: Build working product models featuring realistic state machines (loading, empty, error, recovery), keyboard accessibility, and responsive viewports.

7. **`html-plan`**:
   - **Actionable plans, roadmaps, and rollouts**: Transform technical sequences and implementation commitments into structured HTML documents that remain easily verifiable.

8. **`html-diagram`**:
   - **System topologies, sequences, and state diagrams**: Choose the right visual model (component topology, message sequence, timeline, quantitative hierarchy) to clarify complex relations.

### No-Clone Agent Prompt Installation

Open [Effective HTML on VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=en&sources=effectivehtml), pick your agent, click **Copy Agent Prompt**, and paste it into your project chat.

The agent fetches `install-manifests/<canonical-id>.json`, verifies the SHA-256 digest of every file (`SKILL.md`, `LICENSE`, `NOTICE.md`, references, and agent configs), downloads the snapshot pinned to VAS, and saves the `.vas-manifest.json` receipt.

### CLI Instructions (`./vas`)

From the root checkout:

```bash
# Search skills
./vas search effective-html
./vas search html

# Show detailed runbooks
./vas show html
./vas show design-artifact
./vas show html-wireframe
./vas show html-prototype
./vas show html-plan
./vas show html-diagram
./vas show one-pager
./vas show big-pics-little-words

# Install in copy mode into a project
./vas install html --target claude --mode copy --dest "/path/to/project/.claude/skills"
./vas install design-artifact --target cursor --mode copy --dest "/path/to/project/.cursor/skills"

# Install in symlink mode
./vas install html-prototype --target antigravity --mode link

# Check installation status
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Uninstall cleanly
./vas uninstall html --target claude --dest "/path/to/project/.claude/skills"
```
