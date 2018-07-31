import datetime
from instamojo_wrapper import Instamojo


CUSTOM_APPS = [
    'rest_framework',
    'drfaddons',
    'restaurant.apps.RestaurantConfig',
    'billing.apps.BillingConfig',
    'offers.apps.OffersConfig',
    'drf_user',
    'drf_yasg',
]


AUTHENTICATION_BACKENDS = ['drf_user.auth.MultiFieldModelBackend',]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'drfaddons.auth.JSONWebTokenAuthenticationQS',
    ),

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

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

    'JWT_PAYLOAD_HANDLER': 'drfaddons.auth.jwt_payload_handler',

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

    # 'JWT_ALLOW_REFRESH': False,
    # 'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': '',
    # 'JWT_AUTH_COOKIE': None,
}

JWT_AUTH_KEY = 'Authorization'

USE_TZ = False

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

USER_SETTINGS = {
    'DEFAULT_ACTIVE_STATE': True,
    'OTP': {
        'LENGTH': 4,
        'ALLOWED_CHARS': '1234567890',
        'VALIDATION_ATTEMPTS': 3,
        'SUBJECT': 'OTP for Verification',
        'COOLING_PERIOD': 0
    },
    'MOBILE_VALIDATION': False,
    'EMAIL_VALIDATION': False,
    'REGISTRATION': {
        'SEND_MAIL': True,
        'MAIL_SUBJECT': 'Welcome to OfficeCafe',
        'TEXT_MAIL_BODY': 'Your account has been created.',
        'HTML_MAIL_BODY': 'Your account has been created.',
        'SEND_SMS': True,
        'SMS_BODY': 'Welcome to OfficeCafe. Your account has been created with us.'
    }
}



# api = Instamojo(api_key='test_2e8398986827d0737f5ba3d3a20',
#                 auth_token='test_a3dea9627890cfbf323e8c894ef')
#
# response = api.payment_request_create(
#     amount='3499',
#     purpose='FIFA 16',
#     send_email=True,
#     email="adityagupta93999@gmail.com",
#     redirect_url="http://www.example.com/handle_redirect.py"
#     )
# # print the long URL of the payment request.
# print (response['payment_request']['longurl'])
# # print the unique ID(or payment request ID)
# print (response['payment_request']['id'])