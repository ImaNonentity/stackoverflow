from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from user_profile.permissions import IsOwnerUser, ReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Vote
from .serializers import VoteOutputSerializer
from .services import RatingCountSystem, VotingCountSystem
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError


# class VoteCreateView(APIView):
#     """ Create New Vote """
#     permission_classes = [IsAuthenticated]
#     serializer_class = VoteOutputSerializer
#
#     @swagger_auto_schema(request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={'action_type': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
#                     'content_type': openapi.Schema(type=openapi.TYPE_STRING, description='list'),
#                     'object_id': openapi.Schema(type=openapi.TYPE_STRING, description='string')})
#     )
#     def post(self, request):
#         serializer = VoteOutputSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             count_system = VotingCountSystem(user=self.request.user, data=serializer.validated_data)
#             count_system.validate_vote_create(data=request.data)
#             count_system.validate_user()
#             try:
#                 serializer.save(user=self.request.user)
#             except IntegrityError:
#                 content = {"ERROR": "You've already cast your vote!"}
#                 return Response(content, status=status.HTTP_400_BAD_REQUEST)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class VoteAddView(APIView):
    """ Create/Update Vote """

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'action_type': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                    'content_type': openapi.Schema(type=openapi.TYPE_STRING, description='list'),
                    'object_id': openapi.Schema(type=openapi.TYPE_STRING, description='string')})
    )
    def post(self, request):
        serializer = VoteOutputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        count_system = VotingCountSystem(user=self.request.user, data=serializer.validated_data)
        vote_obj = count_system.execute()
        serializer_data = VoteOutputSerializer(vote_obj)
        # serializer_data.save()
        print(serializer_data.data)
        serializer.save(user=request.user)
        return Response(serializer_data.data, status=status.HTTP_201_CREATED)
        # data=vote_obj != vote_obj
        # при дате - вызываются дефолтный валидации при объекте - только твои сервисы.

class VoteListView(APIView):
    """ Check All Votes """

    def get(self, request):
        votes = Vote.objects.all()
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VoteUserView(APIView):
    """ Check Votes by User ID """

    def get(self, request, pk):
        queryset = Vote.objects.filter(user__pk=self.request.user.id)
        serializer = VoteSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
