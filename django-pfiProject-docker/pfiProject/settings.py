"""
Django settings for pfiProject project.

Generated by 'django-admin startproject' using Django 2.0.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

import textwrap
import json # auth0
from six.moves.urllib import request # auth0

from cryptography.x509 import load_pem_x509_certificate # auth0
from cryptography.hazmat.backends import default_backend # auth0

from dotenv import load_dotenv

load_dotenv('pfiProject/.env')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', True)

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth', # auth0
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # new
    'django.contrib.gis', # new

    'meas_web', #new

    'corsheaders', # new
    'rest_framework', # new
    'rest_framework_gis', # new
    'rest_framework_jwt', # auth0

    'drf', # new
]

REST_FRAMEWORK = {
   'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
   ],
   'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
   ],
   'DEFAULT_FILTER_BACKENDS': [
        #'rest_framework_filters.backends.ComplexFilterBackend',
        'url_filter.integrations.drf.DjangoFilterBackend',
   ],
   'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.IsAuthenticated', # auth0
        'rest_framework.permissions.IsAuthenticatedOrReadOnly', # auth0
   ],
   'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication', # auth0
   ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # auth0
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#new
try:
    from .secrets.secrets import *
    from .secrets import secrets
except ImportError:
    pass

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
        'https://'+secrets.PUBHOST_URL,
)

ROOT_URLCONF = 'pfiProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth', # auth0
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pfiProject.wsgi.application'

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.postgresql',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('POSTGRES_DB', 'postgres'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.getenv('POSTGRES_HOST', '127.0.0.1'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', # auth0
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', # auth0
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', # auth0
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', # auth0
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

#new
STATIC_ROOT = os.path.join(BASE_DIR, 'static') #new

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend", # check
    "django.contrib.auth.backends.RemoteUserBackend", # check
    "allauth.account.auth_backends.AuthenticationBackend", # check
)

AUTH0_DOMAIN = secrets.AUTH0_DOMAIN # auth0
API_IDENTIFIER = secrets.API_IDENTIFIER # auth0
PUBLIC_KEY = None # auth0
JWT_ISSUER = None # auth0

# If AUTH0_DOMAIN is defined, load the jwks.json
if AUTH0_DOMAIN: # auth0
    jsonurl = request.urlopen('https://' + AUTH0_DOMAIN + '/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    cert = '-----BEGIN CERTIFICATE-----\n' + jwks['keys'][0]['x5c'][0] + '\n-----END CERTIFICATE-----'
    certificate = load_pem_x509_certificate(cert.encode('utf-8'), default_backend())
    PUBLIC_KEY = certificate.public_key()
    JWT_ISSUER = 'https://' + AUTH0_DOMAIN + '/'


JWT_AUTH = { # auth0
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': 'meas_web.user.jwt_get_username_from_payload_handler',
    'JWT_PUBLIC_KEY': PUBLIC_KEY,
    'JWT_ALGORITHM': 'RS256',
    'JWT_AUDIENCE': API_IDENTIFIER,
    'JWT_ISSUER': JWT_ISSUER,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

# Default Django logging is WARNINGS+ to console
# so visible via docker-compose logs django
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'WARNING'),
        },
    },
}

