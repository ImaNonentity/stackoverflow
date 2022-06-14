# from user_profile.models import User, TITLES
from rest_framework.response import Response
from user_profile.models import User, NEWBIE, APPRENTICE, THINKER, MASTER, GENIUS, HIGHER_INTELLIGENCE
#


def add_rating(instance):
    """ User rating->role logic """

    user = User.objects.get(pk=instance.id)
    user.rating += 25

    if user.rating < 100:
        user.role = NEWBIE
    elif 100 < user.rating < 200:
        user.role = APPRENTICE
    elif 200 < user.rating < 300:
        user.role = THINKER
    elif 300 < user.rating < 400:
        user.role = MASTER
    elif 400 < user.rating < 500:
        user.role = GENIUS
    else:
        user.role = HIGHER_INTELLIGENCE
    user.save()
    return user

