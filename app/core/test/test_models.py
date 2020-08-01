from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from django.utils import timezone


def sample_user(
    firstname='TestFirstName',
    middlename="TestMiddleName",
    lastname="TestLastName",
    phonenumber='1234567890',
    emailid="test@testmail.com",
    dob="1900-01-01",
    gender="Not Disclosed",
    firebaseuserid="qwerty123456asdfgh0987"
                ):
    """Create a sample user"""
    return get_user_model().objects.create_user(firstname, middlename,
                                                lastname, phonenumber,
                                                emailid, dob, gender,
                                                firebaseuserid)


class ModelTests(TestCase):

    def test_create_user_with_details_successful(self):
        """Test creating a new user with all details is successful"""
        firstname = 'TestFirstName'
        middlename = 'TestMiddleName'
        lastname = 'TestLastName'
        phonenumber = '1234567890'
        emailid = 'test@testmail.com'
        dob = '1900-01-01'
        gender = 'Not Disclosed'
        firebaseuserid = 'qwerty123456asdfgh0987'
        user = get_user_model().objects.create_user(
            firstname=firstname,
            middlename=middlename,
            lastname=lastname,
            phonenumber=phonenumber,
            emailid=emailid,
            dob=dob,
            gender=gender,
            firebaseuserid=firebaseuserid
        )
        self.assertEqual(user.firstname, firstname)
        self.assertEqual(user.middlename, middlename)
        self.assertEqual(user.lastname, lastname)
        self.assertEqual(user.phonenumber, phonenumber)
        self.assertEqual(user.emailid, emailid)
        self.assertEqual(user.dob, dob)
        self.assertEqual(user.gender, gender)
        self.assertEqual(user.firebaseuserid, firebaseuserid)

    def test_new_user_email_normalized(self):
        """Test that the email for a new user is normalized"""
        emailid = 'test@TESTMAIL.com'
        user = get_user_model().objects.create_user(
            'TestFirstName',
            'TestMiddleName',
            'TestLastName',
            '1234567890',
            emailid,
            '1900-01-01',
            'Not Disclosed',
            'qwerty123456asdfgh0987'
        )

        self.assertEqual(user.emailid, emailid.lower())

    def test_new_user_invalid_phonenumber(self):
        """Test that a value error is raised when no phonenumber is provided"""
        phonenumber = None
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                'TestFirstName',
                'TestMiddleName',
                'TestLastName',
                phonenumber,
                'test@testmail.com',
                '1900-01-01',
                'Not Disclosed',
                'qwerty123456asdfgh0987'
            )

    def test_create_super_user(self):
        """Test creating a super user"""
        user = get_user_model().objects.create_superuser(
            'TestFirstName',
            'TestMiddleName',
            'TestLastName',
            '1234567890',
            'test@testmail.com',
            '1900-01-01',
            'Not Disclosed',
            'qwerty123456asdfgh0987'
        )
        self.assertTrue(user.is_superuser)
    #
    # def test_event_str(self):
    #     """Test the event string representation"""
    #     event = models.Event.objects.create(
    #         eventtype='MR',
    #         eventdatetimestamp=timezone.now(),
    #         eventdescription='Big fat wedding',
    #         venueid='001',
    #         user=sample_user()
    #     )
    #     self.assertEqual(str(event), str(event.eventid))
    #
    # def test_event_creation_without_desc(self):
    #     """Test that event can be created without a description"""
    #     event = models.Event.objects.create(
    #         eventtype='MR',
    #         eventdatetimestamp=timezone.now(),
    #         venueid='001',
    #         user=sample_user()
    #     )
    #     self.assertEqual(str(event), str(event.eventid))
    #
    # def test_event_creation_without_datetime(self):
    #     """Test that event can be created without a date time stamp"""
    #     event = models.Event.objects.create(
    #         eventtype='MR',
    #         eventdescription='Big fat wedding',
    #         venueid='001',
    #         user=sample_user()
    #     )
    #     self.assertEqual(str(event), str(event.eventid))
    #
    # def test_event_creation_without_venue(self):
    #     """Test the event string representation"""
    #     event = models.Event.objects.create(
    #         eventtype='MR',
    #         eventdatetimestamp=timezone.now(),
    #         eventdescription='Big fat wedding',
    #         user=sample_user()
    #     )
    #     self.assertEqual(str(event), str(event.eventid))
