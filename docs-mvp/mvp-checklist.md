# MVP E-Commerce — Checklist Hoàn Chỉnh

> Đánh dấu `[x]` từng task khi hoàn thành.
> Không nhảy sang task tiếp theo nếu task hiện tại chưa xong và có dependency.

---

## TUẦN 1 — Setup & Backend Core (Ngày 1–7)

### Ngày 1 — Project Setup

#### Repository & Cấu trúc thư mục

- [ ] Tạo GitHub repository (private hoặc public)
- [ ] Tạo cấu trúc thư mục:
  ```
  e-commerce/
  ├── backend/        ← Django
  ├── frontend/       ← Next.js
  ├── docker-compose.yml
  ├── .env.example
  └── README.md
  ```
- [ ] Tạo `.gitignore` (Python + Node + môi trường)
- [ ] Tạo `.env.example` với tất cả biến cần thiết (không điền giá trị thật)
- [ ] Commit initial structure lên GitHub

#### Docker Compose

- [ ] Viết `docker-compose.yml` với 3 services: `db` (Postgres), `backend` (Django), `frontend` (Next.js)
- [ ] Test `docker compose up` chạy được không lỗi
- [ ] Verify các service kết nối được nhau (backend ping được db)

---

### Ngày 2 — Django Project Init

#### Cài đặt Django

- [ ] Tạo virtual environment (`python -m venv venv`)
- [ ] Cài đặt dependencies:
  ```
  django==5.1
  djangorestframework
  django-cors-headers
  django-environ
  psycopg2-binary
  Pillow
  drf-spectacular
  django-allauth
  djangorestframework-simplejwt
  django-cloudinary-storage
  cloudinary
  pytest-django
  factory-boy
  ```
- [ ] Tạo `requirements.txt` và `requirements-dev.txt`
- [ ] Khởi tạo Django project: `django-admin startproject config .`
- [ ] Tạo các apps: `accounts`, `products`, `orders`, `payments`
- [ ] Cấu hình `settings.py`:
  - [ ] `INSTALLED_APPS` đầy đủ
  - [ ] Database kết nối Neon Postgres qua biến môi trường
  - [ ] `CORS_ALLOWED_ORIGINS` cho Next.js local (`localhost:3000`)
  - [ ] `MEDIA_ROOT` + Cloudinary storage
  - [ ] `django-environ` đọc file `.env`
- [ ] Chạy `migrate` thành công
- [ ] Tạo superuser

#### Next.js Project Init

- [ ] Khởi tạo project: `npx create-next-app@latest frontend --typescript --tailwind --app`
- [ ] Cài đặt dependencies:
  ```
  @tanstack/react-query
  @tanstack/react-table
  react-hook-form
  @hookform/resolvers
  zod
  zustand
  axios
  shadcn-ui
  next-themes
  ```
- [ ] Khởi tạo Shadcn/ui: `npx shadcn@latest init`
- [ ] Cài các Shadcn components cần thiết: Button, Input, Card, Badge, Table, Dialog, Sheet, Form, Select, Skeleton, Toast

---

### Ngày 3 — Database Models

#### App: accounts

- [ ] Model `User` (extend `AbstractUser`):
  - `email` (unique, dùng làm username)
  - `phone_number`
  - `avatar` (Cloudinary field)
  - `is_verified`
- [ ] Model `ShippingAddress`:
  - `user` (FK)
  - `full_name`, `phone`, `address`, `ward`, `district`, `province`
  - `is_default`

#### App: products

- [ ] Model `Category`:
  - `name`, `slug`, `image`, `parent` (self FK — cho phép danh mục con)
  - `is_active`, `order`
- [ ] Model `Product`:
  - `name`, `slug`, `description` (TextField)
  - `category` (FK)
  - `base_price`, `sale_price`
  - `is_active`, `is_featured`
  - `meta_title`, `meta_description` (SEO)
  - `created_at`, `updated_at`
- [ ] Model `ProductImage`:
  - `product` (FK), `image` (Cloudinary), `alt_text`, `is_primary`, `order`
- [ ] Model `ProductVariant`:
  - `product` (FK)
  - `sku` (unique)
  - `size`, `color`
  - `stock_quantity`
  - `price_override` (nullable — override giá base nếu có)

#### App: orders

- [ ] Model `Order`:
  - `user` (FK, nullable — guest checkout để phase 2)
  - `status`: `PENDING / CONFIRMED / SHIPPING / COMPLETED / CANCELLED`
  - `shipping_address` (JSON snapshot — không FK vì địa chỉ có thể thay đổi)
  - `subtotal`, `shipping_fee`, `total`
  - `note`
  - `created_at`, `updated_at`
