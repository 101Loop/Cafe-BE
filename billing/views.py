from drfaddons.generics import OwnerCreateAPIView, OwnerListAPIView

from rest_framework.generics import RetrieveAPIView


def get_user(email: str, mobile: str, name: str=None):
    from django.contrib.auth import get_user_model

    User = get_user_model()

    try:
        user = User.objects.get(mobile=mobile)
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(username=mobile, email=email, mobile=mobile, name=name, is_active=True,
                                            password=User.objects.make_random_password())
    return user


class ShowBillView(OwnerListAPIView):
    """
    This view will show the details of the bill.
    """
    from .models import BillingHeader
    from .serializers import ShowBillSerializer
    # from .filters import BillingFilter

    # filter_backends = (BillingFilter, )
    queryset = BillingHeader.objects.all().order_by('-create_date')
    serializer_class = ShowBillSerializer


class AddBillingHeaderView(OwnerCreateAPIView):
    """
    This view is to create a new bill.
    """
    from .serializers import AddBillingHeaderSerializer
    from rest_framework.permissions import AllowAny

    serializer_class = AddBillingHeaderSerializer
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        from .signals import signals

        name = serializer.validated_data['name']
        email = serializer.validated_data['email']
        mobile = serializer.validated_data['mobile']

        if self.request.user.is_authenticated:
            obj = serializer.save(created_by=self.request.user)
        else:
            obj = serializer.save(created_by=get_user(email, mobile, name))
        signals.order_placed.send(bh=obj, sender=None)


class InstamojoTokenView(OwnerListAPIView):
    """
    This view is for payment gateway with Instamojo.
    """
    from rest_framework.permissions import AllowAny

    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        from django.http.response import HttpResponse

        import requests
        import json

        client_id = "test_pIMCtGp8XxFpDoVPvHYffqDpQnMvkycO0v7"
        client_secret = "test_cptumZ9rNX9TJOyS1WzveRqFfnw9wtDm4JCunScEuMmu1Sifu9Wp9xIocpAPcNMCqohvgqwI2QDs30PMVkLz5d" \
                        "kCh1q2dmLE6y1ABeZa1ZuMRA3iDqSUIUg47om"

        if client_id.startswith("test"):
            url = "https://test.instamojo.com/oauth2/token/"
            env = "test"
        else:
            env = "production"
            url = "https://www.instamojo.com/oauth2/token/"

        payload = "grant_type=client_credentials&client_id=" + client_id + "&client_secret=" + client_secret
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        token = env + json.loads(response.text)['access_token']
        return HttpResponse(token)


class InstamojoRequestPaymentView(OwnerCreateAPIView):
    from rest_framework.permissions import AllowAny

    from .serializers import RequestPaymentSerializer

    permission_classes = (AllowAny, )
    serializer_class = RequestPaymentSerializer

    def create(self, request, *args, **kwargs):
        import json
        from rest_framework.response import Response

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        data['longurl'] = json.loads(serializer.instance.payment_request_raw)['payment_request']['longurl']
        data['payment_request_id'] = serializer.instance.payment_request_id
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=201, headers=headers)

    def perform_create(self, serializer):
        import json

        from .serializers import AddBillingHeaderSerializer

        from instamojo_wrapper.api import Instamojo

        bh_data = serializer.initial_data.pop('bill')

        bh_serializer = AddBillingHeaderSerializer(data=bh_data)

        name = bh_serializer.initial_data['name']
        email = bh_serializer.initial_data['email']
        mobile = bh_serializer.initial_data['mobile']

        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = get_user(email, mobile, name)

        if bh_serializer.is_valid():
            bh_obj = bh_serializer.save(created_by=user)
        else:
            errors = bh_serializer.errors
            raise SystemError('Cannot save Billing Header Serializer')

        # Create Instamojo PaymentRequest
        imojo = Instamojo(api_key='test_2e8398986827d0737f5ba3d3a20', auth_token='test_a3dea9627890cfbf323e8c894ef',
                          endpoint='https://test.instamojo.com/api/1.1/')
        imojo_request = imojo.payment_request_create(
            purpose=serializer.validated_data['purpose'],
            amount=serializer.validated_data['amount'], buyer_name=name, email=email, phone=mobile,
            redirect_url=serializer.validated_data['redirect_url'],
            allow_repeated_payments=serializer.validated_data['allow_repeated_payments']
        )

        if imojo_request['success']:
            imojo_request_id = imojo_request['payment_request']['id']
            imojo_status = imojo_request['payment_request']['status']

            obj = serializer.save(payment_request_raw=json.dumps(imojo_request),
                                  payment_request_id=imojo_request_id, status=imojo_status, bill=bh_obj)
        else:
            raise SystemError('Instamojo Error!')


class InstamojoPaymentTrackView(RetrieveAPIView):
    from .models import InstamojoDetails
    from .serializers import ShowRequestPaymentSerializer

    from rest_framework.permissions import AllowAny

    permission_classes = (AllowAny, )
    queryset = InstamojoDetails.objects.all()
    serializer_class = ShowRequestPaymentSerializer
    lookup_field = 'payment_request_id'
    filter_backends = ()

