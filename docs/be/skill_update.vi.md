# Cập nhật kỹ năng — Backend (VI)

Nguồn lọc: `.skills/antigravity-awesome-skills/skills` và `./03-technical-stack-skills-and-versions.vi.md` (Cập nhật gần nhất: 2026-04-25).

---

## Bảng 1: Skill ưu tiên cho dự án BE

| Khu vực      | Tên skill                                 | Vì sao phù hợp với dự án                                              | Cách sử dụng trong dự án                                            | Trường hợp nên sử dụng                                        | Mức độ bao quát |
| ------------ | ----------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------- | --------------- |
| BE Core      | `backend-development-feature-development` | Orchestrate end-to-end BE feature từ requirement đến deploy           | Skill nền cho thiết kế và triển khai feature BE hằng ngày           | Mọi task BE từ model → serializer → view → test               | Very High       |
| BE Core      | `backend-dev-guidelines`                  | Hướng dẫn production-grade cho routes, controllers, services, DB      | Dùng khi code views, services, middleware và database access        | Mỗi PR BE liên quan API hoặc data layer                       | Very High       |
| API Design   | `api-design-principles`                   | Best practices REST/GraphQL, naming, versioning, pagination           | Thiết kế URL, response shape, error handling chuẩn                  | Khi thêm endpoint mới hoặc đổi contract                       | High            |
| Database     | `database-design`                         | Schema design, indexing, ORM selection, serverless DB                 | Thiết kế models, index strategy, migration plan                     | Khi thêm model mới hoặc tối ưu query                          | High            |
| Database     | `postgresql`                              | PostgreSQL best-practices, data types, indexing, constraints, perf    | Viết migration, thiết kế index, tối ưu query phức tạp               | Khi có bottleneck DB hoặc thiết kế schema                     | High            |
| Auth         | `auth-implementation-patterns`            | JWT/OIDC, token lifecycle, RBAC, session management an toàn           | Thiết kế JWT flow, refresh rotation, permission classes             | Khi làm auth API, refactor auth, session/role handling        | High            |
| Security     | `backend-security-coder`                  | Input validation, authentication, API security, DB protection an toàn | Implement validation, permission gate, error handling defensive     | API route, auth handler, webhook, server action               | High            |
| Security     | `api-security-best-practices`             | Auth, authz, input validation, rate limiting, API vulnerabilities     | Thiết kế/review endpoint, thêm rate limit, chuẩn error handling     | Cart, checkout, order, payment/webhook, user/account endpoint | High            |
| Architecture | `backend-architect`                       | Scalable API design, microservices, distributed systems patterns      | Dùng khi thiết kế pattern/module boundary phức tạp                  | Khi đổi architecture, phase 2 planning, high-impact decisions | Medium          |
| Testing      | `testing-qa`                              | Strategy unit/integration/e2e toàn diện                               | Lập test plan, dựng bộ test theo quality gate                       | Khi lập test plan sprint/release hoặc review test coverage    | High            |
| Testing      | `unit-testing-test-generate`              | Generate comprehensive unit tests với coverage và edge cases          | Tạo test cho service layer, model methods, utility functions        | PR thiếu test hoặc coverage dưới ngưỡng                       | High            |
| Testing      | `systematic-debugging`                    | Trace từ symptom đến root cause trước khi fix                         | Dùng khi debug 500 error, race condition, flaky test                | Bug report, test failure, unexpected behavior                 | High            |
| API Security | `api-security-testing`                    | Test REST/GraphQL API: auth, authz, rate limit, input validation      | Validate endpoint trước khi expose hoặc đổi contract                | Sau implement endpoint mới hoặc trước release                 | High            |
| Code Quality | `lint-and-validate`                       | Bắt buộc chạy validation sau mỗi thay đổi code                        | Tích hợp vào CI: `ruff check`, `black --check`, `pytest --cov`      | Mỗi PR, mỗi lần release                                       | Very High       |
| CI/CD        | `github-actions-templates`                | Production-ready GitHub Actions cho testing, building, deploying      | Dựng workflow lint → test → build Docker → deploy Railway           | Setup CI/CD ban đầu hoặc nâng cấp pipeline                    | High            |
| CI/CD        | `deployment-engineer`                     | CI/CD pipelines, GitOps workflows, deployment automation              | Cấu hình auto-deploy Railway, staging/production separation         | Khi setup CI/CD hoặc troubleshoot deployment                  | Medium          |
| DevOps       | `docker-expert`                           | Container optimization, security hardening, multi-stage builds        | Viết Dockerfile multi-stage, docker-compose.yml cho dev và prod     | Setup Docker ban đầu hoặc optimize build                      | Medium          |
| Monitoring   | `sentry-automation`                       | Quản lý issues/events, cấu hình alerts, track releases                | Setup Sentry DSN, cấu hình alert cho 5xx, theo dõi release          | Sau deploy và trong production monitoring                     | Medium          |
| Code Review  | `code-reviewer`                           | Elite code review cho security, performance, maintainability          | Review PR trước merge, đặc biệt API và service layer                | Trước merge và khi cần quality audit                          | High            |
| Code Review  | `verification-before-completion`          | Không claim xong nếu chưa verify — đặc biệt quan trọng cho BE         | Chạy test + check migration + verify API trước khi báo done         | Sau mỗi task trước khi cập nhật status PR                     | High            |
| Docs/API     | `api-documentation`                       | Workflow sinh OpenAPI spec, developer guides, API docs                | Dùng khi thay đổi endpoint/schema — sync Swagger với implementation | Khi FE-BE handoff bị lệch contract hoặc sau API change        | Medium          |
| Architecture | `architect-review`                        | Review trade-off kiến trúc trước thay đổi lớn                         | Dùng trong design review cho pattern/module boundary change         | Khi đổi app structure, thêm service mới, phase transition     | Medium          |
| Planning     | `writing-plans`                           | Lập kế hoạch đa bước trước khi code                                   | Dùng khi tách epic BE thành task kỹ thuật có dependency             | Feature lớn, migration phức tạp, nhiều phụ thuộc FE/BE        | Medium          |

