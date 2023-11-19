from .base import *
from .base import env

# Base
DEBUG = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]


INSTALLED_APPS += ["django_extensions"]
