# Seed Data & Testing Strategy

## Goal

Provide a consistent dataset for Frontend development and automated testing.

> [!NOTE]
> **Agent Skills Utilized**: [TDD Workflow](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/tdd-workflow/SKILL.md), [Senior Fullstack](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/senior-fullstack/SKILL.md)

## Strategy

### 1. Development Fixtures

- Location: `apps/*/fixtures/*.json`
- Usage: `python manage.py loaddata products.json`
- Content:
  - 10 Categories
  - 50 Products with varying variants
  - 1 Admin User (`admin@example.com` / `admin123`)
  - 2 Test Users (`user1@example.com`, `user2@example.com`)

### 2. Factory Boy (For Tests)

- Use `factory-boy` to generate dynamic data in `pytest`.
- Avoid hardcoding IDs in tests.

### 3. Seed Commands

- Implement a custom management command `python manage.py seed_db` to:
  1. Clear existing data (optional).
  2. Create users.
  3. Create categories.
  4. Create products with images (using placeholder URLs).

## Frontend Sync

The seed data should contain products that match the designs (e.g., specific categories like "Electronics", "Fashion").
