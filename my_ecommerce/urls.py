"""my_ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('product.urls')),
#
#     path('api/', include('cart.urls')),
#
#     path('api/', include('order.urls')),
# ]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),

    # APIs
    path('api/', include('product.urls')),
    path('api/', include('cart.urls')),
    path('api/', include('order.urls')),

    # এই লাইনটি যোগ করা হলো: DEBUG = False হলেও যাতে জ্যাঙ্গো মিডিয়া ফাইল সার্ভ করতে পারে
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# লোকাল ডেভেলপমেন্টের (DEBUG = True) সুরক্ষার জন্য এটিও রাখতে পারেন
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# =========================
# LOCAL MEDIA (DEBUG ONLY)
# =========================
# if settings.DEBUG:
#     urlpatterns += static(
#         settings.MEDIA_URL,
#         document_root=settings.MEDIA_ROOT
#     )

# =========================
# PRODUCTION MEDIA (Render FIX)
# # =========================
# urlpatterns += [
#     re_path(
#         r'^media/(?P<path>.*)$',
#         serve,
#         {'document_root': settings.MEDIA_ROOT}
#     ),
# ]