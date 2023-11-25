from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.timeplace import models
from apps.user import models as usermodels


class TestInterestEndpoints(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a superuser and three different users including tokens
        cls.superuser = usermodels.User.objects.create_superuser(
            username="admin_tp",
            email="admin@stsp.com",
            password="admin@2023",
        )
        cls.supertoken = Token.objects.create(user=cls.superuser)
        cls.user1 = usermodels.User.objects.create_user(
            username="user_1",
            email="user1@stsp.com",
            password="user@2023",
        )
        cls.user1token = Token.objects.create(user=cls.user1)
        cls.user2 = usermodels.User.objects.create_user(
            username="user_2",
            email="user2@stsp.com",
            password="user@2023",
        )
        cls.user2token = Token.objects.create(user=cls.user2)
        cls.user3 = usermodels.User.objects.create_user(
            username="user_3",
            email="user3@stsp.com",
            password="user@2023",
        )
        cls.user3token = Token.objects.create(user=cls.user3)

        cls.testuser = usermodels.User.objects.create_user(
            username="testuser",
            email="testuser@stsp.com",
            password="user@2023",
        )
        cls.testusertoken = Token.objects.create(user=cls.testuser)

        # Create userprofiles for the three users
        cls.user1profile = usermodels.UserProfile.objects.create(
            user = cls.user1,
            name = "user1",
            hometown = "user1town",
            slogan = "user1slogan",
            birthday = "2001-01-01",
            gender = "D",
            phone = "111111111",
            profile_email = "user1@stsp.com",
        )
        usermodels.UserLanguage.objects.create(
            userprofile = cls.user1profile,
            language = usermodels.Language.objects.get(pk=1),
            level = "Fluent"
        )

        cls.user2profile = usermodels.UserProfile.objects.create(
            user = cls.user2,
            name = "user2",
            hometown = "user2town",
            slogan = "user2slogan",
            birthday = "2002-02-02",
            gender = "D",
            phone = "22222222",
            profile_email = "user2@stsp.com",
        )
        usermodels.UserLanguage.objects.create(
            userprofile = cls.user2profile,
            language = usermodels.Language.objects.get(pk=1),
            level = "Fluent"
        )
        usermodels.UserLanguage.objects.create(
            userprofile = cls.user2profile,
            language = usermodels.Language.objects.get(pk=2),
            level = "Fluent"
        )

        cls.user3profile = usermodels.UserProfile.objects.create(
            user = cls.user3,
            name = "user3",
            hometown = "user3town",
            slogan = "user3slogan",
            birthday = "2003-03-03",
            gender = "D",
            phone = "3333333333",
            profile_email = "user3@stsp.com",
        )
        usermodels.UserLanguage.objects.create(
            userprofile = cls.user3profile,
            language = usermodels.Language.objects.get(pk=1),
            level = "Fluent"
        )

        usermodels.UserLanguage.objects.create(
            userprofile = cls.user3profile,
            language = usermodels.Language.objects.get(pk=2),
            level = "Fluent"
        )
        usermodels.UserLanguage.objects.create(
            userprofile = cls.user3profile,
            language = usermodels.Language.objects.get(pk=3),
            level = "Fluent"
        )

        cls.testuserprofile = usermodels.UserProfile.objects.create(
            user = cls.testuser,
            name = "testuser",
            hometown = "testusertown",
            slogan = "testuserslogan",
            birthday = "2003-03-03",
            gender = "D",
            phone = "123456",
            profile_email = "testuser@stsp.com",
        )

        # Create some timeplaces
        # For user1
        cls.user1_tp1 = models.TimePlace.objects.create(
            user=cls.user1,
            start="2025-12-01T12:00+01:00",
            end="2025-12-01T15:00+01:00",
            latitude=10.123456,
            longitude=10.123456,
            radius=10,
            description="I want to run tests, this is user1_tp1",
        )
        cls.user1_tp1.interests.add(1)
        cls.user1_tp1.activities.add(1)

        cls.user1_tp2 = models.TimePlace.objects.create(
            user=cls.user1,
            start="2025-12-01T12:00+01:00",
            end="2025-12-01T15:00+01:00",
            latitude=10.123456,
            longitude=10.123456,
            radius=10,
            description="I want to run tests, this is user1_tp2",
        )
        cls.user1_tp2.interests.add(1, 2)
        cls.user1_tp2.activities.add(1, 2)

        # For user2
        cls.user2_tp1 = models.TimePlace.objects.create(
            user=cls.user2,
            start="2025-12-01T13:00+01:00",
            end="2025-12-01T17:00+01:00",
            latitude=10.123456,
            longitude=10.123456,
            radius=10,
            description="I want to run tests, this is user2_tp1",
        )
        cls.user2_tp1.interests.add(2)
        cls.user2_tp1.activities.add(2)

        cls.user2_tp2 = models.TimePlace.objects.create(
            user=cls.user2,
            start="2025-12-01T13:00+01:00",
            end="2025-12-01T17:00+01:00",
            latitude=10.123456,
            longitude=10.123456,
            radius=10,
            description="I want to run tests, this is user2_tp2",
        )
        cls.user2_tp2.interests.add(2, 3)
        cls.user2_tp2.activities.add(2, 3)

        # For user3
        cls.user3_tp1 = models.TimePlace.objects.create(
            user=cls.user3,
            start="2025-12-01T13:00+01:00",
            end="2025-12-01T17:00+01:00",
            latitude=10.123456,
            longitude=10.193456,
            radius=10,
            description="I want to run tests, this is user3_tp1",
        )
        cls.user3_tp1.interests.add(3)
        cls.user3_tp1.activities.add(3)

        cls.user3_tp2 = models.TimePlace.objects.create(
            user=cls.user3,
            start="2025-12-01T13:00+01:00",
            end="2025-12-01T17:00+01:00",
            latitude=10.123456,
            longitude=10.193456,
            radius=10,
            description="I want to run tests, this is user3_tp2",
        )
        cls.user3_tp2.interests.add(3, 4)
        cls.user3_tp2.activities.add(3, 4)

    def test_user_can_get_own_matches(self):
        """Test if user can get matches for his own timeplaces.
        """
        url = reverse("timeplace-matches", args=(self.user1_tp1.id,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user1token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_get_foreign_matches(self):
        """Test if user can get matches for his own timeplaces.
        """
        url = reverse("timeplace-matches", args=(self.user2_tp1.id,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user1token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_matches_by_interests(self):
        """Test if matches are returned according to interests
        """
        # Set up all languages and all activities
        testlang1 = usermodels.UserLanguage.objects.create(
            userprofile = self.testuserprofile,
            language = usermodels.Language.objects.get(pk=1),
            level = "Fluent"
        )
        testlang2 = usermodels.UserLanguage.objects.create(
            userprofile = self.testuserprofile,
            language = usermodels.Language.objects.get(pk=2),
            level = "Fluent"
        )
        testlang3 = usermodels.UserLanguage.objects.create(
            userprofile = self.testuserprofile,
            language = usermodels.Language.objects.get(pk=3),
            level = "Fluent"
        )
        test_tp = models.TimePlace.objects.create(
            user=self.testuser,
            start="2025-12-01T12:00+01:00",
            end="2025-12-01T15:00+01:00",
            latitude=10.123456,
            longitude=10.123456,
            radius=10,
            description="I want to test interestmatching",
        )
        test_tp.activities.add(1, 2, 3, 4)
        url = reverse("timeplace-matches", args=(test_tp.id,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.testusertoken.key)
        # Add unused interest to verify no matches
        test_tp.interests.add(5)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
        # Only add one interest to check if matches work
        test_tp.interests.add(1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        # Test if matching with multiple interests works
        test_tp.interests.add(3)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 5)
        # Delete TimePlace and languages used for this test
        testlang1.delete()
        testlang2.delete()
        testlang3.delete()
        test_tp.delete()

    def test_get_matches_by_activities(self):
        """Test if matches are returned according to interests
        """
        # Set up all languages and all interests
        testlang1 = usermodels.UserLanguage.objects.create(
            userprofile = self.testuserprofile,
            language = usermodels.Language.objects.get(pk=1),
            level = "Fluent"
        )
        testlang2 = usermodels.UserLanguage.objects.create(
            userprofile = self.testuserprofile,
            language = usermodels.Language.objects.get(pk=2),
            level = "Fluent"
        )
        testlang3 = usermodels.UserLanguage.objects.create(
            userprofile = self.testuserprofile,
            language = usermodels.Language.objects.get(pk=3),
            level = "Fluent"
        )
        test_tp = models.TimePlace.objects.create(
            user=self.testuser,
            start="2025-12-01T12:00+01:00",
            end="2025-12-01T15:00+01:00",
            latitude=10.123456,
            longitude=10.123456,
            radius=10,
            description="I want to test interestmatching",
        )
        test_tp.interests.add(1, 2, 3, 4)
        url = reverse("timeplace-matches", args=(test_tp.id,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.testusertoken.key)
        # Add unused activity to verify no matches
        test_tp.activities.add(5)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
        # Only add one activity to check if matches work
        test_tp.activities.add(1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        # Test if matching with multiple activities works
        test_tp.activities.add(3)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 5)
        # Delete TimePlace and languages used for this test
        testlang1.delete()
        testlang2.delete()
        testlang3.delete()
        test_tp.delete()

    def test_get_matches_by_languages(self):
        """Test if matches are returned according to languages
        """
        # Set up all activities and all interests
        test_tp = models.TimePlace.objects.create(
            user=self.testuser,
            start="2025-12-01T12:00+01:00",
            end="2025-12-01T15:00+01:00",
            latitude=10.123456,
            longitude=10.123456,
            radius=10,
            description="I want to test interestmatching",
        )
        test_tp.interests.add(1, 2, 3, 4)
        test_tp.activities.add(1, 2, 3, 4)
        url = reverse("timeplace-matches", args=(test_tp.id,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.testusertoken.key)
        # Add unused activity to verify no matches
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
        # Only add one language to check if matches work
        testlang1 = usermodels.UserLanguage.objects.create(
            userprofile = self.testuserprofile,
            language = usermodels.Language.objects.get(pk=3),
            level = "Fluent"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        # Test if matching with multiple languages works
        testlang2 = usermodels.UserLanguage.objects.create(
            userprofile = self.testuserprofile,
            language = usermodels.Language.objects.get(pk=1),
            level = "Fluent"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 6)
        # Delete TimePlace and languages used for this test
        testlang1.delete()
        testlang2.delete()
        test_tp.delete()

    def test_get_matches_by_coordinates(self):
        """Test if matches are returned according to coordinates and radius
        """
        # Set up timeplace with small radius and small radius
        test_tp = models.TimePlace.objects.create(
            user=self.testuser,
            start="2025-12-01T12:00+01:00",
            end="2025-12-01T15:00+01:00",
            latitude=10.123456,
            longitude=10.173456,
            radius=1,
            description="I want to test interestmatching",
        )
        # Set up all activities and all interests
        test_tp.interests.add(1, 2, 3, 4)
        test_tp.activities.add(1, 2, 3, 4)
        testlang1 = usermodels.UserLanguage.objects.create(
            userprofile = self.testuserprofile,
            language = usermodels.Language.objects.get(pk=1),
            level = "Fluent"
        )
        url = reverse("timeplace-matches", args=(test_tp.id,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.testusertoken.key)
        # With Radius 1, no matches should be found
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
        # With Radius 4, 2 matches should be found
        test_tp.radius = 4
        test_tp.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        # With Radius 10, 6 matches should be found
        test_tp.radius = 10
        test_tp.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 6)
        # Delete TimePlace and languages used for this test
        testlang1.delete()
        test_tp.delete()
