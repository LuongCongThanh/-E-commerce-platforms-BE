# E-Commerce Platform — Tổng quan chức năng

> Tài liệu này mô tả các chức năng chuẩn của một nền tảng thương mại điện tử,
> phân theo nhóm đối tượng sử dụng và mức độ ưu tiên triển khai.

---

## 1. Chức năng phía Khách hàng (Customer-facing)

### 1.1 Tài khoản & Xác thực

- Đăng ký, đăng nhập, đăng xuất
- Đăng nhập mạng xã hội (Google, Facebook)
- Quên mật khẩu / Đặt lại mật khẩu qua email
- Hồ sơ cá nhân: avatar, họ tên, số điện thoại
- Quản lý địa chỉ giao hàng (nhiều địa chỉ)
- Lịch sử mua hàng

### 1.2 Duyệt & Tìm kiếm sản phẩm

- Trang chủ: banner, sản phẩm nổi bật, flash sale
- Danh mục sản phẩm (có phân cấp cha/con)
- Tìm kiếm theo từ khóa (full-text search)
- Lọc sản phẩm: giá, thương hiệu, kích cỡ, màu sắc, đánh giá sao
- Sắp xếp: mới nhất, bán chạy, giá tăng/giảm
- Trang chi tiết sản phẩm: ảnh, mô tả, biến thể, tồn kho

### 1.3 Giỏ hàng (Shopping Cart)

- Thêm / xóa / cập nhật số lượng sản phẩm
- Lưu giỏ hàng khi chưa thanh toán (persistent cart)
- Hiển thị tổng tiền, phí vận chuyển tạm tính
- Áp dụng mã giảm giá / voucher

### 1.4 Thanh toán (Checkout & Payment)

- Chọn địa chỉ giao hàng
- Chọn đơn vị vận chuyển (tính phí tự động)
- Phương thức thanh toán:
  - COD (tiền mặt khi nhận)
  - VNPAY / Momo / ZaloPay
  - Thẻ tín dụng / Thẻ ATM nội địa
  - Chuyển khoản ngân hàng
- Trang xác nhận đơn hàng + gửi email thông báo

### 1.5 Quản lý đơn hàng

- Xem danh sách & chi tiết đơn hàng
- Theo dõi trạng thái đơn theo thời gian thực
- Hủy đơn hàng (trong thời gian cho phép)
- Yêu cầu đổi trả / hoàn tiền

### 1.6 Đánh giá & Tương tác

- Đánh giá sao + viết nhận xét sản phẩm
- Upload ảnh / video đánh giá
- Like / dislike nhận xét của người khác
- Danh sách yêu thích (Wishlist)

### 1.7 Hỗ trợ khách hàng

- Live chat hoặc chatbot
- Trang FAQ
- Form liên hệ / gửi ticket hỗ trợ

---

## 2. Chức năng phía Quản trị & Người bán (Admin / Seller-facing)

### 2.1 Quản lý sản phẩm

- Thêm / sửa / xóa sản phẩm
- Quản lý biến thể (size, màu, chất liệu…)
- Upload ảnh sản phẩm (hỗ trợ nhiều ảnh)
- Quản lý giá gốc, giá khuyến mãi, giá vốn
- Tối ưu SEO (meta title, description, slug)
- Trạng thái sản phẩm: hiển thị / ẩn / hết hàng

### 2.2 Quản lý kho hàng (Inventory)

- Theo dõi số lượng tồn kho theo từng biến thể
- Cảnh báo sắp hết hàng (threshold alert)
- Lịch sử nhập / xuất kho
- Đồng bộ kho nhiều kênh bán (nếu có)

### 2.3 Quản lý đơn hàng

- Xem danh sách đơn hàng, lọc theo trạng thái
- Xác nhận / từ chối đơn hàng
- Cập nhật trạng thái: `Chờ xử lý → Đã xác nhận → Đang giao → Hoàn thành → Đã hủy`
- In hóa đơn / phiếu giao hàng (PDF)
- Tạo đơn hàng thủ công (offline order)

### 2.4 Quản lý khách hàng

- Xem danh sách khách hàng, thông tin cá nhân
- Lịch sử mua hàng, tổng chi tiêu
- Phân khúc khách hàng (VIP, thường, mới)
- Ghi chú nội bộ về khách hàng

### 2.5 Tích hợp vận chuyển

- Kết nối đơn vị vận chuyển: GHN, GHTK, J&T, Viettel Post, Grab Express
- Tính phí vận chuyển tự động theo địa chỉ & khối lượng
- Tạo đơn vận chuyển, in vận đơn
- Theo dõi trạng thái vận chuyển realtime

### 2.6 Khuyến mãi & Marketing

- Tạo mã giảm giá (coupon): theo %, theo số tiền, theo sản phẩm
- Flash sale theo khung giờ
- Chương trình tích điểm / đổi điểm
- Upsell / Cross-sell (gợi ý sản phẩm liên quan)
- Email marketing / SMS marketing tự động

### 2.7 Báo cáo & Phân tích

- Doanh thu theo ngày / tuần / tháng / năm
- Biểu đồ đơn hàng (tổng số, hoàn thành, hủy)
- Sản phẩm bán chạy nhất
- Khách hàng mới vs khách hàng quay lại
- Báo cáo tồn kho
- Xuất báo cáo ra Excel / PDF

### 2.8 Quản trị hệ thống

- Quản lý tài khoản admin, phân quyền theo vai trò (RBAC)
- Cấu hình phí vận chuyển, thuế
- Cài đặt chính sách đổi trả, bảo hành
- Cấu hình thông tin cửa hàng, logo, favicon
- Quản lý banner / slider trang chủ

