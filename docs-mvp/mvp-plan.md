# MVP E-Commerce — Kế hoạch triển khai 4 tuần (Solo Developer)

> **Mục tiêu:** Cuối tháng 4/2026 có website bán hàng thật, khách vào mua được,
> thanh toán được, đơn hàng hiển thị trong Admin.

---

## Đánh giá khả thi

**Có thể làm trong 1 tháng không?**

**Được — nhưng chỉ MVP cơ bản, không phải full e-commerce.**

| Điều kiện                                      | Kết quả           |
| ---------------------------------------------- | ----------------- |
| Đã biết cả Django lẫn Next.js + code full-time | Xong trong 4 tuần |
| Biết một trong hai + code full-time            | Cần 6 tuần        |
| Vừa học vừa làm                                | Cần 8–10 tuần     |

> Nếu muốn full chức năng (khuyến mãi, review, tích hợp GHN/GHTK thật,
> báo cáo đẹp, wishlist, multi-vendor…) → cần **3–4 tháng**.

---

## Tech Stack

### Stack được chọn (tối ưu cho solo 1 tháng)

| Layer              | Công nghệ                              | Lý do chọn                                     |
| ------------------ | -------------------------------------- | ---------------------------------------------- |
| **Frontend**       | Next.js 15 (App Router) + TypeScript   | SSR sẵn, SEO tốt, ecosystem lớn                |
| **UI Components**  | Tailwind CSS + Shadcn/ui               | Build nhanh, không cần design từ đầu           |
| **Data Fetching**  | TanStack Query v5                      | Cache + sync server state chuẩn nhất           |
| **Tables**         | TanStack Table                         | Bảng dữ liệu admin phức tạp                    |
| **Forms**          | React Hook Form + Zod                  | Validation type-safe, ít boilerplate           |
| **State (client)** | Zustand                                | Giỏ hàng, UI state nhẹ nhàng                   |
| **Backend**        | Django 5.1 + Django REST Framework     | Admin panel sẵn → tiết kiệm 60–70% thời gian   |
| **Database**       | PostgreSQL (Neon — managed, free tier) | Không cần cài local, có dashboard              |
| **Auth**           | django-allauth + SimpleJWT             | Social login Google/Facebook, refresh token    |
| **Payment**        | COD (tiền mặt khi nhận hàng)           | Không cần bên thứ ba — Phase 2 thêm VNPAY/Momo |
| **Media Storage**  | Cloudinary (free 25GB)                 | CDN sẵn, resize ảnh auto, không cần tự host    |
| **Email**          | Django SMTP (Gmail / Mailgun free)     | Gửi xác nhận đơn hàng                          |
| **Testing**        | pytest-django + Playwright             | Unit test backend, E2E test luồng mua hàng     |
| **Monitoring**     | Sentry (free tier)                     | Bắt lỗi production realtime                    |
| **Deployment FE**  | Vercel                                 | 1-click deploy, CI/CD tích hợp sẵn             |
| **Deployment BE**  | Railway                                | Docker support, free $5 credit/tháng           |
| **Local Dev**      | Docker Compose                         | 1 lệnh chạy toàn bộ stack                      |
| **CI/CD**          | GitHub Actions                         | Auto test + deploy khi push                    |

### Tại sao KHÔNG dùng một số thứ ở MVP

| Bỏ qua        | Lý do                                                          |
| ------------- | -------------------------------------------------------------- |
| Redis         | Tiết kiệm 3–4 ngày setup. Thêm vào Phase 2 khi cần cache/queue |
| Elasticsearch | PostgreSQL full-text search đủ dùng cho MVP < 10.000 sản phẩm  |
| Celery        | Chưa cần async task queue ở MVP                                |
| Kubernetes    | Overkill cho 1 developer, 1 project nhỏ                        |

---

## MVP Scope — Chỉ làm những cái này

### Phía khách hàng

