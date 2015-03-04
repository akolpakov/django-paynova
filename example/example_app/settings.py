DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db'
    }
}

INSTALLED_APPS = (
    'paynova_api_django',
    'example_app'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

SECRET_KEY = 'any-key'

ROOT_URLCONF = 'example_app.urls'

PAYNOVA_MERCHANT_ID = 'MERCHANT_ID'
PAYNOVA_PASSWORD = 'PASSWORD'
PAYNOVA_SECRET = 'SECRET'
PAYNOVA_CALLBACK_URL = 'http://mysite.com'