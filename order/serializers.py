from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = "__all__"


class CreateOrderSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=["cart", "buy_now"])

    cart_id = serializers.IntegerField(required=False)
    product_id = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(required=False, default=1)

    full_name = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()