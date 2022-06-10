# from user_profile.models import User, TITLES
#
# def check_user_rating(instance):
#     """ User rating->role logic """
#
#     roles = TITLES
#     user = User.objects.get(pk=instance.id)
#
#     if user.rating < 100:
#         user.role = 'Newbie'
#     elif 100 < user.rating < 200:
#         user.role = 'Apprentice'
#     elif 200 < user.rating < 300:
#         user.role = 'Thinker'
#     elif 300 < user.rating < 400:
#         user.role = 'Master'
#     elif 400 < user.rating < 500:
#         user.role = 'Genius'
#     else:
#         user.role = 'Higher Intelligence'
#     user.save()
#     return user

