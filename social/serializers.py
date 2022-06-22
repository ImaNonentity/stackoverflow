from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from user_profile.models import User
from .models import Tag, Question, Answer, Comment, Vote

from user_profile.serializers import UserSerializer, SimpleUserSerializer
from rest_framework.fields import CurrentUserDefault, IntegerField

MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50

CONTENT_TYPES_MODEL = ['question', 'answer']


# COMMENT SERIALIZERS

class CommentSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(queryset=ContentType.objects.filter(model__in=CONTENT_TYPES_MODEL),
                                                slug_field='model')
    object_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, attrs):
        try:
            attrs['content_object'] = attrs['content_type'].model_class().objects.get(pk=attrs['object_id'])
        except:
            raise serializers.ValidationError(
                {'object_id': ['Invalid pk "' + str(attrs['object_id']) + '" - object does not exist.']})
        return attrs


# TAG SERIALIZERS

class SimpleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


# QUESTION SERIALIZERS

class SimpleQuestionSerializer(serializers.ModelSerializer):
    tag = SimpleTagSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ['title', 'content', 'tag', 'user', 'vote_count']


class CreateQuestionSerializer(serializers.ModelSerializer):

    tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), write_only=True, many=True)

    class Meta:
        model = Question
        fields = ['title', 'content', 'tag', 'user']

    def create(self, validated_data):
        tags = validated_data.pop('tag')
        question = Question.objects.create(**validated_data)
        for tag in tags:
            question.tag.add(tag)
        return question


# ANSWER SERIALIZERS

class AnswerDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['id', 'user', 'question', 'content', 'created_at', 'updated_at', 'vote_count']


class UpdateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['user', 'content']


class CreateAnswerSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=False)

    class Meta:
        model = Answer
        fields = ['user', 'content', 'question']
