from rest_framework import serializers

from ..models import Order, OrderItem


class ShippingAddressSerializer(serializers.Serializer):
    recipient_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=500)
    city = serializers.CharField(max_length=100)


class OrderItemCreateSerializer(serializers.Serializer):
    product_variant_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemCreateSerializer(many=True)
    shipping_address = ShippingAddressSerializer()


class OrderItemSerializer(serializers.ModelSerializer):
    sku = serializers.ReadOnlyField(source="product_variant.sku")
    product_name = serializers.ReadOnlyField(source="product_variant.product.name")

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_variant",
            "sku",
            "product_name",
            "quantity",
            "unit_price",
            "currency",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return sum(item.unit_price * item.quantity for item in obj.items.all())

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "currency",
            "shipping_address",
            "total",
            "items",
            "created_at",
            "updated_at",
        ]
