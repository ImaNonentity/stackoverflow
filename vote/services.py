from requests import Response
from rest_framework.exceptions import ValidationError
from user_profile.models import User, NEWBIE, APPRENTICE, THINKER, MASTER, GENIUS, HIGHER_INTELLIGENCE
from social.models import Question, Answer, Comment
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Vote


class VotingCountSystem:
    """ Voting Count System Logic """

    def __init__(self, content_type, object_id, action_type, user):
        self.content_type = content_type
        self.object_id = object_id
        self.action_type = action_type
        self.model = {
            'question': Question,
            'answer': Answer,
            'comment': Comment
        }
        if self.content_type and self.object_id:
            self.object_id = self.model[self.content_type].objects.get(pk=self.object_id)
        self.user = user
        self.rating_power = 0

    @receiver(pre_save, sender=Vote)
    def custom_pre_save_vote(sender, instance, **kwargs):
        """ Custom pre_save Signal for Votes """

        if instance.id:
            print("i'm here!")
            current = instance
            previous = Vote.objects.get(id=instance.id)
            if previous.rating_choice != current.rating_choice or previous.rating_choice == str(0):
                instance.rating_choice = current.rating_choice
            elif previous.rating_choice == current.rating_choice:
                instance.rating_choice = str(0)

    # def get_user_vote(self, obj):
    #     try:
    #         user = self.user
    #     except KeyError:
    #         return 0
    #     if user in obj.action_type.get(1):
    #         return 1
    #     if user in obj.action_type.get(0):
    #         return -1
    #     return 0


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
