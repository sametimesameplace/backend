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
REST_FRAMEWORK['DEFAULT_PAGINATION_CLASS'] = 'rest_framework.pagination.PageNumberPagination'
REST_FRAMEWORK['PAGE_SIZE'] = 50

SPECTACULAR_SETTINGS = {
    'TITLE': 'SameTimeSamePlace API',
    'DESCRIPTION': 'Find friends for an adventure.',
    'VERSION': '0.3.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # Split components into request and response parts where appropriate
    'COMPONENT_SPLIT_REQUEST': True,
    # Aid client generator targets that have trouble with read-only properties.
    'COMPONENT_NO_READ_ONLY_REQUIRED': False,
    # Create separate components for PATCH endpoints (without required list)
    'COMPONENT_SPLIT_PATCH': True,
    # Optional list of servers.
    # Each entry MUST contain "url", MAY contain "description", "variables"
    # e.g. [{'url': 'https://example.com/v1', 'description': 'Text'}, ...]
    'SERVERS': [{'url': 'http://localhost:8000/', 'description': 'Local Dev Server'},],
}

CORS_ALLOW_ALL_ORIGINS = True
