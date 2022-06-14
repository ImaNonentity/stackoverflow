from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

from .models import User


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'id']


class UserSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'profile_photo', 'last_login', 'birth_date', 'role', 'rating']


class UserAvatarSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['profile_photo', ]

    def save(self, *args, **kwargs):
        if self.instance.profile_photo:
            self.instance.profile_photo.delete()
        return super().save(*args, **kwargs)

    # MY CUSTOM HANDMADE REGISTRATION 8)

# class RegisterSerializer(serializers.ModelSerializer):
#
#     password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
#
#     class Meta:
#         model = User
#         fields = ['email', 'username', 'password', 'password2']
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def save(self):
#         user = User(
#             email=self.validated_data['email'],
#             username=self.validated_data['username'],
#         )
#         password = self.validated_data['password']
#         password2 = self.validated_data['password2']
#         if password != password2:
#             raise serializers.ValidationError({'password': 'Passwords must match.'})
#         user.set_password(password)
#         user.save()
#         return user


