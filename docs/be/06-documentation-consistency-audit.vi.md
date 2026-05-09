# 06. Documentation Consistency Audit — Backend + MVP (VI)

Last updated: 2026-05-09
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

- `docs/be` vẫn là bộ tài liệu chính và hiện đã gần với repo thật hơn trước.
- `docs/mvp` vẫn hữu ích cho planning cấp cao, nhưng không nên dùng để override contract/cấu trúc backend canonical.
- `docs/be/tasks/*` đã được gắn nhãn legacy/reference ở hầu hết file, giúp giảm nhầm lẫn source-of-truth.
- Drift lớn còn lại tập trung ở một số doc chiến lược/planning phụ trợ và các chú thích/path cũ.

Kết luận điều hành:

1. Giữ `docs/be/01-05` làm bộ docs chính.
2. Tiếp tục xem `docs/be/tasks/*` là `reference/legacy planning notes`, không dùng làm canonical source.
3. Giữ `docs/mvp/overview.md` và `docs/mvp/mvp-plan.md` như tài liệu product/planning cấp cao.
4. Ưu tiên dọn các path/chú thích cũ trong `docs/mvp/*` trước khi mở rộng thêm planning docs.
5. Đồng bộ dần các doc phụ trợ với repo thực tế dùng `pyproject.toml` + `uv` + runtime routes hiện tại.

## Current Status Snapshot

Đã được chốt và phản ánh trong repo/docs canonical:

- Routing canonical hiện tại là `/api/auth/`, `/api/`, `/api/orders/`, `/api/admin/orders/`, `secret-panel/`.
- Error shape canonical là `{ code, message, errors }`.
- Lifecycle MVP canonical là `PENDING -> CONFIRMED -> SHIPPED -> DELIVERED`, với `CANCELLED` là nhánh kết thúc hợp lệ.
- Inventory chỉ commit khi `Order` chuyển sang `CONFIRMED`; hủy từ `CONFIRMED` thì restock.
- `pyproject.toml` + `uv.lock` là nguồn chuẩn cho packaging/tooling hiện tại.

Còn nên tiếp tục dọn:

- `README.md` nếu vẫn còn route/response/tooling drift.
- Các ghi chú `docs-mvp/...` cũ trong script/doc phụ trợ.
- Các planning note còn mô tả capability chưa hiện diện thật trong repo.

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

