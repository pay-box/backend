"""
Django settings for pay project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

BASE_URL = os.environ['BASE_URL']

TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_NAME = os.environ.get('DB_NAME', 'pay')
DB_PORT = int(os.environ.get('DB_PORT', '5432'))

MEDIAROOT = os.environ.get('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))
STATICROOT = os.environ.get('STATIC_ROOT', os.path.join(BASE_DIR, 'static'))

CELERY_RESULT_SERIALIZER = 'json'
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_ACKS_LATE = True

CELERY_BROKER_URL = 'redis://%s:%s/1' % (REDIS_HOST, REDIS_PORT)


DEFAULT_LOCALE = os.environ.get("LOCALE", 'en_US.utf8')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5bsqd8j0c$(rz_c&0j88p8!)*k80@uyqcvv53nese+rpwj3+vb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (os.environ.get('DEBUG_VALUE', None) == 'TRUE')
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'drf_yasg',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'colorfield',
    'user',
    'gateway',
    'transaction',
    'form'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pay.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "assets"),
]

WSGI_APPLICATION = 'pay.wsgi.application'


AUTH_USER_MODEL = 'user.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (

    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    )
}


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': DB_NAME,
        'USER': 'postgres',
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": CELERY_BROKER_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '%s/media/' % (BASE_URL)
MEDIA_RELATIVE_URL = '/media/'

STATIC_ROOT = STATICROOT

MEDIA_ROOT = (
    MEDIAROOT
)

GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}


CACHE_TEMP_TRANSACTION_TTL = 60 * 30
