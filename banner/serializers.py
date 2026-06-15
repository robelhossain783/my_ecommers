from rest_framework import serializers
from .models import Banner, NotificationBanner


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


#  Notify banner serializer
class NotificationBannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationBanner
        fields = (
            "id",
            "title",
            "image",
            "target_url",
            "is_active",
            "start_date",
            "end_date",
            "created_at",
        )