from rest_framework.mixins import status
from drfaddons.views import ValidateAndPerformView
from django.contrib.auth import get_user_model
from . import user_settings, update_user_settings
from rest_framework.generics import UpdateAPIView


User = get_user_model()
otp_settings = user_settings['OTP']


def generate_otp(prop, value):
    """
    This function generates an OTP and saves it into Model. It also sets various counters, such as send_counter,
    is_validated, validate_attempt.
    Parameters
    ----------
    prop: str
        This specifies the type for which OTP is being created. Can be::
            email
            mobile
    value: str
        This specifies the value for which OTP is being created.

    Returns
    -------
    otp_object: OTPValidation
        This is the instance of OTP that is created.
    Examples
    --------
    To create an OTP for an Email test@testing.com
    >>> print(generate_otp('email', 'test@testing.com'))
    OTPValidation object

    >>> print(generate_otp('email', 'test@testing.com').otp)
    5039164
    """
    from .models import OTPValidation

    import datetime

    # Create a random number
    random_number = User.objects.make_random_password(length=otp_settings['LENGTH'],
                                                      allowed_chars=otp_settings['ALLOWED_CHARS'])

    # Checks if random number is unique among non-validated OTPs and creates new until it is unique.
    while OTPValidation.objects.filter(otp__exact=random_number).filter(is_validated=False):
        random_number = User.objects.make_random_password(length=otp_settings['LENGTH'],
                                                          allowed_chars=otp_settings['ALLOWED_CHARS'])

    # Get or Create new instance of Model with value of provided value and set proper counter.
    otp_object, created = OTPValidation.objects.get_or_create(destination=value)
    if not created:
        if otp_object.reactive_at > datetime.datetime.now():
            return otp_object

    otp_object.otp = random_number
    otp_object.type = prop

    # Set is_validated to False
    otp_object.is_validated = False

    # Set attempt counter to OTP_VALIDATION_ATTEMPS, user has to enter correct OTP in 3 chances.
    otp_object.validate_attempt = otp_settings['VALIDATION_ATTEMPTS']

    otp_object.reactive_at = datetime.datetime.now() - datetime.timedelta(minutes=1)
    otp_object.save()
    return otp_object


def validate_otp(value, otp):
    """
    This function is used to validate the OTP for a particular value.
    It also reduces the attempt count by 1 and resets OTP.
    Parameters
    ----------
    value: str
        This is the unique entry for which OTP has to be validated.
    otp: int
        This is the OTP that will be validated against one in Database.

    Returns
    -------
    tuple
        Returns a tuple containing::
                data: dict
                    This is a dictionary containing::
                        'success': bool
                            This will be True if OTP is validated, else False
                        'OTP': str
                            This will contain a proper message about the OTP Validation
                status: int
                    This will be a HTTP Status Code with resepect to the type of success or error occurred.
    Examples
    --------
    To validate an OTP against test@testing.com with wrong OTP
    >>> print(validate_otp('test@testing.com', 6518631))
    ({'OTP': 'OTP Validation failed! 2 attempts left!', 'success': False}, 401)

    To validate an OTP against random@email.com with value that doesn't exist
    >>>print(validate_otp('random@email.com', 6518631))
    ({'OTP': 'Provided value to verify not found!', 'success': False}, 404)

    To validate a correct OTP with value test@testing.com
    >>>print(validate_otp('test@testing.com', 5039164))
    ({'OTP': 'OTP Validated successfully!', 'success': True}, 202)

    To validate incorrect OTP more than 3 times or re-validate already validated value with incorrect OTP
    >>>print(validate_otp('test@testing.com', 6518631))
    ({'OTP': 'Attempt exceeded! OTP has been reset!', 'success': False}, 401)
    """
    from .models import OTPValidation

    # Initialize data dictionary that will be returned
    data = {'success': False}

    try:
        # Try to get OTP Object from Model and initialize data dictionary
        otp_object = OTPValidation.objects.get(destination=value)

        # Decrement validate_attempt
        otp_object.validate_attempt -= 1

        if str(otp_object.otp) == str(otp):
            otp_object.is_validated = True
            otp_object.save()
            data['OTP'] = 'OTP Validated successfully!'
            data['success'] = True
            status_code = status.HTTP_202_ACCEPTED
        elif otp_object.validate_attempt <= 0:
            generate_otp(otp_object.type, value)
            status_code = status.HTTP_401_UNAUTHORIZED
            data['OTP'] = 'Attempt exceeded! OTP has been reset!'
        else:
            otp_object.save()
            data['OTP'] = 'OTP Validation failed! ' + str(otp_object.validate_attempt) + ' attempts left!'
            status_code = status.HTTP_401_UNAUTHORIZED
    except OTPValidation.DoesNotExist:
        # If OTP object doesn't exist set proper message and status_code
        data['OTP'] = 'Provided value to verify not found!'
        status_code = status.HTTP_404_NOT_FOUND

    return data, status_code


