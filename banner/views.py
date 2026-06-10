from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Banner, NotificationBanner
from .serializers import BannerSerializer, NotificationBannerSerializer
from rest_framework import status
from django.utils import timezone


class BannerListAPIView(APIView):

    def get(self, request):
        banners = Banner.objects.filter(is_active=True).order_by("-created_at")
        serializer = BannerSerializer(banners, many=True)

        return Response(serializer.data)


class BannerCreateAPIView(APIView):

    def post(self, request):
        serializer = BannerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Banner created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BannerDeleteAPIView(APIView):

    def delete(self, request, pk):
        try:
            banner = Banner.objects.get(pk=pk)
        except Banner.DoesNotExist:
            return Response(
                {"error": "Banner not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        banner.delete()
        return Response(
            {"message": "Banner deleted successfully"},
            status=status.HTTP_200_OK
        )


# Notify banner View
class NotificationBannerAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    # RESPONSE
    # {
    #     "success": true,
    #     "data": {
    #         "id": 1,
    #         "title": "Eid Mega Sale",
    #         "image": "https://cdn.buyfest.com/media/notification_banners/eid_sale.jpg",
    #         "target_url": "https://buyfest.com/eid-sale"
    #     }
    # }

    def get(self, request):
        now = timezone.now()

        # banner = (
        #     NotificationBanner.objects.filter(
        #         is_active=True
        #     )
        #     .filter(
        #         start_date__lte=now
        #     )
        #     .filter(
        #         end_date__gte=now
        #     )
        #     .first()
        # )
        banner = (
            NotificationBanner.objects.filter(
                is_active=True
            )
            .filter(
                Q(start_date__isnull=True) |
                Q(start_date__lte=now)
            )
            .filter(
                Q(end_date__isnull=True) |
                Q(end_date__gte=now)
            )
            .first()
        )

        if not banner:
            return Response(
                {
                    "success": True,
                    "data": None
                },
                status=status.HTTP_200_OK
            )

        serializer = NotificationBannerSerializer(
            banner,
            context={"request": request}
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# API for dashboard adminmanagement
class CreateNotificationBannerAPIView(APIView):
    def post(self, request):
        serializer = NotificationBannerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Notification banner created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class NotificationBannerListAPIView(APIView):

    def get(self, request):
        banners = NotificationBanner.objects.all()

        serializer = NotificationBannerSerializer(
            banners,
            many=True
        )

        return Response(
            {
                "success": True,
                "count": banners.count(),
                "data": serializer.data,
            }
        )


class UpdateNotificationBannerStatusAPIView(APIView):

    def post(self, request, banner_id):
        try:
            banner = NotificationBanner.objects.get(id=banner_id)

        except NotificationBanner.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Banner not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        is_active = request.data.get("is_active")

        if is_active is None:
            return Response(
                {
                    "success": False,
                    "message": "is_active field is required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # string true/false handle করার জন্য
        if isinstance(is_active, str):
            is_active = is_active.lower() == "true"

        banner.is_active = is_active
        banner.save(update_fields=["is_active"])

        return Response(
            {
                "success": True,
                "message": "Banner status updated successfully",
                "data": {
                    "id": banner.id,
                    "is_active": banner.is_active,
                }
            },
            status=status.HTTP_200_OK,
        )


class DeleteNotificationBannerAPIView(APIView):

    def delete(self, request, banner_id):
        try:
            banner = NotificationBanner.objects.get(id=banner_id)

        except NotificationBanner.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Banner not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        banner.delete()

        return Response(
            {
                "success": True,
                "message": "Banner deleted successfully",
            }
        )