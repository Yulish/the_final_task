from pathlib import Path
import os



ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-9@ms+*98yhm(&x(8u0m_57w(6^4xvbh554&(@^v#kao*z0+kuv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'ishmakova1@yandex.ru'
EMAIL_HOST_PASSWORD = 'qsijnzkazzsnsoat'
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'ishmakova1@yandex.ru'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_SIGNUP_REDIRECT_URL = '/login_with_code/'



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_filters',
    'django_apscheduler',
    'board.apps.BoardConfig',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'ckeditor',
    'ckeditor_uploader',

]

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/posters'

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'allauth.account.middleware.AccountMiddleware',

]

ROOT_URLCONF = 'announcement_board.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'announcement_board.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # должна включать static с uploadfile
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

SITE_URL = 'http://127.0.0.1:8000'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_ALLOW_NONIMAGE_FILES = True


# CKEDITOR_CONFIGS = {
#     'default': {
#         'toolbar': 'Full',
#         'contentsCss': ['/static/ckeditor/ckeditor/skins/moono-lisa/content.css'],
#         'extraCss': 'img { width: 20% !important; height: auto !important; }',
#         'extraPlugins': 'html5audio,html5video, embed, uploadfile',
#         'filebrowserUploadUrl': '/ckeditor/upload/',
#         'filebrowserImageUploadUrl': '/ckeditor/upload/?type=Images',
#         'filebrowserVideoUploadUrl': '/ckeditor/upload/?type=Video',
#         'filebrowserBrowseUrl': '/ckeditor/browse/',
#         'filebrowserImageBrowseUrl': '/ckeditor/browse/?type=Images',
#         'filebrowserVideoBrowseUrl': '/ckeditor/browse/?type=Video',
#         'allowedContent': True,
#         'html5video': {
#             'formats': 'mp4,webm,ogg',
#             'allowUrl': True,
#             'width': '50%',
#             'maxWidth': '640',
#             'controls': True,
#             'poster': False,
#             'useSourceTag': True,
#             'video': {
#                 'attributes': {
#                     'controls': 'controls',
#                     'autoplay': '',
#                 }
#             }
#         },
#     }
# }

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'extraPlugins': 'html5audio,html5video, embed, uploadfile',
        'filebrowserUploadUrl': '/ckeditor/upload/',
        'filebrowserImageUploadUrl': '/ckeditor/upload/?type=Images',
        'filebrowserBrowseUrl': '/ckeditor/browse/',
        'filebrowserImageBrowseUrl': '/ckeditor/browse/?type=Images',
        'filebrowserVideoBrowseUrl': '/ckeditor/browse/?type=Video',
        'allowedContent': True,
        'html5video': {
            'formats': 'mp4,webm,ogg',
            'allowUrl': True,
            'maxWidth': '640',
            'controls': True,
            'poster': False,
            'useSourceTag': True,
            'video': {
                'attributes': {
                    'controls': 'controls',
                    'autoplay': '',
                }
            }
        },
    }
}