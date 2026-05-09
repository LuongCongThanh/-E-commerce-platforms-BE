import pytest
from django.contrib.auth import get_user_model

from apps.catalog.models import Category, Product, ProductVariant
from apps.orders.models import Order, OrderItem

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="buyer@example.com",
        password="testpass123",
        first_name="Nguyen",
        last_name="Van A",
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        email="admin@example.com",
        password="adminpass123",
    )


@pytest.fixture
def category(db):
    return Category.objects.create(name="Electronics")


@pytest.fixture
def product(db, category):
    return Product.objects.create(name="Laptop", category=category)


@pytest.fixture
def variant(db, product):
    v = ProductVariant.objects.create(
        product=product,
        sku="LAP-001",
        price="15000000.00",
        currency="VND",
        stock_quantity=10,
    )
    v.refresh_from_db()
    return v


@pytest.fixture
def variant_b(db, product):
    v = ProductVariant.objects.create(
        product=product,
        sku="LAP-002",
        price="20000000.00",
        currency="VND",
        stock_quantity=5,
    )
    v.refresh_from_db()
    return v


@pytest.fixture
def shipping_address():
    return {
        "recipient_name": "Nguyen Van A",
        "phone": "0901234567",
        "address": "123 Le Loi",
        "city": "Ho Chi Minh",
    }


@pytest.fixture
def pending_order(db, user, variant, shipping_address):
    order = Order.objects.create(
        user=user,
        currency="VND",
        shipping_address=shipping_address,
    )
    OrderItem.objects.create(
        order=order,
        product_variant=variant,
        quantity=2,
        unit_price=variant.price,
        currency=variant.currency,
    )
    return order


@pytest.fixture
def confirmed_order(db, pending_order, variant):
    from apps.orders.services import OrderService

    return OrderService.confirm_order(pending_order)
