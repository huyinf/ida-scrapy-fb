# ida-scrapy-fb
Tutorial and How to craw comments from Facebook with Scrapy

---
## Timeline
- 9h sáng 28/04
  - Demo những gì đã làm được.
  - **Code cá nhân cho vào thư mục tên của mình và đẩy lên git.**
  - Làm theo người code tốt nhất
- (Update sau)
- 21h ngày 02/05
  - Soạn slide và hoàn thành project
- 12/05 nộp project trên moodle.

---
- 9h sáng 29/04
  - bot đã cào được toàn bộ bình luận của 1 bài viết nhưng do vi phạm tiêu chuẩn cộng đồng (server ko tiếp nhận kịp, giới hạn tốc độ tải) nên chỉ dùng lần đầu và bị chặn cho các lần sau.
  - **đề xuất giải pháp**
    - vẫn cố gắng cào hết, kèm theo cài đặt cho phù hợp tiêu chuẩn cộng đồng.
    - giới hạn số lần muốn cào cho 1 bài viết (ví dụ: bài viết có 500 bình luận, chia thành 50 trang, ta có thể giới hạn cào dưới 10 trang).
  - **cào nhiều bài viết**
    - thiết kế lại spider để lấy link các bài viết của fan page, gợi ý dùng mục **timeline**. Tui đã thử và bài viết chúaw video không thể xử lý do khi truy cập thì không hiện mục bình luận, nên tui đề xuất tạm bỏ qua video.