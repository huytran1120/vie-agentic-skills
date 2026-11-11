# NVIDIA SkillEvaluator trong VAS / NVIDIA SkillEvaluator in VAS

## Tiếng Việt

Đã thêm **1 skill mới / 16 tệp**, không có bản trùng phải bỏ qua.  
Upstream: [`NVIDIA/SkillEvaluator`](https://github.com/NVIDIA/SkillEvaluator) tại revision `7ae25d2522c9c3b151111fedaa67b814cc3dc5c5`.  
Catalog: **4.079 skill / 119 danh mục**.

Kỹ năng vận hành, kiểm thử và đánh giá toàn diện chất lượng AI Agent Skill chuẩn công nghiệp dành cho **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline**, **OpenCode/Roo Code** và **GitHub Copilot CLI** do **NVIDIA Corporation & Affiliates** phát triển:
cung cấp cho AI coding agent quy trình đánh giá chuẩn xác, đáng tin cậy dựa trên bộ công cụ mã nguồn mở **SkillEvaluator** (thuộc quy trình kiểm định *NVIDIA Verified Skills* và bài báo khoa học *arXiv:2608.20614*).

Kỹ năng hỗ trợ trọn vẹn cả 3 tầng kiểm thử (*3-Tier Evaluation Framework*):
1. **Tier 1 (Kiểm tra tĩnh, bảo mật và chất lượng tĩnh)**:
   - Chạy không cần API key: `quality-check` chấm điểm tài liệu và cấu trúc theo thang 100 điểm, `security-scan` phát hiện shell injection / command chaining / đường dẫn nguy hiểm, `pii-scan` dò quét thông tin định danh cá nhân và khóa API lộ lọt, `lint-scripts` kiểm tra cú pháp Python/Bash.
   - Khi có LLM provider (như NVIDIA Build API hoặc OpenAI): chấm điểm rubric tự động (`rubric-eval`) và rà soát bảo mật ngữ cảnh chuyên sâu.
2. **Tier 2 (Chống trùng lặp và phát hiện giao thoa kiến thức)**:
   - Sử dụng mô hình embedding để đo lường mức độ lặp lại chỉ dẫn bên trong một kỹ năng (`tier2`) và phát hiện chồng chéo nội dung giữa các kỹ năng trong toàn bộ bộ sưu tập (`similarity-check`).
3. **Tier 3 (Kiểm thử thực nghiệm trực tiếp với Agent trong Sandbox)**:
   - Chạy agent thực tế (như OpenCode, Codex, Claude Code) trong môi trường cô lập (Docker container hoặc Seatbelt/Bubblewrap local sandbox).
   - Đo lường chỉ số **Skill Lift** (kỹ năng thực sự giúp tăng tỉ lệ thành công bao nhiêu % so với baseline không có kỹ năng) và tỉ lệ vượt qua thử nghiệm `pass@k`.
   - Hỗ trợ cơ chế mang bộ đánh giá riêng (BYOG - Bring Your Own Grader / BYOT - Harbor tasks).

Mã nguồn và tài liệu phát hành theo giấy phép **Apache License 2.0**, bản quyền thuộc về **NVIDIA Corporation & Affiliates** (2026).

---

### Chi tiết kỹ năng `skillevaluator`

- **Tên kỹ năng (Canonical ID)**: `skillevaluator`
- **Mục tiêu**: Hướng dẫn AI agent cách tự kiểm định, chấm điểm, viết bộ kiểm thử `evals/evals.json`, thiết lập CI gating cho GitHub Actions / GitLab CI và đo lường hiệu quả thực tế của các agent skill.
- **Tập hợp tài liệu tham khảo đi kèm (`references/`)**:
  - `commands-tier1.md`: Bảng lệnh và cờ chi tiết cho Tier 1 (chất lượng tĩnh, quét bảo mật, PII, rubric).
  - `commands-tier2-tier3.md`: Bảng lệnh đo độ trùng lặp Tier 2 và đánh giá thực nghiệm Tier 3.
  - `commands-validate.md`: Pipeline tổng hợp kiểm tra toàn bộ các tầng chỉ với một mã thoát duy nhất.
  - `custom-graders.md`: Đặc tả bộ chấm điểm tùy biến (BYOG) và nhiệm vụ Harbor (BYOT).
  - `providers.md`: Hướng dẫn cấu hình nhà cung cấp LLM (NVIDIA Build API, OpenAI, Anthropic, OpenRouter...).
  - `reports-and-ci.md`: Cấu trúc báo cáo JSON, Markdown, SARIF, mã thoát và mẫu tích hợp CI/CD.
  - `tier3-datasets.md`: Quy chuẩn thiết kế ca kiểm thử tích cực / tiêu cực trong `evals/evals.json`.
  - `tier3-running.md`: Cơ chế thực thi sandbox, quản lý tiến trình và giữ log phân tích trajectory.
  - `troubleshooting.md`: Bảng mã lỗi, nguyên nhân và biện pháp khắc phục triệt để.

---

### Hướng dẫn sử dụng không cần clone repo (Copy Agent Prompt)

Mở trang [NVIDIA SkillEvaluator trên VAS](https://vie-agentic-skills.vercel.app/?lang=vi&sources=skillevaluator), chọn agent bạn đang sử dụng, bấm **Copy Agent Prompt** và dán vào cửa sổ chat của dự án:

```text
Read the installation manifest at https://vie-agentic-skills.vercel.app/install-manifests/skillevaluator.json and install its declared files into .agents/skills/skillevaluator/.
```

Agent sẽ đọc bản kê tệp chính thức, kiểm tra mã băm SHA-256 từng tệp (gồm `SKILL.md`, `LICENSE`, `NOTICE.md`, cấu hình mẫu `evals/` và toàn bộ 9 tài liệu tham khảo trong `references/`), tải đúng phiên bản và ghi receipt quản lý tương thích CLI.

---

### Hướng dẫn sử dụng qua CLI (`./vas`)

Từ thư mục checkout VAS:

```bash
# Tìm kiếm kỹ năng
./vas search skillevaluator

# Xem thông tin và hướng dẫn chi tiết
./vas show skillevaluator

# Cài đặt chế độ link cho Antigravity / Universal
./vas install skillevaluator --target antigravity --mode link

# Cài đặt chế độ copy độc lập vào dự án Claude Code
./vas install skillevaluator --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Kiểm tra trạng thái cài đặt
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Gỡ bỏ cài đặt sạch sẽ
./vas uninstall skillevaluator --target claude --dest "/path/to/project/.claude/skills"
```

---

## English

Added **1 new skill / 16 files**, with zero skipped duplicates.  
Upstream: [`NVIDIA/SkillEvaluator`](https://github.com/NVIDIA/SkillEvaluator) at revision `7ae25d2522c9c3b151111fedaa67b814cc3dc5c5`.  
Catalog: **4,079 skills / 119 categories**.

Industrial-grade agent skill evaluation, benchmarking, and CI gating skill for **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline**, **OpenCode/Roo Code**, and **GitHub Copilot CLI**, developed by **NVIDIA Corporation & Affiliates**:
empowers coding agents to run, interpret, and gate agent skills using the open-source **SkillEvaluator** framework (part of the *NVIDIA Verified Skills* initiative and described in *arXiv:2608.20614*).

Supports the full 3-tier evaluation framework:
1. **Tier 1 (Static Quality, Security & Rubric)**:
   - Keyless checks: deterministic `quality-check` (0-100 score), `security-scan` for command injection / dangerous patterns, `pii-scan` for accidental credentials, and `lint-scripts`.
   - Model-backed checks: automated LLM `rubric-eval` and deep security review via providers like NVIDIA Build API.
2. **Tier 2 (Deduplication & Similarity)**:
   - Embedding-based detection of repeated guidance within a skill (`tier2`) and overlap across skill collections (`similarity-check`).
3. **Tier 3 (Live Agent Benchmarks in Sandboxes)**:
   - Executes live agent runs in Docker containers or local sandboxes (macOS Seatbelt / Linux Bubblewrap).
   - Measures **Skill Lift** (empirical improvement over baseline) and `pass@k` success rates.
   - Supports Bring-Your-Own-Grader (BYOG) and custom Harbor benchmark tasks.

Licensed under **Apache License 2.0**, Copyright (c) 2026 NVIDIA Corporation & Affiliates.

---

### Skill Details: `skillevaluator`

- **Canonical ID**: `skillevaluator`
- **Purpose**: Guide AI agents to self-evaluate, score, write test cases in `evals/evals.json`, enforce CI quality gates in GitHub Actions / GitLab CI, and empirically verify skill lift.
- **Reference Runbooks (`references/`)**:
  - `commands-tier1.md`: Flag tables for Tier 1 quality, security, and rubric evaluations.
  - `commands-tier2-tier3.md`: Commands for Tier 2 deduplication and Tier 3 live trials.
  - `commands-validate.md`: Unified validation pipeline commands.
  - `custom-graders.md`: Bring-your-own-grader (BYOG) and Harbor task specifications.
  - `providers.md`: LLM provider and credentials configuration.
  - `reports-and-ci.md`: Report outputs (JSON, Markdown, SARIF), exit codes, and CI workflows.
  - `tier3-datasets.md`: Positive and negative test case authoring in `evals/evals.json`.
  - `tier3-running.md`: Live sandbox execution, agent selection, and trajectory retention.
  - `troubleshooting.md`: Doctor commands, common errors, and remedies.

---

### No-Clone Copy Agent Prompt

Open [NVIDIA SkillEvaluator on VAS](https://vie-agentic-skills.vercel.app/?lang=en&sources=skillevaluator), select your target agent, click **Copy Agent Prompt**, and paste into your agent chat:

```text
Read the installation manifest at https://vie-agentic-skills.vercel.app/install-manifests/skillevaluator.json and install its declared files into .agents/skills/skillevaluator/.
```

---

### CLI Usage (`./vas`)

From your local VAS repository:

```bash
# Search for the skill
./vas search skillevaluator

# Show detailed runbook and metadata
./vas show skillevaluator

# Link install into Google Antigravity / Universal workspace
./vas install skillevaluator --target antigravity --mode link

# Copy install into Claude Code workspace
./vas install skillevaluator --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Check installation status
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Cleanly uninstall
./vas uninstall skillevaluator --target claude --dest "/path/to/project/.claude/skills"
```