- [ ] Đăng ký / Đăng nhập / Quên mật khẩu
- [ ] Trang chủ + Danh mục + Tìm kiếm + Lọc cơ bản
- [ ] Trang chi tiết sản phẩm (SSR + SEO)
- [ ] Giỏ hàng (add / remove / update) — lưu localStorage, mất khi đổi thiết bị
- [ ] Checkout + Thanh toán COD
- [ ] Trang xác nhận đơn + Email thông báo
- [ ] Xem đơn hàng của mình

### Phía quản trị

- [ ] Django Admin: quản lý sản phẩm, đơn hàng, khách hàng
- [ ] Cập nhật trạng thái đơn hàng (bulk action)

### Kỹ thuật

- [ ] Responsive + Mobile-first
- [ ] Basic SEO (metadata, sitemap, Open Graph)
- [ ] Docker Compose cho local dev
- [ ] Deploy lên Vercel + Railway
- [ ] Error handling nhất quán (API errors → toast, crash → error boundary)

### Phase 2 (sau MVP — không làm ngay)

> Ghi vào đây, không động vào trong tháng này:

- Tích hợp VNPAY / Momo / ZaloPay
- Đánh giá sản phẩm (reviews)
- Mã giảm giá / voucher
- Flash sale
- Wishlist
- Tích hợp GHN/GHTK thật
- Báo cáo doanh thu
- Social login (Google/Facebook)
- Redis cache
- Thông báo realtime (WebSocket)

---

## Kế hoạch 4 tuần chi tiết

### Tuần 1 — Setup & Backend Core (Ngày 1–7)

**Ngày 1–2: Project Setup**

- Tạo GitHub repo, cấu trúc thư mục `frontend/` + `backend/`
- Viết `docker-compose.yml`: Django + PostgreSQL + Next.js
- Setup `.env` template (không commit file `.env` thật)
- Tạo Django project + DRF install
- Tạo Next.js 15 project với TypeScript + Tailwind + Shadcn

**Ngày 3–4: Database Models**

```
User (extend AbstractUser)
├── Category
├── Product
│   └── ProductVariant (size, color, stock, price)
│   └── ProductImage
├── Order
│   └── OrderItem
├── ShippingAddress
└── Payment
```

**Ngày 5–6: Django Admin + API**

- Đăng ký models vào Django Admin (tùy chỉnh list_display, search_fields)
- DRF serializers cho Product, Category
- API endpoints: `GET /api/products/`, `GET /api/products/:slug/`, `GET /api/categories/`
- Swagger / ReDoc tự động qua `drf-spectacular`

**Ngày 7: Auth + Deploy Backend**

- Cài django-allauth + SimpleJWT
- API: register, login, refresh token, profile
- Deploy Django lên Railway
- Test API bằng Swagger UI trên production

**Gate cuối Tuần 1 — không chuyển sang Tuần 2 nếu chưa đạt:**

- [ ] Swagger UI trên production URL trả đúng dữ liệu
- [ ] `POST /api/auth/register/` + `login/` hoạt động trên production
- [ ] `GET /api/products/` trả danh sách (dù chỉ 1–2 sản phẩm test)
- [ ] Docker Compose local chạy được 3 services không lỗi

**API Contract (cuối Tuần 1, trước khi FE bắt đầu):**

Ghi lại response shape chính xác của các endpoint FE sẽ dùng:

```yaml
GET /api/products/        → { results: Product[], count, next, previous }
GET /api/products/:slug/  → Product { id, name, slug, images, variants, price }
POST /api/orders/         → Order { id, status, total }
GET /api/orders/          → { results: Order[] }
POST /api/auth/register/  → { access, refresh, user }
POST /api/auth/login/     → { access, refresh, user }
```

FE không bắt đầu viết code gọi API nếu contract chưa được confirm.

---

### Tuần 2 — Frontend + Kết nối API (Ngày 8–14)

**Ngày 8–9: Frontend Foundation**

- Setup TanStack Query, Zustand, React Hook Form, Zod
- Cấu hình API client (axios hoặc fetch wrapper với interceptor JWT)
- Layout chung: Header (navbar, giỏ hàng icon), Footer
- Setup Cloudinary cho ảnh sản phẩm

