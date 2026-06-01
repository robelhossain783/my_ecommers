from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AdminRegisterAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email", "")

        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            is_staff=True
        )
        return Response(
            {"message": "Admin user created successfully"},
            status=status.HTTP_201_CREATED
        )


class AdminLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_staff or user.is_superuser:
                return Response({
                    "message": "Login successful",
                    "username": user.username,
                    "is_staff": user.is_staff
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Not authorized as admin"},
                    status=status.HTTP_403_FORBIDDEN
                )
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_400_BAD_REQUEST
        )
