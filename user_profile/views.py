from django.db.models.signals import post_save
from django.dispatch import receiver
from drf_yasg import openapi
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .permissions import IsOwnerUser, ReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

from .serializers import UserAvatarSerializer, UserSerializer
from .models import User
from .services import UserProfileService
from django.contrib.auth import authenticate
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema


class UploadUserImageView(APIView):
    """ Upload User Avatar """

    parser_classes = [MultiPartParser]
    permission_classes = [IsOwnerUser | IsAdminUser]

    @swagger_auto_schema(
        operation_description='Upload your avatar image',
        operation_id='Upload avatar file',
        manual_parameters=[openapi.Parameter(
            name="profile_photo",
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            required=True,
            description="Image"
        )],
        responses={400: 'Invalid data in uploaded file',
                   200: 'Success'},
    )
    def post(self, request, pk):
        queryset = User.objects.get(pk=self.request.user.id)
        serializer = UserAvatarSerializer(instance=queryset, data=request.data)
        if serializer.is_valid():
            serializer.update(instance=queryset, validated_data=serializer.validated_data)
            us = UserProfileService(queryset)
            us.save_profile()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileUpdateView(APIView):
    """ Update User Profile """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerUser | IsAdminUser]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
            'birth_date': openapi.Schema(type=openapi.TYPE_STRING, description='birth_date'),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='first_name'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='last_name'),
        }
    ))
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            us = UserProfileService(request.user)
            us.save_profile()
            self.check_object_permissions(request, request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """ Get User Profile Details """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & ReadOnly]

    def get(self, request, pk):
        data = {}
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            data["error"] = "User with this ID does not exist."
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserListView(APIView):
    """ Get Users List For Admin """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        self.check_object_permissions(request, user)
        return Response(serializer.data, status=status.HTTP_200_OK)
