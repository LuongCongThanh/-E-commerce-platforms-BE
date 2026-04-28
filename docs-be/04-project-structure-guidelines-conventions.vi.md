# 04. Project Structure, Guidelines & Conventions — Backend (VI)

Last updated: 2026-04-25  
Source of truth: Django project structure, architecture decisions in this doc set, BE standards  
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
| Architecture style | Django app-based modular, DRF ViewSets + Serializers          |
| Settings strategy  | `settings/base.py` + `development.py` + `production.py`       |
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
- Settings phân tầng: `base.py` → `development.py` / `production.py`.
- Không hardcode secret — tất cả qua biến môi trường (`python-decouple`).
- Mỗi ViewSet/View chứa routing logic, không chứa business logic nặng — đẩy xuống service layer.
- Convention là bắt buộc để merge.

## Detailed Spec

### Target project tree

```text
backend/
  config/
    __init__.py
    settings/
      __init__.py
      base.py          # Shared settings
      development.py   # Local dev overrides
      production.py    # Production overrides
    urls.py            # Root URL config
    wsgi.py
    asgi.py
  apps/
    accounts/          # User auth, profile, address
      migrations/
      admin.py
      apps.py
      models.py
      serializers.py
      views.py
      urls.py
      services.py      # Business logic tách ra view
      tests/
        test_models.py
        test_views.py
        factories.py
    catalog/           # Product, Category, Variant, Image
      migrations/
      admin.py
      apps.py
      models.py
      serializers.py
      views.py
      urls.py
      filters.py       # django-filter FilterSet
      services.py
      tests/
    orders/            # Order, OrderItem, ShippingAddress
      migrations/
      admin.py
      apps.py
      models.py
      serializers.py
      views.py
      urls.py
      services.py      # Atomic order creation, stock deduction
      email.py         # Email notification logic
      tests/
    core/              # Shared utilities
      models.py        # TimeStampedModel, SoftDeleteModel
      pagination.py    # StandardResultsSetPagination
      permissions.py   # IsOwnerOrAdmin, IsAdminUser custom
      exceptions.py    # Custom exception handler → standard error shape
      serializers.py   # Base serializer mixins
      views.py         # Health check view
  requirements/
    base.txt
    development.txt
    production.txt
  templates/
    emails/
      order_confirmation.html
      password_reset.html
  manage.py
  Dockerfile
  docker-compose.yml
  docker-compose.prod.yml
  .env.example
  pyproject.toml       # ruff + black + isort config
  pytest.ini           # pytest config
```

### Architecture rules

- App ownership:
  - `apps/accounts`: User model (extend AbstractUser), auth API, profile, address.
  - `apps/catalog`: Product, Category, ProductVariant, ProductImage, search, filter.
  - `apps/orders`: Order, OrderItem, ShippingAddress, order workflow, email trigger.
  - `apps/core`: Shared models (TimeStampedModel), pagination, permissions, exceptions.
- Layering trong mỗi app:
  - `views.py` / `ViewSet`: Nhận request, gọi serializer, gọi service, trả response.
  - `serializers.py`: Validation input + shape output. Không chứa business logic.
  - `services.py`: Business logic, database transaction, gửi email. Test độc lập.
  - `models.py`: Database schema, model methods thuần túy, không gọi external service.
  - `admin.py`: Admin registration, display, actions.
- Shared boundary:
  - `apps/core` chỉ chứa thứ dùng chung ít nhất 2 app.
  - Cấm app import lẫn nhau ngoài `apps/core` — nếu cần cross-app logic, tách sang service riêng.

### Settings conventions

```python
# config/settings/base.py
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
DATABASES = {
    'default': config('DATABASE_URL', cast=db_url)
}

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# DRF settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    },
    'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 20,
    'EXCEPTION_HANDLER': 'apps.core.exceptions.custom_exception_handler',
}
```

### Coding guidelines

- Naming:
  - File: `snake_case.py`.
  - Class: `PascalCase`.
  - Function/variable: `snake_case`.
  - Constants: `UPPER_SNAKE_CASE`.
  - URL pattern: `kebab-case` (e.g., `/api/products/best-sellers/`).
  - Model field: `snake_case`.
- Imports order (isort/ruff enforce):
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
        Atomic order creation với stock deduction.
        Raises ValidationError nếu stock không đủ.
        """
        items_data = validated_data.pop('items')
        order = Order.objects.create(user=user, **validated_data)

        for item_data in items_data:
            variant = ProductVariant.objects.select_for_update().get(
                pk=item_data['variant_id']
            )
            if variant.stock_quantity < item_data['quantity']:
                raise ValidationError(
                    {'variant_id': f'Sản phẩm "{variant}" vừa hết hàng'}
                )
            variant.stock_quantity -= item_data['quantity']
            variant.save(update_fields=['stock_quantity'])
            OrderItem.objects.create(order=order, variant=variant, **item_data)

        OrderEmailService.send_confirmation(order)
        return order
```

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
    path('', include('apps.core.urls')),          # health check
    path('api/auth/', include('apps.accounts.urls')),
    path('api/', include('apps.catalog.urls')),
    path('api/', include('apps.orders.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(), name='swagger-ui'),
    path('secret-panel/', admin.site.urls),        # Đổi từ /admin/
]

# apps/catalog/urls.py
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
```

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

### Commit và PR conventions

- Commit format theo conventional commits:
  - `feat(orders): add atomic stock deduction in order creation`
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
DATABASE_URL=postgres://user:pass@localhost:5432/ecommerce
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=15
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourstore.com

# Sentry
SENTRY_DSN=https://xxx@sentry.io/xxx

# Frontend URL (cho CORS)
FRONTEND_URL=http://localhost:3000
```

## Acceptance Criteria

- Cấu trúc project và ownership đủ rõ để implement không mơ hồ.
- Coding/migration/testing/commit conventions có thể dùng trực tiếp.
- Service layer tách bạch với View layer.
- Rule app boundary ngăn được coupling sai kiến trúc.

## Open Risks / Next Actions

Open risks:

- Tăng tốc giao tính năng có thể phá conventions — cần PR checklist enforce.
- `apps/core` phình to thành "misc bucket" nếu không review kỹ.
- N+1 query khó detect nếu không dùng `django-debug-toolbar` thường xuyên.

Next actions:

- [ ] Tạo PR template với migration checklist và API contract impact.
- [ ] Cài `django-debug-toolbar` và verify không có N+1 trong product list query.
- [ ] Tạo `TimeStampedModel` base class trong `apps/core/models.py`.
- [ ] Cấu hình `ruff` + `black` + `isort` trong `pyproject.toml`.
- [ ] Review định kỳ `apps/core` mỗi sprint tránh phình to.
