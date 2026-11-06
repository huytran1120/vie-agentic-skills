# Kiểm tra UX/UI trước khi cập nhật Vercel

Website chính: https://vie-agentic-skills.vercel.app/. GitHub Pages giữ nguyên bản cũ, không triển khai lại.

## Những phần cần giữ

- Màu sáng/tối, font hiện tại, chữ và hiệu ứng hero; chỉ đổi thiết kế khi người dùng yêu cầu.
- Thứ tự trang chủ: hero → tìm skill/thư viện → khám phá theo công việc → hướng dẫn chọn lọc → bắt đầu sử dụng → FAQ/nguồn.
- Thư viện là chức năng chính. Blog có trang riêng, luôn có đường về thư viện và liên kết đến đúng skill.
- Chọn agent/ngôn ngữ phải nhất quán giữa trang, liên kết và prompt. Dùng mapping thư mục hiện có.

Baseline nằm trong `tests/fixtures/ui-contract.json`. Khi có thay đổi thiết kế được yêu cầu, cập nhật baseline và giải thích thay đổi trong commit. Không sửa baseline, xóa assertion hoặc bỏ qua test để che lỗi.

## Một lệnh kiểm tra trước khi push

Từ thư mục gốc, chạy:

```bash
python3 scripts/verify_vercel_ui.py
```

Cần Python 3.9+, Node.js và Chrome/Chromium đã có sẵn. Không dùng NPX, không cài thêm thư viện. Lệnh dừng khi test lỗi, hết thời gian hoặc thiếu trình duyệt; không coi test bị bỏ qua là đạt. Bản dựng `_site/` cũng được kiểm tra budget Vercel.

| Nhóm | Kiểm tra tự động |
| --- | --- |
| Thiết kế | Token màu sáng/tối, font thực tế, hero còn hiển thị, thứ tự và khoảng cách tới tìm kiếm; có chèn lỗi giả để chứng minh bộ kiểm tra phát hiện được |
| Responsive | Trang chủ và tất cả bài trong danh sách Blog ở 320/390/768/1024/1440 px, tiếng Việt/Anh; không tràn ngang, nút điều hướng không đè nhau |
| Tìm kiếm/bộ lọc | Tìm mô tả tiếng Việt, loading/error/retry, bộ lọc điện thoại mở trước khi dữ liệu tải xong, empty state |
| Cài skill | Đúng agent/thư mục, đổi agent/ngôn ngữ trong lúc copy không đổi prompt đang chờ, manifest không hợp lệ và lỗi clipboard có hướng xử lý |
| Runbook | Render Markdown, link an toàn, fragment mở trực tiếp/reload, Back/Forward giữ vị trí và focus |
| Blog | HTML tĩnh, metadata/canonical/schema, đường về thư viện, liên kết skill, giữ ngôn ngữ/agent, đọc được ở sáng/tối |
| Bàn phím/chuyển động | Hành vi Ctrl/Cmd+K và `/`, không chiếm phím khi đang nhập, Escape đóng menu và trả focus, reduced motion không giấu nội dung |

Lệnh này chạy các test catalog, contract giao diện, build, Blog và trình duyệt. Các test copy kiểm tra nội dung/hành vi qua môi trường giả lập; quyền clipboard thực tế vẫn cần thử trên trình duyệt. Kiểm tra tự động không chứng nhận đầy đủ WCAG, chất lượng hình ảnh hay thứ hạng SEO.

Với bài Blog mới, thêm bài vào danh sách Blog và sitemap, giữ canonical riêng và link đúng skill. Đưa các tệp dự định phát hành vào staging trước lần kiểm tra cuối. Bộ kiểm tra số trang dùng danh sách tệp Git để phát hiện bài bị bỏ sót; bản nháp chưa theo dõi của tác vụ khác không được tính vào lần phát hành này.

## Xem trực tiếp khi đổi giao diện

Phục vụ từ thư mục gốc để liên kết runbook hoạt động:

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Mở `http://127.0.0.1:8765/_site/` sau khi kiểm tra xong. So sánh trước/sau ở 1440×900 và 390×844, tiếng Việt/Anh, sáng/tối. Cuộn qua các phần để hiệu ứng reveal hoàn tất trước khi chụp toàn trang.

1. Hero còn đúng màu, chữ, reel chọn agent và chuyển động; đổi theme bằng nút thật không kẹt, nháy hoặc làm mất nội dung. Test headless dùng đường xử lý khi thiếu View Transition API vì đồng hồ ảo không mô phỏng compositor; cần xem chuyển cảnh native trực tiếp.
2. Dùng Tab/Shift+Tab đến tìm kiếm, bộ lọc, kết quả, Blog và nút copy; focus phải rõ, không bị header che. Thử Ctrl/Cmd+K, `/`, Enter và Escape bằng bàn phím thật. Test sự kiện tổng hợp không thay thế được thứ tự Tab thực tế.
3. Trên điện thoại, mở/đóng menu và bộ lọc, chọn agent, đổi ngôn ngữ; không đè nút, mất chữ, cuộn ngang hoặc khóa cuộn sau khi đóng.
4. Mở skill → mục runbook → Blog → thư viện; thử Back/Forward, reload và mở link trong tab mới. Vị trí đọc, fragment và agent/ngôn ngữ phải đúng.
5. Copy prompt với ít nhất Codex và Claude, thử môi trường cho phép/từ chối clipboard; prompt hoặc ô sao chép thủ công phải đúng lựa chọn khi bấm.
6. Bật “Reduce motion”, reload: nội dung vẫn hiện và dùng được, hiệu ứng trang trí đứng yên. Với thay đổi CSS/điều hướng, xem thêm Safari/WebKit và một thiết bị cảm ứng thực nếu có; ghi rõ môi trường chưa thử.

## Trước và sau khi phát hành

- Xem diff của staging/commit; không đưa thay đổi ngoài phạm vi hoặc bản nháp của tác vụ khác vào bản phát hành. Kiểm tra lại candidate cuối nếu mã thay đổi sau lần test.
- Chạy toàn bộ test dự án nếu thay đổi CLI/catalog/dữ liệu. Giữ budget Vercel; không khôi phục workflow Pages.
- `vercel.json` chạy test nhanh catalog/contract trước build; lỗi các test này chặn build. Browser test đầy đủ chạy local và GitHub CI. Kết nối GitHub–Vercel hiện không tự đợi GitHub CI; phải kiểm tra local trước khi push production.
- Sau push, đối chiếu SHA commit với CI và Vercel. Kiểm tra website công khai, một trang Blog, runbook và manifest cài đặt của đúng revision. Chỉ báo hoàn tất với các phần đã xác nhận; nêu phần còn thiếu nếu bị chặn.
