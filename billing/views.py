from drfaddons.generics import OwnerCreateAPIView, OwnerListAPIView


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


class Instamojo(OwnerListAPIView):
    """
    This view is for payment gateway with instamojo.
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
        env = "production"

        if client_id.startswith("test"):
            url = "https://test.instamojo.com/oauth2/token/"
            env = "test"

        payload = "grant_type=client_credentials&client_id=" + client_id + "&client_secret=" + client_secret
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        token = env + json.loads(response.text)['access_token']
        return HttpResponse(token)
