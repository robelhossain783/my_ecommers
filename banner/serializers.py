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
            "is_active",
            "start_date",
            "end_date",
            "created_at",
        )

    def get_image(self, obj):
        if not obj.image:
            return None

        request = self.context.get("request")

        if request is not None:
            return request.build_absolute_uri(obj.image.url)

        # fallback: return relative URL if no request context
        return obj.image.url