- [ ] Model `OrderItem`:
  - `order` (FK), `product_variant` (FK)
  - `product_name`, `variant_name` (snapshot tên tại thời điểm mua)
  - `quantity`, `unit_price`

#### App: payments

- [ ] Model `Payment`:
  - `order` (OneToOne FK)
  - `method`: `COD` (MVP) — thiết kế để dễ thêm `VNPAY / MOMO` ở Phase 2
  - `status`: `PENDING / CONFIRMED / CANCELLED / REFUNDED`
  - `amount`
  - `confirmed_at`
  - `note` (ghi chú nội bộ)

- [ ] Viết và chạy migrations cho tất cả models
- [ ] Verify schema trong database (dùng pgAdmin hoặc `dbshell`)

#### Database Indexes (tạo ngay khi migrate)

- [ ] `Product.slug` — unique index (dùng cho SSR trang chi tiết)
- [ ] `Order.user_id + created_at` — composite index (trang lịch sử đơn hàng)
- [ ] `ProductVariant.product_id` — FK index (query biến thể theo sản phẩm)
- [ ] `OrderItem.order_id` — FK index (load items theo đơn)
- [ ] `Category.slug` — unique index (dùng cho trang danh mục)

---

### Ngày 4 — Django Admin

- [ ] Đăng ký `User`, `ShippingAddress` vào admin (`accounts/admin.py`)
- [ ] Đăng ký `Category`, `Product`, `ProductImage`, `ProductVariant` vào admin
  - [ ] `list_display` hiển thị cột hữu ích
  - [ ] `list_filter` theo danh mục, trạng thái
  - [ ] `search_fields` theo tên, SKU
  - [ ] `prepopulated_fields` cho `slug` từ `name`
  - [ ] Inline cho `ProductImage` và `ProductVariant` trong `ProductAdmin`
- [ ] Đăng ký `Order`, `OrderItem` vào admin
  - [ ] `list_display`: mã đơn, khách hàng, tổng tiền, trạng thái, ngày tạo
  - [ ] `list_filter` theo status, ngày
  - [ ] Inline `OrderItem` trong `OrderAdmin`
- [ ] Đăng ký `Payment` vào admin
- [ ] Test nhập thử 2–3 sản phẩm qua Django Admin
- [ ] Đổi URL admin từ `/admin/` sang `/manage/` (bảo mật)

---

### Ngày 5 — DRF Serializers & API Products

- [ ] Serializer: `CategorySerializer` (nested children nếu cần)
- [ ] Serializer: `ProductImageSerializer`
- [ ] Serializer: `ProductVariantSerializer`
- [ ] Serializer: `ProductListSerializer` (ít field — dùng cho danh sách)
- [ ] Serializer: `ProductDetailSerializer` (đầy đủ — dùng cho trang chi tiết)
- [ ] ViewSet: `CategoryViewSet` (list, retrieve)
- [ ] ViewSet: `ProductViewSet` (list, retrieve by slug)
  - [ ] Filter: theo `category`, `min_price`, `max_price`, `is_featured`
  - [ ] Search: theo `name`, `description` (PostgreSQL icontains)
  - [ ] Ordering: `price`, `created_at`, `name`
  - [ ] Pagination: 20 items/page
- [ ] Cấu hình `drf-spectacular` để auto-generate Swagger UI
- [ ] Test API bằng Swagger: `GET /api/products/`, `GET /api/products/{slug}/`

---

### Ngày 6 — Auth API

- [ ] Cấu hình `django-allauth` + `SimpleJWT`
- [ ] API endpoint: `POST /api/auth/register/` (email + password)
  - [ ] Validate email unique
  - [ ] Hash password
  - [ ] Trả về access + refresh token
- [ ] API endpoint: `POST /api/auth/login/`
- [ ] API endpoint: `POST /api/auth/token/refresh/`
- [ ] API endpoint: `POST /api/auth/logout/` (blacklist refresh token)
- [ ] API endpoint: `POST /api/auth/password/reset/` (gửi email)
- [ ] API endpoint: `POST /api/auth/password/reset/confirm/`
- [ ] API endpoint: `GET/PATCH /api/auth/profile/` (protected)
- [ ] API endpoint: `GET/POST/DELETE /api/auth/addresses/` (protected)
- [ ] Middleware JWT authentication hoạt động đúng
- [ ] Test tất cả auth endpoints qua Swagger

---

### Ngày 7 — Deploy Backend

- [ ] Tạo tài khoản Neon Postgres, tạo database production
- [ ] Tạo tài khoản Railway, tạo project mới
- [ ] Tạo `Dockerfile` cho Django (production-ready):
  - [ ] Dùng `python:3.12-slim`
  - [ ] Chạy với `gunicorn`
  - [ ] Collect static files
- [ ] Cấu hình biến môi trường trên Railway (từ `.env.example`)
- [ ] Deploy lên Railway thành công
- [ ] Chạy `migrate` trên production
- [ ] Tạo superuser trên production
- [ ] Test Swagger UI trên URL production
- [ ] Test đăng ký + đăng nhập trên production API

#### Gate cuối Tuần 1 — không bắt đầu Tuần 2 nếu chưa đạt

- [ ] `GET /api/products/` trả đúng dữ liệu trên production URL
- [ ] `POST /api/auth/login/` trả access + refresh token
- [ ] Docker Compose local chạy 3 services không lỗi
- [ ] API Contract đã được ghi lại (response shape của 6 endpoints chính)

---

## TUẦN 2 — Frontend & Kết nối API (Ngày 8–14)

### Ngày 8 — Frontend Foundation

- [ ] Cấu hình `axios` instance với base URL + JWT interceptor:
  - Auto attach `Authorization: Bearer <token>` từ storage
  - Auto refresh token khi nhận 401
- [ ] Setup TanStack Query `QueryClientProvider` trong layout
- [ ] Setup Zustand store:
  - `authStore`: user info, token, login/logout actions
  - `cartStore`: items, add/remove/update, total, persist localStorage
- [ ] Cấu hình Cloudinary (URL builder helper function)
- [ ] Tạo shared components:
  - [ ] `<Navbar>` (logo, search bar, cart icon, auth menu)
  - [ ] `<Footer>`
  - [ ] `<ProductCard>` (ảnh, tên, giá, nút thêm giỏ)
  - [ ] `<PriceDisplay>` (giá gốc gạch ngang + giá sale)
  - [ ] `<LoadingSkeleton>` cho product grid
  - [ ] `<EmptyState>` (dùng nhiều chỗ)

---

### Ngày 9 — Trang chủ & Danh mục

- [ ] Trang chủ `/`:
  - [ ] Hero banner (static hoặc từ Admin)
  - [ ] Section "Danh mục nổi bật" (từ API)
  - [ ] Section "Sản phẩm nổi bật" (`is_featured=true`)
  - [ ] SSR với `fetch` trong `page.tsx`
- [ ] Trang danh mục `/categories/[slug]`:
  - [ ] Breadcrumb
  - [ ] Sidebar filter: khoảng giá (slider), sắp xếp
  - [ ] Product grid (responsive: 2 cột mobile, 3–4 cột desktop)
  - [ ] Pagination
  - [ ] URL params sync với filter (`?min_price=&max_price=&sort=`)
- [ ] Trang tìm kiếm `/search?q=`:
  - [ ] Hiển thị kết quả + số lượng tìm thấy
  - [ ] Empty state khi không có kết quả

---

### Ngày 10 — Trang chi tiết sản phẩm

- [ ] Route `/products/[slug]` với SSR
- [ ] `generateMetadata()` cho SEO (title, description, Open Graph image)
- [ ] Image gallery: ảnh chính + thumbnail list (click để đổi ảnh)
- [ ] Hiển thị biến thể: chọn size/màu (highlight biến thể đang chọn)
- [ ] Logic disable biến thể hết hàng
- [ ] Hiển thị tồn kho ("Còn X sản phẩm" khi < 10)
- [ ] Chọn số lượng (input có giới hạn tối đa = tồn kho)
- [ ] Nút "Thêm vào giỏ" + nút "Mua ngay" (→ thêm giỏ + redirect checkout)
- [ ] Section sản phẩm liên quan (cùng danh mục)
- [ ] `generateStaticParams()` cho các sản phẩm phổ biến (ISR)

---

### Ngày 11 — Trang Auth

- [ ] Trang `/auth/register`:
  - [ ] Form: email, password, confirm password, họ tên
  - [ ] Validation với Zod
  - [ ] Submit → gọi API → lưu token → redirect trang chủ
  - [ ] Hiển thị lỗi từ API (email đã tồn tại...)
- [ ] Trang `/auth/login`:
  - [ ] Form: email, password
  - [ ] "Nhớ đăng nhập" checkbox
  - [ ] Link quên mật khẩu
  - [ ] Redirect về trang trước khi bị redirect login (returnUrl)
- [ ] Trang `/auth/forgot-password`:
  - [ ] Form nhập email
  - [ ] Hiển thị thông báo "Kiểm tra email của bạn"
- [ ] Trang `/auth/reset-password/[token]`:
  - [ ] Form: mật khẩu mới + xác nhận
