# Backend Conventions & Standards

## 1. Coding Rules

- **Python**: PEP 8 compliance (enforced by Ruff/Black).
- **Strings**: Use f-strings for formatting.
- **Typing**: Use Type Hints for all Service layer functions.
- **Docstrings**: Required for all public classes and Service methods (Google Style).

## 2. Architecture: Service Layer Pattern

To keep logic out of Views and Serializers:

- **Views**: Handle HTTP, parameters, and basic permissions.
- **Serializers**: Handle data validation and transformation.
- **Services**: Handle business logic (transactions, external APIs, complex queries).

```python
# Example: apps/catalog/services.py
def create_product_with_variants(product_data, variants_data):
    with transaction.atomic():
        product = Product.objects.create(**product_data)
        # logic for variants...
        return product
```

## 3. Directory Structure

```text
/
├── apps/              # Django applications
├── services/          # Shared business logic
├── config/            # Django settings, wsgi, asgi
├── docs-be/           # Documentation
├── tests/             # Global test suites
├── manage.py
├── Dockerfile
└── docker-compose.yml
```

## 4. API Standards

- **RESTful**: Proper use of GET, POST, PATCH, DELETE.
- **Trailing Slashes**: Enforce trailing slashes (Django default).
- **Versionary**: Prefix all APIs with `/api/v1/`.
- **Pagination**: Use `PageNumberPagination` (default `page_size=20`).
  - Query params: `?page=1&page_size=20`.