**Ngày 10–11: Trang sản phẩm**

- Trang chủ: banner tĩnh + product grid
- Trang danh mục + lọc (filter sidebar)
- Trang chi tiết sản phẩm (SSR với `generateMetadata`)
- Tối ưu ảnh: `next/image` + Cloudinary URL transforms

**Ngày 12–13: Giỏ hàng**

- Zustand store cho cart (persist qua localStorage)
- Cart drawer / Cart page
- Add to cart, update quantity, remove item
- Tính tổng tiền client-side

**Ngày 14: Auth Frontend + Kết nối hoàn chỉnh**

- Trang đăng ký / đăng nhập / quên mật khẩu
- Protected routes (middleware Next.js)
- Responsive test trên mobile (Chrome DevTools + thật nếu có)

---

### Tuần 3 — Checkout & Thanh toán (Ngày 15–21)

**Ngày 15–17: Checkout Flow**

- Checkout page với React Hook Form + Zod:
  - Bước 1: Địa chỉ giao hàng
  - Bước 2: Phương thức thanh toán (COD)
  - Bước 3: Xác nhận đơn
- API tạo đơn hàng (`POST /api/orders/`) với atomic transaction:

  ```python
  from django.db import transaction

  with transaction.atomic():
      variant = ProductVariant.objects.select_for_update().get(pk=variant_id)
      if variant.stock_quantity < quantity:
          raise ValidationError("Sản phẩm vừa hết hàng")
      variant.stock_quantity -= quantity
      variant.save()
  ```

- Error handling: retry logic cho DB timeout, rollback tồn kho khi lỗi

**Ngày 18–19: Order Confirmation + Email**

- Trang `/orders/:id` — chi tiết đơn hàng
- Gửi email xác nhận đơn qua Django (HTML template)
- Trang lịch sử đơn hàng của khách (`/account/orders`)
- Error boundary cho checkout page — hiển thị lỗi thân thiện thay vì crash

**Ngày 20–21: COD Flow hoàn chỉnh + Django Admin nâng cao**

- Luồng COD: tạo order → status `PENDING` → redirect trang success → gửi email
- Trang `/checkout/success` và `/checkout/failed`
- Custom action trong Admin: xác nhận / đánh dấu đang giao / hủy đơn hàng hàng loạt
- Dashboard đơn giản trong Admin: đơn hôm nay, doanh thu hôm nay, sản phẩm sắp hết hàng

**Gate cuối Tuần 3 — không chuyển sang Tuần 4 nếu chưa đạt:**

- [ ] Luồng COD end-to-end chạy thông suốt (đặt hàng → email → xem đơn)
- [ ] Email xác nhận gửi được thật (không chỉ log)
- [ ] Admin có thể cập nhật trạng thái đơn hàng
- [ ] Không có lỗi 500 trong Sentry sau khi test

---

### Tuần 4 — Polish, Test & Deploy (Ngày 22–30)

**Ngày 22–24: Testing**

- **Backend (pytest-django):**
  - Test tạo đơn hàng COD (happy path + edge cases)
  - Test kiểm tra tồn kho + race condition (`select_for_update`)
  - Test hủy đơn → rollback tồn kho đúng số lượng
  - Test auth: register, login, refresh token, logout blacklist
- **Frontend E2E (Playwright):**
  - Luồng: vào web → tìm sản phẩm → thêm giỏ → checkout COD → nhận email
  - Luồng: đăng ký tài khoản mới → đăng nhập → xem lịch sử đơn

**Ngày 25–26: SEO & Performance**

- `generateMetadata()` cho tất cả trang sản phẩm / danh mục
- `sitemap.ts` tự động generate từ database
- Open Graph tags (chia sẻ Facebook/Zalo đẹp)
- `next/image` lazy loading cho tất cả ảnh
- Lighthouse score > 80 (mobile)

**Ngày 27–28: Production Deploy**

