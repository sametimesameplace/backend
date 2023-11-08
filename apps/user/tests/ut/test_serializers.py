from django.test import TestCase

from apps.user.models import User
# from apps.user.models import Language, UserProfile, UserLanguage
from apps.user.serializers import UserModelSerializer


class BaseUserModelTest(TestCase):
    """ Defines common setup and testing logic for user login-related tests """
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@example.com",
        }

    def _perform_user_test(self, serializer_data, expected_data):
        """  helper method that takes serializer_data (data to be serialized), and expected_data (expected values) as parameters """
        
        serializer = UserModelSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, expected_data["username"])
        self.assertEqual(user.email, expected_data["email"])
        self.assertNotEqual(user.password, expected_data["password"])

class UserModelSerializerTest(BaseUserModelTest):
    """ Tests the serialization of user data with a username  an email-based username"""
    
    def test_user_model_serializer_with_username(self):
        self._perform_user_test(self.user_data, self.user_data)

    def test_user_model_serializer_with_email(self):
        email_data = {
            "username": "testuser2",
            "password": "testpassword2",
            "email": "test2@example.com",
        }
        self._perform_user_test(email_data, email_data)

class UserModelDeserializerTest(BaseUserModelTest):
    """ Tests the deserialization of user data with a username an email-based username"""
    
    def setUp(self):
        super().setUp()
        self.serializer = UserModelSerializer(data=self.user_data)
        self.assertTrue(self.serializer.is_valid())
        self.user_instance = self.serializer.save()

    def test_user_deserialization(self):
            """ test the deserialization with unique user data """
            unique_user_data = {
            "username": "testuser_unique",
            "password": "testpassword",
            "email": "test@example.com",
        }
            self._perform_user_test(unique_user_data, unique_user_data)

    def test_user_deserialization_with_email_as_username(self):
        """ test the deserialization with email-based username data """
        email_as_username_data = {
            "username": "test@example.com",
            "password": "testpassword",
            "email": "test@example.com",
        }
        self._perform_user_test(email_as_username_data, email_as_username_data)



