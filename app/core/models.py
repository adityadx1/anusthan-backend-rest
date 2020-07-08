from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, userid, firstname, middlename, lastname, phonenumber,
                    emailid, dob, gender, firebaseuserid, password):

        """Creates and saves a user"""

        if not phonenumber:
            raise ValueError('User must provide a Contact Number')
        user = self.model(userid=userid, firstname=firstname,
                          middlename=middlename, lastname=lastname,
                          phonenumber=phonenumber,
                          emailid=self.normalize_email(emailid),
                          dob=dob, gender=gender,
                          firebaseuserid=firebaseuserid)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_super_user(self, userid, firstname, middlename, lastname,
                          phonenumber, emailid, dob, gender, firebaseuserid,
                          password):
        """Creates and saves a super user"""
        user = self.create_user(userid, firstname, middlename, lastname,
                                phonenumber, emailid, dob, gender,
                                firebaseuserid, password)

        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    """Custom user model"""

    userid = models.CharField(max_length=255, unique=True)
    firstname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=15, unique=True)
    emailid = models.EmailField(max_length=255)
    dob = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)
    firebaseuserid = models.TextField()

    objects = UserManager()

    USERNAME_FIELD = 'userid'
