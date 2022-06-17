from django.urls import path
from .views import VoteCreateView, VoteListView, VoteUpdateView, VoteUserView

urlpatterns = [
    path('vote/create', VoteCreateView.as_view(), name='create_vote'),
    path('vote/list', VoteListView.as_view(), name='votes_list'),
    path('vote/<id>/update', VoteUpdateView.as_view(), name='update_vote'),
    path('vote/list/by', VoteUserView.as_view(), name='votes_list_by_user'),

]