from django.urls import path
from .views import VoteCreateView, VoteListView

urlpatterns = [
    path('vote/create', VoteCreateView.as_view(), name='create_vote'),
    path('vote/list', VoteListView.as_view(), name='votes_list'),

]