# Skill Mapping cho MVP E-Commerce

> Tài liệu này tổng hợp các skill trong `E:\my-pj\learn-python\antigravity-awesome-skills\skills`
> phù hợp với dự án MVP E-Commerce dựa trên 3 tài liệu:
>
> - [overview.md](./overview.md)
> - [mvp-plan.md](./mvp-plan.md)
> - [mvp-checklist.md](./mvp-checklist.md)

## 1. Bối cảnh dự án

Scope hiện tại của dự án:

- Frontend: `Next.js 15`, `TypeScript`, `Tailwind`, `TanStack Query`, `Zod`, `Zustand`
- Backend: `Django`, `Django REST Framework`, `PostgreSQL`
- Core flow: `catalog`, `search`, `auth`, `cart`, `checkout COD`, `orders`, `admin`
- Non-functional: `responsive`, `SEO`, `performance`, `security`, `testing`, `deploy`

Vì vậy, skill được chia theo 2 nhóm:

- `Domain skills`: skill phục vụ trực tiếp cho nghiệp vụ và implementation
- `Tool / review skills`: skill phục vụ review, audit, debugging, verification, quality control

## 2. Cách dùng tài liệu này

- Nếu đang build tính năng theo vai trò, ưu tiên xem section của role đó
- Nếu đang review chất lượng hoặc xử lý bug, xem thêm nhóm `Tool / review skills`
- Nếu muốn tối giản, dùng section `Shortlist đề xuất`

## 3. BA

### Domain skills

- [acceptance-orchestrator](../../antigravity-awesome-skills/skills/acceptance-orchestrator/SKILL.md)
- [writing-plans](../../antigravity-awesome-skills/skills/writing-plans/SKILL.md)
- [api-documentation](../../antigravity-awesome-skills/skills/api-documentation/SKILL.md)
- [api-documentation-generator](../../antigravity-awesome-skills/skills/api-documentation-generator/SKILL.md)
- [api-documenter](../../antigravity-awesome-skills/skills/api-documenter/SKILL.md)
- [wiki-page-writer](../../antigravity-awesome-skills/skills/wiki-page-writer/SKILL.md)
- [wiki-qa](../../antigravity-awesome-skills/skills/wiki-qa/SKILL.md)
- [startup-business-analyst-business-case](../../antigravity-awesome-skills/skills/startup-business-analyst-business-case/SKILL.md)
- [startup-business-analyst-market-opportunity](../../antigravity-awesome-skills/skills/startup-business-analyst-market-opportunity/SKILL.md)
- [analytics-tracking](../../antigravity-awesome-skills/skills/analytics-tracking/SKILL.md)
- [ai-seo](../../antigravity-awesome-skills/skills/ai-seo/SKILL.md)

### Tool / review skills

- [architect-review](../../antigravity-awesome-skills/skills/architect-review/SKILL.md)
- [analyze-project](../../antigravity-awesome-skills/skills/analyze-project/SKILL.md)
- [technical-change-tracker](../../antigravity-awesome-skills/skills/technical-change-tracker/SKILL.md)
- [verification-before-completion](../../antigravity-awesome-skills/skills/verification-before-completion/SKILL.md)

### Gợi ý dùng cho BA trong dự án này

- Chốt scope và acceptance criteria: [acceptance-orchestrator](../../antigravity-awesome-skills/skills/acceptance-orchestrator/SKILL.md), [writing-plans](../../antigravity-awesome-skills/skills/writing-plans/SKILL.md)
- Viết API notes, handoff docs, flow docs: [api-documentation](../../antigravity-awesome-skills/skills/api-documentation/SKILL.md), [api-documenter](../../antigravity-awesome-skills/skills/api-documenter/SKILL.md), [wiki-page-writer](../../antigravity-awesome-skills/skills/wiki-page-writer/SKILL.md)
- Review mức độ bám scope MVP: [architect-review](../../antigravity-awesome-skills/skills/architect-review/SKILL.md), [analyze-project](../../antigravity-awesome-skills/skills/analyze-project/SKILL.md)

