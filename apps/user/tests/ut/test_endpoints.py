from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


from apps.user.models import User, UserProfile, Language


class TestUserEndpoints(APITestCase):
    """
    Tests for the user endpoints.

    """

    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser(
            username="admin",
            email="admin@stsp.com",
            password="admin_2023",
        )
        cls.supertoken = Token.objects.create(user=cls.superuser)

        cls.user = User.objects.create_user(
            username="test_user",
            email="test_user@stsp.com",
            password="test_user_2023",
        )
        cls.usertoken = Token.objects.create(user=cls.user)

        cls.user2 = User.objects.create_user(
            username="test_user2",
            email="test_user2@stsp.com",
            password="test_user2_2023",
        )

        cls.usertoken2 = Token.objects.create(user=cls.user2)

    def test_user_list_authorized(self):
        """Tests that a list of users are returned for admin only"""

        url = reverse("user-list")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.supertoken.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_unauthorized(self):
        """Tests that a user is unauthorized to get a list of users"""

        url = reverse("user-detail", args=(self.user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user(self):
        """Tests that a user can be created"""

        url = reverse("user-list")
        response = self.client.post(
            url,
            data={
                "username": "testuser",
                "password": "testpassword",
                "email": "test@example.com",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_no_username_given(self):
        """Tests that a user cannot be created without a username"""

        url = reverse("user-list")
        response = self.client.post(
            url,
            data={
                "username": "",
                "password": "fred_2023",
                "email": "fred@stsp.com",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_no_password_given(self):
        """Tests that a user cannot be created without a password"""

        url = reverse("user-list")
        response = self.client.post(
            url,
            data={
                "username": "frank",
                "password": "",
                "email": "frank@stsp.com",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_no_email_given(self):
        """Tests that a user cannot be created without an email"""

        url = reverse("user-list")
        response = self.client.post(
            url,
            data={
                "username": "edith",
                "password": "edith_2023",
                "email": "",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_two_users_cannot_have_same_email(self):
        """Tests that two users cannot have the same email"""
        url = reverse("user-list")
        response = self.client.post(
            url,
            data={
                "username": "user1",
                "password": "user1_2023",
                "email": "user1@stsp.com",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            url,
            data={
                "username": "user2",
                "password": "user2_2023",
                "email": "user1@stsp.com",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_two_users_cannot_have_same_username(self):
        """Tests that two users cannot have the same username"""
        url = reverse("user-list")
        response = self.client.post(
            url,
            data={
                "username": "user3",
                "password": "user3_2023",
                "email": "user3@stsp.com",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            url,
            data={
                "username": "user3",
                "password": "user4_2023",
                "email": "user4@stsp.com",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user(self):
        """Tests that a user can only be deleted by the superuser"""

        user_for_deletion = User.objects.create_user(
            username="user1",
            email="user1@stsp.com",
            password="user1_2023",
        )

        usertoken_for_deletion = Token.objects.create(user=user_for_deletion)

        url = reverse("user-detail", args=(self.user.id,))
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + usertoken_for_deletion.key
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = reverse("user-detail", args=(self.user.id,))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.supertoken.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_user(self):
        """Tests that a user can update their own data"""

        user_for_updating = User.objects.create_user(
            username="user2",
            email="user2@stsp.com",
            password="user2_2023",
        )

        usertoken_for_updating = Token.objects.create(user=user_for_updating)

        new_data = {
            "username": "bob",
            "email": "bob@stsp.com",
            "password": "bob_2023",
        }
        url = reverse("user-detail", args=(user_for_updating.id,))
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + usertoken_for_updating.key
        )
        response = self.client.put(url, data=new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserLanguageEndpoints(APITestCase):
    """
    Tests for the UserLanguage endpoints.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
        )

        self.profile = UserProfile.objects.create(
            user=self.user,
            name='Test User',
            hometown='Test Hometown',
            slogan='Test Slogan',
            birthday='1990-01-01',
            gender='M',
            phone='1234567890',
            profile_email='testuser@example.com'
        )

        self.language = Language.objects.create(lang="English")

        self.url_list = reverse("userlanguage-list")
        
    def create_user_language_data(self, level='Fluent'):
        """
        Helper method to create user language data.
        """
        return {
            'userprofile': self.profile.id,
            'language': self.language.id,
            'level': level,
        }

    def assert_status_code(self, response, expected_status):
        """
        Helper method to assert the status code of a response.
        """
        self.assertEqual(response.status_code, expected_status)
    
    def test_create_user_language_authenticated(self):
        """
        Test the creation of a UserLanguage object when the user is authenticated.
        """
        self.client.force_authenticate(user=self.user)

        user_language_data = self.create_user_language_data()

        response = self.client.post(self.url_list, data=user_language_data, format='json')
        self.assert_status_code(response, status.HTTP_201_CREATED)

    def test_create_user_language_unauthenticated(self):
        """
        Test of rejection a UserLanguage creation when the user is unauthenticated.
        """
        user_language_data = self.create_user_language_data()

        response = self.client.post(self.url_list, data=user_language_data, format='json')
        self.assert_status_code(response, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_list_user_languages_authenticated(self):
        """
        Test listing his own UserLanguages when the user is authenticated.
        """
        self.client.force_authenticate(user=self.user)

        user_language_data = self.create_user_language_data()

        response_create = self.client.post(self.url_list, data=user_language_data, format='json')
        self.assert_status_code(response_create, status.HTTP_201_CREATED)

        response_list = self.client.get(self.url_list)
        self.assert_status_code(response_list, status.HTTP_200_OK)

        self.assertEqual(len(response_list.data), 1)
        self.assertEqual(response_list.data[0]['userprofile'], self.profile.id)
        self.assertEqual(response_list.data[0]['language'], 'English')
        self.assertEqual(response_list.data[0]['level'], 'Fluent')

    def test_list_user_languages_unauthenticated(self):
        """
        Test of the rejection of UserLanguages listing if the user is not authenticated.
        """
        response_list = self.client.get(self.url_list)
        self.assertEqual(response_list.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_language_authenticated(self):
        """
        Test that an authenticated user can update the details of their own UserLanguage.
        """
        self.client.force_authenticate(user=self.user)

        user_language_data = self.create_user_language_data()
        
        response_create = self.client.post(self.url_list, data=user_language_data, format='json')
        
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

        user_language_id = response_create.data['id']
        updated_data = {'level': 'Preferred'}
        url_update = reverse("userlanguage-detail", args=[user_language_id])
        response_update = self.client.patch(url_update, data=updated_data, format='json')
        
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response_update.data['level'], 'Preferred')
        
    def test_delete_user_language_authenticated(self):
        """
        Test that an authenticated user can delete their own UserLanguage object. 
        """
        self.client.force_authenticate(user=self.user)

        user_language_data = self.create_user_language_data()
        
        response_create = self.client.post(self.url_list, data=user_language_data, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

        user_language_id = response_create.data['id']
        url_delete = reverse("userlanguage-detail", args=[user_language_id])
        response_delete = self.client.delete(url_delete)
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        
    