---

## Bảng 2: Skill security đề xuất cho BE e-commerce

Project e-commerce Django này nên ưu tiên: secure API design, auth/session safety, input validation, dependency hygiene, database protection, và release hardening.

| Khu vực          | Tên skill                                 | Vì sao phù hợp với BE Django                                                    | Cách sử dụng trong dự án                                           | Trường hợp nên sử dụng                                              | Mức độ bao quát |
| ---------------- | ----------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------- | --------------- |
| Security Audit   | `security-auditor`                        | Trace data flow, review auth/authz control, tìm bypass và prioritize finding    | Review feature rủi ro cao: checkout, payment, admin API            | Trước release hoặc trước khi merge auth/order/admin change          | Very High       |
| Backend Security | `backend-security-coder`                  | Secure coding cho input validation, API security, DB protection, error handling | Implement validation, permission classes, defensive error handling | Mọi API route, server action, webhook, auth handler                 | Very High       |
| API Security     | `api-security-best-practices`             | Pattern thiết kế API an toàn: auth, authz, rate limit, error handling           | Áp dụng cho tất cả REST endpoint, đặc biệt order/checkout/user     | Khi tạo endpoint mới, đổi auth logic, thêm rate limit               | High            |
| Auth Security    | `auth-implementation-patterns`            | JWT flow, token rotation, blacklist, RBAC, session security                     | Thiết kế và review toàn bộ auth/permission system                  | Implement JWT, refresh token, admin permission, protected routes    | High            |
| API Testing      | `api-security-testing`                    | Validate auth, authz, rate limiting, input validation của REST API              | Chạy test workflow trước khi expose hoặc đổi endpoint              | Sau implement endpoint mới, trước merge API change                  | High            |
| SAST             | `security-scanning-security-sast`         | Static scan tìm XSS, secret leak, IDOR, path traversal trong Python/Django code | Thêm vào pre-merge check cho security pattern rủi ro               | PR chạm auth, input handling, file upload, webhook, admin view      | High            |
| Dependencies     | `security-scanning-security-dependencies` | Scan CVE trong `requirements.txt`, supply chain risks, license check            | Audit manifest/requirements rồi triage upgrade an toàn             | Update dependency, hardening release, monthly security maintenance  | High            |
| Web Testing      | `web-security-testing`                    | OWASP Top 10 cho API: injection, broken auth, misconfig, IDOR                   | Chạy trên API endpoint quan trọng sau implementation               | Trước production release, sau thay đổi auth/order/checkout          | High            |
| Threat Modeling  | `threat-modeling-expert`                  | STRIDE cho payment, auth, order, admin data — nhận diện attack vector           | Dùng trong design phase cho checkout, admin, payment API           | Trước implement feature nhạy cảm: payment, admin API, customer data | Medium          |
| Hardening        | `security-scanning-security-hardening`    | Điều phối hardening nhiều lớp: app, infra, compliance controls                  | Dùng sau audit để lập kế hoạch và verify hardening                 | Hardening sprint hoặc remediation sau audit                         | Medium          |
| Compliance       | `security-compliance-compliance-check`    | GDPR, PCI-DSS, tuân thủ Nghị định 13/2023/NĐ-CP cho dữ liệu cá nhân             | Map data handling với requirement pháp lý                          | Khi xử lý dữ liệu khách hàng, payment flow, chuẩn bị audit          | Medium          |
| CI Security      | `gha-security-review`                     | Tìm vulnerability trong GitHub Actions: permission, secret, token               | Review workflow CI/CD trước khi merge                              | Khi thêm deployment, test, release hoặc automation workflow         | Medium          |
| Vuln Reference   | `top-web-vulnerabilities`                 | 100 web vulnerability quan trọng nhất — reference cho code review               | Dùng như checklist review endpoint, model, admin                   | Manual security review, audit, dev training                         | Medium          |
| Race Condition   | `007`                                     | Audit tổng quát: threat modeling, OWASP check, hardening, incident response     | Dùng cho comprehensive security review trước launch                | Trước go-live, sau incident, security sprint                        | Medium          |

