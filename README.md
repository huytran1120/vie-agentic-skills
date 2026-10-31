# 🇻🇳 Vie Agentic Skill (VAS)

<p align="center">
  <a href="#vietnamese"><b>🇻🇳 Tiếng Việt</b></a> &nbsp;|&nbsp;
  <a href="#english"><b>🇬🇧 English (In-page)</b></a> &nbsp;|&nbsp;
  <a href="README_EN.md"><b>🇬🇧 English Edition (README_EN.md)</b></a>
</p>

<p align="center">
  <b>Universal, Modular Agentic Skills Catalog for AI Coding Agents</b><br>
  <i>Empowering Google Antigravity, OpenAI Codex, Claude Code, Cursor, Windsurf, Cline & GitHub Copilot CLI</i>
</p>

<p align="center">
  <a href="https://github.com/huytran1120/vie-agentic-skills"><img src="https://img.shields.io/badge/Agents-Antigravity%20%7C%20Codex%20%7C%20Claude%20%7C%20Cursor%20%7C%20Windsurf%20%7C%20Cline%20%7C%20Copilot-blueviolet?style=for-the-badge" alt="Universal Agents" /></a>
  <a href="https://github.com/huytran1120/vie-agentic-skills"><img src="https://img.shields.io/badge/Google%20Antigravity-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Antigravity" /></a>
  <a href="https://github.com/huytran1120/vie-agentic-skills"><img src="https://img.shields.io/badge/OpenAI%20Codex-412991?style=for-the-badge&logo=openai&logoColor=white" alt="Codex" /></a>
  <a href="https://github.com/huytran1120/vie-agentic-skills"><img src="https://img.shields.io/badge/Claude%20Code-D97706?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude Code" /></a>
  <a href="https://github.com/huytran1120/vie-agentic-skills"><img src="https://img.shields.io/badge/Cursor-000000?style=for-the-badge&logo=cursor&logoColor=white" alt="Cursor" /></a>
  <a href="https://github.com/huytran1120/vie-agentic-skills"><img src="https://img.shields.io/badge/Windsurf-09B6A2?style=for-the-badge&logo=codeium&logoColor=white" alt="Windsurf" /></a>
</p>
<p align="center">
  <a href="https://huytran1120.github.io/vie-agentic-skills/"><img src="https://img.shields.io/badge/Live%20Catalog-GitHub%20Pages-00C853?style=for-the-badge&logo=githubpages&logoColor=white" alt="GitHub Pages Catalog" /></a>
  <a href="CATALOG.md"><img src="https://img.shields.io/badge/Catalog-3%2C057%2B%20Skills-00C853?style=for-the-badge" alt="Skills Count" /></a>
  <a href="vas.py"><img src="https://img.shields.io/badge/Zero--NPX-Pure%20Python%203-FF6D00?style=for-the-badge" alt="Zero NPX" /></a>
  <a href="https://github.com/huytran1120"><img src="https://img.shields.io/badge/Author-huytran1120-6200EA?style=for-the-badge&logo=github" alt="Author" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License: MIT" /></a>
</p>

