from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


from apps.user.models import User, UserProfile


class TestUserEndpoints(APITestCase):
    """
    Tests for the user endpoints.

    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin",
            email="admin@stsp.com",
            password="admin@2023",
        )
        self.supertoken = Token.objects.create(user=self.superuser)

        self.user = User.objects.create_user(
            username="user_delete",
            email="user_delete@stsp.com",
            password="user_delete@2023",
        )

        self.usertoken = Token.objects.create(user=self.user)

    def test_user_list_authorized(self):
        """Tests that a list of users is returned for the admin only"""

        url = reverse("user-list")
        response = self.client.get(url)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.supertoken.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        """Tests that a user can be created"""

        url = reverse("user-list")
        response = self.client.post(
            url,
            data={
                "username": "testuser",
                "password": "testpassword",
                "email": "test@example.com",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_user(self):
        """Tests that a user can only be deleted by the superuser"""

        url = reverse("user-detail", args=(self.user.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        url = reverse("user-detail", args=(self.user.id,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.supertoken.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
