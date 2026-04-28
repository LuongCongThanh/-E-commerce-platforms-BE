# Global Error Handling Logic

## Error Codes

| Code               | HTTP Status | Meaning                           |
| :----------------- | :---------- | :-------------------------------- |
| `VALIDATION_ERROR` | 400         | Input data failed validation      |
| `UNAUTHORIZED`     | 401         | Authentication required           |
| `FORBIDDEN`        | 403         | Permission denied                 |
| `NOT_FOUND`        | 404         | Resource not found                |
| `OUT_OF_STOCK`     | 409         | Requested stock not available     |
| `ORDER_CONFLICT`   | 409         | Order in invalid state for action |
| `RATE_LIMITED`     | 429         | Too many requests                 |
| `INVALID_TOKEN`    | 401         | Authentication token is invalid   |
| `TOKEN_EXPIRED`    | 401         | Authentication token has expired  |
| `PAYMENT_REQUIRED` | 402         | Payment is needed to proceed      |
| `SERVER_ERROR`     | 500         | Unexpected backend error          |

## Implementation

We use a custom DRF exception handler to wrap all responses.

```python
# apps/core/exceptions.py
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        custom_data = {
            "success": false,
            "error": {
                "code": getattr(exc, 'default_code', 'SERVER_ERROR').upper(),
                "message": str(exc.detail) if hasattr(exc, 'detail') else str(exc),
                "details": response.data if response.status_code == 400 else None
            }
        }
        response.data = custom_data
    return response
```

## Frontend Integration

FE should check `success: false` and use `error.code` to trigger specific UI logic (e.g., redirect to login for `UNAUTHORIZED` or show stock warning for `OUT_OF_STOCK`).
