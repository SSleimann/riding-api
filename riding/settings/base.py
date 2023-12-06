import os
import environ

from pathlib import Path

from django.urls import reverse_lazy

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# debug
DEBUG = env.bool("DJANGO_DEBUG", default=False)

# secret
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-=0wh8(zoeg%mfah+5)=9-!txqx@cr5o-w3)4w7+=_f*%ke8yux",
)

# wsgi
WSGI_APPLICATION = "riding.wsgi.application"

# urls
ROOT_URLCONF = "riding.urls"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# apps
BASE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
]

LOCAL_APPS = ["apps.users.apps.UsersConfig", "apps.drivers.apps.DriversConfig"]

THIRD_APPS = [
    "rest_framework",
    "django_filters",
    "oauth2_provider",
    "drf_spectacular",
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS

# databases
DATABASES = {
    "default": env.db_url("DATABASE_URL", default="sqlite:///db.db"),
}

# passwords hashers
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# middlewares
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# templates
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# logger

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} {levelname} {module} {name} {funcName} {lineno} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "riding": {
            "level": "INFO",
            "handlers": ["console"],
        }
    },
}

# usermodel
AUTH_USER_MODEL = "users.User"

# Celery Configuration Options
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
CELERY_RESULT_EXTENDED = True
CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_TASK_SEND_SENT_EVENT = True
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 5 * 60
CELERY_ACCEPT_CONTENT = ["json", "msgpack", "yaml"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_BEAT_SCHEDULE = {
    "clear_expired_tokens": {
        "task": "apps.users.tasks.clear_expired_tokens",
        "schedule": 7200,
    },
}

# JWT
JWT_SECRET_KEY = env(
    "JWT_SECRET_KEY",
    default="749feb426abce5bd7095a6249d7d3e16948ff2db0d3b8b629cd52105eeb6a0ee",
)

# smtp
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# rest framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

OAUTH2_PROVIDER = {
    "OAUTH2_VALIDATOR_CLASS": "apps.users.oauth2_validator.CustomOAuth2Validator"
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Riding API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "CONTACT": {"email": "sleimanjose23@hotmail.com"},
    "OAUTH2_FLOWS": ["password"],
    "OAUTH2_AUTHORIZATION_URL": reverse_lazy("oauth2_provider:authorize"),
    "OAUTH2_TOKEN_URL": reverse_lazy("oauth2_provider:token"),
    "OAUTH2_REFRESH_URL": reverse_lazy("oauth2_provider:token"),
    "SERVE_PUBLIC": False,
    'SWAGGER_UI_SETTINGS': {
        "deepLinking": True,
        'persistAuthorization': True,
    },
}