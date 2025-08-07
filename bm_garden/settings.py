import os
import json
from pathlib import Path

# 🏗️ Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 Security
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'unsafe-default-key')
DEBUG = True

# 🌍 Hosts and CSRF
try:
    ALLOWED_HOSTS = json.loads(os.environ.get('DJANGO_ALLOWED_HOSTS', '["localhost", "127.0.0.1"]'))
except json.JSONDecodeError:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

try:
    CSRF_TRUSTED_ORIGINS = json.loads(os.environ.get('CSRF_TRUSTED_ORIGINS', '[]'))
except json.JSONDecodeError:
    CSRF_TRUSTED_ORIGINS = []

# 🆔 Azure AD Credentials
AZURE_AD_CLIENT_ID = os.environ.get('AZURE_AD_CLIENT_ID')
AZURE_AD_CLIENT_SECRET = os.environ.get('AZURE_AD_CLIENT_SECRET')
AZURE_AD_TENANT_ID = os.environ.get('AZURE_AD_TENANT_ID')

# 🔐 Azure AD + Easy Auth Configuration
AZURE_AUTH = {
    "CLIENT_ID": AZURE_AD_CLIENT_ID,
    "CLIENT_SECRET": AZURE_AD_CLIENT_SECRET,
    "REDIRECT_URI": "https://bm-erp-app.azurewebsites.net/.auth/login/aad/callback",  # updated to match actual redirect URI
    "AUTHORITY": "https://login.microsoftonline.com/530309b4-7b42-400e-9b38-eae5bef5408e",  # updated tenant ID
    "SCOPES": ["User.Read"],
    "USERNAME_ATTRIBUTE": "mail",  # or "preferred_username" depending on token
    "GROUP_ATTRIBUTE": "groups",   # matches Azure AD claim type
    "GROUP_ROLE_MAP": {
        "eb69dbcb-90a4-4f13-9059-d6494812fd8f": "ConstructionGroup",
        "2b36c9c9-5c74-435b-becd-d01df21e4cf4": "SalesGroup",
    }
}
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
    # Azure AD auth
    'azure_auth',
]

# 🔐 Auth
LOGIN_URL = '/azure_auth/login'
LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# ⚙️ Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware' if not DEBUG else '',
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
