from django.contrib.auth.models import AbstractUser

from django.db import models
from django.urls import reverse


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    email_confirmation = models.BooleanField(default=False)
    rating = models.SmallIntegerField(default=0, null=True, blank=True)
    slug = models.SlugField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"slug": self.slug})

