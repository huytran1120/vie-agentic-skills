# Android trong VAS / Android in VAS

## Tiếng Việt

VAS nhập **35 skill mới** từ `android/skills`, Apache-2.0, của Google LLC và
Android Open Source Project. **Bỏ qua `android-cli`** vì catalog đã có cùng
canonical ID và quy trình cho Android CLI; không nâng cấp, ghi đè hay tạo namespace.
Tổng catalog sau lần nhập: **3.093 skill / 119 danh mục**.

Mỗi skill độc lập giữ đủ `SKILL.md`, references, mẫu Kotlin/XML, trace configs
và scripts nếu upstream có, cùng bản đầy đủ `LICENSE.txt`. Có **478 tệp** trong
35 payload; giữ nguyên nội dung hỗ trợ và quyền executable. Chỉ chuẩn hóa
description/license trong YAML và thêm ghi chú VAS có thể đối chiếu ngược;
không nhập marketplace wrapper hay cấu hình CI của upstream.

**Không cần clone:** mở [bộ Android](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&sources=android),
chọn skill, chọn agent, bấm **Copy Agent Prompt** rồi dán vào chat trong dự án.
Agent đọc `install-manifests/<canonical-id>.json` trên website chính thức, kiểm
tra danh tính và `available = true`, tải đủ tệp, xác minh kích thước/SHA-256,
giữ executable và ghi receipt `.vas-manifest.json` tương thích CLI.
Nếu nội dung đã đúng thì bỏ qua; có xung đột phải hỏi, không ghi đè.

**CLI:** từ kho VAS đã clone, thay `/Projects/my-app` bằng dự án thật:

```bash
./vas search android/skills
./vas show navigation-3
./vas install navigation-3 --target cursor --mode link --dest "/Projects/my-app/.cursor/skills"
./vas status --target cursor --dest "/Projects/my-app/.cursor/skills"
./vas uninstall navigation-3 --target cursor --dest "/Projects/my-app/.cursor/skills"
```

`--mode link` cần giữ nguyên vị trí kho VAS; `--mode copy` tạo bản sao độc lập.
Không có `--dest` thì đích nằm trong thư mục đang chạy lệnh. `--global` chỉ dành
cho một agent; `--target all` dùng bảy đích trong dự án. Cài từng skill bằng
canonical ID trong bảng phía dưới; không cần cài cả bộ.

| Agent | Thư mục trong dự án |
|---|---|
| Antigravity | `.agents/skills/<canonical-id>/` |
| Codex | `.codex/skills/<canonical-id>/` |
| Claude Code | `.claude/skills/<canonical-id>/` |
| Cursor | `.cursor/skills/<canonical-id>/` |
| Windsurf | `.windsurf/skills/<canonical-id>/` |
| Cline / Roo Code | `.cline/skills/<canonical-id>/` |
| GitHub Copilot CLI | `.github/skills/<canonical-id>/` |

### Prerequisites và quyền thực thi

Đọc/cài runbook không cần Android SDK; VAS CLI chỉ cần Python 3. Khi thực sự
dùng workflow, phải kiểm tra phiên bản SDK/JDK/Gradle/thư viện, thiết bị/emulator,
preview access và tài khoản theo skill. Không tự cài SDK, plugin, MCP, thư viện,
model hay chạy mã tải về trong quá trình nhập/cài skill.

- `r8-analyzer`: có đủ `analyze.py`, `convert_pb_to_json.py`, `keep_radius_pb2.py`;
  converter cần `google.protobuf` tương thích mã sinh **6.33.4**, không cài sẵn.
- `play-policy-insights`: có đủ scanner, scraper, `template_engine.py`, prompts
  và report template. Scraper có thể đọc Play Store qua mạng; báo cáo hỗ trợ rà
  soát, không bảo đảm tuân thủ pháp lý hay được Google Play duyệt.
- `android-profiler`: có launcher Perfetto Python, không có native binary.
  Launcher có thể tải/cache/chạy binary theo URL/hash trong mã; phải kiểm tra
  cache destination và xin phép trước. Tệp launcher upstream không executable;
  giữ nguyên quyền, chỉ dùng `python3` sau khi được duyệt.

Xin phép trước khi tải/chạy installer, thay đổi thiết bị, thu thập trace, kết
nối dịch vụ, gửi source/thông tin riêng tư hoặc phát sinh chi phí. Các tài liệu
ngoài kho, model, SDK và dịch vụ có điều khoản riêng, không được đóng gói.
Trong lần nhập này không chạy helper, cài runtime hay kết nối thiết bị/dịch vụ.

