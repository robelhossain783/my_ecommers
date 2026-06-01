from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Banner
from .serializers import BannerSerializer
from rest_framework import status


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