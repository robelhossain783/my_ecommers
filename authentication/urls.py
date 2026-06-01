from django.urls import path
from .views import *

urlpatterns = [
    path(
        "authentication/register/",
        AdminRegisterAPIView.as_view()
    ),
    path(
        "authentication/login/",
        AdminLoginAPIView.as_view()
    ),
]