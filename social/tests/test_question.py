# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIRequestFactory, APITestCase
# from rest_framework.authtoken.models import Token
# from rest_framework.test import force_authenticate

# from social.models import Question
# from user_profile.models import User


# factory = APIRequestFactory()
# request = factory.post('/question/', {'title': 'new idea'})

#
# class TestCreateQuestion(APITestCase):
#     def authenticate_user(self):
#         self.client.post(reverse('register'), {'email': 'mytestemail@gmail.com',
#                                                'password': 'mytestpassword'
#                                                })
#         response = self.client.post(
#             reverse('login'), {'email': 'mytestemail@gmail.com', 'password': 'mytestpassword'})
#
#         self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['token']}")
#
#     def test_can_create_question(self):
#         previous_question_count = Question.objects.all().count()
#         self.authenticate_user()
#         test_question = {'title': 'TEST', 'content': 'TEST TEST'}
#         response = self.client.post(reverse('question_new'), test_question)
#         self.assertEqual(Question.objects.all().count(), previous_question_count +1)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#     def test_cannot_create_question(self):
#         test_question = {'title': 'TEST', 'content': 'TEST TEST'}
#         response = self.client.post(reverse('question_new'), test_question)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#



    #
    #     def setUp(self):
    #         test_question = Question.objects.create(title="test title", content="test_content")
    #         test_question.save()
    #
    #         self.user = User.objects.create(email="test@email.com")
    #         self.user.set_password("testpassword")
    #
    #         Token.objects.create(user=self.user)
    #
    #     def test_CreateQuestion(self):
    #         check_login = self.client.login(email="test@email.com", password="testpassword")
    #         self.assertTrue(check_login)
    #
    #         token = Token.objects.get_or_create(user=self.user)
    #         self.client.credentials(HTTP_AUTHORIZATION=f'Token {token[0].key}')
    #
    #         data = {"table": 1}
    #
    #         response = self.client.post(reverse('question_new-order'), data=data, content_type='application/json')
    #         question = Question.objects.filter(table=data['table']).order_by('date')[0]
    #
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def setUp(self):
    #     self.test_user = User.objects.create(email="test@email.com", password="testpassword", rating=100)
    #     Token.objects.create(user=self.test_user)
    #     self.client.login(email="test@email.com", password="testpassword")
    #     self.test_admin = User.objects.create_superuser(email="testadmin@email.com", username="testusername",
    #                                                     password="testpassword")
    #     Token.objects.create(user=self.test_admin)
    #     self.client.login(email="testadmin@email.com", password="testpassword")

    # # HTTP_400_BAD_REQUEST
    # def test_user_can_create_question(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user.auth_token.key)
    #     url = reverse('question_new')
    #     data = {
    #         'title': 'Im just normal user',
    #         'content': 'NORMAL USER'
    #     }
    #     Question.objects.create(user=self.test_user, data=data)
    #     response = self.client.post(url,
    #                                 data,
    #                                 format='json',
    #                                 REMOTE_USER=self.test_user)
    #     self.assertEqual(status.HTTP_201_CREATED, response.status_code)
    #     self.assertEqual(Question.objects.count(), 1)
    #
    # #HTTP_401_UNAUTHORIZED
    # def test_admin_can_create_question(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_admin.auth_token.key)
    #
    #     Question.objects.create(user=self.test_admin, title='Im admin', content='ADMIN USER')
    #     url = reverse('question_new')
    #     response = self.client.get(url)
    #     self.assertEqual(status.HTTP_201_CREATED, response.status_code)
    #     self.assertEqual(Question.objects.count(), 1)

    # def test_anon_user_cannot_create_question(self):
    #     Question.objects.create(title='Im anonymous', content='ANONYMOUS')
    #     url = reverse('question_new')
    #     response = self.client.get(url)
    #     self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    #
    # def test_owner_can_update_question(self):
    #     pass
    #
    # def test_admin_can_update_question(self):
    #     pass
    #
    # def test_random_user_cannot_update_question(self):
    #     pass
    #
    # def test_user_can_delete_question(self):
    #     pass
    #
    # def test_admin_can_delete_question(self):
    #     pass
    #
    # def test_random_user_cannot_delete_question(self):
    #     pass
