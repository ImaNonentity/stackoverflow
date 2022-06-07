from django.urls import path

from .views import (
    QuestionByUserListView,
    QuestionsListView,
    QuestionView,
    QuestionCreateView,
#     update_question_view,
#     delete_question_view,
#     create_question_view,
#     detail_answer_view,
#     update_answer_view,
#     delete_answer_view,
#     create_answer_view,
)
urlpatterns = [
    # QUESTION VIEWS
    path('questions/<int:pk>/', QuestionByUserListView.as_view(), name="questions_list_by_id"),
    path('questions/all/', QuestionsListView.as_view(), name="questions_list"),
    path('question/<int:pk>/', QuestionView.as_view(), name="question_detail"),
    path('question/new', QuestionCreateView.as_view(), name="question_new"),
    # path('question/<id>/update', update_question_view, name="question_update"),
    # path('question/<id>/delete', delete_question_view, name="question_delete"),

    # ANSWER VIEWS
    # path('answer/<id>/', detail_answer_view, name="answer_detail"),
    # path('answer/<id>/update', update_answer_view, name="answer_update"),
    # path('answer/<id>/delete', delete_answer_view, name="answer_delete"),
    # path('answer/new', create_answer_view, name="answer_create"),

    ]