- Setup biến môi trường production (Vercel + Railway)
- GitHub Actions: test → build → deploy tự động khi push `main`
- Cài domain + SSL (Vercel tự xử lý SSL)
- Sentry DSN cấu hình cho cả FE lẫn BE
- Test end-to-end toàn bộ luồng COD trên production (điện thoại thật)

**Ngày 29–30: Final Check & Launch**

- Test toàn bộ luồng mua hàng trên production (điện thoại thật)
- Fix bug phát sinh
- Nhập 10–20 sản phẩm thật vào Django Admin
- Viết `README.md` (setup local, deploy guide)
- Announce / share link

---

## Milestone cuối tháng

```
✅ Website live trên domain thật
✅ Khách vào → tìm sản phẩm → thêm giỏ → đặt hàng COD
✅ Đơn hàng xuất hiện trong Django Admin
✅ Khách nhận email xác nhận
✅ Bạn có thể bán 10–20 sản phẩm thật ngay tuần đầu
```

---

## Chi phí ước tính

| Dịch vụ       | Gói                      | Chi phí/tháng          |
| ------------- | ------------------------ | ---------------------- |
| Vercel        | Hobby (Free)             | $0                     |
| Railway       | Starter                  | ~$5                    |
| Neon Postgres | Free tier (0.5 GB)       | $0                     |
| Cloudinary    | Free (25 GB, 25 credits) | $0                     |
| Sentry        | Free (5K errors/tháng)   | $0                     |
| Domain (.com) | —                        | ~$1.2/tháng (~$15/năm) |
| **Tổng**      |                          | **~$6–7/tháng**        |

> Khi traffic tăng: nâng Railway lên $20/tháng, Neon lên $19/tháng là đủ cho vài nghìn đơn/ngày.

---

## Security Checklist (trước khi go-live)

### Django Backend

- [ ] `DEBUG = False` trên production
- [ ] `SECRET_KEY` lưu trong biến môi trường, không hardcode
- [ ] `ALLOWED_HOSTS` chỉ cho phép domain thật
- [ ] CORS chỉ cho phép domain frontend
- [ ] DRF throttling: `AnonRateThrottle` (100/day), `UserRateThrottle` (1000/day)
- [ ] HTTPS redirect (`SECURE_SSL_REDIRECT = True`)
- [ ] CSRF protection bật (mặc định trong Django)
- [ ] Không expose Django Admin ở URL mặc định `/admin/` → đổi thành `/secret-panel/`

### Next.js Frontend

- [ ] Không để API keys trong code client-side
- [ ] `Content-Security-Policy` header cơ bản
- [ ] Sanitize input trước khi render (tránh XSS)

### Database

- [ ] Backup tự động trên Neon (bật trong dashboard)
- [ ] Không dùng `root` user để kết nối app

### COD / Payment

- [ ] Idempotency: không xử lý 1 đơn hàng 2 lần (check trạng thái trước khi confirm)
- [ ] Race condition: dùng `select_for_update()` khi trừ tồn kho

---

## Lời khuyên cho solo developer

1. **Scope creep là kẻ thù số 1** — Mỗi khi muốn thêm tính năng mới, ghi vào "Phase 2" và tiếp tục. Không làm thêm.

2. **Dùng AI để tăng tốc** — Cursor + Claude cho Shadcn components, DRF serializers, Playwright tests. Không cần viết boilerplate tay.

3. **Commit mỗi ngày** — `git push` mỗi tối. Không để mất 3 ngày công vì máy hỏng.

4. **Deploy sớm từ tuần 1** — Deploy backend lên Railway từ ngày 7, frontend từ ngày 14. Tránh "works on my machine" cuối tháng.

5. **Dùng Django Admin tối đa** — Đừng tốn thời gian build admin frontend riêng ở MVP. Django Admin tuy xấu nhưng đủ dùng để quản lý đơn hàng, sản phẩm trong giai đoạn đầu.

6. **Mobile-first từ đầu** — Hơn 70% khách mua hàng trên điện thoại ở Việt Nam. Test Tailwind responsive từng component khi xây.

---

_Xem tổng quan chức năng tại: [overview.md](./overview.md)_
