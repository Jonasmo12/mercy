from pathlib import Path
import environ


BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'accounts',
    'apps.question',
    'apps.quiz',
    'apps.section',

    'crispy_forms',
    'storages',
]


X_FRAME_OPTIONS='SAMEORIGIN' # only if django version >= 3.0

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'learn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'learn.wsgi.application'
AUTH_USER_MODEL = 'accounts.Account'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mercy',
        'USER': 'postgres',
        'PASSWORD': 'Thaketse93',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Johannesburg'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'

# S3 Buckets Config


AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')


# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None



# # uploading media to s3
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# # automatically upload static to bucket
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

# # EMAIL_BACKEND = 'django_ses.SESBackend'

# # AWS_SES_REGION_NAME = 'us-east-2'
# # AWS_SES_REGION_ENDPOINT = 'email-smtp.us-east-2.amazonaws.com'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# # email stuff
# EMAIL_HOST = env('EMAIL_HOST')
# EMAIL_HOST_USER = env('EMAIL_HOST_USER')
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = env('EMAIL_HOST_USER')
# EMAIL_PORT = 587
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')



STATICFILES_DIRS = BASE_DIR / 'static',

STATIC_ROOT = BASE_DIR / 'staticfiles'
TEMPLATE_DIRS = BASE_DIR / 'templates',

MEDIA_URL = '/section/'

MEDIA_ROOT = BASE_DIR / 'static/section'
