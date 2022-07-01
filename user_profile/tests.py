from unittest import mock
import datetime

import django
import os
import unittest

from vote.exceptions import DailyValidationException
from .services import UserProfileService

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

    def test_validate_user_can_post_daily_records(self):
        records = int(self.mock_user.role)
        instance = RatingUpdateSystem(self.mock_user)
        self.assertEqual(f'{self.mock_user.username}, you can create record!',
                         instance.validate_user_records_per_day(records))

    def test_validate_user_can_not_post_daily_records(self):
        records = int(self.mock_user.role) + 1
        instance = RatingUpdateSystem(user=self.mock_user)
        with self.assertRaises(DailyValidationException) as context:
            message = f'{self.mock_user.username},your limit is {records} record(s) per day'
            instance.validate_user_records_per_day(records)
            self.assertEqual(message, str(context.exception))


class TestUserProfileService(unittest.TestCase):

    def setUp(self):
        self.bonus_fields = dict(
            birth_date=None,
            profile_photo=None,
            first_name=None,
            last_name=None,
        )
        self.mock_user = mock.Mock(
            user='testuser',
            rating=50,
            role=NEWBIE,
            profile_rating_bonuses=self.bonus_fields,
            return_value=None,
            birth_date=None,
            profile_photo=None,
            first_name=None,
            last_name=None,
        )

        self.new_photo_dir = "/example/photo/dir.jpg"

    def test_onetime_addon(self):
        instance = UserProfileService(self.mock_user)
        expected_rating = int(self.mock_user.rating) + 15
        self.assertEqual(expected_rating, instance.onetime_addon().rating)

    def test_save_profile_update_birth_date(self):
        self.mock_user.birth_date = "some birth date"
        instance = UserProfileService(self.mock_user)
        expected_rating = int(self.mock_user.rating) + 15
        self.assertEqual(expected_rating, instance.save_profile().rating)

    def test_save_profile_update_full_name(self):
        self.mock_user.first_name = "some first name"
        self.mock_user.last_name = "some last name"
        instance = UserProfileService(self.mock_user)
        expected_rating = int(self.mock_user.rating) + 15 + 15
        self.assertEqual(expected_rating, instance.save_profile().rating)

    def test_save_profile_update_profile_photo(self):
        self.mock_user.profile_photo = self.new_photo_dir
        instance = UserProfileService(self.mock_user)
        expected_rating = int(self.mock_user.rating) + 15
        self.assertEqual(expected_rating, instance.save_profile().rating)




