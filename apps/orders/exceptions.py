from rest_framework import status
from rest_framework.exceptions import APIException


class OrderInvalidState(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "ORDER_INVALID_STATE"
    default_detail = {
        "message": "Đơn hàng không thể thực hiện hành động ở trạng thái hiện tại.",
        "errors": {
            "status": ["Order cannot perform this action in its current state."]
        },
    }

    def __init__(self, message=None, errors=None):
        detail = {
            "message": message or self.default_detail["message"],
            "errors": errors or self.default_detail["errors"],
        }
        super().__init__(detail=detail)


class OutOfStock(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "OUT_OF_STOCK"
    default_detail = {
        "message": "Tồn kho không đủ để xác nhận đơn hàng.",
        "errors": {"items": ["One or more product variants do not have enough stock."]},
    }

    def __init__(self, message=None, errors=None):
        detail = {
            "message": message or self.default_detail["message"],
            "errors": errors or self.default_detail["errors"],
        }
        super().__init__(detail=detail)
