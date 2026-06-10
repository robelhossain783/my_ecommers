from django.urls import path
from .views import BannerListAPIView, BannerCreateAPIView, BannerDeleteAPIView, NotificationBannerAPIView, \
    CreateNotificationBannerAPIView, NotificationBannerListAPIView, UpdateNotificationBannerStatusAPIView, \
    DeleteNotificationBannerAPIView

urlpatterns = [
    path("banner/list/", BannerListAPIView.as_view()),
    path("banner/create/", BannerCreateAPIView.as_view()),
    path("banner/<int:pk>/delete/", BannerDeleteAPIView.as_view()),
    path(
        "banner/notification-banner/",
        NotificationBannerAPIView.as_view(),
        name="notification-banner"
    ),

    # Notify Create+update+delete
    path(
        "banner/notification-banner/create/",
        CreateNotificationBannerAPIView.as_view(),
        name="create_notification_banner",
    ),

    path(
        "banner/notification-banner/list/",
        NotificationBannerListAPIView.as_view(),
        name="notification_banner_list",
    ),

    path(
        "banner/notification-banner/<int:banner_id>/status/",
        UpdateNotificationBannerStatusAPIView.as_view(),
        name="update_notification_banner_status",
    ),

    path(
        "banner/notification-banner/<int:banner_id>/delete/",
        DeleteNotificationBannerAPIView.as_view(),
        name="delete_notification_banner",
    ),
]