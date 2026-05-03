from django.urls import path

from .views import (
    AdminOrderCancelView,
    AdminOrderConfirmView,
    AdminOrderDeliverView,
    AdminOrderShipView,
)

urlpatterns = [
    path(
        "<uuid:pk>/confirm/",
        AdminOrderConfirmView.as_view(),
        name="admin_order_confirm",
    ),
    path("<uuid:pk>/ship/", AdminOrderShipView.as_view(), name="admin_order_ship"),
    path(
        "<uuid:pk>/deliver/",
        AdminOrderDeliverView.as_view(),
        name="admin_order_deliver",
    ),
    path(
        "<uuid:pk>/cancel/", AdminOrderCancelView.as_view(), name="admin_order_cancel"
    ),
]