## 4. QA

### Domain skills

- [testing-qa](../../antigravity-awesome-skills/skills/testing-qa/SKILL.md)
- [webapp-testing](../../antigravity-awesome-skills/skills/webapp-testing/SKILL.md)
- [test-automator](../../antigravity-awesome-skills/skills/test-automator/SKILL.md)
- [e2e-testing](../../antigravity-awesome-skills/skills/e2e-testing/SKILL.md)
- [e2e-testing-patterns](../../antigravity-awesome-skills/skills/e2e-testing-patterns/SKILL.md)
- [playwright-skill](../../antigravity-awesome-skills/skills/playwright-skill/SKILL.md)
- [testing-patterns](../../antigravity-awesome-skills/skills/testing-patterns/SKILL.md)
- [unit-testing-test-generate](../../antigravity-awesome-skills/skills/unit-testing-test-generate/SKILL.md)
- [tdd-orchestrator](../../antigravity-awesome-skills/skills/tdd-orchestrator/SKILL.md)
- [test-driven-development](../../antigravity-awesome-skills/skills/test-driven-development/SKILL.md)
- [api-testing-observability-api-mock](../../antigravity-awesome-skills/skills/api-testing-observability-api-mock/SKILL.md)

### Tool / review skills

- [verification-before-completion](../../antigravity-awesome-skills/skills/verification-before-completion/SKILL.md)
- [test-fixing](../../antigravity-awesome-skills/skills/test-fixing/SKILL.md)
- [systematic-debugging](../../antigravity-awesome-skills/skills/systematic-debugging/SKILL.md)
- [accessibility-compliance-accessibility-audit](../../antigravity-awesome-skills/skills/accessibility-compliance-accessibility-audit/SKILL.md)
- [screen-reader-testing](../../antigravity-awesome-skills/skills/screen-reader-testing/SKILL.md)
- [web-security-testing](../../antigravity-awesome-skills/skills/web-security-testing/SKILL.md)
- [api-security-testing](../../antigravity-awesome-skills/skills/api-security-testing/SKILL.md)

### Gợi ý dùng cho QA trong dự án này

- Test flow chính của MVP: [testing-qa](../../antigravity-awesome-skills/skills/testing-qa/SKILL.md), [webapp-testing](../../antigravity-awesome-skills/skills/webapp-testing/SKILL.md), [playwright-skill](../../antigravity-awesome-skills/skills/playwright-skill/SKILL.md)
- Viết E2E cho đăng nhập, giỏ hàng, checkout: [e2e-testing](../../antigravity-awesome-skills/skills/e2e-testing/SKILL.md), [e2e-testing-patterns](../../antigravity-awesome-skills/skills/e2e-testing-patterns/SKILL.md)
- Kiểm tra readiness trước release: [verification-before-completion](../../antigravity-awesome-skills/skills/verification-before-completion/SKILL.md)
- Audit phụ trợ quan trọng: [accessibility-compliance-accessibility-audit](../../antigravity-awesome-skills/skills/accessibility-compliance-accessibility-audit/SKILL.md), [api-security-testing](../../antigravity-awesome-skills/skills/api-security-testing/SKILL.md)

## 5. FE

### Domain skills

