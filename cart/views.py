from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Cart, CartItem
from .serializers import CartItemSerializer

from product.models import Product


class AddToCartAPIView(APIView):

    def post(self, request):

        session_id = request.data.get("session_id")

        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        # get product
        try:
            product = Product.objects.get(id=product_id)

        except Product.DoesNotExist:
            return Response(
                {"message": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # create or get cart using session_id
        cart, created = Cart.objects.get_or_create(
            session_id=session_id
        )

        # create or update cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        return Response(
            {
                "message": "Product added to cart",
                "cart_id": cart.id,
                "session_id": session_id
            },
            status=status.HTTP_201_CREATED
        )


class CartListAPIView(APIView):

    def get(self, request):

        user = request.user

        cart = Cart.objects.filter(user=user).first()

        if not cart:
            return Response([])

        items = cart.items.select_related("product")

        serializer = CartItemSerializer(
            items,
            many=True
        )

        return Response(serializer.data)


class RemoveCartItemAPIView(APIView):

    def delete(self, request, item_id):

        user = request.user

        try:
            cart_item = CartItem.objects.get(
                id=item_id,
                cart__user=user
            )

        except CartItem.DoesNotExist:
            return Response(
                {"message": "Cart item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        cart_item.delete()

        return Response(
            {"message": "Item removed"}
        )