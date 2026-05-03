# 06. Documentation Consistency Audit — Backend + MVP (VI)

Last updated: 2026-05-02
Source of truth for this audit: current repository state (`pyproject.toml`, `Dockerfile`, `README.md`) + docs under `docs/be` and `docs/mvp`
Owner: Tech Lead + BE Lead + BA Lead

## TOC

- [Purpose](#purpose)
- [Scope](#scope)
- [Executive Summary](#executive-summary)
- [Decision: Canonical Sources](#decision-canonical-sources)
- [Conflict Matrix](#conflict-matrix)
- [Keep Merge Archive Plan](#keep-merge-archive-plan)
- [Priority Fix Order](#priority-fix-order)
- [Acceptance Criteria](#acceptance-criteria)
- [Open Risks / Next Actions](#open-risks--next-actions)

## Purpose

Tài liệu này audit mức độ nhất quán của bộ tài liệu `docs/be` và `docs/mvp`, chỉ ra các mâu thuẫn quan trọng, và đưa ra quyết định rõ ràng theo hướng:

- file nào nên giữ làm nguồn chuẩn,
- file nào nên hạ cấp thành reference,
- file nào nên gộp/nén lại,
- file nào nên archive hoặc viết lại.

Mục tiêu là giảm rework khi implement, tránh FE/BE hiểu khác contract, và ngăn docs tiếp tục drift khỏi repo thực tế.

## Scope

Bao gồm:

- `docs/be/*.vi.md`
- `docs/be/tasks/*.md`
- `docs/mvp/*.md`
- `README.md`
- repo state hiện tại (`pyproject.toml`, `Dockerfile`, cấu trúc thư mục hiện có)

Không bao gồm:

- Review chất lượng code implementation.
- Review chi tiết nội dung skill catalog trừ khi nó gây nhầm lẫn trực tiếp cho execution docs.

## Executive Summary

Đánh giá tổng quát:

- `docs/be` là bộ tài liệu có cấu trúc tốt nhất và nên là nền để chuẩn hóa.
- `docs/mvp` hữu ích cho góc nhìn planning/solo build, nhưng đang trộn lẫn `MVP now` với `Phase 2 later`.
- `docs/be/tasks/*` có giá trị như tài liệu nháp/refinement, nhưng không còn phù hợp để giữ vai trò canonical source.
- `README.md` và repo thực tế đang lệch với nhiều phát biểu trong docs.

Kết luận điều hành:

1. Giữ `docs/be/01-05` làm bộ docs chính.
2. Hạ `docs/be/tasks/*` xuống vai trò `reference/legacy planning notes`.
3. Giữ `docs/mvp/overview.md` và `docs/mvp/mvp-plan.md` như tài liệu product/planning cấp cao.
4. Viết lại hoặc rút gọn mạnh `docs/mvp/mvp-checklist.md` để chỉ còn checklist đúng với MVP thật.
5. Đồng bộ lại `README.md` và toàn bộ docs kỹ thuật theo repo thực tế dùng `pyproject.toml` + `uv`.

## Decision: Canonical Sources

### 1. Canonical cho scope và contract

- Canonical:
  - `docs/be/01-mvp-overview.vi.md`
  - `docs/be/02-roadmap-and-execution-plan.vi.md`
  - `docs/be/04-project-structure-guidelines-conventions.vi.md`
  - `docs/be/05-priority-implementation-backlog.vi.md`
- Non-canonical:
  - `docs/be/tasks/01-conventions-standards.md`
  - `docs/be/tasks/02-api-contract.md`
  - `docs/be/tasks/03-error-handling.md`
  - `docs/be/tasks/05-order-lifecycle.md`
  - `docs/be/tasks/11-api-versioning.md`

Lý do:

- Bộ `docs/be/01-05` mới hơn, có format ổn định, có acceptance criteria và open risks.
- Bộ `docs/be/tasks/*` đang mâu thuẫn trực tiếp với bộ trên ở response shape, versioning, order states, và project structure.

### 2. Canonical cho tech stack thực tế

- Canonical:
  - `pyproject.toml`
  - `Dockerfile`
  - cấu trúc repo hiện tại
- Không được coi là source of truth:
  - các đoạn docs nói ưu tiên `requirements/base.txt` khi file đó chưa tồn tại.

### 3. Canonical cho planning cấp cao

- Giữ:
  - `docs/mvp/overview.md`
  - `docs/mvp/mvp-plan.md`
- Hạ cấp:
  - `docs/mvp/mvp-checklist.md` thành working draft cho đến khi được trim lại.

## Conflict Matrix

| Topic | Canonical decision | Files in conflict | Conflict summary | Action |
| --- | --- | --- | --- | --- |
| API response shape | Dùng shape `{ code, message, errors }` cho lỗi; success dùng payload trực tiếp hoặc paginated shape đã nêu trong overview | `docs/be/01-mvp-overview.vi.md`, `docs/be/tasks/02-api-contract.md`, `docs/be/tasks/03-error-handling.md`, `README.md` | `overview` dùng error shape gọn; `tasks` và `README` dùng wrapper `success/data/error` | Giữ `docs/be/01...`; sửa hoặc archive `tasks/02`, `tasks/03`, cập nhật `README.md` |
| API path versioning | Chọn một chuẩn duy nhất: hoặc `/api/...` cho MVP, hoặc `/api/v1/...` toàn bộ | `docs/be/01-mvp-overview.vi.md`, `docs/be/04-project-structure-guidelines-conventions.vi.md`, `docs/be/tasks/02-api-contract.md`, `docs/be/tasks/11-api-versioning.md`, `README.md` | Một số docs dùng `/api/...`, một số dùng `/api/v1/...` | Quyết định ở doc contract chính, rồi sửa toàn repo docs theo quyết định đó |
| Admin URL | Dùng một URL duy nhất, khuyến nghị giữ `/secret-panel/` vì đã xuất hiện nhất quán hơn ở BE docs | `docs/be/04-project-structure-guidelines-conventions.vi.md`, `docs/mvp/mvp-plan.md`, `docs/mvp/mvp-checklist.md` | `mvp-checklist` dùng `/manage/`, phần còn lại dùng `/secret-panel/` | Giữ `/secret-panel/`, sửa `docs/mvp/mvp-checklist.md` |
| Order state machine | Chốt tập trạng thái MVP tối thiểu và tách clearly khỏi Phase 2 | `docs/be/02-roadmap-and-execution-plan.vi.md`, `docs/be/tasks/05-order-lifecycle.md`, `docs/mvp/mvp-checklist.md`, `docs/be/tasks/08-p1-order-api.md` | Có nơi dùng `PENDING → CONFIRMED → SHIPPING → DELIVERED → CANCELLED`, có nơi thêm `FAILED_DELIVERY`, `RETURNED`, `COMPLETED` | Giữ một state machine MVP tối thiểu; chuyển trạng thái mở rộng sang Phase 2 |
| Email trigger | Chốt một rule duy nhất: gửi email khi order created hay khi confirmed | `docs/be/01-mvp-overview.vi.md`, `docs/be/02-roadmap-and-execution-plan.vi.md`, `docs/mvp/mvp-checklist.md`, `docs/be/tasks/05-order-lifecycle.md` | Có nơi nói gửi email xác nhận ngay khi tạo đơn COD, có nơi chỉ gửi khi `CONFIRMED` | Với COD MVP, nên gửi email ngay khi order created; docs còn lại sửa theo rule này |
| Payment scope | MVP là COD-only, không kéo payment gateway vào checklist implementation | `docs/be/01-mvp-overview.vi.md`, `docs/be/03-technical-stack-skills-and-versions.vi.md`, `docs/mvp/overview.md`, `docs/mvp/mvp-checklist.md` | `overview` tổng quan sản phẩm có VNPAY/Momo; checklist lại tạo `Payment` model và test VNPAY dù MVP defer | Giữ tổng quan cấp product ở `overview`, nhưng dọn checklist để bỏ VNPAY khỏi MVP execution |
| Tech source of truth | Repo hiện dùng `pyproject.toml` + `uv`; docs không được ưu tiên `requirements/*.txt` khi chưa tồn tại | `docs/be/03-technical-stack-skills-and-versions.vi.md`, `Dockerfile`, `pyproject.toml` | Doc nói `requirements/base.txt` là nguồn chuẩn nhưng repo không có file này | Sửa doc sang `pyproject.toml`; chỉ nói đến `requirements/` nếu thực sự tạo chúng |
| Project structure | Phải phản ánh repo hiện có, không mô tả thêm layer chưa tồn tại như `services/` top-level nếu không dùng | `docs/be/04-project-structure-guidelines-conventions.vi.md`, `docs/be/tasks/01-conventions-standards.md`, `README.md` | `tasks/01` mô tả `services/` top-level và `docs-be/`; repo thực tế khác | Giữ `docs/be/04...`, archive `tasks/01`, cập nhật `README.md` |
| Environment and packaging | Chuẩn hóa ngôn ngữ về package/dependency management | `docs/mvp/mvp-checklist.md`, `docs/be/03-technical-stack-skills-and-versions.vi.md`, `README.md`, `Dockerfile` | Có nơi nói `requirements.txt`, có nơi `requirements/base.txt`, repo dùng `pyproject.toml` | Chốt `pyproject.toml` + `uv` và sửa toàn bộ docs onboarding |
| Staging vs production gate | Chốt nơi FE verify contract: staging hay production | `docs/be/02-roadmap-and-execution-plan.vi.md`, `docs/mvp/mvp-plan.md` | Có chỗ yêu cầu Swagger trên staging, có chỗ yêu cầu verify trên production ngay tuần 1 | Giữ staging là bằng chứng readiness; production chỉ là deploy target sau đó |
| Cross-file references | Tất cả path phải tồn tại thật trong repo | `docs/be/01-mvp-overview.vi.md`, `docs/be/02-roadmap-and-execution-plan.vi.md`, `docs/mvp/find_skills.py` | Có reference `docs-mvp/...` không khớp thư mục hiện tại `docs/mvp/...` | Sửa toàn bộ path sai |
| README alignment | README phải phản ánh đúng docs canonical và repo thực tế | `README.md`, `docs/be/*`, `pyproject.toml` | README đang nói multi-stage Dockerfile, standardized wrapper response, `/api/v1/...` auth routes | Viết lại README theo canonical docs + current repo |

## Keep Merge Archive Plan

### Keep as canonical

- `docs/be/01-mvp-overview.vi.md`
- `docs/be/02-roadmap-and-execution-plan.vi.md`
- `docs/be/04-project-structure-guidelines-conventions.vi.md`
- `docs/be/05-priority-implementation-backlog.vi.md`
- `docs/mvp/overview.md`
- `docs/mvp/mvp-plan.md`

### Keep but revise

- `docs/be/03-technical-stack-skills-and-versions.vi.md`
  - Sửa source of truth và version source.
- `README.md`
  - Sửa onboarding + API format + package management + auth endpoints.
- `docs/mvp/mvp-checklist.md`
  - Cắt những item không thuộc MVP thật.

### Merge into canonical docs, then archive

- `docs/be/tasks/01-conventions-standards.md`
  - Nội dung chính đã được supersede bởi `docs/be/04...`
- `docs/be/tasks/02-api-contract.md`
  - Phần còn giá trị nên merge vào contract section của `docs/be/01...`
- `docs/be/tasks/03-error-handling.md`
  - Phần còn giá trị nên merge vào error standards của `docs/be/01...` hoặc `docs/be/04...`
- `docs/be/tasks/05-order-lifecycle.md`
  - Giữ làm reference sau khi state machine MVP được chốt.
- `docs/be/tasks/11-api-versioning.md`
  - Giữ làm future-policy note nếu chọn chưa bật `/v1` ngay ở MVP.

### Keep as auxiliary / non-execution docs

- `docs/be/learning_path.vi.md`
- `docs/be/skill_update.vi.md`
- `docs/mvp/skills-mapping.md`
- `docs/mvp/define_all_skill.md`
- `docs/mvp/define_all_skill.vi.md`
- `docs/mvp/key-work.md`

Các file này không nên tham gia quyết định implementation scope hay contract.

## Priority Fix Order

### P0 — phải sửa trước khi team bám docs để implement tiếp

1. API response shape
2. API path/versioning
3. Order state machine MVP
4. Email trigger rule cho COD
5. README alignment

### P1 — sửa ngay sau P0

1. Admin URL
2. Staging vs production gate
3. Tech stack source of truth
4. Cross-file references (`docs-mvp` → `docs/mvp`)

### P2 — cleanup để tránh drift lần 2

1. Archive/relocate `docs/be/tasks/*`
2. Trim `docs/mvp/mvp-checklist.md`
3. Thêm note `canonical/non-canonical` ở đầu các file còn giữ

## Acceptance Criteria

- Có một bộ docs canonical duy nhất cho scope, contract, backlog, structure.
- Không còn mâu thuẫn giữa response shape, endpoint prefix, admin URL, order states.
- `README.md` khớp với repo thực tế.
- Tất cả link và source-of-truth path trong docs đều tồn tại thật.
- `docs/mvp/mvp-checklist.md` chỉ chứa checklist đúng với MVP đã khóa scope.

## Open Risks / Next Actions

Open risks:

- Nếu không chốt canonical owner, drift sẽ quay lại sau 1-2 sprint.
- Nếu tiếp tục giữ `docs/be/tasks/*` ngang hàng với `docs/be/01-05`, người mới sẽ không biết tin file nào.
- Nếu không dọn `mvp-checklist`, team dễ vô thức implement cả Phase 2 trong MVP.

Next actions:

- [ ] Chốt quyết định versioning: `/api/...` hay `/api/v1/...`
- [ ] Chốt response shape chuẩn một lần duy nhất
- [ ] Chốt state machine MVP tối thiểu
- [ ] Sửa `README.md` theo repo thực tế
- [ ] Sửa `docs/be/03-technical-stack-skills-and-versions.vi.md`
- [ ] Trim `docs/mvp/mvp-checklist.md`
- [ ] Gắn nhãn `Legacy reference` ở `docs/be/tasks/*`