- [ ] Trang `/account/profile` (protected):
  - [ ] Xem + sửa thông tin cá nhân
  - [ ] Quản lý địa chỉ giao hàng (thêm / sửa / xóa / đặt mặc định)
- [ ] Middleware Next.js bảo vệ route `/account/*` và `/checkout`

---

### Ngày 12 — Giỏ hàng

- [ ] Cart Drawer (slide-in từ phải):
  - [ ] Danh sách sản phẩm trong giỏ
  - [ ] Thêm / giảm số lượng
  - [ ] Xóa sản phẩm
  - [ ] Tổng tiền tạm tính
  - [ ] Nút "Thanh toán"
- [ ] Trang `/cart` (full cart page):
  - [ ] Bảng giỏ hàng (responsive)
  - [ ] Order summary sidebar
  - [ ] Giữ nguyên giỏ hàng khi refresh (Zustand persist)
- [ ] Sync giỏ hàng với server (optional ở MVP — có thể để Phase 2)
- [ ] Hiển thị số lượng item trên cart icon ở Navbar

---

### Ngày 13 — Tích hợp API hoàn chỉnh

- [ ] Verify tất cả API calls dùng TanStack Query (không dùng useState + useEffect thuần)
- [ ] Error boundary cho các trang chính
- [ ] Toast notification cho: thêm giỏ hàng, lỗi API, đăng nhập thành công
- [ ] Loading states đầy đủ (Skeleton, spinner)
- [ ] 404 page cho sản phẩm / danh mục không tồn tại
- [ ] Test API với token hết hạn → auto refresh hoạt động đúng

---

### Ngày 14 — Responsive & Review Tuần 2

- [ ] Test responsive trên các breakpoint: 375px, 768px, 1024px, 1440px
- [ ] Fix layout broken trên mobile
- [ ] Test toàn bộ luồng: vào web → xem sản phẩm → thêm giỏ → xem giỏ
- [ ] Test luồng auth: đăng ký → đăng nhập → xem profile → đăng xuất
- [ ] Lighthouse audit trang chủ (target: > 70 mobile)
- [ ] Code review: xóa console.log, TODO cũ, code thừa
- [ ] Commit + push toàn bộ lên GitHub

#### Gate cuối Tuần 2 — không bắt đầu Tuần 3 nếu chưa đạt

- [ ] Luồng xem sản phẩm → thêm giỏ → xem giỏ chạy thông suốt
- [ ] Đăng ký / đăng nhập / đăng xuất hoạt động đúng
- [ ] JWT auto-refresh khi token hết hạn (test bằng cách set expiry ngắn)
- [ ] Không có lỗi TypeScript khi build (`tsc --noEmit` pass)

#### Acceptance Criteria mẫu — Auth

> - ✅ Đăng ký email mới → nhận token → redirect trang chủ
> - ✅ Đăng ký email đã tồn tại → hiển thị lỗi inline "Email đã được sử dụng"
> - ✅ Đăng nhập đúng → lưu token → redirect về trang trước đó
> - ✅ Đăng nhập sai mật khẩu → hiển thị lỗi, không redirect
> - ✅ Token hết hạn → auto refresh 1 lần → nếu refresh fail → redirect login

---

## TUẦN 3 — Checkout & Thanh toán (Ngày 15–21)

### Ngày 15 — Checkout API (Backend)

- [ ] API `GET /api/shipping/calculate/`:
  - Input: địa chỉ + danh sách sản phẩm (để tính phí)
  - Output: phí vận chuyển (hardcode hoặc tính theo tỉnh thành ở MVP)
- [ ] API `POST /api/orders/`:
  - Validate tồn kho từng sản phẩm (atomic transaction)
  - Trừ tồn kho ngay khi tạo đơn
  - Tạo `Order` + `OrderItem` + `Payment` (status PENDING)
  - Trả về order ID
- [ ] API `GET /api/orders/` (list đơn hàng của user hiện tại)
- [ ] API `GET /api/orders/{id}/` (chi tiết đơn — chỉ xem của mình)
- [ ] API `POST /api/orders/{id}/cancel/` (hủy đơn — chỉ khi PENDING)
- [ ] Xử lý race condition: 2 người cùng mua sản phẩm cuối cùng
  - Dùng `select_for_update()` + database transaction

---

### Ngày 16 — Checkout Frontend

