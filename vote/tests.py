from unittest import mock
from unittest.mock import patch
import datetime

import django
import os
import unittest

from social_core.backends import username

from social.tests import test_question

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf_files.settings")
django.setup()

from vote.services import VotingCountSystem
from django.contrib.contenttypes.models import ContentType


class MockUser:
    def __init__(self, username, rating):
        self.username = username
        self.rating = rating


class MockVote:
    def __init__(self, previous_vote, action_type):
        self.previous_vote = previous_vote
        self.action_type = action_type

    @property
    def latest_vote(self):
        return 1


class TestVoteServices(unittest.TestCase):

    def setUp(self):
        test_user = MockUser(username='testuser', rating=50)
        self.mock_user = mock.Mock(user=test_user, rating=50, return_value=None)
        self.object_id = mock.Mock(object_id=1)
        self.content_object = mock.Mock(id=self.object_id, user=self.mock_user,
                                        title='Test title', content='Test content',
                                        created_at=datetime.datetime.strptime(
                                            '2022-06-27 15:25:48',
                                            '%Y-%m-%d %H:%M:%S'
                                        ))
        resource_type = ContentType.objects.get(model='question')
        self.action_type = 1
        self.instance = VotingCountSystem(user=self.mock_user, content_object=self.content_object,
                                          content_type=resource_type, object_id=self.object_id,
                                          action_type=self.action_type)
        self.mock_vote = mock.Mock(vote=MockVote, previous_vote=1, action_type=1)

    def test_user_rating_validation_can_create_vote(self):
        """ Голосовать можно, если рейтинг больше 50 """
        VotingCountSystem.validate_user(self.mock_user)
        self.assertEqual(self.mock_user.rating, 50)
        self.mock_user.rating = 60
        self.assertGreater(self.mock_user.rating, 50)

    def test_user_rating_validation_can_not_create_vote(self):
        """ Голосовать нельзя, если рейтинг меньше 50 """
        self.mock_user.rating = 20
        VotingCountSystem.validate_user(self.mock_user)
        self.assertIsNot(self.mock_user.rating, 50)
        self.assertLess(self.mock_user.rating, 50)
        with self.assertRaises(Exception) as context:
            self.assertEqual(f"{self.mock_user.username.title()}, "
                             f"you can't vote until your rating reaches 50."
                             f" Your current rating is - {self.mock_user.rating}.",
                             str(context.exception))

    def test_validate_vote_on_question_can_create(self):
        """ Отправлять первый голос можно, если вопросу не больше месяца """
        instance = self.instance.validate_vote_create()
        self.assertEqual(f'{self.mock_user.username.title()}, you can vote for this question.', instance)

    def test_validate_vote_on_question_can_not_create(self):
        """ Отправлять первый голос нельзя, если вопросу больше месяца """
        self.content_object.created_at = datetime.datetime.strptime(
            '2022-03-27 15:25:48',
            '%Y-%m-%d %H:%M:%S'
        )
        with self.assertRaises(Exception) as context:
            self.assertEqual(f'{self.mock_user.username.title()}, '
                             f'the time for voting for this question has expired. :( ', str(context.exception))

    def test_validate_vote_on_answer_can_create(self):
        """ Отправлять первый голос можно на ответ, без временного ограничения """
        resource_type = ContentType.objects.get(model='answer')
        self.instance.content_type = resource_type
        instance = self.instance.validate_vote_create()
        self.assertEqual(f'{self.mock_user.username.title()}, you can vote for this answer.', instance)

    # # TODO: 'Mock' + 'datetime.timedelta'
    # def test_validate_vote_can_update(self):
    #     """ Изменять свой голос можно, если ему не больше 3х часов """
    #     instance = self.instance.validate_vote_update()
    #     VotingCountSystem.validate_vote_update(self.content_object)
    #     self.assertLess(f'{self.mock_user.username.title()}, you can re-vote', instance)
    #
    # # TODO: 'Mock' + 'datetime.timedelta'
    # def test_validate_vote_can_not_update(self):
    #     """ Изменять свой голос нельзя, если ему больше 3х часов """
    #     self.content_object.created_at = datetime.datetime.strptime(
    #                                         '2022-06-27 15:25:48',
    #                                         '%Y-%m-%d %H:%M:%S'
    #                                         )
    #     with self.assertRaises(Exception) as context:
    #         self.assertLess(f'{self.mock_user.username.title()}, '
    #                         f'unfortunately, you can only re-vote within 3 hours', str(context.exception))

    # TODO: 'Mock'
    def test_validate_vote_can_not_vote_alike(self):
        """ Голосование дважды +1 или дважды -1 райзит ошибку """
        with self.assertRaises(Exception) as context:
            if self.mock_vote.latest_vote == -1 and self.mock_vote.action_type == -1:
                self.assertEqual(f"{self.mock_user.username.title()}, "
                                 f"you've already cast your vote!", str(context.exception))
            elif self.mock_vote.latest_vote == 1:
                if self.mock_vote.action_type == +1:
                    self.assertEqual(f"{self.mock_user.username.title()}, "
                                     f"you've already cast your vote!", str(context.exception))

    # TODO: 'Mock'
    def test_validate_vote_can_vote(self):
        """ Голосование можно +1 и -1 """
        self.mock_vote.latest_vote = 0
        if self.mock_vote.action_type == -1:
            self.assertEqual(-1, self.instance.validate_vote())
        if self.mock_vote.action_type == +1:
            self.assertEqual(+1, self.instance.validate_vote())





if __name__ == '__main__':
    unittest.main()
