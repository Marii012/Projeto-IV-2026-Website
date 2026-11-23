from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR.parent / '.env')

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() == 'true'
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'laboratorio',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'projetoIV.urls'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.request',
        'django.contrib.messages.context_processors.messages',
    ]},
}]
WSGI_APPLICATION = 'projetoIV.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'projeto4teste',
        'USER': 'admin',
        'PASSWORD': 'projeto4',
        'HOST': '100.105.58.22',
        'PORT': '5432',
    }
}

LANGUAGE_CODE = 'pt-pt'
TIME_ZONE = 'Europe/Lisbon'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

API_URL = 'http://127.0.0.1:8000/api'
API_TIMEOUT = 10

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'laboratorio.api.authentication.AutenticacaoSessao',
    ],
}