- [react-nextjs-development](../../antigravity-awesome-skills/skills/react-nextjs-development/SKILL.md)
- [nextjs-app-router-patterns](../../antigravity-awesome-skills/skills/nextjs-app-router-patterns/SKILL.md)
- [nextjs-best-practices](../../antigravity-awesome-skills/skills/nextjs-best-practices/SKILL.md)
- [tailwind-patterns](../../antigravity-awesome-skills/skills/tailwind-patterns/SKILL.md)
- [tailwind-design-system](../../antigravity-awesome-skills/skills/tailwind-design-system/SKILL.md)
- [tanstack-query-expert](../../antigravity-awesome-skills/skills/tanstack-query-expert/SKILL.md)
- [zod-validation-expert](../../antigravity-awesome-skills/skills/zod-validation-expert/SKILL.md)
- [zustand-store-ts](../../antigravity-awesome-skills/skills/zustand-store-ts/SKILL.md)
- [typescript-expert](../../antigravity-awesome-skills/skills/typescript-expert/SKILL.md)
- [typescript-pro](../../antigravity-awesome-skills/skills/typescript-pro/SKILL.md)
- [ui-page](../../antigravity-awesome-skills/skills/ui-page/SKILL.md)
- [ui-component](../../antigravity-awesome-skills/skills/ui-component/SKILL.md)
- [ui-pattern](../../antigravity-awesome-skills/skills/ui-pattern/SKILL.md)
- [frontend-dev-guidelines](../../antigravity-awesome-skills/skills/frontend-dev-guidelines/SKILL.md)
- [frontend-developer](../../antigravity-awesome-skills/skills/frontend-developer/SKILL.md)
- [senior-frontend](../../antigravity-awesome-skills/skills/senior-frontend/SKILL.md)
- [ux-flow](../../antigravity-awesome-skills/skills/ux-flow/SKILL.md)
- [ux-audit](../../antigravity-awesome-skills/skills/ux-audit/SKILL.md)
- [ai-seo](../../antigravity-awesome-skills/skills/ai-seo/SKILL.md)

### Tool / review skills

- [ui-review](../../antigravity-awesome-skills/skills/ui-review/SKILL.md)
- [systematic-debugging](../../antigravity-awesome-skills/skills/systematic-debugging/SKILL.md)
- [verification-before-completion](../../antigravity-awesome-skills/skills/verification-before-completion/SKILL.md)
- [web-performance-optimization](../../antigravity-awesome-skills/skills/web-performance-optimization/SKILL.md)
- [accessibility-compliance-accessibility-audit](../../antigravity-awesome-skills/skills/accessibility-compliance-accessibility-audit/SKILL.md)
- [fixing-accessibility](../../antigravity-awesome-skills/skills/fixing-accessibility/SKILL.md)
- [fixing-motion-performance](../../antigravity-awesome-skills/skills/fixing-motion-performance/SKILL.md)

### Gợi ý dùng cho FE trong dự án này

- Dựng app theo stack đang chọn: [react-nextjs-development](../../antigravity-awesome-skills/skills/react-nextjs-development/SKILL.md), [nextjs-app-router-patterns](../../antigravity-awesome-skills/skills/nextjs-app-router-patterns/SKILL.md)
- Làm UI nhanh và đồng bộ: [tailwind-patterns](../../antigravity-awesome-skills/skills/tailwind-patterns/SKILL.md), [ui-page](../../antigravity-awesome-skills/skills/ui-page/SKILL.md), [ui-component](../../antigravity-awesome-skills/skills/ui-component/SKILL.md)
- Form, state, fetching: [zod-validation-expert](../../antigravity-awesome-skills/skills/zod-validation-expert/SKILL.md), [zustand-store-ts](../../antigravity-awesome-skills/skills/zustand-store-ts/SKILL.md), [tanstack-query-expert](../../antigravity-awesome-skills/skills/tanstack-query-expert/SKILL.md)
- Review chất lượng FE trước merge: [ui-review](../../antigravity-awesome-skills/skills/ui-review/SKILL.md), [web-performance-optimization](../../antigravity-awesome-skills/skills/web-performance-optimization/SKILL.md)

## 6. BE

### Domain skills