---

## Bảng 3: Tất cả skill liên quan theo vai trò BE

| Nhóm vai trò | Tên skill                                 | Chức năng                                                        | Cách sử dụng                                                    | Trường hợp nên sử dụng                              |
| ------------ | ----------------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------- |
| BE           | `backend-development-feature-development` | Orchestrate end-to-end BE feature từ requirements đến deployment | Skill nền cho coding BE hằng ngày                               | Mọi task BE liên quan model/serializer/view/service |
| BE           | `backend-dev-guidelines`                  | Senior BE engineer operating production-grade services           | Dùng cho routes, controllers, services, repositories, DB access | Mỗi PR BE                                           |
| BE           | `backend-architect`                       | Scalable API design, microservices, distributed systems          | Design review và pattern decision                               | Kiến trúc phức tạp, multi-module, phase transition  |
| BE           | `api-design-principles`                   | REST/GraphQL API design, naming, versioning, pagination          | Thiết kế và review URL/response/error shape                     | Thêm endpoint mới hoặc đổi contract                 |
| BE           | `database-design`                         | Schema design, indexing strategy, ORM selection                  | Thiết kế models và migration                                    | Model mới hoặc query optimization                   |
| BE           | `postgresql`                              | PostgreSQL best-practices, advanced features, performance        | Migration, indexing, query tuning                               | Bottleneck DB hoặc schema design                    |
| BE           | `auth-implementation-patterns`            | JWT, OIDC, RBAC, session management                              | Auth system design và review                                    | Auth API, permission, session handling              |
| BE           | `backend-security-coder`                  | Secure input validation, API security, DB protection             | Defensive coding patterns                                       | API route, webhook, auth handler                    |
| BE           | `api-security-best-practices`             | Auth, authz, rate limiting, API vulnerabilities                  | Thiết kế/review REST endpoint                                   | Cart, checkout, order, user, admin endpoint         |
| DevOps       | `docker-expert`                           | Container optimization, security, multi-stage builds             | Dockerfile và docker-compose.yml                                | Setup Docker ban đầu hoặc optimize                  |
| DevOps       | `github-actions-templates`                | Production-ready GitHub Actions workflows                        | CI: lint → test → build → deploy                                | Setup CI/CD hoặc nâng cấp pipeline                  |
| DevOps       | `deployment-engineer`                     | CI/CD pipelines, GitOps, deployment automation                   | Auto-deploy Railway, staging/production                         | CI/CD setup hoặc troubleshoot                       |
| DevOps       | `deployment-pipeline-design`              | Multi-stage CI/CD với approval gates                             | Thiết kế pipeline phân tầng staging → production                | Nâng cấp pipeline lên multi-env                     |
| DevOps       | `sentry-automation`                       | Manage issues/events, configure alerts, track releases           | Setup Sentry, alert 5xx, release tracking                       | Sau deploy và trong production monitoring           |
| DevOps       | `lint-and-validate`                       | Validation tools sau mỗi thay đổi code                           | Tích hợp vào CI gate                                            | Mỗi PR và release                                   |
| QA           | `testing-qa`                              | Comprehensive testing: unit, integration, e2e, QA                | Lập test strategy và plan                                       | Test plan sprint/release                            |
| QA           | `unit-testing-test-generate`              | Generate comprehensive unit tests                                | Tạo test cho service/model/utils                                | PR thiếu test hoặc coverage thấp                    |
| QA           | `systematic-debugging`                    | Trace từ symptom đến root cause                                  | Debug 500 error, race condition, flaky test                     | Bug report, test failure                            |
| QA           | `api-security-testing`                    | Test REST/GraphQL: auth, authz, rate limit, validation           | Validate endpoint trước expose/merge                            | Sau implement endpoint mới                          |
| QA           | `k6-load-testing`                         | Load testing cho API: realistic scenarios, CI/CD integration     | Test API performance dưới tải                                   | Trước release, sau P2 hardening                     |
| BA           | `api-documentation`                       | OpenAPI spec, developer guides, API documentation                | Sync Swagger với implementation                                 | Sau API change, FE-BE handoff                       |
| BA           | `writing-plans`                           | Lập kế hoạch đa bước                                             | Tách epic BE thành task kỹ thuật                                | Feature lớn, nhiều phụ thuộc                        |
| BA           | `acceptance-orchestrator`                 | End-to-end từ issue đến acceptance với minimal re-intervention   | Chốt acceptance criteria cho BE feature                         | Planning/scope lock                                 |
| BA           | `architect-review`                        | Software architecture trade-off review                           | Design review trước thay đổi lớn                                | Đổi pattern/module boundary                         |
| Code Review  | `code-reviewer`                           | Elite code review: security, performance, maintainability        | Review PR trước merge                                           | Mọi PR BE                                           |
| Code Review  | `verification-before-completion`          | Không claim xong nếu chưa verify                                 | Chạy test + check migration + verify API                        | Trước update status PR                              |
| Code Review  | `find-bugs`                               | Find bugs, security vulnerabilities trong local branch changes   | Review changes trong branch hiện tại                            | PR review, security audit, bug investigation        |
| Code Review  | `code-review-checklist`                   | Checklist toàn diện: functionality, security, performance        | Checklist chuẩn cho PR review                                   | Trước merge                                         |

---

## Bộ skill bao quát đề xuất cho BE

Nếu cần bộ skill gọn nhưng bao quát đa số task BE hằng ngày:

**Core BE (bắt buộc):**

- `backend-development-feature-development`
- `backend-dev-guidelines`
- `api-design-principles`
- `database-design`
- `postgresql`
- `auth-implementation-patterns`

**Quality & Testing (bắt buộc):**

- `testing-qa`
- `unit-testing-test-generate`
- `lint-and-validate`
- `verification-before-completion`

**DevOps (bắt buộc):**

- `github-actions-templates`
- `docker-expert`
- `sentry-automation`

**Khi làm task security, bổ sung:**

- `backend-security-coder`
- `api-security-best-practices`
- `auth-implementation-patterns`
- `api-security-testing`
- `security-scanning-security-sast`
- `security-scanning-security-dependencies`
- `web-security-testing`
