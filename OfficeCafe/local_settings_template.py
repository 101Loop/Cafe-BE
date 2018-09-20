# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'YOUR SECRET KEY'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'OfficeCafeDB',
        'USER': '---',
        'PASSWORD': '---',
    }
}

HSPSMS = {
    'USER': '',
    'APIKEY': '',
    'SENDER': 'OFCAFE'
}

INSTAMOJO = {
    'API_KEY': '',
    'AUTH_TOKEN': '',
    'ENDPOINT': 'https://www.instamojo.com/api/1.1/',
    'CLIENT_ID': '',
    'CLIENT_SECRET': ''
}
