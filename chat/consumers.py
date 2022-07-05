import os
import django
import json
from channels.generic.websocket import WebsocketConsumer
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework import mixins
from user_profile.models import User
from user_profile.serializers import SimpleUserSerializer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text):
        text_data_json = json.loads(text)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))


class UserConsumer(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.PatchModelMixin,
        mixins.UpdateModelMixin,
        mixins.CreateModelMixin,
        mixins.DeleteModelMixin,
        GenericAsyncAPIConsumer,
):

    queryset = User.objects.all()
    serializer_class = SimpleUserSerializer