- [backend-architect](../../antigravity-awesome-skills/skills/backend-architect/SKILL.md)
- [backend-dev-guidelines](../../antigravity-awesome-skills/skills/backend-dev-guidelines/SKILL.md)
- [backend-development-feature-development](../../antigravity-awesome-skills/skills/backend-development-feature-development/SKILL.md)
- [api-design-principles](../../antigravity-awesome-skills/skills/api-design-principles/SKILL.md)
- [api-patterns](../../antigravity-awesome-skills/skills/api-patterns/SKILL.md)
- [api-endpoint-builder](../../antigravity-awesome-skills/skills/api-endpoint-builder/SKILL.md)
- [auth-implementation-patterns](../../antigravity-awesome-skills/skills/auth-implementation-patterns/SKILL.md)
- [postgresql](../../antigravity-awesome-skills/skills/postgresql/SKILL.md)
- [postgres-best-practices](../../antigravity-awesome-skills/skills/postgres-best-practices/SKILL.md)
- [sql-optimization-patterns](../../antigravity-awesome-skills/skills/sql-optimization-patterns/SKILL.md)
- [database-migrations-sql-migrations](../../antigravity-awesome-skills/skills/database-migrations-sql-migrations/SKILL.md)
- [neon-postgres](../../antigravity-awesome-skills/skills/neon-postgres/SKILL.md)
- [using-neon](../../antigravity-awesome-skills/skills/using-neon/SKILL.md)
- [docker-expert](../../antigravity-awesome-skills/skills/docker-expert/SKILL.md)
- [django-pro](../../antigravity-awesome-skills/skills/django-pro/SKILL.md)

### Tool / review skills

- [architect-review](../../antigravity-awesome-skills/skills/architect-review/SKILL.md)
- [systematic-debugging](../../antigravity-awesome-skills/skills/systematic-debugging/SKILL.md)
- [verification-before-completion](../../antigravity-awesome-skills/skills/verification-before-completion/SKILL.md)
- [api-security-best-practices](../../antigravity-awesome-skills/skills/api-security-best-practices/SKILL.md)
- [api-security-testing](../../antigravity-awesome-skills/skills/api-security-testing/SKILL.md)
- [django-perf-review](../../antigravity-awesome-skills/skills/django-perf-review/SKILL.md)
- [django-access-review](../../antigravity-awesome-skills/skills/django-access-review/SKILL.md)

### Gợi ý dùng cho BE trong dự án này

- Thiết kế API và flow nghiệp vụ: [backend-architect](../../antigravity-awesome-skills/skills/backend-architect/SKILL.md), [api-design-principles](../../antigravity-awesome-skills/skills/api-design-principles/SKILL.md), [api-endpoint-builder](../../antigravity-awesome-skills/skills/api-endpoint-builder/SKILL.md)
- Auth và bảo mật: [auth-implementation-patterns](../../antigravity-awesome-skills/skills/auth-implementation-patterns/SKILL.md), [api-security-best-practices](../../antigravity-awesome-skills/skills/api-security-best-practices/SKILL.md)
- DB và deploy local/prod: [postgresql](../../antigravity-awesome-skills/skills/postgresql/SKILL.md), [using-neon](../../antigravity-awesome-skills/skills/using-neon/SKILL.md), [docker-expert](../../antigravity-awesome-skills/skills/docker-expert/SKILL.md)
- Review backend trước release: [django-perf-review](../../antigravity-awesome-skills/skills/django-perf-review/SKILL.md), [api-security-testing](../../antigravity-awesome-skills/skills/api-security-testing/SKILL.md)

## 7. Nhóm tool / review dùng chung cho cả team

Các skill dưới đây không gắn chặt với một role, nhưng rất hữu ích trong quá trình build MVP:

