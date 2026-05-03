from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.catalog.models import ProductVariant

from .exceptions import OrderInvalidState, OutOfStock
from .models import Order, OrderItem, OrderStatus


class OrderService:
    @staticmethod
    @transaction.atomic
    def create_order(user, items_payload):
        if not items_payload:
            raise ValidationError("Order must include at least one item.")

        variant_ids = [item["product_variant_id"] for item in items_payload]
        variants = ProductVariant.objects.filter(id__in=variant_ids, is_active=True)
        variants_by_id = {str(variant.id): variant for variant in variants}

        if len(variants_by_id) != len(set(variant_ids)):
            raise ValidationError("One or more product variants are invalid.")

        currencies = {
            variants_by_id[item["product_variant_id"]].currency
            for item in items_payload
        }
        if len(currencies) > 1:
            raise ValidationError("A single order must use one currency.")

        order = Order.objects.create(user=user, currency=currencies.pop())
        order_items = []
        for item in items_payload:
            variant = variants_by_id[item["product_variant_id"]]
            order_items.append(
                OrderItem(
                    order=order,
                    product_variant=variant,
                    quantity=item["quantity"],
                    unit_price=variant.price,
                    currency=variant.currency,
                )
            )
        OrderItem.objects.bulk_create(order_items)
        return order

    @staticmethod
    @transaction.atomic
    def confirm_order(order):
        order = Order.objects.select_for_update().get(id=order.id)
        if order.status != OrderStatus.PENDING:
            raise OrderInvalidState(
                message="Chỉ có thể xác nhận đơn hàng đang ở trạng thái PENDING.",
                errors={"status": ["Only PENDING orders can be confirmed."]},
            )

        order_items = list(
            OrderItem.objects.select_related("product_variant").filter(order=order)
        )
        variant_ids = [item.product_variant_id for item in order_items]
        variants = ProductVariant.objects.select_for_update().filter(id__in=variant_ids)
        variants_by_id = {variant.id: variant for variant in variants}

        for item in order_items:
            variant = variants_by_id[item.product_variant_id]
            if variant.stock_quantity < item.quantity:
                raise OutOfStock(
                    message="Tồn kho không đủ để xác nhận đơn hàng.",
                    errors={
                        "items": [f"Insufficient inventory for SKU {variant.sku}."]
                    },
                )

        for item in order_items:
            variant = variants_by_id[item.product_variant_id]
            variant.stock_quantity -= item.quantity
            variant.save(update_fields=["stock_quantity", "updated_at"])

        order.status = OrderStatus.CONFIRMED
        order.save(update_fields=["status", "updated_at"])
        return order

    @staticmethod
    @transaction.atomic
    def customer_cancel_order(order):
        order = Order.objects.select_for_update().get(id=order.id)
        if order.status != OrderStatus.PENDING:
            raise OrderInvalidState(
                message="Khách hàng chỉ có thể hủy đơn của mình khi đơn đang ở trạng thái PENDING.",
                errors={
                    "status": ["Only PENDING orders can be cancelled by customer."]
                },
            )

        order.status = OrderStatus.CANCELLED
        order.save(update_fields=["status", "updated_at"])
        return order

    @staticmethod
    @transaction.atomic
    def admin_cancel_order(order):
        order = Order.objects.select_for_update().get(id=order.id)
        if order.status not in {OrderStatus.PENDING, OrderStatus.CONFIRMED}:
            raise OrderInvalidState(
                message="Admin chỉ có thể hủy đơn đang ở trạng thái PENDING hoặc CONFIRMED.",
                errors={
                    "status": [
                        "Only PENDING or CONFIRMED orders can be cancelled by admin."
                    ]
                },
            )

        if order.status == OrderStatus.CONFIRMED:
            order_items = (
                OrderItem.objects.select_related("product_variant")
                .select_for_update()
                .filter(order=order)
            )
            for item in order_items:
                variant = item.product_variant
                variant.stock_quantity += item.quantity
                variant.save(update_fields=["stock_quantity", "updated_at"])

        order.status = OrderStatus.CANCELLED
        order.save(update_fields=["status", "updated_at"])
        return order

    @staticmethod
    @transaction.atomic
    def ship_order(order):
        order = Order.objects.select_for_update().get(id=order.id)
        if order.status != OrderStatus.CONFIRMED:
            raise OrderInvalidState(
                message="Chỉ có thể chuyển đơn sang SHIPPED khi đơn đang ở trạng thái CONFIRMED.",
                errors={"status": ["Only CONFIRMED orders can be shipped."]},
            )

        order.status = OrderStatus.SHIPPED
        order.save(update_fields=["status", "updated_at"])
        return order

    @staticmethod
    @transaction.atomic
    def deliver_order(order):
        order = Order.objects.select_for_update().get(id=order.id)
        if order.status != OrderStatus.SHIPPED:
            raise OrderInvalidState(
                message="Chỉ có thể chuyển đơn sang DELIVERED khi đơn đang ở trạng thái SHIPPED.",
                errors={"status": ["Only SHIPPED orders can be delivered."]},
            )

        order.status = OrderStatus.DELIVERED
        order.save(update_fields=["status", "updated_at"])
        return order
