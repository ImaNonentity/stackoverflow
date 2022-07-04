import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework import mixins
from djangochannelsrestframework.observer.generics import (ObserverModelInstanceMixin, action)
from djangochannelsrestframework.observer import model_observer

from .models import Room, Message
from user_profile.models import User
# from .serializers import RoomSerializer
from .serializers import MessageSerializer
from user_profile.serializers import SimpleUserSerializer


# class RoomConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer
#     lookup_field = "pk"
#
#     @action()
#     async def join_room(self, pk, **kwargs):
#         self.room_subscribe = pk
#         self.add_user_to_room(pk)
#         self.notify_users()
#
#
#     def add_user_to_room(self, pk):
#         user: User = self.scope["user"]
        # if not user.current_rooms.filter(pk=self.room_subscribe).exists():
        #     user.current_rooms.add(Room.objects.get(pk=pk))





