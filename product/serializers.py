from rest_framework import serializers
from .models import Product, Category, ProductImage, ProductReview


class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category

        fields = [
            "id",
            "name",
            "slug",
            "image",
            "is_active",
            "created_at",
        ]


# class ProductSerializer(serializers.ModelSerializer):
#
#     category = CreateCategorySerializer(read_only=True)
#
#     class Meta:
#         model = Product
#         fields = "__all__"
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ["id", "name", "rating", "comment", "created_at"]


class ProductSerializer(serializers.ModelSerializer):
    category = CreateCategorySerializer(read_only=True)
    gallery_images = ProductImageSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product

        fields = [
            "id",
            "category",
            "name",
            "slug",
            "image",
            "description",
            "sell_price",
            "regular_price",
            "stock",
            "is_active",
            "is_new_arrivals",
        ]
