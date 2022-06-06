from django.urls import path

from .views import (
    detail_question_view,
    update_question_view,
    delete_question_view,
    create_question_view,

)
urlpatterns = [
    # QUESTION VIEWS
    path('question/<id>/', detail_question_view, name="question_detail"),
    path('question/<id>/update', update_question_view, name="question_update"),
    path('question/<id>/delete', delete_question_view, name="question_delete"),
    path('question/new', create_question_view, name="question_new"),


    ]
