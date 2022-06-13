from django.db.models.signals import post_save
from django.dispatch import receiver
from drf_yasg import openapi
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.conf import settings
from .serializers import UserSerializer
from .permissions import IsOwnerUser, ReadOnly
from drf_yasg.utils import swagger_auto_schema

# KNOX IMPORTS
# from knox.views import LoginView as KnoxLoginView
# from knox.models import AuthToken


# USER PROFILE VIEWS

class UpdateUserView(APIView):
    """ Update User Profile """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser|IsOwnerUser]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
            'birth_date': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    ))
    def put(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserDetailView(APIView):
    """ Get User Profile Details """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & ReadOnly]

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

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


class DeleteUserView(APIView):
    """ Delete User """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser|IsOwnerUser]

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        operation = user.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)
