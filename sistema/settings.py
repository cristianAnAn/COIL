import os
import dj_database_url
from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v%yd%ot&63oao2m#y55asa5qixe0#i*2+qj+qgspq!e_-x7l4y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'plataforma',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pwa',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sistema.urls'

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

WSGI_APPLICATION = 'sistema.wsgi.application'

# Function to check internet connectivity

# Load environment variables
load_dotenv()

DATABASES = {
        'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
# settings.py
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'plataforma.validators.CustomPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
# settings.py
LANGUAGE_CODE = 'es'


TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'plataforma/static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'plataforma.Usuario'

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

LOGIN_URL = 'Login'  # URL to redirect if user is not authenticated
# LOGIN_REDIRECT_URL = 'Home'  # URL to redirect after successful login
LOGOUT_REDIRECT_URL = 'Login'  # URL to redirect after logout

PWA_APP_NAME = "COIL"
PWA_APP_DESCRIPTION = "COIL"
PWA_APP_THEME_COLOR = "#3477f5"
PWA_APP_BACKGROUND_COLOR = "#6699f7"

PWA_APP_ICONS = [
    {
        "src": "/static/img/IconCoil.png",
        "sizes": "160x160"
    }
]

PWA_APP_ICONS_APPLE = [
    {
        "src": "/static/img/IconCoil.png",
        "sizes": "160x160"
    }
]

PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, "serviceworker.js")

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'systempycoil@gmail.com'
EMAIL_HOST_PASSWORD = 'k k y c p r t n t n o r t z a u'


SESSION_COOKIE_AGE = 1800 # 1 hour (in seconds)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')