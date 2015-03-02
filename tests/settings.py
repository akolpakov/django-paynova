DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db'
    }
}

INSTALLED_APPS = (
    'paynova_api_django',
)

SECRET_KEY = 'any-key'

PAYNOVA_USERNAME = 'USERNAME'
PAYNOVA_PASSWORD = 'PASSWORD'