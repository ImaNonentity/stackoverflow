from django.urls import path
# from rest_framework_swagger.views import get_swagger_view
#
# schema_view = get_swagger_view(title='Pastebin API')

from .views import (
    QuestionVoteView,
    QuestionByUserListView,
    QuestionsListView,
    QuestionView,
    QuestionCreateView,
    QuestionUpdateView,
    QuestionDeleteView,
    AnswerByUserView,
    AnswerUpdateView,
    AnswerDeleteView,
    AnswerCreateView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    CreateTagView,
    GetTagInfoView,
    GetTagView,
    DeleteTagView,
    GetSingleTagInfoView,

)
urlpatterns = [
    # path('uii', schema_view),
    # QUESTION URLS
    path('questions/<int:pk>/', QuestionByUserListView.as_view(), name="questions_list_by_id"),
    path('questions/all/', QuestionsListView.as_view(), name="questions_list"),
    path('question/<int:pk>/', QuestionView.as_view(), name="question_detail"),
    path('question/new', QuestionCreateView.as_view(), name="question_new"),
    path('question/<id>/update', QuestionUpdateView.as_view(), name="question_update"),
    path('question/<id>/delete', QuestionDeleteView.as_view(), name="question_delete"),
    path('questions/tagged/<id>/', GetTagView.as_view(), name="questions-by-tag"),
    path('question/<id>/vote/', QuestionVoteView.as_view(), name='question_vote'),


    # ANSWER URLS
    path('answer/<id>/', AnswerByUserView.as_view(), name="answer_detail"),
    path('answer/<id>/update', AnswerUpdateView.as_view(), name="answer_update"),
    path('answer/<id>/delete', AnswerDeleteView.as_view(), name="answer_delete"),
    path('answer/new', AnswerCreateView.as_view(), name="answer_create"),

    # COMMENT URLS
    path('comment/<id>/update', CommentUpdateView.as_view(), name="comment_update"),
    path('comment/<id>/delete', CommentDeleteView.as_view(), name="comment_delete"),
    path('comment/new', CommentCreateView.as_view(), name="comment_create"),

    # TAG URLS
    path('tag/new', CreateTagView.as_view(), name="create_tag"),
    path('tag/list', GetTagInfoView.as_view(), name="tag_list"),
    path('tag/<slug:slug>', GetSingleTagInfoView.as_view(), name="tag_info"),
    path('tag/<slug:slug>/delete', DeleteTagView.as_view(), name='delete_tag')
    ]
