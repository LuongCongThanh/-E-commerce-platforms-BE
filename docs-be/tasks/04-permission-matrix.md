# Permission Matrix (RBAC)

## Roles

- **GUEST**: Unauthenticated visitor.
- **USER**: Authenticated customer.
- **ADMIN**: Staff/Superuser.

## Access Levels

| Feature           | GUEST | USER | ADMIN | Permission Class  |
| :---------------- | :---: | :--: | :---: | :---------------- |
| View Products     |  ✅   |  ✅  |  ✅   | `AllowAny`        |
| View Categories   |  ✅   |  ✅  |  ✅   | `AllowAny`        |
| Create Order      |  ❌   |  ✅  |  ✅   | `IsAuthenticated` |
| View Own Orders   |  ❌   |  ✅  |  ✅   | `IsAuthenticated` |
| Manage Products   |  ❌   |  ❌  |  ✅   | `IsAdminUser`     |
| Manage Categories |  ❌   |  ❌  |  ✅   | `IsAdminUser`     |
| View All Orders   |  ❌   |  ❌  |  ✅   | `IsAdminUser`     |

## Object-Level Permissions

Users should only be able to view/update their _own_ profile and _own_ orders.

```python
# apps/orders/permissions.py
class IsOrderOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
```
