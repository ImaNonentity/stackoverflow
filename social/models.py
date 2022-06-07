from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from user_profile.models import User


class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tags"
        verbose_name_plural = "Tags"


class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Asked')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Modified')
    tags = models.ManyToManyField(Tag, verbose_name='User tag(s)', blank=True)
    likes = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f'{self.title}, {self.content}, id={self.id}'

    class Meta:
        verbose_name = "Questions"
        verbose_name_plural = "Questions"


class Answer(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='answered')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='edited')
    # likes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.content[:35]}, id={self.id}'

    class Meta:
        verbose_name = "Answers"
        verbose_name_plural = "Answers"


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    content = models.TextField(max_length=1000, null=True, blank=True)
    # likes = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='answered')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='edited')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.content[:40]}, id={self.id}'

    class Meta:
        verbose_name = "Comments"
        verbose_name_plural = "Comments"


class Votes(models.Model):
    rating_type = (
        ('UP_VOTE', 1),
        ('DOWN_VOTE', -1)
    )
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=rating_type)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.username} - {self.type}'

    class Meta:
        verbose_name = "Votes"
        verbose_name_plural = "Votes"

