from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.timeplace import models
from apps.user.models import User


class TestInterestEndpoints(APITestCase):
    def setUp(self):
        models.Interest.objects.bulk_create(
            [
                models.Interest(name="Cars"),
                models.Interest(name="Animals"),
                models.Interest(name="Museums"),
                models.Interest(name="Bars"),
            ]
        )
        self.superuser = User.objects.create_superuser(
            username="admin",
            email="admin@stsp.com",
            password="admin@2023",
        )
        self.supertoken = Token.objects.create(user=self.superuser)
        self.user = User.objects.create_user(
            username="user",
            email="user@stsp.com",
            password="user@2023",
        )
        self.usertoken = Token.objects.create(user=self.user)

    def testListView(self):
        url = reverse("interest-list")
        response = self.client.get(url)
        expected_content = {
            "count": 4,
            "next": None,
            "previous": None,
            "results": [
                {"id": 2, "name": "Animals"},
                {"id": 4, "name": "Bars"},
                {"id": 1, "name": "Cars"},
                {"id": 3, "name": "Museums"},
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data), expected_content)

    def testPostForbiddenNotAuthenticated(self):
        url = reverse("interest-list")
        response = self.client.post(url, {"name": "Planes"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def testPostForbiddenAuthenticatedUser(self):
        url = reverse("interest-list")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.usertoken.key)
        response = self.client.post(url, {"name": "Planes"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def testPostAsAdmin(self):
        url = reverse("interest-list")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.supertoken.key)
        response = self.client.post(url, {"name": "Planes"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

