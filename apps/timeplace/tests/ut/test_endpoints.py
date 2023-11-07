from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.timeplace import models
from apps.user.models import User


class TestInterestEndpoints(APITestCase):
    @classmethod
    def setUpClass(cls):
        models.Interest.objects.bulk_create(
            [
                models.Interest(name="Cars"),
                models.Interest(name="Animals"),
                models.Interest(name="Museums"),
                models.Interest(name="Bars"),
            ]
        )
        superuser = User.objects.create_superuser(
            username="admin",
            email="admin@stsp.com",
            password="admin@2023",
        )
        Token.objects.create(user=superuser)
        user = User.objects.create_user(
            username="user",
            email="user@stsp.com",
            password="user@2023",
        )
        Token.objects.create(user=user)
        super().setUpClass()

    def setUp(self):
        self.supertoken = Token.objects.get(user__username="admin")
        self.usertoken = Token.objects.get(user__username="user")

    def testListView(self):
        """Test if the GET request to the base entpoint returns the expected
        result.
        """
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

    def testPostPutDeleteForbiddenNotAuthenticated(self):
        """Test if unsafe requests without any authorization return 401.
        """
        url = reverse("interest-list")
        detail_url = reverse("interest-detail", args=(4,))

        post_response = self.client.post(url, {"name": "Planes"})
        self.assertEqual(post_response.status_code, status.HTTP_401_UNAUTHORIZED)

        put_response = self.client.put(detail_url, {"name": "Airplanes"})
        self.assertEqual(put_response.status_code, status.HTTP_401_UNAUTHORIZED)


    def testPostPutDeleteForbiddenAuthenticatedUser(self):
        """Test if unsafe requests from normal user without admin rights
        return 403.
        """
        url = reverse("interest-list")
        detail_url = reverse("interest-detail", args=(4,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.usertoken.key)

        post_response = self.client.post(url, {"name": "Planes"})
        self.assertEqual(post_response.status_code, status.HTTP_403_FORBIDDEN)

        put_response = self.client.put(detail_url, {"name": "Airplanes"})
        self.assertEqual(put_response.status_code, status.HTTP_403_FORBIDDEN)

    def testPostPutDeleteAsAdmin(self):
        """Test if unsafe request with admin token successfully create, modify
        and delete new object.
        """
        url = reverse("interest-list")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.supertoken.key)

        post_response = self.client.post(url, {"name": "Planes"})
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        detail_url = reverse("interest-detail", args=(post_response.data["id"],))

        put_response = self.client.put(detail_url, {"name": "Airplanes"})
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

