
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
    path('api/', include('banner.urls')),
    # path('api/', include('auth.urls')),

    # এই লাইনটি যোগ করা হলো: DEBUG = False হলেও যাতে জ্যাঙ্গো মিডিয়া ফাইল সার্ভ করতে পারে
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# লোকাল ডেভেলপমেন্টের (DEBUG = True) সুরক্ষার জন্য এটিও রাখতে পারেন
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
#
# urlpatterns = [
#     path("admin/", admin.site.urls),
#
#     path("api/", include("product.urls")),
#     path("api/", include("cart.urls")),
#     path("api/", include("order.urls")),
# ]