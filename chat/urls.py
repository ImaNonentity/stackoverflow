from django.urls import path

from . import views
from .views import MessageSendView, MessagesView, SingleMessageDetailView

urlpatterns = [
    path('room/<int:pk>/message/send', MessageSendView.as_view(), name='send_message'),
    path('room/<int:pk>/message/list', MessagesView.as_view(), name='check_all_messages'),
    path('room/<int:pk>/message/detail', SingleMessageDetailView.as_view(), name='check_message_details'),
]