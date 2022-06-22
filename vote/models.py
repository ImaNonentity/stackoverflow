from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import UniqueConstraint

User = get_user_model()


class Vote(models.Model):
    UPVOTE = "1"
    NO_VOTE = "0"
    DOWN_VOTE = "-1"
    rating_choice = (
        (UPVOTE, 1),
        (NO_VOTE, 0),
        (DOWN_VOTE, -1)
    )
    RATING_CHOICES_LIST_INT = [int(NO_VOTE), int(UPVOTE), int(DOWN_VOTE)]
    RATING_CHOICES_LIST_STR = [UPVOTE, DOWN_VOTE, NO_VOTE]
    action_type = models.CharField(max_length=20, choices=rating_choice, default=0)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, verbose_name='related object')
    content_object = GenericForeignKey('content_type', 'object_id')
    # unique_value = UniqueConstraint(content_object, user)

    def __str__(self):
        return f'{self.user}, vote: {self.action_type}, id: {self.id}' \
               f'created_at: {self.created_at}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"
