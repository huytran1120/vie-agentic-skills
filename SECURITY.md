# Chính sách bảo mật

## Phạm vi hỗ trợ

VAS tiếp nhận báo cáo về phiên bản hiện tại trên nhánh `main`: CLI `vas.py`, quá trình cài/gỡ skill, parser và dữ liệu catalog, bản dựng GitHub Pages, manifest tải tệp và nội dung skill được phân phối trong kho. Chưa có cam kết cập nhật bảo mật cho snapshot hoặc bản sao cũ; hãy cập nhật sau khi bản sửa được công bố.

Các báo cáo phù hợp gồm ghi/xóa ngoài thư mục đích, đi theo symlink không an toàn, tải hoặc thực thi nội dung không mong muốn, XSS, lộ bí mật và nội dung skill có khả năng dẫn agent tới thao tác nguy hiểm ngoài tác vụ được giao.

Công cụ và dịch vụ bên ngoài có chính sách riêng. Nếu vấn đề nằm ở dependency hoặc nguồn upstream, maintainer sẽ xác định ảnh hưởng đến VAS và có thể phối hợp với dự án liên quan. Giấy phép MIT của công cụ VAS không thay thế giấy phép riêng của từng skill.

## Báo cáo riêng

Ưu tiên [Report a vulnerability trên GitHub](https://github.com/huytran1120/vie-agentic-skills/security/advisories/new). Nếu biểu mẫu riêng chưa khả dụng hoặc bạn không sử dụng được GitHub, gửi email tới [huycongtranvn@gmail.com](mailto:huycongtranvn@gmail.com), tiêu đề bắt đầu bằng `[VAS Security]`.

Không mở issue/PR công khai chứa chi tiết khai thác, token hoặc dữ liệu của người khác. Chỉ kiểm tra trong môi trường và dữ liệu bạn được phép sử dụng; dùng dữ liệu giả cho bằng chứng tái hiện.

Báo cáo nên có:

- Tóm tắt lỗ hổng, phạm vi ảnh hưởng và tác động có thể xảy ra.
- Commit VAS, ID skill/đường dẫn liên quan, hệ điều hành và agent nếu cần.
- Các bước tái hiện tối thiểu và kết quả thực tế; ghi rõ điều kiện cần để khai thác.
- Bản sửa hoặc cách giảm thiểu nếu đã có. Xóa bí mật khỏi log và tệp đính kèm.

## Xử lý và công bố

Maintainer xác minh báo cáo, đánh giá mức độ ảnh hưởng, trao đổi cách giảm thiểu và chuẩn bị bản sửa. Ưu tiên dựa trên tác động và khả năng khai thác; thời gian phản hồi phụ thuộc khả năng của người duy trì, không có SLA cố định.

Việc công bố được trao đổi với người báo cáo để người dùng có cơ hội cập nhật. Ghi nhận người phát hiện khi họ đồng ý; không công khai danh tính hoặc bằng chứng riêng khi chưa được phép. Dự án chưa công bố chương trình thưởng tìm lỗi; việc gửi báo cáo không tạo cam kết trả thưởng.
