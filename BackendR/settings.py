"""
Django settings for BackendR project – Docker + Gunicorn + Nginx + PostgreSQL
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ---------------------------------------------------------------------
# BASE + ENV
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env.local only for local dev. In Docker, compose injects env directly.
if (BASE_DIR / ".env.local").exists():
    load_dotenv(BASE_DIR / ".env.local")

# ---------------------------------------------------------------------
# CORE CONFIG
# ---------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-dev-key")
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"

# allow comma-separated ALLOWED_HOSTS
ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()] or [
    "engine.cocomatik.com",
    "admin.cocomatik.com",
    "127.0.0.1",
    "178.16.138.130",
]

# ---------------------------------------------------------------------
# APPS
# ---------------------------------------------------------------------
INSTALLED_APPS = [
    # default django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # project apps
    "Accounts.apps.AccountsConfig",
    "POCOS.apps.PocosConfig",
    "POJOS.apps.PojosConfig",
    "Orders.apps.OrdersConfig",
    "Manager.apps.ManagerConfig",
    "Adds.apps.AddsConfig",
    "Api.apps.ApiConfig",
    "Delivery.apps.DeliveryConfig",
    "Reports.apps.ReportsConfig",

    # 3rd party
    "django_extensions",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
]

# ---------------------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------------------
MIDDLEWARE = [
    # "whitenoise.middleware.WhiteNoiseMiddleware",  # optional if nginx handles static
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "BackendR.urls"
WSGI_APPLICATION = "BackendR.wsgi.application"

# ---------------------------------------------------------------------
# AUTH / SESSIONS
# ---------------------------------------------------------------------
AUTH_USER_MODEL = "Accounts.UserAccount"
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 3600  # 1 hour

# ---------------------------------------------------------------------
# SECURITY HEADERS (prod)
# ---------------------------------------------------------------------
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ---------------------------------------------------------------------
# CORS / CSRF
# ---------------------------------------------------------------------
def _split_env(name):
    return [x.strip() for x in os.getenv(name, "").split(",") if x.strip()]

CORS_ALLOWED_ORIGINS = _split_env("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_ALL_ORIGINS = False
CSRF_TRUSTED_ORIGINS = _split_env("DJANGO_CSRF_TRUSTED_ORIGINS") or [
    "https://engine.cocomatik.com",
    "https://admin.cocomatik.com",
    "http://localhost:8001",
]

# ---------------------------------------------------------------------
# DATABASE
# ---------------------------------------------------------------------
if DEBUG:
    # Local dev: SQLite3
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(Path(BASE_DIR) / "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DATABASE_NAME", BASE_DIR / "db.sqlite3"),
            "USER": os.getenv("DATABASE_USERNAME", ""),
            "PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
            "HOST": os.getenv("DATABASE_HOST", ""),
            "PORT": str(os.getenv("DATABASE_PORT", "")),
            "CONN_MAX_AGE": 600,
        }
    }

# ---------------------------------------------------------------------
# REST FRAMEWORK
# ---------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
}

# ---------------------------------------------------------------------
# EMAIL
# ---------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.hostinger.com"
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# ---------------------------------------------------------------------
# SHIPROCKET / CUSTOM CONFIG
# ---------------------------------------------------------------------
SHIPROCKET_EMAIL = os.getenv("SHIPROCKET_EMAIL")
SHIPROCKET_PASSWORD = os.getenv("SHIPROCKET_PASSWORD")
CDN_URL = os.getenv("CDN_URL")

# ---------------------------------------------------------------------
# STATIC & MEDIA (Docker paths)
# ---------------------------------------------------------------------

USE_CDN = os.getenv("USE_CDN", "false").lower() == "true"
if USE_CDN:
    CDN_BASE = os.getenv("CDN_URL", "").rstrip("/")
    if CDN_BASE:
        STATIC_URL = f"{CDN_BASE}/static/"
        MEDIA_URL  = f"{CDN_BASE}/media/"


STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# In dev, keep local static dirs
STATICFILES_DIRS = [BASE_DIR / "static"]

# Inside container, collected static + uploads
STATIC_ROOT = Path("/COCOB/staticfiles")
MEDIA_ROOT = Path("/COCOB/media")

# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ---------------------------------------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------
# AUTH REDIRECTS
# ---------------------------------------------------------------------
LOGIN_URL = "/accounts/login/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# ---------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------
LOG_DIR = BASE_DIR / "logs/runtime"
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": LOG_DIR / "django.log",
        },
    },
    "loggers": {
        "django": {"handlers": ["file"], "level": "DEBUG", "propagate": True},
    },
}

# ---------------------------------------------------------------------
# DEFAULTS
# ---------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
