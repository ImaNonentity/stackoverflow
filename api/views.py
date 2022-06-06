# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
#
# from user_profile.models import User
# from social.models import Question, Answer, Comment, Tag
# from djangoProject.api.serializers import QuestionSerializer
# from djangoProject.user_profile.serializers import UserSerializer
#
#
# # USER VIEW
#
# @api_view(['GET'])
# def api_detail_user_view(request, pk):
#     try:
#         user = User.objects.get(id=pk)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "GET":
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
#
#
# @api_view(['PUT'])
# def api_update_user_view(request, id):
#     try:
#         user = User.objects.get(id=id)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "PUT":
#         serializer = UserSerializer(user, data=request.data)
#         data = {}
#         if serializer.is_valid():
#             serializer.save()
#             data["success"] = "update successful"
#             return Response(data=data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['DELETE'])
# def api_delete_user_view(request, id):
#     try:
#         user = User.objects.get(id=id)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "DELETE":
#         operation = user.delete()
#         data = {}
#         if operation:
#             data["success"] = "delete successful"
#         else:
#             data["failure"] = "delete failed"
#         return Response(data=data)
#
#
# # QUESTION VIEWS
#
# @api_view(['GET'])
# def api_detail_question_view(request, id):
#     try:
#         question = Question.objects.get(id=id)
#     except Question.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "GET":
#         serializer = QuestionSerializer(question)
#         return Response(serializer.data)
#
#
# @api_view(['PUT'])
# def api_update_question_view(request, id):
#     try:
#         question = Question.objects.get(id=id)
#     except Question.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "PUT":
#         serializer = QuestionSerializer(question, data=request.data)
#         data = {}
#         if serializer.is_valid():
#             serializer.save()
#             data["success"] = "update successful"
#             return Response(data=data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['DELETE'])
# def api_delete_question_view(request, id):
#     try:
#         question = Question.objects.get(id=id)
#     except Question.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
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
# def api_create_question_view(request, id):
#
#     account = User.objects.get(id=id)
#
#     question = Question(username=account)
#
#     if request.method == "POST":
#         serializer = QuestionSerializer(question, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
#
#
#
#
#
#
#
#
#
#
#
#
# # @api_view(['GET'])
# # def api_overview(request):
# #     api_urls = {
# #         'List': '/question-list/',
# #         'Detail View': '/question-detail/<str:pk>/',
# #         'Create': '/question-create/',
# #         'Update': '/question-update/<str:pk>/',
# #         'Delete': '/question-delete/<str:pk>/',
# #     }
# #     return Response(api_urls)
# #
# #
# # @api_view(['GET'])
# # def question_list(request):
# #     question = Question.objects.all().order_by('-id')
# #     serializer = QuestionSerializer(question, many=True)
# #     return Response(serializer.data)
# #
# #
# # @api_view(['GET'])
# # def question_detail(request, pk):
# #     question = Question.objects.get(id=pk)
# #     serializer = QuestionSerializer(question, many=False)
# #     return Response(serializer.data)
# #
# #
# # @api_view(['POST'])
# # def question_create(request):
# #     serializer = QuestionSerializer(data=request.data)
# #
# #     if serializer.is_valid():
# #         serializer.save()
# #
# #     return Response(serializer.data)
# #
# #
# # @api_view(['POST'])
# # def question_update(request, pk):
# #     question = Question.objects.get(id=pk)
# #     serializer = QuestionSerializer(instance=question, data=request.data)
# #
# #     if serializer.is_valid():
# #         serializer.save()
# #
# #     return Response(serializer.data)
# #
# #
# # @api_view(['DELETE'])
# # def question_delete(request, pk):
# #     question = Question.objects.get(id=pk)
# #     question.delete()
# #
# #     return Response('Item succsesfully delete!')
#
#
#
#
# # class UserList(generics.ListCreateAPIView):
# #     queryset = User.objects.all()
# #     serializer_class = UserSerializer
# #     permission_classes = [IsAdminUser]
