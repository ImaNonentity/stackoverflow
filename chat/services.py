from datetime import datetime
from django.db.models import Q
from .models import Message, Room


class CreateMessageService:

    def __init__(
            self,
            sender_id: int,
            receiver_id: int,
            created_at: datetime,
            text: str = None,
            media_path: str = None,
            content_type: str = None
    ):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.created_at = created_at
        self.text = text
        self.media_path = media_path
        self.content_type = content_type

    def get_or_create_room(self) -> Room:
        filters = (
                Q(sender_id=self.sender_id, receiver_id=self.receiver_id) |
                Q(sender_id=self.receiver_id, receiver_id=self.sender_id)
        )
        room = Room.objects.filter(*filters)
        if not room:
            room = Room(
                receiver_id=self.receiver_id,
                sender_id=self.sender_id
            )
            room.save()
        else:
            room = room.first()
        return room

    def create_message(self) -> Message:
        room = self.get_or_create_room()
        message = Message(
            text=self.text,
            media_path=self.media_path,
            created_at=self.created_at,
            sender_id=self.sender_id,
            room=room
        )
        message.save()
        return message

    def execute(self) -> Message:
        message = self.create_message()
        return message


class GetMessageService:

    def __init__(
            self,
            user_id: int,
    ):
        self.user_id = user_id

    def get_user_rooms(self) -> Room | list:
        filters = Q(sender_id=self.user_id) | Q(receiver_id=self.user_id)
        rooms = Room.objects.filter(filters).all()
        if not rooms:
            return list()
        return rooms

    def get_last_messages(self) -> dict:
        """ This method is responsible for rooms list UI response data """
        rooms = self.get_user_rooms()
        response = dict()
        for room in rooms:
            messages = Message.objects.filter(room=room).order_by("created_at").last()
            print(room.pk)
            response.update(**{str(room.pk): messages})
        return response

    def get_room_messages(self, room: Room):
        messages = Message.objects.filter(room=room).order_by("-created_at").all()
        return messages
