# API Contract & Endpoint Specification

## Global Response Format

### Success

```json
{
  "success": true,
  "data": {},
  "message": "Operation successful"
}
```

### Error

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {}
  }
}
```

## Endpoint List (V1)

### Accounts & Auth

| Method | Endpoint                          | Description           |
| :----- | :-------------------------------- | :-------------------- |
| POST   | `/api/v1/accounts/register/`      | Create new user       |
| POST   | `/api/v1/accounts/token/`         | Obtain JWT (Login)    |
| POST   | `/api/v1/accounts/token/refresh/` | Refresh JWT           |
| GET    | `/api/v1/accounts/me/`            | Get current user info |

### Catalog

| Method | Endpoint                           | Description                                      |
| :----- | :--------------------------------- | :----------------------------------------------- |
| GET    | `/api/v1/catalog/products/`        | List products (Filters: category, price, search) |
| GET    | `/api/v1/catalog/products/{slug}/` | Product details                                  |
| GET    | `/api/v1/catalog/categories/`      | List all categories (Tree structure)             |

### Orders

| Method | Endpoint               | Description                                |
| :----- | :--------------------- | :----------------------------------------- |
| POST   | `/api/v1/orders/`      | Place new order (Requires Idempotency Key) |
| GET    | `/api/v1/orders/`      | List own orders                            |
| GET    | `/api/v1/orders/{id}/` | Order details                              |

## API Documentation

The backend will expose an interactive OpenAPI/Swagger UI at `/api/docs/` using `drf-spectacular`.
