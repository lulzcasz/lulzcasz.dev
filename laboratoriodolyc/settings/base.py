from pathlib import Path
from os import getenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = getenv("SECRET_KEY")

ALLOWED_HOSTS = getenv("ALLOWED_HOSTS", '*').split(",")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'uploads',
    'posts',
]

TINYMCE_DEFAULT_CONFIG = {
    "height": "800px",
    "width": "100%",
    "menubar": False,
    "plugins": "image codesample directionality fullscreen link lists advlist media preview table code",
    "toolbar": "undo redo | blocks fontsize | bold italic underline strikethrough | align numlist bullist | link image | table media | lineheight outdent indent| forecolor backcolor removeformat | charmap emoticons | code fullscreen preview | pagebreak anchor codesample ltr rtl",
    "toolbar_mode": "wrap",
    "codesample_languages": [
        {"text": "Markup", "value": "markup"},
        {"text": "CSS", "value": "css"},
        {"text": "JavaScript", "value": "javascript"},
        {"text": "Arduino", "value": "arduino"},
        {"text": "ARM Assembly", "value": "armasm"},
        {"text": "6502 Assembly", "value": "asm6502"},
        {"text": "Atmel AVR Assembly", "value": "asmatmel"},
        {"text": "Bash", "value": "bash"},
        {"text": "C", "value": "c"},
        {"text": "C++", "value": "cpp"},
        {"text": "CMake", "value": "cmake"},
        {"text": "Django/Jinja2", "value": "django"},
        {"text": "Docker", "value": "docker"},
        {"text": "Go", "value": "go"},
        {"text": "Go module", "value": "go-module"},
        {"text": ".ignore", "value": "ignore"},
        {"text": "Java", "value": "java"},
        {"text": "JSON", "value": "json"},
        {"text": "Makefile", "value": "makefile"},
        {"text": "Markdown", "value": "markdown"},
        {"text": "MongoDB", "value": "mongodb"},
        {"text": "NASM", "value": "nasm"},
        {"text": "nginx", "value": "nginx"},
        {"text": "PowerShell", "value": "powershell"},
        {"text": "Python", "value": "python"},
        {"text": "QML", "value": "qml"},
        {"text": "Regex", "value": "regex"},
        {"text": "Rust", "value": "rust"},
        {"text": "Sass (Sass)", "value": "sass"},
        {"text": "Sass (SCSS)", "value": "scss"},
        {"text": "SQL", "value": "sql"},
        {"text": "TOML", "value": "toml"},
        {"text": "TypeScript", "value": "typescript"},
        {"text": "URI", "value": "uri"},
        {"text": "YAML", "value": "yaml"},
        {"text": "Treeview", "value": "treeview"},
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'laboratoriodolyc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'laboratoriodolyc.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv("DATABASE_NAME"),
        'USER': getenv("DATABASE_USER"),
        'PASSWORD': getenv("DATABASE_PASSWORD"),
        'HOST': getenv('DATABASE_HOST'),
        'PORT': getenv("DATABASE_PORT"),
    },
}

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

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Santarem'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Santarem'

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "location": "uploads",
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AWS_S3_ACCESS_KEY_ID = getenv("AWS_S3_ACCESS_KEY_ID")
AWS_S3_SECRET_ACCESS_KEY = getenv("AWS_S3_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = getenv("AWS_STORAGE_BUCKET_NAME")
AWS_QUERYSTRING_AUTH = False
