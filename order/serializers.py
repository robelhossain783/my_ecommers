from rest_framework import serializers
from .models import Order, OrderItem, PaymentMethod
from product.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)


class CreateOrderSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=[("cart", "Cart"), ("buy_now", "Buy Now")]
    )

    cart_id = serializers.IntegerField(required=False, allow_null=True)
    product_id = serializers.IntegerField(required=False, allow_null=True)

    quantity = serializers.IntegerField(required=False, default=1)
    items = OrderItemInputSerializer(many=True, required=False)

    full_name = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()

    delivery_charge = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        required=False
    )

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
    amount = serializers.DecimalField(source='total_amount', max_digits=12, decimal_places=2, read_only=True)

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
            "total_amount",
            "amount",
        ]

    def get_user_email(self, obj):
        if obj.user:
            return obj.user.email
        return None