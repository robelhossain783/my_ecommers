from django.urls import path
from .views import *

urlpatterns = [
    # category
    path(
        "categories/list/",
        CategoryListAPIView.as_view()
    ),

    path(
        "categories/create/",
        CategoryCreateAPIView.as_view()
    ),
    # Products

    path(
        "products/create/",
        ProductCreateAPIView.as_view()
    ),

    path(
        "products/list/",
        ProductListAPIView.as_view()
    ),

    path(
        "products/<slug:slug>/",
        ProductDetailAPIView.as_view()
    ),

    path(
        "products/<int:pk>/delete/",
        ProductDeleteAPIView.as_view()
    ),
]