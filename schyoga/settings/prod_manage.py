from schyoga.settings.prod import *

#Define different log file destination where "manage.py" will write

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
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':  "/tmp/django_manage.log",
            'maxBytes': 50000,
            'backupCount': 2,
            #'formatter': 'standard',
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
