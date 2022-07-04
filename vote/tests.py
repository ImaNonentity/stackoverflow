from unittest import mock
import datetime
from unittest.mock import Mock, patch

import django
import os
import unittest

from vote.exceptions import ValidationUserRatingException, ValidationTimeCreateVoteException, \
    ValidationReVoteTimeException, ValidationVoteException

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf_files.settings")
django.setup()

from vote.services import VotingCountSystem
from django.contrib.contenttypes.models import ContentType


# TESTUSER
class MockUser:
    def __init__(self, username, rating: int):
        self.username = username
        self.rating = rating


class MockVote:
    def __init__(
            self,
            user: MockUser,
            action_type: int,
            created_at: datetime = datetime.datetime.now(),
    ):
        self.user = user
        self.action_type = action_type
        self.created_at = created_at


class TestVoteServices(unittest.TestCase):

    def setUp(self):
        test_user = MockUser(username='testuser', rating=50)
        self.mock_user = mock.Mock(user=test_user, rating=50, return_value=None)
        self.object_id = mock.Mock(object_id=1)
        self.action_type = 1
        self.content_object = mock.Mock(id=self.object_id, user=self.mock_user,
                                        title='Test title', content='Test content',
                                        created_at=datetime.datetime.strptime(
                                            '2022-06-27 15:25:48',
                                            '%Y-%m-%d %H:%M:%S'
                                        ))
        resource_type = ContentType.objects.get(model='question')
        self.instance = VotingCountSystem(user=self.mock_user, content_object=self.content_object,
                                          content_type=resource_type, object_id=self.object_id,
                                          action_type=self.action_type)
        self.mock_vote = mock.Mock(vote=MockVote, previous_vote=1, action_type=1)
        self.mock_positive_previous_vote = mock.Mock(
            vote=MockVote, action_type=1,
            created_at=datetime.datetime.strptime(
                '2022-06-27 15:25:48',
                '%Y-%m-%d %H:%M:%S'
            ))
        self.mock_expired_previous_vote = mock.Mock(
            vote=MockVote, action_type=1,
            created_at=datetime.datetime.strptime(
                '2022-06-27 03:25:48',
                '%Y-%m-%d %H:%M:%S'
            ))
        self.mock_negative_previous_vote = mock.Mock(
            vote=MockVote, action_type=-1,
            created_at=datetime.datetime.strptime(
                '2022-06-27 15:25:48',
                '%Y-%m-%d %H:%M:%S'
            ))
        self.mock_zero_previous_vote = mock.Mock(
            vote=MockVote, action_type=0,
            created_at=datetime.datetime.strptime(
                '2022-06-27 15:25:48',
                '%Y-%m-%d %H:%M:%S'
            ))

    def test_user_rating_validation_can_create_vote(self):
        """ Голосовать можно, если рейтинг больше 50 """
        VotingCountSystem.validate_user(self.mock_user)
        self.assertEqual(self.mock_user.rating, 50)
        self.mock_user.rating = 60
        self.assertGreater(self.mock_user.rating, 50)

    def test_user_rating_validation_can_not_create_vote(self):
        """ Голосовать нельзя, если рейтинг меньше 50 """
        self.mock_user.rating = 20
        self.assertIsNot(self.mock_user.rating, 50)
        self.assertLess(self.mock_user.rating, 50)
        with self.assertRaises(ValidationUserRatingException) as context:
            message = (f"{self.mock_user.username.title()},"
                       f" you can't vote until your rating reaches 50."
                       f" Your current rating is - {self.mock_user.rating}.")
            self.instance.validate_user()
            self.assertEqual(message, str(context.exception))

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
        with self.assertRaises(ValidationTimeCreateVoteException) as context:
            message = (f"{self.mock_user.username.title()},"
                       f" the time for voting for this question has expired. :( ")
            self.instance.validate_vote_create()
            self.assertEqual(message, str(context.exception))

    def test_validate_vote_on_answer_can_create(self):
        """ Отправлять первый голос можно на ответ, без временного ограничения """
        resource_type = ContentType.objects.get(model='answer')
        self.instance.content_type = resource_type
        instance = self.instance.validate_vote_create()
        self.assertEqual(f'{self.mock_user.username.title()}, you can vote for this answer.', instance)

    def test_validate_vote_can_update(self):
        """ Изменять свой голос можно, если ему не больше 3х часов """
        current_mock_vote = mock.Mock(user=self.mock_user, choose_rating='-1',
                                      created_at=datetime.datetime.strptime(
                                          '2022-06-27 17:25:48',
                                          '%Y-%m-%d %H:%M:%S'
                                      ))
        with patch.object(VotingCountSystem, 'latest_vote', self.mock_positive_previous_vote):
            self.instance = VotingCountSystem(
                user=self.mock_user,
                content_object=self.content_object,
                action_type=1,
                current_time=current_mock_vote.created_at
            )
            instance = self.instance.validate_vote_update()
            self.assertEqual(f'{self.mock_user.username.title()}, you can re-vote', instance)

    def test_validate_vote_can_not_update(self):
        """ Изменять свой голос нельзя, если ему больше 3х часов """
        current_mock_vote = MockVote(
            user=self.mock_user,
            action_type=-1,
            created_at=datetime.datetime.strptime(
                '2022-06-27 15:25:48',
                '%Y-%m-%d %H:%M:%S'
            )
        )
        with patch.object(VotingCountSystem, 'latest_vote', self.mock_expired_previous_vote):
            self.instance = VotingCountSystem(
                user=self.mock_user,
                content_object=self.content_object,
                action_type=1,
                current_time=current_mock_vote.created_at
            )
            with self.assertRaises(ValidationReVoteTimeException) as context:
                message = (f'{self.mock_user.username.title()},'
                           f' unfortunately, you can only re-vote within 3 hours')
                self.instance.validate_vote_update()
                self.assertEqual(message, str(context.exception))

    def test_validate_vote_can_not_vote_alike_negative(self):
        """ Голосование -1 райзит ошибку, если мы изначально стояли на -1 """

        with patch.object(VotingCountSystem, 'latest_vote', self.mock_negative_previous_vote):
            self.instance = VotingCountSystem(
                user=self.mock_user,
                content_object=self.content_object,
                action_type=-1,
            )
            with self.assertRaises(ValidationVoteException) as context:
                message = f"{self.mock_user.username.title()}, you've already cast your vote!"
                self.instance.validate_vote()
                self.assertEqual(message, str(context.exception))

    def test_validate_vote_can_not_vote_alike_positive(self):
        """ Голосование +1 райзит ошибку, если мы изначально стояли на +1 """
        with patch.object(VotingCountSystem, 'latest_vote', self.mock_positive_previous_vote):
            self.instance = VotingCountSystem(
                user=self.mock_user,
                content_object=self.content_object,
                action_type=+1,
            )
            with self.assertRaises(ValidationVoteException) as context:
                message = f"{self.mock_user.username.title()}, you've already cast your vote!"
                self.instance.validate_vote()
                self.assertEqual(message, str(context.exception))

    def test_validate_vote_can_up_vote_from_negative(self):
        """ Голосование +1 с позиции -1 дает 0 """
        with patch.object(VotingCountSystem, 'latest_vote', self.mock_negative_previous_vote):
            self.instance = VotingCountSystem(
                user=self.mock_user,
                content_object=self.content_object,
                action_type=1,
            )
            self.assertEqual(0, self.instance.validate_vote())

    def test_validate_vote_can_up_vote_from_zero(self):
        """ Голосование +1 с позиции 0 дает +1 """
        with patch.object(VotingCountSystem, 'latest_vote', self.mock_zero_previous_vote):
            self.instance = VotingCountSystem(
                user=self.mock_user,
                content_object=self.content_object,
                action_type=-1,
            )
            self.assertEqual(-1, self.instance.validate_vote())

    def test_validate_vote_can_down_voteFrom_positive(self):
        """ Голосование -1 с позиции +1 дает 0 """
        with patch.object(VotingCountSystem, 'latest_vote', self.mock_positive_previous_vote):
            self.instance = VotingCountSystem(
                user=self.mock_user,
                content_object=self.content_object,
                action_type=-1,
            )
            self.assertEqual(0, self.instance.validate_vote())

    def test_validate_vote_can_down_vote_from_zero(self):
        """ Голосование -1 с позиции 0 дает -1 """
        with patch.object(VotingCountSystem, 'latest_vote', self.mock_zero_previous_vote):
            self.instance = VotingCountSystem(
                user=self.mock_user,
                content_object=self.content_object,
                action_type=-1,
            )
            self.assertEqual(-1, self.instance.validate_vote())

    def test_vote_count_active_calc_first_positive(self):
        """ Если прошлый голос был +1 а настоящий -1, то от общего значения отнимется 1 """
        self.content_object = mock.Mock(id=self.object_id, user=self.mock_user,
                                        vote_count=5)
        with patch.object(VotingCountSystem, 'latest_vote', self.mock_positive_previous_vote):
            self.instance = VotingCountSystem(
                user=self.mock_user,
                content_object=self.content_object,
                action_type=-1,
            )
            self.assertEqual(self.content_object, self.instance.vote_count())

    def test_vote_count_active_calc_first_negative(self):
        """ Если прошлый голос был -1 а настоящий +1, то к общему значению прибавится 1 """
        self.content_object = mock.Mock(id=self.object_id, user=self.mock_user,
                                        vote_count=5)
        with patch.object(VotingCountSystem, 'latest_vote', self.mock_negative_previous_vote):
            self.instance = VotingCountSystem(
                user=self.mock_user,
                content_object=self.content_object,
                action_type=+1,
            )
            self.assertEqual(self.content_object, self.instance.vote_count())

    def test_vote_count_passive_calc(self):
        """ Если прошлый голос был +1 и настоящий тоже +1, то общее значение не изменится """
        self.content_object = mock.Mock(id=self.object_id, user=self.mock_user,
                                        vote_count=5)
        with patch.object(VotingCountSystem, 'latest_vote', self.mock_positive_previous_vote):
            self.instance = VotingCountSystem(
                user=self.mock_user,
                content_object=self.content_object,
                action_type=+1,
            )
            self.assertEqual(self.content_object, self.instance.vote_count())

    def test_vote_count_negative_calc(self):
        """ Если прошлый голос был -1 и настоящий тоже -1, то общее значение не изменится """
        self.content_object = mock.Mock(id=self.object_id, user=self.mock_user,
                                        vote_count=5)
        with patch.object(VotingCountSystem, 'latest_vote', self.mock_negative_previous_vote):
            self.instance = VotingCountSystem(
                user=self.mock_user,
                content_object=self.content_object,
                action_type=-1,
            )
            self.assertEqual(self.content_object, self.instance.vote_count())

    def test_execute(self, ):
        """ RUN SYSTEM """

        self.content_object = mock.Mock(
            id=self.object_id,
            user=self.mock_user,
            vote_count=5
        )
        current_mock_vote = MockVote(
            user=self.mock_user,
            action_type=1,
            created_at=datetime.datetime.strptime(
                '2022-03-27 17:25:48',
                '%Y-%m-%d %H:%M:%S'
            )
        )
        with patch.object(VotingCountSystem, 'latest_vote', self.mock_zero_previous_vote):
            self.instance = VotingCountSystem(
                user=self.mock_user,
                content_object=self.content_object,
                action_type=1,
                current_time=current_mock_vote.created_at
            )

            execute = self.instance.execute()
            self.assertEqual(current_mock_vote.action_type, execute)


if __name__ == '__main__':
    unittest.main()
