from rest_framework import serializers

from .models import Room, Message
from user_profile.serializers import SimpleUserSerializer


class OutputMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['user']


class InputMessageSerializer(serializers.ModelSerializer):
    media_path = serializers.CharField(required=False)
    room = serializers.CharField(required=False)

    class Meta:
        model = Message
        fields = '__all__'


