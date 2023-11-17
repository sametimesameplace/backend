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
        usermodels.UserLanguage.objects.create(
            userprofile = cls.user1profile,
            language = usermodels.Language.objects.get(pk=2),
            level = "Fluent"
        )
        usermodels.UserLanguage.objects.create(
            userprofile = cls.user1profile,
            language = usermodels.Language.objects.get(pk=3),
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
            language = usermodels.Language.objects.get(pk=3),
            level = "Fluent"
        )

        # Create activities and interests
        cls.interest1 = models.Interest.objects.create(name="Cars")
        cls.interest2 = models.Interest.objects.create(name="Animals")
        cls.interest3 = models.Interest.objects.create(name="Museums")
        cls.interest4 = models.Interest.objects.create(name="Planes")

        cls.activity1 = models.Activity.objects.create(name="Carneval")
        cls.activity2 = models.Activity.objects.create(name="Airsoft")
        cls.activity3 = models.Activity.objects.create(name="Football")
        cls.activity4 = models.Activity.objects.create(name="Bars")

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
        cls.user1_tp1.interests.add(cls.interest1.id, cls.interest2.id)
        cls.user1_tp1.activities.add(cls.activity1.id, cls.activity2.id)
        
        cls.user1_tp2 = models.TimePlace.objects.create(
            user=cls.user1,
            start="2025-12-01T12:00+01:00",
            end="2025-12-01T15:00+01:00",
            latitude=10.123456,
            longitude=10.213456,
            radius=5,
            description="I want to run tests, this is user1_tp2",
        )
        cls.user1_tp2.interests.add(cls.interest1.id, cls.interest2.id)
        cls.user1_tp2.activities.add(cls.activity1.id)
        
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
        cls.user2_tp1.interests.add(cls.interest1.id, cls.interest2.id)
        cls.user2_tp1.activities.add(cls.activity1.id)
        
        cls.user2_tp2 = models.TimePlace.objects.create(
            user=cls.user2,
            start="2025-12-01T13:00+01:00",
            end="2025-12-01T17:00+01:00",
            latitude=10.123456,
            longitude=10.123456,
            radius=10,
            description="I want to run tests, this is user2_tp2",
        )
        cls.user2_tp2.interests.add(cls.interest3.id)
        cls.user2_tp2.activities.add(cls.activity1.id, cls.activity2.id)

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
        cls.user3_tp1.interests.add(cls.interest2.id, cls.interest3.id)
        cls.user3_tp1.activities.add(cls.activity1.id)
        
        cls.user3_tp2 = models.TimePlace.objects.create(
            user=cls.user3,
            start="2025-12-01T13:00+01:00",
            end="2025-12-01T17:00+01:00",
            latitude=10.123456,
            longitude=10.123456,
            radius=10,
            description="I want to run tests, this is user3_tp2",
        )
        cls.user3_tp2.interests.add(cls.interest3.id)
        cls.user3_tp2.activities.add(cls.activity2.id)

    def test_user_can_get_own_matches(self):
        """Test if user can get matches for his own timeplaces.
        """
        url = reverse("timeplace-matches", args=(self.user1_tp1.id,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user1token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for result in response.data["results"]:
            print(result["description"])

    def test_user_cant_get_foreign_matches(self):
        """Test if user can get matches for his own timeplaces.
        """
        url = reverse("timeplace-matches", args=(self.user2_tp1.id,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user1token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)