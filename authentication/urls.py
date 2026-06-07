from django.urls import path
from .views import *

urlpatterns = [
    path(
        "auth/register/",
        AdminRegisterAPIView.as_view()
    ),
    path(
        "auth/login/",
        AdminLoginAPIView.as_view()
    ),
    path(
        "auth/customer/register/",
        CustomerRegisterAPIView.as_view()
    ),
    path(
        "auth/customer/login/",
        CustomerLoginAPIView.as_view()
    ),
]