# from .views import RegisterAPI
# from knox import views as knox_views
# from .views import LoginAPI

from django.urls import path, include
from .views import (
    UpdateUserView,
    UserDetailView,
    UserListView,
    DeleteUserView,
)



urlpatterns = [
    # USER URLS
    path('user/<pk>/', UserDetailView.as_view(), name="user_detail"),
    path('user/<pk>/update', UpdateUserView.as_view(), name="user_update"),
    path('user/list', UserListView.as_view(), name="users_list"),
    path('user/<pk>/delete', DeleteUserView.as_view(), name="user_delete"),
    # path('user/image_upload/', ImageUploadView.as_view())

]

