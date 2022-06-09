from rest_framework import serializers
from user_profile.models import User
from .models import Tag, Question, Answer, Comment, Vote
from user_profile.serializers import UserSerializer, SimpleUserSerializer
from rest_framework.fields import CurrentUserDefault

MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50


# COMMENT SERIALIZERS

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


# TAG SERIALIZERS

class SimpleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        prepopulated_fields = {'slug': ('title',)}
        # lookup_field = 'slug'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'slug'}
        # }


# QUESTION SERIALIZERS

class SimpleQuestionSerializer(serializers.ModelSerializer):
    answer = serializers.StringRelatedField(many=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'answer']


class QuestionSerializer(serializers.ModelSerializer):
    tag = SimpleTagSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at', 'tag']

    # def get_tags_name(self, question):
    #     tags = question.tags.title
    #     return tags


class UpdateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['user', 'title', 'content']

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


class CreateQuestionSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=False)

    class Meta:
        model = Question
        fields = ['user', 'title', 'content']


# ANSWER SERIALIZERS

class AnswerDetailSerializer(serializers.ModelSerializer):
    # question = serializers.SerializerMethodField('get_question_id')

    class Meta:
        model = Answer
        fields = ['id', 'user', 'question', 'content', 'created_at', 'updated_at']


    # def get_question_id(self, answer):
    #     question = answer.question.id
    #     return question


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





