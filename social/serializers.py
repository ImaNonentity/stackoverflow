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
        # prepopulated_fields = {'slug': ('title',)}
        # lookup_field = 'slug'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'slug'}
        # }


# QUESTION SERIALIZERS

class SimpleQuestionSerializer(serializers.ModelSerializer):
    tag = SimpleTagSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at', 'tag']

    # def get_tags_name(self, question):
    #     tags = question.tags.title
    #     return tags


class QuestionSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)
    upvote = serializers.IntegerField(source='upvote.count')
    downvote = serializers.IntegerField(source='downvote.count')

    class Meta:
        model = Question
        fields = ['user', 'title', 'content', 'tag', 'upvote', 'downvote']

    def validate(self, question):
        try:
            title = question['title']
            if len(title) < MIN_TITLE_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})

            content = question['content']
            if len(content) < MIN_BODY_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})
        except KeyError:
            raise serializers.ValidationError({"response": "You must have a title and content."})
        return question

    # def get_user_vote(self, obj):
    #     try:
    #         user = self.context['request'].user
    #     except KeyError:
    #         return 0
    #     if user in obj.upvote.all():
    #         return 1
    #     if user in obj.downvote.all():
    #         return -1
    #     return 0


# ANSWER SERIALIZERS

class AnswerDetailSerializer(serializers.ModelSerializer):
    upvote = serializers.IntegerField(source='upvote.count')
    downvote = serializers.IntegerField(source='downvote.count')

    class Meta:
        model = Answer
        fields = ['id', 'user', 'question', 'content', 'created_at', 'updated_at', 'upvote', 'downvote']

    # def get_user_vote(self, obj):
    #     try:
    #         user = self.context['request'].user
    #     except KeyError:
    #         return 0
    #     if user in obj.upvote.all():
    #         return 1
    #     if user in obj.downvote.all():
    #         return -1
    #     return 0


class UpdateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['user', 'content']

    def validate(self, answer):
        try:
            content = answer['content']
            if len(content) < MIN_BODY_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})
        except KeyError:
            pass
        return answer


class CreateAnswerSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=False)

    class Meta:
        model = Answer
        fields = ['user', 'content', 'question']

    # def save(self, answer):
    #     try:
    #         content = answer['content']
    #         if len(content) < MIN_BODY_LENGTH:
    #             raise serializers.ValidationError(
    #                 {"response": "Enter a body longer than" + str(MIN_BODY_LENGTH) + " characters."}
    #             )
    #     except KeyError:
    #         pass
    #     answer = Answer(
    #         id=id,
    #         usere=self.validated_data['user'],
    #         question=self.validated_data['question'],
    #         content=content,
    #     )
    #     answer.save()
    #     return answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
