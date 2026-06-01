from django.urls import path
from .views import *

urlpatterns = [

    path(
        "create-order/",
        CreateOrderAPIView.as_view()
    ),

    path(
        "orders/list/",
        OrderListAPIView.as_view()
    ),
    path(
        "orders/<int:pk>/update-status/",
        OrderStatusUpdateAPIView.as_view()
    ),
]