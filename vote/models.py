from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from user_profile.models import User


class Vote(models.Model):
    rating_choice = (
        ('1', 1),
        ('0', 0),
        ('-1', -1)
    )
    action_type = models.CharField(max_length=20, choices=rating_choice)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, null=True, blank=True,  on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, verbose_name='related object')
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.user}, vote: {self.action_type}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"
