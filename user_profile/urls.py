# from .views import RegisterAPI
# from knox import views as knox_views
# from .views import LoginAPI

from django.urls import path
from .views import (
    RegistrationView,
    ObtainAuthTokenView,
    UpdateUserView,
    UserDetailView,
    UserListView,
    DeleteUserView,

)
# from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    # USER URLS
    path('api/user/<pk>/', UserDetailView.as_view(), name="user_detail"),
    path('api/user/<pk>/update', UpdateUserView.as_view(), name="user_update"),
    path('api/user/list/', UserListView.as_view(), name="users_list"),
    path('api/user/<pk>/delete', DeleteUserView.as_view(), name="user_delete"),

    # REGISTRATION & LOGIN URLS
    path('api/register/', RegistrationView.as_view(), name="registration"),
    path('api/login', ObtainAuthTokenView.as_view(), name="login"),


    # KNOX URLS
    # path('api/login/', LoginAPI.as_view(), name='login'),
    # path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]

