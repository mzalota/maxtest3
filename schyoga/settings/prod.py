# Django settings for maxtest3 project.

import sys
sys.path.append('/opt/bitnami/apps/django/lib/usr-lib/')

# Django settings for maxtest3 project.
from schyoga.settings.base import *

import os
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '../../','templates').replace('\\','/'),)

#DEBUG = True
#TEMPLATE_DEBUG = DEBUG

DEBUG = False
#TEMPLATE_DEBUG = False

MANAGERS = ADMINS

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
#STATIC_ROOT = "/opt/bitnami/apps/django/lib/python2.7/site-packages/django/contrib/admin/static"

STATIC_ROOT = "/opt/bitnami/apps/django/django_projects/schyoga/staticfiles"

STATICFILES_DIRS = (
    "/opt/bitnami/apps/django/django_projects/schyoga/schyoga/static",
)

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['204.236.217.131', 'www.scheduleyoga.com', '107.20.155.154']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'schyoga4',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': '4floacient',
        'HOST': '127.0.0.1',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',                      # Set to empty string for default.
    }
}

DATABASE_OPTIONS = {
    'unix_socket' : '/opt/bitnami/mysql/tmp/mysql.sock',
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':  "/tmp/django.log",
            'maxBytes': 5000000,
            'backupCount': 8,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django': {
            'handlers': ['logfile'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['mail_admins', 'logfile'],
            'level': 'DEBUG', #ERROR
            'propagate': True,
        },
        'maxtest3': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
