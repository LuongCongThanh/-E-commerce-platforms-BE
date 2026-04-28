# 03. Technical Stack, Skills And Versions — Backend (VI)

Last updated: 2026-04-25  
Source of truth: `requirements/base.txt`, `requirements/development.txt`, engineering conventions in this doc set  
Owner: BE Lead + Tech Lead

## TOC

- [Purpose](#purpose)
- [Scope](#scope)
- [Decisions](#decisions)
- [Detailed Spec](#detailed-spec)
- [Acceptance Criteria](#acceptance-criteria)
- [Open Risks / Next Actions](#open-risks--next-actions)

## Summary Table

| Item           | Value                                              |
| -------------- | -------------------------------------------------- |
| Framework core | Django 5.1 + Django REST Framework 3.15+           |
| Auth           | djangorestframework-simplejwt 5.x + django-allauth |
| Database       | PostgreSQL 16 (Neon managed)                       |
| API Docs       | drf-spectacular 0.27+                              |
| Testing        | pytest-django 4.x + factory-boy 3.x                |
| Monitoring     | sentry-sdk 2.x                                     |

## Purpose

Tài liệu này khóa cấu hình kỹ thuật chính thức cho backend: công nghệ, phiên bản, lý do chọn, skill BE cần dùng theo phase, quality gates kỹ thuật, và decision log cho hạng mục defer.

## Scope

Bao gồm:

- Version matrix cho runtime và dev dependencies.
- Tech stack theo layer và rationale.
- Skill matrix tập trung BE/QA (must-have/nice-to-have) theo phase.
- Quality gates bắt buộc: lint/test/build/deploy.
- Decision log: chọn ngay và defer.

Không bao gồm:

- Hướng dẫn cài đặt chi tiết từng package (xem `04-project-structure`).
- Skill matrix đầy đủ cho mọi role ngoài BE/QA.

## Decisions

- Nếu docs cũ mâu thuẫn phiên bản, ưu tiên `requirements/base.txt`.
- Ưu tiên stack Django thuần túy — không mix Node/Express vào BE.
- Django Admin là admin interface MVP — không build custom frontend.
- SimpleJWT stateless — không dùng session-based auth.
- Swagger tự động (drf-spectacular) — không viết tay OpenAPI spec.
- Quality gates là tiêu chuẩn merge/release tối thiểu — không được bỏ qua.

## Detailed Spec

### Technical stack by layer

| Layer                | Technology                          | Why this choice                                                    |
| -------------------- | ----------------------------------- | ------------------------------------------------------------------ |
| App framework        | Django 5.1                          | Admin panel sẵn, ORM mạnh, ecosystem lớn, battle-tested production |
| REST API             | Django REST Framework 3.15+         | Serializers, ViewSets, Pagination, Throttling out-of-the-box       |
| Authentication       | djangorestframework-simplejwt 5.x   | Stateless JWT, refresh token rotation, blacklist support           |
| Social auth (phase2) | django-allauth 0.63+                | Google/Facebook OAuth — defer sang Phase 2                         |
| API Documentation    | drf-spectacular 0.27+               | Auto-generate OpenAPI 3 schema từ code, Swagger UI + ReDoc         |
| Database ORM         | Django ORM (built-in)               | Type-safe queries, migration system, admin integration             |
| Database             | PostgreSQL 16 (Neon)                | Managed, free tier đủ dùng MVP, dashboard trực quan                |
| Media storage        | Cloudinary SDK + django-cloudinary  | CDN sẵn, resize ảnh auto, không cần tự host                        |
| Email                | Django EmailBackend (SMTP)          | Gmail/Mailgun free — đủ cho transactional email MVP                |
| Task queue           | Sync in-request (MVP)               | Celery defer sang Phase 2 — MVP sync OK                            |
| Caching              | None (MVP)                          | Redis/Memcached defer sang Phase 2                                 |
| Testing              | pytest-django 4.x + factory-boy 3.x | Fast, Django-native, fixture tốt với Factory Boy                   |
| Code quality         | ruff + black + isort                | Nhanh hơn flake8+pylint, format nhất quán                          |
| Monitoring           | sentry-sdk 2.x (Django integration) | Error tracking production realtime, breadcrumbs, performance       |
| Containerization     | Docker + Docker Compose             | 1-lệnh chạy toàn bộ stack local                                    |
| CI/CD                | GitHub Actions                      | Auto test + deploy khi push main                                   |
| Deployment           | Railway                             | Docker support, free $5 credit/tháng, simple env vars              |

### Selected version matrix

#### Runtime dependencies

| Package                       | Version |
| ----------------------------- | ------- |
| Django                        | ~=5.1   |
| djangorestframework           | ~=3.15  |
| djangorestframework-simplejwt | ~=5.3   |
| django-allauth                | ~=0.63  |
| drf-spectacular               | ~=0.27  |
| psycopg2-binary               | ~=2.9   |
| django-cloudinary-storage     | ~=0.3   |
| cloudinary                    | ~=1.40  |
| sentry-sdk                    | ~=2.0   |
| django-cors-headers           | ~=4.3   |
| python-decouple               | ~=3.8   |
| Pillow                        | ~=10.0  |
| gunicorn                      | ~=22.0  |

#### Dev dependencies

| Package              | Version |
| -------------------- | ------- |
| pytest               | ~=8.0   |
| pytest-django        | ~=4.8   |
| factory-boy          | ~=3.3   |
| faker                | ~=24.0  |
| pytest-cov           | ~=5.0   |
| ruff                 | ~=0.4   |
| black                | ~=24.0  |
| isort                | ~=5.13  |
| django-debug-toolbar | ~=4.3   |
| ipython              | ~=8.0   |

### Skill matrix focused on BE và QA

#### BE skills

Must-have:

- `backend-development-feature-development`
- `backend-dev-guidelines`
- `api-design-principles`
- `database-design`
- `postgresql`
- `auth-implementation-patterns`
- `backend-security-coder`

Nice-to-have:

- `backend-architect`
- `api-security-best-practices`
- `api-security-testing`
- `database-optimizer` (phase 2)
- `docker-expert`

#### QA skills

Must-have:

- `testing-qa`
- `unit-testing-test-generate`
- `systematic-debugging`

Nice-to-have:

- `e2e-testing` (integration với FE)
- `k6-load-testing` (phase 2)
- `api-security-testing`

### Skill usage by phase

| Phase              | BE focus skills                                                             | QA focus skills                   |
| ------------------ | --------------------------------------------------------------------------- | --------------------------------- |
| Setup & models     | backend-dev-guidelines, database-design, postgresql                         | unit-testing-test-generate        |
| API implementation | api-design-principles, auth-implementation-patterns, backend-security-coder | testing-qa, systematic-debugging  |
| Admin & hardening  | backend-architect, api-security-best-practices                              | api-security-testing, e2e-testing |
| Release            | docker-expert, deployment-engineer                                          | k6-load-testing, security-auditor |

### Technical quality gates

Gate rules before merge:

- `ruff check .` must pass (no lint errors).
- `black --check .` must pass.
- `pytest --cov=. --cov-report=term-missing` phải pass, coverage ≥ 80% cho `apps/`.
- Migration conflict check: `python manage.py migrate --check` must pass.
- Không có hardcoded secret trong code (ruff rule hoặc pre-commit hook).

Gate rules before release:

- Regression test cho auth + catalog + order pass.
- Không còn lỗi severity cao trong Sentry staging.
- `python manage.py check --deploy` pass.
- Backup database verify.
- Health check endpoint `GET /api/health/` trả `200 OK`.

### Decision log (chosen vs deferred)

Chosen now:

- Django Admin làm admin interface MVP.
- SimpleJWT stateless auth.
- COD-only payment.
- Sync email send (không dùng Celery).
- drf-spectacular auto-generate Swagger.
- pytest-django cho unit/integration test.

Deferred to phase later:

- Celery + Redis (async tasks, email queue).
- Elasticsearch (full-text search nâng cao).
- Social login (Google/Facebook).
- Payment gateways (VNPay/Momo/ZaloPay).
- Custom admin frontend (thay Django Admin).
- Kubernetes (overkill cho MVP solo).
- Rate limiting nâng cao (Redis-backed).

### Deferred stack (Phase 2+)

| Bỏ qua ở MVP  | Lý do                                                         |
| ------------- | ------------------------------------------------------------- |
| Redis         | Tiết kiệm 3–4 ngày setup. Thêm khi cần cache/queue Celery     |
| Elasticsearch | PostgreSQL full-text search đủ dùng cho MVP < 10.000 sản phẩm |
| Celery        | Chưa cần async task queue — sync email OK ở MVP               |
| Kubernetes    | Overkill cho 1 developer, 1 project nhỏ                       |

### Glossary (VI-EN sync)

| Term               | Meaning                                                              |
| ------------------ | -------------------------------------------------------------------- |
| MVP                | Phiên bản khả dụng tối thiểu để vận hành thật                        |
| API contract       | Giao kèo request/response shape giữa FE và BE                        |
| select_for_update  | Django ORM lock row để tránh race condition khi trừ tồn kho          |
| atomic transaction | Django `transaction.atomic()` — rollback toàn bộ nếu 1 bước lỗi      |
| Quality gate       | Điều kiện bắt buộc trước merge/release                               |
| drf-spectacular    | Package tự động sinh OpenAPI 3 schema từ DRF code                    |
| Factory Boy        | Thư viện tạo test fixture/data cho Django models                     |
| Idempotency        | Gọi API 2 lần cho cùng request → kết quả như nhau, không tạo đơn kép |

## Acceptance Criteria

- Version matrix phản ánh đúng `requirements/base.txt` hiện tại.
- Skill matrix BE/QA có phân must-have/nice-to-have và theo phase.
- Quality gates mô tả được tiêu chuẩn merge/release cho BE.
- Decision log thể hiện rõ chọn ngay và defer.

## Open Risks / Next Actions

Open risks:

- Package drift khi nâng cấp không cập nhật docs.
- Team bỏ qua quality gate khi deadline gấp.
- psycopg2-binary có thể cần psycopg2 thuần trên Railway (build khác).

Next actions:

- [ ] Tạo `requirements/base.txt`, `requirements/development.txt`, `requirements/production.txt`.
- [ ] Thêm check định kỳ đối chiếu version docs với requirements files.
- [ ] Đưa quality gate vào PR template.
- [ ] Review lại shortlist skills mỗi cuối phase.
- [ ] Cập nhật glossary khi thêm thuật ngữ mới.
