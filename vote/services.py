from django.core.exceptions import ObjectDoesNotExist
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

    def __init__(self, user, data):
        self.content_object = data['content_object']
        self.action_type = data['action_type']
        self.content_type = data['content_type']
        self.object_id = data['object_id']
        self.data = data
        self.user = user
        self.vote = 0
        self.update_obj = None
        self.obj = None
        self.number = 0

    def validate_user(self):
        if self.user.rating < 50:
            raise serializers.ValidationError(f"{self.user.username.title()}, "
                                              f"you can't vote until your rating reaches 50."
                                              f" Your current rating is - {self.user.rating}.")
        else:
            pass

    # TODO: что-то не так с проверкой, протестить на вопросах, которым месяц +
    # Голосовать можно в течении 1 месяца, с даты публикации вопроса, для ответа - бессрочно
    def validate_vote_create(self):
        # try:
        #     previous_vote = self.content_object.vote.filter(user=self.user).latest('created_at')
        # except ObjectDoesNotExist:
        #     pass
        current_date = date.today()
        current_month = current_date.month
        last_month = current_month - 1 if current_month != 1 else 12
        today_a_month_ago = date(current_date.year, last_month, current_date.day)
        print(self.content_type == "question", self.content_type)
        if self.content_type == "Question":
            active_questions = Question.objects.filter(created_at__range=[today_a_month_ago, current_date])\
                .values_list('id', flat=True)
            current_question = self.data
            print(active_questions)
            print(int(current_question.get('object_id')))
            if int(current_question.get('object_id')) not in active_questions:
                raise ValidationError(f'{self.user.username.title()}, '
                                      f'the time for voting for this question has expired')
            pass
        pass

    # TODO: доработать выборку времени
    # Переголосовать можно в течении 3 часов, одинаково для вопросов и ответов
    def validate_vote_update(self):
        try:
            previous_vote = self.content_object.vote.filter(user=self.user).latest('created_at')
            current_vote = self.data
            current_hour = datetime.now().hour
            start_hour = current_hour - 3 if current_hour != 1 else 24
            active_votes = Vote.objects.filter(user=self.user, created_at__hour__range=[start_hour, current_hour])\
                .values_list('id', flat=True)

            print(f'"ACTIVE VOTE IDS"  {active_votes}')
            print(f'"PREVIOUS VOTE": {previous_vote}')
            print(f'"CURRENTVOTE": {current_vote}')
            if previous_vote.id not in active_votes:
                raise ValidationError(f'{self.user.username.title()}, '
                                      f'unfortunately, you can only re-vote within 3 hours')
            pass
        except ObjectDoesNotExist:
            pass
        pass

    def validate_vote(self):
        try:
            previous_vote = self.content_object.vote.filter(user=self.user).latest('created_at')
            new_action_type = self.data['action_type']
            if int(previous_vote.action_type) == int(new_action_type):
                self.data['action_type'] = 0
            current_vote = self.data
        except ObjectDoesNotExist:
            current_vote = self.data
        return current_vote

    def execute(self):
        """ RUN SYSTEM """
        self.validate_user()
        self.validate_vote_create()
        self.validate_vote_update()
        return self.validate_vote()


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
                                                created_at__date=date.today()).count() + 1
        if self.user.role:
            if today_records > int(self.user.role):
                limit = int(self.user.role) + 1
                raise serializers.ValidationError(f'{self.user.username}, '
                                                  f'your limit is {limit} record(s) per day')
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
