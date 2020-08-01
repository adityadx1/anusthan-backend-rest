from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, firstname, middlename, lastname, phonenumber,
                    emailid, dob, gender, firebaseuserid,
                    **extra_fields):
        """Creates and saves a user"""
        if not phonenumber:
            raise ValueError('User must provide a Contact Number')
        if not firebaseuserid:
            raise ValueError('FireBase ID was not supplied')
        user = self.model(firstname=firstname,
                          middlename=middlename, lastname=lastname,
                          phonenumber=phonenumber,
                          emailid=self.normalize_email(emailid),
                          dob=dob, gender=gender,
                          firebaseuserid=firebaseuserid,
                          **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, firstname, middlename, lastname,
                         phonenumber, emailid, dob, gender, firebaseuserid):
        """Creates and saves a super user"""
        user = self.create_user(firstname, middlename, lastname,
                                phonenumber, emailid, dob, gender,
                                firebaseuserid)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    """Custom user model"""
    userid = models.BigAutoField(primary_key=True)
    firstname = models.CharField(max_length=255, blank=True)
    middlename = models.CharField(max_length=255, blank=True)
    lastname = models.CharField(max_length=255, blank=True)
    phonenumber = models.CharField(max_length=10, unique=True)
    emailid = models.EmailField(max_length=255, blank=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=20, blank=True)
    firebaseuserid = models.TextField(unique=True, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['firstname', 'middlename', 'lastname', 'phonenumber',
                       'emailid', 'dob', 'gender']
    objects = UserManager()

    USERNAME_FIELD = 'firebaseuserid'


# class Event(models.Model):
#     """Event model to be used"""
#     eventid = models.AutoField(primary_key=True)
#     MARRIAGE = 'MR'
#     ANNIVERSARY = 'AN'
#     BIRTHDAY = 'BD'
#     ENGAGEMENT = 'EG'
#     HOUSEWARMING = 'HW'
#     EVENT_TYPE_CHOICES = [
#         (MARRIAGE, 'Marriage'),
#         (ANNIVERSARY, 'Anniversary'),
#         (BIRTHDAY, 'Birthday'),
#         (ENGAGEMENT, 'Engagment'),
#         (HOUSEWARMING, 'Housewarming'),
#     ]
#     eventtype = models.CharField(
#         max_length=2,
#         choices=EVENT_TYPE_CHOICES,
#         null=False
#     )
#     eventdatetimestamp = models.DateTimeField(null=True)
#     eventdescription = models.TextField(null=True)
#     venueid = models.IntegerField(null=True)
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE
#     )
#
#     def __str__(self):
#         return str(self.eventid)
