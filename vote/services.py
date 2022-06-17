from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status, serializers
from user_profile.models import User, TITLES, NEWBIE, APPRENTICE, THINKER, MASTER, GENIUS, HIGHER_INTELLIGENCE
from social.models import Question, Answer, Comment
import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Vote


# TODO: catch exceptions on UNIQUE constraint failed (IntegrityError at /vote/create)

class VotingCountSystem:
    """ Voting Count System Logic """

    def __init__(self, user, data):
        self.content_object = data['content_object']
        self.action_type = data['action_type']
        self.data = data
        self.user = user
        self.vote = 0
        self.update_obj = None
        self.obj = None
        self.number = 0

    def update_vote(self):
        new_action_type = self.data['action_type']
        vote = self.content_object.vote.get(user=self.user)
        if vote.action_type == new_action_type:
            self.action_type = 0

        vote.action_type = self.action_type
        vote.save()
        return vote


# TODO: написать валидацию юзера.
# Голосовать можно, если рейтинг пользователя >= 50

# за вопросы:
# Голосовать можно в течении 1 месяца, с даты публикации вопроса
# Переголосовать можно в течение 3 часов

# за ответы:
# Переголосовать можно в течении 3 часов
# Голосование за ответ бессрочное

    # @receiver(pre_save, sender=Vote)
    # def custom_pre_save_vote(sender, instance: Vote, **kwargs):
    #     """ Custom pre_save Signal for Votes """
    #     previous = Vote.objects.filter(
    #         user=instance.user,
    #         content_object=instance.content_object
    #     ).latest(updated_at=instance.updated_at)
    #     if previous:
    #         if previous.action_type == instance.action_type:
    #             instance.action_type = ('0', 0)


class RatingCountSystem:
    """ Rating Count System Logic """

    AWARD_POINTS = {
        "ACCEPT_ANSWER": 1,
        "MY_ANSWER_ACCEPTED": 3,
        "ASK_QUESTION": 5,
        "VOTE_ANSWER_UP": 7,
        "VOTE_ANSWER_DOWN": 11,
        "MY_ANSWER_VOTE_ANSWER_UP": 13,
        "MY_ANSWER_VOTE_ANSWER_DOWN": -13,
        "VOTE_QUESTION_UP": 17,
        "VOTE_QUESTION_DOWN": 19,
        "MY_QUESTION_VOTE_QUESTION_UP": 23,
        "MY_QUESTION_VOTE_QUESTION_DOWN": -23,
    }

    def __init__(self, data, user):
        self.user = user
        self.data = data
        self.rating_power = 0

    def validate_user(self):
        today_records = Question.objects.filter(user=self.user,
                                                created_at__date=datetime.date.today()).count()
        if self.user.role:
            if today_records >= int(self.user.role):
                raise serializers.ValidationError(f'{self.user.username}, '
                                                  f'your limit is {self.user.role} record(s) per day')
            return Response(self.data, status=status.HTTP_201_CREATED)

    def check_rank(self):
        """ User rating -> role logic """

        question = Question.objects.filter(user=self.user.id).count()
        answer = Answer.objects.filter(user=self.user.id).count()
        comment = Comment.objects.filter(user=self.user.id).count()
        self.rating_power = 5 * (question + answer + comment)
        self.user.rating += self.rating_power

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
