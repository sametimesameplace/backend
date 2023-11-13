# import psycopg as pg
import environ

from .base import *

env = environ.Env()
environ.Env.read_env(str(BASE_DIR / ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("DB_SECRET")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env.str("DB_NAME"),
        "HOST": env.str("DB_HOST"),
        "PORT": env.int("DB_PORT"),
        "USER": env.str("DB_USER"),
        "PASSWORD": env.str("DB_PASSWORD"),
    }
}

# Register drf_spectacular to create the OpenAPI schema
INSTALLED_APPS = [
    *INSTALLED_APPS,
    'drf_spectacular',
]

REST_FRAMEWORK['DEFAULT_SCHEMA_CLASS'] = 'drf_spectacular.openapi.AutoSchema'

SPECTACULAR_SETTINGS = {
    'TITLE': 'SameTimeSamePlace API',
    'DESCRIPTION': 'Find friends for an adventure.',
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': False,
}