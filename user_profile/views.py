from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import UserSerializer, RegisterSerializer
from .models import User
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
        return Response (serializer.data, status=status.HTTP_200_OK)


class DeleteUserView(APIView):
    """ Delete User """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser|IsOwnerUser]

    def delete(self, request, pk):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        operation = user.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)


# REGISTRATION & AUTHENTICATIONS VIEWS

class RegistrationView(APIView):
    """ Registration """

    authentication_classes = []
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_description="registration")
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Successfully registered new user.'
            data['email'] = user.email
            data['username'] = user.username
            data['id'] = user.id
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


class ObtainAuthTokenView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        context = {}

        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            context['response'] = 'Successfully authenticated.'
            context['id'] = user.id
            context['email'] = email.lower()
            context['token'] = token.key
        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid credentials'

        return Response(context)










# USER VIEWS
# @api_view(['GET'])
# def api_detail_user_view(request, id):
#     try:
#         user = User.objects.get(id=id)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "GET":
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
#
#
# @api_view(['PUT'])
# def api_update_user_view(request, id):
#     try:
#         user = User.objects.get(id=id)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "PUT":
#         serializer = UserSerializer(user, data=request.data)
#         data = {}
#         if serializer.is_valid():
#             serializer.save()
#             data["success"] = "update successful"
#             return Response(data=data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['DELETE'])
# def api_delete_user_view(request, id):
#     try:
#         user = User.objects.get(id=id)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "DELETE":
#         operation = user.delete()
#         data = {}
#         if operation:
#             data["success"] = "delete successful"
#         else:
#             data["failure"] = "delete failed"
#         return Response(data=data)
#
#
# # REGISTRATION & AUTHENTICATIONS VIEWS
# @api_view(['POST'])
# @permission_classes([])
# @authentication_classes([])
# def registration_view(request):
#     if request.method == 'POST':
#         data = {}
#         email = request.data.get('email', '0').lower()
#         if validate_email(email) is not None:
#             data['error_message'] = 'That email is already in use.'
#             data['response'] = 'Error'
#             return Response(data)
#
#         username = request.data.get('username', '0')
#         if validate_username(username) is not None:
#             data['error_message'] = 'That username is already in use.'
#             data['response'] = 'Error'
#             return Response(data)
#
#         serializer = RegisterSerializer(data=request.data)
#
#         if serializer.is_valid():
#             user = serializer.save()
#             data['response'] = 'Successfully registered new user.'
#             data['email'] = user.email
#             data['username'] = user.username
#             data['id'] = user.id
#             token = Token.objects.get(user=user).key
#             data['token'] = token
#         else:
#             data = serializer.errors
#         return Response(data)
#
#
# def validate_email(email):
#     user = None
#     try:
#         user = User.objects.get(email=email)
#     except User.DoesNotExist:
#         return None
#     if user is not None:
#         return email
#
#
# def validate_username(username):
#     user = None
#     try:
#         user = User.objects.get(username=username)
#     except User.DoesNotExist:
#         return None
#     if user is not None:
#         return username






# KNOX REGISTRATION & LOGIN

# class RegisterAPI(generics.GenericAPIView):
#     serializer_class = RegisterSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({
#             "user": UserSerializer(user, context=self.get_serializer_context()).data,
#             "token": AuthToken.objects.create(user)[1]
#         })
#
#
# class LoginAPI(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)
#
#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return super(LoginAPI, self).post(request, format=None)