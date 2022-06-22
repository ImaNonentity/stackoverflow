from django.urls import path
from .views import VoteAddView, VoteListView, VoteUserView
urlpatterns = [
    path('vote/add', VoteAddView.as_view(), name='VoteAddView_vote'),
    path('vote/list', VoteListView.as_view(), name='votes_list'),
    path('vote/<int:pk>/list/', VoteUserView.as_view(), name='votes_list_by_user'),
]