- [ ] Trang `/checkout` (protected):
  - [ ] Bước 1 — Địa chỉ giao hàng:
    - [ ] Chọn địa chỉ đã lưu (nếu đã đăng nhập + có địa chỉ)
    - [ ] Form nhập địa chỉ mới (tên, SĐT, địa chỉ, phường/xã, quận/huyện, tỉnh/thành)
    - [ ] Tùy chọn lưu địa chỉ vào tài khoản
  - [ ] Bước 2 — Xem lại đơn hàng:
    - [ ] Danh sách sản phẩm (readonly)
    - [ ] Tóm tắt chi phí: tạm tính + phí vận chuyển + tổng
  - [ ] Bước 3 — Chọn thanh toán:
    - [ ] COD (MVP — duy nhất)
  - [ ] Nút "Đặt hàng" → gọi `POST /api/orders/`
- [ ] Validation toàn bộ form với Zod
- [ ] Hiển thị lỗi "hết hàng" nếu API trả về lỗi tồn kho
- [ ] Disable nút "Đặt hàng" sau khi submit (tránh double-submit)

---

### Ngày 17 — COD Flow + Error Handling

- [ ] Luồng COD hoàn chỉnh (backend):
  - [ ] `POST /api/orders/` tạo `Order` (PENDING) + `Payment` (method=COD, status=PENDING)
  - [ ] Atomic transaction + `select_for_update()` khi trừ tồn kho:

    ```python
    with transaction.atomic():
        variant = ProductVariant.objects.select_for_update().get(pk=variant_id)
        if variant.stock_quantity < quantity:
            raise ValidationError("Sản phẩm vừa hết hàng")
        variant.stock_quantity -= quantity
        variant.save()
    ```

  - [ ] Idempotency: kiểm tra đơn không bị tạo 2 lần nếu user submit liên tiếp

- [ ] Custom DRF exception handler — mọi lỗi đều trả JSON chuẩn:

  ```python
  # {"error": "...", "code": "out_of_stock", "status": 400}
  ```

- [ ] Phân biệt HTTP status: 400 validation, 401/403 auth, 404 not found, 409 conflict (hết hàng), 500 server
- [ ] Sentry tự động bắt lỗi 500 (cấu hình `sentry_sdk.init` trong Django settings)
- [ ] Test: 2 request đồng thời mua sản phẩm cuối → chỉ 1 thành công, 1 nhận lỗi 409

---

### Ngày 18 — COD Frontend + Trang xác nhận

- [ ] Trang `/checkout/success?orderId=`:
  - [ ] Fetch và hiển thị thông tin đơn hàng vừa đặt (tên, địa chỉ, tổng tiền)
  - [ ] Nút "Xem đơn hàng" và "Tiếp tục mua sắm"
  - [ ] Clear Zustand cart store sau khi đặt thành công
  - [ ] Redirect về trang chủ nếu vào URL này mà không có orderId
- [ ] Trang `/checkout/failed`:
  - [ ] Thông báo lỗi rõ ràng (hết hàng / lỗi server)
  - [ ] Nút "Thử lại" → quay về checkout
- [ ] Error boundary bọc toàn bộ checkout flow
- [ ] Toast notification cho lỗi API (network error, server error)

---

### Ngày 19 — Email & Quản lý đơn hàng

- [ ] Cấu hình Django email backend (Gmail SMTP hoặc Mailgun)
- [ ] HTML email template "Xác nhận đơn hàng":
  - Logo, tên khách hàng
  - Danh sách sản phẩm đã mua
  - Tổng tiền, địa chỉ giao hàng
  - Mã đơn hàng + link xem đơn
- [ ] Signal hoặc service gửi email khi Order status → CONFIRMED
- [ ] Trang `/account/orders` (protected):
  - [ ] Danh sách đơn hàng (sắp xếp theo ngày mới nhất)
  - [ ] Badge trạng thái đơn màu sắc khác nhau
  - [ ] Link xem chi tiết
- [ ] Trang `/account/orders/[id]` (protected):
  - [ ] Thông tin đơn hàng đầy đủ
  - [ ] Timeline trạng thái
  - [ ] Nút "Hủy đơn" (nếu đang PENDING)

---

### Ngày 20 — Django Admin nâng cao

- [ ] Custom action trong OrderAdmin: "Xác nhận đơn hàng đã chọn"
- [ ] Custom action: "Đánh dấu đang giao"
- [ ] Custom action: "Hủy đơn hàng đã chọn"
- [ ] Dashboard đơn giản trong Admin:
  - Số đơn hàng hôm nay
  - Doanh thu hôm nay
  - Sản phẩm sắp hết hàng (< 5)
- [ ] Thêm `list_select_related` để tránh N+1 queries
- [ ] Test toàn bộ Admin với 10+ sản phẩm và 5+ đơn hàng mẫu

---

