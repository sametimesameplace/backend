from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.timeplace import models
from apps.user.models import User


class TestInterestEndpoints(APITestCase):
    @classmethod
    def setUpTestData(cls):
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

    def test_list_view_returns_correct_format(self):
        """Test if the GET request to the base Interest endpoint returns the 
        expected result.
        """
        url = reverse("interest-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 81)

    def test_unauthenticated_user_unsafe_methods_forbidden(self):
        """Test if unsafe requests to the Interest endpoint without any 
        authorization return 401.
        """
        url = reverse("interest-list")
        detail_url = reverse("interest-detail", args=(4,))

        post_response = self.client.post(url, {"name": "Planes"})
        self.assertEqual(post_response.status_code, status.HTTP_401_UNAUTHORIZED)

        put_response = self.client.put(detail_url, {"name": "Airplanes"})
        self.assertEqual(put_response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_authenticated_user_unsafe_methods_forbidden(self):
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

    def test_superuser_unsafe_methods_successful(self):
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

    def test_list_view_returns_correct_format(self):
        """Test if the GET request to the base Activity endpoint returns the 
        expected result.
        """
        url = reverse("activity-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 86)

    def test_unauthenticated_user_unsafe_methods_forbidden(self):
        """Test if unsafe requests to the Activity endpoint without any 
        authorization return 401.
        """
        url = reverse("activity-list")
        detail_url = reverse("activity-detail", args=(4,))

        post_response = self.client.post(url, {"name": "Go swimming"})
        self.assertEqual(post_response.status_code, status.HTTP_401_UNAUTHORIZED)

        put_response = self.client.put(detail_url, {"name": "Diving"})
        self.assertEqual(put_response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_authenticated_user_unsafe_methods_forbidden(self):
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

    def test_superuser_unsafe_methods_successful(self):
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
            user=cls.user1,
            start="2025-12-01T12:00+01:00",
            end="2025-12-01T15:00+01:00",
            latitude=20.123456,
            longitude=0.123456,
            radius=10,
            description="I want to run tests",
        )
        cls.tp1.interests.add(1, 2)
        cls.tp1.activities.add(1)

        cls.tp2 = models.TimePlace.objects.create(
            user=cls.user1,
            start="2025-12-02T12:00+01:00",
            end="2025-12-02T15:00+01:00",
            latitude=20.123456,
            longitude=0.123456,
            radius=10,
            description="I want to run more tests",
        )
        cls.tp2.interests.add(1)
        cls.tp2.activities.add(1, 2)

        cls.tp3 = models.TimePlace.objects.create(
            user=cls.user2,
            start="2025-12-02T12:00+01:00",
            end="2025-12-02T15:00+01:00",
            latitude=20.123456,
            longitude=0.123456,
            radius=10,
            description="I want to run tests with different users",
        )
        cls.tp3.interests.add(1)
        cls.tp3.activities.add(2)

    def test_unauthenticated_user_forbidden(self):
        """Test if an unauthenticated user can use any method on TimePlace endpoint.
        """
        url = reverse("timeplace-list")
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_401_UNAUTHORIZED)
        post_response = self.client.post(url, {"description":"test"})
        self.assertEqual(post_response.status_code, status.HTTP_401_UNAUTHORIZED)

        url = reverse("timeplace-detail", args=(self.tp1.id,))
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_401_UNAUTHORIZED)
        put_response = self.client.post(url, {"description":"test"})
        self.assertEqual(put_response.status_code, status.HTTP_401_UNAUTHORIZED)
        delete_response = self.client.post(url)
        self.assertEqual(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_list_has_only_own_items(self):
        """Test if an authenticated user can only see it's own timeplaces.
        """
        url = reverse("timeplace-list")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user1token.key)
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data["count"], 2)

    def test_superuser_list_has_all_items(self):
        """Test if a superuser can see the timeplaces of all users.
        """
        url = reverse("timeplace-list")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.supertoken.key)
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data["count"], 3)

    def test_authenticated_user_can_create_timeplace_with_correct_data(self):
        """Test if an authenticated user can create a timeplace with valid data.
        """
        url = reverse("timeplace-list")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user1token.key)
        post_response = self.client.post(url, {
            "start":"2025-12-03T12:00+01:00",
            "end":"2025-12-04T12:00+01:00",
            "latitude":20.123456,
            "longitude":-20.654321,
            "radius":10,
            "description":"We need more tests here!",
            "interests":[1],
            "activities":[1]
        })
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

    def test_timeplace_has_to_be_in_future(self):
        """Test if an authenticated user can create a timeplace in the past.
        """
        url = reverse("timeplace-list")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user1token.key)
        post_response = self.client.post(url, {
            "start":"2020-12-03T12:00+01:00",
            "end":"2025-12-04T12:00+01:00",
            "latitude":20.123456,
            "longitude":-20.654321,
            "radius":10,
            "description":"We need more tests here!",
            "interests":[1],
            "activities":[1]
        })
        self.assertEqual(post_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_timeplace_end_has_to_be_after_start(self):
        """Test if a user can create a timeplace with end before start.
        """
        url = reverse("timeplace-list")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user1token.key)
        post_response = self.client.post(url, {
            "start":"2025-12-03T12:00+01:00",
            "end":"2024-12-04T12:00+01:00",
            "latitude":20.123456,
            "longitude":-20.654321,
            "radius":10,
            "description":"We need more tests here!",
            "interests":[1],
            "activities":[1]
        })
        self.assertEqual(post_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_timeplace_invalid_latitude(self):
        """Test if a user can create a timeplace with invalid latitude.
        """
        url = reverse("timeplace-list")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user1token.key)
        post_response = self.client.post(url, {
            "start":"2020-12-03T12:00+01:00",
            "end":"2025-12-04T12:00+01:00",
            "latitude":120.123456,
            "longitude":-20.654321,
            "radius":10,
            "description":"We need more tests here!",
            "interests":[1],
            "activities":[1]
        })
        self.assertEqual(post_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_timeplace_invalid_longitude(self):
        """Test if a user can create a timeplace with invalid longitude.
        """
        url = reverse("timeplace-list")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user1token.key)
        post_response = self.client.post(url, {
            "start":"2020-12-03T12:00+01:00",
            "end":"2025-12-04T12:00+01:00",
            "latitude":20.123456,
            "longitude":220.654321,
            "radius":10,
            "description":"We need more tests here!",
            "interests":[1],
            "activities":[1]
        })
        self.assertEqual(post_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_modify_own_timeplace(self):
        """Test if a user can modify his own timeplace.
        """
        url = reverse("timeplace-detail", args=(self.tp1.id,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user1token.key)
        put_response = self.client.put(url, {
            "start":"2025-12-01T12:00+01:00",
            "end":"2025-12-01T16:00+01:00",
            "latitude":20.123456,
            "longitude":0.123456,
            "radius":10,
            "description":"I want to run different tests!",
            "interests":[1],
            "activities":[1]
        })
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

    def test_user_can_not_modify_timeplace_of_other_user(self):
        """Test if a user can modify a timeplace of another user.
        """
        url = reverse("timeplace-detail", args=(self.tp1.id,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user2token.key)
        put_response = self.client.put(url, {
            "start":"2025-12-01T12:00+01:00",
            "end":"2025-12-01T16:00+01:00",
            "latitude":20.123456,
            "longitude":0.123456,
            "radius":10,
            "description":"I want to run different tests!",
            "interests":[1],
            "activities":[1]
        })
        self.assertEqual(put_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_view_own_timeplace(self):
        """Test if user can view details of his own timeplaces.
        """
        url = reverse("timeplace-detail", args=(self.tp1.id,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user1token.key)
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_user_can_view_foreign_timeplace(self):
        """Test if user can view details of foreign timeplaces.
        """
        url = reverse("timeplace-detail", args=(self.tp1.id,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user2token.key)
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_superuser_can_view_own_timeplace(self):
        """Test if superuser can view timeplaces.
        """
        url = reverse("timeplace-detail", args=(self.tp1.id,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.supertoken.key)
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_user_can_delete_own_timeplace(self):
        """Test if user can delete his own timeplaces.
        """
        timeplace = models.TimePlace.objects.create(
            user=self.user1,
            start="2025-12-01T12:00+01:00",
            end="2025-12-01T15:00+01:00",
            latitude=20.123456,
            longitude=0.123456,
            radius=10,
            description="I want to delete tests",
        )
        url = reverse("timeplace-detail", args=(timeplace.id,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user1token.key)
        delete_response = self.client.delete(url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_superuser_can_delete_timeplace(self):
        """Test if a superuser can delete timeplaces.
        """
        timeplace = models.TimePlace.objects.create(
            user=self.user1,
            start="2025-12-01T12:00+01:00",
            end="2025-12-01T15:00+01:00",
            latitude=20.123456,
            longitude=0.123456,
            radius=10,
            description="I want to delete tests",
        )
        url = reverse("timeplace-detail", args=(timeplace.id,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.supertoken.key)
        delete_response = self.client.delete(url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
