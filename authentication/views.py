from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import CustomerProfile



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class AdminRegisterAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_staff and not request.user.is_superuser:
            return Response(
                {"error": "Only admins are allowed to register new admin users"},
                status=status.HTTP_403_FORBIDDEN
            )

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
                tokens = get_tokens_for_user(user)
                return Response({
                    "message": "Login successful",
                    "username": user.username,
                    "is_staff": user.is_staff,
                    "access": tokens["access"],
                    "refresh": tokens["refresh"],
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


class CustomerRegisterAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email", "")
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")

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
            first_name=first_name,
            last_name=last_name,
            is_staff=False
        )
        CustomerProfile.objects.create(user=user)
        return Response(
            {
                "message": "Customer account created successfully",
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            },
            status=status.HTTP_201_CREATED
        )


class CustomerLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            profile, _ = CustomerProfile.objects.get_or_create(user=user)
            avatar_url = None
            if profile.avatar:
                try:
                    avatar_url = profile.avatar.url
                    if not avatar_url.startswith('http'):
                        avatar_url = request.build_absolute_uri(avatar_url)
                except Exception:
                    pass
            return Response({
                "message": "Login successful",
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_staff": user.is_staff,
                "phone": profile.phone,
                "address": profile.address,
                "avatar": avatar_url
            }, status=status.HTTP_200_OK)
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_400_BAD_REQUEST
        )


class CustomerProfileAPIView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        profile, _ = CustomerProfile.objects.get_or_create(user=user)
        
        avatar_url = None
        if profile.avatar:
            try:
                avatar_url = profile.avatar.url
                if not avatar_url.startswith('http'):
                    avatar_url = request.build_absolute_uri(avatar_url)
            except Exception:
                pass

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_staff": user.is_staff,
            "phone": profile.phone,
            "address": profile.address,
            "avatar": avatar_url,
        }, status=status.HTTP_200_OK)

    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        profile, _ = CustomerProfile.objects.get_or_create(user=user)
        
        # Update User details
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if email is not None:
            user.email = email
        user.save()
        
        # Update profile details
        phone = request.data.get("phone")
        address = request.data.get("address")
        
        # Check if an avatar file is uploaded
        avatar = request.FILES.get("avatar")
        
        if phone is not None:
            profile.phone = phone
        if address is not None:
            profile.address = address
        if avatar is not None:
            profile.avatar = avatar
            
        profile.save()
        
        avatar_url = None
        if profile.avatar:
            try:
                avatar_url = profile.avatar.url
                if not avatar_url.startswith('http'):
                    avatar_url = request.build_absolute_uri(avatar_url)
            except Exception:
                pass
                
        return Response({
            "message": "Profile updated successfully",
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_staff": user.is_staff,
            "phone": profile.phone,
            "address": profile.address,
            "avatar": avatar_url,
        }, status=status.HTTP_200_OK)