---

## 3. Chức năng nâng cao (dành cho giai đoạn mở rộng)

| Tính năng               | Mô tả                                                                      |
| ----------------------- | -------------------------------------------------------------------------- |
| **Omnichannel**         | Bán đồng thời: Website + App + Facebook Shop + TikTok Shop + Shopee/Lazada |
| **Mobile App**          | iOS/Android native hoặc PWA                                                |
| **AI Gợi ý**            | Recommend sản phẩm theo hành vi người dùng                                 |
| **AI Chatbot**          | Hỗ trợ khách hàng tự động 24/7                                             |
| **Dự báo kho**          | Dự báo nhu cầu nhập hàng dựa trên lịch sử bán                              |
| **Multi-vendor**        | Nhiều người bán trên cùng một nền tảng (mô hình marketplace)               |
| **Livestream bán hàng** | Tích hợp live shopping                                                     |
| **Subscription**        | Mô hình đăng ký định kỳ                                                    |

---

## 4. Yêu cầu phi chức năng (Non-functional Requirements)

### Bảo mật

- HTTPS / SSL bắt buộc toàn site
- Xác thực 2 yếu tố (2FA) cho admin
- Mã hóa thông tin thanh toán (PCI-DSS nếu cần)
- Bảo vệ dữ liệu cá nhân (tuân thủ Nghị định 13/2023/NĐ-CP Việt Nam)
- Chống DDoS, rate limiting API
- SQL Injection / XSS / CSRF protection

### Hiệu năng

- Thời gian load trang < 3 giây (LCP)
- Hỗ trợ ít nhất 500 người dùng đồng thời (MVP)
- CDN cho ảnh và static assets
- Database indexing đúng cách

### Khả năng mở rộng

- Kiến trúc tách biệt Frontend / Backend (API-first)
- Thiết kế database có thể scale
- Stateless API (dễ horizontal scaling)

### SEO & Analytics

- Server-side rendering (SSR) cho trang sản phẩm
- Sitemap XML tự động
- Open Graph / Twitter Card
- Tích hợp Google Analytics 4, Google Search Console
- Facebook Pixel, Google Tag Manager

---

## 5. Tám chức năng cốt lõi — phân theo giai đoạn

> **Ghi chú:** Không phải tất cả đều có ở MVP tháng đầu.
> Xem phạm vi cụ thể tại [mvp-plan.md](./mvp-plan.md).

| #   | Chức năng             | MVP (tháng 1)                | Phase 2              | Lý do cốt lõi                            |
| --- | --------------------- | ---------------------------- | -------------------- | ---------------------------------------- |
| 1   | Quản lý sản phẩm      | ✅ Django Admin              | Custom FE admin      | Không có sản phẩm thì không có gì để bán |
| 2   | Giỏ hàng & Thanh toán | ✅ Giỏ hàng + COD            | VNPAY / Momo / Zalo  | Dòng tiền chính của toàn hệ thống        |
| 3   | Quản lý đơn hàng      | ✅ Django Admin + email      | Dashboard riêng      | Xử lý nghiệp vụ sau khi mua              |
| 4   | Quản lý kho           | ✅ Tồn kho theo variant      | Cảnh báo & dự báo    | Tránh bán hàng không có sẵn              |
| 5   | Tích hợp vận chuyển   | ⏳ Phí ship cố định          | GHN / GHTK realtime  | Giao hàng đến tay khách                  |
| 6   | Tìm kiếm & Lọc        | ✅ Full-text + filter cơ bản | Elasticsearch        | Khách cần tìm được thứ muốn mua          |
| 7   | Đánh giá khách hàng   | ⏳ Phase 2                   | Rating + review      | Xây dựng uy tín và trust                 |
| 8   | Báo cáo doanh thu     | ⏳ Admin dashboard đơn giản  | Biểu đồ + xuất Excel | Theo dõi hiệu quả kinh doanh             |

> ✅ Có trong MVP &nbsp;|&nbsp; ⏳ Phiên bản tối giản hoặc Phase 2

---

## 6. So sánh nền tảng có sẵn vs tự xây dựng

| Tiêu chí              | Nền tảng có sẵn (Shopify, Haravan, Sapo) | Tự xây dựng (Custom)            |
| --------------------- | ---------------------------------------- | ------------------------------- |
| **Thời gian ra mắt**  | 1–7 ngày                                 | 1–6 tháng                       |
| **Chi phí ban đầu**   | Thấp (subscription)                      | Cao (dev cost)                  |
| **Chi phí dài hạn**   | Cao (phí hàng tháng + app)               | Thấp (tự kiểm soát)             |
| **Tùy biến**          | Hạn chế theo template                    | Toàn quyền                      |
| **Kiểm soát dữ liệu** | Phụ thuộc vendor                         | Hoàn toàn tự chủ                |
| **Khả năng mở rộng**  | Giới hạn bởi platform                    | Không giới hạn                  |
| **Phù hợp với**       | Kinh doanh nhanh, ít kỹ thuật            | Sản phẩm tech, cần tùy biến sâu |

> **Gợi ý:** Nếu mục tiêu là bán hàng nhanh → dùng nền tảng có sẵn.
> Nếu mục tiêu là xây dựng sản phẩm tech / học / kiểm soát hoàn toàn → tự xây.

---

_Xem kế hoạch triển khai chi tiết tại: [mvp-plan.md](./mvp-plan.md)_