### Ngày 21 — Review & Integration Test Tuần 3

- [ ] Test end-to-end luồng hoàn chỉnh (thủ công):
  1. Vào web → tìm sản phẩm → xem chi tiết
  2. Thêm vào giỏ → vào checkout
  3. Nhập địa chỉ → chọn COD → đặt hàng
  4. Quay về trang success → nhận email xác nhận
  5. Vào `/account/orders` xem đơn
  6. Admin xác nhận đơn → cập nhật trạng thái
- [ ] Test hủy đơn hàng → tồn kho hoàn lại đúng
- [ ] Verify không có N+1 query nghiêm trọng (Django Debug Toolbar)
- [ ] Commit + push

#### Gate cuối Tuần 3 — không bắt đầu Tuần 4 nếu chưa đạt

- [ ] Luồng COD end-to-end chạy thông suốt trên môi trường local
- [ ] Email xác nhận gửi được thật (không chỉ console log)
- [ ] Admin cập nhật được trạng thái đơn hàng
- [ ] Không có lỗi 500 nào trong Sentry sau khi chạy test thủ công

#### Acceptance Criteria mẫu — Checkout COD

> Dùng để xác nhận feature "done" trước khi chuyển sang Tuần 4:
>
> - ✅ Khách đăng nhập → vào checkout → điền địa chỉ → chọn COD → nhấn Đặt hàng
> - ✅ Trang success hiển thị mã đơn và thông tin đơn hàng
> - ✅ Email xác nhận được gửi đến địa chỉ email của khách (kiểm tra inbox thật)
> - ✅ Đơn hàng xuất hiện trong Django Admin với status `PENDING`
> - ✅ Tồn kho giảm đúng số lượng đã đặt
> - ❌ Nếu sản phẩm hết hàng → hiển thị thông báo lỗi, không tạo đơn

---

## TUẦN 4 — Testing, Polish & Deploy (Ngày 22–30)

### Ngày 22 — Unit Tests (Backend)

- [ ] Cấu hình `pytest.ini` và `conftest.py`
- [ ] Tạo factories với `factory-boy`:
  - `UserFactory`, `ProductFactory`, `ProductVariantFactory`, `OrderFactory`
- [ ] Tests cho `products`:
  - [ ] `test_product_list_returns_active_only`
  - [ ] `test_product_filter_by_category`
  - [ ] `test_product_search_by_name`
  - [ ] `test_product_detail_by_slug`
- [ ] Tests cho `orders`:
  - [ ] `test_create_order_success`
  - [ ] `test_create_order_reduces_stock`
  - [ ] `test_create_order_fails_when_out_of_stock`
  - [ ] `test_cannot_create_order_with_zero_items`
  - [ ] `test_cancel_order_restores_stock`
- [ ] Tests cho `payments`:
  - [ ] `test_vnpay_signature_verification_valid`
  - [ ] `test_vnpay_signature_verification_invalid`
  - [ ] `test_vnpay_ipn_updates_order_status`
  - [ ] `test_vnpay_ipn_idempotent` (gọi 2 lần không xử lý 2 lần)
- [ ] Tests cho `auth`:
  - [ ] `test_register_success`
  - [ ] `test_register_duplicate_email`
  - [ ] `test_login_success`
  - [ ] `test_login_wrong_password`
  - [ ] `test_refresh_token`
- [ ] Coverage report: target > 70%

---

### Ngày 23 — E2E Tests (Frontend)

- [ ] Cài đặt Playwright: `npx playwright install`
- [ ] Cấu hình `playwright.config.ts`
- [ ] Test file: `e2e/auth.spec.ts`
  - [ ] Đăng ký tài khoản mới thành công
  - [ ] Đăng nhập thành công
  - [ ] Đăng nhập sai mật khẩu hiển thị lỗi
  - [ ] Đăng xuất
- [ ] Test file: `e2e/shopping.spec.ts`
  - [ ] Tìm sản phẩm theo từ khóa
  - [ ] Lọc theo danh mục
  - [ ] Xem chi tiết sản phẩm
  - [ ] Thêm vào giỏ hàng
  - [ ] Cập nhật số lượng trong giỏ
  - [ ] Xóa sản phẩm khỏi giỏ
- [ ] Test file: `e2e/checkout.spec.ts`
  - [ ] Checkout COD hoàn chỉnh (đặt hàng → trang success → nhận email)
  - [ ] Hiển thị lỗi khi sản phẩm hết hàng trong lúc checkout
  - [ ] Không thể checkout khi chưa đăng nhập (redirect login)
- [ ] Chạy toàn bộ E2E tests pass

---

### Ngày 24 — SEO & Performance

