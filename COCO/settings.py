import os,socket
from dotenv import load_dotenv
load_dotenv()
import dj_database_url
from pathlib import Path
import cloudinary

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-(zi1i7$!50u8o)et6g!icnlz=9@_0*6ftp6m6eji*fq8#n37c9'

DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ('true', '1')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split(',')



INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'Accounts.apps.AccountsConfig',
    'POCOS.apps.PocosConfig',
    'POJOS.apps.PojosConfig',
    'Orders.apps.OrdersConfig',
    'Manager.apps.ManagerConfig',
    'Api.apps.ApiConfig',

    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',

]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'Manager.middleware.SessionAuthOnlyMiddleware',

    
    
]


CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if os.getenv("CORS_ALLOWED_ORIGINS") else [
    "https://cocomatik.com",
    "http://127.0.0.1:5500",  
]

CORS_ALLOW_ALL_ORIGINS = False  


SHIPROCKET_EMAIL = os.getenv("SHIPROCKET_EMAIL", default="")
SHIPROCKET_PASSWORD = os.getenv("SHIPROCKET_PASSWORD", default="")


ROOT_URLCONF = 'COCO.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'COCO.wsgi.application'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  
]

SESSION_COOKIE_AGE = 3600  
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = True  
SESSION_ENGINE = "django.contrib.sessions.backends.db"  

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',  
        'rest_framework.authentication.SessionAuthentication',  
    ),
}

LOGIN_URL = '/accounts/login/'  
LOGOUT_REDIRECT_URL = '/accounts/login/'  


DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.hostinger.com'  
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True
EMAIL_PORT = 587


EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')


cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True,
)


DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"


AUTH_USER_MODEL = "Accounts.UserAccount"

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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True 


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage" 


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