def send_otp(prop: str, value: str, otpobj, recip: str):
    """
    This function sends OTP to specified value.
    Parameters
    ----------
    prop: str
        This is the type of value. It can be "email" or "mobile"
    value: str
        This is the value at which and for which OTP is to be sent.
    otpobj: OTPValidation
        This is the OTP or One Time Passcode that is to be sent to user.
    recip: str
        This is the recipient to whom EMail is being sent. This will be deprecated once SMS feature is brought in.

    Returns
    -------

    """
    from drfaddons.add_ons import send_message

    import datetime

    otp = otpobj.otp
    rdata = {'success': False, 'message': None}

    if otpobj.reactive_at > datetime.datetime.now():
        rdata['message'] = 'OTP sending not allowed until: ' + otpobj.reactive_at.strftime('%d-%h-%Y %H:%M:%S')
        return rdata

    message = "OTP for verifying " + prop + ": " + value + " is " + otp + ". Don't share this with anyone!"

    rdata = send_message(message, otp_settings['SUBJECT'], value, recip)

    otpobj.reactive_at = datetime.datetime.now() + datetime.timedelta(minutes=otp_settings['COOLING_PERIOD'])
    otpobj.save()

    return rdata


def login_user(user: User, request)->(dict, int):
    """
    This function is used to login a user. It saves the authentication in AuthTransaction model.
    Parameters
    ----------
    user: django.contrib.auth.get_user_model
    request: HttpRequest

    Returns
    -------
    tuple:
        data: dict
        status_code: int
    """
    from drfaddons.add_ons import get_client_ip
    from drfaddons.auth import jwt_payload_handler

    from rest_framework_jwt.utils import jwt_encode_handler

    from .models import AuthTransaction

    import datetime

    token = jwt_encode_handler(jwt_payload_handler(user))
    user.last_login = datetime.datetime.now()
    user.save()
    AuthTransaction(user=user, ip_address=get_client_ip(request), token=token, session=user.get_session_auth_hash()) \
        .save()

    data = {'session': user.get_session_auth_hash(), 'token': token}
    status_code = status.HTTP_200_OK
    return data, status_code


def check_validation(value):
    """
    This functions check if given value is already validated via OTP or not.
    Parameters
    ----------
    value: str
        This is the value for which OTP validation is to be checked.

    Returns
    -------
    bool
        True if value is validated, False otherwise.
    Examples
    --------
    To check if 'test@testing.com' has been validated!
    >>> print(check_validation('test@testing.com'))
    True

    """
    from .models import OTPValidation

    try:
        otp_object = OTPValidation.objects.get(destination=value)
        if otp_object.is_validated:
            return True
        else:
            return False
    except OTPValidation.DoesNotExist:
        return False


class LoginOTP(ValidateAndPerformView):
    """
    This function allows the user to login using the otp. The data require is mobile no.
    If something happens and the otp is not send to the mobile no then it will ask for the email of the user
    and the otp will be send to the email of the user.
    """
    from .serializer import LoginOTPSerializer

    serializer_class = LoginOTPSerializer

    def validated(self, serialized_data, *args, **kwargs):
        created = False

        otp = serialized_data.data['otp']
        mobile = serialized_data.data['mobile']
        email = serialized_data.data['email']

        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            user = User.objects.create_user(username=mobile,
                                            email=mobile+'@officecafe.in',
                                            name=mobile,
                                            password=User.objects.make_random_password(),
                                            mobile=mobile)
            created = True

        if email:
            user.email = email
            user.save()

        if 'name' in serialized_data.initial_data.keys():
            user.name = serialized_data.initial_data['name']
            user.save()

        if otp is None:
            otp_obj = generate_otp('mobile', mobile)
            data = send_otp('mobile', mobile, otp_obj, user.email)

            if data['success']:
                status_code = status.HTTP_201_CREATED
            else:
                status_code = status.HTTP_400_BAD_REQUEST
        else:
            if otp == '0000':
                if not created:
                    otp_obj = generate_otp('email', user.email)
                    data = send_otp('email', user.email, otp_obj, user.email)

                    if data['success']:
                        status_code = status.HTTP_201_CREATED
                    else:
                        status_code = status.HTTP_400_BAD_REQUEST
                else:
                    return {'success': False, 'message': 'Server error occurred.'}, \
                           status.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                data, status_code = validate_otp(user.mobile, int(otp)) or validate_otp(user.email, int(otp))
                if status_code == status.HTTP_202_ACCEPTED:
                    data, status_code = login_user(user, self.request)

        data['created'] = created
        data['name'] = user.name
        email_split = user.email.split('@')
        data['email'] = email_split[0][-1] + '@' + email_split[1]

        return data, status_code


class UpdateProfileView(UpdateAPIView):
    """
    This view is to update a user profile.
    """

    from .serializer import UpdateProfileSerializer
    from .models import User

    queryset = User.objects.all()
    serializer_class = UpdateProfileSerializer

    def update(self, request, *args, **kwargs):

        from drfaddons.add_ons import JsonResponse

        serializer = self.UpdateProfileSerializer(request.user, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            request.user.save()
            return JsonResponse(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
