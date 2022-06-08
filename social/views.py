from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from user_profile.permissions import IsOwnerUser, ReadOnly
from user_profile.models import User
from .models import Question, Answer, Comment, Tag
from .serializers import (
    QuestionSerializer,
    UpdateQuestionSerializer,
    CreateQuestionSerializer,
    AnswerSerializer,
    AnswerDetailSerializer,
    CreateAnswerSerializer,
    UpdateAnswerSerializer,
    CommentSerializer,

)


# QUESTION VIEWS

class QuestionByUserListView(APIView):
    """ List of Questions by user id """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & ReadOnly]

    @swagger_auto_schema(responses={50: QuestionSerializer(many=True)})
    def get(self, request, pk):
        question = Question.objects.filter(user__pk=self.request.user.id)
        serializer = QuestionSerializer(question, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionsListView(APIView):
    """ List of all Questions """

    authentication_classes = [TokenAuthentication]
    permission_classes = [ReadOnly]

    @swagger_auto_schema(responses={50: QuestionSerializer(many=True)})
    def get(self, request):
        question = Question.objects.all()
        serializer = QuestionSerializer(question, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionView(APIView):
    """ Single Question details """

    authentication_classes = [TokenAuthentication]
    permission_classes = [ReadOnly]

    def get(self, request, pk):
        try:
            question = Question.objects.get(id=pk)
            serializer = QuestionSerializer(question)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionCreateView(APIView):
    """ Create new Question """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={50: QuestionSerializer(many=True)})
    def post(self, request):
        question = request.data

        new_question = Question.objects.create(title=question['title'], content=question['content'])
        new_question.save()

        serializer = CreateQuestionSerializer(new_question)
        # if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionUpdateView(APIView):
    """ Update Question """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerUser|IsAdminUser]

    def put(self, request, pk):
        question = Question.objects.get(id=pk)
        serializer = UpdateQuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDeleteView(APIView):
    """ Delete Question """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerUser|IsAdminUser]

    def delete(self, request, pk):
        question = Question.objects.get(id=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ANSWER VIEWS

class AnswerByUserView(APIView):
    """ List of Answers by user id """

    authentication_classes = []
    permission_classes = [ReadOnly]

    def get(self, request, pk):
        answer = Answer.objects.get(user__pk=self.request.user.id)
        serializer = AnswerDetailSerializer(answer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerCreateView(APIView):
    """ Create new Answer """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateAnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerUpdateView(APIView):
    """ Update Answer """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerUser|IsAdminUser]

    def put(self, request, pk):
        answer = Answer.objects.get(id=pk)
        serializer = UpdateAnswerSerializer(answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerDeleteView(APIView):
    """ Delete Answer """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerUser|IsAdminUser]

    def delete(self, request, pk):
        answer = Answer.objects.get(id=pk)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# COMMENT VIEWS

class CommentCreateView(APIView):
    """ Create new Comment """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentUpdateView(APIView):
    """ Update Comment """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerUser|IsAdminUser]

    def put(self, request, pk):
        comment = Comment.objects.get(id=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDeleteView(APIView):
    """ Delete Comment """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerUser|IsAdminUser]

    def delete(self, request, pk):
        comment = Comment.objects.get(id=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






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