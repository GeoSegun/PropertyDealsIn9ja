from datetime import timedelta
from pathlib import Path
import os

from django.contrib import messages
from google.oauth2 import service_account

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%*#vd8z9(rj0fyv)oimes0rpe3%mj#9hc&!@%s+!8v@t1luk%#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG", 1)))

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

    # Core Apps...
    'apps.accounts',
    'apps.contacts',
    'apps.agents',
    'apps.notifications',
    'apps.profiles',
    'apps.properties',
    'apps.wallets',
    'apps.enquiries',
    'apps.chats',
    'apps.inboxes',

    # Third party app...
    'django_extensions',
    'social_django',  # Social auth
    'rest_framework',
    'django_filters',
    'django_countries',
    'phonenumber_field',
    "corsheaders",
    'rest_framework_simplejwt',
    'widget_tweaks',
    'crispy_forms',
    # 'guardian',
]

SITE_ID = 1
SITE_NAME = "PropertyDealsIn9ja"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',  # Social auth
    'apps.accounts.middleware.LastVisitMiddleware',
]

ROOT_URLCONF = 'propertyDealsIn9ja.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.notifications.views.notification_counts',
                'social_django.context_processors.backends',  # Social auth
            ],
        },
    },
]

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    },
    'ROUTING': 'propertyDealsIn9ja.asgi.application'
}

ASGI_APPLICATION = 'propertyDealsIn9ja.asgi.application'
# WSGI_APPLICATION = 'propertyDealsIn9ja.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
# STATIC_ROOT = os.path.join(BASE_DIR, 'propin9ja', 'static')
STATIC_ROOT = '/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'propertydealsin9ja-webapp2.appspot.com'
# STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    "propertyDealsIn9ja/json_dirs/propertydealsin9ja-webapp2-6bfa725aa663.json"
)

# Default authentication model...
AUTH_USER_MODEL = "accounts.User"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Default authentication model...
AUTH_USER_MODEL = "accounts.User"

# Social app custom settings
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend', # this is default
    'apps.accounts.backends.MyBackend'
)

LOGIN_URL = 'accounts/login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_URL = 'accounts/logout'
LOGOUT_REDIRECT_URL = 'home'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '654243012660-t26a053klabkujq0p87pea3tfprf6hpp.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 3
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": (
        "Bearer",
        "JWT",
    ),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'SIGNING_KEY': "os.environ.get('SIGNING_KEY')",
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ORIGIN_ALLOW_ALL = True

# Email Settings...
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'propertydeals9ja@gmail.com'
EMAIL_HOST_PASSWORD = 'djkyfqovubziqjne'
EMAIL_USE_TLS = True
SUPPORT_EMAIL = 'propertydeals9ja@gmail.com'

# This validates the file size...
FILE_UPLOAD_PERMISSION = 0o640

MESSAGE_TAGS = {
    messages.ERROR: "danger"
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
            'redirect_uri': 'http://127.0.0.1:8000/'
        }
    }
}

GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_API_KEY"

import tinify
tinify.key = "tC5sWsRfcPMvxHYF2kQFCpMj5yNKFND3"
