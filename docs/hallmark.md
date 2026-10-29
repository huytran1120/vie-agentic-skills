# Hallmark trong VAS / Hallmark in VAS

## Tiếng Việt

Hallmark là **một skill** thiết kế frontend của Hallmark contributors / Together AI,
từ [Nutlope/hallmark](https://github.com/Nutlope/hallmark/tree/8f6969f8922caabde9de1784959eae11ddf68073).
50 theme là tài nguyên đi kèm, không phải 50 skill riêng. Bản nhập gồm đủ 182 tệp:
runbook, references, ảnh theme, scripts, fixtures, metadata agent và giấy phép MIT.
Chỉ phần ghi chú cài đặt VAS được thêm vào cuối runbook; mã helper không bị sửa.

**Cài không cần clone:** mở [Hallmark trên catalog](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&skill=hallmark),
chọn agent, bấm **Copy Agent Prompt** và dán vào chat trong dự án đang mở.
Agent dùng [manifest chính thức](https://huytran1120.github.io/vie-agentic-skills/install-manifests/hallmark.json)
để tải đủ tệp, kiểm tra kích thước/SHA-256, giữ quyền executable và ghi receipt
tương thích CLI. Nội dung trùng thì bỏ qua; khác nội dung thì phải hỏi trước.

**CLI:** chạy từ kho VAS đã clone. Thay `/Projects/my-app` bằng đường dẫn dự án
thực; ba lệnh dưới dùng cùng nơi cài cho Cursor:

```bash
./vas search hallmark
./vas show hallmark
./vas install hallmark --target cursor --mode link --dest "/Projects/my-app/.cursor/skills"
./vas status --target cursor --dest "/Projects/my-app/.cursor/skills"
./vas uninstall hallmark --target cursor --dest "/Projects/my-app/.cursor/skills"
```

`--mode link` cần giữ kho VAS ở nguyên vị trí; dùng `--mode copy` để tạo bản sao
độc lập. Không có `--dest` thì lệnh cài vào dự án tại thư mục đang chạy lệnh.
`--global` dành cho một agent; không kết hợp với `--target all`.

| Agent | Thư mục trong dự án |
|---|---|
| Antigravity | `.agents/skills/hallmark/` |
| Codex | `.codex/skills/hallmark/` |
| Claude Code | `.claude/skills/hallmark/` |
| Cursor | `.cursor/skills/hallmark/` |
| Windsurf | `.windsurf/skills/hallmark/` |
| Cline / Roo Code | `.cline/skills/hallmark/` |
| GitHub Copilot CLI | `.github/skills/hallmark/` |

VAS chỉ cần Python 3; đọc runbook không cần Node. Helper Hallmark cần Node.js 18+;
kiểm tra có render/chụp ảnh cần thêm Chrome và puppeteer-core/puppeteer tương thích.
Không tự cài những phụ thuộc đó, chạy installer/hook upstream, cấu hình MCP hay
kết nối dịch vụ. Chỉ dùng Hallmark để sửa giao diện hiện có khi người dùng yêu cầu.

Sinh ảnh Together AI là tùy chọn, cần khóa API của người dùng và đồng ý trước
khi phát sinh chi phí. Danh mục 755 ảnh chỉ lưu URL và thông tin ghi công; từng
ảnh giữ giấy phép CC0/public domain/CC BY/CC BY-SA riêng, không trở thành MIT.
Kiểm tra điều kiện và giữ ghi công khi dùng ảnh.

## English

Hallmark is **one frontend design skill**, by Hallmark contributors / Together AI,
from the pinned [Nutlope/hallmark snapshot](https://github.com/Nutlope/hallmark/tree/8f6969f8922caabde9de1784959eae11ddf68073).
Its 50 themes are supporting assets, not separate skills. VAS includes all 182
upstream skill files and the MIT notice. Only VAS-specific installation notes are
appended to the runbook; helper implementations are unchanged.

**No-clone installation:** open [Hallmark in the catalog](https://huytran1120.github.io/vie-agentic-skills/?lang=en&skill=hallmark),
choose an agent, copy **Copy Agent Prompt**, and paste it into that agent's chat
in the open project. The [official manifest](https://huytran1120.github.io/vie-agentic-skills/install-manifests/hallmark.json)
inventories the complete tree, sizes, SHA-256, executable flags and compatible
CLI receipt. Matching installations are skipped; conflicting files need approval.

**CLI:** from a VAS checkout, replace `/Projects/my-app` with your actual project:

```bash
./vas search hallmark
./vas show hallmark
./vas install hallmark --target cursor --mode copy --dest "/Projects/my-app/.cursor/skills"
./vas status --target cursor --dest "/Projects/my-app/.cursor/skills"
./vas uninstall hallmark --target cursor --dest "/Projects/my-app/.cursor/skills"
```

Use `--mode link` for symlinks, retaining the VAS checkout at its original path;
`--mode copy` is independent. Without `--dest`, the current directory is the
project. Use the agent-folder mapping in the table above. `--global` is for one
agent only; `--target all` installs into the seven current-project destinations.

VAS needs only Python 3. Reading the runbook needs no Node runtime; Hallmark's
helpers require Node.js 18+, and rendered checks/screenshots additionally need
compatible Chrome and puppeteer-core/puppeteer supplied separately. Installation
does not run downloaded code, install dependencies or hooks, configure MCP,
connect services or redesign the catalog. Existing designs require an explicit
request naming Hallmark.

Together AI image generation is optional, requires the user's own API key and
approval before paid requests. The photo library contains 755 URL/attribution
records, not downloaded photographs. Their individual CC0, public-domain,
CC BY or CC BY-SA terms remain separate from MIT; preserve credits and verify
the applicable terms before using an image.

## Provenance

- Upstream: `Nutlope/hallmark`
- Commit: `8f6969f8922caabde9de1784959eae11ddf68073`
- Canonical ID and installed folder: `hallmark`
- Import inventory: [`data/hallmark-import.json`](https://github.com/huytran1120/vie-agentic-skills/blob/main/data/hallmark-import.json)
- License: [`skills/hallmark/LICENSE`](https://github.com/huytran1120/vie-agentic-skills/blob/main/skills/hallmark/LICENSE)
- Installation manifests pin the **VAS publication commit**, not the upstream SHA.
