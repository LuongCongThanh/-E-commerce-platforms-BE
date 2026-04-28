# Task [P0]: Foundation - Environment & Base Structure

## Goal

Set up the professional development environment using Docker, define the project architecture, and implement base models with migrations.

> [!NOTE]
> **Agent Skills Utilized**: [Python Pro](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/python-pro/SKILL.md), [Django Pro](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/django-pro/SKILL.md), [Database Architect](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/database-architect/SKILL.md), [Senior Architect](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/senior-architect/SKILL.md), [GitHub Automation](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/github/SKILL.md), [Powershell Windows](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/powershell-windows/SKILL.md)

## Sub-tasks

### [P0-01] Initialize Project & Docker Environment

- **Description**: Create `Dockerfile`, `docker-compose.yml`, and `pyproject.toml` (using `uv` or `poetry` as suggested by `uv` trend).
- **Requirements**:
  - Python 3.12+
  - PostgreSQL 16
  - Redis 7 (for caching/celery later)
- **Commands**:
  ```bash
  docker-compose up --build
  ```

### [P0-02] Core Architecture & Folder Structure

- **Description**: Setup Django project structure following the Service Layer pattern.
- **Structure**:
  ```text
  apps/
    core/         # Base models, mixins, utils
    accounts/     # User, Profile, Auth
    catalog/      # Product, Category, Variant
    orders/       # Order, OrderItem
  services/       # Business logic layer
  ```

### [P0-03] Database Schema & Base Models

- **Description**: Implement models for User, Category, Product, Variant, and Order based on the refined schema.
- **ERD Diagram**:

  ```mermaid
  erDiagram
      USER ||--o{ ORDER : places
      USER ||--o{ SHIPPING_ADDRESS : has
      CATEGORY ||--o{ CATEGORY : "parent of"
      CATEGORY ||--o{ PRODUCT : contains
      PRODUCT ||--o{ PRODUCT_VARIANT : has
      PRODUCT ||--o{ PRODUCT_IMAGE : has
      ORDER ||--o{ ORDER_ITEM : contains
      PRODUCT_VARIANT ||--o{ ORDER_ITEM : "ordered as"

      USER {
          int id PK
          string email UNIQUE
          string phone
          string avatar_url
          datetime created_at
          datetime updated_at
      }

      CATEGORY {
          int id PK
          string name
          string slug UNIQUE
          int parent_id FK
          datetime created_at
          datetime updated_at
      }

      PRODUCT {
          int id PK
          string name
          string slug UNIQUE
          text description
          int category_id FK
          boolean is_active
          datetime created_at
          datetime updated_at
      }

      PRODUCT_VARIANT {
          int id PK
          int product_id FK
          string sku UNIQUE
          decimal price
          string currency
          int stock_quantity
          datetime created_at
          datetime updated_at
      }

      PRODUCT_IMAGE {
          int id PK
          int product_id FK
          string image_url
          boolean is_thumbnail
      }

      SHIPPING_ADDRESS {
          int id PK
          int user_id FK
          string receiver_name
          string phone
          string address_line1
          string city
      }

      ORDER {
          int id PK
          int user_id FK
          string status
          decimal total
          string currency
          string payment_status
          string idempotency_key UNIQUE
          datetime created_at
          datetime updated_at
      }

      ORDER_ITEM {
          int id PK
          int order_id FK
          int variant_id FK
          int quantity
          decimal price_at_purchase
      }
  ```

- **Key Constraints & Fields**:
  - `Product`: `slug` must be UNIQUE.
  - `ProductVariant`: `sku` must be UNIQUE. Add `currency` (USD/VND).
  - `Order`: `idempotency_key` must be UNIQUE. Add `currency` (USD/VND).
  - `Order`: Add `payment_status` (PENDING, PAID, FAILED, REFUNDED, CANCELLED).
  - `BaseModel`: `created_at`, `updated_at`, `is_active`.

### [P0-04] CI/CD Pipeline Setup

- **Description**: Configure GitHub Actions for Linting (Ruff), Formatting (Black), and Tests.
- **Config**: `.github/workflows/backend-ci.yml`.
- **Quality Gates**:
  - `python manage.py makemigrations --check --dry-run`
  - `python manage.py migrate --plan`

### [P0-05] Global Error Handling & Idempotency

- **Description**: Implement a unified DRF exception handler and middleware for Idempotency keys.

## Implementation Flow

1. **Dockerize**: Ensure DB is reachable.
2. **Scaffold**: Create apps and settings.
3. **Migrate**: Run initial migrations.
4. **Verify**: Check if `http://localhost:8000/admin` is accessible.

## Reference

- See [01-conventions-standards.md](./01-conventions-standards.md) for naming and structure rules.
