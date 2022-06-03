from django.shortcuts import render
# from user_profile.models import User
# from rest_framework import generics
# from rest_framework.permissions import IsAdminUser


def home_screen_view(request):
    print(request.headers)
    return render(request, "base.html", {})


