"""conf_files URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("stackoverflow.urls")),
    # path('', include("api.urls")),
    # path('', include("social.urls")),
    # path('', include('user_profile.urls')),

    # REST FRAMEWORK URLS
    path('', include("api.urls")),
    # path('api/questions/', include('api.urls')),
    # path('api/overview/', include('api.urls')),
    # path('question-list/', include('api.urls'), 'question-list'),
    # path('question-detail/<str:pk>/', include('api.urls'), 'question-detail'),
    # path('question-create/', include('api.urls'), 'question-create'),
    #
    # path('question-update/<str:pk>/', include('api.urls'), 'question-update'),
    # path('question-delete/<str:pk>/', include('api.urls'), 'question-delete'),
    #
    # path('user_profile-profile/<str:pk>', include('api.urls'), 'detail')

]