- [analyze-project](../../antigravity-awesome-skills/skills/analyze-project/SKILL.md)
- [architect-review](../../antigravity-awesome-skills/skills/architect-review/SKILL.md)
- [ui-review](../../antigravity-awesome-skills/skills/ui-review/SKILL.md)
- [systematic-debugging](../../antigravity-awesome-skills/skills/systematic-debugging/SKILL.md)
- [verification-before-completion](../../antigravity-awesome-skills/skills/verification-before-completion/SKILL.md)
- [technical-change-tracker](../../antigravity-awesome-skills/skills/technical-change-tracker/SKILL.md)
- [test-fixing](../../antigravity-awesome-skills/skills/test-fixing/SKILL.md)
- [testing-patterns](../../antigravity-awesome-skills/skills/testing-patterns/SKILL.md)
- [web-performance-optimization](../../antigravity-awesome-skills/skills/web-performance-optimization/SKILL.md)
- [accessibility-compliance-accessibility-audit](../../antigravity-awesome-skills/skills/accessibility-compliance-accessibility-audit/SKILL.md)
- [api-security-testing](../../antigravity-awesome-skills/skills/api-security-testing/SKILL.md)
- [web-security-testing](../../antigravity-awesome-skills/skills/web-security-testing/SKILL.md)
- [django-perf-review](../../antigravity-awesome-skills/skills/django-perf-review/SKILL.md)
- [django-access-review](../../antigravity-awesome-skills/skills/django-access-review/SKILL.md)

## 8. Shortlist đề xuất

Nếu muốn giữ bộ skill gọn nhưng mạnh, có thể ưu tiên:

Mẹo: các skill trong shortlist đã được gắn link đầy đủ ở các section phía trên.

### BA shortlist

- `acceptance-orchestrator`
- `writing-plans`
- `api-documentation`
- `wiki-page-writer`
- `architect-review`

### QA shortlist

- `testing-qa`
- `webapp-testing`
- `playwright-skill`
- `e2e-testing`
- `verification-before-completion`

### FE shortlist

- `react-nextjs-development`
- `nextjs-app-router-patterns`
- `tailwind-patterns`
- `tanstack-query-expert`
- `zod-validation-expert`
- `zustand-store-ts`
- `ui-review`

### BE shortlist

- `backend-architect`
- `django-pro`
- `api-design-principles`
- `api-endpoint-builder`
- `auth-implementation-patterns`
- `postgresql`
- `api-security-testing`

## 9. Đề xuất áp dụng theo giai đoạn MVP

### Giai đoạn 1: Planning và setup

- BA: `acceptance-orchestrator`, `writing-plans`
- FE: `react-nextjs-development`, `nextjs-app-router-patterns`
- BE: `backend-architect`, `django-pro`, `api-design-principles`
- QA: `testing-qa`

### Giai đoạn 2: Build core features

- FE: `tailwind-patterns`, `tanstack-query-expert`, `zod-validation-expert`, `zustand-store-ts`
- BE: `api-endpoint-builder`, `auth-implementation-patterns`, `postgresql`
- QA: `webapp-testing`, `playwright-skill`, `e2e-testing`

### Giai đoạn 3: Hardening và release

- FE: `ui-review`, `web-performance-optimization`
- BE: `api-security-testing`, `django-perf-review`, `django-access-review`
- QA: `verification-before-completion`, `test-fixing`, `accessibility-compliance-accessibility-audit`
- BA: `architect-review`, `technical-change-tracker`

## 10. Ghi chú

- Danh sách này được chọn theo mức độ phù hợp với scope MVP hiện tại, không phải toàn bộ skill tốt nhất trong kho skill
- Một số skill có thể trùng vùng trách nhiệm, nên không nhất thiết dùng hết cùng lúc
- Khi team đã ổn định workflow, có thể tách riêng thành 2 danh mục:
  - `core execution skills`
  - `review / audit / quality gate skills`

## 11. Priority Guide

- `Must-have`: nên dùng sớm vì bám sát scope MVP hoặc giúp giảm rủi ro chính
- `Nice-to-have`: rất hữu ích nhưng có thể thêm sau khi core flow đã chạy ổn
- `Optional`: chỉ cần khi team muốn tăng chiều sâu review, audit hoặc tối ưu

## 12. Bảng tổng hợp nhanh

