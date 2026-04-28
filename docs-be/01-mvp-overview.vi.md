# 01. MVP Overview — Backend (VI)

Last updated: 2026-04-25  
Source of truth: `docs-mvp/mvp-plan.md`, `docs/01-mvp-overview.vi.md`, Django project structure, API contracts  
Owner: BE Lead + BA Lead + Tech Lead

## TOC

- [Purpose](#purpose)
- [Scope](#scope)
- [Decisions](#decisions)
- [Detailed Spec](#detailed-spec)
- [Acceptance Criteria](#acceptance-criteria)
- [Open Risks / Next Actions](#open-risks--next-actions)

## Summary Table

| Item        | Definition                                                                  |
| ----------- | --------------------------------------------------------------------------- |
| Product     | Django REST API backend cho nền tảng e-commerce thị trường Việt Nam         |
| MVP target  | API ổn định phục vụ COD checkout, quản trị đơn/sản phẩm, xác thực JWT       |
| Core users  | FE Next.js (API consumer), vận hành cửa hàng (Django Admin), admin hệ thống |
| Primary KPI | API uptime, checkout success rate, order processing SLA, auth success rate  |

## Purpose

Tài liệu này định nghĩa đầy đủ MVP Backend ở góc độ nghiệp vụ và kỹ thuật: mục tiêu, phạm vi API, luồng chính, tiêu chí chấp nhận, và định nghĩa thành công. Đây là tài liệu chuẩn để BE/BA đồng thuận trước khi triển khai, và là nguồn sự thật cho API contract với FE.

## Scope

In-scope cho MVP:

- Auth API: register, login, logout, refresh token, forgot/reset password.
- Catalog API: danh sách sản phẩm, chi tiết sản phẩm theo slug, danh mục, tìm kiếm, lọc cơ bản.
- Cart/Inventory: kiểm tra tồn kho khi tạo đơn, trừ kho atomic (select_for_update).
- Order API: tạo đơn COD, xem lịch sử đơn, chi tiết đơn — phía khách hàng.
- Admin API / Django Admin: CRUD sản phẩm, quản lý đơn hàng, cập nhật trạng thái đơn.
- Email: gửi email xác nhận đơn qua SMTP.
- Media: upload/serve ảnh sản phẩm qua Cloudinary.
- NFR nền tảng: throttling, CORS, HTTPS, Sentry error tracking, OpenAPI docs.

Out-of-scope cho MVP (defer):

- Online payment gateways (VNPay/Momo/ZaloPay).
- Async task queue (Celery/Redis).
- Full-text search engine (Elasticsearch).
- Webhook outbound (shipping provider).
- Multi-vendor / marketplace.
- Advanced reporting / BI.
- Social login (Google/Facebook OAuth).

## Decisions

- Django Admin là giao diện quản trị MVP — không build custom admin frontend riêng.
- SimpleJWT cho auth token — stateless, dễ scale.
- Tất cả API response phải theo shape đã chốt trong API Contract doc.
- COD-first: không tích hợp payment gateway trong MVP.
- Atomic transaction cho mọi thao tác trừ kho — không cho phép oversell.
- drf-spectacular cho OpenAPI docs — FE dùng Swagger UI để xác nhận contract.
- Success được đo bằng khả năng phục vụ FE end-to-end, không chỉ unit test pass.

## Detailed Spec

### Business context và personas

- Persona 1 - FE Consumer (Next.js app):
  - Mục tiêu: gọi API stable, response shape nhất quán, lỗi rõ ràng.
  - Pain points: contract thay đổi không báo trước, response không nhất quán.
- Persona 2 - Store operator:
  - Mục tiêu: dùng Django Admin để cập nhật sản phẩm, xử lý đơn nhanh.
  - Pain points: UI admin chậm, bulk action thiếu, không có audit trail.
- Persona 3 - Admin owner:
  - Mục tiêu: hệ thống ổn định, lỗi được theo dõi, dữ liệu không bị corrupt.

### Goals và success outcomes

- Goal 1: Tất cả API endpoint phục vụ FE MVP hoạt động ổn định trên production.
- Goal 2: Django Admin đủ dùng để vận hành đơn và sản phẩm hằng ngày không cần dev.
- Goal 3: Không có lỗi tồn kho (oversell) hay mất đơn do race condition.
- Goal 4: Tài liệu API (Swagger) luôn đồng bộ với implementation.

### Core API journeys

1. Auth flow:
   - `POST /api/auth/register/` → trả `{ access, refresh, user }`.
   - `POST /api/auth/login/` → trả `{ access, refresh, user }`.
   - `POST /api/auth/token/refresh/` → rotate refresh token.
   - `POST /api/auth/password/reset/` → gửi email reset.
2. Catalog flow:
   - `GET /api/products/` → paginated list với filter/search.
   - `GET /api/products/{slug}/` → product detail + variants + images.
   - `GET /api/categories/` → category tree.
3. Order flow:
   - `POST /api/orders/` → tạo đơn COD, atomic stock deduction.
   - `GET /api/orders/` → lịch sử đơn của user đang đăng nhập.
   - `GET /api/orders/{id}/` → chi tiết đơn.
4. Admin flow (Django Admin):
   - CRUD sản phẩm, variant, hình ảnh.
   - Xem danh sách đơn, lọc theo trạng thái, bulk update trạng thái.

### API contract baseline

```yaml
GET  /api/products/         → { count, next, previous, results: Product[] }
GET  /api/products/{slug}/  → Product { id, name, slug, description, images[], variants[], price_min, price_max, category }
GET  /api/categories/       → Category[] { id, name, slug, parent, children[] }
POST /api/orders/           → Order { id, status, total, items[], shipping_address }
GET  /api/orders/           → { count, next, previous, results: Order[] }
GET  /api/orders/{id}/      → Order { id, status, total, items[], shipping_address, created_at, updated_at }
POST /api/auth/register/    → { access, refresh, user: { id, email, first_name, last_name } }
POST /api/auth/login/       → { access, refresh, user: { id, email, first_name, last_name } }
POST /api/auth/token/refresh/ → { access, refresh }
```

FE không bắt đầu viết code gọi API nếu contract chưa được confirm.

### Error response shape (chuẩn)

```json
{
  "code": "VALIDATION_ERROR",
  "message": "Dữ liệu không hợp lệ",
  "errors": {
    "field_name": ["Thông báo lỗi cụ thể"]
  }
}
```

### Non-functional requirements (MVP level)

- Security:
  - `DEBUG = False` trên production.
  - CORS chỉ cho phép domain FE.
  - DRF throttling: AnonRateThrottle (100/day), UserRateThrottle (1000/day).
  - Không expose Django Admin tại `/admin/` — đổi sang path tùy chỉnh.
  - JWT access token TTL: 15 phút. Refresh token TTL: 7 ngày.
- Performance:
  - API response < 500ms cho 95th percentile.
  - Database indexing cho các query chính (slug, email, order status).
- Observability:
  - Sentry DSN cấu hình cho BE.
  - Log lỗi 5xx với request context.
  - Health check endpoint `GET /api/health/`.
- Data integrity:
  - `select_for_update()` cho mọi thao tác trừ kho.
  - Idempotency check cho tạo đơn.

### MVP KPIs và definition of success

- API KPIs:
  - API uptime > 99% trong 4 tuần đầu.
  - Error rate 5xx < 1% tổng request.
  - Thời gian phản hồi trung bình < 300ms.
- Ops KPIs:
  - Không có case oversell (tồn kho âm).
  - Đơn hàng COD được tạo thành công > 99%.
- Quality KPIs:
  - Test coverage backend ≥ 80% cho business logic cốt lõi.
  - Swagger docs tự động sinh và đúng với implementation.

Definition of success:

- FE có thể chạy end-to-end COD flow sử dụng BE API trên production.
- Django Admin vận hành được đơn và sản phẩm hằng ngày.
- Không có incident data corruption trong 4 tuần đầu.

## Acceptance Criteria

- Tài liệu này là baseline được BE/BA/FE dùng làm chuẩn scope.
- Tất cả API endpoint trong scope có contract rõ và được xác nhận bởi FE.
- In-scope/out-of-scope được khóa để tránh scope creep.
- Error shape chuẩn được thống nhất trước khi implement.

## Open Risks / Next Actions

Open risks:

- FE và BE không đồng bộ contract → cần freeze sprint-by-sprint.
- Race condition khi nhiều user đặt cùng variant hết hàng → đã mitigation bằng `select_for_update`.
- Railway free tier có thể bị cold start → ảnh hưởng response time đầu ngày.

Next actions:

- [ ] Chốt và publish API contract baseline cho FE review.
- [ ] Thiết lập Swagger UI trên staging để FE tự test.
- [ ] Cài Sentry DSN và verify error tracking hoạt động.
- [ ] Viết `README.md` local setup cho BE (docker-compose).
- [ ] Review lại phạm vi sau tuần vận hành đầu tiên.
