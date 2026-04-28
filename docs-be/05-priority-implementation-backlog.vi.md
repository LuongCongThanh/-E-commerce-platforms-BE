# 05. Priority Implementation Backlog — Backend (VI)

Last updated: 2026-04-25  
Source of truth: `01-04` docs in this set, `docs/05-priority-implementation-backlog.vi.md` (FE sync)  
Owner: BE Lead + BA Lead + PM

## TOC

- [Purpose](#purpose)
- [Scope](#scope)
- [Decisions](#decisions)
- [Detailed Spec](#detailed-spec)
- [Acceptance Criteria](#acceptance-criteria)
- [Open Risks / Next Actions](#open-risks--next-actions)

## Summary Table

| Priority | Intent                                                     |
| -------- | ---------------------------------------------------------- |
| P0       | Nền tảng bắt buộc để BE bắt đầu implement đúng hướng       |
| P1       | API cốt lõi phục vụ FE tạo giá trị MVP trực tiếp           |
| P2       | Hardening, security, và Django Admin đủ mạnh trước release |
| P3       | Mở rộng sau MVP, không chặn launch                         |

## Purpose

Tài liệu này cung cấp backlog triển khai Backend theo thứ tự ưu tiên tuyệt đối để team BE có thể đi vào implementation ngay, không cần tự quyết định lại scope hay thứ tự công việc.

## Scope

Bao gồm:

- Danh sách công việc P0/P1/P2/P3 theo thứ tự thực thi.
- Mỗi item có objective, output, dependencies, owner role, acceptance checks.
- Mapping skills BE/QA cho từng cụm công việc.
- FE dependency rõ (BE cần xong trước khi FE làm gì).
- Not-now list để kiểm soát scope.

Không bao gồm:

- Low-level task breakdown theo từng file code.

## Decisions

- Luôn ưu tiên xong P0 trước khi nhận bất kỳ task P1+.
- P1 phải dẫn trước FE ít nhất 3 ngày tại mỗi milestone.
- Không thực hiện P3 khi P1/P2 chưa đạt quality gate.
- Backlog này là thứ tự chuẩn cho build mới từ zero đến MVP-ready.
- Mọi change request ngoài backlog phải qua change-control.

## Detailed Spec

### P0 - Foundation và execution control

| ID    | Objective                              | Output                                                 | Dependencies | Owner role | Acceptance checks                                  | Skill mapping                                     |
| ----- | -------------------------------------- | ------------------------------------------------------ | ------------ | ---------- | -------------------------------------------------- | ------------------------------------------------- |
| P0-01 | Khóa scope BE và API contract baseline | Contract doc lock + error shape chuẩn                  | FE P0-01     | BA + BE    | FE confirm contract, error shape nhất quán         | BE: backend-dev-guidelines, api-design-principles |
| P0-02 | Khóa kiến trúc Django app-based        | Project tree + app boundaries + settings strategy      | P0-01        | BE         | Apps tách đúng domain, settings phân tầng rõ       | BE: backend-development-feature-development       |
| P0-03 | Setup môi trường dev + CI              | Docker Compose chạy được + GitHub Actions CI pass      | P0-02        | BE         | `docker-compose up` không lỗi, CI lint + test pass | BE: docker-expert, github-actions-templates       |
| P0-04 | Thiết lập database models + migrations | Schema models + migrations cho accounts/catalog/orders | P0-02        | BE         | Migrations apply clean, indexes đúng chỗ           | BE: database-design, postgresql                   |
| P0-05 | Cấu hình quality gate + PR template    | `ruff`+`black`+`pytest-cov` pass + PR template         | P0-02        | BE         | Gate tự động trong CI, coverage target rõ          | BE: lint-and-validate                             |

### P1 - Core API build

| ID    | Objective               | Output                                                    | Dependencies | Owner role | Acceptance checks                                       | Skill mapping                                            | FE unblocks           |
| ----- | ----------------------- | --------------------------------------------------------- | ------------ | ---------- | ------------------------------------------------------- | -------------------------------------------------------- | --------------------- |
| P1-01 | Auth API                | Register/login/logout/refresh/password-reset endpoints    | P0-\*        | BE         | JWT flow hoạt động, token TTL đúng, blacklist works     | BE: auth-implementation-patterns, backend-security-coder | FE P1-02 (auth)       |
| P1-02 | Catalog API             | Products list/detail + categories + search/filter         | P0-\*        | BE         | Paginated response đúng shape, slug unique, images đúng | BE: api-design-principles, database-design               | FE P1-01 (storefront) |
| P1-03 | Swagger UI trên staging | `/api/docs/` tự động sinh từ code, staging URL public     | P1-01, P1-02 | BE         | FE có thể test endpoint qua Swagger UI                  | BE: backend-dev-guidelines                               | FE bắt đầu tích hợp   |
| P1-04 | Order API (COD)         | Create order + stock deduction atomic + order list/detail | P1-01, P1-02 | BE         | COD order tạo thành công, race condition không xảy ra   | BE: backend-development-feature-development              | FE P1-04 (checkout)   |
| P1-05 | Email xác nhận đơn      | HTML email template gửi khi order created                 | P1-04        | BE         | Email gửi thật qua SMTP, nội dung đúng đơn hàng         | BE: backend-dev-guidelines                               | FE P1-05 (order)      |
| P1-06 | Seed data staging       | 5 categories, 20+ products, 3 variants mỗi product        | P1-02        | BE         | FE có data để test catalog, search, filter hoạt động    | BE: database-design                                      | FE bắt đầu test UI    |

### P2 - Hardening trước release

| ID    | Objective             | Output                                                   | Dependencies | Owner role  | Acceptance checks                                 | Skill mapping                                           |
| ----- | --------------------- | -------------------------------------------------------- | ------------ | ----------- | ------------------------------------------------- | ------------------------------------------------------- |
| P2-01 | Django Admin nâng cao | Bulk actions, order status workflow, dashboard đơn giản  | P1-\*        | BE          | Admin có thể xử lý đơn mà không cần dev can thiệp | BE: backend-development-feature-development             |
| P2-02 | Security hardening    | Rate limiting, CORS, ALLOWED_HOSTS, Admin URL đổi        | P1-\*        | BE          | 429 khi quá rate limit, CORS block domain lạ      | BE: backend-security-coder, api-security-best-practices |
| P2-03 | Test coverage ≥ 80%   | Unit + integration tests cho auth/catalog/orders         | P1-\*        | BE + QA     | `pytest --cov` report ≥ 80% cho `apps/`           | QA: testing-qa, unit-testing-test-generate              |
| P2-04 | Performance baseline  | select_related/prefetch, indexes, debug-toolbar check    | P1-\*        | BE          | Không có N+1 trong product list, API < 300ms avg  | BE: postgresql, database-design                         |
| P2-05 | Production readiness  | HTTPS, backup, Sentry DSN, health check, deploy CI/CD    | P1-\*        | BE + DevOps | Health check `200 OK`, Sentry nhận test event     | DevOps: deployment-engineer, github-actions-templates   |
| P2-06 | API security testing  | Validate auth/authz/rate-limit/input cho tất cả endpoint | P2-02        | BE + QA     | Không có endpoint accessible mà không cần auth    | QA: api-security-testing, systematic-debugging          |

### P3 - Post-MVP expansion

| ID    | Objective                    | Output                                           | Dependencies | Owner role | Acceptance checks                                  | Skill mapping                               |
| ----- | ---------------------------- | ------------------------------------------------ | ------------ | ---------- | -------------------------------------------------- | ------------------------------------------- |
| P3-01 | Account API nâng cao         | Profile update, address book CRUD                | P2-\*        | BE         | FE có thể CRUD địa chỉ giao hàng                   | BE: backend-development-feature-development |
| P3-02 | Order cancellation API       | `POST /api/orders/{id}/cancel/` + rollback stock | P2-\*        | BE         | Cancel thành công, tồn kho rollback đúng           | BE: backend-dev-guidelines                  |
| P3-03 | Payment gateway (VNPay/Momo) | Tích hợp payment + webhook xử lý                 | P2-\*        | BE         | Payment flow hoạt động end-to-end sandbox          | BE: backend-architect                       |
| P3-04 | Celery + Redis async tasks   | Email gửi async, không block request             | P2-\*        | BE         | Email gửi được sau khi response trả về             | DevOps: docker-expert                       |
| P3-05 | Advanced admin dashboard     | Doanh thu, đơn hôm nay, sản phẩm hot, biểu đồ    | P2-\*        | BE         | Admin thấy được KPI cơ bản mà không cần SQL        | BE: backend-development-feature-development |
| P3-06 | Social login                 | Google/Facebook OAuth qua django-allauth         | P2-\*        | BE         | Login Google hoạt động, trả JWT như password login | BE: auth-implementation-patterns            |

### Sequencing rules

1. Không bỏ qua P0 — kể cả khi có áp lực thời gian.
2. Trong cùng priority, ưu tiên item mà FE đang chờ (FE unblocks column).
3. P1-03 (Swagger staging) là priority cao nhất trong P1 vì unblock cả FE team.
4. P1-04 (Order API) là critical path — chặn checkout, không được trễ.
5. Không bắt đầu P3 nếu chưa pass gate release P2.

### FE sync dependency map

| BE Item | FE Item bị chặn          | Mô tả dependency                                   |
| ------- | ------------------------ | -------------------------------------------------- |
| P1-01   | FE P1-02 (auth UI)       | FE cần auth endpoint để implement login form       |
| P1-02   | FE P1-01 (storefront)    | FE cần catalog API để render product list/PDP      |
| P1-03   | FE tất cả                | Swagger staging giúp FE self-service test endpoint |
| P1-04   | FE P1-04 (checkout)      | FE cần order API để submit COD form                |
| P1-05   | FE P1-05 (order confirm) | FE cần email hoạt động để test order confirmation  |
| P1-06   | FE test/QA               | FE cần seed data để test UI đa dạng sản phẩm       |

### Not now list (anti scope creep)

- Payment gateways (VNPay/Momo/ZaloPay) — defer P3.
- Celery + Redis async queue — sync email OK ở MVP.
- Elasticsearch — PostgreSQL full-text search đủ dùng MVP.
- Social login (Google/Facebook) — defer P3.
- Custom admin frontend — Django Admin đủ dùng MVP.
- WebSocket realtime — không cần ở MVP.
- Kubernetes / advanced orchestration — overkill.
- Multi-vendor marketplace — hoàn toàn ngoài MVP.

### Delivery readiness checklist (per priority)

- P0 done:
  - [ ] Scope và contract locked + confirmed bởi FE
  - [ ] Docker Compose local chạy không lỗi
  - [ ] CI GitHub Actions pass (lint + test)
  - [ ] Database models + migrations apply clean
- P1 done:
  - [ ] Auth API hoạt động end-to-end (token flow)
  - [ ] Catalog API trả đúng shape, staging có seed data
  - [ ] Swagger UI live trên staging
  - [ ] Order API tạo đơn COD thành công + email gửi thật
- P2 done:
  - [ ] Test coverage ≥ 80% cho `apps/`
  - [ ] Security hardening pass (rate limit, CORS, auth gate)
  - [ ] Django Admin vận hành đơn và sản phẩm không cần dev
  - [ ] Production readiness pass (health, Sentry, backup)

## Acceptance Criteria

- Backlog có thứ tự ưu tiên tuyệt đối và triển khai được ngay.
- Mỗi item có đầy đủ objective/output/dependency/owner/acceptance.
- FE dependency rõ ràng để không có trường hợp "BE nói xong rồi" nhưng FE vẫn bị chặn.
- Not-now list kiểm soát scope creep.

## Open Risks / Next Actions

Open risks:

- Nhảy task P1 theo yêu cầu ad-hoc làm vỡ thứ tự ưu tiên.
- Contract thay đổi sau khi FE đã implement → rework cả hai bên.
- Chưa đủ seed data thực tế để test edge case catalog.

Next actions:

- [ ] Tạo board theo cột P0/P1/P2/P3 và trạng thái gate.
- [ ] Gán owner cụ thể cho từng backlog item.
- [ ] Chốt SLA xử lý blocker cho item critical path.
- [ ] Review lại not-now list mỗi lần có change request từ FE.
- [ ] Publish link Swagger staging ngay sau khi P1-03 done.
