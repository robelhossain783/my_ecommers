from django.urls import path
from .views import BannerListAPIView, BannerCreateAPIView, BannerDeleteAPIView

urlpatterns = [
    path("banner/list/", BannerListAPIView.as_view()),
    path("banner/create/", BannerCreateAPIView.as_view()),
    path("banner/<int:pk>/delete/", BannerDeleteAPIView.as_view()),
]