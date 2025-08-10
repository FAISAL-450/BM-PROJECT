import os
import json
from pathlib import Path

# 🏗️ Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 Security
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'unsafe-default-key')
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# 🌍 Hosts and CSRF
try:
    ALLOWED_HOSTS = json.loads(os.environ.get('DJANGO_ALLOWED_HOSTS', '["localhost", "127.0.0.1"]'))
except json.JSONDecodeError:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

try:
    CSRF_TRUSTED_ORIGINS = json.loads(os.environ.get('CSRF_TRUSTED_ORIGINS', '[]'))
except json.JSONDecodeError:
    CSRF_TRUSTED_ORIGINS = []

# 📦 Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Project apps
    'home',
    'construction_department',
    'sales_department',
    'project',
    'customer',

    'django_auth_adfs',

]



AUTHENTICATION_BACKENDS = [
    'django_auth_adfs.backend.AdfsAuthCodeBackend',
    'django.contrib.auth.backends.ModelBackend',
]


AUTH_ADFS = {
    "TENANT_ID": "530309b4-7b42-400e-9b38-eae5bef5408e",
    "CLIENT_ID": "090954ee-4a87-4ac9-99eb-a112551c09a8",
    "RELYING_PARTY_ID": "090954ee-4a87-4ac9-99eb-a112551c09a8",  # ✅ Often same as CLIENT_ID
    "AUDIENCE": "090954ee-4a87-4ac9-99eb-a112551c09a8",           # ✅ Optional but valid
    "ISSUER": "https://sts.windows.net/530309b4-7b42-400e-9b38-eae5bef5408e/",  # ✅ Correct format
}





LOGIN_URL = '/oauth2/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/oauth2/logout/'




# ⚙️ Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware' if not DEBUG else '',  # Enable in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
MIDDLEWARE = [mw for mw in MIDDLEWARE if mw]  # Remove empty string if DEBUG


# 🌐 Root URLs and WSGI
ROOT_URLCONF = 'bm_garden.urls'
WSGI_APPLICATION = 'bm_garden.wsgi.application'

# 🎨 Templates
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
            ],
        },
    },
]

# 🗄️ Database
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME', BASE_DIR / 'db.sqlite3'),
    }
}

# 🔒 Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌍 Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_TZ = True

# 📁 Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 🆔 Default primary key field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 👥 Azure AD Email to Group Mapping
AZURE_AD_EMAIL_TO_GROUP = {
    "masud@dzignscapeprofessionals.onmicrosoft.com": "ConstructionGroup",
    "nayan@dzignscapeprofessionals.onmicrosoft.com": "SalesGroup",
}






