from django.urls import reverse
from django.test import TestCase
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.user import models
from apps.user.models import User, UserProfile
from apps.user.serializers import UserModelSerializer, UserProfileCreateSerializer, UserProfileUpdateSerializer, UserProfileRetrieveSerializer


class TestUserModelSerializer(TestCase):
    def test_valid_user_model_serializer(self):
        valid_data = {

        }
        serializer = UserProfileCreateSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())


class TestUserProfileSerializer(TestCase):
    def test_valid_serializer_data_create(self):
        # Valid data that can be used for serialization

        valid_data = {

            "user": 42,
            "name": "Alice",
            "hometown": "Paris",
            "slogan": "Carpe diem",
            "birthday": "1990-01-01",
            "gender": "F",
            "phone": "+33291020404",
            "profile_email": "alice@email.com",
            "languages": [1, 2],
        }

        serializer = UserProfileCreateSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer_data_update(self):
        valid_data = {

            "user": 42,
            "name": "Alice",
            "hometown": "Berlin",
            "slogan": "Memento mori",
            "gender": "F",
            "phone": "+33291020888",
            "profile_email": "alice.new@email.com",
            "languages": [1, 2, 3, 4],
        }

        serializer = UserProfileUpdateSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_valid_serializer_data_retrieve(self):

        valid_data = {

            "user": 42,
            "name": "Alice",
            "hometown": "Paris",
            "slogan": "Carpe diem",
            "age": "33",
            "gender": "F",
            "phone": "+33291020404",
            "profile_email": "alice@email.com",
            "languages": [1, 2, 3, 4],
        }

        serializer = UserProfileRetrieveSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
