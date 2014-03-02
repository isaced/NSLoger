# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')

        now = timezone.now()
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            date_joined=now, last_login=now,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(username,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Member(AbstractBaseUser):
    email = models.EmailField(
        verbose_name=u'邮箱',
        max_length=255,
        unique=True,
    )
    username = models.CharField("用户名", max_length=16, unique=True)

    weibo_id = models.CharField("新浪微博", max_length=30, blank=True)

    blog = models.CharField("个人网站", max_length=200, blank=True)

    location = models.CharField("城市", max_length=10, blank=True)
    profile = models.CharField("个人简介", max_length=140, blank=True)
    avatar = models.CharField("头像", max_length=128, blank=True)


    email_verified = models.BooleanField("邮箱是否验证", default=False)
    date_joined = models.DateTimeField("用户注册时间", default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def is_email_verified(self):
        return self.email_verified

    def get_weibo(self):
        return self.weibo_id

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
