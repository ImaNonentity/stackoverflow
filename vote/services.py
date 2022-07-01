from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status, serializers
from user_profile.models import User, TITLES, NEWBIE, APPRENTICE, THINKER, MASTER, GENIUS, HIGHER_INTELLIGENCE
from social.models import Question, Answer, Comment
# import datetime
from datetime import datetime, date, time, timedelta, timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Vote
from .exceptions import (DailyValidationException,
                         ValidationVoteException,
                         ValidationReVoteTimeException,
                         ValidationTimeCreateVoteException,
                         ValidationUserRatingException
                         )


class VotingCountSystem:
    """ Voting Count System Logic """

    def __init__(
            self,
            user,
            content_object: Vote | Answer | Question,
            action_type: int,
            content_type: Question | Answer = None,
            object_id: int = None,
            _latest_vote=None,
            current_time: datetime = datetime.now(),
    ):
        self.content_object = content_object
        self.action_type = action_type
        self.content_type = content_type
        self.object_id = object_id
        self.user = user
        self._latest_vote = _latest_vote
        self.current_time: datetime = current_time

    def validate_user(self):
        if self.user.rating < 50:
            message = (f"{self.user.username.title()}, you can't vote until your rating reaches 50."
                       f" Your current rating is - {self.user.rating}.")
            raise ValidationUserRatingException(message)
        return

    def validate_vote_create(self):
        if self.content_type == ContentType.objects.get_for_model(Question):
            if (self.content_object.created_at + timedelta(hours=730)).timestamp() < self.current_time.timestamp():
                message = f'{self.user.username.title()}, the time for voting for this question has expired. :( '
                raise ValidationTimeCreateVoteException(message)
            return f'{self.user.username.title()}, you can vote for this question.'
        else:
            return f'{self.user.username.title()}, you can vote for this answer.'

    # TODO: @patch this in unittest
    @property
    def latest_vote(self) -> Vote:
        if not self._latest_vote:
            return self.content_object.vote.filter(user=self.user).latest('created_at')
        return self._latest_vote

    def validate_vote_update(self):
        try:
            latest_vote = self.latest_vote
        except ObjectDoesNotExist:
            return
        else:
            if (latest_vote.created_at + timedelta(hours=3)).timestamp() < self.current_time.timestamp():
                message = f'{self.user.username.title()}, unfortunately, you can only re-vote within 3 hours'
                raise ValidationReVoteTimeException(message)
            return f'{self.user.username.title()}, you can re-vote'

    def validate_vote(self):
        try:
            previous_vote = self.latest_vote
            new_action_type = self.action_type
            if int(previous_vote.action_type) == 1 and int(new_action_type) == -1:
                self.action_type = 0
            if int(previous_vote.action_type) == -1 and int(new_action_type) == 1:
                self.action_type = 0
            if int(previous_vote.action_type) == int(new_action_type):
                message = f"{self.user.username.title()}, you've already cast your vote!"
                raise ValidationVoteException(message)
            current_vote = self.action_type
        except ObjectDoesNotExist:
            current_vote = self.action_type
        return current_vote

    def vote_count(self):
        try:
            latest_vote = self.latest_vote
            if int(latest_vote.action_type) != int(self.action_type):
                self.content_object.vote_count += int(self.action_type)
        except ObjectDoesNotExist:
            self.content_object.vote_count += int(self.action_type)
        self.content_object.save()
        return self.content_object

    def execute(self):
        """ RUN SYSTEM """
        self.validate_user()
        self.validate_vote_create()
        self.validate_vote_update()
        self.vote_count()
        return self.validate_vote()


class RatingUpdateSystem:
    """ Rating Count System Logic """

    def __init__(self, user):
        self.user = user
        self.rating_power = 0

    def validate_user_records_per_day(self, today_records):
        if today_records > int(self.user.role):
            limit = int(self.user.role) + 1
            message = f'{self.user.username},your limit is {limit} record(s) per day'
            raise DailyValidationException(message)
        return f'{self.user.username}, you can create record!'

    def check_role(self):
        """ User rating -> role logic """
        if self.user.rating < 100:
            self.user.role = NEWBIE
        elif 100 <= self.user.rating < 200:
            self.user.role = APPRENTICE
        elif 200 <= self.user.rating < 300:
            self.user.role = THINKER
        elif 300 <= self.user.rating < 400:
            self.user.role = MASTER
        elif 400 <= self.user.rating < 500:
            self.user.role = GENIUS
        else:
            self.user.role = HIGHER_INTELLIGENCE
        self.user.save()
        return self.user.role

    def calculate_rating_power(self):
        if self.user.rating < 100:
            self.rating_power = 5
        elif 100 <= self.user.rating < 200:
            self.rating_power = 10
        elif 200 <= self.user.rating < 300:
            self.rating_power = 15
        elif 300 <= self.user.rating < 400:
            self.rating_power = 20
        elif 400 <= self.user.rating < 500:
            self.rating_power = 25
        else:
            self.rating_power = 30
        self.user.rating += self.rating_power
        self.user.save()
        return self.user.rating

    def execute(self):
        """ RUN SYSTEM """
        today_records = Question.objects.filter(user=self.user,
                                                created_at__date=date.today()).count()
        user_can_vote = self.validate_user_records_per_day(today_records)
        user_role = self.check_role()
        user_rating = self.calculate_rating_power()
        return user_role, user_rating, user_can_vote
