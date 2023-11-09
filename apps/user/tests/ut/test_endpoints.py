from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


from apps.user.models import User, UserProfile


class TestUserEndpoints(APITestCase):
    """
    Tests for the user endpoints.

    """

    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser(
            username="admin",
            email="admin@stsp.com",
            password="admin_2023",
        )
        cls.supertoken = Token.objects.create(user=cls.superuser)

        cls.user = User.objects.create_user(
            username="test_user",
            email="test_user@stsp.com",
            password="test_user_2023",
        )
        cls.usertoken = Token.objects.create(user=cls.user)

    def test_user_list_authorized(self):
        """Tests that a list of users are returned for admin only"""

        url = reverse("user-list")
        response = self.client.get(url)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.supertoken.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_unauthorized(self):
        """Tests that a user is unauthorized to get a list of users"""

        url = reverse("user-detail", args=(self.user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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

    def test_user_no_username_given(self):
        """Tests that a user cannot be created without a username"""

        url = reverse("user-list")
        response = self.client.post(
            url,
            data={
                "username": "",
                "password": "fred_2023",
                "email": "fred@stsp.com",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_no_password_given(self):
        """Tests that a user cannot be created without a password"""

        url = reverse("user-list")
        response = self.client.post(
            url,
            data={
                "username": "frank",
                "password": "",
                "email": "frank@stsp.com",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user(self):
        """Tests that a user can only be deleted by the superuser"""

        user_for_deletion = User.objects.create_user(
            username="user1",
            email="user1@stsp.com",
            password="user1_2023",
        )

        usertoken_for_deletion = Token.objects.create(user=user_for_deletion)

        url = reverse("user-detail", args=(self.user.id,))
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + usertoken_for_deletion.key
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse("user-detail", args=(self.user.id,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.supertoken.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_user(self):
        """Tests that a user can update their own data"""

        user_for_updating = User.objects.create_user(
            username="user2",
            email="user2@stsp.com",
            password="user2_2023",
        )

        usertoken_for_updating = Token.objects.create(user=user_for_updating)

        new_data = {
            "username": "bob",
            "email": "bob@stsp.com",
            "password": "bob_2023",
        }
        url = reverse("user-detail", args=(user_for_updating.id,))
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + usertoken_for_updating.key
        )
        response = self.client.put(url, data=new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
