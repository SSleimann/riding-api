from .base import *
from .base import env

# Base
DEBUG = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default='django-insecure-=0wh8(zoeg%mfah+5)=9-!txqx@cr5o-w3)4w7+=_f*%ke8yux')


ALLOWED_HOSTS = []


INSTALLED_APPS += ['django_extensions']