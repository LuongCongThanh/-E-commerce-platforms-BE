from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return response

    error_code = str(getattr(exc, "default_code", "SERVER_ERROR")).upper()
    response_data = response.data

    if (
        isinstance(response_data, dict)
        and "message" in response_data
        and "errors" in response_data
    ):
        message = response_data["message"]
        errors = response_data["errors"]
    elif isinstance(response_data, dict) and "detail" in response_data:
        message = str(response_data["detail"])
        errors = None
    elif isinstance(response_data, dict):
        message = (
            "Dữ liệu không hợp lệ" if response.status_code == 400 else "Request failed"
        )
        errors = response_data
    else:
        message = str(response_data)
        errors = None

    response.data = {
        "code": error_code,
        "message": message,
        "errors": errors,
    }
    return response
