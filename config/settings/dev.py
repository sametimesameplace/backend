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

# set drf_spectacular servers to localhost for dev
SPECTACULAR_SETTINGS['SERVERS'] = [
    {'url': 'http://localhost:8000/', 'description': 'Local Dev Server'},]

# allow all origins for CORS to make swagger work for dev
CORS_ALLOW_ALL_ORIGINS = True
