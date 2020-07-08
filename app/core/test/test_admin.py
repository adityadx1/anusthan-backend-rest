from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class adminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_super_user(
            userid='adminUserId',
            firstname='AdminFirstName',
            middlename="AdminMiddleName",
            lastname="AdminLastName",
            phonenumber='1234567890',
            emailid="admin@testmail.com",
            dob="01/01/1900",
            gender="Not Disclosed",
            firebaseuserid="qwerty123456asdfgh0987",
            password='adminpassword'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            userid='testUserId',
            firstname='TestFirstName',
            middlename="TestMiddleName",
            lastname="TestLastName",
            phonenumber='1234567891',
            emailid="test@testmail.com",
            dob="01/01/1900",
            gender="Not Disclosed",
            firebaseuserid="qwerty123456asdfgh0987",
            password='testpassword'
        )

    def test_users_listed(self):
        """Test that all users are listed"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.userid)
        self.assertContains(res, self.user.firstname)
        self.assertContains(res, self.user.middlename)
        self.assertContains(res, self.user.lastname)
        self.assertContains(res, self.user.phonenumber)
        self.assertContains(res, self.user.emailid)
        self.assertContains(res, self.user.dob)
        self.assertContains(res, self.user.gender)
        self.assertContains(res, self.user.firebaseuserid)

    def test_user_change_page(self):
        """Test that user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that user create page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
