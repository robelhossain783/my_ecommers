from rest_framework import serializers
from .models import Order, OrderItem, PaymentMethod


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = "__all__"


class CreateOrderSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=[("cart", "Cart"), ("buy_now", "Buy Now")]
    )

    cart_id = serializers.IntegerField(required=False, allow_null=True)
    product_id = serializers.IntegerField(required=False, allow_null=True)

    quantity = serializers.IntegerField(required=False, default=1)

    full_name = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()

    payment_type = serializers.ChoiceField(
        choices=[
            ("COD", "Cash on Delivery"),
            ("BKASH", "bKash"),
            ("NAGAD", "Nagad"),
        ]
    )


class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "user_email",
            "status",
            "payment_type",
            "full_name",
            "phone",
            "address",
            "created_at",
            "items",
        ]

    def get_user_email(self, obj):
        if obj.user:
            return obj.user.email
        return None