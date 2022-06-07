from rest_framework import serializers
from user_profile.models import User
from .models import Tag, Question, Answer, Comment, Votes
from user_profile.serializers import UserSerializer


MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50


# Тэги надо доделать. Мэни-ту-мэни.
class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


# QUESTION SERIALIZERS
class QuestionSerializer(serializers.ModelSerializer):

    username = UserSerializer()
    tag = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ['id', 'username', 'title', 'content', 'created_at', 'updated_at', 'tag']

    # def get_username_from_author(self, question):
    #     username = question.user.username
    #     return username

    # def get_tags_name(self, question):
    #     tags = question.tags.title
    #     return tags


class UpdateQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['title', 'content']

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

    user = serializers.CharField(required=False)
    # username = serializers.SerializerMethodField('get_username_from_user')

    class Meta:
        model = Question
        fields = ['user', 'title', 'content']

    # def get_username_from_user(self, question):
    #     username = question.user.username
    #     return username

    def to_representation(self, user):
        return user.username


# class CreateQuestionSerializer(serializers.ModelSerializer):
#
#     # tag = TagSerializer(read_only=True, many=True)
#     username = serializers.SerializerMethodField('get_username_from_author')
#
#     class Meta:
#         model = Question
#         fields = ['id', 'username', 'title', 'content']
#
#     def get_username_from_author(self, question):
#         username = question.user.username
#         return username

    # def save(self):
    #     try:
    #         title = self.validated_data['title']
    #         if len(title) < MIN_TITLE_LENGTH:
    #             raise serializers.ValidationError(
    #                 {"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})
    #
    #         content = self.validated_data['content']
    #         if len(content) < MIN_BODY_LENGTH:
    #             raise serializers.ValidationError(
    #                 {"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})
    #         question = Question(
    #             id=id,
    #             user=self.validated_data['username'],
    #             title=title,
    #             content=content,
    #         )
    #         question.save()
    #         return question
    #     except KeyError:
    #         pass
            # raise serializers.ValidationError({"response": "You must have a title and content."})


# ANSWER SERIALIZERS
class AnswerDetailSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username_from_author')
    question = serializers.SerializerMethodField('get_question_id')

    class Meta:
        model = Answer
        fields = ['id', 'username', 'question', 'content', 'created_at', 'updated_at']


    def get_username_from_author(self, answer):
        username = answer.user.username
        return username

    def get_question_id(self, answer):
        question = answer.question.id
        return question


class UpdateAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['content']

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

    question = serializers.SerializerMethodField('get_question_id')

    class Meta:
        model = Answer
        fields = ['id', 'username', 'question', 'content', 'created_at', 'updated_at']

    def get_question_id(self, answer):
        question = answer.question.id
        return question

    def save(self, answer):
        try:
            content = answer['content']
            if len(content) < MIN_BODY_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a body longer than" + str(MIN_BODY_LENGTH) + " characters."}
                )
            answer = Answer(
                id=id,
                username=self.validated_data['username'],
                question=self.validated_data['question'],
                content=content,
        )
            answer.save()
            return answer

        except KeyError:
            pass







class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
