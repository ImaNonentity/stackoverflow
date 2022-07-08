from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

from .models import User


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=50, required=False)
    profile_photo = serializers.ImageField(required=False)
    birth_date = serializers.DateField(required=False)
    first_name = serializers.CharField(max_length=25, required=False)
    last_name = serializers.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'profile_photo', 'last_login', 'birth_date',
                  'first_name', 'last_name', 'role', 'rating', 'questions', 'answers']
        depth = 1


class UserAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['profile_photo', ]

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
