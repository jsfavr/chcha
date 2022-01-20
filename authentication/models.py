from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from datetime import timedelta


# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, phone=None, name=None, role_id=None):
        if username is None:
            raise TypeError('Username cannot be blank')
        if email is None:
            raise TypeError('Username cannot be blank')

        user = self.model(username=username, email=self.normalize_email(email), phone=phone, name=name, role_id=role_id)
        user.set_password(password)
        user.save()

        return user

    def create_admin_user(self, username, email, password=None, phone=None, name=None, role_id=None):
        if password is None:
            raise TypeError('Password Cannot be blank')
        user = self.model(username=username, email=self.normalize_email(email), phone=phone, name=name, role_id=role_id)
        # user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.password = make_password(user.password)
        user.register()
        return user

    def create_vendor(self, username, email, password=None, phone=None, name=None, role_id=None):
        if username is None:
            raise TypeError('Username cannot be blank')
        if email is None:
            raise TypeError('Username cannot be blank')

        user = self.model(username=username, email=self.normalize_email(email), phone=phone, name=name, role_id=role_id)
        user.set_password(password)
        user.save()
        return user

    def create_pos(self, username, email, password=None, phone=None, name=None, role_id=None):
        if username is None:
            raise TypeError('Username cannot be blank')
        if email is None:
            raise TypeError('Username cannot be blank')

        user = self.model(username=username, email=self.normalize_email(email), phone=phone, name=name, role_id=role_id)
        user.set_password(password)
        user.save()
        return user

    def create_delboy(self, username, email, password=None, phone=None, name=None, role_id=None):
        if username is None:
            raise TypeError('Username cannot be blank')
        if email is None:
            raise TypeError('Username cannot be blank')

        user = self.model(username=username, email=self.normalize_email(email), phone=phone, name=name, role_id=role_id)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=45, null=True)
    phone = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role_id = models.IntegerField(default=1)
    status = models.BooleanField(default=True)
    refer_code = models.CharField(max_length=45, null=True)
    referUserID=models.IntegerField(default=0)
    subscriptionStatus=models.BooleanField(default=False)
    profile_image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    # def __str__(self):
    #     return self

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        token = refresh.access_token
        token.set_exp(lifetime=timedelta(days=10))
        return {
            "refresh": str(refresh),
            "access": str(token)
        }
