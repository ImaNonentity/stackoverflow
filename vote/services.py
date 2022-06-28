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


class VotingCountSystem:
    """ Voting Count System Logic """

    def __init__(self, user, content_object, action_type, content_type, object_id):
        self.content_object = content_object
        self.action_type = action_type
        self.content_type = content_type
        self.object_id = object_id
        self.user = user
        self.vote = 0
        self.obj_votes = 0
        self.update_obj = None

    def validate_user(self):
        if self.user.rating < 50:
            raise serializers.ValidationError(f"{self.user.username.title()}, "
                                              f"you can't vote until your rating reaches 50."
                                              f" Your current rating is - {self.user.rating}.")
        return

    def validate_vote_create(self):
        if self.content_type == ContentType.objects.get_for_model(Question):
            if (self.content_object.created_at + timedelta(hours=730)).timestamp() < datetime.now().timestamp():
                raise ValidationError(f'{self.user.username.title()}, '
                                      f'the time for voting for this question has expired. :( ')
            return f'{self.user.username.title()}, you can vote for this question.'
        else:
            return f'{self.user.username.title()}, you can vote for this answer.'

    @property
    def latest_vote(self):
        result = self.content_object.vote.filter(user=self.user).latest('created_at')
        return result

    def validate_vote_update(self):
        try:
            latest_vote = self.latest_vote
        except ObjectDoesNotExist:
            return
        else:
            if (latest_vote.created_at + timedelta(hours=3)).timestamp() < datetime.now().timestamp():
                raise ValidationError(f'{self.user.username.title()}, '
                                      f'unfortunately, you can only re-vote within 3 hours')
            return f'{self.user.username.title()}, you can re-vote'

    def validate_vote(self):
        try:
            previous_vote = self.latest_vote
            print(previous_vote)
            new_action_type = self.action_type
            print(new_action_type)
            if int(previous_vote.action_type) == 1 and int(new_action_type) == -1:
                self.action_type = 0
            if int(previous_vote.action_type) == -1 and int(new_action_type) == 1:
                self.action_type = 0
            if int(previous_vote.action_type) == int(new_action_type):
                raise ValidationError(f"{self.user.username.title()}, "
                                      f"you've already cast your vote!")
            current_vote = self.action_type
        except ObjectDoesNotExist:
            current_vote = self.action_type
        return current_vote

    def vote_count(self):
        try:
            latest_vote = self.latest_vote
            if int(latest_vote.action_type) == int(self.action_type):
                pass
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

    def __init__(self, data, user):
        self.user = user
        self.data = data
        self.rating_power = 0

    def validate_user(self):
        today_records = Question.objects.filter(user=self.user,
                                                created_at__date=date.today()).count()
        if today_records > int(self.user.role):
            limit = int(self.user.role) + 1
            raise ValidationError(f'{self.user.username}, '
                                  f'your limit is {limit} record(s) per day')

    def check_rank(self):
        """ User rating -> role logic """

        if self.user.rating < 100:
            self.rating_power = 5
            self.user.role = NEWBIE
        elif 100 < self.user.rating < 200:
            self.rating_power = 10
            self.user.role = APPRENTICE
        elif 200 < self.user.rating < 300:
            self.rating_power = 15
            self.user.role = THINKER
        elif 300 < self.user.rating < 400:
            self.rating_power = 20
            self.user.role = MASTER
        elif 400 < self.user.rating < 500:
            self.rating_power = 25
            self.user.role = GENIUS
        else:
            self.rating_power = 30
            self.user.role = HIGHER_INTELLIGENCE

        self.user.rating += self.rating_power
        print(self.rating_power)
        self.user.save()
        return self.user
