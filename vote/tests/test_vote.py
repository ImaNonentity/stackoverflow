from unittest import mock
from unittest.mock import patch
from datetime import datetime

import django
import os
import unittest

from social_core.backends import username

from social.tests import test_question

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf_files.settings")
django.setup()

from vote.services import VotingCountSystem


class MockUser:
    def __init__(self, username, rating):
        self.username = username
        self.rating = rating


class MockQuestion:
    def __init__(self, content_type, created_at):
        self.content_type = content_type
        self.created_at = created_at



class TestVoteServices(unittest.TestCase):
    test_user = MockUser(username='testuser', rating=50)
    mock_user = mock.Mock(user=test_user, rating=50, return_value=None)

    test_question = MockQuestion(content_type='Question', created_at='2022-06-20 15:25:48.402388')
    mock_question = mock.Mock(id=1, content_type=test_question, created_at='2022-06-20 15:25:48.402388')

    mock_vote = mock.Mock(id=1, created_at='2022-06-27 15:25:48.402388')

    def test_user_rating_validation_can_create_vote(self):
        """ Голосовать можно, если рейтинг больше 50 """
        VotingCountSystem.validate_user(TestVoteServices.mock_user)
        self.assertEqual(TestVoteServices.mock_user.rating, 50)
        TestVoteServices.mock_user.rating = 60
        self.assertGreater(TestVoteServices.mock_user.rating, 50)

    def test_user_rating_validation_can_not_create_vote(self):
        """ Голосовать нельзя, если рейтинг меньше 50 """
        TestVoteServices.mock_user.rating = 20
        VotingCountSystem.validate_user(TestVoteServices.mock_user)
        self.assertIsNot(TestVoteServices.mock_user.rating, 50)
        self.assertLess(TestVoteServices.mock_user.rating, 50)

    # def test_validate_vote_can_create(self):
    #     """ Отправлять первый голос можно, если вопросу не больше месяца """
    #
    #     conditional_today = "2022-06-27 15:25:48.402388"
    #     question_create_time = TestVoteServices.mock_question.created_at
    #     VotingCountSystem.validate_vote_create(TestVoteServices.mock_question)
    #     self.assertLess(question_create_time, conditional_today)
    #
    # def test_validate_vote_can_not_create(self):
    #     """ Отправлять первый голос нельзя, если вопросу больше месяца """
    #
    #     conditional_today = "2022-06-27 15:25:48.402388"
    #     TestVoteServices.mock_question.created_at = '2022-03-20 15:25:48.402388'
    #     question_create_time = TestVoteServices.mock_question.created_at
    #     VotingCountSystem.validate_vote_create(TestVoteServices.mock_question)
    #     self.assertLess(question_create_time, conditional_today)

    def test_validate_vote_can_update(self):
        """ Изменять свой голос можно, если ему не больше 3х часов """
        conditional_today = "2022-06-27 15:25:48.402388"
        question_create_time = TestVoteServices.mock_question.created_at
        VotingCountSystem.validate_vote_update(TestVoteServices.mock_question)
        print('imhere')
        self.assertLess(question_create_time, conditional_today)

    def test_validate_vote_can_not_update(self):
        """ Изменять свой голос нельзя, если ему больше 3х часов """
        conditional_today = "2022-06-27 15:25:48.402388"
        TestVoteServices.mock_vote.created_at = '2022-03-20 15:25:48.402388'
        question_create_time = TestVoteServices.mock_question.created_at
        VotingCountSystem.validate_vote_update(TestVoteServices.mock_question)
        self.assertLess(question_create_time, conditional_today)
    #
    # def test_validate_vote(self):
    #     pass


if __name__ == '__main__':
    unittest.main()
