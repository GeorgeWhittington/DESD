"""
Django settings for smartcare_django project.

Generated by "django-admin startproject" using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "foo")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(" ")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "knox",
    "corsheaders",
    "django_filters",
    "smartcare_appointments.apps.SmartcareAppointmentsConfig",
    "smartcare_auth.apps.SmartcareAuthConfig",
    "smartcare_finance.apps.SmartcareFinanceConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "smartcare_django.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "smartcare_django.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "8080"),
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

AUTH_USER_MODEL = "smartcare_auth.User"

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "knox.auth.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication"
        ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

AUTHENTICATION_BACKENDS = ["smartcare_auth.authentication.UsernameOrEmailBackend"]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "https://localhost:8000",
    "http://0.0.0.0:8000",
    "https://0.0.0.0:8000",
    "http://localhost:5173",
    "https://localhost:5173",
    "http://0.0.0.0:5173",
    "https://0.0.0.0:5173"
]

EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.environ.get("EMAIL_PORT")

SLOTS = {
    0: {"start": "08:00", "end": "08:15", "label": "Early Morning"},
    1: {"start": "08:20", "end": "08:35", "label": "Early Morning"},
    2: {"start": "08:40", "end": "08:55", "label": "Early Morning"},
    3: {"start": "09:00", "end": "09:15", "label": "Early Morning"},
    4: {"start": "09:20", "end": "09:35", "label": "Early Morning"},
    5: {"start": "09:40", "end": "09:55", "label": "Early Morning"},
    6: {"start": "10:00", "end": "10:15", "label": "Late Morning"},
    7: {"start": "10:20", "end": "10:35", "label": "Late Morning"},
    8: {"start": "10:40", "end": "10:55", "label": "Late Morning"},
    9: {"start": "11:00", "end": "11:15", "label": "Late Morning"},
    10: {"start": "11:20", "end": "11:35", "label": "Late Morning"},
    11: {"start": "11:40", "end": "11:55", "label": "Late Morning"},
    12: {"start": "12:00", "end": "12:15", "label": "Late Morning"},
    13: {"start": "12:20", "end": "12:35", "label": "Early Afternoon"},
    14: {"start": "12:40", "end": "12:55", "label": "Early Afternoon"},
    15: {"start": "13:00", "end": "13:15", "label": "Early Afternoon"},
    16: {"start": "13:20", "end": "13:35", "label": "Early Afternoon"},
    17: {"start": "13:40", "end": "13:55", "label": "Early Afternoon"},
    18: {"start": "14:00", "end": "14:15", "label": "Early Afternoon"},
    19: {"start": "14:20", "end": "14:35", "label": "Early Afternoon"},
    20: {"start": "14:40", "end": "14:55", "label": "Early Afternoon"},
    21: {"start": "15:00", "end": "15:15", "label": "Early Afternoon"},
    22: {"start": "15:20", "end": "15:35", "label": "Early Afternoon"},
    23: {"start": "15:40", "end": "15:55", "label": "Late Afternoon"},
    24: {"start": "16:00", "end": "16:15", "label": "Late Afternoon"},
    25: {"start": "16:20", "end": "16:35", "label": "Late Afternoon"},
    26: {"start": "16:40", "end": "16:55", "label": "Late Afternoon"},
    27: {"start": "17:00", "end": "17:15", "label": "Late Afternoon"},
    28: {"start": "17:20", "end": "17:35", "label": "Late Afternoon"},
    29: {"start": "17:40", "end": "17:55", "label": "Late Afternoon"},
}


DAY_CHOICES = [
    ('Monday', 'Monday'), 
    ('Tuesday', 'Tuesday'), 
    ('Wednesday', 'Wednesday'), 
    ('Thursday', 'Thursday'), 
    ('Friday', 'Friday'), 
    ('Saturday', 'Saturday'), 
    ('Sunday', 'Sunday'),
]

FULL_TIME_WORKING_DAYS = ['Tuesday', 'Wednesday', 'Thursday', 'Saturday', 'Sunday']
PART_TIME_WORKING_DAYS = ['Monday', 'Friday']