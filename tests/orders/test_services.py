from unittest.mock import patch

import pytest
from rest_framework.exceptions import ValidationError

from apps.orders.exceptions import OrderInvalidState, OutOfStock
from apps.orders.models import Order, OrderItem, OrderStatus
from apps.orders.services import OrderService

# ---------------------------------------------------------------------------
# create_order
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_create_order_happy_path(user, variant, shipping_address):
    items = [{"product_variant_id": str(variant.id), "quantity": 2}]

    with patch("apps.orders.services.send_mail"):
        order = OrderService.create_order(user, items, shipping_address)

    assert order.status == OrderStatus.PENDING
    assert order.user == user
    assert order.currency == "VND"
    assert order.items.count() == 1

    item = order.items.first()
    assert item.quantity == 2
    assert item.unit_price == variant.price


@pytest.mark.django_db
def test_create_order_does_not_deduct_inventory(user, variant, shipping_address):
    stock_before = variant.stock_quantity
    items = [{"product_variant_id": str(variant.id), "quantity": 3}]

    with patch("apps.orders.services.send_mail"):
        OrderService.create_order(user, items, shipping_address)

    variant.refresh_from_db()
    assert variant.stock_quantity == stock_before


@pytest.mark.django_db
def test_create_order_empty_items_raises(user, shipping_address):
    with pytest.raises(ValidationError, match="at least one item"):
        OrderService.create_order(user, [], shipping_address)


@pytest.mark.django_db
def test_create_order_invalid_variant_raises(user, shipping_address):
    import uuid

    items = [{"product_variant_id": str(uuid.uuid4()), "quantity": 1}]
    with pytest.raises(ValidationError, match="invalid"):
        OrderService.create_order(user, items, shipping_address)


@pytest.mark.django_db
def test_create_order_inactive_variant_raises(user, variant, shipping_address):
    variant.is_active = False
    variant.save(update_fields=["is_active"])

    items = [{"product_variant_id": str(variant.id), "quantity": 1}]
    with pytest.raises(ValidationError, match="invalid"):
        OrderService.create_order(user, items, shipping_address)


@pytest.mark.django_db
def test_create_order_mixed_currencies_raises(db, user, product, shipping_address):
    from apps.catalog.models import ProductVariant

    vnd = ProductVariant.objects.create(
        product=product, sku="SKU-VND", price="100", currency="VND", stock_quantity=5
    )
    usd = ProductVariant.objects.create(
        product=product, sku="SKU-USD", price="5", currency="USD", stock_quantity=5
    )
    items = [
        {"product_variant_id": str(vnd.id), "quantity": 1},
        {"product_variant_id": str(usd.id), "quantity": 1},
    ]
    with pytest.raises(ValidationError, match="one currency"):
        OrderService.create_order(user, items, shipping_address)


@pytest.mark.django_db
def test_create_order_email_failure_does_not_abort_order(
    user, variant, shipping_address
):
    """Email is non-blocking — order must be created even if SMTP fails."""
    items = [{"product_variant_id": str(variant.id), "quantity": 1}]

    with patch("apps.orders.services.send_mail", side_effect=Exception("SMTP down")):
        order = OrderService.create_order(user, items, shipping_address)

    assert Order.objects.filter(id=order.id).exists()
    assert order.status == OrderStatus.PENDING


# ---------------------------------------------------------------------------
# confirm_order
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_confirm_order_transitions_to_confirmed(pending_order, variant):
    stock_before = variant.stock_quantity
    qty = pending_order.items.first().quantity

    order = OrderService.confirm_order(pending_order)

    assert order.status == OrderStatus.CONFIRMED
    variant.refresh_from_db()
    assert variant.stock_quantity == stock_before - qty


@pytest.mark.django_db
def test_confirm_order_deducts_exact_quantity(pending_order, variant):
    order = OrderService.confirm_order(pending_order)
    item = order.items.first()

    variant.refresh_from_db()
    assert variant.stock_quantity == 10 - item.quantity


@pytest.mark.django_db
def test_confirm_order_already_confirmed_raises(confirmed_order):
    with pytest.raises(OrderInvalidState):
        OrderService.confirm_order(confirmed_order)


@pytest.mark.django_db
def test_confirm_order_insufficient_stock_raises(pending_order, variant):
    variant.stock_quantity = 1
    variant.save(update_fields=["stock_quantity"])

    with pytest.raises(OutOfStock):
        OrderService.confirm_order(pending_order)


@pytest.mark.django_db
def test_confirm_order_insufficient_stock_does_not_change_status(
    pending_order, variant
):
    """Order must stay PENDING when stock is insufficient — full rollback."""
    variant.stock_quantity = 0
    variant.save(update_fields=["stock_quantity"])

    with pytest.raises(OutOfStock):
        OrderService.confirm_order(pending_order)

    pending_order.refresh_from_db()
    assert pending_order.status == OrderStatus.PENDING


