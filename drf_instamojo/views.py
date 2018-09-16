from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView


# TODO: Import this from drfaddons
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


def get_imojo_obj():
    from instamojo_wrapper.api import Instamojo

    return Instamojo(api_key='test_2e8398986827d0737f5ba3d3a20', auth_token='test_a3dea9627890cfbf323e8c894ef',
                              endpoint='https://test.instamojo.com/api/1.1/')


def update_payments(payment_request):
    from .models import Payment

    import json

    from billing.serializers import ShowBillSerializer

    imojo = get_imojo_obj()

    imojo = imojo.payment_request_status(payment_request.id)

    if imojo['success']:
        imojo_payment_request = imojo['payment_request']
        payments = imojo_payment_request['payments']
        status = 202
        for each_payment in payments:
            try:
                Payment.objects.get(id=each_payment['payment_id'])
                status = 202
            except Payment.DoesNotExist:
                payment_obj = Payment()
                payment_obj.id = each_payment['payment_id']
                payment_obj.instamojo_raw_response = json.dumps(each_payment)
                payment_obj.payment_request = payment_request
                payment_obj.mac = None
                if each_payment['status'] == 'Failed':
                    payment_obj.status = 'F'
                else:
                    payment_obj.status = 'C'
                    if not payment_request.bill.paid:
                        payment_request.bill.paid = True
                        payment_request.bill.save()
                payment_obj.fees = each_payment['fees']
                payment_obj.currency = each_payment['currency']
                payment_obj.save()
                status = 201
        if payment_request.status != imojo_payment_request['status']:
            payment_request.status = imojo_payment_request['status']
            payment_request.save()
            status = 201
        data = ShowBillSerializer(payment_request.bill).data
    else:
        data = {'instamojo': imojo}
        status = 500

    return data, status


def create_payment_request_from_id(id, bill):
    from .models import PaymentRequest

    import json

    imojo = get_imojo_obj()
    imojo = imojo.payment_request_status(id)

    if imojo['success']:
        imojo = imojo['payment_request']
        try:
            payment_request = PaymentRequest.objects.get(id=id)
        except PaymentRequest.DoesNotExist:
            payment_request = PaymentRequest()
            payment_request.id = id
        payment_request.amount = imojo['amount']
        payment_request.purpose = imojo['purpose']
        payment_request.redirect_url = imojo['redirect_url']
        payment_request.allow_repeated_payments = imojo['allow_repeated_payments']
        payment_request.instamojo_raw_response = json.dumps(imojo)
        payment_request.longurl = imojo['longurl']
        payment_request.expires_at = imojo['expires_at']
        payment_request.status = imojo['status']
        payment_request.bill = bill
        payment_request.save()
        return payment_request
    else:
        # TODO: this error should return in JSON Format
        raise ValueError(imojo)


class TokenView(APIView):
    """
    This view is for payment gateway integration with Instamojo.
    It will return a token that will be further used for payment request via instamojo.
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


class CreatePaymentRequestView(CreateAPIView):
    """
    This view will return a long url which will be used to fetch payment request id
    which will be further used to track the payment request.
    """
    from rest_framework.permissions import AllowAny

    from .serializers import CreatePaymentRequestSerializer

    permission_classes = (AllowAny, )
    serializer_class = CreatePaymentRequestSerializer

    def create(self, request, *args, **kwargs):
        from rest_framework.response import Response

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data, status = self.perform_create(serializer)
        return Response(data, status=status)

    def perform_create(self, serializer):
        import json

        from billing.signals import signals

        from billing.serializers import AddBillingHeaderSerializer

        bill = AddBillingHeaderSerializer(data=serializer.initial_data.pop('bill'))
        bill.is_valid(raise_exception=True)

        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = get_user(bill.validated_data['email'], bill.validated_data['mobile'], bill.validated_data['name'])

        bill = bill.save(created_by=user)

        amount = round(bill.total, 2)

        if amount < 9:
            bill.save(mode='C')
            signals.order_placed.send(bh=bill, sender=None)
            data = serializer.validated_data
            data['bill'] = bill
            data['longurl'] = None
            data['id'] = None
            status = 201
        else:
            # Create Instamojo PaymentRequest
            imojo = get_imojo_obj()
            imojo_request = imojo.payment_request_create(
                purpose=serializer.validated_data['purpose'],
                amount=amount, buyer_name=bill.name, email=bill.email, phone=bill.mobile,
                redirect_url=serializer.validated_data['redirect_url'],
                allow_repeated_payments=False
            )

            if imojo_request['success']:
                request_id = imojo_request['payment_request']['id']
                status_imojo = imojo_request['payment_request']['status']
                serializer.save(instamojo_raw_response=json.dumps(imojo_request), id=request_id, status=status_imojo,
                                bill=bill, longurl=imojo_request['payment_request']['longurl'], amount=bill.total)

                data = serializer.data
                status = 201
            else:
                data = {'instamojo': imojo_request}
                status = 500

        return data, status


class PaymentTrackView(RetrieveAPIView):
    """
    This view is to track the payment and return the response of whether payment is competed or not.
    """
    from .models import PaymentRequest

    from rest_framework.permissions import AllowAny
    from rest_framework.serializers import Serializer

    permission_classes = (AllowAny, )
    queryset = PaymentRequest.objects.all().order_by('-bill__create_date')
    filter_backends = ()
    serializer_class = Serializer

    def retrieve(self, request, *args, **kwargs):
        import json

        from billing.signals import signals

        from rest_framework.response import Response

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)
        instamojo_object = serializer.instance

        if instamojo_object.bill.paid:
            from billing.serializers import ShowBillSerializer

            return Response(ShowBillSerializer(instamojo_object.bill).data, status=202)

        data, status = self.perform_update(serializer)
        if instamojo_object.status == 'Completed':
            signals.order_placed.send(bh=instamojo_object.bill, sender=None)
            return Response(data, status=status)
        else:
            if status != 500:
                data = {'message': 'Payment is still pending or has failed. try again.',
                        'longurl': json.loads(instamojo_object.instamojo_raw_response)['payment_request']['longurl']}
            return Response(data, status=status)

    def perform_update(self, serializer):
        payment_request = serializer.instance

        data, status = update_payments(payment_request)

        return data, status


class AndroidCreatePaymentView(CreateAPIView):
    """
    This view is for payment gateway integration for android.
    """
    from rest_framework.permissions import AllowAny

    from .serializers import AndroidCreatePaymentSerializer

    permission_classes = (AllowAny, )
    serializer_class = AndroidCreatePaymentSerializer

    def create(self, request, *args, **kwargs):
        from rest_framework.response import Response

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data, status = self.perform_create(serializer)
        return Response(data, status=status)

    def perform_create(self, serializer):
        from billing.signals import signals

        from billing.serializers import AddBillingHeaderSerializer

        bill = AddBillingHeaderSerializer(data=serializer.initial_data.pop('bill'))
        bill.is_valid(raise_exception=True)

        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = get_user(bill.validated_data['email'], bill.validated_data['mobile'], bill.validated_data['name'])

        bill = bill.save(created_by=user)
        signals.order_placed.send(bh=bill, sender=None)

        payment_request = create_payment_request_from_id(serializer.validated_data.pop('payment_id'), bill)
        data, status = update_payments(payment_request)

        return data, status
