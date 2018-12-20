from django.utils.text import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework import serializers


class OTPLoginSerializer(serializers.Serializer):
    """
    This Serializer is for sending OTP & verifying destination via otp.
    is_login: Set is_login true if trying to login via OTP.
    """

    from rest_framework import serializers

    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    verify_otp = serializers.IntegerField(default=None, required=False)
    mobile = serializers.CharField(required=True)

    @staticmethod
    def get_user(email: str, mobile: str):
        from drf_user.models import User

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(mobile=mobile)
            except User.DoesNotExist:
                user = None

        if user:
            if user.email != email:
                raise serializers.ValidationError(_(
                    "Your account is registered with {mobile} does not has "
                    "{email} as registered email. Please login directly via "
                    "OTP with your mobile.".format(mobile=mobile, email=email)
                ))
            if user.mobile != mobile:
                raise serializers.ValidationError(_(
                    "Your account is registered with {email} does not has "
                    "{email} as registered email. Please login directly via "
                    "OTP with your email.".format(mobile=mobile, email=email)))
        return user

    def validate(self, attrs: dict) -> dict:
        attrs['user'] = self.get_user(email=attrs.get('email'),
                                      mobile=attrs.get('mobile'))
        return attrs


class OTPLoginView(APIView):
    """
    Used to register/login to OfficeCafe
    name - Required
    email - Required
    mobile - Required
    verify_otp - Not Required (only when verifying OTP)
    """

    from rest_framework.permissions import AllowAny
    from rest_framework.renderers import JSONRenderer
    from rest_framework.parsers import JSONParser

    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)
    serializer_class = OTPLoginSerializer

    def post(self, request, *args, **kwargs):
        from rest_framework.response import Response
        from rest_framework.mixins import status

        from rest_framework.exceptions import APIException

        from drf_user.utils import validate_otp, generate_otp, send_otp
        from drf_user.utils import login_user

        from drf_user.models import User

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        verify_otp = serializer.validated_data.get('verify_otp', None)
        name = serializer.validated_data.get('name')
        mobile = serializer.validated_data.get('mobile')
        email = serializer.validated_data.get('email')
        user = serializer.validated_data.get('user', None)

        message = {}

        if verify_otp:
            if validate_otp(email, verify_otp):
                if not user:
                    user = User.objects.create(
                        name=name, mobile=mobile, email=email, username=mobile,
                        password=User.objects.make_random_password()
                    )
                return Response(login_user(user, self.request),
                                status=status.HTTP_202_ACCEPTED)
            return Response(data={'OTP': [_('OTP Validated successfully!'), ]},
                            status=status.HTTP_202_ACCEPTED)

        else:
            otp_obj_email = generate_otp('E', email)
            otp_obj_mobile = generate_otp('M', mobile)

            # Set same OTP for both Email & Mobile
            otp_obj_mobile.otp = otp_obj_email.otp
            otp_obj_mobile.save()

            # Send OTP to Email & Mobile
            sentotp_email = send_otp(email, otp_obj_email, email)
            sentotp_mobile = send_otp(mobile, otp_obj_mobile, email)

            if sentotp_email['success']:
                otp_obj_email.send_counter += 1
                otp_obj_email.save()
                message['email'] = {
                    'otp': _("OTP has been sent successfully.")
                }
            else:
                message['email'] = {
                    'otp':_("OTP sending failed {}".format(sentotp_email['message']))
                }

            if sentotp_mobile['success']:
                otp_obj_mobile.send_counter += 1
                otp_obj_mobile.save()
                message['mobile'] = {
                    'otp': _("OTP has been sent successfully.")
                }
            else:
                message['mobile'] = {
                    'otp': _("OTP sending failed {}".format(sentotp_mobile['message']))
                }

            if sentotp_email['success'] or sentotp_mobile['success']:
                curr_status = status.HTTP_201_CREATED
            else:
                raise APIException(
                    detail=_(
                        'A Server Error occurred: ' + sentotp_mobile['message']
                    ))

            return Response(data=message, status=curr_status)
