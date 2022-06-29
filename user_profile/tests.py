from unittest import mock
import datetime

import django
import os
import unittest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf_files.settings")
django.setup()

from vote.services import RatingUpdateSystem
from .models import NEWBIE, APPRENTICE, THINKER, MASTER, GENIUS, HIGHER_INTELLIGENCE


class TestRatingServices(unittest.TestCase):

    def setUp(self):
        self.mock_user = mock.Mock(user='testuser',
                                   rating=50,
                                   role=NEWBIE,
                                   return_value=None
        )

    def test_check_rank_newbie(self):
        self.mock_user.rating = 50
        instance = RatingUpdateSystem(self.mock_user)
        new_role = NEWBIE
        self.assertEqual(new_role, instance.check_role())

    def test_check_rank_apprentice(self):
        self.mock_user.rating = 100
        instance = RatingUpdateSystem(self.mock_user)
        new_role = APPRENTICE
        self.assertEqual(new_role, instance.check_role())

    def test_check_rank_thinker(self):
        self.mock_user.rating = 200
        instance = RatingUpdateSystem(self.mock_user)
        new_role = THINKER
        self.assertEqual(new_role, instance.check_role())

    def test_check_rank_master(self):
        self.mock_user.rating = 300
        instance = RatingUpdateSystem(self.mock_user)
        new_role = MASTER
        self.assertEqual(new_role, instance.check_role())

    def test_check_rank_genius(self):
        self.mock_user.rating = 400
        instance = RatingUpdateSystem(self.mock_user)
        new_role = GENIUS
        self.assertEqual(new_role, instance.check_role())

    def test_check_rank_higher_intelligence(self):
        self.mock_user.rating = 500
        instance = RatingUpdateSystem(self.mock_user)
        new_role = HIGHER_INTELLIGENCE
        self.assertEqual(new_role, instance.check_role())

    def test_calculate_rating_power_5(self):
        self.mock_user.rating = 50
        instance = RatingUpdateSystem(self.mock_user)
        rating_power = 5 + self.mock_user.rating
        self.assertEqual(rating_power, instance.calculate_rating_power())

    def test_calculate_rating_power_10(self):
        self.mock_user.rating = 100
        instance = RatingUpdateSystem(self.mock_user)
        rating_power = 10 + self.mock_user.rating
        self.assertEqual(rating_power, instance.calculate_rating_power())

    def test_calculate_rating_power_15(self):
        self.mock_user.rating = 200
        instance = RatingUpdateSystem(self.mock_user)
        rating_power = 15 + self.mock_user.rating
        self.assertEqual(rating_power, instance.calculate_rating_power())

    def test_calculate_rating_power_20(self):
        self.mock_user.rating = 300
        instance = RatingUpdateSystem(self.mock_user)
        rating_power = 20 + self.mock_user.rating
        self.assertEqual(rating_power, instance.calculate_rating_power())

    def test_calculate_rating_power_25(self):
        self.mock_user.rating = 400
        instance = RatingUpdateSystem(self.mock_user)
        rating_power = 25 + self.mock_user.rating
        self.assertEqual(rating_power, instance.calculate_rating_power())

    def test_calculate_rating_power_30(self):
        self.mock_user.rating = 500
        instance = RatingUpdateSystem(self.mock_user)
        rating_power = 30 + self.mock_user.rating
        self.assertEqual(rating_power, instance.calculate_rating_power())

    def test_execute(self):
        """ RUN SYSTEM """
        self.mock_user.rating = 500
        instance = RatingUpdateSystem(self.mock_user)
        rating_power = 30 + self.mock_user.rating
        new_role = HIGHER_INTELLIGENCE
        self.assertEqual((new_role, rating_power), instance.execute())
