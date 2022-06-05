# from .views import RegisterAPI
# from knox import views as knox_views
# from .views import LoginAPI

from django.urls import path
from .views import registration_view
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/register/', registration_view, name="register"),
    path('api/login/', obtain_auth_token, name="login"),


    # TRYING KNOX, 4 fun
    # path('api/login/', LoginAPI.as_view(), name='login'),
    # path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]

