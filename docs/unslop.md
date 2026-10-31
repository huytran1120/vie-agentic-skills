# UI Unslop trong VAS / UI Unslop in VAS

## Tiếng Việt

Đã thêm **1 skill mới / 19 tệp**, không có bản trùng phải bỏ qua.
Catalog: **3.172 skill / 119 danh mục**.
Đây là workflow UI của **Damir Sokolovsky ([@heydamir](https://x.com/heydamir))**:
audit, xác nhận direction rồi sửa spacing, color, icons, copy, type, layout,
details, visuals và motion. Giữ nội dung/feature và không đổi màn hình tốt
chỉ để tạo khác biệt. Không dùng skill này để thiết kế lại giao diện VAS khi nhập.

Tên upstream `unslop` trùng với skill **xử lý văn bản bằng CLI** của
MohamedAbdallah-14, nhưng khác nguồn và toàn bộ workflow. Canonical ID và
thư mục mới là **`heydamir-unslop`**; có thể cài cùng bản cũ mà không ghi đè.
Đã đối chiếu 3.171 bản ghi theo ID, repo/thư mục, hash, body chuẩn hóa,
body đổi tên, containment và shingles; không có fork/mirror hay bản đổi tên cùng nội dung.

**Không cần clone:** mở [UI Unslop](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&skill=heydamir-unslop&agent=cursor),
chọn agent, bấm **Copy Agent Prompt** rồi dán vào chat của dự án.
Agent kiểm tra danh tính và `available = true` của
`install-manifests/heydamir-unslop.json`, tải đủ tệp theo byte size/SHA-256,
giữ executable và ghi receipt `.vas-manifest.json` tương thích CLI.
Snapshot giống nhau thì bỏ qua; khác nội dung phải hỏi trước khi ghi đè.
URL tệp pin cùng một **commit VAS**, không phải SHA upstream.

**CLI:** từ checkout VAS, thay đường dẫn bằng đích thật:

```bash
./vas search heydamir
./vas show heydamir-unslop
./vas install heydamir-unslop --target cursor --mode copy --dest "/Projects/my-app/.cursor/skills"
./vas status --target cursor --dest "/Projects/my-app/.cursor/skills"
./vas uninstall heydamir-unslop --target cursor --dest "/Projects/my-app/.cursor/skills"
```

`--mode link` cần giữ vị trí checkout; `--mode copy` độc lập.
Không có `--dest` thì thư mục đang chạy lệnh là dự án đích.
`--global` chỉ dùng cho một agent; `--target all` dùng bảy đích trong dự án,
không kết hợp global.

| Agent | Thư mục cài trong dự án |
|---|---|
| Antigravity | `.agents/skills/heydamir-unslop/` |
| Codex | `.codex/skills/heydamir-unslop/` |
| Claude Code | `.claude/skills/heydamir-unslop/` |
| Cursor | `.cursor/skills/heydamir-unslop/` |
| Windsurf | `.windsurf/skills/heydamir-unslop/` |
| Cline / Roo Code | `.cline/skills/heydamir-unslop/` |
| GitHub Copilot CLI | `.github/skills/heydamir-unslop/` |

### Giấy phép, đóng gói và prerequisites

**CC-BY-4.0**, không phải MIT. Giữ credit Damir Sokolovsky, link repo gốc,
LICENSE/CITATION.cff và chỉ rõ thay đổi khi phân phối/adapt; không hàm ý tác giả
endorse VAS. Giữ cả credit trong reference và video của helper.
Đủ SKILL.md, 5 reference, 5 hình WebP, 2 helper, 2 ví dụ HTML với asset chung,
LICENSE, CITATION.cff và ADAPTATIONS.md. Các tệp upstream đều không có bit executable;
chạy helper bằng Node chỉ khi được yêu cầu và đã duyệt mã.

VAS đổi YAML name để namespace, thêm notes và thay **chỉ diagnostic**
thiếu Playwright của hai helper bằng hướng dẫn setup cần quyền, không NPX.
Workflow, hình, ví dụ và logic helper vẫn nguyên; hash/Git blob gốc và bản
đóng gói cùng thay đổi đảo ngược được ghi trong `data/unslop-import.json`.

Đọc runbook không cần runtime ngoài agent. Helper snapshot/story tùy chọn cần
Node.js, Playwright hoặc playwright-core và browser tương thích; video cần ffmpeg.
`CHROME_PATH` chọn browser hiện có khi phù hợp. Không tự tải dependency/browser,
cài MCP, kết nối tài khoản/dịch vụ hoặc tạo ảnh trả phí. Setup cần quyền riêng
và package manager của dự án. Snapshot mở URL, chạy JavaScript website, tải
CSS/ảnh/font; chỉ dùng trang được phép và kiểm tra copyright, quyền riêng tư,
authentication/điều khoản dịch vụ. Story chạy HTML, phục vụ thư mục local,
ghi video và xóa frames tạm; phải duyệt trước và hỏi khi ghi đè.
Tải/chạy mã, gửi dữ liệu riêng tư, tạo ảnh trả phí, upload và publish cần
authorization riêng cùng budget khi áp dụng. Không helper hay example nào
được chạy trong quá trình nhập.

## English

VAS adds **one new UI skill / 19 files**, with **zero duplicate skips**, bringing
the catalog to **3,172 skills / 119 categories**. Damir Sokolovsky's UI Unslop
audits a screen, confirms direction and applies nine craft passes. It is
unrelated to the existing MohamedAbdallah-14 prose-processing CLI skill;
**`heydamir-unslop`** is its distinct canonical ID and installed folder.
Both workflows coexist without replacement. Existing revisions are not upgraded.

**Without cloning:** open [UI Unslop](https://huytran1120.github.io/vie-agentic-skills/?lang=en&skill=heydamir-unslop&agent=cursor),
choose an agent and paste **Copy Agent Prompt** into your project chat.
Check manifest identity, `available = true`, full size/SHA-256/mode inventory
and the CLI receipt. Skip matching payloads; ask before conflicting overwrite.
All download URLs pin the same VAS publication commit, not the upstream SHA.
The CLI commands and seven exact agent paths above apply to both languages:
copy is standalone, link needs the checkout, no `--dest` means the current
project, global is for one agent and `all` means seven project folders.

The complete payload includes original references/visuals/helpers, top-level
examples with their shared asset, LICENSE and CITATION.cff, plus VAS notes.
**CC-BY-4.0** attribution to **Damir Sokolovsky ([@heydamir](https://x.com/heydamir))**,
original repository link and license remain mandatory in copies/adaptations;
identify modifications and do not imply endorsement. It is not relicensed MIT.
Only the YAML name, appended packaging notes and missing-Playwright diagnostics
change; helper logic and visuals remain intact, with original/vendored hashes
and reversible changes recorded. Original modes are all non-executable.

Optional helpers need Node.js, Playwright/playwright-core and a compatible
browser; video also needs ffmpeg. Use an existing browser via `CHROME_PATH`
where applicable. No package/browser/MCP setup, helper/example execution,
image-service connection, paid generation or publishing is automatic.
An authorized snapshot visits a URL, executes site JavaScript and may fetch
remote styles/images/fonts; respect copyright, privacy, authentication and terms.
Story playback executes local HTML and serves its directory; rendering writes
video output and removes temporary frames. Review code and request approval
before downloads, execution or overwrites, sensitive data, service/account
connection, paid generation, uploads and publication; agree a budget if relevant.
The VAS interface remains unchanged apart from catalog integration.

## Provenance

- Author: Damir Sokolovsky / [@heydamir](https://x.com/heydamir)
- Source: [heydamir/unslop](https://github.com/heydamir/unslop/tree/4652254daff586ff4739849395a127b56f7f8cc7)
- Upstream SHA: `4652254daff586ff4739849395a127b56f7f8cc7`
- License: [CC-BY-4.0](https://github.com/heydamir/unslop/blob/4652254daff586ff4739849395a127b56f7f8cc7/LICENSE)
- Canonical ID: `heydamir-unslop`; category: `front-end`
- [Import manifest and reversible adaptations](https://github.com/huytran1120/vie-agentic-skills/blob/main/data/unslop-import.json)
