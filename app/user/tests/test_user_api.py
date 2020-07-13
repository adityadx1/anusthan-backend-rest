from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the user API public"""

    def setup(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test whether user has been successfully created on valid payload"""
        payload = {
            'userid': 'testUserId',
            'firstname': 'TestFirstName',
            'middlename': "TestMiddleName",
            'lastname': "TestLastName",
            'phonenumber': '1234567890',
            'emailid': "test@testmail.com",
            'dob': "01/01/1900",
            'gender': "Not Disclosed",
            'firebaseuserid': "qwerty123456asdfgh0987",
            'password': 'testpassword'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(
            user.check_password(payload['password'])
        )
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating user which already exists fails"""
        payload = {
            'userid': 'testUserId',
            'firstname': 'TestFirstName',
            'middlename': "TestMiddleName",
            'lastname': "TestLastName",
            'phonenumber': '1234567890',
            'emailid': "test@testmail.com",
            'dob': "01/01/1900",
            'gender': "Not Disclosed",
            'firebaseuserid': "qwerty123456asdfgh0987",
            'password': 'testpassword'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be greater than 8 characters"""
        payload = {
            'userid': 'testUserId',
            'firstname': 'TestFirstName',
            'middlename': "TestMiddleName",
            'lastname': "TestLastName",
            'phonenumber': '1234567890',
            'emailid': "test@testmail.com",
            'dob': "01/01/1900",
            'gender': "Not Disclosed",
            'firebaseuserid': "qwerty123456asdfgh0987",
            'password': 'pw'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            userid=payload['userid']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that the token is created for the user"""
        payload = {
            'userid': 'testUserId',
            'firstname': 'TestFirstName',
            'middlename': "TestMiddleName",
            'lastname': "TestLastName",
            'phonenumber': '1234567890',
            'emailid': "test@testmail.com",
            'dob': "01/01/1900",
            'gender': "Not Disclosed",
            'firebaseuserid': "qwerty123456asdfgh0987",
            'password': 'testpassword'
        }
        create_user(**payload)
        tokenPayload = {
            'userid': 'testUserId',
            'password': 'testpassword'
        }
        res = self.client.post(TOKEN_URL, tokenPayload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(
            userid='testUserId',
            firstname='TestFirstName',
            middlename="TestMiddleName",
            lastname="TestLastName",
            phonenumber='1234567890',
            emailid="test@testmail.com",
            dob="01/01/1900",
            gender="Not Disclosed",
            firebaseuserid="qwerty123456asdfgh0987",
            password='testpassword',
        )
        payload = {
            'userid': 'wrong'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_without_user(self):
        """Test that token is not created if user does not exist"""
        payload = {
            'userid': 'qwerty123456asdfgh0987'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that token is not created if field is missing"""
        payload = {
            'userid': ''
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that users require authentication"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            userid='testUserId',
            firstname='TestFirstName',
            middlename="TestMiddleName",
            lastname="TestLastName",
            phonenumber='1234567890',
            emailid="test@testmail.com",
            dob="01/01/1900",
            gender="Not Disclosed",
            firebaseuserid="qwerty123456asdfgh0987",
            password='testpassword',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['userid'], self.user.userid)
        self.assertEqual(res.data['firebaseuserid'], self.user.firebaseuserid)

    def test_post_me_not_allowed(self):
        """Test that POST requests are not allowed on ME url"""
        res = self.client.post(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user(self):
        """Test updating the user profile for authenticated user"""
        payload = {
            'userid': 'newtestUserId',
            'firstname': 'newTestFirstName',
            'middlename': "newTestMiddleName",
            'lastname': "newTestLastName",
            'phonenumber': 'new1234567890',
            'emailid': "newtest@testmail.com",
            'dob': "01/01/1990",
            'gender': "Disclosed",
            'firebaseuserid': "newqwerty123456asdfgh0987",
            'password': 'newtestpassword'
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.userid, payload['userid'])
        self.assertEqual(self.user.firstname, payload['firstname'])
        self.assertEqual(self.user.middlename, payload['middlename'])
        self.assertEqual(self.user.lastname, payload['lastname'])
        self.assertEqual(self.user.phonenumber, payload['phonenumber'])
        self.assertEqual(self.user.emailid, payload['emailid'])
        self.assertEqual(self.user.dob, payload['dob'])
        self.assertEqual(self.user.gender, payload['gender'])
        self.assertEqual(self.user.firebaseuserid, payload['firebaseuserid'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
