from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from ..models import Order
from ..services import OrderService
from .serializers import OrderCreateSerializer, OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user, is_active=True
        ).prefetch_related("items__product_variant__product")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = OrderService.create_order(
            user=request.user,
            items_payload=serializer.validated_data["items"],
            shipping_address=serializer.validated_data["shipping_address"],
        )
        data = OrderSerializer(order).data
        return Response(data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user, is_active=True
        ).prefetch_related("items__product_variant__product")

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class OrderCancelView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(
            Order, id=kwargs["pk"], user=request.user, is_active=True
        )
        order = OrderService.customer_cancel_order(order)
        serializer = self.get_serializer(order)
        return Response(serializer.data)


class AdminOrderConfirmView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs["pk"], is_active=True)
        order = OrderService.confirm_order(order)
        serializer = self.get_serializer(order)
        return Response(serializer.data)


class AdminOrderShipView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs["pk"], is_active=True)
        order = OrderService.ship_order(order)
        serializer = self.get_serializer(order)
        return Response(serializer.data)


class AdminOrderDeliverView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs["pk"], is_active=True)
        order = OrderService.deliver_order(order)
        serializer = self.get_serializer(order)
        return Response(serializer.data)


class AdminOrderCancelView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs["pk"], is_active=True)
        order = OrderService.admin_cancel_order(order)
        serializer = self.get_serializer(order)
        return Response(serializer.data)
