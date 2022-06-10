from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from user_profile.models import User


class Vote(models.Model):
    rating_type = [
        ('UP_VOTE', 1),
        ('DOWN_VOTE', -1)
    ]
    username = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=50, choices=rating_type)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, null=True, blank=True,  on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, verbose_name='related object')
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.username} - {self.type}'

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"
