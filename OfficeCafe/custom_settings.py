import datetime


CUSTOM_APPS = [
    'lead',
    'comment',
    'currency',
    'order',
    'business',
    'product',
    'taxation',
    'outlet',
    'location',
    'rest_framework',
    'corsheaders',
    'drfaddons',
    'drf_instamojo',
    'drf_paytm',
    'drf_user',
    'drf_yasg',
]


CUSTOM_MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware'
]

CORS_ORIGIN_WHITELIST = (
    'officecafe.in',
    'localhost:4200',
)


CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST

CORS_ALLOW_METHODS = (
    'GET',
    'OPTIONS',
    'POST',
    'PUT'
)

AUTHENTICATION_BACKENDS = ['drf_user.auth.MultiFieldModelBackend',]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'drfaddons.auth.JSONWebTokenAuthenticationQS',
    ),

    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),

    'DEFAULT_FILTER_BACKENDS': (
        'drfaddons.filters.IsOwnerFilterBackend',
        'django_filters.rest_framework.DjangoFilterBackend'
    ),

}


AUTH_USER_MODEL = 'drf_user.User'


JWT_AUTH = {
    'JWT_ENCODE_HANDLER': 'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER': 'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER': 'drf_user.auth.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER': 'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_response_payload_handler',

    # 'JWT_SECRET_KEY': settings.SECRET_KEY,
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS512',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(weeks=4),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    # 'JWT_AUTH_COOKIE': None,
}

JWT_AUTH_KEY = 'Authorization'

TIME_ZONE = 'Asia/Kolkata'

STATIC_URL = '/static/'

STATIC_ROOT = 'static'

JET_THEMES = [
    {
        'theme': 'default',
        'color': '#47bac1',
        'title': 'Default'
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]

user_settings = {
    'DEFAULT_ACTIVE_STATE': True,
    'OTP': {
        'LENGTH': 4,
        'ALLOWED_CHARS': '1234567890',
        'VALIDATION_ATTEMPTS': 3,
        'SUBJECT': 'OTP for Verification',
        'COOLING_PERIOD': 3
    },
    'MOBILE_VALIDATION': True,
    'EMAIL_VALIDATION': True,
    'REGISTRATION': {
        'SEND_MAIL': True,
        'SEND_MESSAGE': False,
        'MAIL_SUBJECT': 'Welcome to OfficeCafe',
        'SMS_BODY': 'Your account has been created',
        'TEXT_MAIL_BODY': 'Your account has been created.',
        'HTML_MAIL_BODY': 'Your account has been created.'
    }
}
