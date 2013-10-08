import os
import sys
import json
from django.conf import global_settings

SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.abspath(os.path.dirname(SETTINGS_DIR))
 
try:
    with open('/home/dotcloud/environment.json') as f:
        env = json.load(f)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'default',
                'USER': env['DOTCLOUD_DB_SQL_LOGIN'],
                'PASSWORD': env['DOTCLOUD_DB_SQL_PASSWORD'],
                'HOST': env['DOTCLOUD_DB_SQL_HOST'],
                'PORT': int(env['DOTCLOUD_DB_SQL_PORT']),
            },
            'udd': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'udd',
                'USER': 'public-udd-mirror',
                'PASSWORD': 'public-udd-mirror',
                'HOST': 'public-udd-mirror.xvm.mit.edu',
                'PORT': 465,
            }
        }
        log_file_dir = '/var/log/supervisor/greenhouse.log'
        DEBUG = True
        TEMPLATE_DEBUG = DEBUG
        DEBUG_MIDDLEWARE_CLASSES = ()
        DEBUG_APPS = ()
except IOError:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'default',
            'USER': 'daveeloo',
            'PASSWORD': 'password',
            'HOST': '',
            'PORT': '',
        },
        'udd': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'udd',
            'USER': 'public-udd-mirror',
            'PASSWORD': 'public-udd-mirror',
            'HOST': 'public-udd-mirror.xvm.mit.edu',
            'PORT': 465,
        }
    }
    log_file_dir = os.path.join(PROJECT_PATH, 'logs/')
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    DEBUG_MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_APPS = ('debug_toolbar',)
    INTERNAL_IPS = ('127.0.0.1',)

if 'test' in sys.argv or 'test_coverage' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'default',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        },
    }

STATIC_SERVE = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/home/dotcloud/data/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/dotcloud/volatile/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '!^@y642$s-)!5e#z36i@ed5*o__1&amp;oq+)c=ov81e1r(bit^)$*'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'example_settings.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'example_settings.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.comments',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'greenhouse',
    'south',
    'django_openid_auth',
)
INSTALLED_APPS += DEBUG_APPS
MIDDLEWARE_CLASSES += DEBUG_MIDDLEWARE_CLASSES

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'greenhouse.context_processor.user_context',
)

# OpenID and Launchpad intigration
AUTHENTICATION_BACKENDS = (
    'django_openid_auth.auth.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

OPENID_CREATE_USERS = True
LOGIN_URL = '/openid/login/'
LOGIN_REDIRECT_URL = '/'
OPENID_SSO_SERVER_URL = 'server-endpoint-url'
OPENID_SSO_SERVER_URL = 'https://login.ubuntu.com/'
OPENID_LAUNCHPAD_STAFF_TEAMS = ['ubuntu-developer-advisory-team']
OPENID_LAUNCHPAD_TEAMS_MAPPING_AUTO = True
OPENID_UPDATE_DETAILS_FROM_SREG = True
OPENID_USE_AS_ADMIN_LOGIN = True
OPENID_FOLLOW_RENAMES = True
OPENID_STRICT_USERNAMES = True
# Currently we allow DAT, CC, DMB to see everything. This could
# be extended at some point to give other teams (say Ubuntu Members)
# the ability to see anonymous data.
#
# Whn this is changed './manage.py create_user_groups'
# must be run.
ALLOWED_LAUNCHPAD_TEAMS = ['ubuntu-developer-advisory-team',
                           'developer-membership-board',
                           'communitycouncil',
                           'canonical-community',
                           'greenhouse', ]

SOUTH_TESTS_MIGRATE = False

AUTH_PROFILE_MODULE = "greenhouse.UserProfile"

DATABASE_ROUTERS = ['greenhouse.router.DBRouter']

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s \
                       %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': log_file_dir,
            'maxBytes': 1024*1024*25,  # 25 MB
            'backupCount': 5,
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        # Catch All Logger -- Captures any other logging
        '': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}
