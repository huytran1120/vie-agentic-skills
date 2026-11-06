# Hướng dẫn đóng góp

Bạn có thể giúp VAS bằng cách báo lỗi, cải thiện tài liệu, sửa CLI/website hoặc đề xuất skill có nguồn và giấy phép rõ ràng. Khi tham gia, hãy tuân thủ [quy tắc ứng xử](CODE_OF_CONDUCT.md).

## Chọn kênh phù hợp

- **Lỗi CLI, website hoặc runbook:** dùng [mẫu báo lỗi](https://github.com/huytran1120/vie-agentic-skills/issues/new?template=bug_report.md).
- **Skill hoặc bộ sưu tập mới:** dùng [mẫu đề xuất skill](https://github.com/huytran1120/vie-agentic-skills/issues/new?template=skill_request.md), kèm nguồn, giấy phép và cách kiểm tra trùng lặp.
- **Tính năng hoặc cải tiến:** dùng [mẫu đề xuất cải tiến](https://github.com/huytran1120/vie-agentic-skills/issues/new?template=feature_request.md). Với thay đổi lớn, trao đổi phạm vi trước khi triển khai.
- **Lỗ hổng bảo mật:** báo riêng theo [SECURITY.md](SECURITY.md), không đăng mã khai thác hay thông tin nhạy cảm trong issue công khai.

Trước khi mở issue, tìm xem vấn đề đã được báo chưa. Khi báo lỗi, ghi ID skill, phiên bản hoặc commit VAS, agent, hệ điều hành, các bước tái hiện, kết quả mong đợi và kết quả thực tế. Xóa token, dữ liệu cá nhân và đường dẫn nhạy cảm khỏi log.

## Chuẩn bị thay đổi

Fork kho, tạo nhánh riêng và giữ mỗi pull request tập trung vào một mục tiêu. Đọc [AGENTS.md](AGENTS.md) nếu dùng trợ lý AI. Công cụ quản lý VAS dùng Python tiêu chuẩn; không thêm phụ thuộc ngoài cho CLI và không dùng `npx`.

Skill cần có `skills/<skill-id>/SKILL.md` với frontmatter `name`, `description`, `category`, `tags` và hướng dẫn có thể thực hiện, kiểm tra kết quả. Dùng ID ổn định; tìm skill trùng bằng `python3 vas.py search <từ-khóa>` trước khi thêm. Giữ ID, lệnh, đường dẫn và API chính xác; tài liệu sử dụng chung viết bằng tiếng Việt, còn runbook nhập từ nguồn ngoài giữ nội dung và thông báo nguồn cần thiết.

Khi nhập bộ sưu tập, ghi lại URL nguồn, revision, tác giả, giấy phép và các thay đổi cục bộ trong bản ghi nhập tương ứng. Giữ các tệp `LICENSE`, `NOTICE`, tài nguyên và thông báo bản quyền của từng skill. Chỉ đóng góp nội dung bạn có quyền phân phối; xem thêm [nguồn và giấy phép](README.md#nguon-va-giay-phep). Không khôi phục các bản upstream bị loại của `pdf`, `docx`, `pptx`, `xlsx`; đây là các runbook thay thế được viết độc lập theo MIT.

## Kiểm tra trước khi gửi

Chạy từ thư mục gốc dự án. Khi thay đổi skill hoặc metadata, dựng lại chỉ mục và đưa cả ba tệp sinh ra vào pull request:

```bash
python3 vas.py sync
git diff -- skills_index.json docs/skills.min.json CATALOG.md
```

Chọn kiểm tra phù hợp với thay đổi. Thay đổi CLI cần kiểm thử Python; thay đổi website cần kiểm thử JavaScript và kiểm tra trên trình duyệt. Bộ kiểm tra đầy đủ cần Python, Node.js và Chrome/Chromium:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py'
node --test tests/*.test.cjs
node skills/cloudflare-security-audit/validate-coverage-ledger.test.cjs
node skills/cloudflare-security-audit/validate-findings.test.cjs
python3 scripts/build_pages.py
```

CI chạy trên pull request và các lần push lên nhánh chính. Xem [workflow kiểm thử](.github/workflows/test.yml) để đối chiếu các bước đang áp dụng. Với sửa lỗi, thêm kiểm thử tái hiện có ý nghĩa; với sửa tài liệu, kiểm tra nội dung, đường dẫn và mẫu hiển thị.

Sau khi thêm tài nguyên hoặc nhập skill, kiểm tra bản dựng `_site/`: [size budget](pages-budget.json) cảnh báo ở 850 MB và chặn trên 900 MB (1 MB = 1.000.000 byte). Đây là tổng dung lượng xuất bản, không phải dữ liệu tải trang đầu. Log build liệt kê 5 thư mục lớn nhất; không tăng giới hạn để bỏ qua vấn đề dung lượng.

Để xem website trên máy:

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Mở [http://127.0.0.1:8765/docs/](http://127.0.0.1:8765/docs/). Phục vụ thư mục gốc để liên kết runbook hoạt động. Khi sửa giao diện, kiểm tra màn hình nhỏ, điều hướng bàn phím, focus và chế độ giảm chuyển động theo [cam kết khả năng tiếp cận](ACCESSIBILITY.md).

## Gửi pull request

Nêu vấn đề cụ thể, hành vi sau thay đổi và cách kiểm tra trong mẫu PR. Liên kết issue liên quan; thêm ảnh khi thay đổi giao diện. Ghi rõ bước chưa kiểm tra và lý do. Không đưa `_site/`, thông tin đăng nhập hoặc dữ liệu cá nhân vào commit. Người gửi chịu trách nhiệm kiểm tra cả thay đổi do công cụ AI hỗ trợ.

Maintainer sẽ review phạm vi, độ đúng, nguồn/giấy phép và kết quả CI. Cập nhật cùng PR khi cần sửa; thay đổi được hợp nhất sau khi các yêu cầu liên quan đã đạt. Thời gian review phụ thuộc khả năng của người duy trì.
