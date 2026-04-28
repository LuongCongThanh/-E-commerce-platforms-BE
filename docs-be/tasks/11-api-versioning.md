# API Versioning & Evolution Strategy

## Goal

Ensure the API can evolve over time without breaking existing Frontend integrations.

## Strategy

### 1. URL Versioning

- All endpoints are prefixed with `/api/v1/`.
- When breaking changes are required, a new `/api/v2/` will be created.

### 2. Header-Based Versioning (Optional/Future)

- Support `Accept: application/vnd.ecommerce.v1+json`.

### 3. Deprecation Policy

- Old versions will be supported for at least 6 months after a new version is released.
- Response headers will include `Warning: 299 - "API version v1 is deprecated"`.

### 4. Backward Compatibility Rules

- **Non-breaking**: Adding new fields, adding new endpoints, making optional fields.
- **Breaking**: Removing fields, renaming fields, changing data types, changing logic flow.

## Implementation in DRF

Use `NamespaceVersioning` or a custom versioning class if needed.

```python
# config/settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
}
```
