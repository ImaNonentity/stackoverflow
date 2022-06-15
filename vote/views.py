from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from user_profile.permissions import IsOwnerUser, ReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Vote
from .serializers import VoteSerializer
from .services import VotingCountSystem, RatingCountSystem


class VoteCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'action_type': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                    'content_type': openapi.Schema(type=openapi.TYPE_STRING, description='list'),
                    'object_id': openapi.Schema(type=openapi.TYPE_STRING, description='string')})
    )
    def post(self, request):
        rate = RatingCountSystem(action_type=request.data['action_type'],
                                 content_type=request.data['content_type'],
                                 object_id=request.data['object_id'],
                                 user=request.user)
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            rate.validate_user(user=self.request.user)
            serializer.save(user=self.request.user)
            # count.votes_count()
            # count.custom_pre_save_vote.send_robust(sender=Vote)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class VoteListView(APIView):

    # permission_classes = [IsAdminUser]

    def get(self, request):
        votes = Vote.objects.all()
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
