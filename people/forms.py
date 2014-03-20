# -*- coding: utf-8 -*-

from django import forms
from people.models import Member
from django.core.validators import RegexValidator, URLValidator
import re


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", min_length=4, max_length=16,
                               required=True,)
    password = forms.CharField(label="密码", min_length=6, max_length=30, widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(label="重复密码", min_length=6, max_length=30, widget=forms.PasswordInput(), required=True)
    email = forms.EmailField(label="邮箱", max_length=255, required=True)

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("两次密码不相同")

        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username").strip()
        if not re.match(r"^[a-zA-Z0-9_.]+$", username):
            raise forms.ValidationError(u"用户名只支持字母、数字、下划线")
            
        if username[:1] == '_':
            raise forms.ValidationError(u"用户名不能以下划线打头")

        try:
            Member._default_manager.get(username=username)
        except Member.DoesNotExist:
            return username

        raise forms.ValidationError(u"用户名 %s 已经存在" % username)

    def clean_email(self):
        email = self.cleaned_data.get("email").strip()

        try:
            Member._default_manager.get(email=email)
        except Member.DoesNotExist:
            return email

        raise forms.ValidationError(u"邮箱 %s 已经存在" % email)


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名",
                               required=True,)
    password = forms.CharField(label="密码", widget=forms.PasswordInput(), required=True)

    def clean_username(self):
        username = self.cleaned_data.get("username").strip()
        username_not_exist = True
        email_not_exits = True
        try:
            Member._default_manager.get(username=username)
        except Member.DoesNotExist:
            username_not_exist = False
        try:
            Member._default_manager.get(email=username)
        except Member.DoesNotExist:
            email_not_exits = False

        print email_not_exits, username_not_exist

        if username_not_exist or email_not_exits:
            return username

        raise forms.ValidationError("用户名或邮箱不存在")


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(label="邮箱", required=True, max_length=255,
                             widget=forms.TextInput(attrs={
                                 'class':'disabled form-control',
                                 }))
    blog = forms.CharField(label="博客", max_length=128, required=False,
                           validators=[URLValidator],
                           widget=forms.URLInput(attrs={'class':'form-control'}))
    location = forms.CharField(label="城市", max_length=10,required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    weibo_id = forms.CharField(label="新浪微博", max_length=30,required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    profile = forms.CharField(label="个人简介", max_length=140, required=False,
                              widget=forms.Textarea(attrs={'class':'form-control'}))
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        user = kwargs.pop('instance',None)
        self.new_email = user.email


    class Meta:
        model = Member
        fileds = ('email', 'blog', 'location', 'weibo_id', 'profile')
        exclude = ('is_active', "is_admin", "password", "last_login",
                   "date_joined", "email_verified", "username", "avatar",
                   "au", "last_ip", "comment_num", "topic_num")


    def clean_email(self):
        cleaned_data = super(ProfileForm, self).clean()

        email = cleaned_data.get("email").strip()

        try:
            user = Member.objects.get(email=email)
        except (Member.DoesNotExist, ValueError):
            return email
        else:
            if user.email == self.new_email:
                return email
            else:
                raise forms.ValidationError(u"邮箱 %s 已经存在" % email)

    def clean_weibo_id(self):
        weibo = self.cleaned_data.get("weibo_id").strip()
        if weibo.startswith('@'):
            weibo = weibo[1:]

        return weibo


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label="原密码", widget=forms.PasswordInput(attrs={'class':'form-control'}), required=True)
    password = forms.CharField(label="新密码", min_length=6, max_length=30, widget=forms.PasswordInput(attrs={'class':'form-control'}), required=True)
    password2 = forms.CharField(label="重复密码", min_length=6, max_length=30, widget=forms.PasswordInput(attrs={'class':'form-control'}), required=True)

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("两次密码不相同")

        return password2
