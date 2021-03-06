"""
Django settings for sgpa project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^ha-+9%y41n0!x60_#r84x&5il6twz^uwiy$*q_jrcak%o$xzl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [""]

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'GestiondeUsuarios',
    'GestiondeRolesyPermisos',
    'GestiondeFlujos',
    'GestiondeProyectos',
    'GestiondeSistema',
    'GestiondeUserStories',
    'GestiondeSprints',
    'GestiondeTableroKanban',
    'GestiondeMensajeria',
    'GestiondeBurndownChart',
    'GestiondeReleases',
)
SITE_ID = 1
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sgpa.urls'

WSGI_APPLICATION = 'sgpa.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sgpa',
        'USER': 'postgres',
        'PASSWORD':'postgres',
        'HOST':'localhost',
        'PORT':'5432'
    }
}
UPLOAD_PATH = 'subidos/%Y/%m'
DEFAULT_FILE_STORAGE = 'GestiondeUserStories.storage.DatabaseStorage'
MEDIA_ROOT = '/home/Desarrollo/Desktop/is2project/sgpa/media/'
MEDIA_URL = 'media/'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Asuncion'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]


STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/sgpa/static'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
