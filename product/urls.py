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
    path(
        "categories/<int:pk>/delete/",
        DeleteCategoryAPIView.as_view(),
        name="delete-category"
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

    # Gallery
    path(
        "products/<int:pk>/gallery/add/",
        ProductGalleryAddAPIView.as_view(),
        name="product-gallery-add"
    ),
    path(
        "products/gallery/<int:img_id>/delete/",
        ProductGalleryDeleteAPIView.as_view(),
        name="product-gallery-delete"
    ),

    # Reviews
    path(
        "products/<int:pk>/reviews/add/",
        ProductReviewAddAPIView.as_view(),
        name="product-review-add"
    ),
]