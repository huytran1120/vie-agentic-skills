# GameDev trong VAS / GameDev in VAS

## Tiếng Việt

Đã thêm **78 skill: 77 chuyên biệt và một router** từ
`gamedev-skills/awesome-gamedev-agent-skills`; **0 skill trùng phải bỏ qua**.
Catalog có **3.171 skill / 119 danh mục**. Các skill hỗ trợ Godot, Unity,
Unreal, Ebitengine, Bevy, Phaser, PixiJS, three.js, Defold, LÖVE, pygame,
Roblox, cùng game design, genres và quy trình phát hành.

Hai tên trùng nhưng **khác nội dung**, không phải bản nâng cấp hay mirror:

| Tên upstream | Canonical ID / thư mục cài VAS | Khác với bản đã có |
|---|---|---|
| `performance-optimization` | `gamedev-performance-optimization` | Game frame time/CPU/GPU, không phải hiệu năng web/database của Addy Osmani |
| `godot-export` | `gamedev-godot-export` | Build/phát hành ứng dụng Godot, không phải xuất mesh từ Blender |

Các tên khác giữ nguyên. Hai thư mục có tiền tố giúp cài đồng thời với bản cũ
mà không ghi đè hay đổi receipt của skill khác.

**Không cần clone:** mở [bộ GameDev](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&sources=gamedev),
chọn skill và agent rồi bấm **Copy Agent Prompt**, dán vào chat trong dự án.
Agent xác minh `install-manifests/<canonical-id>.json`, danh tính và
`available = true`, tải đủ tệp theo kích thước/SHA-256, giữ executable và ghi
`.vas-manifest.json` tương thích CLI. Bản giống nhau thì bỏ qua; khác nội dung
phải hỏi trước, không ghi đè.

**CLI:** từ kho VAS đã clone, thay đường dẫn dự án thật:

```bash
./vas search gamedev-skills
./vas show router
./vas install router --target cursor --mode link --dest "/Projects/my-app/.cursor/skills"
./vas status --target cursor --dest "/Projects/my-app/.cursor/skills"
./vas uninstall router --target cursor --dest "/Projects/my-app/.cursor/skills"
```

`--mode copy` tạo bản sao độc lập; `--mode link` cần giữ vị trí kho VAS.
Không có `--dest` thì đích nằm trong thư mục đang chạy lệnh. `--global` chỉ
dành cho một agent; `--target all` dùng bảy đích trong dự án, không dùng global.

| Agent | Thư mục trong dự án |
|---|---|
| Antigravity | `.agents/skills/<canonical-id>/` |
| Codex | `.codex/skills/<canonical-id>/` |
| Claude Code | `.claude/skills/<canonical-id>/` |
| Cursor | `.cursor/skills/<canonical-id>/` |
| Windsurf | `.windsurf/skills/<canonical-id>/` |
| Cline / Roo Code | `.cline/skills/<canonical-id>/` |
| GitHub Copilot CLI | `.github/skills/<canonical-id>/` |

### Đóng gói và prerequisites

**582 tệp** giữ đủ references, scripts, mẫu Go/Luau, assets, agent metadata,
LICENSE và NOTICE. Router độc lập kèm đủ 77 payload dưới `bundled/skills/`,
dùng `RUNBOOK.md` thay `SKILL.md` để không bị lập chỉ mục như skill mới.
Đường dẫn router được điều chỉnh và có `bundled/docs/VERSION-SUPPORT.md`.
Chỉ đọc companion được chọn và references cần thiết; không tải toàn bộ vào context.
Các skill chuyên biệt giữ đủ phụ thuộc tệp nội bộ của chính nó. Gợi ý phối hợp
skill khác không có nghĩa skill đó hoặc engine đã được cài.

Đọc/cài không cần engine; VAS CLI chỉ dùng Python 3. Khi thực thi phải có
engine/toolchain/SDK đúng phiên bản dự án. Helper ảnh của `create-game-assets`
cần **Pillow>=10,<14**; Ebitengine starter pin **v2.10.5 / Go 1.25+** và có
Go modules riêng; các helper Roblox economy cần **Luau**. Không tự cài runtime,
tải module/model, chạy helper, kết nối MCP/tài khoản hay dùng dịch vụ trả phí.
Tải/chạy mã, gửi dữ liệu riêng tư, signing và publish Steam/itch cần quyền riêng.
Giữ giấy phép **Go-Fonts (BSD-style)** trong starter; Apache-2.0 không thay thế
giấy phép của dependency, engine, asset hay điều khoản platform.

## English

VAS adds **78 canonical skills: 77 specialized skills plus one router**, with
**0 duplicate skips**, bringing the catalog to **3,171 skills / 119 categories**.
Only two genuinely different name collisions receive a `gamedev-` prefix:
game frame-time performance and whole-Godot-project builds are not the existing
Addy application-performance or Blender-to-Godot asset-export workflows.
Their distinct canonical IDs and installed folders are listed above; existing
skills and receipts are preserved.

**Without cloning:** open the [GameDev collection](https://huytran1120.github.io/vie-agentic-skills/?lang=en&sources=gamedev),
choose a skill/agent and paste **Copy Agent Prompt** into your project chat.
Each official manifest inventories all files, byte sizes, SHA-256, executable
flags and a CLI-compatible receipt. Check identity and `available = true`,
skip matching files and ask before conflicts. All download URLs pin the same
**VAS publication commit**, not the upstream SHA.

**CLI:** use the commands and exact agent-folder mapping above. Substitute your
project path and skill ID. Copy is independent; link needs the source checkout
to stay in place. Without `--dest`, the current directory is the project.
Global is for one agent, not `all`; quick `all` means seven current-project folders.

The **582-file** payload retains all local references/helpers, Go/Luau templates,
assets, agent metadata, executable modes and Apache-2.0 LICENSE/NOTICE.
The standalone router includes the complete specialized library as read-only
`bundled/skills/**/RUNBOOK.md` companions and a bundled version-support reference.
They are not additional catalog entries or auto-registered agent skills. Load
only the selected companion/reference. Specialized skills include their own local
file dependencies; composition hints do not install other skills or engines.

Actual workflows need a compatible engine/toolchain/SDK. Optional image helpers
need **Pillow>=10,<14**; the Ebitengine starter pins **v2.10.5 / Go 1.25+** and
downloads its own modules only after approval; Roblox economy helpers use **Luau**.
No helper, generated game, engine, package or downloaded code was run for this
import. No runtime/MCP/plugin was installed, account connected, paid asset
generated or build published. Permission, privacy review and separate credentials
are required before downloads, execution, services, signing or publishing.
Retain the starter's separate **BSD-style Go-Fonts** notice and dependency terms.
Pinned engine baselines are snapshots, not claims about the newest release.

## Provenance

- Source: [gamedev-skills/awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/tree/19d93f97c9c1ea0f8b306e77aa81e0d3e352d3e9)
- Upstream SHA: `19d93f97c9c1ea0f8b306e77aa81e0d3e352d3e9`
- Copyright 2026 Abhishek Barali and the awesome-gamedev-agent-skills contributors
- License: [Apache-2.0](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/19d93f97c9c1ea0f8b306e77aa81e0d3e352d3e9/LICENSE)
- [Original NOTICE](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/19d93f97c9c1ea0f8b306e77aa81e0d3e352d3e9/NOTICE)
- Inventory, naming/path adaptations, upstream blobs and original/vendored SHA-256:
  [`data/gamedev-import.json`](https://github.com/huytran1120/vie-agentic-skills/blob/main/data/gamedev-import.json)
- VAS category: `game-development`; source folder groups remain in metadata tags.