- [ ] SEO:
  - [ ] `generateMetadata()` cho `/`, `/categories/[slug]`, `/products/[slug]`
  - [ ] `sitemap.ts` — tự generate URL sản phẩm + danh mục từ API
  - [ ] `robots.txt` — cho phép crawl, disallow `/account`, `/checkout`
  - [ ] Open Graph tags (title, description, image) cho chia sẻ mạng xã hội
  - [ ] Canonical URL cho tránh duplicate content
  - [ ] Schema.org structured data cho sản phẩm (JSON-LD)
- [ ] Performance:
  - [ ] Tất cả ảnh dùng `next/image` với `width` + `height` hoặc `fill`
  - [ ] Lazy load ảnh dưới fold
  - [ ] Cloudinary URL có `f_auto,q_auto` (auto format + quality)
  - [ ] Font: dùng `next/font` (tránh layout shift)
  - [ ] Không có render-blocking resources
- [ ] Lighthouse audit:
  - [ ] Trang chủ: Performance > 75, SEO > 90 (mobile)
  - [ ] Trang chi tiết sản phẩm: Performance > 80
  - [ ] Nếu score < 75: kiểm tra LCP (ảnh banner), CLS (font/image), FID (JS blocking)
- [ ] Accessibility baseline (tối thiểu trước launch):
  - [ ] Tất cả `<img>` có `alt` mô tả sản phẩm (không để trống hoặc "image")
  - [ ] Tất cả button/link có label rõ ràng (không chỉ dùng icon đơn thuần)
  - [ ] Color contrast đủ 4.5:1 cho text trên nền (dùng Chrome DevTools → Accessibility)
  - [ ] Focus visible trên keyboard navigation (tab qua form checkout)

---

### Ngày 25 — GitHub Actions CI/CD

- [ ] File `.github/workflows/backend.yml`:
  - [ ] Trigger: push to `main`, pull request
  - [ ] Steps: checkout → setup Python → install deps → run pytest
  - [ ] Badge hiển thị trên README
- [ ] File `.github/workflows/frontend.yml`:
  - [ ] Trigger: push to `main`, pull request
  - [ ] Steps: checkout → setup Node → install deps → `tsc --noEmit` → build
- [ ] File `.github/workflows/deploy.yml`:
  - [ ] Trigger: push to `main` (sau khi CI pass)
  - [ ] Deploy backend lên Railway tự động
  - [ ] Vercel tự deploy từ GitHub (cấu hình trong Vercel dashboard)
- [ ] Test pipeline: push một commit và xem CI/CD chạy thành công

---

### Ngày 26 — Deploy Production

- [ ] **Vercel (Frontend):**
  - [ ] Kết nối GitHub repo với Vercel
  - [ ] Cấu hình environment variables (API URL production, ...)
  - [ ] Cấu hình custom domain (nếu có)
  - [ ] Kiểm tra build log không có lỗi

- [ ] **Railway (Backend):**
  - [ ] Cấu hình đầy đủ environment variables production
  - [ ] `DEBUG=False`, `ALLOWED_HOSTS=yourdomain.com`
  - [ ] Chạy `migrate` trên production
  - [ ] Health check endpoint `GET /api/health/` → `{"status": "ok"}`

- [ ] **Neon Postgres:**
  - [ ] Bật automatic backups trong dashboard
  - [ ] Verify connection pooling hoạt động

- [ ] **Cloudinary:**
  - [ ] Tạo "Upload Preset" riêng cho production
  - [ ] Cấu hình folder structure: `products/`, `users/`

- [ ] **Sentry:**
  - [ ] Tạo project Sentry cho Django (backend)
  - [ ] Tạo project Sentry cho Next.js (frontend)
  - [ ] Cài `sentry-sdk` vào Django, `@sentry/nextjs` vào Next.js
  - [ ] Cấu hình DSN từ biến môi trường
  - [ ] Test: trigger một lỗi thủ công → kiểm tra Sentry nhận được

---

### Ngày 27 — Security Hardening

- [ ] Django:
  - [ ] `SECRET_KEY` từ biến môi trường (không hardcode)
  - [ ] `DEBUG = False` trên production
  - [ ] `ALLOWED_HOSTS` chỉ cho phép domain thật
  - [ ] `SECURE_SSL_REDIRECT = True`
  - [ ] `SESSION_COOKIE_SECURE = True`
  - [ ] `CSRF_COOKIE_SECURE = True`
  - [ ] CORS chỉ cho phép domain frontend production
  - [ ] DRF throttling:
    ```python
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/hour',
        'user': '1000/day',
    }
    ```
  - [ ] Đổi admin URL (không dùng `/admin/`)