> 🌐 **Web Explorer / Tra cứu kỹ năng trực quan**: [GitHub Pages](https://huytran1120.github.io/vie-agentic-skills/) · [Bản xem trước local](http://127.0.0.1:8765/docs/)  
> 🎨 **Bộ sưu tập mới nổi bật**: Đã tích hợp trọn bộ **94 kỹ năng Blender Studio** ([arjun988/blender-skills](https://github.com/arjun988/blender-skills)) cho 3D modeling, texturing, animation và pipeline! Xem chi tiết tại mục [Blender Studio](#blender-studio).

Giao diện web ưu tiên danh mục: tìm theo từ khóa/tác giả/nguồn, lọc danh mục, chọn agent và sao chép lệnh cài ngay trong kết quả. Số lượng lấy trực tiếp từ catalog; không có số lượt tải hoặc đánh giá giả. Website chỉ cung cấp lệnh, không tự cài vào máy.  
* **Chạy local**: `python3 -m http.server 8765 --bind 127.0.0.1` và mở `http://127.0.0.1:8765/docs/`.  
* **Kiểm tra giao diện**: `node --test tests/pages.test.cjs`.  
* **Tự động triển khai**: GitHub Pages tự triển khai từ `main` qua `.github/workflows/deploy-pages.yml` (hoặc build artifact bằng `python3 scripts/build_pages.py` tạo `_site/`).

---

<a id="vietnamese"></a>
## 🇻🇳 Tiếng Việt

### 📌 Mục Lục
- [1. Giới Thiệu](#1-giới-thiệu)
- [2. Hỗ Trợ Đa Nền Tảng (Multi-Agent Compatibility)](#2-hỗ-trợ-đa-nền-tảng-multi-agent-compatibility)
- [3. Vì Sao Chọn Vie Agentic Skill?](#3-vì-sao-chọn-vie-agentic-skill)
- [4. Cài Đặt & Sử Dụng Nhanh (Quickstart)](#4-cài-đặt--sử-dụng-nhanh-quickstart)
- [5. Hướng Dẫn Từng AI Agent](#5-hướng-dẫn-từng-ai-agent)
- [6. Cẩm Nang Lệnh CLI (`./vas`)](#6-cẩm-nang-lệnh-cli-vas)
- [7. Cấu Trúc Chuẩn Của Một Skill](#7-cấu-trúc-chuẩn-của-một-skill)
- [8. Vòng Đời Kỹ Thuật Chuẩn Cấp Cao & Bộ 25 Kỹ Năng Addy Osmani](#8-vòng-đời-kỹ-thuật-chuẩn-cấp-cao--bộ-25-kỹ-năng-addy-osmani)
- [9. Hệ Thống 7 Checklist Kỹ Thuật & Hội Đồng Thẩm Định Personas](#9-hệ-thống-7-checklist-kỹ-thuật--hội-đồng-thẩm-định-personas)
- [10. Bảng So Sánh Chi Tiết (How VAS Compares)](#10-bảng-so-sánh-chi-tiết-how-vas-compares)
- [11. Danh Mục & Top 20 Siêu Kỹ Năng Nổi Bật](#11-danh-mục--top-20-siêu-kỹ-năng-nổi-bật)
- [12. Câu Hỏi Thường Gặp (FAQ)](#12-câu-hỏi-thường-gặp-faq)
- [13. Tác Giả & Giấy Phép](#13-tác-giả--giấy-phép)

---

### 1. Giới Thiệu

**Vie Agentic Skill (VAS)** là dự án do **Huy Tran** ([@huytran1120](https://github.com/huytran1120)) sáng lập và phát triển, với mục tiêu **tổng hợp, chọn lọc và chuẩn hóa toàn bộ các kỹ năng agentic (agent skills) tốt nhất trên thế giới** cho các AI Coding Agent.

Thay vì để các kỹ năng bị phân mảnh ở nhiều công cụ, định dạng hay nền tảng khác nhau, VAS quy tụ hơn **3,172+ playbooks (`SKILL.md`)** chuyên sâu thuộc **119 danh mục công nghệ**, được chuẩn hóa nghiêm ngặt theo **Chuẩn mở Agent Skills Quốc tế ([agentskills.io](https://agentskills.io/))**. Dự án tổng hợp tinh hoa từ các chuyên gia, tổ chức kỹ thuật và cộng đồng mã nguồn mở uy tín nhất toàn cầu (như Addy Osmani, Cloudflare, Matt Pocock, Blender Studio, Google Devs, Open Agent Skills...).

Với VAS, các AI Coding Agent không còn là lập trình viên chung chung sinh code nông cạn, mà biến thành các cộng sự kỹ thuật cấp Senior thực thụ: có checklist bảo mật, quy trình kiểm thử TDD, công thức tối ưu và kịch bản thực thi chính xác.

---

### 2. Hỗ Trợ Đa Nền Tảng (Multi-Agent Compatibility)

VAS hỗ trợ cài đặt bằng một câu lệnh duy nhất cho tất cả các AI coding tools thịnh hành nhất hiện nay:

| AI Agent / IDE | Thư Mục Đích | Lệnh Cài Đặt Nhanh |
| :--- | :--- | :--- |
| **Google Antigravity** | `.agents/skills/` hoặc `~/.gemini/antigravity/skills/` | `./vas install <skill> --target antigravity` |
| **OpenAI Codex / OpenCode** | `.codex/skills/` hoặc `.agents/skills/` | `./vas install <skill> --target codex` |
| **Claude Code** | `.claude/skills/` hoặc `~/.claude/skills/` | `./vas install <skill> --target claude` |
| **Cursor IDE** | `.cursor/skills/` | `./vas install <skill> --target cursor` |
| **Windsurf (Codeium)** | `.windsurf/skills/` | `./vas install <skill> --target windsurf` |
| **Cline / Roo Code** | `.cline/skills/` | `./vas install <skill> --target cline` |
| **GitHub Copilot CLI** | `.github/skills/` | `./vas install <skill> --target copilot` |
| **TẤT CẢ CÁC AGENTS** | Đồng bộ vào toàn bộ thư mục trên | `./vas install <skill> --target all` |

---

### 3. Vì Sao Chọn Vie Agentic Skill?

| Tiêu Chí | Giải Pháp Cũ (`npx`) | Vie Agentic Skill (VAS) |
| :--- | :--- | :--- |
| **Công cụ quản lý** | Bắt buộc Node.js & gọi `npx` từ xa | **Native Python 3 CLI (`./vas`)** dùng thư viện chuẩn |
| **Kết nối mạng** | Cần Internet mỗi lần chạy `npx` | **100% Offline & Zero Dependencies** |
| **Tốc độ phản hồi** | 3s - 15s mỗi lần chạy | **< 0.05 giây** (tức thì) |
| **Khả năng tương thích** | Giới hạn hoặc nạp thủ công | **Hỗ trợ 7+ AI Agent lớn** (Antigravity, Codex, Claude, Cursor, Windsurf, Cline, Copilot) |
| **Cơ chế cài đặt** | Copy thủ công | Hỗ trợ cả **Symlink** (`--mode link`) và **Copy nguyên tử** với cơ chế phục hồi tự động |
| **Bảo toàn ngữ cảnh** | Dễ gây phình token ngữ cảnh | Tuân thủ tuyệt đối **Progressive Disclosure** (tiết kiệm 99% prompt token) |

---

### 4. Cài Đặt & Sử Dụng Nhanh (Quickstart)

#### Cách 1: Copy Agent Prompt — không cần clone kho

Mở [thư viện skill](https://huytran1120.github.io/vie-agentic-skills/?lang=vi),
tìm skill, chọn agent rồi bấm **Copy prompt** ở kết quả hoặc **Copy Agent Prompt**
trong trang chi tiết. Dán prompt vào chat của agent trong dự án đang mở.
Prompt tự điền đúng ID, thư mục agent và manifest chính thức.

Agent tải **đủ bộ tệp**, gồm `SKILL.md`, scripts, templates, references, license
và tài nguyên đi kèm; kiểm tra SHA-256 từ cùng một snapshot VAS. Đã cài đúng thì
bỏ qua; nội dung khác hoặc trùng tên skill khác thì hỏi trước, không tự ghi đè.
Không cần clone, chạy `./vas` hay cài thêm Python cho cách này.

Ví dụ cho Cursor với skill YouTube:

```text
Hãy cài skill "youtube-agent-skill/yt-script" vào dự án hiện tại cho Cursor,
tại ".cursor/skills/yt-script/". Đọc manifest chính thức:
https://huytran1120.github.io/vie-agentic-skills/install-manifests/youtube-agent-skill/yt-script.json
Kiểm tra đúng skill và available = true; tải đủ các tệp được liệt kê, giữ cấu trúc
và kiểm tra SHA-256 trước khi hoàn tất. Không clone kho, đi xuyên symlink hay ghi
ra ngoài dự án. Đã có đúng nội dung thì bỏ qua; khác nội dung hoặc receipt hỏng
thì hỏi trước, không ghi đè. Ghi receipt vào .vas-manifest.json trong thư mục skills
của agent, giữ các mục khác. Đọc SKILL.md, báo đường dẫn và yêu cầu còn thiếu.
Không tự chạy scripts, cài dependency hoặc kết nối dịch vụ; lỗi tải/hash thì dừng.
```

Agent cần quyền mạng và ghi tệp; runbook có thể cần runtime/MCP riêng hoặc nạp
lại danh sách skill của ứng dụng. Website chỉ sao chép hướng dẫn, không tự cài
lên máy. Các lựa chọn global/link/đường dẫn tuyệt đối chỉ dành cho CLI bên dưới.
Chọn `all` trong luồng chat chỉ cài vào bảy thư mục agent của **dự án hiện tại**.

#### Cách 2: CLI — quản lý offline, link/copy và nhiều skill

```bash
# Bước 1: Clone hoặc mở thư mục dự án
git clone https://github.com/huytran1120/vie-agentic-skills.git
cd vie-agentic-skills
chmod +x vas vas.py

# Bước 2: Tìm kiếm kỹ năng
./vas search docker-expert
./vas list --category security --limit 10
./vas categories

# Bước 3: Cài đặt cho AI Agent bạn đang dùng
./vas install ui-ux-pro-max --target codex
./vas install docker-expert --target antigravity
./vas install fastapi-pro --target claude
./vas install react-component-performance --target cursor

# Cài cho tất cả AI Agent trong dự án:
./vas install ui-ux-pro-max 007 pdf --target all
```
*(Hệ thống hỗ trợ bí danh tự động: các lệnh gọi như `docker-security`, `fastapi-best-practices`, `react-performance`, `nextjs-perf` sẽ tự động trỏ tới skill thực).*

**Chọn đúng nơi cài:** lệnh không có `--dest` hoặc `--global` cài vào thư mục
agent bên trong thư mục đang chạy lệnh, không tự tìm dự án khác. Trên website,
mở một skill, chọn agent và “Dự án cụ thể” hoặc “Toàn máy”; lệnh cài, kiểm tra
và gỡ đều dùng cùng nơi đã chọn. Ví dụ chạy từ kho VAS để cài cho dự án khác:

```bash
./vas install code-review --target codex --mode link --dest "/Projects/my-app/.codex/skills"
./vas status --target codex --dest "/Projects/my-app/.codex/skills"
./vas uninstall code-review --target codex --dest "/Projects/my-app/.codex/skills"
```

Thay `/Projects/my-app` bằng đường dẫn dự án thật. Dùng `--global` thay cho
`--dest` nếu cài toàn máy cho một agent; không kết hợp `--target all` với
`--global`. `--mode link` cần giữ nguyên vị trí kho VAS; `--mode copy` tạo bản
sao độc lập, cần cài lại để cập nhật. Sau khi cài, mở dự án trong agent, nạp lại
danh sách skill nếu cần và yêu cầu đọc runbook đã cài trước khi thực hiện tác vụ.
Website có lệnh `status`, lệnh gỡ và prompt mẫu với đúng đường dẫn, kể cả skill
có namespace như `blender-skills/blender-director`.

---

#### Hallmark: thiết kế frontend theo yêu cầu

[Mở Hallmark trên catalog](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&skill=hallmark),
chọn agent và **Copy Agent Prompt** để cài đủ 182 tệp mà không cần clone.
Hallmark là **1 skill**, kèm 50 theme, references, ảnh mẫu, scripts và MIT notice;
không tự thay giao diện hiện có hoặc chạy helper sau khi cài.

Từ kho VAS, thay `/Projects/my-app` bằng đường dẫn dự án của bạn:

```bash
./vas install hallmark --target cursor --mode link --dest "/Projects/my-app/.cursor/skills"
./vas status --target cursor --dest "/Projects/my-app/.cursor/skills"
./vas uninstall hallmark --target cursor --dest "/Projects/my-app/.cursor/skills"
```

`--mode copy` tạo bản sao độc lập thay cho symlink. Đọc runbook không cần Node;
helper cần Node.js 18+, kiểm tra render cần Chrome và Puppeteer riêng.
Sinh ảnh Together AI là tùy chọn có thể mất phí; từng ảnh trong photo catalog
giữ giấy phép/ghi công riêng. Xem [hướng dẫn Hallmark VI/EN](docs/hallmark.md)
để chọn đúng thư mục cho từng agent và xem đầy đủ prerequisites.

#### TypeSafe: tích hợp Jev/System One

[Mở TypeSafe trên catalog](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&skill=typesafe-ai),
chọn agent và **Copy Agent Prompt** để cài đủ `SKILL.md` và `LICENSE` mà không
cần clone. Từ kho VAS, thay `/Projects/my-app` bằng dự án thật:

```bash
./vas install typesafe-ai --target cursor --mode link --dest "/Projects/my-app/.cursor/skills"
./vas status --target cursor --dest "/Projects/my-app/.cursor/skills"
./vas uninstall typesafe-ai --target cursor --dest "/Projects/my-app/.cursor/skills"
```

`--mode copy` tạo bản sao độc lập thay cho symlink. Skill dùng MIT; chỉ việc gọi
API mới cần quyền truy cập TypeSafe và `TYPESAFE_API_KEY` ở server. Không tự cài
SDK, đọc key hoặc gửi dữ liệu; probe API cần xin phép, công bố dữ liệu và thống
nhất ngân sách trước. Xem [hướng dẫn TypeSafe VI/EN](docs/typesafe.md) để chọn đúng
thư mục cho mọi agent và xem đầy đủ prerequisites.

#### Android — 35 skill mới từ Google

[Mở bộ Android](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&sources=android),
chọn skill và agent rồi **Copy Agent Prompt** để cài đủ tệp mà không cần clone.
Đã giữ nguyên `android-cli` có sẵn; không nâng cấp hay đổi tên để nhập lại.
Ví dụ từ kho VAS:

```bash
./vas install navigation-3 --target cursor --mode link --dest "/Projects/my-app/.cursor/skills"
./vas status --target cursor --dest "/Projects/my-app/.cursor/skills"
./vas uninstall navigation-3 --target cursor --dest "/Projects/my-app/.cursor/skills"
```

`--mode copy` tạo bản sao độc lập. Mỗi skill giữ Apache-2.0, `LICENSE.txt`,
references, mẫu code và helper liên quan. SDK/JDK/Gradle, protobuf cho R8,
thiết bị và tải binary Perfetto là prerequisites riêng; không tự chạy/cài hoặc
gửi dữ liệu. Xem [hướng dẫn Android VI/EN](docs/android.md) để chọn đúng thư mục
agent, xem đủ danh sách và yêu cầu trước khi sử dụng.

#### GameDev — 77 skill chuyên biệt và một router

[Mở bộ GameDev](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&sources=gamedev),
chọn skill và agent rồi **Copy Agent Prompt** để cài đủ tệp, không cần clone.
Router kèm thư viện 77 companion để cài riêng vẫn định tuyến được; companion
không tạo thêm bản ghi catalog. Ví dụ từ kho VAS:

```bash
./vas install router --target cursor --mode link --dest "/Projects/my-app/.cursor/skills"
./vas status --target cursor --dest "/Projects/my-app/.cursor/skills"
./vas uninstall router --target cursor --dest "/Projects/my-app/.cursor/skills"
```

`--mode copy` tạo bản sao độc lập. Giữ Apache-2.0, LICENSE/NOTICE, quyền executable
và giấy phép Go-Fonts đi kèm. Chỉ hai skill khác nội dung nhưng trùng tên dùng
`gamedev-performance-optimization` và `gamedev-godot-export`; bản cũ không thay đổi.
Không tự cài engine/Pillow, chạy helper hay publish game. Xem
[hướng dẫn GameDev VI/EN](docs/gamedev.md) cho mapping agent và prerequisites.

#### UI Unslop — Damir Sokolovsky

[Mở UI Unslop](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&skill=heydamir-unslop&agent=cursor),
chọn agent và **Copy Agent Prompt** để cài đủ 19 tệp, không cần clone.
ID `heydamir-unslop` phân biệt workflow chỉnh UI với `unslop` xử lý văn bản đã có.
Giữ **CC-BY-4.0**, credit Damir Sokolovsky ([@heydamir](https://x.com/heydamir)),
nguồn [heydamir/unslop](https://github.com/heydamir/unslop), LICENSE và các điều chỉnh
được ghi lại; không đổi giấy phép thành MIT.

```bash
./vas install heydamir-unslop --target cursor --mode copy --dest "/Projects/my-app/.cursor/skills"
./vas status --target cursor --dest "/Projects/my-app/.cursor/skills"
./vas uninstall heydamir-unslop --target cursor --dest "/Projects/my-app/.cursor/skills"
```

`--mode link` cần giữ vị trí kho VAS. References, hình minh họa, examples và helper
đi kèm độc lập. Node/Playwright/browser và ffmpeg chỉ cần cho helper tùy chọn;
không tự cài, chạy, chụp website hay kết nối dịch vụ tạo ảnh. Xem
[hướng dẫn UI Unslop VI/EN](docs/unslop.md) cho mapping và quyền cần thiết.

### 5. Hướng Dẫn Từng AI Agent

- **Google Antigravity**: Quét tự động qua `.agents/skills/` hoặc `~/.gemini/antigravity/skills/`:
  ```bash
  ./vas install <skill_id> --target antigravity --mode link
  ./vas install <skill_id> --target global
  ```
- **OpenAI Codex / OpenCode**: Tận dụng tối đa khả năng suy luận code và thực thi terminal:
  ```bash
  ./vas install <skill_id> --target codex --mode link
  ```
  *Prompt mẫu trong Codex:*
  > *"Hãy đọc runbook trong skill `.codex/skills/<skill_id>/SKILL.md` và thực thi kịch bản kiểm tra bảo mật cho dự án này."*
- **Claude Code**: Đọc kỹ năng từ `.claude/skills/` hoặc toàn cục `~/.claude/skills/`:
  ```bash
  ./vas install <skill_id> --target claude --mode link
  ```
- **Cursor IDE**: Đọc qua `.cursor/skills/` hoặc tag `@.cursor/skills/<skill_id>` trong Composer:
  ```bash
  ./vas install <skill_id> --target cursor --mode link
  ```
- **Windsurf (Codeium)**: Nạp quy trình từ `.windsurf/skills/`:
  ```bash
  ./vas install <skill_id> --target windsurf --mode link
  ```
- **Cline / Roo Code**:
  ```bash
  ./vas install <skill_id> --target cline --mode link
  ```
- **GitHub Copilot CLI**:
  ```bash
  ./vas install <skill_id> --target copilot --mode link
  ```

---

### 6. Cẩm Nang Lệnh CLI (`./vas`)

```bash
# 1. Tìm kiếm kỹ năng theo từ khóa
./vas search kubernetes
./vas search "react performance" --limit 15

# 2. Liệt kê kỹ năng có bộ lọc
./vas list --category security
./vas list --tag python --limit 20

# 3. Xem chi tiết & Preview Runbook
./vas show ui-ux-pro-max
./vas show docker-expert

# 4. Cài đặt kỹ năng
./vas install ui-ux-pro-max 007 --target codex
./vas install --category devops --target claude
./vas install --category security --target all

# 5. Gỡ bỏ kỹ năng
./vas uninstall 007 --target codex
./vas uninstall docker-expert --target all

# 6. Kiểm tra kỹ năng đã cài
./vas status --target codex
./vas status --target antigravity

# 7. Khởi tạo workspace mới & đồng bộ index
./vas init
./vas sync
./vas guide
```

---

### 7. Cấu Trúc Chuẩn Của Một Skill

Mỗi kỹ năng trong thư mục `skills/<skill_name>/` tuân thủ chuẩn mở quốc tế:

```text
skills/<skill_name>/
├── SKILL.md          # [Bắt buộc] YAML Frontmatter + Runbook từng bước
├── scripts/          # [Tuỳ chọn] Script tự động hóa (Python, Bash, JS)
├── examples/         # [Tuỳ chọn] Cấu hình mẫu, input/output tham khảo
└── references/       # [Tuỳ chọn] Checklist chi tiết hoặc tài liệu kỹ thuật
```

```markdown
---
name: docker-expert
category: devops
tags: [docker, security, hardening, containers]
risk: safe
description: >-
  Use this skill when auditing Dockerfile or container configurations
  against security vulnerabilities, root execution, and secret leaks.
---

# Docker Security Hardening Runbook

## Instructions
1. Run static analysis: `scripts/analyze.sh`
2. Verify base image tags and non-root USER directive.
3. Review exposed ports and multi-stage build patterns.
```

---

### 8. Vòng Đời Kỹ Thuật Chuẩn Cấp Cao & Bộ 25 Kỹ Năng Addy Osmani

Mặc định, các AI Coding Agent thường chọn con đường tắt có điện trở thấp nhất: nhảy vào viết code ngay mà không có bản đặc tả (spec), bỏ qua việc viết test trước, không tự đánh giá ranh giới bảo mật hay hiệu năng, và dễ dàng tự ngụy biện rằng *"chắc là code chạy được rồi"*.

Lấy cảm hứng và đồng bộ trực tiếp từ bộ kỹ năng tiêu chuẩn **v0.6.13 của Addy Osmani** ([addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) & [skills.addy.ie](https://skills.addy.ie/)), VAS tích hợp toàn bộ **25 kỹ năng kỹ sư cấp cao** được ánh xạ 1:1 vào **6 giai đoạn của vòng đời phát triển phần mềm (SDLC)**:

```text
  ĐỊNH NGHĨA        KẾ HOẠCH        XÂY DỰNG        KIỂM THỬ        ĐÁNH GIÁ        TRIỂN KHAI
   DEFINE            PLAN            BUILD           VERIFY          REVIEW           SHIP
  ┌────────┐      ┌────────┐      ┌────────┐      ┌────────┐      ┌────────┐      ┌────────┐
  │  Idea  │ ───▶ │  Spec  │ ───▶ │  Code  │ ───▶ │  Test  │ ───▶ │   QA   │ ───▶ │   Go   │
  │ Refine │      │  PRD   │      │  Impl  │      │ Debug  │      │  Gate  │      │  Live  │
  └────────┘      └────────┘      └────────┘      └────────┘      └────────┘      └────────┘
   /spec           /plan           /build          /test          /review          /ship
```

#### 🛡️ 4 Nguyên Tắc Vàng Kỷ Luật Kỹ Thuật (Senior Engineering Discipline)
1. **Quy trình thay vì văn phong (Process, not prose)**: Kỹ năng không phải prompt chung chung hay lời khuyên trừu tượng. Mỗi skill là một cẩm nang hành động có các bước thực hiện rõ ràng, các trạm kiểm soát (checkpoints) và điều kiện nghiệm thu nghiêm ngặt.
2. **Chặn ngụy biện của AI (Anti-rationalization)**: Mọi kỹ năng đều trang bị bảng *Common Rationalizations* — vạch trần mọi cái cớ phổ biến mà AI thường đưa ra để trốn tránh công việc (như *"Tôi sẽ bổ sung test sau"*, *"Thay đổi này nhỏ nên không cần kiểm tra bảo mật"*,...) cùng lời bác bỏ đanh thép và danh sách dấu hiệu cảnh báo (*Red Flags*).
3. **Bằng chứng thực nghiệm (Verification is non-negotiable)**: Yêu cầu bằng chứng định lượng rõ ràng trước khi coi là hoàn thành (test chạy qua, log trace, DOM thực tế, heap snapshot). Tuyên bố *"Trông có vẻ đúng"* bị nghiêm cấm hoàn toàn.
4. **Tiết lộ lũy tiến (Progressive disclosure)**: File `SKILL.md` đóng vai trò là cửa ngõ tinh gọn (< 150 tokens metadata). Các tài liệu kỹ thuật chuyên sâu chỉ được nạp vào ngữ cảnh khi thật sự có tác vụ tương ứng.

#### 📋 Danh Sách 25 Kỹ Năng Addy Osmani Phân Theo Giai Đoạn

##### 🧭 Meta - Điều phối & Định tuyến Kỹ Năng
| Kỹ Năng | Năng Lực Trọng Tâm | Khi Nào Sử Dụng |
| :--- | :--- | :--- |
| [`using-agent-skills`](skills/using-agent-skills/SKILL.md) | Phân tích yêu cầu và định tuyến tác vụ đến đúng skill phù hợp nhất | Bắt đầu phiên làm việc hoặc xác định quy trình áp dụng |

##### 🎯 1. Define - Làm Rõ & Định Nghĩa Yêu Cầu
| Kỹ Năng | Năng Lực Trọng Tâm | Khi Nào Sử Dụng |
| :--- | :--- | :--- |
| [`interview-me`](skills/interview-me/SKILL.md) | Phỏng vấn người dùng từng câu một (one-question-at-a-time) bóc tách mong muốn thực sự đạt độ tin cậy ~95% | Yêu cầu còn mơ hồ, hoặc khi người dùng gõ lệnh "interview me" / "grill me" |
| [`idea-refine`](skills/idea-refine/SKILL.md) | Tư duy phân kỳ / hội tụ có cấu trúc biến ý tưởng sơ khai thành đề xuất kỹ thuật cụ thể | Có ý tưởng thô cần khám phá và xác định phạm vi |
| [`spec-driven-development`](skills/spec-driven-development/SKILL.md) | Viết PRD chi tiết gồm mục tiêu, lệnh, cấu trúc thư mục, code style, chiến lược test và ranh giới trước khi gõ code | Bắt đầu dự án mới, tính năng lớn hoặc thay đổi trọng yếu |
| [`constraint-driven-development`](skills/constraint-driven-development/SKILL.md) | Thiết lập hợp đồng chất lượng bằng văn bản `CONSTRAINTS.md`, ngăn agent tự ý hạ chuẩn hoặc bỏ qua bài test | Dự án chưa có chuẩn mực rõ ràng, hoặc agent sinh code ồ ạt |

##### 🗺️ 2. Plan - Lập Kế Hoạch & Chia Nhỏ Tác Vụ
| Kỹ Năng | Năng Lực Trọng Tâm | Khi Nào Sử Dụng |
| :--- | :--- | :--- |
| [`planning-and-task-breakdown`](skills/planning-and-task-breakdown/SKILL.md) | Tách PRD thành các tác vụ nhỏ nguyên tử, có tiêu chí nghiệm thu (acceptance criteria) và thứ tự phụ thuộc | Đã có đặc tả kỹ thuật và cần chia thành các đơn vị thực thi độc lập |

##### 🔨 3. Build - Xây Dựng & Lập Trình
| Kỹ Năng | Năng Lực Trọng Tâm | Khi Nào Sử Dụng |
| :--- | :--- | :--- |
| [`incremental-implementation`](skills/incremental-implementation/SKILL.md) | Triển khai theo từng lát cắt dọc mỏng: Triển khai → Kiểm thử → Xác thực → Commit. Hỗ trợ feature flag và rollback an toàn | Bất kỳ thay đổi nào tác động từ 2 file trở lên |
| [`test-driven-development`](skills/test-driven-development/SKILL.md) | Red-Green-Refactor, kim tự tháp kiểm thử 80/15/5, DAMP hơn DRY, nguyên tắc Beyonce, kiểm thử runtime trình duyệt | Xây dựng logic mới, sửa lỗi phần mềm hoặc thay đổi hành vi code |
| [`context-engineering`](skills/context-engineering/SKILL.md) | Nạp đúng thông tin vào đúng thời điểm: rules files, context packing, MCP tool scoping | Bắt đầu phiên làm việc, chuyển đổi tác vụ, hoặc khi chất lượng output giảm sút |
| [`source-driven-development`](skills/source-driven-development/SKILL.md) | Căn cứ mọi quyết định framework trên tài liệu chính thức (official docs), dẫn nguồn đầy đủ, cảnh báo pattern lỗi thời | Cần code chính xác tuyệt đối, tránh pattern bị deprecated |
| [`doubt-driven-development`](skills/doubt-driven-development/SKILL.md) | Đánh giá nghịch đảo trong ngữ cảnh tươi mới: YÊU CẦU → TRÍCH XUẤT → HOÀI NGHI → ĐỐI CHIẾU → DỪNG LẠI | Mã nguồn ở hệ thống trọng yếu (production, security), hoặc code lạ |
| [`frontend-ui-engineering`](skills/frontend-ui-engineering/SKILL.md) | Kiến trúc component, quản lý state, responsive design, tiêu chuẩn tiếp cận WCAG 2.1 AA | Xây dựng hoặc tinh chỉnh giao diện người dùng frontend |
| [`api-and-interface-design`](skills/api-and-interface-design/SKILL.md) | Thiết kế Contract-first, định luật Hyrum, One-Version Rule, ngữ nghĩa mã lỗi, kiểm tra ranh giới dữ liệu | Thiết kế API endpoint, ranh giới module hoặc public interface |

##### 🔍 4. Verify - Kiểm Chứng & Gỡ Lỗi
| Kỹ Năng | Năng Lực Trọng Tâm | Khi Nào Sử Dụng |
| :--- | :--- | :--- |
| [`browser-testing-with-devtools`](skills/browser-testing-with-devtools/SKILL.md) | Kết nối Chrome DevTools MCP thu thập dữ liệu runtime trực tiếp: DOM, console log, network traces, profiling hiệu năng | Xây dựng hoặc gỡ lỗi bất kỳ ứng dụng nào chạy trên trình duyệt |
| [`debugging-and-error-recovery`](skills/debugging-and-error-recovery/SKILL.md) | Quy trình 5 bước: Tái lập → Khoanh vùng → Tối giản → Khắc phục → Thiết lập phòng thủ. Nguyên tắc Stop-the-line | Bài test thất bại, build bị lỗi, hoặc phần mềm có hành vi bất thường |

##### ⚖️ 5. Review - Cổng Chất Lượng Trước Khi Merge
| Kỹ Năng | Năng Lực Trọng Tâm | Khi Nào Sử Dụng |
| :--- | :--- | :--- |
| [`code-review-and-quality`](skills/code-review-and-quality/SKILL.md) | Rà soát code 5 trục chất lượng, chia nhỏ thay đổi ~100 dòng, gắn nhãn mức độ nghiêm trọng (Nit/Optional/FYI) | Trước khi hợp nhất (merge) bất kỳ pull request nào |
| [`code-simplification`](skills/code-simplification/SKILL.md) | Áp dụng Chesterton's Fence & Rule of 500: loại bỏ phức tạp không cần thiết, tối ưu độ đọc hiểu mà giữ nguyên 100% logic | Code đã chạy đúng nhưng khó đọc hoặc bảo trì phức tạp |
| [`security-and-hardening`](skills/security-and-hardening/SKILL.md) | Phòng thủ OWASP Top 10, quản lý bí mật, kiểm toán rủi ro chuỗi cung ứng dependency, mô hình 3 ranh giới tin cậy | Tiếp nhận dữ liệu người dùng, xác thực, lưu trữ dữ liệu hoặc gọi API bên thứ ba |
| [`performance-optimization`](skills/performance-optimization/SKILL.md) | Phương pháp đo trước tối ưu sau: chỉ số Core Web Vitals (LCP, INP, CLS), profiling CPU/RAM, phân tích bundle size | Dự án có yêu cầu hiệu năng cao hoặc nghi ngờ có suy giảm tốc độ |

##### 🚀 6. Ship - Phát Hành Đáng Tin Cậy
| Kỹ Năng | Năng Lực Trọng Tâm | Khi Nào Sử Dụng |
| :--- | :--- | :--- |
| [`git-workflow-and-versioning`](skills/git-workflow-and-versioning/SKILL.md) | Trunk-based development, atomic commits, commit như một điểm lưu trạng thái (commit-as-save-point) | Luôn luôn áp dụng khi thực hiện bất kỳ thay đổi mã nguồn nào |
| [`ci-cd-and-automation`](skills/ci-cd-and-automation/SKILL.md) | Shift Left, nguyên tắc Faster is Safer, đường ống kiểm duyệt chất lượng, tính năng feature flag | Thiết lập hoặc tối ưu đường ống build và deploy tự động |
| [`deprecation-and-migration`](skills/deprecation-and-migration/SKILL.md) | Xem code như nợ kỹ thuật (code-as-liability), loại bỏ zombie code, quản lý chiến lược di chuyển người dùng | Dọn dẹp hệ thống cũ, di chuyển API hoặc gỡ bỏ tính năng |
| [`documentation-and-adrs`](skills/documentation-and-adrs/SKILL.md) | Lưu trữ quyết định kiến trúc (Architecture Decision Records - ADRs), tài liệu hóa lý do *Tại sao* đưa ra quyết định | Đưa ra quyết định kiến trúc, thay đổi API hoặc ra mắt tính năng mới |
| [`observability-and-instrumentation`](skills/observability-and-instrumentation/SKILL.md) | Structured logging, RED/USE metrics, OpenTelemetry tracing, cảnh báo dựa trên triệu chứng (symptom alerting) | Bổ sung hệ thống giám sát hoặc chuẩn bị đưa code lên production |
| [`shipping-and-launch`](skills/shipping-and-launch/SKILL.md) | Checklist trước giờ G, phát hành theo giai đoạn (staged rollouts), kịch bản rollback tức thì | Chuẩn bị triển khai hệ thống lên môi trường production |

```bash
# Cài đặt trọn bộ 25 kỹ năng Addy Osmani vào dự án của bạn:
./vas install test-driven-development debugging-and-error-recovery security-and-hardening performance-optimization code-review-and-quality --target all
```

---

### 9. Hệ Thống 7 Checklist Kỹ Thuật & Hội Đồng Thẩm Định Personas

#### 📚 Hệ Thống 7 Checklist Kỹ Thuật Chuẩn Doanh Nghiệp (`references/`)
Các kỹ năng trong VAS tự động liên kết và nạp theo nhu cầu 7 checklist kỹ thuật chuyên sâu tại thư mục `references/`:

| Tài Liệu Tham Khảo | Trọng Tâm Chuyên Sâu |
| :--- | :--- |
| [`references/definition-of-done.md`](references/definition-of-done.md) | Chuẩn mực hoàn thành (DoD) chung cho toàn bộ dự án mà mọi thay đổi code bắt buộc phải vượt qua |
| [`references/testing-patterns.md`](references/testing-patterns.md) | Cấu trúc test, quy ước đặt tên, chiến lược mock, mẫu test React/API/E2E và các anti-patterns cần tránh |
| [`references/security-checklist.md`](references/security-checklist.md) | Danh mục kiểm tra trước commit, xác thực, phân quyền, CSP headers, CORS, phòng ngừa OWASP Top 10 |
| [`references/performance-checklist.md`](references/performance-checklist.md) | Ngưỡng chỉ số Core Web Vitals, checklist tối ưu frontend/backend, các lệnh đo đạc định lượng |
| [`references/accessibility-checklist.md`](references/accessibility-checklist.md) | Điều hướng bàn phím, tương thích screen reader, độ tương phản thị giác, thuộc tính ARIA chuẩn WCAG 2.1 AA |
| [`references/observability-checklist.md`](references/observability-checklist.md) | Câu hỏi trực ban on-call, structured logging, RED/USE metrics, phân tán tracing và cảnh báo triệu chứng |
| [`references/orchestration-patterns.md`](references/orchestration-patterns.md) | Các mẫu điều phối đa agent được khuyến nghị, nguyên tắc "chuyên gia không tự gọi chuyên gia" tránh vòng lặp vô tận |

#### 👥 Hội Đồng Thẩm Định Chuyên Gia (Specialist Reviewer Personas)
Trước khi ra mắt sản phẩm (`/ship`), hệ thống hỗ trợ kích hoạt song song 4 vai trò chuyên gia độc lập để đánh giá toàn diện:
* 👨‍💻 **Code Reviewer (Staff Engineer)**: Đánh giá chất lượng 5 trục với tiêu chuẩn *"Liệu một Staff Engineer có chấp thuận PR này không?"*.
* 🧪 **Test Engineer (QA Specialist)**: Phân tích độ bao phủ kiểm thử, cấu trúc kim tự tháp test và nguyên tắc Prove-It.
* 🛡️ **Security Auditor (Security Specialist)**: Rà soát mô hình đe dọa STRIDE, ranh giới dữ liệu và phát hiện lỗ hổng OWASP.
* ⚡ **Web Performance Auditor (Performance Specialist)**: Kiểm toán chỉ số Core Web Vitals ở 2 chế độ Quick/Deep với nguyên tắc trung thực số liệu.

---

### 10. Bảng So Sánh Chi Tiết (How VAS Compares)

| Tiêu Chí Đánh Giá | Vie Agentic Skill (VAS) | Addy Osmani (`agent-skills`) | Superpowers (`obra`) | Matt Pocock Skills |
| :--- | :--- | :--- | :--- | :--- |
| **Quy mô Catalog** | **3,172+ Kỹ năng** (Toàn diện nhất thế giới) | 25 Kỹ năng cốt lõi | ~14 Kỹ năng | ~30 Kỹ năng |
| **Công cụ Quản trị** | **Native Python 3 CLI (`./vas`) — Zero-NPX** | `npx skills` / Plugin | Git Worktrees / Scripts | Claude Code / `npx skills` |
| **Phụ thuộc Mạng & NPX**| **100% Offline & Không cần Node/NPX** | Cần Node & npx khi cài | Cần clone & setup | Cần Node & npx khi cài |
| **Hỗ trợ Đa Agent** | **7+ AI Agents** (Antigravity, Codex, Claude, Cursor, Windsurf, Cline, Copilot) | Claude Code, Codex, Antigravity, Cursor, Copilot | Claude Code, Codex, Cursor | Claude Code ưu tiên |
| **Bao phủ Vòng đời SDLC**| **Toàn diện 6 pha**: Define ➔ Plan ➔ Build ➔ Verify ➔ Review ➔ Ship | Toàn diện 6 pha | Trọng tâm vòng lặp Build/Plan | Trọng tâm Grilling & TDD |
| **Chặn ngụy biện của AI** | **Có bảng Anti-Rationalization & Red Flags** | Có trong cả 25 kỹ năng | Có quy trình task reviewer | Không có bảng riêng |
| **Kiểm định Chất lượng** | **95 Bài test tự động (Python, Node, Cloudflare Security)** | Framework Evals 3 tầng | TDD cho tài liệu | Không tích hợp test trong repo |
| **Bảo toàn Ngữ cảnh** | **Strict Progressive Disclosure** (< 150 token metadata ban đầu) | Progressive Disclosure | Subagent Context Handoff | Split User/Model Invoked |

---

### 11. Danh Mục & Top 20 Siêu Kỹ Năng Nổi Bật

Kho lưu trữ gồm **3,172+ skills** chia theo **119 danh mục**. Xem chi tiết tại [CATALOG.md](CATALOG.md).

| # | Skill ID | Stars | Mô Tả Năng Lực | Lệnh Cài Đặt Nhanh |
| :-: | :--- | :---: | :--- | :--- |
| 1 | `ui-ux-pro-max` | ⭐ 139K | Tạo hệ thống Design System hoàn chỉnh (79 styles, 192 palettes, 74 font pairings) từ mô tả dự án | `./vas install ui-ux-pro-max --target all` |
| 2 | `impeccable` | ⭐ 86K | Chống giao diện "AI-slop" với 62 quy tắc kiểm tra tự động & 30+ chế độ tinh chỉnh thiết kế | `./vas install impeccable --target all` |
| 3 | `hyperframes` | ⭐ 71K | Viết HTML xuất video MP4 chuẩn cho AI Agent; đi kèm `hyperframes-figma`, `motion-doctrine`, `seam-craft` | `./vas install hyperframes --target all` |
| 4 | `remotion` | ⭐ 67K | Bộ 12 kỹ năng chính thức lập trình video bằng React (`remotion-create`, `remotion-render`, `remotion-captions`...) | `./vas install remotion-best-practices --target all` |
| 5 | `penpot` | ⭐ 62K | Kết nối Penpot (Figma mã nguồn mở) qua MCP Server kèm 14 kỹ năng AI Kit (`penpot-build-screen`, `penpot-audit-tokens`...) | `./vas install penpot penpot-router --target all` |
| 6 | `diagram-design` | ⭐ 60K | Xuất 45 loại sơ đồ kiến trúc thành 1 file HTML+SVG độc lập chuẩn màu sắc & font thương hiệu | `./vas install diagram-design --target all` |
| 7 | `blender-mcp` | ⭐ 32K | Kết nối Blender 3D với bất kỳ LLM nào để dựng hình, gán vật liệu, ánh sáng, rigging & animation bằng prompt | `./vas install blender-mcp --target all` |
| 8 | `img2threejs` | ⭐ 19K | Tái tạo đối tượng từ ảnh tham chiếu thành mô hình 3D Three.js thuần code, sẵn sàng diễn hoạt | `./vas install img2threejs --target all` |
| 9 | `video-shotcraft` | ⭐ 13K | Chụp trang thực tế, chọn từ 152 công thức góc máy (shot recipes) và kết xuất video quảng cáo bằng Remotion | `./vas install video-shotcraft --target all` |
| 10 | `lemo-opuscar` | ⭐ 6.5K | Đạo diễn & sản xuất phim ngắn bằng 59 phong cách điện ảnh viết hoàn toàn bằng code, không cần video model | `./vas install lemo-opuscar --target all` |
| 11 | `landing-page-design` | ⭐ Hot | Hệ thống thiết kế landing page chuyển đổi cao từ A-Z (intake, layout, copy, visual system, fluid island nav, fluid motion) | `./vas install landing-page-design --target all` |
| 12 | `day-trader-skill` | ⭐ Hot | Bộ 11 kỹ năng Day Trading chứng khoán Mỹ (quét chart, tin SEC 8-K, time entry/exit, mô phỏng Monte Carlo Time Machine, quản lý rủi ro & lệnh Alpaca) | `./vas install day-trader-skill --target all` |
| 13 | `ffmpeg-skill` | ⭐ Hot | Bộ công cụ 42 script FFmpeg tự động hoá chỉnh sửa video/audio (cắt ghép, 9:16 reframe, phụ đề karaoke, lọc khoảng lặng, ducking âm thanh, HDR sang SDR) | `./vas install ffmpeg-skill --target all` |
| 14 | `design-to-motion` | ⭐ Hot | Chuyển đổi thiết kế tĩnh (Figma frame, dashboard, UI card) thành HTML động, MP4 cho X và GIF 800×500 lặp mượt mà | `./vas install design-to-motion --target all` |
| 15 | `skills-manager` | ⭐ Hot | Điều phối, sao lưu và đồng bộ thư viện skills cho Claude Code, Antigravity, Cursor, Windsurf, Codex | `./vas install skills-manager --target all` |
| 16 | `react-spring` | ⭐ 28K | Động cơ animation vật lý đàn hồi (spring physics) tự nhiên cho React, Three.js & Canvas | `./vas install react-spring --target all` |
| 17 | `pixijs` | ⭐ 43K | Động cơ đồ họa 2D WebGL/WebGPU 60-120fps cho canvas tương tác, hạt và hiệu ứng thị giác | `./vas install pixijs --target all` |
| 18 | `rapier` | ⭐ 6.8K | Động cơ vật lý 2D & 3D WebAssembly viết bằng Rust siêu tốc cho Three.js & React Three Fiber | `./vas install rapier --target all` |
| 19 | `faster-whisper` | ⭐ 17K | Phiên âm giọng nói đa ngôn ngữ siêu tốc bằng CTranslate2, trích xuất phụ đề SRT/VTT theo từng từ | `./vas install faster-whisper --target all` |
| 20 | `obs-studio` | ⭐ 60K | Tự động hóa quay màn hình, chuyển cảnh và ghi video phần mềm chất lượng cao qua OBS WebSocket v5 | `./vas install obs-studio --target all` |

```text
📊 PHÂN BỔ CÁC DANH MỤC HÀNG ĐẦU:
├── 🛡️  Security              : 267 skills (OWASP, Pentest, Secret Audit, IAM, Hardening)
├── 💻  Development           : 230 skills (Refactoring, Clean Code, Design Patterns, OOP)
├── 📈  Business & Strategy   : 179 skills (Market Research, Financial Models, Growth)
├── ☁️  Cloud                 : 170 skills (AWS, GCP, Azure, Serverless, Cloud Architecture)
├── ⚙️  DevOps                : 169 skills (Docker, K8s, Terraform, CI/CD, Ansible, SRE)
├── 🤖  AI & Machine Learning : 135 skills (RAG, LLM Evaluation, Prompt Engineering)
├── 🎨  Design, 3D & Video    : 120+ skills (Impeccable, UI/UX Pro Max, HyperFrames, Remotion, Penpot, Blender)
├── 🌐  Web & Fullstack       : 113 skills (React, Next.js, Vue, Node.js, FastAPI, Spring)
├── 🧪  Testing & QA          :  51 skills (Playwright, Jest, Pytest, E2E, Chaos Testing)
└── ... và hơn 100+ danh mục chuyên biệt khác.
```

#### 🌟 10 Thẻ Demo Đồ Họa Cao Cấp: Trưng Bày Đầy Đủ Các Kỹ Năng

<p align="center">
  <img src="docs/assets/demos/10-skills-demo-showcase.svg" alt="10 Thẻ Demo Đồ Họa Cao Cấp - Vie Agentic Skill" width="100%" />
</p>

* 🚀 **landing-page-design**: Kiến trúc trang đích chuyển đổi cao & Fluid Nav
* 🎨 **ui-ux-pro-max**: Hệ thống Design System, 192 bảng màu & font pairing
* 🛡️ **impeccable**: Bộ công cụ chống AI-slop với 62 quy tắc định lượng
* 🧊 **blender-mcp & img2threejs**: Điều khiển Blender 3D & Three.js thuần code
* 🎬 **video-shotcraft, hyperframes, remotion**: Lập trình video trong React/HTML
* 📊 **diagram-design**: Sơ đồ kiến trúc cloud HTML+SVG
* 🛠️ **chrome-devtools**: Gỡ lỗi LCP, rò rỉ bộ nhớ & A11y
* ⚡ **bigquery-sql**: Tối ưu hóa chi phí & hiệu năng BigQuery
* 🔒 **firebase-firestore**: Kiểm toán bảo mật rules & data model
* 🧬 **alphafold-fetch**: Phân tích sinh học phân tử 3D & pLDDT

<details open>
<summary><b>1. Kiến Trúc Landing Page Chuyển Đổi Cao (<code>landing-page-design</code>)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/landing-page-design.svg" alt="Landing Page Architecture Demo" width="850" />
</p>

* **Bộ quy chuẩn kép**: Phân định rõ ràng giữa **Part A (Chiến lược & Bố cục)** và **Part B (Hệ thống thị giác nghiêm ngặt)**.
* **Nguyên tắc cốt lõi**: *One offer → One audience → One primary action*.
* **Kỹ thuật tiên tiến**: Fluid Island Navigation (floating pill bo góc), công thức lồng bo góc `r_in = r_out - padding`, vật lý chuyển động mượt mà `cubic-bezier(0.32, 0.72, 0, 1)`, cấm gradient nền lòe loẹt.
* **Cài đặt**: `./vas install landing-page-design --target all`
</details>

<details open>
<summary><b>2. Sinh Design System & Bảng Màu Toàn Diện (<code>ui-ux-pro-max</code> — ⭐ 139K)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/ui-ux-pro-max.svg" alt="UI UX Pro Max Demo" width="850" />
</p>

* **Năng lực**: Tự động sinh trọn bộ Design System từ project brief ngắn gọn (79 phong cách nghệ thuật, 192 bảng màu hòa hợp, 74 phối cặp font typography chuẩn quốc tế).
* **Tiêu chuẩn**: Đáp ứng tỷ lệ tương phản tiếp cận WCAG 2.1 (AAA/AA) và tích hợp script tra cứu style tức thì qua CLI.
* **Cài đặt**: `./vas install ui-ux-pro-max --target all`
</details>

<details open>
<summary><b>3. Bộ Công Cụ Chống Giao Diện "AI-Slop" (<code>impeccable</code> — ⭐ 86K)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/impeccable.svg" alt="Impeccable Anti AI-Slop Demo" width="850" />
</p>

* **Năng lực**: Loại bỏ hoàn toàn giao diện "AI-slop" (gradient tím sến, card nhồi nhét, spacing lộn xộn, template sáo rỗng) với 62 quy tắc kiểm tra định lượng.
* **Chế độ Senior**: Cung cấp hơn 30 chế độ tinh chỉnh (`/delight`, `/polish`, `/audit`, `/critique`) nâng tầm thẩm mỹ frontend lên chuẩn Out-of-Distribution Craft.
* **Cài đặt**: `./vas install impeccable --target all`
</details>

<details open>
<summary><b>4. Điều Khiển Blender 3D & Three.js Thuần Code (<code>blender-mcp</code> & <code>img2threejs</code>)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/blender-and-3d.svg" alt="Blender and Three.js 3D Demo" width="850" />
</p>

* **Blender MCP**: Kết nối trực tiếp Blender 3D qua Model Context Protocol. Tạo mesh, gán vật liệu PBR, điều chỉnh ánh sáng, rigging và render bằng câu lệnh tự nhiên.
* **img2threejs**: Tái tạo vật thể từ ảnh tham chiếu 2D thành code Three.js tối ưu, nhẹ tênh và sẵn sàng animation mà không cần file 3D nặng nề bên ngoài.
* **Cài đặt**: `./vas install blender-mcp img2threejs --target all`
</details>

<details open>
<summary><b>5. Lập Trình Video & Chuyển Động Bằng Code (<code>hyperframes</code>, <code>remotion</code>, <code>video-shotcraft</code>, <code>lemo-opuscar</code>)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/video-and-motion.svg" alt="Video and Motion Demo" width="850" />
</p>

* **HyperFrames**: Lập trình video MP4 từ HTML/CSS/SVG thuần túy dành cho AI Agent.
* **Remotion Suite**: Bộ 12 skills chính thức viết video bằng React components.
* **Video Shotcraft & Lemo Opuscar**: 152 công thức góc máy tự động và 59 phong cách điện ảnh viết hoàn toàn bằng code, không phụ thuộc AI video model đắt đỏ.
* **Cài đặt**: `./vas install hyperframes video-shotcraft remotion --target all`
</details>

<details open>
<summary><b>6. Sơ Đồ Kiến Trúc Đám Mây & Hệ Thống Chuẩn Xuất Bản (<code>diagram-design</code> — ⭐ 60K)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/diagram-design.svg" alt="Diagram Design Demo" width="850" />
</p>

* **Năng lực**: Xuất hơn 45 loại sơ đồ kiến trúc phức tạp (AWS/GCP Cloud Architecture, K8s topology, Sequence Diagram) thành một file HTML+SVG duy nhất.
* **Chuẩn thương hiệu**: Tự động áp dụng bảng màu, phông chữ và tỷ lệ bố cục chuẩn doanh nghiệp.
* **Cài đặt**: `./vas install diagram-design --target all`
</details>

<details open>
<summary><b>7. Gỡ Lỗi Trình Duyệt Tự Động & Kiểm Toán A11y (<code>chrome-devtools</code> — Google Official)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/chrome-devtools.svg" alt="Chrome DevTools MCP Automation Demo" width="850" />
</p>

* **Năng lực**: Điều khiển trình duyệt trực tiếp qua giao thức Chrome DevTools MCP, gỡ lỗi DOM theo thời gian thực, chẩn đoán rò rỉ bộ nhớ (Heap Snapshot), đo lường chỉ số Core Web Vitals (LCP) và kiểm toán khả năng tiếp cận WCAG A11y.
* **Tự động hóa**: Hỗ trợ ghi lại network trace, chẩn đoán mã lỗi 401/403/500 và tự sửa lỗi giao diện không cần thao tác tay.
* **Cài đặt**: `./vas install chrome-devtools --target all`
</details>

<details open>
<summary><b>8. Tối Ưu Hóa Chi Phí & Hiệu Năng BigQuery SQL (<code>bigquery-sql</code> — Data Agent Kit)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/bigquery-sql.svg" alt="BigQuery SQL Performance Demo" width="850" />
</p>

* **Năng lực**: Tự động kiểm tra cú pháp và tối ưu hóa truy vấn BigQuery SQL, áp dụng Partitioning theo ngày/tháng, gom cụm Clustering dữ liệu, giảm thiểu tới 84% dung lượng quét (bytes billed) và tăng tốc độ xử lý slot-ms.
* **Hệ sinh thái**: Tích hợp chặt chẽ với dbt-bigquery, Dataform ELT và Dataproc Serverless Spark.
* **Cài đặt**: `./vas install bigquery-sql --target all`
</details>

<details open>
<summary><b>9. Kiểm Toán Bảo Mật Rules & Data Model NoSQL (<code>firebase-firestore</code> — Firebase Suite)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/firebase-firestore.svg" alt="Firebase Firestore Security Demo" width="850" />
</p>

* **Năng lực**: Đánh giá an ninh Red-Team cho `firestore.rules`, triệt tiêu lỗ hổng leo thang đặc quyền (Privilege Escalation), đảm bảo kiểm tra kiểu dữ liệu tĩnh (type safety) và phòng chống cạn kiệt tài nguyên (resource exhaustion).
* **Kiến trúc**: Thiết kế cấu trúc NoSQL đa đối tượng, thiết lập chỉ mục hỗn hợp (composite indexes) và tích hợp an toàn với App Hosting SSR (Next.js/Angular).
* **Cài đặt**: `./vas install firebase-firestore --target all`
</details>

<details open>
<summary><b>10. Phân Tích Cấu Trúc Sinh Học Phân Tử 3D & pLDDT (<code>alphafold-fetch</code> — Science Plugin)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/alphafold-science.svg" alt="AlphaFold Science 3D Suite Demo" width="850" />
</p>

* **Năng lực**: Tự động tra cứu và phân tích cấu trúc 3D protein từ AlphaFold Database qua mã UniProt ID, đánh giá độ tin cậy cấu trúc pLDDT, xác định ranh giới domain cứng và vùng rối vô định hình (disordered regions).
* **Sidecar 3D tương tác**: Kết nối trực tiếp trình hiển thị Mol* 3D Viewer và bộ công cụ tính toán sinh học (ChEMBL, ClinVar, BLAST).
* **Cài đặt**: `./vas install alphafold-fetch --target all`
</details>

---

#### Bộ skill Matt Pocock

Bổ sung **16 skill ổn định** từ [mattpocock/skills](https://github.com/mattpocock/skills)
tại commit `5beb35b040e3de97e54fa9e386d7e42d15c295c2`: review code, triển khai spec,
viết PR, nghiên cứu, retrospective, chia ticket, lập kế hoạch, wizard và công cụ workflow.
Giữ nguyên **19 skill đã tùy biến**; không nhập **7 skill thử nghiệm** trong `in-progress/`.
Toàn bộ 31 skill ổn định hiện tại của upstream đều đã có mặt trong kho; 4 bản legacy vẫn được giữ.

```bash
./vas search mattpocock/skills --limit 40
./vas install code-review to-spec to-tickets writing-for-agents --target antigravity
```

Mỗi skill mới giữ nguyên giấy phép MIT, tác giả Matt Pocock và các file hỗ trợ.
Một số workflow cần công cụ riêng của dự án đích (ví dụ Claude Code, Bash/jq hoặc Node.js);
chúng không phải phụ thuộc của CLI VAS. Xem [nguồn và bản ghi nhập](data/mattpocock-skills.json).

---

#### 🛡️ Cloudflare Security Audit (`cloudflare-security-audit`)

Tích hợp trực tiếp từ repo mã nguồn mở chính thức của Cloudflare: [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill).

Đây là bộ khung kiểm toán an ninh mã nguồn cấp doanh nghiệp giúp biến AI Coding Agent thành một kiểm toán viên an ninh bảo vệ trust boundary thực thụ:
* **Quy trình 6 giai đoạn (Six-Phase Pipeline)**: Reconnaissance (thăm dò kiến trúc), Coverage-Led Hunting (rà soát định hướng), Candidate Validation (phản biện độc lập), Structured Output (xuất JSON Schema), Record Verification (đối soát chéo), Target-Neutral Report (báo cáo hoàn chỉnh).
* **12 Chuyên đề an ninh thực chiến**: AI/LLM Prompt Injection & Tool Poisoning, Memory Safety (Rust/C/Go), Cloud & Deployment SSRF, ReDoS, Web Protocols & Auth, Supply Chain, Data Isolation.
* **Tích hợp sẵn Validator không phụ thuộc thư viện ngoài**: Kèm 2 script kiểm định `validate-coverage-ledger.cjs` và `validate-findings.cjs` đạt 65/65 unit test pass.

```bash
# Tra cứu thông tin hoặc dùng alias ngắn gọn:
./vas show cloudflare-security-audit
./vas show security-audit-skill

# Cài đặt cho AI Agent yêu thích:
./vas install cloudflare-security-audit --target antigravity --mode link
./vas install cloudflare-security-audit --target all
```

---

<a id="blender-studio"></a>
#### 🧊 Blender Studio — Bộ 94 Kỹ Năng 3D Animation & Pipeline

Đã nhập trọn bộ [arjun988/blender-skills](https://github.com/arjun988/blender-skills) tại commit `8f778d2405a214b508d4c7d80742be8e43acdd52` với namespace `blender-skills/<name>`, không ghi đè các skill hiện có. Giữ nguyên tài liệu tham chiếu và giấy phép MIT trong từng skill; chỉ nhập một bản canonical, không nhân đôi bản Cursor. Xem [ghi chú nhập bộ Blender](skills/blender-skills/README.md) và [bản ghi mã băm sha256](data/blender-import.json).

```bash
# Liệt kê tất cả 94 kỹ năng trong danh mục blender:
./vas list --category blender

# Cài đặt các kỹ năng điều phối & dựng hình Blender:
./vas install blender-skills/blender-director blender-skills/blender-modeler --target claude --global
./vas install blender-skills/geometry-nodes blender-skills/texture-workflow --target antigravity
```

*Lưu ý:* Phần mềm Blender và kết nối Blender MCP là yêu cầu riêng độc lập. VAS không tự cài Blender, khởi chạy server hay cấp quyền MCP. Chế độ link (`--mode link`) cần giữ nguyên kho nguồn; dùng `--mode copy` nếu muốn sao chép skill cùng tài liệu tham chiếu sang dự án đích.

---

#### 🎬 Siêu Bộ 20 Kỹ Năng Creative Coding, Motion Design & Lập Trình Video

VAS tích hợp trọn bộ 20 công cụ tiêu chuẩn hàng đầu cho AI Agent trong lĩnh vực đồ họa, animation, mô phỏng vật lý 2D/3D, audio và kết xuất video thuần code:

| STT | Công Cụ | Kỹ Năng / Alias | Lĩnh Vực Chuyên Sâu | Lệnh Cài Đặt Nhanh |
| :-: | :--- | :--- | :--- | :--- |
| 01 | **Remotion** | `remotion` | React Video Engine lập trình video bằng React | `./vas install remotion --target all` |
| 02 | **HyperFrames** | `hyperframes` | HTML-to-video render pipeline cho AI Agent | `./vas install hyperframes --target all` |
| 03 | **Anime.js** | `animejs` / `anime.js` | Điều phối timeline, SVG morphing, CSS animation | `./vas install animejs --target all` |
| 04 | **React Spring** | `react-spring` | Animation dựa trên vật lý đàn hồi cho React & 3D | `./vas install react-spring --target all` |
| 05 | **PixiJS** | `pixijs` / `pixi` | Engine đồ họa 2D WebGL/WebGPU 60-120fps | `./vas install pixijs --target all` |
| 06 | **p5.js** | `p5js` / `p5` | Nghệ thuật sinh học (generative art) & creative coding | `./vas install p5js --target all` |
| 07 | **Paper.js** | `paperjs` / `paper` | Xử lý vector, đường cong Bézier & phép toán boolean SVG | `./vas install paperjs --target all` |
| 08 | **Matter.js** | `matterjs` / `matter` | Mô phỏng vật lý vật thể rắn 2D (rigid body dynamics) | `./vas install matterjs --target all` |
| 09 | **Three.js** | `threejs` / `three` | Dựng cảnh 3D không gian, vật liệu & ánh sáng WebGL | `./vas install threejs --target all` |
| 10 | **Rapier** | `rapier` / `rapier3d` | Động cơ vật lý 2D/3D bằng Rust & WebAssembly siêu tốc | `./vas install rapier --target all` |
| 11 | **OGL** | `ogl` / `ogl-webgl` | Thư viện WebGL tối giản (~10KB) viết custom GLSL shader | `./vas install ogl --target all` |
| 12 | **tsParticles** | `tsparticles` | Hiệu ứng hạt tương tác, mạng lưới kết nối & confetti | `./vas install tsparticles --target all` |
| 13 | **glTF Transform**| `gltf-transform` / `gltf` | Tối ưu hóa 3D glTF/GLB, nén DRACO, Meshopt & KTX2 | `./vas install gltf-transform --target all` |
| 14 | **GL Transitions**| `gl-transitions` | 50+ hiệu ứng chuyển cảnh GLSL shader cho canvas/video | `./vas install gl-transitions --target all` |
| 15 | **OBS Studio** | `obs-studio` / `obs` | Tự động hóa quay màn hình & stream qua OBS WebSocket v5 | `./vas install obs-studio --target all` |
| 16 | **Chatterbox** | `chatterbox` | Lồng tiếng AI & nhân bản giọng nói nơ-ron (Resemble AI) | `./vas install chatterbox --target all` |
| 17 | **Tone.js** | `tonejs` / `tone` | Tổng hợp âm thanh, synthesizer, SFX & Web Audio API | `./vas install tonejs --target all` |
| 18 | **faster-whisper**| `faster-whisper` / `whisper` | Phiên âm giọng nói siêu tốc & tự động tạo phụ đề SRT/VTT | `./vas install faster-whisper --target all` |
| 19 | **OpenCut** | `opencut` / `video-editor` | Dựng video dòng thời gian (timeline editing) bằng code | `./vas install opencut --target all` |
| 20 | **FFmpeg** | `ffmpeg` / `ffmpeg-skill` | 42 kịch bản encode, cắt ghép, xử lý LUFS & xuất nền tảng | `./vas install ffmpeg --target all` |

---

#### 📈 Bộ Kỹ Năng Giao Dịch Chứng Khoán Tự Động (`day-trader-skill` Suite)

Bộ 11 kỹ năng chuyên sâu hỗ trợ AI Agent phân tích, quét thị trường và lập kế hoạch giao dịch chứng khoán Mỹ (US Equities):
* **Hệ thống 11 modules chuyên biệt**:
  - `trader-scanner`: Quét cổ phiếu biến động, momentum & khối lượng bất thường.
  - `trader-news`: Phân tích tin tức thời gian thực & tâm lý thị trường (sentiment analysis).
  - `trader-entry` & `trader-exit`: Xác định điểm vào/ra lệnh kỹ thuật theo tỷ lệ R:R.
  - `trader-risk` & `trader-budget`: Quản trị vốn, tỷ lệ đòn bẩy và ngưỡng cắt lỗ an toàn.
  - `trader-broker`: Kết nối API môi giới (Alpaca, Interactive Brokers) đặt lệnh tự động.
  - `trader-timemachine`: Backtest chiến lược giao dịch trên dữ liệu nến lịch sử.
  - `trader-alerts`: Thiết lập cảnh báo biến động đa kênh (Telegram, Discord, Webhook).
  - `trader-analyst`: Phân tích cơ bản báo cáo tài chính & chỉ số định giá.
  - `trader-pelosi`: Theo dõi giao dịch cổ phiếu công khai của các nhà lập pháp Quốc hội Mỹ.

```bash
# Cài đặt trọn bộ giao dịch cho AI Agent:
./vas install day-trader-skill --target all

# Hoặc cài đặt từng module lẻ:
./vas install trader-scanner trader-risk trader-entry --target antigravity
```

---

#### 🗂️ Quản Lý & Điều Phối Thư Viện Kỹ Năng Đa Agent (`skills-manager`)

Kỹ năng điều phối và đồng bộ hóa thư viện skills trên mọi môi trường lập trình của AI Agent:
* **Hỗ trợ toàn diện**: Quản lý skills đồng thời cho Claude Code, Google Antigravity, Cursor, Windsurf, Codex, Cline và Copilot CLI.
* **Tính năng chính**: Tự động phát hiện cấu hình cài đặt, sao lưu thư viện, kiểm tra tính toàn vẹn (integrity audit) và kích hoạt chế độ đồng bộ symlink không trùng lặp tài nguyên.

```bash
./vas show skills-manager
./vas install skills-manager --target all
```

---

#### 🎨 Chuyển Đổi Thiết Kế Thành Motion Động (`design-to-motion`)

Kỹ năng 3 giai đoạn giúp AI coding agent chuyển đổi thiết kế tĩnh (Figma frame, UI card, dashboard, app screen...) thành trang HTML động pixel-perfect có animation lặp mượt mà:
* **Part A (Tái tạo chính xác)**: Dựng lại layout 1:1 từ bản thiết kế hoặc Figma screenshot.
* **Part B (Hệ thống chuyển động)**: Thiết lập timeline chuyển động tự nhiên từ trạng thái rỗng (empty state) đến khi dữ liệu hiển thị.
* **Part C (Xuất bản đa định dạng)**: Hỗ trợ render video MP4 cho X/Twitter, GIF chất lượng cao cho website hoặc ảnh động kích thước chuẩn 800×500.

```bash
./vas show design-to-motion
./vas install design-to-motion --target all
```

---

#### 🎞️ Bộ Công Cụ FFmpeg Toàn Năng Cho Video & Audio (`ffmpeg-skill`)

Bộ công cụ 42 kịch bản tự động hóa xử lý âm thanh và video bằng Python thuần (không cần thư viện bên ngoài):
* **Xử lý video chuyên nghiệp**: Cắt ghép lossless không encode lại, reframe sang tỉ lệ dọc 9:16 (TikTok/Reels), phát hiện cảnh chuyển đổi và tạo contact sheet.
* **Xử lý âm thanh & Phụ đề**: Chuẩn hóa âm lượng EBU R128 (-14 LUFS), tự động ducking nhạc nền khi có giọng nói, trích xuất phụ đề karaoke chuẩn xác từng từ.

```bash
./vas show ffmpeg-skill
./vas install ffmpeg-skill --target all
```

### 12. Câu Hỏi Thường Gặp (FAQ)

**Q: Mục đích ra đời của Vie Agentic Skill (VAS) là gì?**  
Dự án do tác giả Huy Tran sáng lập nhằm giải quyết sự phân mảnh các kỹ năng agent trên toàn thế giới. Thay vì người dùng phải tìm kiếm rời rạc, đối mặt với lỗi cài đặt hoặc phụ thuộc `npx` qua mạng, VAS tổng hợp, tinh tuyển và chuẩn hóa toàn bộ các kỹ năng AI hàng đầu thế giới (từ Google, Addy Osmani, Cloudflare, Matt Pocock, Blender Studio...) vào một kho lưu trữ duy nhất theo chuẩn mở [agentskills.io](https://agentskills.io/), hỗ trợ cài đặt tức thì vào mọi AI coding agent chỉ bằng một câu lệnh Python thuần 100% offline.

**Q: Bộ 25 kỹ năng kỹ sư cấp cao của Addy Osmani mang lại giá trị gì cho AI Agent?**  
AI coding agent mặc định thường chọn con đường tắt có điện trở thấp nhất: bỏ qua PRD/spec, nhảy vào viết code ngay mà không viết test, bỏ qua rà soát bảo mật OWASP, hoặc ngụy biện rằng "chắc là code chạy được". Bộ 25 kỹ năng cung cấp quy trình chặt chẽ (SDLC), trạm kiểm soát bắt buộc (checkpoints), bảng phản bác ngụy biện (Anti-Rationalization) và yêu cầu cung cấp bằng chứng định lượng (test pass, log trace, DOM thực tế) trước khi chuyển bước.

**Q: Tôi dùng OpenAI Codex thì có cần cấu hình gì thêm không?**  
*Không cần.* Bạn chỉ cần chạy `./vas install <skill_id> --target codex`. Codex có khả năng đọc Markdown và gọi các script thực thi trực tiếp trong môi trường của bạn.

**Q: Tôi có cần cài đặt Node.js hay npm/npx không?**  
*Hoàn toàn không.* Dự án được xây dựng theo tiêu chuẩn **Zero-NPX**. Tất cả lệnh tìm kiếm, liệt kê và cài đặt đều chạy bằng Python 3 tích hợp sẵn trên máy qua `./vas`.

**Q: Làm sao để cài đặt một kỹ năng cho TẤT CẢ các AI tools tôi đang dùng?**  
Chỉ cần chạy `./vas install <skill_id> --target all`. Lệnh này sẽ tạo symlink đồng bộ vào tất cả các thư mục `.agents/skills`, `.claude/skills`, `.cursor/skills`, `.windsurf/skills`, `.codex/skills`, `.cline/skills`, `.github/skills`.

**Q: Cơ chế Progressive Disclosure tiết kiệm token như thế nào?**  
Dù bạn cài hàng trăm kỹ năng, AI agent chỉ quét phần tóm tắt ngắn (YAML frontmatter). Chỉ khi câu hỏi của bạn khớp với chuyên môn của skill, Agent mới nạp toàn bộ nội dung chi tiết vào ngữ cảnh.

---

### 13. Tác Giả & Giấy Phép

* **Tác giả & Sáng lập**: **Huy Tran** ([@huytran1120](https://github.com/huytran1120))
* **Email**: `66549585+huytran1120@users.noreply.github.com`
* **Repository**: [https://github.com/huytran1120/vie-agentic-skills](https://github.com/huytran1120/vie-agentic-skills)
* **Website Catalog**: [GitHub Pages](https://huytran1120.github.io/vie-agentic-skills/) · [Local preview](http://127.0.0.1:8765/docs/)
* **Mục tiêu dự án**: Tổng hợp, chuẩn hóa và cung cấp kho kỹ năng AI agent toàn diện nhất thế giới cho cộng đồng lập trình viên.
* **Giấy phép**: [MIT License](LICENSE) — Áp dụng cho mã nguồn công cụ dự án; các kỹ năng được tổng hợp giữ nguyên giấy phép và quyền tác giả ban đầu.

---

<p align="center">
  <b>Được sáng lập, tổng hợp & phát triển bởi Huy Tran 🇻🇳 🌏</b><br>
  <i>Mọi đóng góp, đề xuất tổng hợp kỹ năng mới hoặc báo lỗi vui lòng gửi qua <a href="https://github.com/huytran1120/vie-agentic-skills/issues">GitHub Issues</a>.</i>
</p>

---

<a id="english"></a>
## 🇬🇧 English

### 📌 Table of Contents
- [1. Overview](#1-overview)
- [2. Multi-Agent Compatibility](#2-multi-agent-compatibility)
- [3. Why Vie Agentic Skill?](#3-why-vie-agentic-skill)
- [4. Quickstart](#4-quickstart)
- [5. Agent-Specific Setup Guides](#5-agent-specific-setup-guides)
- [6. CLI Reference (`./vas`)](#6-cli-reference-vas)
- [7. Open Skill Specification (`SKILL.md`)](#7-open-skill-specification-skillmd)
- [8. Senior Engineering SDLC & 25 Addy Osmani Skills](#8-senior-engineering-sdlc--25-addy-osmani-skills)
- [9. 7 Technical Checklists & Reviewer Personas](#9-7-technical-checklists--reviewer-personas)
- [10. Honest Comparison Matrix (How VAS Compares)](#10-honest-comparison-matrix-how-vas-compares)
- [11. Featured & Viral Skills Showcase (Top 20)](#11-featured--viral-skills-showcase-top-20)
- [12. Frequently Asked Questions (FAQ)](#12-frequently-asked-questions-faq)
- [13. Author & License](#13-author--license)

---

### 1. Overview

**Vie Agentic Skill (VAS)** is an open-source project authored, curated, and maintained by **Huy Tran** ([@huytran1120](https://github.com/huytran1120)) with the mission to **aggregate, curate, and standardize the world's best agentic skills** for modern AI coding assistants.

Rather than leaving skills fragmented across different tools, isolated plugins, or proprietary repositories, VAS consolidates **3,172+ production-grade playbooks (`SKILL.md`)** across **119 specialized categories** into a unified ecosystem adhering to the **Open Agent Skills specification ([agentskills.io](https://agentskills.io/))**. It brings together the finest engineering runbooks from premier open-source contributors and industry organizations worldwide—including Addy Osmani, Cloudflare, Matt Pocock, Blender Studio, Google Devs, and Open Agent Skills.

Instead of treating your AI coding assistant as an entry-level intern that generates shallow answers, VAS equips agents with Senior-grade playbooks: deep diagnostic checklists, security hardening rules, performance formulas, and deterministic execution scripts.

---

### 2. Multi-Agent Compatibility

VAS installs skills into native target directories across all leading AI coding assistants with a single command:

| AI Agent / IDE | Target Directory | Install Command |
| :--- | :--- | :--- |
| **Google Antigravity** | `.agents/skills/` or `~/.gemini/antigravity/skills/` | `./vas install <skill> --target antigravity` |
| **OpenAI Codex / OpenCode** | `.codex/skills/` or `.agents/skills/` | `./vas install <skill> --target codex` |
| **Claude Code** | `.claude/skills/` or `~/.claude/skills/` | `./vas install <skill> --target claude` |
| **Cursor IDE** | `.cursor/skills/` | `./vas install <skill> --target cursor` |
| **Windsurf (Codeium)** | `.windsurf/skills/` | `./vas install <skill> --target windsurf` |
| **Cline / Roo Code** | `.cline/skills/` | `./vas install <skill> --target cline` |
| **GitHub Copilot CLI** | `.github/skills/` | `./vas install <skill> --target copilot` |
| **ALL AGENTS AT ONCE** | Installs into all target folders above | `./vas install <skill> --target all` |

---

### 3. Why Vie Agentic Skill?

| Feature | Legacy NPX Solutions | Vie Agentic Skill (VAS) |
| :--- | :--- | :--- |
| **Runtime Requirements** | Requires Node.js & remote `npx` execution | **Native Python 3 CLI (`./vas`)** with standard library only |
| **Network Reliance** | Requires internet connectivity on every run | **100% Offline & Zero Dependencies** |
| **CLI Latency** | 3s - 15s per invocation | **< 0.05 seconds** (instantaneous) |
| **Agent Ecosystem** | Limited or manual copy-pasting | **Native support for 7+ AI Coding Agents** |
| **Installation Engine** | Manual file copying | **Symlink (`--mode link`) & Atomic Copy** with automatic rollbacks |
| **Context Window Preservation** | Prone to context bloat | **Strict Progressive Disclosure** (saving up to 99% of prompt tokens) |

---

### 4. Quickstart

#### Option 1: Copy Agent Prompt — no repository clone

Open the [skill library](https://huytran1120.github.io/vie-agentic-skills/?lang=en),
find a skill, choose your agent, and click **Copy prompt** in the results or
**Copy Agent Prompt** in its details. Paste it into your agent chat in the open
project. The prompt includes the correct ID, agent folder and official manifest.

Your agent downloads the **complete skill**, including `SKILL.md`, scripts,
templates, references, licenses and assets, checking SHA-256 at one VAS snapshot.
Matching installations are skipped; differing files or another skill using the
same folder require confirmation, never silent replacement. This route does not
require cloning VAS, running `./vas` or installing Python.

Example for Cursor and a YouTube skill:

```text
Install "youtube-agent-skill/yt-script" into this project for Cursor at
".cursor/skills/yt-script/". Read the official manifest:
https://huytran1120.github.io/vie-agentic-skills/install-manifests/youtube-agent-skill/yt-script.json
Check the skill identity and available = true; download every listed file,
preserve its tree and verify SHA-256 before completing. Do not clone VAS, follow
symlinks or write outside this project. Skip matching installations; ask before
overwriting differing contents or an invalid receipt. Record receipt in
.vas-manifest.json in the agent skills folder, preserving other entries.
Read SKILL.md and report its path and missing prerequisites. Do not run scripts,
install dependencies or connect services automatically; stop on download/hash errors.
```

The agent needs network and file access. Individual runbooks may need additional
runtimes/MCP or an application skill reload. The website only copies instructions;
it does not install software. Global/link/absolute-path settings apply only to the
CLI below. Selecting `all` in chat installation means the seven agent folders in
the **current project**, not user-wide installation.

#### Option 2: CLI — offline, linked/copied and multi-skill management

```bash
# Step 1: Clone or enter the project directory
git clone https://github.com/huytran1120/vie-agentic-skills.git
cd vie-agentic-skills
chmod +x vas vas.py

# Step 2: Search for skills
./vas search docker-expert
./vas list --category security --limit 10
./vas categories

# Step 3: Install for your AI coding assistant
./vas install ui-ux-pro-max --target codex
./vas install docker-expert --target antigravity
./vas install fastapi-pro --target claude
./vas install react-component-performance --target cursor

# Install for ALL agents in your repository at once:
./vas install ui-ux-pro-max 007 pdf --target all
```
*(Smart alias system included: invoking `docker-security`, `fastapi-best-practices`, `react-performance`, or `nextjs-perf` will automatically map to the canonical skill).*

**Choose the destination explicitly:** without `--dest` or `--global`, the CLI
installs into the agent directory under the current working directory. It does
not locate another project automatically. On the website, open a skill and select
an agent and either a project or user-wide installation. Install, status and
uninstall commands share the same destination. For a separate project, run:

```bash
./vas install code-review --target codex --mode link --dest "/Projects/my-app/.codex/skills"
./vas status --target codex --dest "/Projects/my-app/.codex/skills"
./vas uninstall code-review --target codex --dest "/Projects/my-app/.codex/skills"
```

Replace `/Projects/my-app` with your actual project path. Use `--global` instead
of `--dest` for one agent across your user account; do not combine it with
`--target all`. Link mode requires keeping the VAS checkout in place; copy mode
creates an independent snapshot that must be reinstalled to update. Open your
project in the agent, reload its skill list if necessary, and ask it to read the
installed runbook before applying it. The website provides matching status and
uninstall commands and a sample prompt, including for namespaced Blender skills.

---

#### Hallmark: frontend design on request

[Open Hallmark in the catalog](https://huytran1120.github.io/vie-agentic-skills/?lang=en&skill=hallmark),
choose an agent and use **Copy Agent Prompt** to install all 182 files without
cloning. Hallmark is **one skill**, with 50 themes, references, previews, scripts
and its MIT notice; installation never redesigns a page or runs helpers.

From your VAS checkout, replace `/Projects/my-app` with your actual project:

```bash
./vas install hallmark --target cursor --mode copy --dest "/Projects/my-app/.cursor/skills"
./vas status --target cursor --dest "/Projects/my-app/.cursor/skills"
./vas uninstall hallmark --target cursor --dest "/Projects/my-app/.cursor/skills"
```

Use `--mode link` for symlinks, retaining the VAS checkout. Reading needs no Node;
helpers require Node.js 18+, and rendered checks need separate Chrome/Puppeteer.
Together AI generation is optional and may incur costs; photo licenses and
credits remain separate from MIT. See the [Hallmark VI/EN guide](docs/hallmark.md)
for every agent destination and complete prerequisites.

#### TypeSafe: Jev/System One integrations

[Open TypeSafe in the catalog](https://huytran1120.github.io/vie-agentic-skills/?lang=en&skill=typesafe-ai),
choose an agent and use **Copy Agent Prompt** to install `SKILL.md` and `LICENSE`
without cloning. From a VAS checkout, replace `/Projects/my-app` with your project:

```bash
./vas install typesafe-ai --target cursor --mode copy --dest "/Projects/my-app/.cursor/skills"
./vas status --target cursor --dest "/Projects/my-app/.cursor/skills"
./vas uninstall typesafe-ai --target cursor --dest "/Projects/my-app/.cursor/skills"
```

Use `--mode link` for symlinks, retaining the VAS checkout. The skill is MIT;
actual API calls need TypeSafe access and a server-side `TYPESAFE_API_KEY`.
Installation never installs an SDK, reads keys or sends data. Live probes need
permission, data disclosure and an agreed budget. See the [TypeSafe VI/EN guide](docs/typesafe.md)
for every agent destination and complete prerequisites.

#### Android — 35 new skills from Google

[Open the Android collection](https://huytran1120.github.io/vie-agentic-skills/?lang=en&sources=android),
choose a skill and agent, then **Copy Agent Prompt** to install every file without
cloning. The existing `android-cli` is preserved, not upgraded or renamed.
From a VAS checkout:

```bash
./vas install navigation-3 --target cursor --mode copy --dest "/Projects/my-app/.cursor/skills"
./vas status --target cursor --dest "/Projects/my-app/.cursor/skills"
./vas uninstall navigation-3 --target cursor --dest "/Projects/my-app/.cursor/skills"
```

`--mode link` requires keeping the checkout in place. Each skill retains
Apache-2.0, `LICENSE.txt`, references, code samples and local helpers.
SDK/JDK/Gradle, optional R8 protobuf, devices and Perfetto binary downloads are
separate prerequisites, never automatic installation, execution or data submission.
See the [Android VI/EN guide](docs/android.md) for all skills, agent paths and requirements.

#### GameDev — 77 specialized skills and one router

[Open the GameDev collection](https://huytran1120.github.io/vie-agentic-skills/?lang=en&sources=gamedev),
choose a skill and agent, then **Copy Agent Prompt** without cloning.
The standalone router bundles all 77 specialized companions as read-only
references, not additional catalog entries. From a VAS checkout:

```bash
./vas install router --target cursor --mode copy --dest "/Projects/my-app/.cursor/skills"
./vas status --target cursor --dest "/Projects/my-app/.cursor/skills"
./vas uninstall router --target cursor --dest "/Projects/my-app/.cursor/skills"
```

`--mode link` requires keeping the checkout in place. Apache-2.0 LICENSE/NOTICE,
support files, executable modes and the separate Go-Fonts notice are preserved.
Only two genuinely different name collisions use `gamedev-performance-optimization`
and `gamedev-godot-export`; existing skills stay unchanged. Engine/Pillow setup,
helper execution and publishing are never automatic. See the
[GameDev VI/EN guide](docs/gamedev.md) for all agent paths and prerequisites.

#### UI Unslop — Damir Sokolovsky

[Open UI Unslop](https://huytran1120.github.io/vie-agentic-skills/?lang=en&skill=heydamir-unslop&agent=cursor),
choose an agent and **Copy Agent Prompt** to install all 19 files without cloning.
`heydamir-unslop` is the UI workflow, not the existing prose-processing `unslop`.
Retain **CC-BY-4.0**, Damir Sokolovsky ([@heydamir](https://x.com/heydamir)) credit,
[heydamir/unslop](https://github.com/heydamir/unslop) attribution, LICENSE and
recorded adaptation notices; the original work is not relicensed as MIT.

```bash
./vas install heydamir-unslop --target cursor --mode copy --dest "/Projects/my-app/.cursor/skills"
./vas status --target cursor --dest "/Projects/my-app/.cursor/skills"
./vas uninstall heydamir-unslop --target cursor --dest "/Projects/my-app/.cursor/skills"
```

`--mode link` needs the VAS checkout to remain in place. References, visuals,
examples and optional helpers are complete. Node/Playwright/browser and ffmpeg
are separate helper prerequisites, never automatic installation, execution,
website capture or image-service connection. See the
[UI Unslop VI/EN guide](docs/unslop.md) for every agent folder and required consent.

### 5. Agent-Specific Setup Guides

- **Google Antigravity**: Discovered automatically through `.agents/skills/` or globally at `~/.gemini/antigravity/skills/`:
  ```bash
  ./vas install <skill_id> --target antigravity --mode link
  ./vas install <skill_id> --target global
  ```
- **OpenAI Codex / OpenCode**: Excels at direct code reasoning and command execution:
  ```bash
  ./vas install <skill_id> --target codex --mode link
  ```
  *Sample prompt for Codex:*
  > *"Inspect the runbook at `.codex/skills/<skill_id>/SKILL.md` and execute the security audit workflow for this workspace."*
- **Claude Code**: Reads skills from `.claude/skills/` or user home `~/.claude/skills/`:
  ```bash
  ./vas install <skill_id> --target claude --mode link
  ```
- **Cursor IDE**: Links to `.cursor/skills/` and integrates with `.cursorrules` or `@.cursor/skills/<skill_id>` in Composer:
  ```bash
  ./vas install <skill_id> --target cursor --mode link
  ```
- **Windsurf (Codeium)**: Loads workflows seamlessly from `.windsurf/skills/`:
  ```bash
  ./vas install <skill_id> --target windsurf --mode link
  ```
- **Cline / Roo Code**:
  ```bash
  ./vas install <skill_id> --target cline --mode link
  ```
- **GitHub Copilot CLI**: Integrates test & CI/CD skills under `.github/skills/`:
  ```bash
  ./vas install <skill_id> --target copilot --mode link
  ```

---

### 6. CLI Reference (`./vas`)

```bash
# 1. Search skills by keyword
./vas search kubernetes
./vas search "react performance" --limit 15

# 2. List skills with optional filters
./vas list --category security
./vas list --tag python --limit 20

# 3. Inspect metadata and preview Runbook
./vas show ui-ux-pro-max
./vas show docker-expert

# 4. Install skills
./vas install ui-ux-pro-max 007 --target codex
./vas install --category devops --target claude
./vas install --category security --target all

# 5. Uninstall skills
./vas uninstall 007 --target codex
./vas uninstall docker-expert --target all

# 6. Check installed skills status
./vas status --target codex
./vas status --target antigravity

# 7. Initialize workspace & rebuild index
./vas init
./vas sync
./vas guide
```

---

### 7. Open Skill Specification (`SKILL.md`)

Every skill within `skills/<skill_name>/` follows the vendor-neutral Open Agent Skills format:

```text
skills/<skill_name>/
├── SKILL.md          # [Required] YAML Frontmatter + Step-by-step Runbook
├── scripts/          # [Optional] Automation scripts (Python, Bash, JS)
├── examples/         # [Optional] Sample configs, input/output fixtures
└── references/       # [Optional] In-depth technical guides & checklists
```

```markdown
---
name: docker-expert
category: devops
tags: [docker, security, hardening, containers]
risk: safe
description: >-
  Use this skill when auditing Dockerfile or container configurations
  against security vulnerabilities, root execution, and secret leaks.
---

# Docker Security Hardening Runbook

## Instructions
1. Run static analysis: `scripts/analyze.sh`
2. Verify base image tags and non-root USER directive.
3. Review exposed ports and multi-stage build patterns.
```

---

### 8. Senior Engineering SDLC & 25 Addy Osmani Skills

By default, AI coding agents follow the path of least resistance: jumping directly into code without a specification, bypassing test-driven development, skipping security or performance threat modeling, and self-rationalizing that *"it seems right"*.

Inspired by and directly synchronized with the official **v0.6.13 release of Addy Osmani's agent skills** ([addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) & [skills.addy.ie](https://skills.addy.ie/)), VAS integrates all **25 production-grade skills** mapped 1:1 across **6 phases of the software development lifecycle (SDLC)**:

```text
   DEFINE           PLAN            BUILD           VERIFY          REVIEW           SHIP
  ┌────────┐      ┌────────┐      ┌────────┐      ┌────────┐      ┌────────┐      ┌────────┐
  │  Idea  │ ───▶ │  Spec  │ ───▶ │  Code  │ ───▶ │  Test  │ ───▶ │   QA   │ ───▶ │   Go   │
  │ Refine │      │  PRD   │      │  Impl  │      │ Debug  │      │  Gate  │      │  Live  │
  └────────┘      └────────┘      └────────┘      └────────┘      └────────┘      └────────┘
   /spec           /plan           /build          /test          /review          /ship
```

#### 🛡️ The 4 Pillars of Senior Engineering Discipline
1. **Process, not prose**: Skills are actionable execution workflows with discrete steps, checkpoints, and strict exit criteria—not generic prompt advice.
2. **Anti-rationalization**: Every skill includes a *Common Rationalizations* table dismantling typical agent excuses (*"I'll write tests later"*, *"This is too trivial for security review"*), paired with actionable *Red Flags*.
3. **Verification is non-negotiable**: Agents must prove claims with reproducible evidence (passing test suites, runtime logs, DOM inspection, heap snapshots). "Seems right" is never accepted.
4. **Progressive disclosure**: `SKILL.md` serves as a lightweight entry point (< 150 prompt tokens initially). Supplementary in-depth guides load strictly on demand.

#### 📋 Complete Catalog of 25 Addy Osmani Skills by Phase

##### 🧭 Meta - Workflow Routing
| Skill | Core Capability | Trigger Condition |
| :--- | :--- | :--- |
| [`using-agent-skills`](skills/using-agent-skills/SKILL.md) | Maps incoming work to the appropriate skill workflow and defines shared operating boundaries | Starting a session or deciding which workflow applies |

##### 🎯 1. Define - Clarify What to Build
| Skill | Core Capability | Trigger Condition |
| :--- | :--- | :--- |
| [`interview-me`](skills/interview-me/SKILL.md) | Interrogates requirements one question at a time until reaching ~95% confidence on user intent | Requirements are ambiguous or user invokes "interview me" / "grill me" |
| [`idea-refine`](skills/idea-refine/SKILL.md) | Structured divergent/convergent thinking transforming raw ideas into concrete technical proposals | Exploring or scoping a rough early concept |
| [`spec-driven-development`](skills/spec-driven-development/SKILL.md) | Authors detailed PRDs covering objectives, CLI commands, architecture, code style, and testing gates before code | Starting a greenfield project, new feature, or major refactor |
| [`constraint-driven-development`](skills/constraint-driven-development/SKILL.md) | Establishes an enforceable quality bar in `CONSTRAINTS.md`, preventing agents from lowering thresholds | Team standards lack enforcement or an agent writes excessive unchecked code |

##### 🗺️ 2. Plan - Deconstruct & Sequence
| Skill | Core Capability | Trigger Condition |
| :--- | :--- | :--- |
| [`planning-and-task-breakdown`](skills/planning-and-task-breakdown/SKILL.md) | Decomposes specs into atomic, testable units with explicit acceptance criteria and topological ordering | A spec exists and needs implementation-ready task slices |

##### 🔨 3. Build - Implement with Rigor
| Skill | Core Capability | Trigger Condition |
| :--- | :--- | :--- |
| [`incremental-implementation`](skills/incremental-implementation/SKILL.md) | Delivers thin vertical slices: Implement → Test → Verify → Commit. Features safe defaults & rollback safety | Any code change touching more than one file |
| [`test-driven-development`](skills/test-driven-development/SKILL.md) | Red-Green-Refactor, 80/15/5 test pyramid, DAMP over DRY, Beyonce Rule, runtime browser verification | Writing new logic, fixing bugs, or changing system behavior |
| [`context-engineering`](skills/context-engineering/SKILL.md) | Feeds agents optimal context: rules configuration, context packing, MCP tool scoping | Starting a session, context switching, or when response quality degrades |
| [`source-driven-development`](skills/source-driven-development/SKILL.md) | Anchors framework decisions in official upstream documentation, citing sources and flagging deprecated APIs | High-correctness implementations requiring verified modern patterns |
| [`doubt-driven-development`](skills/doubt-driven-development/SKILL.md) | Fresh-context adversarial review of high-stakes decisions: CLAIM → EXTRACT → DOUBT → RECONCILE → STOP | High-risk changes (production, auth, finance), or unfamiliar codebases |
| [`frontend-ui-engineering`](skills/frontend-ui-engineering/SKILL.md) | Component architecture, state machines, responsive typography, and WCAG 2.1 AA accessibility | Designing or implementing client-facing web interfaces |
| [`api-and-interface-design`](skills/api-and-interface-design/SKILL.md) | Contract-first API design, Hyrum's Law, One-Version Rule, robust error semantics, input boundary validation | Authoring public APIs, microservice contracts, or module boundaries |

##### 🔍 4. Verify - Prove Correctness
| Skill | Core Capability | Trigger Condition |
| :--- | :--- | :--- |
| [`browser-testing-with-devtools`](skills/browser-testing-with-devtools/SKILL.md) | Leverages Chrome DevTools MCP for live runtime telemetry: DOM tree, console logs, network waterfalls, profiling | Building or troubleshooting browser-executed applications |
| [`debugging-and-error-recovery`](skills/debugging-and-error-recovery/SKILL.md) | 5-step triage: Reproduce → Localize → Reduce → Fix → Guard. Stop-the-line protocol and safe fallbacks | Failing test suites, broken builds, or unexpected runtime faults |

##### ⚖️ 5. Review - Pre-Merge Quality Gates
| Skill | Core Capability | Trigger Condition |
| :--- | :--- | :--- |
| [`code-review-and-quality`](skills/code-review-and-quality/SKILL.md) | Multi-axis review, ~100-line change sizing, explicit severity labels (Nit/Optional/FYI), review speed norms | Prior to merging any Pull Request |
| [`code-simplification`](skills/code-simplification/SKILL.md) | Chesterton's Fence, Rule of 500, dead code removal, minimizing cognitive complexity while preserving behavior | Functional code that suffers from excessive indirection or bloat |
| [`security-and-hardening`](skills/security-and-hardening/SKILL.md) | OWASP Top 10 mitigation, secrets hygiene, dependency supply-chain auditing, 3-tier trust boundary model | Handling untrusted input, user authentication, storage, or external APIs |
| [`performance-optimization`](skills/performance-optimization/SKILL.md) | Measurement-driven performance: Core Web Vitals (LCP, INP, CLS), CPU/RAM profiling, bundle budgeting | Strict performance SLAs exist or regression is suspected |

##### 🚀 6. Ship - Deploy with High Confidence
| Skill | Core Capability | Trigger Condition |
| :--- | :--- | :--- |
| [`git-workflow-and-versioning`](skills/git-workflow-and-versioning/SKILL.md) | Trunk-based development, atomic commits, and the commit-as-save-point pattern | Making any code modification in version control |
| [`ci-cd-and-automation`](skills/ci-cd-and-automation/SKILL.md) | Shift Left testing, Faster is Safer principle, quality gate pipelines, failure feedback loops | Establishing or optimizing automated build and deployment pipelines |
| [`deprecation-and-migration`](skills/deprecation-and-migration/SKILL.md) | Treating code as a liability, sunsetting zombie code, managing structured data & user migration paths | Sunsetting legacy services, deprecating endpoints, or refactoring schemas |
| [`documentation-and-adrs`](skills/documentation-and-adrs/SKILL.md) | Architecture Decision Records (ADRs), API references, documenting the *Why* behind engineering choices | Making architectural choices, public interface changes, or shipping milestones |
| [`observability-and-instrumentation`](skills/observability-and-instrumentation/SKILL.md) | Structured JSON logging, RED/USE metrics, OpenTelemetry distributed tracing, symptom-based alerting | Instrumenting telemetry or preparing services for production operations |
| [`shipping-and-launch`](skills/shipping-and-launch/SKILL.md) | Pre-flight checklists, staged canary rollouts, instant rollback procedures, active monitoring watch | Pre-release production deployments |

```bash
# Install the entire Addy Osmani Engineering Suite into your workspace:
./vas install test-driven-development debugging-and-error-recovery security-and-hardening performance-optimization code-review-and-quality --target all
```

---

### 9. 7 Technical Checklists & Reviewer Personas

#### 📚 Enterprise-Grade Reference Checklists (`references/`)
VAS skills dynamically load 7 comprehensive technical reference checklists housed in `references/`:

| Reference Guide | Subject Matter |
| :--- | :--- |
| [`references/definition-of-done.md`](references/definition-of-done.md) | Global Definition of Done (DoD) contract that every PR and task slice must satisfy |
| [`references/testing-patterns.md`](references/testing-patterns.md) | Production test layouts, naming semantics, mocking boundaries, React/API/E2E patterns, and anti-patterns |
| [`references/security-checklist.md`](references/security-checklist.md) | Pre-commit sanity checks, authz/authn, CSP headers, CORS policies, OWASP Top 10 mitigations |
| [`references/performance-checklist.md`](references/performance-checklist.md) | Core Web Vitals thresholds, frontend/backend optimization checklists, quantitative profiling commands |
| [`references/accessibility-checklist.md`](references/accessibility-checklist.md) | Keyboard navigation, screen reader compatibility, color contrast ratios, WCAG 2.1 AA ARIA rules |
| [`references/observability-checklist.md`](references/observability-checklist.md) | 2 AM on-call operational checks, structured logging standards, RED/USE metrics, distributed traces |
| [`references/orchestration-patterns.md`](references/orchestration-patterns.md) | Approved multi-agent orchestration designs, with the rule that personas cannot recursively invoke personas |

#### 👥 Specialist Reviewer Personas
During `/ship` pre-flight or code auditing, 4 specialist personas can be fanned out in parallel for multi-perspective validation:
* 👨‍💻 **Code Reviewer (Staff Engineer)**: 5-axis review upholding the standard *"Would a Staff Engineer approve this PR?"*.
* 🧪 **Test Engineer (QA Specialist)**: Evaluates test pyramid distribution, boundary conditions, and the Prove-It pattern.
* 🛡️ **Security Auditor (Security Specialist)**: Audits STRIDE threat boundaries, privilege escalation, and OWASP vulnerabilities.
* ⚡ **Web Performance Auditor (Performance Specialist)**: Enforces Core Web Vitals metrics honesty with Quick/Deep audit passes.

---

### 10. Honest Comparison Matrix (How VAS Compares)

| Dimension | Vie Agentic Skill (VAS) | Addy Osmani (`agent-skills`) | Superpowers (`obra`) | Matt Pocock Skills |
| :--- | :--- | :--- | :--- | :--- |
| **Catalog Scale** | **3,172+ Skills** (World's most extensive) | 25 Core Skills | ~14 Skills | ~30 Skills |
| **Tooling & Engine** | **Native Python 3 CLI (`./vas`) — Zero-NPX** | `npx skills` / Plugins | Git Worktrees / Shell scripts | Claude Code / `npx skills` |
| **Dependencies & Offline**| **100% Offline, Zero external dependencies** | Requires Node & remote NPX | Requires clone & git setup | Requires Node & remote NPX |
| **Agent Support** | **7+ AI Coding Assistants** (Antigravity, Codex, Claude, Cursor, Windsurf, Cline, Copilot) | Claude Code, Codex, Antigravity, Cursor, Copilot | Claude Code, Codex, Cursor | Claude Code primary |
| **SDLC Lifecycle Depth**| **Complete 6-Phase Lifecycle**: Define ➔ Plan ➔ Build ➔ Verify ➔ Review ➔ Ship | Complete 6-Phase Lifecycle | Focused on Build/Plan loop | Focused on Grilling & TDD |
| **Anti-Rationalization**| **Common Rationalizations & Red Flags in skills** | Built into all 25 skills | Task reviewer sign-off gate | None explicit |
| **Quality & Regression**| **95 Automated Tests (Python, Node, Cloudflare Security)** | 3-tier eval framework | TDD for documentation | No in-repo tests |
| **Context Optimization**| **Strict Progressive Disclosure** (< 150 prompt tokens initially) | Progressive Disclosure | Subagent Context Handoff | Split User/Model Invoked |

---

### 11. Featured & Viral Skills Showcase (Top 20)

VAS includes **3,172+ skills** across **119 specialized categories**. Browse the full directory in [CATALOG.md](CATALOG.md).

| # | Skill ID | Stars | Capability Overview | Quick Install Command |
| :-: | :--- | :---: | :--- | :--- |
| 1 | `ui-ux-pro-max` | ⭐ 139K | Generates a full Design System (79 styles, 192 palettes, 74 font pairings) from a project brief | `./vas install ui-ux-pro-max --target all` |
| 2 | `impeccable` | ⭐ 86K | Anti "AI-slop" design skill with 62 rule-based checks and 30+ bespoke design refinement modes | `./vas install impeccable --target all` |
| 3 | `hyperframes` | ⭐ 71K | HTML-rendered MP4 video for AI agents; includes `hyperframes-figma`, `motion-doctrine`, `seam-craft` | `./vas install hyperframes --target all` |
| 4 | `remotion` | ⭐ 67K | Official 12-skill suite for programming video in React (`remotion-create`, `remotion-render`, `remotion-captions`...) | `./vas install remotion-best-practices --target all` |
| 5 | `penpot` | ⭐ 62K | Open-source Figma alternative MCP server + 14 Penpot AI Kit skills (`penpot-build-screen`, `penpot-audit-tokens`...) | `./vas install penpot penpot-router --target all` |
| 6 | `diagram-design` | ⭐ 60K | Outputs 45 architectural & technical diagram types as standalone HTML+SVG matched to your brand tokens | `./vas install diagram-design --target all` |
| 7 | `blender-mcp` | ⭐ 32K | Connects Blender 3D to any LLM via MCP for prompt-driven modeling, materials, lighting, and rendering | `./vas install blender-mcp --target all` |
| 8 | `img2threejs` | ⭐ 19K | Procedurally reconstructs objects from reference images into code-only, animation-ready Three.js | `./vas install img2threejs --target all` |
| 9 | `video-shotcraft` | ⭐ 13K | Captures real web pages, selects from 150+ shot recipes, and renders promo videos using Remotion | `./vas install video-shotcraft --target all` |
| 10 | `lemo-opuscar` | ⭐ 6.5K | Directs and produces short films with 59 cinema styles crafted entirely in code, no video model required | `./vas install lemo-opuscar --target all` |
| 11 | `landing-page-design` | ⭐ Hot | Complete system for building high-converting landing pages (intake, layout, copy, visual system, fluid island nav, fluid motion) | `./vas install landing-page-design --target all` |
| 12 | `day-trader-skill` | ⭐ Hot | 11-skill Day Trading suite for US equities: chart scanning, SEC EDGAR news, entry/exit timing, Monte Carlo Time Machine, risk management & broker orders | `./vas install day-trader-skill --target all` |
| 13 | `ffmpeg-skill` | ⭐ Hot | 42-script local FFmpeg automation suite: lossless cutting, 9:16 reframe, karaoke subtitles, silence removal, ducking & compliance exports | `./vas install ffmpeg-skill --target all` |
| 14 | `design-to-motion` | ⭐ Hot | Converts static designs (Figma frames, dashboards, UI cards) into animated HTML, MP4 for X, and seamless 800×500 GIFs | `./vas install design-to-motion --target all` |
| 15 | `skills-manager` | ⭐ Hot | Orchestrates, syncs, backs up, and audits skills across Claude Code, Antigravity, Cursor, Windsurf, Codex | `./vas install skills-manager --target all` |
| 16 | `react-spring` | ⭐ 28K | Physics-based spring animation engine for natural, fluid UI motion in React, Three.js & Canvas | `./vas install react-spring --target all` |
| 17 | `pixijs` | ⭐ 43K | High-performance 2D WebGL/WebGPU graphics rendering engine for interactive canvases, particles & visual effects | `./vas install pixijs --target all` |
| 18 | `rapier` | ⭐ 6.8K | Fast 2D & 3D WebAssembly physics engine written in Rust for Three.js, React Three Fiber & game simulations | `./vas install rapier --target all` |
| 19 | `faster-whisper` | ⭐ 17K | Up to 4x faster speech-to-text transcription via CTranslate2 with word-level timestamps & SRT/VTT export | `./vas install faster-whisper --target all` |
| 20 | `obs-studio` | ⭐ 60K | Programmatic screen capture, scene automation, and high-bitrate recording pipelines via OBS WebSocket v5 | `./vas install obs-studio --target all` |

```text
📊 TOP CATEGORY DISTRIBUTION:
├── 🛡️  Security              : 267 skills (OWASP, Pentest, Secret Audit, IAM, Hardening)
├── 💻  Development           : 230 skills (Refactoring, Clean Code, Design Patterns, OOP)
├── 📈  Business & Strategy   : 179 skills (Market Research, Financial Models, Growth)
├── ☁️  Cloud                 : 170 skills (AWS, GCP, Azure, Serverless, Cloud Architecture)
├── ⚙️  DevOps                : 169 skills (Docker, K8s, Terraform, CI/CD, Ansible, SRE)
├── 🤖  AI & Machine Learning : 135 skills (RAG, LLM Evaluation, Prompt Engineering)
├── 🎨  Design, 3D & Video    : 120+ skills (Impeccable, UI/UX Pro Max, HyperFrames, Remotion, Penpot, Blender)
├── 🌐  Web & Fullstack       : 113 skills (React, Next.js, Vue, Node.js, FastAPI, Spring)
├── 🧪  Testing & QA          :  51 skills (Playwright, Jest, Pytest, E2E, Chaos Testing)
└── ... and 100+ more specialized domains.
```

#### 🌟 Top 10 High-End Demo Cards: Full Capabilities Showcase

<p align="center">
  <img src="docs/assets/demos/10-skills-demo-showcase.svg" alt="Top 10 High-End Demo Cards - Vie Agentic Skill" width="100%" />
</p>

* 🚀 **landing-page-design**: High-converting landing page architecture & Fluid Island Nav
* 🎨 **ui-ux-pro-max**: Generative Design System, 192 product palettes & 74 font pairings
* 🛡️ **impeccable**: Anti AI-slop design suite with 62 quantitative audit rules
* 🧊 **blender-mcp & img2threejs**: Natural language Blender 3D control & procedural Three.js
* 🎬 **video-shotcraft, hyperframes, remotion**: Programmatic video generation in React/HTML
* 📊 **diagram-design**: Enterprise cloud architecture diagrams in single HTML+SVG
* 🛠️ **chrome-devtools**: Automated browser debugging, LCP optimization, heap profiling & A11y
* ⚡ **bigquery-sql**: BigQuery query optimization, cost reduction & partition tuning
* 🔒 **firebase-firestore**: NoSQL data modeling & Firestore security rules red-team audit
* 🧬 **alphafold-fetch**: 3D biomolecular structure analysis & pLDDT confidence scoring

<details open>
<summary><b>1. High-Converting Landing Page Architecture (<code>landing-page-design</code>)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/landing-page-design.svg" alt="Landing Page Architecture Demo" width="850" />
</p>

* **Dual-Track Framework**: Strict separation between **Part A (Conversion Strategy & Copy)** and **Part B (Strict Visual Token System)**.
* **Core Doctrine**: *One offer → One audience → One primary action*.
* **Precision Engineering**: Fluid Island Navigation (floating pill nav), nested corner radius formula `r_in = r_out - padding`, fluid motion physics `cubic-bezier(0.32, 0.72, 0, 1)`, zero gratuitous background gradients.
* **Install**: `./vas install landing-page-design --target all`
</details>

<details open>
<summary><b>2. Full Design System & Palette Generation (<code>ui-ux-pro-max</code> — ⭐ 139K)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/ui-ux-pro-max.svg" alt="UI UX Pro Max Demo" width="850" />
</p>

* **Capabilities**: Generates complete, harmonious design systems from brief descriptions (79 styles, 192 product palettes, 74 typography pairings).
* **Standards**: WCAG 2.1 AAA/AA contrast compliance, 119 UX guidelines, with fast interactive CLI style search.
* **Install**: `./vas install ui-ux-pro-max --target all`
</details>

<details open>
<summary><b>3. Anti AI-Slop & Design Refinement Suite (<code>impeccable</code> — ⭐ 86K)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/impeccable.svg" alt="Impeccable Anti AI-Slop Demo" width="850" />
</p>

* **Capabilities**: Eliminates generic AI design tropes (gratuitous purple gradients, card soup, random spacing) using 62 rule-based checks.
* **Senior Modes**: Offers 30+ bespoke refinement modes (`/delight`, `/polish`, `/audit`, `/critique`) to elevate code to Out-of-Distribution Craft.
* **Install**: `./vas install impeccable --target all`
</details>

<details open>
<summary><b>4. Blender 3D Control & Procedural Three.js (<code>blender-mcp</code> & <code>img2threejs</code>)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/blender-and-3d.svg" alt="Blender and Three.js 3D Demo" width="850" />
</p>

* **Blender MCP**: Direct two-way bridge to Blender 3D via MCP server. Create meshes, assign PBR materials, rig, light, and render via natural language prompts.
* **img2threejs**: Reconstructs objects from 2D reference images into lightweight, code-only, animation-ready Three.js procedural models.
* **Install**: `./vas install blender-mcp img2threejs --target all`
</details>

<details open>
<summary><b>5. Programmatic Video & Motion Suite (<code>hyperframes</code>, <code>remotion</code>, <code>video-shotcraft</code>, <code>lemo-opuscar</code>)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/video-and-motion.svg" alt="Video and Motion Demo" width="850" />
</p>

* **HyperFrames**: Render HTML/CSS/SVG into deterministic MP4 videos for AI agents.
* **Remotion Suite**: Official 12-skill suite for programming video compositions in React.
* **Video Shotcraft & Lemo Opuscar**: 152 automated shot recipes and 59 cinema styles crafted completely in code, zero expensive video models needed.
* **Install**: `./vas install hyperframes video-shotcraft remotion --target all`
</details>

<details open>
<summary><b>6. Editorial & Cloud Architecture Diagramming (<code>diagram-design</code> — ⭐ 60K)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/diagram-design.svg" alt="Diagram Design Demo" width="850" />
</p>

* **Capabilities**: Generates 45+ complex architectural and system diagrams (AWS/GCP Cloud Architecture, K8s topology, Sequence Diagrams) into a single standalone HTML+SVG file.
* **Brand Alignment**: Automatically adopts corporate color palettes, font stacks, and layout hierarchy.
* **Install**: `./vas install diagram-design --target all`
</details>

<details open>
<summary><b>7. Automated Browser Debugging & A11y Audits (<code>chrome-devtools</code> — Google Official)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/chrome-devtools.svg" alt="Chrome DevTools MCP Automation Demo" width="850" />
</p>

* **Capabilities**: Direct autonomous browser interaction via Chrome DevTools MCP protocol. Live DOM tree inspection, memory leak diagnostics via heap snapshots, Core Web Vitals (LCP) performance profiling, and automated WCAG accessibility audits.
* **Automation**: Captures network HAR logs, pinpoints auth / CORS redirects, and autonomously fixes UI and rendering bugs.
* **Install**: `./vas install chrome-devtools --target all`
</details>

<details open>
<summary><b>8. Enterprise BigQuery SQL Cost & Performance Optimizer (<code>bigquery-sql</code> — Data Agent Kit)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/bigquery-sql.svg" alt="BigQuery SQL Performance Demo" width="850" />
</p>

* **Capabilities**: Analyzes SQL queries for anti-patterns, recommends date/timestamp partitioning and clustering keys, cuts scan volume (bytes billed) by up to 84%, and slashes query execution slot-ms.
* **Data Ecosystem**: Pairs seamlessly with dbt-bigquery, Dataform ELT, and Dataproc Serverless PySpark.
* **Install**: `./vas install bigquery-sql --target all`
</details>

<details open>
<summary><b>9. Firestore Security Rules Red-Team Auditor & NoSQL Modeling (<code>firebase-firestore</code> — Firebase Suite)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/firebase-firestore.svg" alt="Firebase Firestore Security Demo" width="850" />
</p>

* **Capabilities**: Automated security rule auditor identifying privilege escalation vulnerabilities, missing authorization checks, unvalidated writes, and resource exhaustion attacks.
* **Architecture**: Production-ready NoSQL document modeling, composite index creation, and SSR integration with Next.js/Angular via Firebase App Hosting.
* **Install**: `./vas install firebase-firestore --target all`
</details>

<details open>
<summary><b>10. 3D Biomolecular Structure Analysis & AlphaFold Scoring (<code>alphafold-fetch</code> — Science Plugin)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/alphafold-science.svg" alt="AlphaFold Science 3D Suite Demo" width="850" />
</p>

* **Capabilities**: Queries the AlphaFold Database by UniProt accession ID, retrieves predicted 3D structures (mmCIF), calculates pLDDT confidence scores, assesses domain boundaries, and flags disordered regions.
* **Interactive 3D Viewer**: Plugs directly into the Mol* Biomolecular Structure Viewer sidecar and biological research databases (ChEMBL, ClinVar, BLAST).
* **Install**: `./vas install alphafold-fetch --target all`
</details>

---

#### Matt Pocock skills

Added **16 missing stable skills** from [mattpocock/skills](https://github.com/mattpocock/skills)
at revision `5beb35b040e3de97e54fa9e386d7e42d15c295c2`, preserving **19 existing customized skills**.
All 31 current stable upstream skills are represented; 4 legacy entries remain available.
The 7 experimental `in-progress/` skills are intentionally excluded.

```bash
./vas search mattpocock/skills --limit 40
./vas install code-review to-spec to-tickets writing-for-agents --target antigravity
```

New imports retain Matt Pocock's MIT license and supporting files. Target-project prerequisites
(such as Claude Code, Bash/jq, or Node.js) are separate from the dependency-free VAS manager.
See the [pinned import manifest](data/mattpocock-skills.json) for provenance.

---

#### 🛡️ Cloudflare Security Audit (`cloudflare-security-audit`)

Integrated directly from Cloudflare's official open-source repository: [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill).

Enterprise-grade security guidance and adversarial vulnerability review pipeline designed to eliminate LLM context degradation and speculative false positives:
* **Deterministic Six-Phase Review Pipeline**: Reconnaissance, Coverage-Led Hunting, Candidate Validation, Structured Output, Independent Record Verification, Target-Neutral Reporting.
* **12 Targeted Attack Class Companions**: AI/LLM Prompt Injection & Tool Poisoning, Memory Safety & Binary, Cloud & Deployment SSRF, Web Protocols & Auth, ReDoS, Supply Chain, and Data Isolation.
* **Zero-Dependency Validators Included**: Bundled with deterministic Node.js verification harnesses (`validate-coverage-ledger.cjs` & `validate-findings.cjs`, passing all 65 test suites).

```bash
# Inspect the skill or use convenient aliases:
./vas show cloudflare-security-audit
./vas show security-audit-skill

# Install into your preferred AI agent:
./vas install cloudflare-security-audit --target antigravity --mode link
./vas install cloudflare-security-audit --target all
```

---

<a id="blender-studio-en"></a>
#### 🧊 Blender Studio — 94-Skill 3D Modeling & Animation Suite

The MIT-licensed [arjun988/blender-skills](https://github.com/arjun988/blender-skills) pack is pinned to `8f778d2405a214b508d4c7d80742be8e43acdd52` and imported once under `blender-skills/<name>`. Each skill includes its complete reference files and MIT notice. See [import notes](skills/blender-skills/README.md) and [source/vendored hashes](data/blender-import.json).

```bash
# List all 94 Blender skills:
./vas list --category blender

# Install core skills for your preferred AI agent:
./vas install blender-skills/blender-director blender-skills/blender-modeler --target claude --global
./vas install blender-skills/geometry-nodes blender-skills/texture-workflow --target antigravity
```

*Prerequisites Note:* Blender and a compatible Blender MCP server connection are separate prerequisites. VAS provides standardized agent playbooks and execution guides; it does not install Blender or launch external daemons. Use `--mode copy` for an independent workspace copy; `--mode link` requires preserving the repository source tree.

---

#### 🎬 The 20 Creative Coding, Motion & Programmatic Video Stack

VAS integrates the comprehensive modern stack of 20 creative coding, animation, 2D/3D physics, audio, and programmatic video rendering tools for AI agents:

| # | Tool | Skill / Alias | Core Focus & Domain | Quick Install Command |
| :-: | :--- | :--- | :--- | :--- |
| 01 | **Remotion** | `remotion` | React Video Engine for code-driven video | `./vas install remotion --target all` |
| 02 | **HyperFrames** | `hyperframes` | High-fidelity HTML-to-video rendering pipeline | `./vas install hyperframes --target all` |
| 03 | **Anime.js** | `animejs` / `anime.js` | Timeline choreography, SVG morphing & CSS animations | `./vas install animejs --target all` |
| 04 | **React Spring** | `react-spring` | Physics-based spring animation engine for React & 3D | `./vas install react-spring --target all` |
| 05 | **PixiJS** | `pixijs` / `pixi` | High-performance 2D WebGL/WebGPU graphics rendering | `./vas install pixijs --target all` |
| 06 | **p5.js** | `p5js` / `p5` | Generative art, algorithmic visuals & creative coding | `./vas install p5js --target all` |
| 07 | **Paper.js** | `paperjs` / `paper` | Vector graphics, Bézier math & boolean path operations | `./vas install paperjs --target all` |
| 08 | **Matter.js** | `matterjs` / `matter` | 2D rigid body dynamics & collision simulation | `./vas install matterjs --target all` |
| 09 | **Three.js** | `threejs` / `three` | 3D scenes, WebGL geometry, materials & lighting | `./vas install threejs --target all` |
| 10 | **Rapier** | `rapier` / `rapier3d` | Ultra-fast 2D & 3D physics in Rust & WebAssembly | `./vas install rapier --target all` |
| 11 | **OGL** | `ogl` / `ogl-webgl` | Minimal (~10KB) WebGL library for custom GLSL shaders | `./vas install ogl --target all` |
| 12 | **tsParticles** | `tsparticles` | Interactive particle nodes, canvas backgrounds & confetti | `./vas install tsparticles --target all` |
| 13 | **glTF Transform**| `gltf-transform` / `gltf` | 3D glTF/GLB optimization, DRACO, Meshopt & KTX2 | `./vas install gltf-transform --target all` |
| 14 | **GL Transitions**| `gl-transitions` | 50+ GLSL shader transitions for web canvas & video | `./vas install gl-transitions --target all` |
| 15 | **OBS Studio** | `obs-studio` / `obs` | Programmatic screen capture & OBS WebSocket v5 | `./vas install obs-studio --target all` |
| 16 | **Chatterbox** | `chatterbox` | Neural AI voiceover & voice cloning (Resemble AI) | `./vas install chatterbox --target all` |
| 17 | **Tone.js** | `tonejs` / `tone` | Web Audio framework for synths, SFX & audio scheduling | `./vas install tonejs --target all` |
| 18 | **faster-whisper**| `faster-whisper` / `whisper` | Fast speech-to-text transcription & SRT/VTT captions | `./vas install faster-whisper --target all` |
| 19 | **OpenCut** | `opencut` / `video-editor` | Timeline-based video composition & editing via code | `./vas install opencut --target all` |
| 20 | **FFmpeg** | `ffmpeg` / `ffmpeg-skill` | 42 local scripts for cutting, LUFS, subtitles & exports | `./vas install ffmpeg --target all` |

---

#### 📈 Automated US Equities Day Trading Suite (`day-trader-skill` - 11 Modules)

A modular 11-skill trading pipeline equipping AI agents to analyze, screen, and execute US equity trades:
* **The 11 Dedicated Modules**:
  - `trader-scanner`: Momentum, relative volume & volatility breakout screener.
  - `trader-news`: Real-time financial headlines & sentiment extraction.
  - `trader-entry` & `trader-exit`: Precise technical entry/exit triggers based on Risk-to-Reward.
  - `trader-risk` & `trader-budget`: Capital allocation, position sizing, and stop-loss enforcement.
  - `trader-broker`: Brokerage execution API connector (Alpaca, Interactive Brokers).
  - `trader-timemachine`: Strategy backtesting over historical tick and bar data.
  - `trader-alerts`: Multi-channel notification pipeline (Telegram, Discord, Webhooks).
  - `trader-analyst`: Fundamental balance sheet & valuation metrics analysis.
  - `trader-pelosi`: Real-time tracking of congressional stock trade disclosures.

```bash
# Install the complete suite:
./vas install day-trader-skill --target all

# Or install individual modules:
./vas install trader-scanner trader-risk trader-entry --target antigravity
```

---

#### 🗂️ Multi-Agent Skills Library Orchestrator (`skills-manager`)

Orchestrates, syncs, backs up, and audits skill configurations across modern AI coding assistants:
* **Cross-Agent Support**: Native coordination for Claude Code, Google Antigravity, Cursor, Windsurf, Codex, Cline, and Copilot CLI.
* **Core Capabilities**: Automatic discovery of installed skill directories, zero-copy symlink distribution, and configuration integrity audits.

```bash
./vas show skills-manager
./vas install skills-manager --target all
```

---

#### 🎨 Static Design to Fluid Motion & Video (`design-to-motion`)

A structured 3-phase methodology converting static designs (Figma frames, UI cards, dashboards) into living, interactive animated HTML, MP4 video for X, and seamless 800×500 showcase GIFs:
* **Part A (Pixel-Exact Recreation)**: 1:1 fidelity reconstruction of the design without arbitrary styling divergence.
* **Part B (Motion Choreography)**: Natural enter transitions from empty states into perpetual narrative loops.
* **Part C (Multi-Format Delivery)**: Automated video and GIF encoding for social sharing and web embedding.

```bash
./vas show design-to-motion
./vas install design-to-motion --target all
```

---

#### 🎞️ Automated Local Video & Audio Suite (`ffmpeg-skill`)

A comprehensive 42-script automation toolkit for pure Python local video and audio workflows:
* **Lossless Editing**: Keyframe-exact cuts, 9:16 vertical reframing for Reels/TikTok, scene detection, and visual contact sheets.
* **Audio & Subtitle Processing**: EBU R128 loudness normalization (-14 LUFS), automatic speech ducking, and word-accurate animated subtitles.

```bash
./vas show ffmpeg-skill
./vas install ffmpeg-skill --target all
```

### 12. Frequently Asked Questions (FAQ)

**Q: What is the primary purpose and mission of Vie Agentic Skill (VAS)?**  
Created and curated by author Huy Tran, VAS was founded to solve skill fragmentation across modern AI coding assistants. Instead of scattered repositories or brittle remote `npx` installs, VAS aggregates, standardizes, and curates world-class agentic workflows from industry leaders and open-source pioneers (Google, Addy Osmani, Cloudflare, Matt Pocock, Blender Studio, and more) into a unified open specification ([agentskills.io](https://agentskills.io/)), empowering developers with instant, offline, zero-NPX tooling across 7+ major AI coding agents.

**Q: What value does the 25 Addy Osmani Senior Engineering skills suite bring to AI coding agents?**  
AI coding agents default to the path of least resistance: bypassing specs, jumping straight to code without test coverage, ignoring OWASP threat boundaries, and rationalizing that "it seems to work". The 25 production-grade skills enforce a disciplined 6-phase SDLC (Define → Plan → Build → Verify → Review → Ship) with anti-rationalization tables and strict evidence requirements before code can ship.

**Q: Do I need any special setup for OpenAI Codex / OpenCode?**  
*No.* Simply run `./vas install <skill_id> --target codex`. Codex parses markdown instructions natively and executes companion scripts directly in your shell environment.

**Q: Is Node.js or npm/npx required?**  
*Not at all.* VAS is built on the **Zero-NPX** philosophy. Searching, listing, and installing operate offline using standard Python 3 via `./vas`.

**Q: How do I install a skill across ALL my AI assistants?**  
Run `./vas install <skill_id> --target all`. This automatically provisions symlinks into `.agents/skills`, `.claude/skills`, `.cursor/skills`, `.windsurf/skills`, `.codex/skills`, `.cline/skills`, and `.github/skills`.

**Q: How does Progressive Disclosure save prompt tokens?**  
Even with hundreds of skills installed, AI agents initially only load the short YAML frontmatter summary. Full runbooks and scripts are injected into context only when your prompt matches the skill's trigger domain.

---

### 13. Author & License

* **Author & Curator**: **Huy Tran** ([@huytran1120](https://github.com/huytran1120))
* **Email**: `66549585+huytran1120@users.noreply.github.com`
* **Repository**: [https://github.com/huytran1120/vie-agentic-skills](https://github.com/huytran1120/vie-agentic-skills)
* **Website Catalog**: [GitHub Pages](https://huytran1120.github.io/vie-agentic-skills/) · [Local preview](http://127.0.0.1:8765/docs/)
* **Project Mission**: Aggregating, standardizing, and curating world-class agentic skills for AI developers and coding agents worldwide.
* **License**: [MIT License](LICENSE) — Applies to project engine and tooling; individual aggregated skills preserve their original licenses and attribution.

---

<p align="center">
  <b>Proudly created, aggregated & maintained by Huy Tran 🇻🇳 🌏</b><br>
  <i>Feedback, new skill suggestions, and issues are welcomed via <a href="https://github.com/huytran1120/vie-agentic-skills/issues">GitHub Issues</a>.</i>
</p>