| Skill                                                                                                             | Role       | Priority     | Purpose                                      | Link                                                                                        |
| ----------------------------------------------------------------------------------------------------------------- | ---------- | ------------ | -------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [acceptance-orchestrator](../../antigravity-awesome-skills/skills/acceptance-orchestrator/SKILL.md)               | BA         | Must-have    | Chốt acceptance criteria, scope, handoff     | [Mở skill](../../antigravity-awesome-skills/skills/acceptance-orchestrator/SKILL.md)        |
| [writing-plans](../../antigravity-awesome-skills/skills/writing-plans/SKILL.md)                                   | BA         | Must-have    | Lập kế hoạch triển khai, breakdown task      | [Mở skill](../../antigravity-awesome-skills/skills/writing-plans/SKILL.md)                  |
| [api-documentation](../../antigravity-awesome-skills/skills/api-documentation/SKILL.md)                           | BA, BE     | Must-have    | Viết tài liệu API, contract, handoff         | [Mở skill](../../antigravity-awesome-skills/skills/api-documentation/SKILL.md)              |
| [architect-review](../../antigravity-awesome-skills/skills/architect-review/SKILL.md)                             | BA, BE     | Nice-to-have | Review scope, kiến trúc, rủi ro              | [Mở skill](../../antigravity-awesome-skills/skills/architect-review/SKILL.md)               |
| [testing-qa](../../antigravity-awesome-skills/skills/testing-qa/SKILL.md)                                         | QA         | Must-have    | Khung QA tổng quát cho feature và regression | [Mở skill](../../antigravity-awesome-skills/skills/testing-qa/SKILL.md)                     |
| [webapp-testing](../../antigravity-awesome-skills/skills/webapp-testing/SKILL.md)                                 | QA         | Must-have    | Test luồng web app theo user flow            | [Mở skill](../../antigravity-awesome-skills/skills/webapp-testing/SKILL.md)                 |
| [playwright-skill](../../antigravity-awesome-skills/skills/playwright-skill/SKILL.md)                             | QA, FE     | Must-have    | Viết và chạy E2E Playwright                  | [Mở skill](../../antigravity-awesome-skills/skills/playwright-skill/SKILL.md)               |
| [verification-before-completion](../../antigravity-awesome-skills/skills/verification-before-completion/SKILL.md) | QA, FE, BE | Must-have    | Checklist verify trước khi chốt task         | [Mở skill](../../antigravity-awesome-skills/skills/verification-before-completion/SKILL.md) |
| [react-nextjs-development](../../antigravity-awesome-skills/skills/react-nextjs-development/SKILL.md)             | FE         | Must-have    | Phát triển app React/Next.js                 | [Mở skill](../../antigravity-awesome-skills/skills/react-nextjs-development/SKILL.md)       |
| [nextjs-app-router-patterns](../../antigravity-awesome-skills/skills/nextjs-app-router-patterns/SKILL.md)         | FE         | Must-have    | Pattern cho Next.js App Router               | [Mở skill](../../antigravity-awesome-skills/skills/nextjs-app-router-patterns/SKILL.md)     |
| [tailwind-patterns](../../antigravity-awesome-skills/skills/tailwind-patterns/SKILL.md)                           | FE         | Must-have    | Tăng tốc dựng UI bằng Tailwind               | [Mở skill](../../antigravity-awesome-skills/skills/tailwind-patterns/SKILL.md)              |
| [tanstack-query-expert](../../antigravity-awesome-skills/skills/tanstack-query-expert/SKILL.md)                   | FE         | Must-have    | Fetching, caching, server state              | [Mở skill](../../antigravity-awesome-skills/skills/tanstack-query-expert/SKILL.md)          |
| [zod-validation-expert](../../antigravity-awesome-skills/skills/zod-validation-expert/SKILL.md)                   | FE         | Must-have    | Validation form và schema                    | [Mở skill](../../antigravity-awesome-skills/skills/zod-validation-expert/SKILL.md)          |
| [zustand-store-ts](../../antigravity-awesome-skills/skills/zustand-store-ts/SKILL.md)                             | FE         | Must-have    | Store client-side cho auth/cart/UI           | [Mở skill](../../antigravity-awesome-skills/skills/zustand-store-ts/SKILL.md)               |
| [ui-review](../../antigravity-awesome-skills/skills/ui-review/SKILL.md)                                           | FE         | Nice-to-have | Review UI consistency, usability             | [Mở skill](../../antigravity-awesome-skills/skills/ui-review/SKILL.md)                      |
| [web-performance-optimization](../../antigravity-awesome-skills/skills/web-performance-optimization/SKILL.md)     | FE, QA     | Nice-to-have | Tối ưu performance, Core Web Vitals          | [Mở skill](../../antigravity-awesome-skills/skills/web-performance-optimization/SKILL.md)   |
| [backend-architect](../../antigravity-awesome-skills/skills/backend-architect/SKILL.md)                           | BE         | Must-have    | Thiết kế service, module, domain flow        | [Mở skill](../../antigravity-awesome-skills/skills/backend-architect/SKILL.md)              |
| [django-pro](../../antigravity-awesome-skills/skills/django-pro/SKILL.md)                                         | BE         | Must-have    | Best practices cho Django app                | [Mở skill](../../antigravity-awesome-skills/skills/django-pro/SKILL.md)                     |
| [api-design-principles](../../antigravity-awesome-skills/skills/api-design-principles/SKILL.md)                   | BE         | Must-have    | Thiết kế REST API rõ ràng, ổn định           | [Mở skill](../../antigravity-awesome-skills/skills/api-design-principles/SKILL.md)          |
| [api-endpoint-builder](../../antigravity-awesome-skills/skills/api-endpoint-builder/SKILL.md)                     | BE         | Must-have    | Xây endpoint nhanh theo use case             | [Mở skill](../../antigravity-awesome-skills/skills/api-endpoint-builder/SKILL.md)           |
| [auth-implementation-patterns](../../antigravity-awesome-skills/skills/auth-implementation-patterns/SKILL.md)     | BE         | Must-have    | Auth/JWT/profile/address flow                | [Mở skill](../../antigravity-awesome-skills/skills/auth-implementation-patterns/SKILL.md)   |
| [postgresql](../../antigravity-awesome-skills/skills/postgresql/SKILL.md)                                         | BE         | Must-have    | Thiết kế và sử dụng PostgreSQL               | [Mở skill](../../antigravity-awesome-skills/skills/postgresql/SKILL.md)                     |
| [using-neon](../../antigravity-awesome-skills/skills/using-neon/SKILL.md)                                         | BE         | Nice-to-have | Làm việc với Neon Postgres                   | [Mở skill](../../antigravity-awesome-skills/skills/using-neon/SKILL.md)                     |
| [docker-expert](../../antigravity-awesome-skills/skills/docker-expert/SKILL.md)                                   | BE         | Nice-to-have | Docker, compose, local dev stack             | [Mở skill](../../antigravity-awesome-skills/skills/docker-expert/SKILL.md)                  |
| [api-security-testing](../../antigravity-awesome-skills/skills/api-security-testing/SKILL.md)                     | QA, BE     | Nice-to-have | Kiểm tra lỗi auth, permission, input         | [Mở skill](../../antigravity-awesome-skills/skills/api-security-testing/SKILL.md)           |
| [django-perf-review](../../antigravity-awesome-skills/skills/django-perf-review/SKILL.md)                         | BE         | Optional     | Review hiệu năng Django, query, ORM          | [Mở skill](../../antigravity-awesome-skills/skills/django-perf-review/SKILL.md)             |
| [systematic-debugging](../../antigravity-awesome-skills/skills/systematic-debugging/SKILL.md)                     | QA, FE, BE | Must-have    | Debug có hệ thống, giảm mò lỗi               | [Mở skill](../../antigravity-awesome-skills/skills/systematic-debugging/SKILL.md)           |
