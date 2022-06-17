from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.fields import CurrentUserDefault
from user_profile.permissions import IsOwnerUser, ReadOnly
from user_profile.models import User
from vote.services import RatingCountSystem
from .models import Question, Answer, Comment, Tag
from .serializers import (
    CreateQuestionSerializer,
    QuestionSerializer,
    SimpleQuestionSerializer,
    AnswerSerializer,
    AnswerDetailSerializer,
    CreateAnswerSerializer,
    UpdateAnswerSerializer,
    CommentSerializer,
    TagSerializer,

)


# QUESTION VIEWS

class QuestionByUserListView(APIView):
    """ List of Questions by user id """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & ReadOnly]

    @swagger_auto_schema(responses={50: QuestionSerializer(many=True)})
    def get(self, request, pk):
        question = Question.objects.filter(user__pk=self.request.user.id)
        serializer = SimpleQuestionSerializer(question, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionsListView(APIView):
    """ List of all Questions """

    authentication_classes = [TokenAuthentication]
    permission_classes = [ReadOnly]

    @swagger_auto_schema(responses={50: QuestionSerializer(many=True)})
    def get(self, request):
        question = Question.objects.all()
        serializer = SimpleQuestionSerializer(question, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionView(APIView):
    """ Single Question details """

    authentication_classes = [TokenAuthentication]
    permission_classes = [ReadOnly]

    def get(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
            serializer = SimpleQuestionSerializer(question)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionCreateView(APIView):
    """ Create new Question """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='title'),
            'content': openapi.Schema(type=openapi.TYPE_STRING, description='content'),
            'tag': openapi.Schema(type=openapi.TYPE_STRING, description='list'),
        }
    ))
    def post(self, request):
        serializer = CreateQuestionSerializer(data=request.data)
        rating_system = RatingCountSystem(user=request.user, data=request.data)
        rating_system.validate_user()
        rating_system.check_rank()
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionUpdateView(APIView):
    """ Update Question """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerUser | IsAdminUser]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='title'),
            'content': openapi.Schema(type=openapi.TYPE_STRING, description='content'),
            'tag': openapi.Schema(type=openapi.TYPE_STRING, description='list'),
        }
    ))
    def put(self, request, id):
        question = Question.objects.get(id=id, user=request.user)
        serializer = CreateQuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TEST VIEW
class QuestionVoteView(APIView):

    def post(self, request, id):
        question = Question.objects.get(id=id, user=request.user)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDeleteView(APIView):
    """ Delete Question """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerUser | IsAdminUser]

    def delete(self, request, id):
        question = Question.objects.get(id=id)
        operation = question.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)


# ANSWER VIEWS

class AnswerByUserView(APIView):
    """ List of Answers by user id """

    authentication_classes = []
    permission_classes = [ReadOnly]

    @swagger_auto_schema(responses={50: QuestionSerializer(many=True)})
    def get(self, request, id):
        user = User.objects.get(id=id)
        answer = Answer.objects.filter(user=user)
        serializer = AnswerDetailSerializer(answer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerCreateView(APIView):
    """ Create new Answer """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'content': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                    'question': openapi.Schema(type=openapi.TYPE_STRING, description='id')}
    ))
    def post(self, request):
        user = User.objects.get(pk=request.user.id)
        serializer = CreateAnswerSerializer(data=request.data)
        rating_system = RatingCountSystem(user=request.user, data=request.data)
        rating_system.check_rank()
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerUpdateView(APIView):
    """ Update Answer """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerUser | IsAdminUser]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'content': openapi.Schema(type=openapi.TYPE_STRING, description='string')}
    ))
    def put(self, request, id):
        user = User.objects.get(pk=request.user.id)
        answer = Answer.objects.get(id=id)
        serializer = UpdateAnswerSerializer(answer, data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerDeleteView(APIView):
    """ Delete Answer """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerUser | IsAdminUser]

    def delete(self, request, id):
        answer = Answer.objects.get(id=id)
        operation = answer.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)


# COMMENT VIEWS

class CommentCreateView(APIView):
    """ Create new Comment """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'content': openapi.Schema(type=openapi.TYPE_STRING, description='content'),
                    'content_type': openapi.Schema(type=openapi.TYPE_STRING, description='content_type'),
                    'object_id': openapi.Schema(type=openapi.TYPE_STRING, description='object_id')}
    ))
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        rating_system = RatingCountSystem(user=request.user, data=request.data)
        rating_system.check_rank()
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentUpdateView(APIView):
    """ Update Comment """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerUser | IsAdminUser]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'content': openapi.Schema(type=openapi.TYPE_STRING, description='content'),
                    'content_type': openapi.Schema(type=openapi.TYPE_STRING, description='content_type'),
                    'object_id': openapi.Schema(type=openapi.TYPE_STRING, description='object_id')}
    ))
    def put(self, request, id):
        # user = User.objects.get(id=request.user.id)
        comment = Comment.objects.get(id=id)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDeleteView(APIView):
    """ Delete Comment """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerUser | IsAdminUser]

    def delete(self, request, id):
        comment = Comment.objects.get(id=id)
        operation = comment.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)


# TAG VIEWS

class CreateTagView(APIView):
    """ Create Tag """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'title': openapi.Schema(type=openapi.TYPE_STRING, description='title'),
                    'content': openapi.Schema(type=openapi.TYPE_STRING, description='content')}
    ))
    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTagInfoView(APIView):
    """ Get all Tags """

    authentication_classes = []
    permission_classes = [ReadOnly]

    def get(self, request):
        tag = Tag.objects.all()
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetSingleTagInfoView(APIView):
    """ Get single Tag """

    authentication_classes = []
    permission_classes = [ReadOnly]

    def get(self, request, id):
        tag = Tag.objects.get(id=id)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteTagView(APIView):
    """ Delete Tag """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def delete(self, request, id):
        tag = Tag.objects.get(id=id)
        operation = tag.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)


class GetTagView(APIView):
    """ Get all Questions by Tag """

    authentication_classes = []
    permission_classes = [ReadOnly]

    def get(self, request, id):
        tag = Tag.objects.filter(id=id)
        question = Question.objects.filter(tag=tag)
        serializer = QuestionSerializer(tag, question)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
