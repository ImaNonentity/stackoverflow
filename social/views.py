from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from user_profile.models import User
from .models import Question, Answer, Comment, Tag
from .serializers import QuestionSerializer



@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def detail_question_view(request, id):
    try:
        question = Question.objects.get(id=id)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = QuestionSerializer(question)
        return Response(serializer.data)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def update_question_view(request, id):
    try:
        question = Question.objects.get(id=id)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if question.username != user:
        return Response({'response': "You don't have permission to update that"})

    if request.method == "PUT":
        serializer = QuestionSerializer(question, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_question_view(request, id):
    try:
        question = Question.objects.get(id=id)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if question.username != user:
        return Response({'response': "You don't have permission to delete that."})

    if request.method == "DELETE":
        operation = question.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_question_view(request):

    user = request.user

    question = Question(username=user)

    if request.method == "POST":
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

