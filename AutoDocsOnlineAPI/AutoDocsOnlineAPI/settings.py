from os import getenv as env
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG') == 'True'

ALLOWED_HOSTS = env('ALLOWED_HOSTS', '127.0.0.1:8000,localhost').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'djoser',
    'api.apps.ApiConfig',
    'users.apps.UsersConfig',
    'documents.apps.DocumentsConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AutoDocsOnlineAPI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'AutoDocsOnlineAPI.wsgi.application'

CORS_ORIGIN_WHITELIST = env(
    'CORS_ORIGIN_WHITELIST', 'http://localhost:3001'
).split(',')


# Use sql in debug mode and postgers in production(on server)

DATABASE = env("DATABASE", 'POSTGRES')

DATABASES = {
    'default': {
        'SQLITE': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
        'POSTGRES': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('POSTGRES_DB', 'django'),
            'USER': env('POSTGRES_USER', 'django'),
            'PASSWORD': env('POSTGRES_PASSWORD', ''),
            'HOST': env('POSTGRES_HOST', ''),
            'PORT': env('POSTGRES_PORT', 5432)
        }
    }[DATABASE]
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 100

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Api settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
}


SWAGGER_SETTINGS = {
    'sheme': 'bearer',
    "bearerFormat": 'JWT',
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}


# Auth settings
AUTH_USER_MODEL = 'users.User'

CONFIRM_CODE_LENGHT = 6

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = env('TIME_ZONE', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = env('USE_TZ') == 'True'


# Static/meta settings
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'collected_static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'backend_static' / 'static' / 'media'


# Email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
DEAFAULT_FROM_EMAIL = env("EMAIL_HOST_USER")
SERVER_EMAIL = env("EMAIL_HOST_USER")

# Email letters settings
FROM_EMAIL = "AutoDocsOnline Support"
USER_SEND_CONFIRM_CODE_EMAIL_SUBJECT = "Registration on AutoDocsOnline"
USER_SEND_CONFIRM_CODE_EMAIL_MESSAGE = "Your confirm code: {code}"


# Models settings
SHORT_END = "..."

# User
USER_USERNAME_MAX_LENGTH = 150
USER_USERNAME_MIN_LENGTH = 4

USER_EMAIL_MAX_LENGTH = 100

USER_FIRST_NAME_MAX_LENGTH = 25
USER_FIRST_NAME_MIN_LENGTH = 3

USER_LAST_NAME_MAX_LENGTH = 25
USER_LAST_NAME_MIN_LENGTH = 3

# Template
TEMPLATE_TITLE_MAX_LENGTH = 100
TEMPLATE_TITLE_MIN_LENGTH = 3

TEMPLATE_NAME_IN_DOCUMENT_PREFIX = '{{'
TEMPLATE_NAME_IN_DOCUMENT_POSTFIX = '}}'
TEMPLATE_NAME_IN_DOCUMENT_MAX_LENGTH = 30
TEMPLATE_NAME_IN_DOCUMENT_MIN_LENGTH = (
    3
    + len(TEMPLATE_NAME_IN_DOCUMENT_POSTFIX)
    + len(TEMPLATE_NAME_IN_DOCUMENT_PREFIX)
)

TEMPLATE_DESCRIPTION_MAX_LENGTH = 500

USER_TEMPLATE_VALUE_VALUE_MAX_LENGTH = 300
USER_TEMPLATE_VALUE_SHORT_VALUE_LENGTH = 30


# Document
DOCUMENT_TITLE_MAX_LENGTH = 150
DOCUMENT_DESCRIPTION_MAX_LENGTH = 500
DOCUMENTS_FOLDER_NAME = "documents"
DOCUMENT_TITLE_SHORT_LENGTH = 20

# DockumentPackage
DOCKUMENT_PACKAGE_TITLE_MAX_LENGTH = 100
DOCKUMENT_PACKAGE_TITLE_MIN_LENGTH = 3
