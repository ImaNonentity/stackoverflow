from django.shortcuts import render
from django.core import serializers
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from .models import Message, Room
from .serializers import InputMessageSerializer, OutputMessageSerializer
from .services import CreateMessageService, GetMessageService


def index_view(request):
    return render(request, 'chat/index.html', {
        'rooms': Room.objects.all(),
    })


def room_view(request, pk):
    chat_room = Room.objects.get(pk=pk)
    return render(request, 'chat/room.html', {
        'room': chat_room,
    })


class MessageSendView(APIView):

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'receiver_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='receiver_id'),
                    'sender_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='sender_id'),
                    'text': openapi.Schema(type=openapi.TYPE_STRING, description='text')})
    )
    def post(self, request):
        message_service = CreateMessageService(
            sender_id=request.data['sender_id'],
            receiver_id=request.data['receiver_id'],
            text=request.data['text']
        )
        message = message_service.execute()
        return Response(serializers.serialize('json', [message]), status=status.HTTP_200_OK)


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
            user_id=request.query_params.get('sender_id'),
        )
        message = message_service.get_room_messages(room=request.query_params.get('room'))
        serializer = OutputMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)
