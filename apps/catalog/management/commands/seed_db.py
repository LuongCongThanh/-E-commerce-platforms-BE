import random

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.catalog.models import Category, Product, ProductImage, ProductVariant


class Command(BaseCommand):
    help = "Seeds the database with initial catalog data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # 1. Create Categories
        categories_data = [
            "Electronics",
            "Clothing",
            "Home & Garden",
            "Books",
            "Sports",
            "Toys",
            "Health",
            "Beauty",
            "Automotive",
            "Jewelry",
        ]

        categories = []
        for name in categories_data:
            cat, created = Category.objects.get_or_create(
                name=name, defaults={"slug": slugify(name)}
            )
            categories.append(cat)
            if created:
                self.stdout.write(f"Created category: {name}")

        # 2. Create Products
        for i in range(1, 51):
            category = random.choice(categories)
            product_name = f"Product {i} - {category.name}"
            product, created = Product.objects.get_or_create(
                name=product_name,
                category=category,
                defaults={
                    "slug": slugify(product_name),
                    "description": f"Premium quality {product_name} with exceptional features.",
                },
            )

            if created:
                # 3. Create Variants
                skus = [f"SKU-{i}-A", f"SKU-{i}-B"]
                for sku in skus:
                    ProductVariant.objects.create(
                        product=product,
                        sku=sku,
                        price=random.randint(100, 5000) * 1000,  # In VND
                        stock_quantity=random.randint(10, 100),
                    )

                # 4. Create Images
                # Using placeholder images
                ProductImage.objects.create(
                    product=product,
                    image_url=f"https://picsum.photos/seed/{product.slug}/600/600",
                    is_thumbnail=True,
                )

                self.stdout.write(f"Created product: {product_name}")

        self.stdout.write(self.style.SUCCESS("Successfully seeded database!"))
