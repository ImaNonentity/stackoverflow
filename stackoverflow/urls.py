from django.contrib import admin
from .views import home_screen_view

from django.urls import path, include

# app_name = 'stackoverflow'
#
urlpatterns = [
    path('', home_screen_view, name='home'),
]
