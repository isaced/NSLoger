# -*- coding: utf-8 -*-

"""
Django settings for      project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*7&kl0hzdgy6+8jlsg=05l__!7$ayjxlnh+3ae4zeujc#k=dq)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'bbs',      # 帖子相关
    'people',   # 用户相关
    'sites',    # 酷站
    'page',     # 页面
    'south',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'people.views.MyMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'NSLoger.urls'

WSGI_APPLICATION = 'NSLoger.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',

        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Chongqing'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

AUTH_USER_MODEL = 'people.Member'

LOGIN_URL = '/login'

# Email setting
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.ym.163.com"
#EMAIL_PORT = 994
#EMAIL_USE_TLS = True
EMAIL_HOST_USER = "no-reply@nsloger.com"
EMAIL_HOST_PASSWORD = ""
EMAIL_TOKEN_SALT = "NSLoger"

# Constant Define
NUM_TOPICS_PER_PAGE = 20
NUM_COMMENT_PER_PAGE = 30

# Gravtar Define
GRAVATAR_DEFAULT_IMAGE = ""
#GRAVATAR_URL_PREFIX = "https://secure.gravatar.com/"
GRAVATAR_URL_PREFIX = "http://gravatar.duoshuo.com/"
GRAVATAR_DEFAULT_RATING = "g"
GRAVATAR_DEFAULT_SIZE = "48"

SITE_URL = "http://localhost:8080"
