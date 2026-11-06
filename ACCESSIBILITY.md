# Khả năng tiếp cận

VAS hướng tới việc giúp người dùng tìm và đọc skill trên website, sử dụng CLI và đóng góp tài liệu dù có cách tương tác hoặc công nghệ hỗ trợ khác nhau. Với phần website do VAS duy trì, mục tiêu cải tiến là [WCAG 2.2 mức AA](https://www.w3.org/TR/WCAG22/). Đây là mục tiêu phát triển; dự án chưa được kiểm toán đầy đủ hoặc chứng nhận đạt mức tuân thủ này.

## Những hỗ trợ hiện có

- Liên kết bỏ qua điều hướng để tới nội dung chính, nhãn cho các điều khiển và trạng thái tải/kết quả tìm kiếm.
- Điều hướng bằng bàn phím, focus có thể nhận biết, phím tắt tìm kiếm và khôi phục focus khi quay về thư viện.
- Giao diện thích ứng với màn hình nhỏ; chế độ sáng/tối và tôn trọng lựa chọn giảm chuyển động của hệ điều hành.
- Giao diện website tiếng Việt/tiếng Anh; README sử dụng tiếng Việt. Nội dung runbook giữ ngôn ngữ nguồn.

## Môi trường và giới hạn

Bộ kiểm thử giao diện tự động dùng Chrome/Chromium trên máy tính, kích thước viewport 320–1440 px và cả chế độ giảm chuyển động. Điều đó không thay thế kiểm tra thủ công với bàn phím, phóng to văn bản hoặc trình đọc màn hình.

Khi kiểm tra thủ công, ưu tiên Chrome, Edge, Firefox và Safari bản ổn định, cùng VoiceOver hoặc NVDA khi có thể. Các tổ hợp trình duyệt, hệ điều hành và công nghệ hỗ trợ chưa được kiểm tra toàn diện; báo cáo lỗi cần ghi rõ phiên bản đang dùng.

Runbook và tài nguyên nhập từ bên ngoài có thể chứa bảng rộng, khối mã dài, hình ảnh thiếu mô tả hoặc tệp không tối ưu cho công nghệ hỗ trợ. Bản dịch, độ tương phản của mọi trạng thái và trải nghiệm trình đọc màn hình trên toàn bộ catalog chưa được kiểm toán đầy đủ. Các ứng dụng agent và dịch vụ liên kết nằm ngoài giao diện do VAS kiểm soát.

## Báo rào cản sử dụng

Mở [issue báo lỗi](https://github.com/huytran1120/vie-agentic-skills/issues/new?template=bug_report.md) và ghi rõ đây là vấn đề khả năng tiếp cận. Nêu URL/ID skill, thao tác bị cản trở, kết quả mong đợi, thiết bị, trình duyệt, mức phóng to và công nghệ hỗ trợ nếu có. Có thể gửi ảnh hoặc mô tả bằng văn bản; không bắt buộc cung cấp thông tin sức khỏe hay khuyết tật cá nhân.

Nếu không thể dùng biểu mẫu GitHub hoặc cần trao đổi riêng, gửi tới [huycongtranvn@gmail.com](mailto:huycongtranvn@gmail.com). Maintainer sẽ đánh giá ảnh hưởng và ưu tiên các rào cản ngăn tác vụ chính. Thời gian xử lý tùy mức độ phức tạp và khả năng của người duy trì.

Người đóng góp có thể xem [CONTRIBUTING.md](CONTRIBUTING.md) để chạy kiểm tra giao diện và gửi bản sửa.
