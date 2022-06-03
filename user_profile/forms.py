from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User

#
# class RegistrationForm(UserCreationForm):
#     email = forms.EmailField(max_length=60, help_text="Required a valid email adress")
#
#     class Meta:
#         model = User
#         fields = ('email', 'username', 'password1', 'password2')
