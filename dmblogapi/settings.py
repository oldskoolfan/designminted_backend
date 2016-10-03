"""
Django settings for dmblogapi project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open('/etc/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_json_api',
    'blogwebapp',
    'blogapi',
    'corsheaders',
    'oauth2_provider',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    #'django.middleware.gzip',
)

ROOT_URLCONF = 'dmblogapi.urls'
CORS_ORIGIN_ALLOW_ALL = True

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

REST_FRAMEWORK= {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    #'PAGINATE_BY': 10,
    #'PAGINATE_BY_PARAM': 'page_size',
    #'MAX_PAGINATE_BY': 100,
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    #'DEFAULT_PAGINATION_SERIALIZER_CLASS':
    #    'rest_framework_json_api.pagination.PageNumberPagination',
    #    'rest_framework_ember.pagination.PaginationSerializer',
    'DEFAULT_PARSER_CLASSES': (
        #'rest_framework_json_api.parsers.JSONParser',
        #"rest_framework_json_api.parsers.JsonApiParser",
        'rest_framework_ember.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        #'rest_framework_json_api.renderers.JSONRenderer',
        #"rest_framework_json_api.renderers.JsonApiRenderer",
        'rest_framework_ember.renderers.JSONRenderer',
        #'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
}

REST_EMBER_FORMAT_KEYS = True
REST_EMBER_PLURALIZE_KEYS = True
#JSON_API_FORMAT_KEYS = 'dasherize'
#JSON_API_FORMAT_RELATION_KEYS = 'dasherize'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dmblogapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dmblogapi',
        'USER': 'wwwuser',
        'PASSWORD': 'bad6508333',
        'HOST': 'ubuntudb1',
        'PORT': '3306',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/users/andrew/PycharmProjects/dmblogapi/blogwebapp/static/'

#APPEND_SLASH = True

# email settings
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "harris.1305.autobot@gmail.com"
with open("/etc/email_pass.txt") as f:
    EMAIL_HOST_PASSWORD = f.read().strip()
EMAIL_PORT = 465
EMAIL_USE_SSL = True







