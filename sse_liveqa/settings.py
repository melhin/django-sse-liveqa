"""
Django settings for sse_liveqa project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from urllib.parse import urlsplit, urlunsplit

from configurations.values import BooleanValue, ListValue, Value

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.abspath(os.path.dirname(__name__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = Value(environ_prefix=None, environ_name="SECRET_KEY")


DEBUG = BooleanValue(environ_prefix=None, environ_name="DEBUG", default=False)

ALLOWED_HOSTS = ListValue(
    environ_prefix=None,
    environ_name="ALLOWED_HOSTS",
    default=["*"],
    converter=str.strip,
)


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "qa",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sse_liveqa.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "sse_liveqa.wsgi.application"
ASGI_APPLICATION = "sse_liveqa.asgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR + "/static",
]
STATIC_ROOT = BASE_DIR + "/staticfiles"
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REDIS_PASSWORD = Value(environ_prefix=None, environ_name="REDIS_PASSWORD", default=None)
REDIS_DSN = Value(
    environ_prefix=None, environ_name="REDIS_DSN", default="redis://redis:6379/1"
)

if REDIS_DSN:
    if REDIS_PASSWORD:
        scheme, host, path = urlsplit(REDIS_DSN)[:3]
        REDIS_DSN = urlunsplit([scheme, f":{REDIS_PASSWORD}@{host}", path, "", ""])

NOTIFICATION_POST = "notification.post"
LOG_LEVEL = Value(
    environ_prefix=None, environ_name="LOG_LEVEL", default="DEBUG" if DEBUG else "INFO"
)
LOG_JSON = BooleanValue(environ_prefix=None, environ_name="LOG_JSON", default=True)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["console"],
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "text",
            "stream": "ext://sys.stdout",
        }
    },
    "formatters": {
        "text": {
            "format": "%(asctime)s %(levelname)s %(thread)d %(process)d %(module)s %(name)s %(message)s",
        },
    },
}

BASIC_USER = Value(environ_prefix=None, environ_name="BASIC_USER", default="User")
BASIC_PASSWORD = Value(
    environ_prefix=None, environ_name="BASIC_PASSWORD", default="Password"
)
