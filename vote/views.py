from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from user_profile.permissions import IsOwnerUser, ReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Vote
from .serializers import VoteOutputSerializer, VoteSerializer
from .services import RatingUpdateSystem, VotingCountSystem
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError


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
        val_data = serializer.validated_data
        count_system = VotingCountSystem(user=self.request.user,
                                         content_object=val_data.get('content_object'),
                                         content_type=val_data.get('content_type'),
                                         object_id=val_data.get('object_id'),
                                         action_type=val_data.get('action_type'))
        vote_obj = count_system.execute()
        serializer_data = VoteOutputSerializer(vote_obj)
        serializer.save(user=request.user)
        return Response(serializer_data.data, status=status.HTTP_201_CREATED)


class VoteListView(APIView):
    """ Check All Votes """

    def get(self, request):
        votes = Vote.objects.all()
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VoteUserView(APIView):
    """ Check Votes by User ID """

    def get(self, request, pk):
        votes = Vote.objects.filter(user__pk=self.request.user.id)
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
