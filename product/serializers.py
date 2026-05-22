from rest_framework import serializers
from .models import Product, Category


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
class ProductSerializer(serializers.ModelSerializer):
    category = CreateCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product

        fields = [
            "category",
            "name",
            "slug",
            "image",
            "description",
            "sell_price",
            "regular_price",
            "stock",
            "is_active",
        ]
