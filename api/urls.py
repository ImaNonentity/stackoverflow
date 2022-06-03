from django.urls import path

from api import views

urlpatterns = [
    path('api/', views.api_detail_user_view, name='api_view'),
    path('api/overview/', views.api_overview, name="api-overview"),
    path('question-list/', views.question_list, name="question-list"),
    path('question-detail/<str:pk>/', views.question_detail, name="question-detail"),
    path('question-create/', views.question_create, name="question-create"),

    path('question-update/<str:pk>/', views.question_update, name="question-update"),
    path('question-delete/<str:pk>/', views.question_delete, name="question-delete"),

    path('user_profile-profile/<str:pk>', views.api_detail_user_view, name='detail')
]
