from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from user_profile.models import User
from .models import Question, Answer, Comment, Tag
from .serializers import (
    QuestionSerializer,
    UpdateQuestionSerializer,
    CreateQuestionSerializer,
    AnswerSerializer,
    AnswerDetailSerializer,
)


class QuestionByUserListView(APIView):

    """ List of Questions by user id """

    def get(self, request, pk):
        question = Question.objects.filter(user__pk=self.request.user.id)
        serializer = QuestionSerializer(question, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionsListView(APIView):

    """ List of all Questions """

    def get(self, request):
        question = Question.objects.all()
        serializer = QuestionSerializer(question, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionView(APIView):

    """ Single Question details """

    def get(self, request, pk):
        try:
            question = Question.objects.get(id=pk)
            serializer = QuestionSerializer(question)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionCreateView(APIView):

    """ Create new Question """

    def post(self, request):
        serializer = CreateQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class QuestionUpdateView(APIView):
#
#     """ Update Question """
#

# QUESTION VIEW
# @api_view(['GET'])
# @permission_classes((IsAuthenticatedOrReadOnly,))
# def detail_question_view(request, id):
#     try:
#         question = Question.objects.get(id=id)
#     except Question.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "GET":
#         serializer = QuestionSerializer(question)
#         return Response(serializer.data)


# @api_view(['PUT'])
# @permission_classes((IsAuthenticated,))
# def update_question_view(request, id):
#     try:
#         question = Question.objects.get(id=id)
#     except Question.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     user = request.user
#     if question.username != user:
#         return Response({'response': "You don't have permission to update that"})
#
#     if request.method == "PUT":
#         serializer = UpdateQuestionSerializer(question, data=request.data)
#         data = {}
#         if serializer.is_valid():
#             serializer.save()
#             data["success"] = "update successful"
#             return Response(data=data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['DELETE'])
# @permission_classes((IsAuthenticated,))
# def delete_question_view(request, id):
#     try:
#         question = Question.objects.get(id=id)
#     except Question.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     user = request.user
#     if question.username != user:
#         return Response({'response': "You don't have permission to delete that."})
#
#     if request.method == "DELETE":
#         operation = question.delete()
#         data = {}
#         if operation:
#             data["success"] = "delete successful"
#         else:
#             data["failure"] = "delete failed"
#         return Response(data=data)
#
#
# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# def create_question_view(request):
#
#     user = request.user
#
#     question = Question(username=user)
#
#     if request.method == "POST":
#         serializer = CreateQuestionSerializer(question, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# ANSWER VIEW
# @api_view(['GET'])
# @permission_classes((IsAuthenticatedOrReadOnly,))
# def detail_answer_view(request, id):
#     try:
#         answer = Answer.objects.get(id=id)
#     except Answer.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "GET":
#         serializer = AnswerDetailSerializer(answer)
#         return Response(serializer.data)
#
#
# @api_view(['PUT'])
# @permission_classes((IsAuthenticated,))
# def update_answer_view(request, id):
#     try:
#         answer = Answer.objects.get(id=id)
#     except Answer.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     user = request.user
#     if answer.username != user:
#         return Response({'response': "You don't have permission to update that!"})
#
#     if request.method == "PUT":
#         serializer = AnswerSerializer(answer, data=request.data)
#         data = {}
#         if serializer.is_valid():
#             serializer.save()
#             data['success'] = "update successful"
#             return Response(data=data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['DELETE'])
# @permission_classes((IsAuthenticated,))
# def delete_answer_view(request, id):
#     try:
#         answer = Answer.objects.get(id=id)
#     except Answer.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     user = request.user
#     if answer.usermane != user:
#         return Response({'response': "You don't have permission to delete that."})
#
#     if request.method == "DELETE":
#         operation = answer.delete()
#         data = {}
#         if operation:
#             data["success"] = "delete successful"
#         else:
#             data["failure"] = "delete failed"
#         return Response(data=data)
#
#
# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# def create_answer_view(request):
#
#     user = request.user
#
#     answer = Answer(username=user)
#
#     if request.method == "POST":
#         serializer = QuestionSerializer(answer, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)