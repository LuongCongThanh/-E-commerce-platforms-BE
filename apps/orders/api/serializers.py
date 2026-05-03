from rest_framework import serializers

from apps.catalog.models import ProductVariant

from ..models import Order, OrderItem


class OrderItemCreateSerializer(serializers.Serializer):
    product_variant_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_variant_id(self, value):
        if not ProductVariant.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Invalid product variant.")
        return str(value)


class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemCreateSerializer(many=True)


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

    class Meta:
        model = Order
        fields = ["id", "status", "currency", "items", "created_at", "updated_at"]
