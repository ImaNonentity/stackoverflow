from requests import Response


# def upvote(self, request, pk):
#     """Upvote a post. Remove downvote of user if present. """
#
#     item = self.objects.get(pk=pk)
#     item.downvote.remove(request.user)
#     item.upvotes.add(request.user)
#     return Response(self.data)
#
#
# def downvote(self, request, pk):
#     """ Downvote a post. Remove upvote of user if present. """
#
#     item = self.objects.get(pk=pk)
#     item.upvote.remove(request.user)
#     item.downvote.add(request.user)
#     return Response(self.data)
#
#
# def remove_vote(self, request, pk):
#     """ Remove casted vote. Upvote -> remove_vote -> no vote."""
#
#     item = self.objects.get(pk=pk)
#     item.upvote.remove(request.user)
#     item.downvote.remove(request.user)
#     return Response(self.data)


def get_user_vote(self, obj):
    try:
        user = self.context['request'].user
    except KeyError:
        return 0
    if user in obj.upvotes.all():
        return 1
    if user in obj.downvotes.all():
        return -1
    return 0
