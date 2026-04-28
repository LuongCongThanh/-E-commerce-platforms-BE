# 02. Roadmap And Execution Plan — Backend (VI)

Last updated: 2026-04-25  
Source of truth: `01-mvp-overview.vi.md`, `docs/02-roadmap-and-execution-plan.vi.md`, `docs-mvp/mvp-plan.md`  
Owner: BE Lead + BA Lead + PM

## TOC

- [Purpose](#purpose)
- [Scope](#scope)
- [Decisions](#decisions)
- [Detailed Spec](#detailed-spec)
- [Acceptance Criteria](#acceptance-criteria)
- [Open Risks / Next Actions](#open-risks--next-actions)

## Summary Table

| Item              | Value                                               |
| ----------------- | --------------------------------------------------- |
| Delivery model    | Phase-based, song song với FE — BE dẫn trước 1 tuần |
| MVP window        | 4 tuần (BE hoàn thiện trước để FE tích hợp)         |
| Core dependency   | API contract stability + Django Admin vận hành được |
| Control mechanism | Weekly gate + Swagger UI làm bằng chứng API ready   |

## Purpose

Tài liệu này chuyển scope MVP Backend thành lộ trình và kế hoạch thực thi theo tuần, đồng bộ với lịch FE, có dependency rõ, gate rõ, và cách theo dõi tiến độ thống nhất.

## Scope

Bao gồm:

- Roadmap theo phase: MVP, Post-MVP Phase 1, Phase 2, Later.
- Kế hoạch triển khai theo tuần cho MVP BE.
- Dependency map giữa BE và FE.
- Entry/exit criteria, delivery gates.
- Risk register và mitigation plan.
- RACI vai trò BE/BA/FE/QA.
- Tracking model và blocker protocol.

Không bao gồm:

- Chi tiết implementation ở mức code/file.
- Hướng dẫn setup local chi tiết (xem `04-project-structure`).

## Decisions

- BE phải hoàn thiện API contract và staging URL trước khi FE bắt đầu tích hợp.
- Swagger UI trên staging là bằng chứng API ready — không chấp nhận "chạy local".
- Không mở rộng scope nếu chưa đạt exit criteria của gate hiện tại.
- Database migration phải review trước khi chạy production.
- Blocker được escalated trong vòng 24h.

## Detailed Spec

### Phase roadmap

1. MVP (Phase 0):
   - Outcomes: auth API + catalog API + order API COD + Django Admin + email xác nhận đơn.
   - Timebox: 4 tuần.
2. Post-MVP Phase 1:
   - Outcomes: account API (profile, address book), advanced filtering, order cancellation API.
3. Post-MVP Phase 2:
   - Outcomes: payment gateway integration (VNPay/Momo), Celery async tasks, Redis cache.
4. Later:
   - Outcomes: Elasticsearch, social login, multi-vendor, advanced reporting/BI.

### MVP weekly execution plan

**Tuần 1 — Setup & Core Models (Ngày 1–7)**

Goal: Backend chạy trên production với API catalog và auth cơ bản.

- Ngày 1–2: Project setup
  - Tạo Django project, cấu hình `settings/` (base/dev/prod).
  - Setup Docker Compose: Django + PostgreSQL.
  - Cài DRF, drf-spectacular, SimpleJWT, django-allauth.
  - Cấu hình `.env` template, không commit secret.
  - Setup GitHub Actions: lint + test + build.
- Ngày 3–4: Database models
  - `User` (extend AbstractUser, thêm phone, avatar).
  - `Category` (name, slug, parent FK).
  - `Product` (name, slug, description, category FK, is_active).
  - `ProductVariant` (product FK, sku, price, stock_quantity, attributes JSON).
  - `ProductImage` (product FK, url, alt, order, is_primary).
- Ngày 5–6: Django Admin + Catalog API
  - Đăng ký models vào Admin với `list_display`, `search_fields`, `list_filter`.
  - DRF serializers: `ProductListSerializer`, `ProductDetailSerializer`, `CategorySerializer`.
  - Endpoints: `GET /api/products/`, `GET /api/products/{slug}/`, `GET /api/categories/`.
  - Cấu hình drf-spectacular → Swagger UI tự động.
- Ngày 7: Auth API + Deploy
  - SimpleJWT: register, login, refresh, logout (token blacklist).
  - Custom `UserSerializer` trả `{ id, email, first_name, last_name }`.
  - Deploy lên Railway, cấu hình biến môi trường production.
  - Verify Swagger UI trên production URL.

**Gate cuối Tuần 1 — không chuyển Tuần 2 nếu chưa đạt:**

- [ ] Swagger UI trên production URL hoạt động và trả đúng schema.
- [ ] `POST /api/auth/register/` + `login/` hoạt động trên production.
- [ ] `GET /api/products/` trả danh sách (dù chỉ seed data test).
- [ ] Docker Compose local chạy được không lỗi.
- [ ] GitHub Actions CI pass (lint + test).

---

**Tuần 2 — Order API + Email (Ngày 8–14)**

Goal: FE có thể tích hợp cart → checkout → order confirmation end-to-end.

- Ngày 8–9: Order models
  - `Order` (user FK, status, shipping_address JSON, total, notes).
  - `OrderItem` (order FK, variant FK, quantity, price_at_purchase).
  - `ShippingAddress` (user FK, address, ward, district, province, phone).
  - Django migration với indexes cho `order.status`, `order.user`.
- Ngày 10–11: Order API
  - `POST /api/orders/` — atomic transaction: validate stock → deduct → create order.
  - `select_for_update()` trên `ProductVariant` để tránh race condition.
  - Trả `Order` shape chuẩn theo contract.
  - `GET /api/orders/` + `GET /api/orders/{id}/` — chỉ trả data của user đang đăng nhập.
- Ngày 12–13: Email + Cloudinary
  - Django email backend (SMTP Gmail/Mailgun).
  - HTML email template: xác nhận đơn hàng (order ID, items, tổng tiền, địa chỉ).
  - Gửi email async trong view (sync OK ở MVP — defer Celery sang Phase 2).
  - Cloudinary: cấu hình `DEFAULT_FILE_STORAGE` hoặc xử lý URL ảnh.
- Ngày 14: Hardening + Test coverage
  - Viết pytest tests cho order flow: happy path + stock validation + race condition.
  - Verify email gửi được thật trên staging.
  - Seed data đủ để FE test: 5 categories, 20 products, 3 variants mỗi product.

**Gate cuối Tuần 2:**

- [ ] `POST /api/orders/` tạo đơn thành công trên staging.
- [ ] Email xác nhận gửi được thật (không chỉ log).
- [ ] Không có lỗi 500 trong Sentry sau test.
- [ ] Seed data đủ cho FE bắt đầu tích hợp.

---

**Tuần 3 — Admin nâng cao + Hardening (Ngày 15–21)**

Goal: Django Admin đủ mạnh để vận hành, API ổn định cho FE tích hợp hoàn chỉnh.

- Ngày 15–16: Django Admin nâng cao
  - Custom action: confirm order, mark shipping, cancel order (bulk).
  - `list_display` cho Order admin: id, user email, status, total, created_at.
  - Dashboard đơn giản trong Admin: đơn hôm nay, doanh thu hôm nay, sản phẩm sắp hết hàng.
  - `readonly_fields` cho tổng tiền, trạng thái audit trail.
- Ngày 17–18: Cập nhật trạng thái đơn API
  - `PATCH /api/admin/orders/{id}/status/` — chỉ admin role.
  - Workflow trạng thái: `PENDING → CONFIRMED → SHIPPING → DELIVERED → CANCELLED`.
  - Không cho phép nhảy trạng thái bất hợp lệ (state machine cơ bản).
  - Log thay đổi trạng thái với timestamp và user thực hiện.
- Ngày 19–20: Security hardening
  - Kiểm tra tất cả endpoint yêu cầu authentication đúng cách.
  - Rate limiting: cấu hình AnonRateThrottle, UserRateThrottle, AuthRateThrottle.
  - CORS chỉ cho phép FE domain production và staging.
  - Đổi Django Admin URL ra khỏi `/admin/`.
- Ngày 21: Performance baseline
  - `select_related` / `prefetch_related` cho product list query.
  - Index review: slug, email, order status, variant stock.
  - `django-debug-toolbar` trong development để phát hiện N+1.

**Gate cuối Tuần 3:**

- [ ] Admin có thể cập nhật trạng thái đơn hàng qua bulk action.
- [ ] Không có N+1 query trong product list endpoint.
- [ ] Rate limiting hoạt động — 429 khi vượt ngưỡng.
- [ ] `PATCH /api/admin/orders/{id}/status/` từ chối non-admin.

---

**Tuần 4 — Testing, Deploy & Launch (Ngày 22–30)**

Goal: Production-ready, CI/CD hoàn chỉnh, launch với 10–20 sản phẩm thật.

- Ngày 22–24: Test coverage
  - pytest-django: order creation (happy path + edge cases), stock deduction, race condition test.
  - Auth tests: register, login, refresh, logout blacklist, password reset.
  - Permission tests: anonymous user không access protected endpoints.
  - Factory Boy cho test fixtures.
- Ngày 25–26: CI/CD hoàn chỉnh
  - GitHub Actions: lint (flake8/ruff) + pytest + build Docker image.
  - Auto-deploy lên Railway khi push `main` pass CI.
  - Staging environment riêng cho FE integration test.
- Ngày 27–28: Production readiness
  - Backup PostgreSQL tự động (Neon dashboard).
  - Sentry DSN cấu hình, verify error tracking.
  - `ALLOWED_HOSTS`, `SECURE_SSL_REDIRECT`, `CSRF_COOKIE_SECURE`.
  - Health check endpoint `GET /api/health/` trả `{ status: "ok", version }`.
- Ngày 29–30: Launch
  - Nhập 10–20 sản phẩm thật qua Django Admin.
  - Test end-to-end toàn luồng COD trên production (điện thoại thật).
  - Fix bug phát sinh.
  - Viết/cập nhật `README.md` (local setup, deploy guide).

**Gate cuối Tuần 4 (Release Gate):**

- [ ] CI/CD pass và auto-deploy hoạt động.
- [ ] Core regression pass cho auth + catalog + order.
- [ ] Không có lỗi severity cao trong Sentry.
- [ ] Health check endpoint trả `200 OK` trên production.
- [ ] 10+ sản phẩm thật có ảnh trong database.

---

### Dependency map

- **D1:** API contract phải được confirm giữa BE và FE trước cuối Tuần 1.
- **D2:** Swagger UI trên staging phải live trước khi FE bắt đầu tích hợp Tuần 2.
- **D3:** Seed data đủ (`20 products`, `3 categories`) phải có trước khi FE test catalog.
- **D4:** Email SMTP phải verify hoạt động trên staging trước khi FE test checkout.
- **D5:** Railway production URL phải stable (không thay đổi) trước khi FE config.

### Delivery gates (entry/exit criteria)

Gate A — Foundation complete:

- Entry: kickoff và scope locked.
- Exit:
  - Django project chạy được trên Docker Compose.
  - Auth API và catalog API live trên staging.
  - Swagger UI tự động sinh OpenAPI schema đúng.

Gate B — Feature complete:

- Entry: Gate A pass.
- Exit:
  - Order API hoạt động end-to-end trên staging.
  - Django Admin CRUD sản phẩm và quản lý đơn vận hành được.
  - Email xác nhận đơn gửi thật.
  - Không còn blocker severity cao.

Gate C — Release ready:

- Entry: Gate B pass.
- Exit:
  - CI/CD chạy tự động và deploy thành công.
  - QA smoke + regression pass trên production.
  - Monitoring/Sentry hoạt động.
  - Backup database configured.

### Risk register và mitigation

| Risk                      | Impact               | Likelihood | Mitigation                                     | Owner   |
| ------------------------- | -------------------- | ---------- | ---------------------------------------------- | ------- |
| API contract churn        | Rework FE            | Medium     | Contract freeze per sprint, Swagger làm chuẩn  | BE Lead |
| Race condition oversell   | Dữ liệu sai          | Medium     | `select_for_update()` bắt buộc trong order API | BE Lead |
| Railway cold start        | Slow first response  | Low        | Health check + warming cron                    | DevOps  |
| Email delivery failure    | Khách không nhận đơn | Low        | Fallback log + retry, verify SMTP sớm          | BE Lead |
| Migration conflict        | Downtime             | Low        | Review migration trước deploy, backup trước    | BE Lead |
| Scope creep từ FE request | Trễ tiến độ          | High       | Change control + phase backlog                 | BA Lead |

### RACI (simple)

| Workstream                          | BA  | FE  | QA  | BE  |
| ----------------------------------- | --- | --- | --- | --- |
| API contract và scope               | A/R | C   | C   | C   |
| Database design và models           | C   | I   | I   | A/R |
| API implementation                  | C   | C   | I   | A/R |
| Django Admin setup                  | C   | I   | C   | A/R |
| Test strategy (BE unit/integration) | C   | I   | C   | A/R |
| E2E integration test                | C   | R   | A/R | C   |
| Release readiness                   | A   | R   | R   | R   |

Legend: A: Accountable | R: Responsible | C: Consulted | I: Informed

### Tracking model và blocker protocol

- Tracking model:
  - Milestone theo gate A/B/C và weekly checkpoint.
  - Progress đo bằng Swagger endpoint coverage + gate status.
  - Burn-down theo backlog ưu tiên (P0-P3).
- Blocker protocol:
  1. Gắn nhãn blocker trong tracker ngay khi phát hiện.
  2. Nêu impact cụ thể (FE bị chặn? data corrupt? deploy fail?).
  3. Nêu owner và ETA workaround.
  4. Escalate trong 24h nếu chưa tháo gỡ.
  5. Nếu blocker ảnh hưởng FE critical path, re-plan ngay trong ngày.

## Acceptance Criteria

- Roadmap có phase rõ và outcome rõ.
- Execution plan có phụ thuộc FE/BE, gate, RACI, tracking model đầy đủ.
- BE phải dẫn trước FE ít nhất 3–5 ngày tại mỗi milestone.
- Có cơ chế quản lý rủi ro contract churn và blocker.

## Open Risks / Next Actions

Open risks:

- Kéo dài chốt contract gây trễ FE tích hợp.
- Under-estimation effort ở order edge cases (huỷ đơn, rollback tồn kho).

Next actions:

- [ ] Chốt owner cho từng gate và deadline tương ứng.
- [ ] Publish staging URL và Swagger UI link cho FE team.
- [ ] Cài tracker template theo milestone/gate.
- [ ] Tạo phiên review cố định hằng tuần cho risk & blockers.
- [ ] Khóa baseline test checklist trước sprint feature complete.
