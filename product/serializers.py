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


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class ProductReviewSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductReview
        fields = ["id", "name", "rating", "comment", "created_at", "avatar_url"]

    def get_avatar_url(self, obj):
        """Return the reviewer's avatar URL if they are a linked user with a profile."""
        if not obj.user:
            return None
        try:
            profile = obj.user.customer_profile
            if profile.avatar:
                request = self.context.get("request")
                try:
                    url = profile.avatar.url
                    if request and not url.startswith("http"):
                        return request.build_absolute_uri(url)
                    return url
                except Exception:
                    return None
        except Exception:
            return None
        return None


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
