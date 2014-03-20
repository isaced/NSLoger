# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
import urllib, hashlib
from django.contrib.auth import get_user_model

GRAVATAR_URL_PREFIX = getattr(settings, "GRAVATAR_URL_PREFIX",
                                      "http://www.gravatar.com/")
GRAVATAR_DEFAULT_IMAGE = getattr(settings, "GRAVATAR_DEFAULT_IMAGE", "")
GRAVATAR_DEFAULT_RATING = getattr(settings, "GRAVATAR_DEFAULT_RATING", "g")
GRAVATAR_DEFAULT_SIZE = getattr(settings, "GRAVATAR_DEFAULT_SIZE", 80)

User = get_user_model()
register = template.Library()

# ---Qiniu---
import qiniu.rs


def _get_user(user):
    if not isinstance(user, User):
        try:
            user = User.objects.get(username=user)
        except User.DoesNotExist:
            raise Exception("Bad user for gravatar.")
    return user.email


def _get_gravatar_id(email):
    return hashlib.md5(email).hexdigest()


class GravatarUrlNode(template.Node):
    def __init__(self, email):
        self.email = template.Variable(email)

    def render(self, context):
        try:
            email = self.email.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        default = "http://example.com/static/images/defaultavatar.jpg"
        size = 40

        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})

        return gravatar_url

@register.simple_tag
def gravatar_url(parser, token):
    try:
        tag_name, email = token.split_contents()


    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]

    return GravatarUrlNode(email)


@register.simple_tag
def gravatar(user, size=None):
    try:
        if isinstance(user, User):
            return gravatar_url_for_user(user, size)

        return gravatar_url_for_email(user, size)
    except ValueError:
        raise template.TemplateSyntaxError, u"语法错误"


@register.simple_tag
def gravatar_url_for_user(user, size=None):
    if user.avatar and  user.avatar != '':
        img = 'http://nsloger.qiniudn.com/' + user.avatar
        if size == None:
            img = img + '?imageView2/2/w/58'
        else:
            img = img + '?imageView2/2/w/' + str(size)
        return img

    email = _get_user(user)
    return gravatar_url_for_email(email, size)



@register.simple_tag
def gravatar_url_for_email(email, size=None):
    gravatar_url = "%savatar/%s" % (GRAVATAR_URL_PREFIX,
            _get_gravatar_id(email))

    parameters = [p for p in (
        ('d', GRAVATAR_DEFAULT_IMAGE),
        ('s', size or GRAVATAR_DEFAULT_SIZE),
        ('r', GRAVATAR_DEFAULT_RATING),
    ) if p[1]]
    if parameters:
        gravatar_url += '?' + urllib.urlencode(parameters, doseq=True)

    return gravatar_url
