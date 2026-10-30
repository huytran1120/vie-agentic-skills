# TypeSafe trong VAS / TypeSafe in VAS

## Tiếng Việt

`typesafe-ai` là **một skill** của TypeSafe AI về tích hợp Jev/System One:
thiết kế state, câu hỏi có kiểu, xác suất, ngưỡng và logic quyết định trong code.
Bản nhập gồm đủ hai tệp upstream, `SKILL.md` và `LICENSE`, theo MIT; chỉ thêm
ghi chú VAS có thể đối chiếu ngược. Không có scripts hay phụ thuộc nội bộ cần tải.

**Không cần clone:** mở [TypeSafe trên catalog](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&skill=typesafe-ai),
chọn agent, bấm **Copy Agent Prompt** và dán vào chat trong dự án đang mở.
Agent đọc [manifest chính thức](https://huytran1120.github.io/vie-agentic-skills/install-manifests/typesafe-ai.json),
kiểm tra đúng skill và `available = true`, tải đủ tệp, xác minh kích thước/SHA-256,
giữ quyền executable và ghi receipt `.vas-manifest.json` tương thích CLI.
Nếu nội dung đã đúng thì bỏ qua; khác nội dung thì phải hỏi trước, không ghi đè.

**CLI:** chạy từ kho VAS đã clone, thay `/Projects/my-app` bằng đường dẫn dự án thật:

```bash
./vas search typesafe
./vas show typesafe-ai
./vas install typesafe-ai --target cursor --mode link --dest "/Projects/my-app/.cursor/skills"
./vas status --target cursor --dest "/Projects/my-app/.cursor/skills"
./vas uninstall typesafe-ai --target cursor --dest "/Projects/my-app/.cursor/skills"
```

`--mode link` dùng symlink và cần giữ nguyên vị trí kho VAS; `--mode copy` tạo
bản sao độc lập. Không có `--dest` thì đích nằm trong thư mục đang chạy lệnh.
`--global` chỉ dành cho một agent; `--target all` dùng bảy đích trong dự án.

| Agent | Thư mục trong dự án |
|---|---|
| Antigravity | `.agents/skills/typesafe-ai/` |
| Codex | `.codex/skills/typesafe-ai/` |
| Claude Code | `.claude/skills/typesafe-ai/` |
| Cursor | `.cursor/skills/typesafe-ai/` |
| Windsurf | `.windsurf/skills/typesafe-ai/` |
| Cline / Roo Code | `.cline/skills/typesafe-ai/` |
| GitHub Copilot CLI | `.github/skills/typesafe-ai/` |

VAS CLI chỉ cần Python 3; đọc runbook không cần SDK hay API key. Khi thực sự tích
hợp Jev, người dùng cần quyền truy cập dịch vụ TypeSafe và `TYPESAFE_API_KEY`
được giữ ở server. SDK là tùy chọn; tra tài liệu live/kiểu của SDK đã cài để
chọn schema và phiên bản đúng. Các liên kết tài liệu bên ngoài không phải snapshot
được đóng gói và cần mạng khi tra cứu.

**Trước khi probe API:** phải xin phép, thống nhất ngân sách và nói rõ dữ liệu sẽ
gửi. Không tự đọc key, gửi dữ liệu riêng tư, cài SDK/plugin/MCP, kết nối dịch vụ
hay phát sinh chi phí khi nhập/cài skill. Giấy phép MIT của runbook không thay thế
điều khoản dịch vụ TypeSafe. Lỗi API phải báo lỗi, không giả thành câu trả lời.

## English

`typesafe-ai` is **one skill** by TypeSafe AI for Jev/System One integrations:
state and question design, typed probabilities, thresholds and decisions in code.
VAS includes both upstream files, `SKILL.md` and `LICENSE`, under MIT. Only
reversible VAS installation notes are appended; no scripts or internal support
dependencies are missing.

**No-clone installation:** open [TypeSafe in the catalog](https://huytran1120.github.io/vie-agentic-skills/?lang=en&skill=typesafe-ai),
choose an agent, copy **Copy Agent Prompt** and paste it into chat in your project.
The [official manifest](https://huytran1120.github.io/vie-agentic-skills/install-manifests/typesafe-ai.json)
lists every file, byte size, SHA-256, executable flag and compatible CLI receipt.
The agent checks identity and `available = true`, skips matching installations
and asks before replacing conflicting contents.

**CLI:** from a VAS checkout, replace `/Projects/my-app` with your actual project:

```bash
./vas search typesafe
./vas show typesafe-ai
./vas install typesafe-ai --target cursor --mode copy --dest "/Projects/my-app/.cursor/skills"
./vas status --target cursor --dest "/Projects/my-app/.cursor/skills"
./vas uninstall typesafe-ai --target cursor --dest "/Projects/my-app/.cursor/skills"
```

`--mode copy` is independent; `--mode link` needs the VAS checkout to stay in
place. Without `--dest`, the current directory is the project. Use the exact
agent-folder mapping above. `--global` applies to one agent, not `--target all`;
quick-install `all` means the seven current-project destinations.

VAS needs only Python 3. Reading the runbook requires neither an SDK nor a key.
Actually calling Jev requires separately provisioned TypeSafe service access and
the user's own `TYPESAFE_API_KEY`, kept server-side. An SDK is optional; use the
live docs or installed types, not guessed versions/schemas. External documentation
is a live reference and is not included in the immutable skill snapshot.

Before any live probe, obtain permission, agree a budget and disclose the data
being sent. Installing the skill never reads keys, sends private data, installs
an SDK/plugin/MCP server, connects to TypeSafe or makes paid requests. MIT covers
the runbook, not service access or separate service/data-handling terms. Surface
API failures explicitly rather than treating them as model answers.

## Provenance

- Source: [typesafe-ai/skills](https://github.com/typesafe-ai/skills/tree/302eea662c54bca6730873fe245bec1d69ebc23d)
- Upstream SHA: `302eea662c54bca6730873fe245bec1d69ebc23d`
- Canonical ID and installed folder: `typesafe-ai`
- Original notice: Copyright (c) 2026 TypeSafe AI, MIT
- Inventory: [`data/typesafe-import.json`](https://github.com/huytran1120/vie-agentic-skills/blob/main/data/typesafe-import.json)
- License: [`skills/typesafe-ai/LICENSE`](https://github.com/huytran1120/vie-agentic-skills/blob/main/skills/typesafe-ai/LICENSE)
- Installation manifests pin the **VAS publication commit**, not the upstream SHA.
