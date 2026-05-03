# 🚀 Senior Backend Engineer Learning Path (FE → BE → System)

> Đây là tài liệu học tập phụ trợ để phát triển năng lực Backend.
> Không phải tài liệu canonical cho implementation hiện tại của repo.
> Khi có mâu thuẫn, ưu tiên `CONTEXT.md`, `docs/adr/0001-order-inventory-lifecycle.md`, và `docs/be/01-05`.

Chào mừng bạn đến với lộ trình "thực chiến" để trở thành một Backend Engineer thực thụ. Với 6 năm kinh nghiệm Frontend, bạn đã có tư duy hệ thống tốt. Lộ trình này không chỉ dạy bạn "cách dùng Django", mà là **cách xây dựng hệ thống Backend chuẩn production**.

---

## 🧠 Phase 0: Mindset Shift (Rất quan trọng)

Đừng học Python như một ngôn ngữ mới, hãy học cách "map" tư duy:

| Khía cạnh      | Frontend Mindset           | Backend Mindset                            |
| :------------- | :------------------------- | :----------------------------------------- |
| **Trọng tâm**  | UI State & UX              | **Data Integrity & Consistency**           |
| **Đơn vị**     | Component                  | **Service / Module**                       |
| **Thành công** | Giao diện mượt, không giật | **Dữ liệu chính xác, xử lý song song tốt** |
| **Lỗi**        | Async UI (Spinners)        | **Concurrency & Deadlocks**                |

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
- **Làm trong repo này:** Triển khai order flow theo rule đã khóa: `Create order (PENDING) -> Admin confirm -> Lock row -> Deduct stock`.
- **Lưu ý domain:** Trong repo này, tạo order không đồng nghĩa với commit tồn kho. Tồn kho chỉ bị trừ khi `Order` chuyển sang `CONFIRMED`.
- **⚠️ Critical:** **Concurrency > Syntax**.

## 🔴 Phase 4: Database Mastery (Week 4)

**Mục tiêu:** Không còn bị "ORM Blind" (mù quáng tin vào ORM).

- **Học:** N+1 Problem, `select_related`, `prefetch_related`, Indexing, Query Plan (`explain`).
- **Làm:** Optimize API danh sách sản phẩm, thêm Index cho `slug`, `category`, `price`.

## 🟣 Phase 5: System Design Basics (Week 5)

**Mục tiêu:** Tư duy hệ thống lớn.

- **Học:** Stateless API, Idempotency (Tính duy nhất), Pagination strategy (Offset vs Cursor), API Versioning.
- **Làm:** Tìm hiểu `X-Idempotency-Key` cho Order API như một hướng hardening nâng cao.
- **Trong MVP hiện tại:** Không xem idempotency là phần đã khóa scope nếu canonical docs chưa yêu cầu.

## ⚙️ Phase 6: Async & Background Jobs (Week 6)

**Mục tiêu:** Giải phóng Request thread - "Don't keep the user waiting".

- **Học:** Celery, Redis, Message Queues.
- **Làm:** Gửi email xác nhận đơn hàng async, xử lý ảnh sản phẩm async.
- **Phạm vi repo hiện tại:** Đây là kiến thức Phase 2+, không phải baseline bắt buộc của MVP đang triển khai.

## 🔐 Phase 7: Security (Week 7)

- **Học:** JWT Flow, Refresh Token rotation, CSRF (cho Web), Rate Limiting (Throttle).
- **Làm:** Bảo vệ API với Permissions và Throttling classes.

## 🚀 Phase 8: Performance & Scaling (Week 8)

- **Học:** Caching strategies (Redis), CDN cho media, Database Scaling (Read Replicas concept).
- **Làm:** Cache danh sách sản phẩm và Category tree.
- **Phạm vi repo hiện tại:** Chỉ nên đụng đến sau khi API contract, order lifecycle, và admin flow đã ổn định.

## 🧪 Phase 9: Testing (Thực hiện song song)

- **Học:** Unit test (Services), Integration test (APIs), Factories (Factory Boy).
- **Làm:** Chạy `pytest` cho toàn bộ luồng Order.
- **Lưu ý thực tế:** Nếu test stack trong repo chưa cài đủ, phải kiểm tra `pyproject.toml` trước khi xem đây là checklist đã sẵn sàng chạy.

## 🏗️ Phase 10: Production & DevOps

- **Học:** Docker, CI/CD (GitHub Actions), Logging (ELK/Graylog concept), Monitoring (Sentry, Prometheus).
- **Làm:** Containerize hệ thống với Docker Compose (Postgres + Redis + Django).
- **Phạm vi repo hiện tại:** `Redis` ở dòng trên nên hiểu là hướng mở rộng. Không mặc định xem đó là thành phần bắt buộc của MVP hiện tại.

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
2. **Scope và contract canonical:** `docs/be/01-mvp-overview.vi.md`
3. **Quy tắc domain cốt lõi:** `CONTEXT.md`
4. **Quyết định tồn kho theo lifecycle:** `docs/adr/0001-order-inventory-lifecycle.md`
5. **Quy chuẩn cấu trúc:** `docs/be/04-project-structure-guidelines-conventions.vi.md` *(đọc kèm repo thực tế vì file này vẫn còn điểm cần cập nhật)*
6. **Task thực thi:** `docs/be/05-priority-implementation-backlog.vi.md`
