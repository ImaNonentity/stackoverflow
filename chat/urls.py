from django.urls import path

from . import views
from .views import MessageSendView, LastMessagesInRoomsView, SingleRoomMessagesView, index_view, room_view

urlpatterns = [
    path('index', index_view, name='index'),
    path('<str:pk>/', views.room_view, name='chat-room'),
    path('room/message/send', MessageSendView.as_view(), name='send_message'),
    path('message/list', LastMessagesInRoomsView.as_view(), name='check_last_messages'),
    path('room/message', SingleRoomMessagesView.as_view(), name='check_messages_in_specific_room'),

]