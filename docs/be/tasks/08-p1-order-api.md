# Task [P1]: Order API & Stock Logic

> [!WARNING]
> Legacy planning note. Order and inventory rules in this file must yield to `CONTEXT.md` and `docs/adr/0001-order-inventory-lifecycle.md` when they conflict.

## Goal

Implement the checkout process, order creation, and critical stock management logic.

> [!NOTE]
> **Agent Skills Utilized**: [Django Pro](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/django-pro/SKILL.md), [SQL Pro](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/sql-pro/SKILL.md), [PostgreSQL Optimization](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/postgres-best-practices/SKILL.md), [TDD Workflow](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/tdd-workflow/SKILL.md), [Performance Engineer](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/performance-engineer/SKILL.md)

## Sub-tasks

### [P1-01] Order Creation (Idempotent)

- **Feature**: Create order from cart items.
- **Requirement**: Use `X-Idempotency-Key` to prevent duplicates.
- **Service Layer**: `OrderService.create_order(user, items, idempotency_key)`.

### [P1-02] Stock Management (Atomic)

- **Feature**: Protect stock consistency during order lifecycle transitions.
- **Mechanism**:
  ```python
  with transaction.atomic():
      variant = ProductVariant.objects.select_for_update().get(id=id)
      if variant.stock_quantity < requested:
          raise OutOfStockException()
      variant.stock_quantity -= requested
      variant.save()
  ```

### [P1-03] Order History & Details

- **Feature**: User can view past orders and their current status.
- **Endpoints**:
  - `GET /api/orders/`
  - `GET /api/orders/{id}/`

## Business Logic: Order Lifecycle

- `PENDING`: Initial state.
- `CONFIRMED`: Order confirmed and stock deducted at this transition.
- `SHIPPED`: Sent to carrier.
- `DELIVERED`: Final state.
- `CANCELLED`: Stock must be returned if previously deducted.

## Reference

- [05-order-lifecycle.md](./05-order-lifecycle.md)
- [03-error-handling.md](./03-error-handling.md)
