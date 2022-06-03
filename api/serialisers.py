from rest_framework import serializers
from user_profile.models import User
from social.models import Tag, Question, Answer, Comment, Votes


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model: Tag
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model: Question
        fields = '__all__'







