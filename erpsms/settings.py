"""
Django settings for erpsms project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_PATH = os.path.dirname(__file__)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^aznd8sb(!%sgw7z%8z^9(((tp(t(rwddk+^b$tneijjezxqco'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites.models.Site',
    'django.contrib.sites',

    # 'social.apps.django_app.default',
    # 'erpproj'
    # 'mce',
    'schools',
    'registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'corsheaders',
    'common',
    'erpsms',
    'api',
    'redis_cache',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'corsheaders.middleware.CorsPostCsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

CORS_ORIGIN_WHITELIST = (
    'madhu.erpforppl.com:8000',
)
CORS_ALLOW_CREDENTIALS = True
#CSRF_COOKIE_NAME = 'madhu'

# Dont Make it as true
#CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'erpsms.urls'

WSGI_APPLICATION = 'wsgi.application'

CORS_ORIGIN_WHITELIST = (
    'madhu.erpsms.com:8000',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME': 'erp',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': 'sqlsql',
        'HOST': 'localhost',
        'PORT': '',
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates"),
    '/path/to/psa_test/registration/templates/',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'erpsms/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
            ],
        },
    },
]

SITE_ID = 3
TEMPLATE_LOADERS = ['django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader']

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

STATIC_URL = "static/"
#STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, "static/"),)
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
ADMIN_MEDIA_PREFIX = '/madhu/madhu/'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = '/signin_login_success/'
AUTH_USER_MODEL = 'registration.CustomUser'
#HOST = "madhu.erpforppl.com:8000"
HOST = "10.80.6.113:8000"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'erp4ppl@gmail.com'
EMAIL_HOST_PASSWORD = 'haihai1818'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'erp4ppl@gmail.com'
domain = "http://madhu.erpforppl.com:8000"
SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
         {'METHOD': 'oauth2',
          'SCOPE': ['email', 'public_profile', 'user_friends'],
          'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
          'FIELDS': [
              'id',
              'email',
              'name',
              'first_name',
              'last_name',
              'verified',
              'locale',
              'timezone',
              'link',
              'gender',
              'updated_time'],
          'EXCHANGE_TOKEN': True,
          'LOCALE_FUNC': 'path.to.callable',
          'VERIFIED_EMAIL': True,
          'VERSION': 'v2.4'},
     'google':
         {'SCOPE': ['profile', 'email'],
          'AUTH_PARAMS': {'access_type': 'online'}}}

ADMINS = (
    ('Madhu sudan', 'erp4ppl@gmail.com')
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_PATH, 'logs/erpsms.log'),
            'formatter': 'verbose'
        },
	'statsfile': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_PATH, 'logs/erpsms_stats.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'erpsms': {
            'handlers': ['file'],
            'level': 'INFO',
        },
	'erpsms_stats':{
        'handlers': ['statsfile'],
            'level': 'INFO',
        },
        'erpsms_debug': {
         'handlers': ['statsfile'],
            'level': 'DEBUG',
	},
        'erpsms_error': {
         'handlers': ['statsfile'],
            'level': 'ERROR',
        },

    }
}

flavor = 'webwww'
REDIS_REMOTE_SUPPORT = False
WEATHER_APP_ID = 'dd970c41e0165fc185f85709d288d77e'
CACHE_DURATION = 900
CACHES = {
'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379:1',
    },
'localcache': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379:1',
        'TIMEOUT': 24*60*60,
        'OPTIONS': {
             'DB': 2
         }
    },
    'remotecache':
    {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION':'redis-17602.us-east-1-4.3.ec2.garantiadata.com:17602'

    },
    }
