from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from .models import Message, Room
from .serializers import MessageSerializer, OutputMessageSerializer, RoomSerializer
from .services import CreateMessageService, GetMessageService


def index(request):
    return render(request, 'chat/index.html')


class MessageSendView(APIView):

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message_service = CreateMessageService(
            sender_id=self.request.sender_id,
            receiver_id=self.request.receiver_id,
            created_at=self.request.created_at
        )
        message = message_service.execute()
        serializer.save(message=message)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LastMessagesInRoomsView(APIView):
    user_param = openapi.Parameter('sender_id', in_=openapi.IN_QUERY, description='sender_id',
                                   type=openapi.TYPE_STRING, )

    @swagger_auto_schema(manual_parameters=[user_param])
    def get(self, request):
        message_service = GetMessageService(
            user_id=request.query_params.get('sender_id'),
        )
        message = message_service.get_last_messages()
        serializer = OutputMessageSerializer(message, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SingleRoomMessagesView(APIView):

    def get(self, request):
        message_service = GetMessageService(
            user_id=request.data['sender_id'],
        )
        message = message_service.get_room_messages(room=request.room)
        serializer = OutputMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)
