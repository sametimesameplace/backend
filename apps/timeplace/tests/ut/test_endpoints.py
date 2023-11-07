from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.timeplace import models
from apps.user.models import User


class TestInterestEndpoints(APITestCase):
    @classmethod
    def setUpTestData(cls):
        models.Interest.objects.bulk_create(
            [
                models.Interest(name="Cars"),
                models.Interest(name="Animals"),
                models.Interest(name="Museums"),
                models.Interest(name="Bars"),
            ]
        )
        cls.superuser = User.objects.create_superuser(
            username="admin_interest",
            email="admin_interest@stsp.com",
            password="admin@2023",
        )
        cls.supertoken = Token.objects.create(user=cls.superuser)
        cls.user = User.objects.create_user(
            username="user_interest",
            email="user_interest@stsp.com",
            password="user@2023",
        )
        cls.usertoken = Token.objects.create(user=cls.user)

    def testListView(self):
        """Test if the GET request to the base Interest endpoint returns the 
        expected result.
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
        """Test if unsafe requests to the Interest endpoint without any 
        authorization return 401.
        """
        url = reverse("interest-list")
        detail_url = reverse("interest-detail", args=(4,))

        post_response = self.client.post(url, {"name": "Planes"})
        self.assertEqual(post_response.status_code, status.HTTP_401_UNAUTHORIZED)

        put_response = self.client.put(detail_url, {"name": "Airplanes"})
        self.assertEqual(put_response.status_code, status.HTTP_401_UNAUTHORIZED)


    def testPostPutDeleteForbiddenAuthenticatedUser(self):
        """Test if unsafe requests to the Interest endpoint from normal user 
        without admin rights return 403.
        """
        url = reverse("interest-list")
        detail_url = reverse("interest-detail", args=(4,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.usertoken.key)

        post_response = self.client.post(url, {"name": "Planes"})
        self.assertEqual(post_response.status_code, status.HTTP_403_FORBIDDEN)

        put_response = self.client.put(detail_url, {"name": "Airplanes"})
        self.assertEqual(put_response.status_code, status.HTTP_403_FORBIDDEN)

    def testPostPutDeleteAsAdmin(self):
        """Test if unsafe requests to the Interest endpoint with admin token 
        successfully create, modify and delete new object.
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


class TestActivityEndpoints(APITestCase):
    @classmethod
    def setUpTestData(cls):
        models.Activity.objects.bulk_create(
            [
                models.Activity(name="Carneval"),
                models.Activity(name="Airsoft"),
                models.Activity(name="Football"),
                models.Activity(name="Bars"),
            ]
        )
        cls.superuser = User.objects.create_superuser(
            username="admin_activity",
            email="admin_activity@stsp.com",
            password="admin@2023",
        )
        cls.supertoken = Token.objects.create(user=cls.superuser)
        cls.user = User.objects.create_user(
            username="user_activity",
            email="user_activity@stsp.com",
            password="user@2023",
        )
        cls.usertoken = Token.objects.create(user=cls.user)

    def testListView(self):
        """Test if the GET request to the base Activity endpoint returns the 
        expected result.
        """
        url = reverse("activity-list")
        response = self.client.get(url)
        expected_content = {
            "count": 4,
            "next": None,
            "previous": None,
            "results": [
                {"id": 2, "name": "Airsoft"},
                {"id": 4, "name": "Bars"},
                {"id": 1, "name": "Carneval"},
                {"id": 3, "name": "Football"},
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data), expected_content)

    def testPostPutDeleteForbiddenNotAuthenticated(self):
        """Test if unsafe requests to the Activity endpoint without any 
        authorization return 401.
        """
        url = reverse("activity-list")
        detail_url = reverse("activity-detail", args=(4,))

        post_response = self.client.post(url, {"name": "Go swimming"})
        self.assertEqual(post_response.status_code, status.HTTP_401_UNAUTHORIZED)

        put_response = self.client.put(detail_url, {"name": "Diving"})
        self.assertEqual(put_response.status_code, status.HTTP_401_UNAUTHORIZED)


    def testPostPutDeleteForbiddenAuthenticatedUser(self):
        """Test if unsafe requests to the Activity endpoint from normal 
        user without admin rights return 403.
        """
        url = reverse("activity-list")
        detail_url = reverse("activity-detail", args=(4,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.usertoken.key)

        post_response = self.client.post(url, {"name": "Go swimming"})
        self.assertEqual(post_response.status_code, status.HTTP_403_FORBIDDEN)

        put_response = self.client.put(detail_url, {"name": "Diving"})
        self.assertEqual(put_response.status_code, status.HTTP_403_FORBIDDEN)

    def testPostPutDeleteAsAdmin(self):
        """Test if unsafe requests to the Activity endpoint with admin token 
        successfully create, modify and delete new object.
        """
        url = reverse("activity-list")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.supertoken.key)

        post_response = self.client.post(url, {"name": "Go swimming"})
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        detail_url = reverse("activity-detail", args=(post_response.data["id"],))

        put_response = self.client.put(detail_url, {"name": "Diving"})
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)


class TestTimePlaceEndpoints(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create Interest and Activity Objects to use in the TimePlace
        cls.interest1 = models.Interest.objects.create(name="Animals")
        cls.interest2 = models.Interest.objects.create(name="Art")

        cls.activity1 = models.Activity.objects.create(name="Swimming")
        cls.activity2 = models.Activity.objects.create(name="Go Party")
        
        # Create a superuser and two different users including tokens
        cls.superuser = User.objects.create_superuser(
            username="admin_tp",
            email="admin@stsp.com",
            password="admin@2023",
        )
        cls.supertoken = Token.objects.create(user=cls.superuser)
        cls.user1 = User.objects.create_user(
            username="user_1",
            email="user1@stsp.com",
            password="user@2023",
        )
        cls.user1token = Token.objects.create(user=cls.user1)
        cls.user2 = User.objects.create_user(
            username="user_2",
            email="user2@stsp.com",
            password="user@2023",
        )
        cls.user2token = Token.objects.create(user=cls.user2)
        # Create some TimePlace objects for each user
        cls.tp1 = models.TimePlace.objects.create(
            user_id=cls.user1,
            start="2025-12-01T12:00+01:00",
            end="2025-12-01T15:00+01:00",
            latitude=20.123456,
            longitude=0.123456,
            description="I want to run tests",
        )
        cls.tp1.interests.add(cls.interest1.id, cls.interest2.id)
        cls.tp1.activities.add(cls.activity1.id)

    def testUnauthenticatedForbidden(self):
        """Test if an unauthenticated user can use any method on TimePlace endpoint.
        """
        url = reverse("timeplace-list")
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_401_UNAUTHORIZED)
        post_response = self.client.post(url, {"description":"test"})
        self.assertEqual(post_response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        url = reverse("timeplace-detail", args=(self.tp1.id,))
        put_response = self.client.post(url, {"description":"test"})
        self.assertEqual(put_response.status_code, status.HTTP_401_UNAUTHORIZED)
        delete_response = self.client.post(url)
        self.assertEqual(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)

