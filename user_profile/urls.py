# from .views import RegisterAPI
# from knox import views as knox_views
# from .views import LoginAPI

from django.urls import path
from .views import registration_view
from .views import (
    api_detail_user_view,
    api_update_user_view,
    api_delete_user_view,
    ObtainAuthTokenView,
)
# from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    # USER URLS
    path('api/user/<pk>/', api_detail_user_view, name="user_detail"),
    path('api/user/<pk>/update', api_update_user_view, name="user_update"),
    path('api/user/<pk>/delete', api_delete_user_view, name="user_delete"),

    # REGISTRATION & LOGIN URLS
    path('api/register/', registration_view, name="register"),
    path('api/login', ObtainAuthTokenView.as_view(), name="login"),


    # KNOX URLS
    # path('api/login/', LoginAPI.as_view(), name='login'),
    # path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]

