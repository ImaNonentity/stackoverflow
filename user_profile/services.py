def uploading(instance, file):
    """ Path to upload avatar file """

    return f'profile_avatar/{instance.username}/{file}'

class UserProfileService:

    def __init__(self, user):
        self.user = user
        self.bonus_fields = [
            "birth_date",
            "profile_photo",
            "first_name",
            "last_name",
        ]

    def onetime_addon(self):
        self.user.rating += 15
        self.user.save()
        return self.user

    def save_profile(self):
        for bonus_field in self.bonus_fields:
            if getattr(self.user, bonus_field, False):
                if not self.user.profile_rating_bonuses.get(bonus_field):
                    self.onetime_addon()
                    self.user.profile_rating_bonuses[bonus_field] = True
        self.user.profile_rating_bonuses = self.user.profile_rating_bonuses
        self.user.save()



