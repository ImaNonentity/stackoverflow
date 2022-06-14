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

from .serializers import UserAvatarSerializer, UserSerializer
from .models import User
from django.contrib.auth import authenticate
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema


# class CheckUserImageView(APIView):
#     """ Check User Avatar """
#     def get(self, request):
#
#         serializer = UserAvatarSerializer(data=request.data, instance=request.user)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=request.data, status=status.HTTP_200_OK)


class UploadUserImageView(APIView):
    """ Upload User Avatar """

    # permission_classes = [IsOwnerUser]
    parser_classes = (MultiPartParser, )

    @swagger_auto_schema(
        operation_description='Upload your avatar image',
        operation_id='Upload avatar file',
        manual_parameters=[openapi.Parameter(
            name="file",
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            required=True,
            description="Image"
        )],
        responses={400: 'Invalid data in uploaded file',
                   200: 'Success'},
    )
    def post(self, request, format=None):

        serializer = UserAvatarSerializer(data=request.data, instance=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response("Image updated!", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#
# class UploadUserImageView(ListAPIView):
#     parser_classes = [MultiPartParser, FormParser]
#     serializer_class = UserAvatarSerializer
#
#     @swagger_auto_schema(
#             operation_description='Upload your avatar image',
#             operation_id='Upload avatar file',
#             manual_parameters=[openapi.Parameter(
#                 name="file",
#                 in_=openapi.IN_FORM,
#                 type=openapi.TYPE_FILE,
#                 required=True,
#                 description="Image"
#             )],
#             responses={400: 'Invalid data in uploaded file',
#                        200: 'Success'},
#         )
#     def post(self, request, *args, **kwargs):
#         file = request.data['profile_photo']
#         user = User.objects.get(pk=pk)
#         user.profile_photo = file
#         user.save()
#         return Response("Image updated!", status=status.HTTP_200_OK)




# USER PROFILE VIEWS

# class UpdateUserView(APIView):
#     """ Update User Profile """
#
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAdminUser|IsOwnerUser]
#
#     @swagger_auto_schema(request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'email': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
#             'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
#             'birth_date': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
#         }
#     ))
#     def put(self, request, pk):
#         try:
#             user = User.objects.get(id=pk)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#         self.check_object_permissions(request, user)
#         serializer = UserSerializer(user, data=request.data)
#         data = {}
#         if serializer.is_valid():
#             serializer.save()
#             data["success"] = "update successful"
#             return Response(data=data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
#
#
# class UserDetailView(APIView):
#     """ Get User Profile Details """
#
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated & ReadOnly]
#
#     def get(self, request, pk):
#         try:
#             user = User.objects.get(id=pk)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#         serializer = UserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class UserListView(APIView):
#     """ Get Users List For Admin """
#
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAdminUser]
#
#     def get(self, request):
#         user = User.objects.all()
#         serializer = UserSerializer(user, many=True)
#         self.check_object_permissions(request, user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class DeleteUserView(APIView):
#     """ Delete User """
#
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAdminUser|IsOwnerUser]
#
#     def delete(self, request, pk):
#         try:
#             user = User.objects.get(pk=pk)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#         operation = user.delete()
#         data = {}
#         if operation:
#             data["success"] = "delete successful"
#         else:
#             data["failure"] = "delete failed"
#         return Response(data=data)
