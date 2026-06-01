from django.urls import path
from .views import BannerListAPIView, BannerCreateAPIView

urlpatterns = [
    path("banner/list/", BannerListAPIView.as_view()),
    path("banner/create/", BannerCreateAPIView.as_view()),
]