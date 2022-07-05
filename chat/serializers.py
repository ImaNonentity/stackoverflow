from rest_framework import serializers

from .models import Room, Message
from user_profile.serializers import SimpleUserSerializer


class OutputMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['user']


class MessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = SimpleUserSerializer()

    class Meta:
        model = Message
        fields = '__all__'
        # depth = 1

    def get_created_at_formatted(self, obj: Message):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")


class RoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'
        extra_fields = ['messages']
        depth = 1

