from django.contrib.auth.models import AbstractUser

from django.db import models


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    email_confirmation = models.BooleanField(default=False)
    rating = models.SmallIntegerField(default=0, null=True, blank=True)


