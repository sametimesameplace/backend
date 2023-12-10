from pathlib import Path

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Application definition
DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

CUSTOM_APPS = [
    "apps.user",
    "apps.timeplace",
    "apps.match",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "drf_spectacular",
]

INSTALLED_APPS = [*DEFAULT_APPS, *CUSTOM_APPS, *THIRD_PARTY_APPS]

AUTHENTICATION_BACKENDS = ["apps.user.backends.EmailOrUsernameModelBackend"]

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

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,    
}


WSGI_APPLICATION = "config.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = "static/"
STATICFILES_DIRS = [
    #str(BASE_DIR / "static"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# needed to use the user model from the user app
AUTH_USER_MODEL = "user.User"

# Encrypt Cookies on the client
SESSION_COOKIE_SECURE = True

# Settings for drf_spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": "SameTimeSamePlace API",
    "DESCRIPTION": "Find friends for an adventure.",
    "VERSION": "0.3.1",
    "SERVE_INCLUDE_SCHEMA": False,
    # Split components into request and response parts where appropriate
    "COMPONENT_SPLIT_REQUEST": True,
    # Aid client generator targets that have trouble with read-only properties.
    "COMPONENT_NO_READ_ONLY_REQUIRED": False,
    # Create separate components for PATCH endpoints (without required list)
    "COMPONENT_SPLIT_PATCH": True,
    # Optional list of servers.
    # Each entry MUST contain "url", MAY contain "description", "variables"
    # e.g. [{"url": "https://example.com/v1", "description": "Text"}, ...]
    # "SERVERS": [{"url": "http://localhost:8000/", "description": "Local Dev Server"},],
}
