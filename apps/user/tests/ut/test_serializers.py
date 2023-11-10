import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.user.models import User
from apps.user.models import Language, UserProfile, UserLanguage
from apps.user.serializers import UserModelSerializer, LanguageModelSerializer, UserLanguageModelSerializer, UserProfileModelSerializer


class BaseUserModelTest(TestCase):
    """ Defines common setup and testing logic for user login-related tests """

    def setUp(self):
        self.user_data = {
            "username": "testuser1",
            "password": "testpassword",
            "email": "test@example.com",
        }

    def _perform_user_test(self, serializer_data, expected_data):
        """helper method that takes serializer_data (data to be serialized), and expected_data (expected values) as parameters"""

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
    """ Tests the deserialization of user data with a username an email-based username
    """

    def test_user_deserialization(self):
        """ test the deserialization with unique user data
        """
        unique_user_data = {
            "username": "testuser_unique",
            "password": "testpassword",
            "email": "test1@example.com",
        }
        self._perform_user_test(unique_user_data, unique_user_data)

    def test_user_deserialization_with_email_as_username(self):
        """ test the deserialization with email-based username data
        """
        email_as_username_data = {
            "username": "test2@example.com",
            "password": "testpassword",
            "email": "test2@example.com",
        }
        self._perform_user_test(email_as_username_data, email_as_username_data)


class LanguageModelSerializerTest(TestCase):
    """ Test for valid and invalid language data.
    """
    def setUp(self):
        self.valid_language_data = {"lang": "اردو (Urdu)"}
        self.invalid_language_data = {"lang": ""}

    def test_valid_language_model_serializer(self):
        serializer = LanguageModelSerializer(data=self.valid_language_data)
        self.assertTrue(serializer.is_valid())

        language = serializer.save()

        self.assertIsInstance(language, Language)
        self.assertEqual(language.lang, self.valid_language_data["lang"])

    def test_invalid_language_model_serializer(self):
        serializer = LanguageModelSerializer(data=self.invalid_language_data)
        self.assertFalse(serializer.is_valid())


class UserProfileModelSerializerGetAgeTest(TestCase):
    
    def test_get_age(self):
        """Test for the right age calculation in the get_age method.
        """
        birthdate = datetime.date(1990, 1, 1)
        user_profile = UserProfile(birthday=birthdate)

        serializer = UserProfileModelSerializer(instance=user_profile)

        age = serializer.get_age(user_profile)

        today = datetime.date.today()
        expected_age = today.year - birthdate.year - \
            ((today.month, today.day) < (birthdate.month, birthdate.day))

        self.assertEqual(age, expected_age)


class UserProfileModelSerializerTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):

        cls.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )

        cls.language = Language.objects.create(lang='English')

        cls.user_profile = UserProfile.objects.create(
            user=cls.user,
            name='Test Name',
            hometown='Test Hometown',
            slogan='Test Slogan',
            birthday='1990-01-01',
            gender='M',
            phone='1234567890',
            profile_email='test@example.com',

        )
        # birthday needs to be processed to be a date object, not a string
        cls.user_profile = UserProfile.objects.get(pk=cls.user_profile.id)

        cls.user_language = UserLanguage.objects.create(
            userprofile=cls.user_profile,
            language=cls.language,
            level='Fluent'
        )

    def test_serialization(self):
        """ test that the serialization of a user profile produces the expected output
        """
        serializer = UserProfileModelSerializer(instance=self.user_profile)
        serialized_data = serializer.data

        self.assertEqual(serialized_data['name'], 'Test Name')
        self.assertEqual(serialized_data['hometown'], 'Test Hometown')
        self.assertEqual(serialized_data['slogan'], 'Test Slogan')
        self.assertEqual(serialized_data['birthday'], '1990-01-01')
        self.assertEqual(serialized_data['gender'], 'M')
        self.assertEqual(serialized_data['phone'], '1234567890')
        self.assertEqual(serialized_data['profile_email'], 'test@example.com')