@pytest.mark.django_db
def test_confirm_order_insufficient_stock_does_not_deduct_inventory(
    pending_order, variant
):
    """No partial deduction — inventory untouched when confirm fails."""
    variant.stock_quantity = 0
    variant.save(update_fields=["stock_quantity"])

    with pytest.raises(OutOfStock):
        OrderService.confirm_order(pending_order)

    variant.refresh_from_db()
    assert variant.stock_quantity == 0


@pytest.mark.django_db
def test_confirm_order_multiple_items_all_or_nothing(
    db, user, product, shipping_address
):
    """If second item has no stock, neither item should be deducted."""
    from apps.catalog.models import ProductVariant

    v1 = ProductVariant.objects.create(
        product=product, sku="V1", price="100", currency="VND", stock_quantity=10
    )
    v2 = ProductVariant.objects.create(
        product=product, sku="V2", price="200", currency="VND", stock_quantity=0
    )
    order = Order.objects.create(
        user=user, currency="VND", shipping_address=shipping_address
    )
    OrderItem.objects.create(
        order=order, product_variant=v1, quantity=1, unit_price=v1.price, currency="VND"
    )
    OrderItem.objects.create(
        order=order, product_variant=v2, quantity=1, unit_price=v2.price, currency="VND"
    )

    with pytest.raises(OutOfStock):
        OrderService.confirm_order(order)

    v1.refresh_from_db()
    assert v1.stock_quantity == 10


# ---------------------------------------------------------------------------
# customer_cancel_order
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_customer_cancel_pending_order(pending_order):
    order = OrderService.customer_cancel_order(pending_order)
    assert order.status == OrderStatus.CANCELLED


@pytest.mark.django_db
def test_customer_cancel_confirmed_order_raises(confirmed_order):
    with pytest.raises(OrderInvalidState):
        OrderService.customer_cancel_order(confirmed_order)


@pytest.mark.django_db
def test_customer_cancel_shipped_order_raises(confirmed_order):
    shipped = OrderService.ship_order(confirmed_order)
    with pytest.raises(OrderInvalidState):
        OrderService.customer_cancel_order(shipped)


# ---------------------------------------------------------------------------
# admin_cancel_order
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_admin_cancel_pending_order(pending_order, variant):
    stock_before = variant.stock_quantity

    order = OrderService.admin_cancel_order(pending_order)

    assert order.status == OrderStatus.CANCELLED
    variant.refresh_from_db()
    # no restock for PENDING cancel
    assert variant.stock_quantity == stock_before


@pytest.mark.django_db
def test_admin_cancel_confirmed_order_restocks_inventory(confirmed_order, variant):
    qty = confirmed_order.items.first().quantity
    variant.refresh_from_db()
    stock_after_confirm = variant.stock_quantity

    OrderService.admin_cancel_order(confirmed_order)

    variant.refresh_from_db()
    assert variant.stock_quantity == stock_after_confirm + qty


@pytest.mark.django_db
def test_admin_cancel_shipped_order_raises(confirmed_order):
    shipped = OrderService.ship_order(confirmed_order)
    with pytest.raises(OrderInvalidState):
        OrderService.admin_cancel_order(shipped)


@pytest.mark.django_db
def test_admin_cancel_delivered_order_raises(confirmed_order):
    shipped = OrderService.ship_order(confirmed_order)
    delivered = OrderService.deliver_order(shipped)
    with pytest.raises(OrderInvalidState):
        OrderService.admin_cancel_order(delivered)


# ---------------------------------------------------------------------------
# ship_order
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_ship_confirmed_order(confirmed_order):
    order = OrderService.ship_order(confirmed_order)
    assert order.status == OrderStatus.SHIPPED


@pytest.mark.django_db
def test_ship_pending_order_raises(pending_order):
    with pytest.raises(OrderInvalidState):
        OrderService.ship_order(pending_order)


# ---------------------------------------------------------------------------
# deliver_order
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_deliver_shipped_order(confirmed_order):
    shipped = OrderService.ship_order(confirmed_order)
    order = OrderService.deliver_order(shipped)
    assert order.status == OrderStatus.DELIVERED


@pytest.mark.django_db
def test_deliver_confirmed_order_raises(confirmed_order):
    with pytest.raises(OrderInvalidState):
        OrderService.deliver_order(confirmed_order)


@pytest.mark.django_db
def test_deliver_pending_order_raises(pending_order):
    with pytest.raises(OrderInvalidState):
        OrderService.deliver_order(pending_order)
