from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_details_successful(self):
        """Test creating a new user with all details is successful"""
        userid = 'testUserId'
        firstname = 'TestFirstName'
        middlename = "TestMiddleName"
        lastname = "TestLastName"
        phonenumber = '1234567890'
        emailid = "test@testmail.com"
        dob = "01/01/1900"
        gender = "Not Disclosed"
        firebaseuserid = "qwerty123456asdfgh0987"
        password = 'testpassword'
        user = get_user_model().objects.create_user(
            userid=userid,
            firstname=firstname,
            middlename=middlename,
            lastname=lastname,
            phonenumber=phonenumber,
            emailid=emailid,
            dob=dob,
            gender=gender,
            firebaseuserid=firebaseuserid,
            password=password
        )
        self.assertEqual(user.userid, userid)
        self.assertEqual(user.firstname, firstname)
        self.assertEqual(user.middlename, middlename)
        self.assertEqual(user.lastname, lastname)
        self.assertEqual(user.phonenumber, phonenumber)
        self.assertEqual(user.emailid, emailid)
        self.assertEqual(user.dob, dob)
        self.assertEqual(user.gender, gender)
        self.assertEqual(user.firebaseuserid, firebaseuserid)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test that the email for a new user is normalized"""
        emailid = 'test@TESTMAIL.com'
        user = get_user_model().objects.create_user(
            'testUserId',
            'TestFirstName',
            'TestMiddleName',
            'TestLastName',
            '1234567890',
            emailid,
            '01/01/1900',
            'Not Disclosed',
            'qwerty123456asdfgh0987',
            'testpassword'
        )

        self.assertEqual(user.emailid, emailid.lower())

    def test_new_user_invalid_phonenumber(self):
        """Test that a value error is raised when no phonenumber is provided"""
        phonenumber = None
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                'testUserId',
                'TestFirstName',
                'TestMiddleName',
                'TestLastName',
                phonenumber,
                'test@testmail.com',
                '01/01/1900',
                'Not Disclosed',
                'qwerty123456asdfgh0987',
                'testpassword'
            )

    def test_create_super_user(self):
        """Test creating a super user"""
        user = get_user_model().objects.create_super_user(
            'testUserId',
            'TestFirstName',
            'TestMiddleName',
            'TestLastName',
            '1234567890',
            'test@testmail.com',
            '01/01/1900',
            'Not Disclosed',
            'qwerty123456asdfgh0987',
            'testpassword'
        )
        self.assertTrue(user.is_superuser)
