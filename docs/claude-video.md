# Claude Video (Watch) trong VAS / Claude Video (Watch) in VAS

## Tiếng Việt

Đã thêm **1 skill mới / 16 tệp**, không có bản trùng phải bỏ qua.  
Upstream: [`bradautomates/claude-video`](https://github.com/bradautomates/claude-video) tại revision `03ceb42f7fa2c4439aca01752118044baabffb8f` (phiên bản `v0.3.2`).  
Catalog: **4.078 skill / 119 danh mục**.

Kỹ năng xem, bóc tách và phân tích video đa phương thức dành cho **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline** và **GitHub Copilot CLI** do **Bradley Bonanno** phát triển:
cung cấp cho AI coding agent bằng chứng thị giác và âm thanh đa tầng từ URL video (YouTube, Vimeo, TikTok...) hoặc tệp video cục bộ (`.mp4`, `.mov`). Kỹ năng tích hợp hai engine mạnh mẽ:
1. **Engine Gemini (`gemini`)**: Sử dụng mô hình hiểu video đa phương thức của Google thông qua Gemini API (`GEMINI_API_KEY`), xem trực tiếp video và trả lời tức thì với mốc thời gian chính xác (YouTube gửi trực tiếp URL tới Google, tệp cục bộ được upload qua Files API rồi tự động dọn dẹp sau khi phân tích).
2. **Engine cục bộ (`local`)**: Không cần API key; tải video bằng `yt-dlp`, trích xuất khung hình tự thích ứng theo cảnh chuyển động bằng `ffmpeg` (scene-aware / keyframe), bóc tách phụ đề gốc (VTT captions) hoặc phiên âm giọng nói qua WhisperX cục bộ (hoặc API Groq/OpenAI Whisper khi cần).

Mã nguồn và tài liệu phát hành theo giấy phép **MIT License**, bản quyền thuộc về **Bradley Bonanno** (2026).

---

### Chi tiết kỹ năng `watch`

- **Tên kỹ năng (Canonical ID)**: `watch`
- **Mục tiêu**: Cho phép AI agent "xem" video thực tế để trả lời câu hỏi, tóm tắt bài giảng, kiểm tra lỗi giao diện, xác minh thời điểm và trích xuất bằng chứng thị giác cụ thể thay vì chỉ đọc phụ đề chữ.
- **Hai cơ chế vận hành chính**:
  - **Gemini Engine**: Khuyên dùng khi có `GEMINI_API_KEY`. Xem trọn vẹn cả video và âm thanh mà không tốn tài nguyên máy tính cục bộ.
  - **Local Engine**: Khung hình trích xuất được giới hạn chặt chẽ theo các mức chi tiết (`transcript`: không lấy khung hình; `efficient`: tối đa 50 khung hình; `balanced`: scene-aware tối đa 100 khung hình; `token-burner`: không giới hạn khung hình).
- **Bộ công cụ bundled scripts** (chạy bằng Python standard library, không phụ thuộc package ngoài):
  - `watch.py`: Điểm vào chính tiếp nhận URL/tệp, điều phối download, cắt khung hình, phân tích phụ đề và tổng hợp báo cáo Markdown cho agent.
  - `setup.py`: Trình hướng dẫn cấu hình tương tác đầu tiên, kiểm tra các binary cần thiết (`ffmpeg`, `yt-dlp`), chọn engine và lưu cấu hình bảo mật vào `~/.config/watch/.env`.
  - `frames.py`: Trích xuất khung hình thông minh dựa trên độ thay đổi cảnh (scene detection) và tự động tính toán FPS (`auto_fps`) để giữ số lượng ảnh trong tầm kiểm soát chi phí token.
  - `download.py`: Tải phụ đề và video giới hạn an toàn qua `yt-dlp`.
  - `transcribe.py`: Phân tích và lọc dòng thời gian phụ đề định dạng WebVTT/SRT.
  - `gemini.py`: Giao tiếp trực tiếp với Google Gemini Files API và Multimodal Video Model.
  - `whisper.py` & `local_whisperx.py`: Cơ chế phiên âm giọng nói dự phòng khi video không có phụ đề có sẵn.

---

### Hướng dẫn sử dụng không cần clone repo (Copy Agent Prompt)

Mở trang [Claude Video trên VAS](https://vie-agentic-skills.vercel.app/?lang=vi&sources=claudevideo), chọn agent bạn đang sử dụng, bấm **Copy Agent Prompt** và dán vào cửa sổ chat của dự án:

```text
Read the installation manifest at https://vie-agentic-skills.vercel.app/install-manifests/watch.json and install its declared files into .agents/skills/watch/.
```

Agent sẽ đọc bản kê tệp chính thức, kiểm tra mã băm SHA-256 từng tệp (gồm `SKILL.md`, `LICENSE`, `NOTICE.md` và toàn bộ 11 script trong thư mục `scripts/`), tải đúng phiên bản và ghi receipt quản lý tương thích CLI.

---

### Hướng dẫn sử dụng qua CLI (`./vas`)

Từ thư mục checkout VAS:

```bash
# Tìm kiếm kỹ năng
./vas search watch

# Xem thông tin và hướng dẫn sử dụng
./vas show watch

# Cài đặt chế độ link cho Antigravity / Universal
./vas install watch --target antigravity --mode link

# Cài đặt chế độ copy độc lập vào dự án Claude Code
./vas install watch --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Kiểm tra trạng thái cài đặt
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Gỡ bỏ cài đặt sạch sẽ
./vas uninstall watch --target claude --dest "/path/to/project/.claude/skills"
```

---

## English

Added **1 new skill / 16 files**, with zero skipped duplicates.  
Upstream: [`bradautomates/claude-video`](https://github.com/bradautomates/claude-video) at revision `03ceb42f7fa2c4439aca01752118044baabffb8f` (version `v0.3.2`).  
Catalog: **4,078 skills / 119 categories**.

Multimodal video inspection and understanding skill for **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline**, and **GitHub Copilot CLI**, developed by **Bradley Bonanno**:
equips AI coding agents with verifiable visual and auditory evidence from video URLs (YouTube, Vimeo, TikTok) or local media files (`.mp4`, `.mov`). The skill features two distinct operational engines:
1. **Gemini Engine (`gemini`)**: Leverages Google's agentic multimodal video model via the Gemini API (`GEMINI_API_KEY`) to watch full videos including audio, answering questions directly with timestamps without taxing local CPU/GPU resources.
2. **Local Engine (`local`)**: Operates entirely offline with zero required API keys; downloads media with `yt-dlp`, extracts scene-aware auto-scaled frames using `ffmpeg`, parses native VTT captions, and falls back to local WhisperX or cloud Whisper (Groq/OpenAI) when captions are absent.

Licensed under the **MIT License**, Copyright (c) 2026 Bradley Bonanno.

---

### Skill Highlights (`watch`)

- **Canonical ID**: `watch`
- **Primary Goal**: Ground agent reasoning in actual video frames and timestamped transcripts, eliminating hallucinated answers about video content and lectures.
- **Detail Levels**:
  - `transcript`: Zero frames; downloads captions only when available.
  - `efficient`: Fast keyframe selection capped at 50 frames.
  - `balanced` (default / recommended): Scene-aware frame sampling capped at 100 frames.
  - `token-burner`: Uncapped scene-aware extraction for dense visual inspection.
- **Bundled Scripts**:
  - Fully self-contained inside `scripts/`, operating on Python 3.10+ standard library.
  - Safe local installation writes only static configuration (`~/.config/watch/.env`) without executing unvetted code during installation.
