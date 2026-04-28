# Task [P1]: Core API - Auth & Catalog

## Goal

Implement the core APIs needed by the Frontend to display products and manage user authentication.

> [!NOTE]
> **Agent Skills Utilized**: [Python Pro](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/python-pro/SKILL.md), [Django Pro](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/django-pro/SKILL.md), [TDD Workflow](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/tdd-workflow/SKILL.md), [Senior Fullstack](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/senior-fullstack/SKILL.md)

## Sub-tasks

### [P1-01] Authentication (JWT & Social)

- **Feature**: Login, Registration, Password Reset, JWT Refresh.
- **Library**: `djangorestframework-simplejwt`.
- **Flow**:
  1. User submits credentials.
  2. Server validates.
  3. Return `access` and `refresh` tokens in the standard response format.

### [P1-02] Catalog API (Categories & Products)

- **Feature**: Nested category tree, Product list with filtering, Product details with variants.
- **Endpoints**:
  - `GET /api/catalog/categories/`
  - `GET /api/catalog/products/` (Filter by category, price, search)
  - `GET /api/catalog/products/{slug}/`
- **Performance**: Use `prefetch_related` for variants and images to avoid N+1.

### [P1-03] User Profiles

- **Feature**: Get/Update profile, manage shipping addresses.
- **Endpoints**:
  - `GET /api/accounts/profile/`
  - `PATCH /api/accounts/profile/`

## API Contract Preview

| Method | Endpoint                  | Description      | Permission |
| :----- | :------------------------ | :--------------- | :--------- |
| POST   | `/api/accounts/register/` | New user signup  | AllowAny   |
| POST   | `/api/accounts/login/`    | JWT token obtain | AllowAny   |
| GET    | `/api/catalog/products/`  | Product listing  | AllowAny   |

## Implementation Details

- **Serializers**: Use `ModelSerializer` with explicit fields.
- **Filters**: Implement `django-filter` backends.
- **Permission**: Most Catalog APIs are `AllowAny` (Read-only).

## Reference

- [02-api-contract.md](./02-api-contract.md)
- [04-permission-matrix.md](./04-permission-matrix.md)
