# 04. Project Structure, Guidelines & Conventions — Backend (VI)

Last updated: 2026-05-04
Source of truth: current repo structure, `config/settings/base.py`, `config/urls.py`, `pyproject.toml`, architecture decisions in this doc set
Owner: BE Lead + Architect Reviewer

## TOC

- [Purpose](#purpose)
- [Scope](#scope)
- [Decisions](#decisions)
- [Detailed Spec](#detailed-spec)
- [Acceptance Criteria](#acceptance-criteria)
- [Open Risks / Next Actions](#open-risks--next-actions)

## Summary Table

| Item               | Standard                                                      |
| ------------------ | ------------------------------------------------------------- |
| Architecture style | Django app-based modular, DRF APIView/serializers + services  |
| Settings strategy  | `config/settings/base.py` + `config/settings/local.py`        |
| DB access pattern  | ORM-first, raw SQL chỉ khi cần tối ưu rõ ràng                 |
| Convention policy  | Naming, imports, typing, testing, migration, commit standards |

## Purpose

Tài liệu này mô tả chuẩn cấu trúc dự án Django và nguyên tắc coding để mọi thành viên implement nhất quán, giảm rework, dễ onboard và dễ mở rộng.

## Scope

Bao gồm:

- Target project tree cho MVP và mở rộng.
- Kiến trúc app Django ownership và shared utilities.
- Coding guidelines và conventions.
- Database và migration conventions.
- Testing conventions.
- Commit và PR conventions.

Không bao gồm:

- UI mockups hay FE-side concerns.
- Hướng dẫn setup cloud infrastructure chi tiết.

## Decisions

- Mỗi Django app chứa một domain nghiệp vụ rõ ràng — không mix concerns.
- Settings hiện tại tách theo `base.py` + `local.py`; nếu thêm `production.py` sau này thì phải cập nhật lại doc này.
- Dependency/config source hiện tại dùng `django-environ` + `.env`.
- API code ưu tiên tách dưới `apps/<domain>/api/` thay vì nhồi toàn bộ serializer/view vào root app.
- View/APIView chỉ chứa routing, authz, orchestration nhẹ; business logic nặng đẩy xuống service layer.
- Convention là bắt buộc để merge.

## Detailed Spec

### Target project tree

```text
repo-root/
  apps/
    accounts/
      api/
        serializers.py
        urls.py
        views.py
      models.py
      urls.py
    catalog/
      api/
        serializers.py
        urls.py
        views.py
      management/commands/
        seed_db.py
      models.py
      urls.py
    orders/
      api/
        admin_urls.py
        serializers.py
        urls.py
        views.py
      exceptions.py
      models.py
      services.py
      urls.py
    core/
      exceptions.py
      models.py
  config/
    settings/
      __init__.py
      base.py
      local.py
    urls.py
    wsgi.py
  docs/
  tests/
  manage.py
  Dockerfile
  docker-compose.yml
  pyproject.toml
  uv.lock
```

### Architecture rules

- App ownership:
  - `apps/accounts`: User model (extend AbstractUser), auth API, profile, address.
  - `apps/catalog`: Product, Category, ProductVariant, ProductImage, search, filter.
  - `apps/orders`: Order, OrderItem, ShippingAddress, order workflow, email trigger.
  - `apps/core`: Shared models/exceptions và các utility thực sự được nhiều app dùng chung.
- Layering trong mỗi app:
  - `api/views.py`: Nhận request, gọi serializer/service, trả response.
  - `api/serializers.py`: Validation input + shape output. Không chứa business logic.
  - `api/urls.py`: Route public API của domain.
  - `services.py`: Business logic, database transaction, state transition quan trọng.
  - `models.py`: Database schema, model methods thuần túy, không gọi external service.
  - `api/admin_urls.py`: Chỉ dùng khi có admin API tách riêng khỏi Django Admin UI.
- Shared boundary:
  - `apps/core` chỉ chứa thứ dùng chung ít nhất 2 app.
  - Cấm app import lẫn nhau ngoài `apps/core` — nếu cần cross-app logic, tách sang service riêng.

### Settings conventions

```python
# config/settings/base.py
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
DATABASES = {
    "default": env.db(),
}

# JWT settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# DRF settings
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "EXCEPTION_HANDLER": "apps.core.exceptions.custom_exception_handler",
}
```

Ghi chú:

- Các snippet trên phản ánh repo hiện tại, không phải target state giả định.
- Những thứ như throttling chi tiết, custom pagination class, hay `production.py` chỉ nên thêm vào doc khi đã tồn tại thật trong codebase.

### Coding guidelines

- Naming:
  - File: `snake_case.py`.
  - Class: `PascalCase`.
  - Function/variable: `snake_case`.
  - Constants: `UPPER_SNAKE_CASE`.
  - URL pattern: `kebab-case` (e.g., `/api/products/best-sellers/`).
  - Model field: `snake_case`.
- Imports order (theo quy ước code style; hiện repo dùng `ruff` và `black` trong `pyproject.toml`):
  1. Standard library.
  2. Third-party.
  3. Django.
  4. DRF.
  5. Local app imports.
- Typing:
  - Dùng type hints cho function signature.
  - Không dùng `Any` nếu không có lý do bắt buộc.
  - Model field types phải explicit (không để Django tự infer).
- Error handling:
  - Tất cả exception trả về shape chuẩn qua `custom_exception_handler`.
  - Không để stack trace lộ ra response production.
  - Log exception với context (user, request) qua Sentry.
- Database:
  - Luôn dùng `select_related` / `prefetch_related` khi query có FK/M2M.
  - Không chạy query trong loop (N+1 problem).
  - `select_for_update()` bắt buộc khi đọc để ghi (stock deduction, order status update).
  - Dùng `transaction.atomic()` bao toàn bộ multi-step write operation.

### Model conventions

```python
# apps/core/models.py
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# apps/catalog/models.py
class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'created_at']),
        ]
```

### Serializer conventions

```python
# ListSerializer vs DetailSerializer pattern
class ProductListSerializer(serializers.ModelSerializer):
    """Dùng cho GET /api/products/ — chỉ trả các field cần thiết cho listing"""
    price_min = serializers.DecimalField(...)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price_min', 'thumbnail']

class ProductDetailSerializer(serializers.ModelSerializer):
    """Dùng cho GET /api/products/{slug}/ — trả full detail"""
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'variants', 'images', 'category']
```

### Service layer conventions

```python
# apps/orders/services.py
from django.db import transaction

class OrderService:
    @staticmethod
    @transaction.atomic
    def create_order(user, validated_data: dict) -> Order:
        """
        Tạo order ở PENDING.
        Không deduct stock tại bước này.
        """
        # Validate input, snapshot line-item data, create Order + OrderItems.
        # Inventory commit xảy ra ở bước confirm riêng.
        return order
```

Quy tắc canonical của repo:

- `POST /api/orders/` chỉ tạo order ở `PENDING`.
- Tồn kho chỉ bị trừ khi order chuyển sang `CONFIRMED`.
- `select_for_update()` là bắt buộc ở bước confirm/cancel có tác động tồn kho.

### Migration conventions

- Mỗi migration file phải có tên mô tả: `0002_add_product_slug_index.py`.
- Không chỉnh sửa migration đã push lên production — tạo migration mới.
- Review migration SQL trước khi chạy production: `python manage.py sqlmigrate app 000x`.
- Luôn test migration: `python manage.py migrate --run-syncdb` trên staging trước production.
- `RunPython` trong migration phải có `reverse_code` nếu cần rollback.
- Backup database trước mọi migration production.

### API URL conventions

```python
# config/urls.py
urlpatterns = [
    path("secret-panel/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/", include("apps.catalog.urls")),
    path("api/orders/", include("apps.orders.urls")),
    path("api/admin/orders/", include("apps.orders.api.admin_urls")),
]

# apps/accounts/api/urls.py
urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
```

Ghi chú:

- Repo hiện tại chưa có `apps.core.urls` hay health endpoint trong `config/urls.py`.
- Catalog được mount dưới `api/`, còn orders được mount dưới `api/orders/`.
- Admin order actions có namespace route riêng: `api/admin/orders/...`.

### Testing conventions

- Unit tests:
  - Cho models methods, service layer, utility functions.
  - Dùng Factory Boy cho test fixtures — không hardcode data.
  - Test mỗi service function độc lập (mock external calls nếu cần).
- Integration tests:
  - Cho ViewSet endpoints — dùng `APIClient` của DRF.
  - Test authentication, authorization, pagination, filtering.
  - Test error cases: validation errors, 404, 403, race conditions.
- Test structure:
  ```
  apps/orders/tests/
    __init__.py
    factories.py      # OrderFactory, OrderItemFactory, etc.
    test_models.py    # Model method tests
    test_services.py  # OrderService unit tests
    test_views.py     # API endpoint integration tests
  ```
- Coverage target: ≥ 80% cho `apps/` directory.
- Pytest marks: `@pytest.mark.django_db`, `@pytest.mark.slow` cho test chậm.

Ghi chú thực tế:

- Test layout ở trên là target convention tốt, nhưng chưa phải toàn bộ cấu trúc đã tồn tại sẵn trong repo hiện tại.
- Không được viết như thể `pytest.ini`, `factories.py`, hay full test tree đã có nếu repo chưa chứa chúng.

### Commit và PR conventions

- Commit format theo conventional commits:
  - `feat(orders): add admin confirm flow for inventory commit`
  - `fix(auth): fix refresh token rotation not blacklisting old token`
  - `test(catalog): add product list API tests`
  - `chore(deps): upgrade django to 5.1.2`
- PR phải có:
  - Scope rõ (app và layer bị ảnh hưởng).
  - Migration checklist nếu có schema change.
  - Test evidence (coverage diff).
  - Risk notes nếu ảnh hưởng API contract.
  - Rollback notes nếu migration không reversible.

### Environment variables

```bash
# .env.example
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgres://user:pass@localhost:5433/ecommerce
```

Ghi chú:

- Biến môi trường ở trên là baseline tối thiểu phản ánh `base.py` hiện tại.
- Các biến cho Cloudinary, Email, Sentry, CORS whitelist nên chỉ thêm khi codebase thực sự đọc chúng.

## Acceptance Criteria

- Cấu trúc project và ownership đủ rõ để implement không mơ hồ.
- Mô tả repo không được mâu thuẫn với file/folder đang tồn tại thật.
- Coding/migration/testing/commit conventions có thể dùng trực tiếp.
- Service layer tách bạch với View layer.
- Rule app boundary ngăn được coupling sai kiến trúc.

## Open Risks / Next Actions

Open risks:

- Tăng tốc giao tính năng có thể phá conventions — cần PR checklist enforce.
- `apps/core` phình to thành "misc bucket" nếu không review kỹ.
- N+1 query khó detect nếu không dùng `django-debug-toolbar` thường xuyên.
- Doc này có nguy cơ drift lại nếu tiếp tục mô tả target-state chưa implement như thể đã tồn tại.

Next actions:

- [ ] Tạo PR template với migration checklist và API contract impact.
- [ ] Quyết định rõ phần nào là `current state` và phần nào là `target convention` nếu tiếp tục mở rộng doc này.
- [ ] Cài `django-debug-toolbar` và verify không có N+1 trong product list query.
- [ ] Chỉ thêm `TimeStampedModel`, health endpoint, custom pagination, throttling policy chi tiết vào doc sau khi code tương ứng tồn tại.
- [ ] Đồng bộ ví dụ quality tools với `pyproject.toml` hiện tại; repo đang có `ruff` và `black`, chưa có cấu hình `isort` tách riêng.
- [ ] Review định kỳ `apps/core` mỗi sprint tránh phình to.
