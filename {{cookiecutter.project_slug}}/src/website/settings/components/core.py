# coding=utf-8
"""
This is are sensible defaults that can be shared between projects.

They are different from django's global_settings but they should
be common enough to be shared between projects.
"""

import logging
import os
import pathlib
import re
import socket

import environ

log = logging.getLogger(__name__)

# Project root folder
BASE_DIR = pathlib.Path(__file__).parents[4]

env = environ.Env()

# This is defined here as a do-nothing function because we can't import
# django.utils.translation -- that module depends on the settings.
# https://docs.djangoproject.com/en/1.9/topics/i18n/translation/#marking-strings-as-no-op
gettext_noop = lambda s: s  # noqa: E731

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', bool, False)
logging.debug("DEBUG: %s", DEBUG)
ENVIRONMENT_NAME = env('ENVIRONMENT_NAME', default='')

SITE_ID = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

INTERNAL_IPS = [
    '127.0.0.1',
]

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '.example.com',
    'vagrant',
]

BASE_DOMAIN = HOSTNAME = socket.gethostname().lower()
if 'ALLOWED_HOSTS' in os.environ and os.environ['ALLOWED_HOSTS'].strip():
    hosts = os.environ['ALLOWED_HOSTS'].split(" ")
    ALLOWED_HOSTS = [host.strip() for host in hosts if host.strip()]

BASE_URL = env('BASE_URL', default="https://" + ALLOWED_HOSTS[0])

SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)

ADMINS = (
    ("Administrator", "{domain} admin <admin@{domain}>".format(domain=BASE_DOMAIN)),
)
if 'ADMINS' in os.environ:
    from email.utils import getaddresses

    admins = os.environ['ADMINS'].split(";")
    addresses = getaddresses(admins)
    ADMINS = [(name, named_email) for ((name, email), named_email) in zip(addresses, admins)]

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default="Help <help@{domain}>".format(domain=BASE_DOMAIN))
HELP_EMAIL = env('HELP_EMAIL', default=DEFAULT_FROM_EMAIL)
ERR_EMAIL = env('ERR_EMAIL', default="errors@{domain}".format(domain=BASE_DOMAIN))
SERVER_EMAIL = env('SERVER_EMAIL', default="Errors <errors@{domain}>".format(domain=BASE_DOMAIN))
EMAIL_SUBJECT_PREFIX = env('EMAIL_SUBJECT_PREFIX', default='[DJANGO] ')

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
)

MIDDLEWARE = (
    # https://docs.djangoproject.com/en/1.10/ref/middleware/#django.middleware.security.SecurityMiddleware,
    # 'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # 'django_babel.middleware.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',  # https://docs.djangoproject.com/en/1.9/topics/i18n/translation/#how-django-discovers-language-preference
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'website.misc.middleware.XHeadersMiddleware',
    'website.misc.context_processors.SystemInfoMiddleware',
)

ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/1.8/topics/templates/#django.template.backends.django.DjangoTemplates
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(BASE_DIR / 'templates'),
            str(BASE_DIR / "templates" / "errors"),
        ],
        # 'APP_DIRS': False, # APP_DIRS=True and loaders are conflicting
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'website.wsgi.application'

FIXTURE_DIRS = [str(BASE_DIR / 'fixtures')]

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if "DATABASE_URL" in os.environ:  # pragma: no cover
    # Enable database config through environment
    DATABASES = {
        'default': env.db(),  # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    }

    if DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
        DATABASES['default']['TEST'] = {'NAME': env("DATABASE_TEST_NAME", default=None)}
        DATABASES['default']['OPTIONS'] = {
            'sslmode': 'require',
        }
else:
    # A fallback default
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            # 'ENGINE': 'django.contrib.gis.db.backends.spatialite',
            'NAME': str(BASE_DIR / 'data' / 'db.dev.sqlite3'),
            'TEST': {
                'NAME': str(BASE_DIR / 'data' / 'db.test.sqlite3'),
            }
        }
    }

# The email backend to use. For possible shortcuts see django.core.mail.
# The default is to use the SMTP backend.
# Third-party backends can be specified by providing a Python path
# to a module that defines an EmailBackend class.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# https://github.com/joke2k/django-environ#email-settings
EMAIL_CONFIG = env.email_url('EMAIL_URL')
vars().update(EMAIL_CONFIG)

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', gettext_noop('English')),
    ('pl', gettext_noop('Polish')),
)
TIME_ZONE = 'Europe/Warsaw'
USE_I18N = True

# https://docs.djangoproject.com/en/1.9/topics/i18n/translation/#how-django-discovers-language-preference
LOCALE_PATHS = [
    str(BASE_DIR / 'locale'),
]

USE_L10N = True
USE_TZ = True

# Python module path where user will place custom format definition.
# The directory where this setting is pointing should contain subdirectories
# named as the locales, containing a formats.py file
# (i.e. "myproject.locale" for myproject/locale/en/formats.py etc. use)
FORMAT_MODULE_PATH = [
    'website.locale',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = BASE_URL + '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = str(BASE_DIR / 'media')
STATIC_ROOT = str(BASE_DIR / 'static')

STATICFILES_DIRS = (
    ('assets', str(BASE_DIR / 'assets')),
    ('vendor', str(BASE_DIR / 'vendor')),
    ('styles', str(BASE_DIR / 'styles')),
)

# The default file storage backend used during the build process
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

IGNORABLE_404_URLS = (
    re.compile(r'\.(php|cgi)$'),
    re.compile(r'^/admin/'),
    re.compile(r'^/phpmyadmin/'),
)

# django-guardian
# http://django-guardian.readthedocs.org/en/v1.2/configuration.html

ANONYMOUS_USER_ID = -1
# AUTH_USER_MODEL = '{{ cookiecutter.package_name }}.CustomUser'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # this is default
)

LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/'

# https://docs.djangoproject.com/en/1.9/ref/settings/#logging
LOGGING = {
    'version': 1,
    # Setting this to True will disable for eg. preexisting Celery loggers
    'disable_existing_loggers': False,
    'formatters': {
        'short': {
            'format': '%(asctime)s %(levelname)-7s %(thread)-5d %(message)s',
            'datefmt': '%H:%M:%S',
        },
        # this may slow down the app a little, due to
        'verbose': {
            'format': '%(asctime)s %(levelname)-7s %(thread)-5d %(name)s %(filename)s:%(lineno)s | %(funcName)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'heroku': {
            'format': '%(levelname)-7s %(thread)-5d %(name)s %(filename)s:%(lineno)s | %(funcName)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },

    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'short',
            'level': 'DEBUG',
        },
        'mail_admins': {
            'level': 'ERROR',
            'email_backend': 'django.core.mail.backends.smtp.EmailBackend',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        # 'file': {
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'formatter': 'verbose',
        #     'backupCount': 3,
        #     'maxBytes': 4194304,  # 4MB
        # },
    },
    'loggers': {
        # This duplicates Sentry functionality
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'INFO',
        },
        'django.security.DisallowedHost': {
            'handlers': [],
            'propagate': False,
        },
        'suds': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'factory.generate': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'factory.containers': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'dinja2': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'environ.environ': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'pil': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'pil.image': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        # 'django.security.DisallowedHost': {
        #     'handlers': [],
        #     'propagate': False,
        # },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    }
}

# Default exception reporter filter class used in case none has been
# specifically assigned to the HttpRequest instance.
DEFAULT_EXCEPTION_REPORTER_FILTER = 'website.debug.SaferExceptionReporterFilter'
