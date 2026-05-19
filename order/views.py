from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from product.models import Product
from .models import Order, OrderItem

from cart.models import Cart
from .serializers import CreateOrderSerializer


class CreateOrderAPIView(APIView):

    def post(self, request):

        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        full_name = data["full_name"]
        phone = data["phone"]
        address = data["address"]

        order_type = data["type"]

        total_amount = 0
        order_items_data = []

        # 🛒 CART FLOW
        if order_type == "cart":

            cart = Cart.objects.filter(id=data.get("cart_id")).first()

            if not cart:
                return Response({"message": "Cart not found"}, status=400)

            cart_items = cart.items.select_related("product")

            for item in cart_items:
                total_amount += item.product.price * item.quantity

                order_items_data.append({
                    "product": item.product,
                    "quantity": item.quantity,
                    "price": item.product.price
                })

            cart_items.delete()

        # ⚡ BUY NOW FLOW
        elif order_type == "buy_now":

            product = Product.objects.filter(id=data.get("product_id")).first()

            if not product:
                return Response({"message": "Product not found"}, status=400)

            quantity = data.get("quantity", 1)

            total_amount = product.price * quantity

            order_items_data.append({
                "product": product,
                "quantity": quantity,
                "price": product.price
            })

        # 🧾 CREATE ORDER
        order = Order.objects.create(
            user=None,
            full_name=full_name,
            phone=phone,
            address=address,
            total_amount=total_amount
        )

        # 🧾 ORDER ITEMS
        OrderItem.objects.bulk_create([
            OrderItem(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["price"]
            )
            for item in order_items_data
        ])

        return Response({
            "message": "Order placed successfully",
            "order_id": order.id,
            "total_amount": total_amount
        }, status=201)


class OrderListAPIView(APIView):

    # permission_classes = [IsAdminUser]

    def get(self, request):

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        order_status = request.query_params.get("status")

        orders = Order.objects.prefetch_related(
            "items",
            "items__product"
        ).select_related(
            "user"
        ).order_by("-id")

        if order_status:
            orders = orders.filter(status=order_status)

        if start_date:
            orders = orders.filter(created_at__date__gte=start_date)

        if end_date:
            orders = orders.filter(created_at__date__lte=end_date)

        serializer = CreateOrderSerializer(orders, many=True)

        return Response(
            {
                "message": "Order list fetched successfully",
                "total_orders": orders.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )