"""
Django settings for graphsearch project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, 'graphsearch')

# BASE_URL = "http://ayushchd.com/graphsearch/"
# NEO4J_SERVER = "http://neo4jcloud.sb01.stations.graphenedb.com:24789/db/data/"
# NEO4J_USERNAME = "neo4j_cloud"
# NEO4J_PASSWORD = "Y159eqIqWHzTnMPkZffA"
# NEO4J_CONN_STR = "http://neo4j_cloud:Y159eqIqWHzTnMPkZffA@neo4jcloud.sb01.stations.graphenedb.com:24789/db/data/"

BASE_URL = "http://127.0.0.1:8000/"
NEO4J_SERVER = "http://localhost:7474/db/data/"
NEO4J_USERNAME = ""
NEO4J_PASSWORD = ""
NEO4J_CONN_STR = "http://localhost:7474/db/data/"

TWITTER_APP_KEY = 'E8ds3rRK7g7jQEacYaaginqBb'
TWITTER_APP_SECRET = 'QMNUSJlLpGFeePfRfXEIcxwskEdpLXVmzjAVMSF0BksNv6zO6o'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r*tm*t9(#znpwg&(l_7%=ghwc*-a*dbs$-3xebabo%sp7l+r&a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'customtags'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'graphsearch.urls'

WSGI_APPLICATION = 'graphsearch.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates/')
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, "static/"),
    # '/var/www/static/',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # "graphsearch.context_processor.getSettings",
)

SESSION_ENGINE = 'django.contrib.sessions.backends.file'