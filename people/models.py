# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone
from django.conf import settings
import hashlib
import random
import string

SALT = getattr(settings, "EMAIL_TOKEN_SALT",
                         "NSLoger")

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

    au = models.IntegerField("用户活跃度", default=0)
    last_ip = models.IPAddressField("上次访问IP", default="0.0.0.0")


    email_verified = models.BooleanField("邮箱是否验证", default=False)
    date_joined = models.DateTimeField("用户注册时间", default=timezone.now)
    topic_num = models.IntegerField("帖子数", default=0)
    comment_num = models.IntegerField("评论数", default=0)

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

    def calculate_au(self):
        """
        计算活跃度
        公式：Topic * 5 + Comment * 1
        """
        self.au = self.topic_num * 5 + self.comment_num * 1
        return self.au


class Follower(models.Model):
    """
    用户的关系表
    B is the follower of A
    B 是 A 的关注者
    A 被 B 关注
    """
    user_a = models.ForeignKey(Member, related_name="user_a")
    user_b = models.ForeignKey(Member, related_name="user_b")
    date_followed = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user_a', 'user_b')


    def __unicode__(self):
        return "%s following %s" % (self.user_a, self.user_b)


class EmailVerified(models.Model):
    user = models.OneToOneField(Member, related_name="user")
    token = models.CharField("Email 验证 token", max_length=32, default=None)
    timestamp = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return "%s@%s" % (self.user, self.token)

    def generate_token(self):
        year = self.timestamp.year
        month = self.timestamp.month
        day = self.timestamp.day
        date = "%s-%s-%s" % (year, month, day)
        token = hashlib.md5(str(self.user.id)+self.user.username+self.ran_str()+date).hexdigest()
        return token

    def ran_str(self):
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        return salt + SALT


class FindPass(models.Model):
    user = models.OneToOneField(Member, verbose_name="用户")
    token = models.CharField(max_length=32, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return "%s@%s" % (self.user, self.token)

    def generate_token(self):
        year = self.timestamp.year
        month = self.timestamp.month
        day = self.timestamp.day
        date = "%s-%s-%s" % (year, month, day)
        token = hashlib.md5(str(self.user.id)+self.user.username+self.ran_str()+date).hexdigest()
        return token

    def ran_str(self):
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        return salt + SALT