| Topic                      | Canonical decision                                                                                                        | Files in conflict                                                                                                                                                                   | Conflict summary                                                                                          | Action                                                                                     |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| API response shape         | Dùng shape `{ code, message, errors }` cho lỗi; success dùng payload trực tiếp hoặc paginated shape đã nêu trong overview | `docs/be/01-mvp-overview.vi.md`, `docs/be/tasks/02-api-contract.md`, `docs/be/tasks/03-error-handling.md`, `README.md`                                                              | `overview` dùng error shape gọn; `tasks` và `README` dùng wrapper `success/data/error`                    | Giữ `docs/be/01...`; sửa hoặc archive `tasks/02`, `tasks/03`, cập nhật `README.md`         |
| API path versioning        | Dùng `/api/...` cho contract hiện tại                                                                                     | `docs/be/01-mvp-overview.vi.md`, `docs/be/04-project-structure-guidelines-conventions.vi.md`, `docs/be/tasks/02-api-contract.md`, `docs/be/tasks/11-api-versioning.md`, `README.md` | Canonical docs đã chốt `/api/...`; phần còn lại chỉ còn ở legacy/reference hoặc README cũ                 | Giữ `/api/...`, không tái đưa `/api/v1/...` nếu chưa có quyết định mới                     |
| Admin URL                  | Dùng `/secret-panel/`                                                                                                     | `docs/be/04-project-structure-guidelines-conventions.vi.md`, `docs/mvp/mvp-plan.md`, `docs/mvp/mvp-checklist.md`                                                                    | Canonical route đã rõ; chỉ cần dọn những note/planning file còn nhắc path cũ nếu có                       | Giữ `/secret-panel/`                                                                       |
| Order state machine        | Dùng `PENDING -> CONFIRMED -> SHIPPED -> DELIVERED`, với `CANCELLED` là terminal alternate path                           | `docs/be/02-roadmap-and-execution-plan.vi.md`, `docs/be/tasks/05-order-lifecycle.md`, `docs/mvp/mvp-checklist.md`, `docs/be/tasks/08-p1-order-api.md`                               | Canonical docs đã chốt; drift còn nằm ở một số historical extension note                                  | Giữ state machine MVP tối thiểu; extension chỉ để reference                                |
| Email trigger              | Chốt một rule duy nhất: gửi email khi order created hay khi confirmed                                                     | `docs/be/01-mvp-overview.vi.md`, `docs/be/02-roadmap-and-execution-plan.vi.md`, `docs/mvp/mvp-checklist.md`, `docs/be/tasks/05-order-lifecycle.md`                                  | Có nơi nói gửi email xác nhận ngay khi tạo đơn COD, có nơi chỉ gửi khi `CONFIRMED`                        | Với COD MVP, nên gửi email ngay khi order created; docs còn lại sửa theo rule này          |
| Payment scope              | MVP là COD-only, không kéo payment gateway vào checklist implementation                                                   | `docs/be/01-mvp-overview.vi.md`, `docs/be/03-technical-stack-skills-and-versions.vi.md`, `docs/mvp/overview.md`, `docs/mvp/mvp-checklist.md`                                        | `overview` tổng quan sản phẩm có VNPAY/Momo; checklist lại tạo `Payment` model và test VNPAY dù MVP defer | Giữ tổng quan cấp product ở `overview`, nhưng dọn checklist để bỏ VNPAY khỏi MVP execution |
| Tech source of truth       | Repo hiện dùng `pyproject.toml` + `uv`; docs không được ưu tiên `requirements/*.txt` khi chưa tồn tại                     | `docs/be/03-technical-stack-skills-and-versions.vi.md`, `Dockerfile`, `pyproject.toml`                                                                                              | Đã chốt ở canonical docs; drift còn lại chủ yếu ở vài note phụ trợ/skill catalog                          | Tiếp tục thay `requirements*.txt` cũ bằng `pyproject.toml` khi gặp                         |
| Project structure          | Phải phản ánh repo hiện có, không mô tả thêm layer chưa tồn tại như `services/` top-level nếu không dùng                  | `docs/be/04-project-structure-guidelines-conventions.vi.md`, `docs/be/tasks/01-conventions-standards.md`, `README.md`                                                               | `tasks/01` mô tả `services/` top-level và `docs-be/`; repo thực tế khác                                   | Giữ `docs/be/04...`, archive `tasks/01`, cập nhật `README.md`                              |
| Environment and packaging  | Chuẩn hóa ngôn ngữ về package/dependency management                                                                       | `docs/mvp/mvp-checklist.md`, `docs/be/03-technical-stack-skills-and-versions.vi.md`, `README.md`, `Dockerfile`                                                                      | Có nơi nói `requirements.txt`, có nơi `requirements/base.txt`, repo dùng `pyproject.toml`                 | Chốt `pyproject.toml` + `uv` và sửa toàn bộ docs onboarding                                |
| Staging vs production gate | Chốt nơi FE verify contract: staging hay production                                                                       | `docs/be/02-roadmap-and-execution-plan.vi.md`, `docs/mvp/mvp-plan.md`                                                                                                               | Có chỗ yêu cầu Swagger trên staging, có chỗ yêu cầu verify trên production ngay tuần 1                    | Giữ staging là bằng chứng readiness; production chỉ là deploy target sau đó                |
| Cross-file references      | Tất cả path phải tồn tại thật trong repo                                                                                  | `docs/be/01-mvp-overview.vi.md`, `docs/be/02-roadmap-and-execution-plan.vi.md`, `docs/mvp/find_skills.py`                                                                           | Một số reference `docs-mvp/...` cũ vẫn còn trong script/doc phụ trợ                                       | Sửa toàn bộ path sai                                                                       |
| README alignment           | README phải phản ánh đúng docs canonical và repo thực tế                                                                  | `README.md`, `docs/be/*`, `pyproject.toml`                                                                                                                                          | README đang nói multi-stage Dockerfile, standardized wrapper response, `/api/v1/...` auth routes          | Viết lại README theo canonical docs + current repo                                         |

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

1. README alignment
2. Cross-file references còn sai
3. Doc phụ trợ còn mô tả capability planned như thể đã active
4. Trim tiếp các planning note ít giá trị cao
5. Kiểm tra lại `docs/mvp/mvp-checklist.md` nếu còn kéo Phase 2 vào MVP

### P1 — sửa ngay sau P0

1. Staging vs production gate wording
2. Tech stack source of truth trong doc phụ trợ
3. Skill catalog wording còn trỏ `requirements.txt`
4. Cross-file references (`docs-mvp` -> `docs/mvp`)

### P2 — cleanup để tránh drift lần 2

1. Giữ `docs/be/tasks/*` ở trạng thái legacy có cảnh báo rõ
2. Trim `docs/mvp/mvp-checklist.md`
3. Tiếp tục thêm note `canonical/non-canonical` ở các file phụ trợ còn thiếu

## Acceptance Criteria

- Có một bộ docs canonical duy nhất cho scope, contract, backlog, structure.
- Không còn mâu thuẫn trong canonical docs về response shape, endpoint prefix, admin URL, order states.
- Các file legacy/reference không còn dễ bị hiểu nhầm là canon.
- Tất cả link và source-of-truth path trong docs vừa sửa đều tồn tại thật.
- `README.md` và `docs/mvp/mvp-checklist.md` là 2 điểm cần follow-up nếu còn drift.

## Open Risks / Next Actions

Open risks:

- Nếu không chốt canonical owner, drift sẽ quay lại sau 1-2 sprint.
- README hoặc planning docs phụ trợ có thể lại trở thành nguồn drift nếu sửa tách khỏi canonical docs.
- Nếu không dọn `mvp-checklist`, team dễ vô thức implement cả Phase 2 trong MVP.

Next actions:

- [x] Chốt contract hiện tại dùng `/api/...`
- [x] Chốt response shape chuẩn `{ code, message, errors }`
- [x] Chốt state machine MVP tối thiểu
- [x] Gắn nhãn legacy/reference cho `docs/be/tasks/*`
- [ ] Sửa `README.md` theo repo thực tế nếu còn drift
- [ ] Trim `docs/mvp/mvp-checklist.md`
- [ ] Quét tiếp doc/script phụ trợ để bỏ path `docs-mvp/...` cũ
