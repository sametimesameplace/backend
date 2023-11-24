from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.timeplace import models
from apps.user import models as usermodels
from apps.match import models

class TestMatchEndpoints(APITestCase):
    """ Tests for the match endpoints """
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
       
        
        cls.user1_tp2 = models.TimePlace.objects.create(
            user=cls.user1,
            start="2025-12-01T12:00+01:00",
            end="2025-12-01T15:00+01:00",
            latitude=10.123456,
            longitude=10.213456,
            radius=5,
            description="I want to run tests, this is user1_tp2",
        )
       
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
        
        
        cls.user2_tp2 = models.TimePlace.objects.create(
            user=cls.user2,
            start="2025-12-01T13:00+01:00",
            end="2025-12-01T17:00+01:00",
            latitude=10.123456,
            longitude=10.123456,
            radius=10,
            description="I want to run tests, this is user2_tp2",
        )
       
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
        
        cls.user3_tp2 = models.TimePlace.objects.create(
            user=cls.user3,
            start="2025-12-01T13:00+01:00",
            end="2025-12-01T17:00+01:00",
            latitude=10.123456,
            longitude=10.123456,
            radius=10,
            description="I want to run tests, this is user3_tp2",
        )
        
        cls.user1_m1 = models.Match.objects.create(
            timeplace_1 = cls.user1_tp1,
            timeplace_2 = cls.user2_tp1,
        )
        
        cls.user2_m1 = models.Match.objects.create(
            timeplace_1 = cls.user2_tp1,
            timeplace_2 = cls.user1_tp1,
        )
        
        
    def test_user_can_get_own_matches(self):
        url = reverse('match-detail', kwargs={'pk': self.user1.id})
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user1token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_user_cannot_get_foreign_matches(self):
        url = reverse('match-detail', kwargs={'pk': self.user2.id})
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user1token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_superuser_can_get_all_matches(self):
        url = reverse('match-list')
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.supertoken.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_foreign_user_phone_number_is_hidden(self):
        url = reverse('match-detail', kwargs={'pk': self.user1.id})
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user2token.key)
        response = self.client.get(url)
        self.assertEqual(response.data['foreign_phone'], None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_foreign_user_email_is_hidden(self):
        url = reverse('match-detail', kwargs={'pk': self.user1.id})
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user2token.key)
        response = self.client.get(url)
        self.assertEqual(response.data['foreign_email'], None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_chat_accepted_for_users(self):
        url = reverse('match-detail', kwargs={'pk': self.user1.id})
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user2token.key)
        response = self.client.get(url)
        self.assertFalse(response.data['chat_accepted'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)