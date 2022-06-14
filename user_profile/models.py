from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .services import uploading


NEWBIE = '0'
APPRENTICE = '1'
THINKER = '2'
MASTER = '3'
GENIUS = '4'
HIGHER_INTELLIGENCE = '5'

TITLES = [
    [NEWBIE, 'Newbie'],
    [APPRENTICE, 'Apprentice'],
    [THINKER, 'Thinker'],
    [MASTER, 'Master'],
    [GENIUS, 'Genius'],
    [HIGHER_INTELLIGENCE, 'Higher Intelligence']
]


class User(AbstractUser):
    email = models.EmailField(max_length=50, verbose_name='email', unique=True)
    birth_date = models.DateField(verbose_name='birth date', null=True, blank=True)
    profile_photo = models.ImageField(upload_to=uploading, null=True, blank=True)
    role = models.CharField(choices=TITLES, max_length=20, default=NEWBIE, verbose_name='user title')
    rating = models.SmallIntegerField(default=20, null=True, blank=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    email_confirmation = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.email}, {self.username}, your rank - {self.role}'

    # def has_perm(self, perm, obj=None):
    #     return self.is_admin
    #
    # def has_module_perms(self, app_label):
    #     return True

    # def get_absolute_url(self):
    #     return reverse("user_detail", kwargs={"slug": self.slug})
