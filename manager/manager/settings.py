"""
Django settings for manager project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import urllib

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.environ.get("DATA_DIR") or os.path.join(
    os.path.dirname(BASE_DIR), "manager-data"
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "s245*pzp1poz*#_!&$65&ld!f)5de2eshwc*!8w(2#5d&w0b=0"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "manager",
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

ROOT_URLCONF = "manager.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "manager.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(DATA_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/


###############
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "timed-console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "formatters": {
        "verbose": {"format": "{levelname} {asctime} {message}", "style": "{"},
        "simple": {"format": "{levelname} {message}", "style": "{"},
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        },
        "manager": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "DEBUG"),
        },
    },
}

# configure database from env DSN
if os.getenv("DATABASE", ""):
    database = {}
    dsn = urllib.parse.urlparse(os.getenv("DATABASE"))
    if dsn.scheme in ("mariadb", "mysql"):
        database = {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': dsn.path[1:] if dsn.path else None,
            'USER': dsn.username,
            'PASSWORD': dsn.password or '',
            'HOST': dsn.hostname,
            'PORT': str(dsn.port or 3306),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
            }
        }
    elif dsn.scheme.startswith("sqlite"):
        database = {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": dsn.path,
        }
    DATABASES["default"] = database

    MESSAGE_STORAGE = "django.contrib.messages.storage.fallback.FallbackStorage"


MEDIA_ROOT = os.path.join(DATA_DIR, "media")
MEDIA_URL = "/media/"
STATIC_ROOT = os.path.join(DATA_DIR, "static")
STATIC_URL = "/static/"
LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", "stephane@kiwix.org")
# manager admin account's password
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
# manager's token over the API (/!\)
MANAGER_API_USERNAME = os.getenv("MANAGER_API_USERNAME", "manager")
MANAGER_API_KEY = os.getenv("MANAGER_API_KEY", "manager")
# API URL
CARDSHOP_API_URL = os.getenv(
    "CARDSHOP_API_URL", "https://api.cardshop.hotspot.kiwix.org"
)
CARDSHOP_API_URL_EXTERNAL = os.getenv(
    "CARDSHOP_API_URL_EXTERNAL", "https://api.cardshop.hotspot.kiwix.org"
)
# Token for API allowing creation of user accounts
ACCOUNTS_API_TOKEN = os.getenv(
    "ACCOUNTS_API_TOKEN", "dev"
)
# email-sending related (mailgun API)
MAIL_FROM = os.getenv("MAIL_FROM", "cardshop@kiwix.org")
MAILGUN_API_URL = os.getenv("MAILGUN_API_URL",
                            "https://api.mailgun.net/v3/cardshop.hotspot.kiwix.org")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY", "")
# used for sending reset password links in emails
CARDSHOP_PUBLIC_URL = os.getenv("CARDSHOP_PUBLIC_URL",
                                "https://cardshop.hotspot.kiwix.org")
# content download mirror
MIRROR = "http://mirror.download.kiwix.org"
CONTENTS_FILE = os.path.join(BASE_DIR, "contents.json")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(DATA_DIR, "cache"),
        "TIMEOUT": 86400,
        "OPTIONS": {"MAX_ENTRIES": 1000},
    }
}
