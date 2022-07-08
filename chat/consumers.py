import os
import django
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chat.models import Room, Message
from chat.services import CreateMessageService, GetMessageService

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework import mixins
from user_profile.models import User
from user_profile.serializers import SimpleUserSerializer


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room = Room.objects.get(id=self.room_name)
        self.user = self.scope['user']
        print(f'User {self.user}')
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )
        message_service = GetMessageService(
            user_id=self.user,
        )
        messages = message_service.get_room_messages(self.room_name)
        self.accept()
        return messages

    def receive(self, text_data=None, bytes_data=None):
        self.send(text_data="Message from server to client")
        data = json.loads(text_data)
        msg = data['message']
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'chat_message',
                'user': self.user.username,
                'message': msg
            }
        )
        # Message.objects.create(sender_id=self.user, room=self.room, text=msg)
        receiver = self.room.receiver_id if self.room.receiver_id != self.user else self.room.sender_id
        message_service = CreateMessageService(
            sender_id=self.user.id,
            receiver_id=receiver.id,
            text=msg
        )
        message_service.execute()

    def chat_message(self, event):
        print("Event...", event)
        self.send(text_data=json.dumps({
            'message': event['message'],
            'type': event['type'],
            'user': event['user'],
        }))

    def disconnect(self, close_code):
        print("Websocket disconnected...", close_code)