## English

VAS imports **35 new Android skills** under Apache-2.0 by Google LLC and the
Android Open Source Project. **One skill, `android-cli`, is skipped**: the
existing canonical skill already covers the same CLI workflow and stays unchanged.
No upgrade or namespace is introduced. Catalog total: **3,093 skills / 119 categories**.

The **478-file** payload preserves every skill's references, Kotlin/XML samples,
trace configurations, scripts and executable modes, plus the complete upstream
`LICENSE.txt` in each standalone folder. Only reversible YAML description/license
normalization and VAS notes differ. Repository marketplace wrappers and CI are
not part of the installed payload.

**Without cloning:** open the [Android collection](https://huytran1120.github.io/vie-agentic-skills/?lang=en&sources=android),
select a skill and agent, copy **Copy Agent Prompt** and paste it into your
project's agent chat. The official per-skill manifest lists all files, byte
sizes, SHA-256, executable flags and the CLI-compatible receipt. Check identity
and `available = true`, skip matching installations and ask before replacing
conflicting contents. The manifest pins the **VAS publication commit**, not
the upstream revision.

**CLI:** use the commands above from a VAS checkout. Substitute the actual
project path and agent mapping in the table; `--mode copy` is independent,
while `--mode link` needs the checkout to stay in place. Without `--dest`, the
current directory is the project. Global applies to one agent, not `all`;
quick-install `all` means the seven current-project folders.

Reading/installing does not need Android SDK. Executing a workflow needs the
matching SDK/JDK/Gradle/libraries and, where applicable, a device/emulator, preview
access or account. The R8 converter's generated module declares protobuf **6.33.4**;
its local helper is bundled, its Python runtime dependency is not installed.
Play Policy includes all local helpers/templates but can make Play Store network
requests; reports are assistance, not legal or store-approval guarantees.
The bundled non-executable Perfetto Python launcher can download/cache/execute
native binaries: review its URL/hash and cache destination before permission to
run it with `python3`. No helpers or downloaded code were run during this import.

Obtain permission before installation/downloads, device changes, tracing,
network/service use, sensitive-data submission or paid operations. SDKs, models,
external documents and services are separate prerequisites with their own terms.
Skill installation never provisions them, connects devices, configures MCP/plugins
or submits project data.

## Skills

Canonical IDs and standalone installed folder names are identical:

| Area | Canonical IDs |
|---|---|
| Build | `agp-9-upgrade` |
| Camera / cars | `camerax`, `android-for-cars-parked-apps` |
| On-device AI | `appfunctions`, `litert-lm`, `litert-runtime`, `ml-kit-genai-prompt-api`, `mlkit-agent-api` |
| Identity | `restore-credentials`, `verified-email` |
| Compose | `adaptive`, `ink-app-builder`, `ink-custom-brush-builder`, `jetpack-compose-performance`, `migrate-xml-views-to-jetpack-compose` |
| Media / navigation | `media3-cast-integration`, `navigation-3`, `navigation-event` |
| Performance | `anr-audit-and-fix`, `r8-analyzer`, `android-profiler` |
| Play | `engage-sdk-integration`, `play-billing-library-version-upgrade`, `play-policy-insights` |
| Security | `android-intent-security`, `android-permissions-security` |
| System / widgets | `edge-to-edge`, `glance-appwidget-updates-and-memory`, `glance-canonical-layouts` |
| Testing / TV | `testing-setup`, `leanback-to-compose-tv-migration` |
| Wear / XR | `wear-compose-m3`, `wear-widgets`, `display-glasses-with-jetpack-compose-glimmer`, `projected-hardware` |

## Provenance

- Source: [android/skills](https://github.com/android/skills/tree/6daa53ef27fa2aa87827d183a85c06cedceca833)
- Upstream SHA: `6daa53ef27fa2aa87827d183a85c06cedceca833`
- License: [Apache-2.0](https://github.com/android/skills/blob/6daa53ef27fa2aa87827d183a85c06cedceca833/LICENSE.txt);
  all original Google/AOSP copyright headers are retained.
- Inventory/adaptations/skip record: [`data/android-import.json`](https://github.com/huytran1120/vie-agentic-skills/blob/main/data/android-import.json)
- VAS metadata category: `mobile`; original source paths and keywords remain recorded.
