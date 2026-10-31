# DaVinci Resolve Video Editor trong VAS / DaVinci Resolve Video Editor in VAS

## Tiếng Việt

Đã thêm **12 skill mới / 26 tệp**, không có bản trùng phải bỏ qua.
Catalog: **3.184 skill / 119 danh mục**.
Đây là bộ kỹ năng biên tập video chuyên sâu cho **DaVinci Resolve Studio** kết hợp cùng **Claude Code** (hoặc Cursor, Codex, Antigravity) do tác giả **appariciojunior ([@appariciojunior](https://github.com/appariciojunior))** phát triển:
quy trình dựng thô từ transcript, cắt retakes, giữ nhịp vlog tự nhiên, đồng bộ B-roll, phối nhạc Epidemic Sound, tạo phụ đề burned-in, motion graphics Remotion và render chuẩn YouTube.

Toàn bộ 12 skill được cấp phép theo **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**. Bạn được phép sử dụng, sao chép, chia sẻ và tùy biến miễn phí nhưng phải ghi nhận tác giả và dẫn link nguồn gốc. Nghiêm cấm bán hoặc tích hợp vào các sản phẩm/khóa học thương mại nếu chưa có sự đồng ý bằng văn bản của tác giả.

### Danh mục 12 kỹ năng

1. **`video-editor-setup`**: Thiết lập workspace biên tập video hoàn chỉnh với Claude Code và DaVinci Resolve Studio (cấu trúc thư mục, tệp mẫu `templates/config.example.json`, tài liệu học tập `references/LEARNINGS.md`).
2. **`edit-video`**: Lệnh dựng one-command hoàn chỉnh: lấy footage từ `raw video/`, tạo transcript, cắt bỏ retakes/khoảng lặng chết, giữ B-roll và dựng timeline trong DaVinci Resolve.
3. **`rough-cut`**: Tiêu chuẩn biên tập cho cảnh talking-head, định dạng `keep.json` và `moments.json` cho planner script cắt chính xác từng frame.
4. **`vlog-pacing`**: Các thông số căn chỉnh nhịp độ vlog tự nhiên (độ dài khoảng dừng, word padding, jump-cut zoom alternation 1.075x / punch-in 1.15x).
5. **`broll`**: Phương pháp nhận diện, đánh giá và cắt ghép cảnh quay chèn (B-roll) theo nhịp kể chuyện, tránh bị transcript cut bỏ sót các clip không lời.
6. **`captions`**: Tạo phụ đề burned-in chuẩn xác từ transcript verbatim, loại bỏ từ đệm/nói lắp, chuẩn hóa tiếng lóng và căn chỉnh thời gian hiển thị.
7. **`voice-and-audio`**: Xử lý âm thanh giọng nói, chuẩn hóa loudness theo chuẩn **ITU-R BS.1770-4 (-16 LKFS / -2.0 dBTP)**, Voice Isolation và cân chỉnh EQ.
8. **`music-and-sound`**: Phối nhạc nền với Epidemic Sound MCP, tạo ducking envelope (nhỏ khi nói, nổi lên khi B-roll), thiết kế âm thanh chuyển cảnh tinh tế.
9. **`motion-overlays`**: Thiết kế motion graphics theo thương hiệu bằng Remotion, render ProRes trong suốt đặt lên layer V2+ của DaVinci Resolve.
10. **`figma-roundtrip`**: Quy trình đồng bộ 2 chiều giữa Figma boards và bộ component Remotion cùng token thương hiệu (`brand.json`).
11. **`resolve-scripting`**: Kỹ thuật scripting DaVinci Resolve Studio 21 bằng Python/Lua an toàn (thêm mới timeline/bin, đọc lại để xác minh, tránh crash).
12. **`youtube-export`**: Thiết lập Deliver tối ưu cho YouTube: QuickTime H.264, tag màu chính xác tránh hiện tượng nhạt màu (gamma shift) trên YouTube.

### Hướng dẫn sử dụng không cần clone repo (Copy Agent Prompt)

Mở giao diện web [Vie Agentic Skill](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&sources=videoeditor), chọn skill mong muốn và agent đang dùng (Claude Code, Cursor, Codex, Antigravity...), sau đó bấm **Copy Agent Prompt** và dán vào chat của agent.

Agent sẽ kiểm tra manifest `install-manifests/<skill-id>.json`, xác thực SHA-256 từng tệp, giữ nguyên cấu trúc thư mục và ghi receipt `.vas-manifest.json` tương thích với CLI.

### Hướng dẫn sử dụng qua CLI (`./vas`)

Từ thư mục checkout VAS:

```bash
# Tìm kiếm các skill biên tập video
./vas search "video editor"

# Xem chi tiết một skill
./vas show edit-video

# Cài đặt một skill vào dự án (chế độ copy độc lập)
./vas install edit-video --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Cài đặt bộ thiết lập ban đầu (kèm templates và references)
./vas install video-editor-setup --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Kiểm tra trạng thái các skill đã cài
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Gỡ bỏ skill khi không dùng
./vas uninstall edit-video --target claude --dest "/path/to/project/.claude/skills"
```

### Bảng thư mục cài đặt mặc định theo Agent

| Agent | Thư mục cài đặt trong dự án |
|---|---|
| Claude Code | `.claude/skills/<skill-id>/` |
| Cursor | `.cursor/skills/<skill-id>/` |
| Antigravity | `.agents/skills/<skill-id>/` |
| OpenAI Codex | `.codex/skills/<skill-id>/` |
| Windsurf | `.windsurf/skills/<skill-id>/` |
| Cline / Roo Code | `.cline/skills/<skill-id>/` |
| GitHub Copilot CLI | `.github/skills/<skill-id>/` |

### Yêu cầu tiên quyết & Lưu ý an toàn

- **DaVinci Resolve Studio**: Bắt buộc dùng bản Studio (bản miễn phí không hỗ trợ external scripting). Vào *Preferences > System > General*, đặt *External scripting using: Local* và khởi động lại DaVinci Resolve.
- **Quyền riêng tư & API**: Việc cài đặt skill qua VAS không tự động kích hoạt script, không cài runtime và không gọi API bên ngoài. Các dịch vụ như Epidemic Sound MCP, mô hình chuyển giọng nói thành văn bản (Speech-to-Text), Remotion hay Figma chỉ chạy khi người dùng trực tiếp yêu cầu và cấp phép rõ ràng.

---

## English

Added **12 new skills / 26 files**, zero duplicates skipped.
Catalog total: **3,184 skills / 119 categories**.
This is the complete video editing workflow for **DaVinci Resolve Studio** paired with **Claude Code** (or Cursor, Codex, Antigravity), created by **appariciojunior ([@appariciojunior](https://github.com/appariciojunior))**:
rough cutting from verbatim transcripts, cutting retakes while preserving vlog rhythm, B-roll timing, scoring with Epidemic Sound, burned-in captions, Remotion motion graphics, and YouTube Deliver settings.

All 12 skills are distributed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license. You MAY use, copy, share, and adapt them for free, provided you retain attribution and link back to the upstream repository. Commercial use, paid courses, or selling derivatives requires explicit permission from the author.

### 12 Video Editor Skills

1. **`video-editor-setup`**: Initial setup for a DaVinci Resolve Studio & Claude Code video editing workspace (folder layouts, `templates/config.example.json`, and `references/LEARNINGS.md`).
2. **`edit-video`**: The one-command first-pass edit: imports raw footage, transcribes, cuts dead air and retakes, retains B-roll, and builds the timeline in DaVinci Resolve.
3. **`rough-cut`**: Editorial rules for talking-head footage, producing `keep.json` and `moments.json` for frame-accurate cuts.
4. **`vlog-pacing`**: Natural vlog pacing parameters (silence detection, word padding, jump-cut zoom alternating at 1.075x / punch-ins at 1.15x).
5. **`broll`**: Techniques to identify, review, and cut non-speech B-roll by narrative flow rather than fixed lengths.
6. **`captions`**: Burned-in style subtitle generation from verbatim transcripts with speech slurs cleaned and timing snapped.
7. **`voice-and-audio`**: Voice processing and loudness normalization (**ITU-R BS.1770-4 at -16 LKFS / -2.0 dBTP**), Voice Isolation, and EQ.
8. **`music-and-sound`**: Scoring vlogs with Epidemic Sound MCP, baking ducking envelopes, and transition sound effects.
9. **`motion-overlays`**: Brand-consistent Remotion motion graphics kit rendered as transparent ProRes on V2+ video tracks.
10. **`figma-roundtrip`**: Two-way synchronization between editable Figma boards and Remotion component code / design tokens (`brand.json`).
11. **`resolve-scripting`**: Battle-tested DaVinci Resolve Studio 21 scripting practices in Python/Lua (safe track appends, readback verification).
12. **`youtube-export`**: Optimal Deliver export presets for YouTube (QuickTime H.264, correct color tags avoiding washed-out gamma shifts).

### No-Clone Setup (Copy Agent Prompt)

Browse the [Vie Agentic Skill Catalog](https://huytran1120.github.io/vie-agentic-skills/?lang=en&sources=videoeditor), pick any skill, select your target agent, click **Copy Agent Prompt**, and paste it into your coding agent's prompt box.

Your agent verifies `install-manifests/<skill-id>.json`, validates SHA-256 checksums, downloads required files, and writes a CLI-compatible `.vas-manifest.json` receipt.

### CLI Setup (`./vas`)

Run from your local VAS repository clone:

```bash
# Search for video editing skills
./vas search "video editor"

# Inspect skill details
./vas show edit-video

# Install into your project directory (copy mode)
./vas install edit-video --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Install setup skill with templates and references
./vas install video-editor-setup --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Check installation status
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Uninstall cleanly
./vas uninstall edit-video --target claude --dest "/path/to/project/.claude/skills"
```

### Agent Installation Directory Mapping

| Agent | Project Destination Path |
|---|---|
| Claude Code | `.claude/skills/<skill-id>/` |
| Cursor | `.cursor/skills/<skill-id>/` |
| Antigravity | `.agents/skills/<skill-id>/` |
| OpenAI Codex | `.codex/skills/<skill-id>/` |
| Windsurf | `.windsurf/skills/<skill-id>/` |
| Cline / Roo Code | `.cline/skills/<skill-id>/` |
| GitHub Copilot CLI | `.github/skills/<skill-id>/` |

### Prerequisites & Safety Notes

- **DaVinci Resolve Studio**: Requires the Studio edition (free edition does not support external scripting). Enable *Preferences > System > General > External scripting using: Local* and restart Resolve.
- **External Dependencies & Services**: Installing skills does not run scripts, modify projects, or connect to external services. Optional tools (ffmpeg, speech-to-text APIs, Epidemic Sound, Remotion, Figma) require explicit user consent and separate API credentials.
