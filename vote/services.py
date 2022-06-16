from django.db.models import UniqueConstraint
from requests import Response
from rest_framework.exceptions import ValidationError
from user_profile.models import User, NEWBIE, APPRENTICE, THINKER, MASTER, GENIUS, HIGHER_INTELLIGENCE
from social.models import Question, Answer, Comment
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Vote


class VotingCountSystem:
    """ Voting Count System Logic """

    def __init__(self, serializer, user, data):
        self.model = {
            'question': Question,
            'answer': Answer,
            'comment': Comment
        }
        self.data = data
        print(f'DATA = {data}')
        self.content_type = data['content_type']
        self.object_id = data['object_id']
        self.content_object = data['content_object']
        self.object = self.model[self.content_type].objects.get(pk=self.object_id)
        self.serializer = serializer
        self.user = user
        self.rating_power = 0

    def validate_user(self):
        values = UniqueConstraint(self.content_object, self.user)
        if self.user.id in values:
            raise ValidationError("You've already cast your vote!")
        else:
            if self.serializer.is_valid():
                self.serializer.save(user=self.user)
                # self.check_rank()
            return self.serializer

    @receiver(pre_save, sender=Vote)
    def custom_pre_save_vote(sender, instance: Vote, **kwargs):
        """ Custom pre_save Signal for Votes """
        # В order_by добавить сортировку по дате
        # В запрос добавить фильтр по юзеру и вопросу на который оставилии голос
        previous = Vote.objects.filter(
            user=instance.user,
            content_object=instance.content_object
        ).latest(updated_at=instance.updated_at)
        if previous:
            if previous.action_type == instance.action_type:
                instance.action_type = ('0', 0)


class RatingCountSystem(VotingCountSystem):
    """ Rating Count System Logic """

    # def votes_count(self):
    #     upvote = self.objects.action_type.filter(rating_choice=1).count()
    #     downvote = self.objects.action_type.filter(rating_choice=-1).count()
    #     self.objects.votes_count = (upvote + (downvote * -1))
    #     self.objects.save()
    #     return self.objects

    def check_rank(self):
        """ User rating -> role logic """

        question = Question.objects.filter(user=self.user.id).count()
        answer = Answer.objects.filter(user=self.user.id).count()
        self.rating_power = 5 * (question + answer)
        self.user.rating = self.rating_power
                           # + self.obj.votes_count

        if self.user.rating < 100:
            self.user.role = NEWBIE
        elif 100 < self.user.rating < 200:
            self.user.role = APPRENTICE
        elif 200 < self.user.rating < 300:
            self.user.role = THINKER
        elif 300 < self.user.rating < 400:
            self.user.role = MASTER
        elif 400 < self.user.rating < 500:
            self.user.role = GENIUS
        else:
            self.user.role = HIGHER_INTELLIGENCE

        self.user.save()
        return self.user
