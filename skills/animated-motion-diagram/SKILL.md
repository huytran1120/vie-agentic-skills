---
name: animated-motion-diagram
description: "Tạo sơ đồ kiến trúc động (Animated Motion Diagram) phong cách bản vẽ kỹ thuật (engineering graph-paper) với logo thương hiệu chuẩn, đường nối trực giao có dòng chảy dữ liệu chuyển động liên tục (flowing dashed streams), các hạt năng lượng phát sáng (luminous data particles) chạy dọc theo luồng, thanh điều khiển tương tác (Tạm dừng/Tiếp tục, Tốc độ 0.5x/1x/2x, Lọc luồng dữ liệu, Đổi theme Sáng/Tối) và bóng chi tiết khi rê chuột. Đóng gói thành 1 file HTML duy nhất, chạy offline 100%, không phụ thuộc thư viện ngoài. Sử dụng skill này khi người dùng yêu cầu: sơ đồ kiến trúc chuyển động, animated architecture diagram, motion diagram, interactive flow diagram, dynamic tech stack, hoặc 'vẽ giống như cũ nhưng chuyển động', 'sơ đồ chuyển động', 'animated motion diagram'."
license: MIT
compatibility: Python 3.9+ (chuẩn thư viện có sẵn, không cần cài thêm package nào)
---

# Animated Motion Diagram

Tạo sơ đồ kiến trúc hệ thống dạng **bản vẽ kỹ thuật chuyển động (Animated Motion Diagram)**:
- Giữ trọn vẹn phong cách thanh lịch của `stack-diagram`: logo thương hiệu chuẩn xác trên nền ô trắng, các khối nhóm phân tầng (group boxes), mũi tên trực giao, nền giấy kẻ ô kỹ thuật (graph-paper).
- **Chuyển động dòng chảy dữ liệu (Flowing Data Streams)**: Mọi đường kết nối đều có nét đứt chuyển động theo hướng truyền dữ liệu với hiệu ứng CSS hardware-accelerated.
- **Hạt xung năng lượng (Luminous SVG Particles)**: Các hạt dữ liệu phát sáng di chuyển mượt mà dọc theo các chu trình chính bằng `<animateMotion>`.
- **Bảng điều khiển tương tác (Interactive Controls Bar)**:
  - ⏯️ **Tạm dừng / Tiếp tục** (Pause / Play).
  - ⚡ **Tốc độ chuyển động**: `0.5x`, `1x`, `2x`.
  - 🎯 **Bộ lọc luồng (Flow Filter)**: Chuyển đổi giữa các luồng (vd: Luồng gõ phím, Luồng AI Agent, Luồng xuất file), tự động làm nổi bật các khối liên quan.
  - 🌓 **Chuyển theme Sáng / Tối**: Tương thích Dark Mode & Light Mode tức thì.
- **Tương tác chạm / rê chuột (Hover & Tooltip)**: Rê chuột vào từng Crate/Module để thấy hiệu ứng nổi khối (elevation bounce) và xem chi tiết (số dòng mã, chức năng, layer).
- **Độc lập 100% (Self-contained)**: Toàn bộ font chữ (Geist, JetBrains Mono), icon vector SVG, CSS animation và JavaScript được nhúng trực tiếp dạng data-URI trong 1 file `.html` duy nhất, hoạt động hoàn toàn offline.

---

## 🛠️ Công cụ có sẵn trong Skill

```bash
skills/animated-motion-diagram/
├── SKILL.md                          # Tài liệu hướng dẫn sử dụng
├── scripts/
│   ├── animate_diagram.py            # Chuyển đổi file sơ đồ tĩnh thành sơ đồ chuyển động
│   └── fetch_icons.py                # Tải logo vector chính thức (svgl, devicon, AWS)
├── assets/
│   ├── fonts/                        # Font chữ Geist và JetBrains Mono
│   └── generic/                      # Icon mẫu
└── references/
    └── geometry.md                   # Toạ độ và quy tắc vẽ đường trực giao
```

---

## 🚀 Quy trình thực hiện (Workflow)

### Bước 1: Chuẩn bị nội dung kiến trúc
Xác định các thành phần của hệ thống:
1. **Nodes**: Tên dịch vụ/thư viện + vai trò ngắn gọn (vd: `vforge-engine` / `Session & Commands`).
2. **Groups**: Đóng khung các dịch vụ cùng tầng/nền tảng (vd: Apps, L6 UI, L4 Engine, L2 Formats).
3. **Edges (Liên kết)**:
   - Nét chính nổi bật (Accent flow): Luồng người dùng và dữ liệu thời gian thực.
   - Nét phụ (Neutral flow): Gọi nội bộ giữa các tầng phụ thuộc.
   - Nét đứt (Dashed flow): IPC socket, kiểm thử CI/CD, webhook.

### Bước 2: Tải logo vector chính thức (nếu chưa có)
```bash
python3 scripts/fetch_icons.py <icons-dir> rust wasm egui "zotero:zotero"
```
*Nguyên tắc:* Luôn dùng logo chính thức từ `svgl` hoặc trang chủ dự án, **tuyệt đối không tự ý vẽ lại hoặc đổi màu logo**.

### Bước 3: Tạo và kích hoạt chuyển động
Dùng công cụ `animate_diagram.py` để đóng gói sơ đồ với đầy đủ hiệu ứng chuyển động:

```bash
python3 scripts/animate_diagram.py input_diagram.html output_animated.html
```

Lệnh này sẽ tự động:
1. Thêm bộ animation CSS `flowForward` trên các lớp `.e`, `.n`, `.dash`.
2. Trích xuất toạ độ SVG đường dẫn `<path d="..." />` để tạo hạt năng lượng `<circle><animateMotion /></circle>`.
3. Gắn thanh điều khiển tương tác (Play/Pause, Tốc độ, Bộ lọc luồng, Đổi màu giao diện).
4. Kích hoạt hiệu ứng hover nhấc nổi và bóng thông tin chi tiết (Tooltip).

---

## 🎨 Cấu hình CSS chuyển động chính

```css
/* Đường nối chuyển động liên tục */
.e {
  stroke: var(--color-accent);
  stroke-width: 1.8;
  stroke-dasharray: 8 6;
  animation: flowForward var(--flow-speed, 1.1s) linear infinite;
  stroke-linecap: round;
}

.n {
  stroke: var(--color-neutral);
  stroke-width: 1.5;
  stroke-dasharray: 6 6;
  animation: flowForward var(--flow-speed-slow, 1.6s) linear infinite;
}

/* Hạt xung dữ liệu phát sáng */
.particle {
  fill: var(--color-accent);
  filter: drop-shadow(0 0 5px var(--color-accent));
}

@keyframes flowForward {
  from { stroke-dashoffset: 28; }
  to { stroke-dashoffset: 0; }
}
```

---

## 💡 Định dạng bàn giao cho người dùng

- **File HTML độc lập (Standalone HTML)**: File chính thức hoàn chỉnh, người dùng có thể nhấp đúp mở bằng bất kỳ trình duyệt nào.
- **Nhúng trực tiếp vào hội thoại (Inline Generative UI)**:
  ```html
  <agent-embed src="file:///<path_to_animated.html>"></agent-embed>
  ```
