from django.urls import path

from .views import OrderCancelView, OrderDetailView, OrderListCreateView

urlpatterns = [
    path("", OrderListCreateView.as_view(), name="order_list_create"),
    path("<uuid:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("<uuid:pk>/cancel/", OrderCancelView.as_view(), name="order_cancel"),
]
