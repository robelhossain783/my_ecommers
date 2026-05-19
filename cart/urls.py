from django.urls import path
from .views import *

urlpatterns = [

    path(
        "add-to-cart/",
        AddToCartAPIView.as_view()
    ),

    path(
        "cart-list/",
        CartListAPIView.as_view()
    ),

    path(
        "remove-cart-item/<int:item_id>/",
        RemoveCartItemAPIView.as_view()
    ),
]