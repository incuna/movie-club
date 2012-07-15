# Django settings for movie_club project.
import os

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
from django.core.urlresolvers import reverse_lazy
import dj_database_url
from S3 import CallingFormat


DIRNAME = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

DEBUG = bool(os.environ.get('DEBUG', False))
DEVELOPMENT_SITE = bool(os.environ.get('DEVELOPMENT_SITE', False))

DATABASES = {'default': dj_database_url.config(default='postgres://localhost/movie_club')}

ADMINS = (('Admin', 'bugs@incuna.com'),)
MANAGERS = ADMINS
ADMIN_EMAILS = zip(*ADMINS)[1]
SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'info@incuna.com'
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

TIME_ZONE = 'UTC'
USE_L10N = True  # Locale
USE_TZ = True

LANGUAGE_CODE = 'en-GB'
USE_I18N = False  # Internationalization

# AWS
if not DEBUG:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    S3_URL = 'http://{0}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)

# Static
MEDIA_ROOT = os.path.join(DIRNAME, 'client_media')
MEDIA_URL = '/client_media/'
STATIC_ROOT = os.path.join(DIRNAME, 'static_media')
STATIC_URL = '/static/' if DEBUG else S3_URL
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_DEBUG = DEBUG
TEMPLATE_DIRS = (os.path.join(DIRNAME, 'templates'))
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.google.GoogleOAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = reverse_lazy('login')

AUTH_PROFILE_MODULE = 'profiles.Profile'
ROOT_URLCONF = 'movie_club.urls'
SECRET_KEY = '+%euhby2%5^@%dv@u7$_s9gpz77a-va++eg&amp;7&amp;jpp7+5+9h^8y'
SITE_ID = 1
WSGI_APPLICATION = 'movie_club.wsgi.application'

INSTALLED_APPS = (
    # Project Apps
    'movie_club',

    # Libraries
    'crispy_forms',
    'south',
    'debug_toolbar',
    'django_extensions',
    'gunicorn',
    'raven.contrib.django',
    'social_auth',

    # Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)

SENTRY_DSN = 'http://1e7382d8d03d471eb384c7752f0a30ee:6fe16fb822554283b11d14d0af7bd9fd@sentry.incuna.com/20'
SENTRY_TESTING = DEBUG
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
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Debug Toolbar
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
INTERNAL_IPS = ('127.0.0.1',)

# Movie Club
TMDB_IMAGE_URL = 'http://cf2.imgobject.com/t/p/'

# Social auth
GOOGLE_OAUTH2_CLIENT_ID = os.environ['GOOGLE_OAUTH2_CLIENT_ID']
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ['GOOGLE_OAUTH2_CLIENT_SECRET']
GOOGLE_WHITE_LISTED_DOMAINS = ['incuna.com']
SOCIAL_AUTH_USER_MODEL = 'auth.User'
