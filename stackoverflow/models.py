from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from django.contrib.contenttypes.models import ContentType

# Create your models here.


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    nickname = models.CharField(max_length=200, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField()
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    role = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField()
    email_confirmation = models.BooleanField(default=False)
    rating = models.SmallIntegerField(default=0, null=True, blank=True)


    def __str__(self):
        return self.nickname


class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(max_length=500, null=True, blank=True)


class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Asked')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Modified')
    tags = models.ManyToManyField(Tag, verbose_name='User`s tag(s)')
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"""
        username = {self.username}
        title = {self.title};
        content = {self.content};
        created_at = {self.created_at};
        updated_at = {self.updated_at};
        tags = {self.tags};
        likes = {self.likes};
        """


class Answer(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='answered')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='edited')
    likes = models.IntegerField(default=0)


    def __str__(self):
        return f"""
        username = {self.username};
        content = {self.content};
        created_at = {self.created_at};
        updated_at = {self.updated_at};
        likes = {self.likes};
        """


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    likes = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='answered')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='edited')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Votes(models.Model):
    rating_type = (
        ('UP_VOTE', 1),
        ('DOWN_VOTE', -1)
    )
    username = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    type = models.\
        CharField(max_length=50, choices=rating_type)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.username} - {self.type}'
