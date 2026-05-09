# E-commerce Platform Backend

Backend cho MVP e-commerce dùng Django và Django REST Framework, ưu tiên API-first, COD-first, và Django Admin để vận hành nhanh trong giai đoạn MVP.

## Tech Stack

- Core: Python 3.12+, Django, Django REST Framework
- Auth: SimpleJWT
- Database: PostgreSQL
- Docs: `drf-spectacular`
- Dependency management: `pyproject.toml` + `uv`
- Local runtime: `Dockerfile` + `docker-compose.yml`

## Project Structure

```text
apps/         # Domain apps
config/       # Settings, urls, ASGI/WSGI
docs/         # Backend and MVP documentation
tests/        # Shared tests
Dockerfile
docker-compose.yml
manage.py
pyproject.toml
```

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL (local hoặc Docker)
- `uv` để quản lý dependency

### Local setup (PostgreSQL local)

```bash
# 1. Clone và cài dependency
uv sync

# 2. Copy env và chỉnh thông tin DB
cp .env.example .env
# Sửa DATABASE_URL theo PostgreSQL local của bạn:
# DATABASE_URL=postgres://<user>:<password>@localhost:5432/<dbname>

# 3. Chạy migrations
python manage.py migrate

# 4. Tạo superuser (để vào Django Admin)
python manage.py createsuperuser

# 5. Seed data mẫu (catalog)
python manage.py seed_db

# 6. Chạy dev server
python manage.py runserver
```

### Local setup (Docker)

```bash
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py seed_db
```

### Pre-commit setup

```bash
uv sync --group dev
uv run pre-commit install
uv run pre-commit run --all-files
```

Các hook hiện tại:

- `ruff check --fix`
- `black`
- `end-of-file-fixer`
- `trailing-whitespace`

## Commands

### Database

```bash
python manage.py makemigrations          # tạo migration mới
python manage.py makemigrations <app>    # cho 1 app cụ thể
python manage.py migrate                 # apply migrations
python manage.py showmigrations          # xem trạng thái migrations
python manage.py seed_db                 # seed data mẫu
python manage.py createsuperuser         # tạo admin account
```

### Code quality

```bash
ruff check .                             # lint
ruff check . --fix                       # lint + auto fix
black .                                  # format
pre-commit run --all-files               # chạy tất cả hooks
```

### Tests

```bash
python manage.py test                    # chạy tất cả tests
python manage.py test apps.orders        # test 1 app
pytest                                   # nếu dùng pytest
pytest --cov=apps --cov-report=term      # với coverage report
```

## API Baseline

| Method | Endpoint                            | Mô tả                                       |
| ------ | ----------------------------------- | ------------------------------------------- |
| POST   | `/api/auth/register/`               | Đăng ký tài khoản                           |
| POST   | `/api/auth/login/`                  | Đăng nhập, trả JWT                          |
| POST   | `/api/auth/logout/`                 | Logout, blacklist refresh token             |
| POST   | `/api/auth/token/refresh/`          | Rotate refresh token                        |
| POST   | `/api/auth/password/reset/`         | Yêu cầu reset password                      |
| POST   | `/api/auth/password/reset/confirm/` | Xác nhận reset password                     |
| GET    | `/api/products/`                    | Danh sách sản phẩm (filter/search/ordering) |
| GET    | `/api/products/{slug}/`             | Chi tiết sản phẩm                           |
| GET    | `/api/categories/`                  | Cây danh mục                                |
| POST   | `/api/orders/`                      | Tạo đơn COD                                 |
| GET    | `/api/orders/`                      | Lịch sử đơn của user                        |
| GET    | `/api/orders/{id}/`                 | Chi tiết đơn                                |
| POST   | `/api/orders/{id}/cancel/`          | Huỷ đơn (customer, chỉ PENDING)             |
| GET    | `/api/health/`                      | Health check                                |

**Admin** (yêu cầu `is_staff=True`):

| Method | Endpoint                          | Mô tả                    |
| ------ | --------------------------------- | ------------------------ |
| POST   | `/api/admin/orders/{id}/confirm/` | Xác nhận đơn → CONFIRMED |
| POST   | `/api/admin/orders/{id}/ship/`    | Chuyển sang SHIPPED      |
| POST   | `/api/admin/orders/{id}/deliver/` | Chuyển sang DELIVERED    |
| POST   | `/api/admin/orders/{id}/cancel/`  | Huỷ đơn (admin)          |

Nếu sau này bật versioning chính thức, toàn bộ docs sẽ được cập nhật đồng bộ từ canonical docs trong `docs/be`.

## API Docs

- Swagger UI: `http://localhost:8000/api/docs/`

## Error Format

Canonical error shape hiện tại trong docs backend:

```json
{
  "code": "VALIDATION_ERROR",
  "message": "Dữ liệu không hợp lệ",
  "errors": {
    "field_name": ["Thông báo lỗi cụ thể"]
  }
}
```

## Canonical Documentation

- Scope và API baseline: `docs/be/01-mvp-overview.vi.md`
- Execution plan: `docs/be/02-roadmap-and-execution-plan.vi.md`
- Tech stack và quality gates: `docs/be/03-technical-stack-skills-and-versions.vi.md`
- Project structure và conventions: `docs/be/04-project-structure-guidelines-conventions.vi.md`
- Priority backlog: `docs/be/05-priority-implementation-backlog.vi.md`
- Documentation audit: `docs/be/06-documentation-consistency-audit.vi.md`
