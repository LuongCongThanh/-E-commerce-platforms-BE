from rest_framework import serializers

from ..models import Category, Product, ProductImage, ProductVariant


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent", "children"]

    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.all(), many=True).data
        return []


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ["id", "sku", "price", "currency", "stock_quantity"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image_url", "is_thumbnail"]


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name")
    thumbnail = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category_name",
            "thumbnail",
            "min_price",
            "created_at",
        ]

    def get_thumbnail(self, obj):
        image = obj.images.filter(is_thumbnail=True).first()
        if image:
            return image.image_url
        return None

    def get_min_price(self, obj):
        variant = obj.variants.order_by("price").first()
        if variant:
            return {"price": variant.price, "currency": variant.currency}
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "category",
            "variants",
            "images",
            "created_at",
        ]
