from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from user_profile.models import User
from vote.models import Vote


class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    content = models.TextField(max_length=1000, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='answered')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='edited')
    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(
        verbose_name='related object',
        null=True,
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.content[:40]}, id={self.id}'

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Asked')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Modified')
    tag = models.ManyToManyField(Tag, verbose_name='User tag(s)', blank=True)
    comment = GenericRelation(Comment)
    vote_count = models.IntegerField(default=0)
    vote = GenericRelation(Vote)

    def __str__(self):
        return f'{self.title}, {self.content}, id={self.id}'

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"


class Answer(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='answered')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='edited')
    comment = GenericRelation(Comment)
    vote_count = models.IntegerField(default=0)
    vote = GenericRelation(Vote)

    def __str__(self):
        return f'{self.content[:35]}, id={self.id}'

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"


