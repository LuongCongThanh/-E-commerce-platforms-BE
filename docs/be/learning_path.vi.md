# 🚀 Senior Backend Engineer Learning Path (FE → BE → System)

Chào mừng bạn đến với lộ trình "thực chiến" để trở thành một Backend Engineer thực thụ. Với 6 năm kinh nghiệm Frontend, bạn đã có tư duy hệ thống tốt. Lộ trình này không chỉ dạy bạn "cách dùng Django", mà là **cách xây dựng hệ thống Backend chuẩn production**.

---

## 🧠 Phase 0: Mindset Shift (Rất quan trọng)

Đừng học Python như một ngôn ngữ mới, hãy học cách "map" tư duy:

| Khía cạnh | Frontend Mindset | Backend Mindset |
| :--- | :--- | :--- |
| **Trọng tâm** | UI State & UX | **Data Integrity & Consistency** |
| **Đơn vị** | Component | **Service / Module** |
| **Thành công** | Giao diện mượt, không giật | **Dữ liệu chính xác, xử lý song song tốt** |
| **Lỗi** | Async UI (Spinners) | **Concurrency & Deadlocks** |

👉 **BE không chỉ là "trả về JSON", mà là: Data integrity + Scalability + Correctness.**

---

## 🟢 Phase 1: Django Fundamentals (Week 1)

**Mục tiêu:** Hiểu Framework, không bị "Magic Django" đánh lừa.

- **Học:**
  - Django Request/Response Lifecycle (Request đi qua đâu?).
  - Cấu trúc Apps (Modular design).
  - ORM cơ bản & Migrations.
- **Làm:** Tạo models `User`, `Product`, `Category`. Chạy `makemigrations` & `migrate`.
- **⚠️ Lưu ý:** `Model != Interface`. Model là Database Schema + Business Constraints.

## 🟡 Phase 2: API Layer (Week 2)

**Mục tiêu:** Biến Data thành API chuẩn RESTful.

- **Học:** DRF (Serializers, ViewSets), Pagination, Filtering, Validation.
- **Làm:** Viết API `GET /products`, `GET /products/:slug`.
- **Thêm:** Định dạng lỗi (Error format) và Response chuẩn hóa.

## 🔵 Phase 3: Business Logic (Week 3)

**Mục tiêu:** Tách biệt logic khỏi View - Chống lại "Fat Views".

- **Học:** Service Layer pattern, Transactions (`@transaction.atomic`), Database Locks (`select_for_update`).
- **Làm:** Triển khai Checkout flow (Validate stock -> Lock row -> Deduct stock -> Create order).
- **⚠️ Critical:** **Concurrency > Syntax**.

## 🔴 Phase 4: Database Mastery (Week 4)

**Mục tiêu:** Không còn bị "ORM Blind" (mù quáng tin vào ORM).

- **Học:** N+1 Problem, `select_related`, `prefetch_related`, Indexing, Query Plan (`explain`).
- **Làm:** Optimize API danh sách sản phẩm, thêm Index cho `slug`, `category`, `price`.

## 🟣 Phase 5: System Design Basics (Week 5)

**Mục tiêu:** Tư duy hệ thống lớn.

- **Học:** Stateless API, Idempotency (Tính duy nhất), Pagination strategy (Offset vs Cursor), API Versioning.
- **Làm:** Implement `X-Idempotency-Key` cho Order API.

## ⚙️ Phase 6: Async & Background Jobs (Week 6)

**Mục tiêu:** Giải phóng Request thread - "Don't keep the user waiting".

- **Học:** Celery, Redis, Message Queues.
- **Làm:** Gửi email xác nhận đơn hàng async, xử lý ảnh sản phẩm async.

## 🔐 Phase 7: Security (Week 7)

- **Học:** JWT Flow, Refresh Token rotation, CSRF (cho Web), Rate Limiting (Throttle).
- **Làm:** Bảo vệ API với Permissions và Throttling classes.

## 🚀 Phase 8: Performance & Scaling (Week 8)

- **Học:** Caching strategies (Redis), CDN cho media, Database Scaling (Read Replicas concept).
- **Làm:** Cache danh sách sản phẩm và Category tree.

## 🧪 Phase 9: Testing (Thực hiện song song)

- **Học:** Unit test (Services), Integration test (APIs), Factories (Factory Boy).
- **Làm:** Chạy `pytest` cho toàn bộ luồng Order.

## 🏗️ Phase 10: Production & DevOps

- **Học:** Docker, CI/CD (GitHub Actions), Logging (ELK/Graylog concept), Monitoring (Sentry, Prometheus).
- **Làm:** Containerize hệ thống với Docker Compose (Postgres + Redis + Django).

---

## 🎯 Checklist đạt chuẩn Senior Backend

- [ ] Không viết business logic trong View (dùng Service).
- [ ] Mọi thao tác ghi dữ liệu quan trọng đều nằm trong `transaction.atomic`.
- [ ] Hiểu và xử lý được N+1 queries.
- [ ] Hệ thống có cơ chế Idempotency cho các hành động nhạy cảm (thanh toán, đặt hàng).
- [ ] Có đầy đủ Logging & Error Tracking (Sentry).

---

## 📚 Tài liệu tham khảo trong dự án

1. **Roadmap chi tiết:** `docs/be/02-roadmap-and-execution-plan.vi.md`
2. **Quy chuẩn cấu trúc:** `docs/be/04-project-structure-guidelines-conventions.vi.md`
3. **Task thực thi:** `docs/be/05-priority-implementation-backlog.vi.md`
