from django.urls import path

from api import views

urlpatterns = [
    # USER VIEWS
    path('api/user/<pk>/', views.api_detail_user_view, name="user_detail"),
    path('api/user/<pk>/update', views.api_update_user_view, name="user_update"),
    path('api/user/<pk>/delete', views.api_delete_user_view, name="user_delete"),

    # QUESTION VIEWS
    path('api/question/<pk>/', views.api_detail_question_view, name="question_detail"),
    path('api/question/<pk>/update', views.api_update_question_view, name="question_update"),
    path('api/question/<pk>/delete', views.api_delete_question_view, name="question_delete"),
    path('api/question/new', views.api_create_question_view, name="question_new"),


    # path('api/overview/', views.api_overview, name="api-overview"),
    # path('question-list/', views.question_list, name="question-list"),
    # path('question-detail/<str:pk>/', views.question_detail, name="question-detail"),
    # path('question-create/', views.question_create, name="question-create"),
    # path('question-update/<str:pk>/', views.question_update, name="question-update"),
    # path('question-delete/<str:pk>/', views.question_delete, name="question-delete"),

    # path('user_profile-profile/<str:pk>', views.api_detail_user_view, name='detail')
]
