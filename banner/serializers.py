from rest_framework import serializers
from .models import Banner, NotificationBanner


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


#  Notify banner serializer
class NotificationBannerSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = NotificationBanner
        fields = (
            "id",
            "title",
            "image",
            "target_url",
        )

    def get_image(self, obj):
        request = self.context.get("request")

        if not obj.image:
            return None

        return request.build_absolute_uri(
            obj.image.url
        )