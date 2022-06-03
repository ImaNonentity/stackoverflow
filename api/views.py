from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from user_profile.models import User
from social.models import Question, Answer, Comment, Tag
from api.serialisers import UserSerializer, QuestionSerializer


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'List': '/question-list/',
        'Detail View': '/question-detail/<str:pk>/',
        'Create': '/question-create/',
        'Update': '/question-update/<str:pk>/',
        'Delete': '/question-delete/<str:pk>/',
    }
    return Response(api_urls)


@api_view(['GET'])
def question_list(request):
    question = Question.objects.all().order_by('-id')
    serializer = QuestionSerializer(question, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def question_detail(request, pk):
    question = Question.objects.get(id=pk)
    serializer = QuestionSerializer(question, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def question_create(request):
    serializer = QuestionSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def question_update(request, pk):
    question = Question.objects.get(id=pk)
    serializer = QuestionSerializer(instance=question, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def question_delete(request, pk):
    question = Question.objects.get(id=pk)
    question.delete()

    return Response('Item succsesfully delete!')



@api_view(['GET',])
def api_detail_user_view(request):

	try:
		user = User.objects.get(id=pk)
	except User.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "GET":
		serializer = UserSerializer(user)
		return Response(serializer.data)






# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAdminUser]
