# from user_profile.models import User, TITLES
from rest_framework.response import Response
from user_profile.models import TITLES, User
#


def add_rating(instance):
    """ User rating->role logic """

    roles = TITLES
    user = User.objects.get(pk=instance.id)
    user.rating += 25

    if user.rating < 100:
        user.role = 'Newbie'
    elif 100 < user.rating < 200:
        user.role = 'Apprentice'
    elif 200 < user.rating < 300:
        user.role = 'Thinker'
    elif 300 < user.rating < 400:
        user.role = 'Master'
    elif 400 < user.rating < 500:
        user.role = 'Genius'
    else:
        user.role = 'Higher Intelligence'
    user.save()
    return user


# VOTE

def upvote(self, request, pk):
    """Upvote a post. Remove downvote of user if present. """

    item = self.objects.get(pk=pk)
    item.downvote.remove(request.user)
    item.upvotes.add(request.user)
    return Response(self.data)


def downvote(self, request, pk):
    """ Downvote a post. Remove upvote of user if present. """

    item = self.objects.get(pk=pk)
    item.upvote.remove(request.user)
    item.downvote.add(request.user)
    return Response(self.data)


def remove_vote(self, request, pk):
    """ Remove casted vote. Upvote -> remove_vote -> no vote."""

    item = self.objects.get(pk=pk)
    item.upvote.remove(request.user)
    item.downvote.remove(request.user)
    return Response(self.data)

