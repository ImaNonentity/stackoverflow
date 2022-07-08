from abc import ABC

from rest_framework import serializers

from .models import Room, Message
from user_profile.serializers import SimpleUserSerializer


class CustomMessageSerializer(serializers.Serializer):
    sender_id = serializers.IntegerField()
    text = serializers.CharField(max_length=5000)
    room = serializers.IntegerField()
    receiver_id = serializers.IntegerField()


class OutputMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender_id', 'text', 'created_at', 'room']
        # depth = 1


class InputMessageSerializer(serializers.ModelSerializer):
    media_path = serializers.CharField(required=False)
    room = serializers.CharField(required=False)

    class Meta:
        model = Message
        fields = '__all__'


