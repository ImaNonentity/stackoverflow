#
# class TestCaseSuite(Base):
#
#     def test_permissions(self):
#         user = UserFactory()
#         admin = AdminFactory()
#         # 401 Not authenticated
#         self.api_client.logout()
#         response = self.api_client.post(url, data=data)
#         assert response.status_code == 401
#         # 403 Not admin
#         self.api_client.force_authenticate(user)
#         response = self.api_client.post(url, data=data)
#         assert response.status_code == 403
#         # 201 Admin
#         self.api_client.logout()
#         self.api_client.force_authenticate(admin)
#         response = self.api_client.post(url, data=data)
#         assert response.status_code == self.success_code