- [ ] Next.js:
  - [ ] Không expose biến môi trường nhạy cảm ra client
  - [ ] Security headers trong `next.config.js`:
    - `X-Frame-Options: DENY`
    - `X-Content-Type-Options: nosniff`
    - `Referrer-Policy: strict-origin-when-cross-origin`
- [ ] Chạy `pip-audit` để kiểm tra dependency vulnerabilities

---

### Ngày 28 — End-to-End Production Test

- [ ] Test toàn bộ luồng trên production (điện thoại thật, không dùng localhost):
  - [ ] Luồng 1: Khách mới → đăng ký → mua hàng COD → nhận email xác nhận
  - [ ] Luồng 2: Đăng nhập → tìm kiếm → lọc → thêm giỏ → checkout COD → nhận email
  - [ ] Luồng 3: Admin xác nhận đơn → cập nhật trạng thái → khách xem đơn
  - [ ] Luồng 4: Hủy đơn hàng → tồn kho hoàn lại đúng số lượng
- [ ] Test trên nhiều thiết bị / trình duyệt:
  - [ ] Chrome (desktop + mobile)
  - [ ] Safari (iOS)
  - [ ] Firefox
- [ ] Kiểm tra Sentry không có lỗi nghiêm trọng sau test
- [ ] Kiểm tra response time API < 500ms trên production

---

### Ngày 29 — Content & Nội dung thật

- [ ] Nhập sản phẩm thật vào Django Admin (ít nhất 10–20 sản phẩm):
  - [ ] Tên, mô tả, giá đầy đủ
  - [ ] Ảnh thật (upload lên Cloudinary)
  - [ ] Danh mục đúng
  - [ ] Tồn kho thực tế
- [ ] Kiểm tra hiển thị sản phẩm trên web

#### UI Review trước launch (dùng điện thoại thật + Chrome desktop)

- [ ] Spacing và alignment nhất quán giữa trang chủ, danh mục, chi tiết sản phẩm
- [ ] Loading skeleton hiển thị đúng khi fetch chậm (throttle Network → Slow 3G)
- [ ] Empty state hiển thị khi: giỏ hàng trống, không tìm thấy sản phẩm, chưa có đơn hàng
- [ ] Error state hiển thị khi: API lỗi (tắt backend thử), hết hàng khi checkout
- [ ] Breakpoint 375px (iPhone SE) — không bị overflow ngang, text không bị cắt
- [ ] Toast notification hiển thị đúng vị trí (không che nút hành động)

- [ ] Viết `README.md` đầy đủ:
  - [ ] Mô tả dự án
  - [ ] Tech stack
  - [ ] Hướng dẫn chạy local (`docker compose up`)
  - [ ] Hướng dẫn deploy
  - [ ] Biến môi trường cần thiết
- [ ] Tạo `CHANGELOG.md` ghi lại MVP v1.0

---

### Ngày 30 — Launch

- [ ] Final smoke test (5 phút):
  - [ ] Trang chủ load được
  - [ ] Thanh toán sandbox hoạt động
  - [ ] Admin đăng nhập được
  - [ ] Email gửi được
- [ ] Announce link website
- [ ] Theo dõi Sentry trong 2–4 tiếng đầu sau launch
- [ ] Ghi lại backlog Phase 2 (những thứ đã ghi "không làm" trong tháng này)

---

## Phase 2 Backlog (Sau MVP)

> Không động vào những thứ này cho đến khi MVP live và có người dùng thật.

- [ ] **Tích hợp VNPAY / Momo / ZaloPay** (payment gateway)
- [ ] Đánh giá & Review sản phẩm
- [ ] Mã giảm giá / Voucher
- [ ] Flash sale theo khung giờ
- [ ] Wishlist
- [ ] Đồng bộ giỏ hàng server-side (hiện tại mất khi đổi thiết bị)
- [ ] Tích hợp GHN / GHTK thật (tính phí realtime)
- [ ] Báo cáo doanh thu (biểu đồ, xuất Excel)
- [ ] Social login (Google / Facebook)
- [ ] Redis cache (sản phẩm nổi bật, session)
- [ ] Celery + tác vụ nền (gửi email async, cập nhật tồn kho)
- [ ] Notification realtime (WebSocket)
- [ ] Progressive Web App (PWA)
- [ ] Multi-vendor (marketplace)
- [ ] Tích hợp Google Analytics 4
- [ ] A/B testing

---

_Xem tổng quan chức năng: [overview.md](./overview.md)_
_Xem chi tiết tech stack & timeline: [mvp-plan.md](./mvp-plan.md)_
