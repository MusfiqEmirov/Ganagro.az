from pathlib import Path
import os

from dotenv import load_dotenv


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
#

##
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

CSRF_TRUSTED_ORIGINS = [
    "https://www.ganaqro.az",
    'https://ganaqro.az',
    'http://localhost:8080',
    'http://127.0.0.1:8080',
 
]

# CSRF Cookie Settings
CSRF_COOKIE_SECURE = True  
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False

# Session Cookie Settings
SESSION_COOKIE_SECURE = True  
SESSION_COOKIE_HTTPONLY = True


# Admin URL - secret path (required)
ADMIN_URL = os.getenv('ADMIN_URL')
if not ADMIN_URL:
    raise ValueError("ADMIN_URL environment variable is required!")
if not ADMIN_URL.endswith('/'):
    ADMIN_URL += '/'

# Admin panel default language (used by CustomLocaleMiddleware)
ADMIN_LANGUAGE_CODE = 'az'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    # Third Packages
    'django_cleanup.apps.CleanupConfig',
    'ckeditor',
    'compressor',

    # Apps
    'projects'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'ganaqro.middleware.CustomLocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ganaqro.middleware.PublicHtmlCacheControlMiddleware',
]



ROOT_URLCONF = 'ganaqro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ganaqro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'az'

LANGUAGES = [
    ('az', 'Azərbaycan'),
    ('en', 'English'),
    ('ru', 'Русский'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = 'Asia/Baku'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Media / Static configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Static files directories
STATICFILES_DIRS = [
    os.path.join(str(BASE_DIR), 'static'),
]

# Cache configuration
# https://docs.djangoproject.com/en/5.2/topics/cache/

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'ganaqro-cache',
        'TIMEOUT': 7200,  # 2 hours default timeout
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

# Cache timeout settings (in seconds)
CACHE_TIMEOUT_SHORT = 1800  # 30 minutes for occasionally changing data
CACHE_TIMEOUT_MEDIUM = 7200  # 2 hours for normal pages (projects, vacancies lists)
CACHE_TIMEOUT_LONG = 86400  # 24 hours for stable data (about, contact, background images)

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = os.getenv(
    'EMAIL_BACKEND',
    'django.core.mail.backends.smtp.EmailBackend',
)
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False').lower() in ('true', '1', 'yes')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

# Lokal inkişaf: .env-də EMAIL yoxdursa settings_local-dakı SMTP istifadə et
if DEBUG and not EMAIL_HOST_USER:
    try:
        from ganaqro import settings_local as _local_settings

        EMAIL_BACKEND = _local_settings.EMAIL_BACKEND
        EMAIL_HOST = _local_settings.EMAIL_HOST
        EMAIL_PORT = _local_settings.EMAIL_PORT
        EMAIL_HOST_USER = _local_settings.EMAIL_HOST_USER
        EMAIL_HOST_PASSWORD = _local_settings.EMAIL_HOST_PASSWORD
        EMAIL_USE_TLS = _local_settings.EMAIL_USE_TLS
        EMAIL_USE_SSL = _local_settings.EMAIL_USE_SSL
        DEFAULT_FROM_EMAIL = _local_settings.DEFAULT_FROM_EMAIL
    except ImportError:
        pass

from .ckeditor_presets import CKEDITOR_PROJECT_CONFIG  # noqa: E402 — sonda saxlanılıb ki, INSTALLED_APPS oxunsun

CKEDITOR_CONFIGS = CKEDITOR_PROJECT_CONFIG
