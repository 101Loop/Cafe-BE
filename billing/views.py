from drfaddons.generics import OwnerCreateAPIView, OwnerListAPIView


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

    serializer_class = AddBillingHeaderSerializer

    def perform_create(self, serializer):
        from .signals import signals
        from restaurant.models import Order
        from billing.models import BillingHeader

        obj = serializer.save(created_by=self.request.user)
        signals.order_placed.send(bh=obj, sender=None)

        # order = Order()
        # order.save(id=BillingHeader.pk)


class Instamojo(OwnerListAPIView):
    from rest_framework.permissions import AllowAny

    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        import requests
        import json
        from rest_framework.response import Response

        client_id = "test_pIMCtGp8XxFpDoVPvHYffqDpQnMvkycO0v7"
        client_secret = "test_cptumZ9rNX9TJOyS1WzveRqFfnw9wtDm4JCunScEuMmu1Sifu9Wp9xIocpAPcNMCqohvgqwI2QDs30PMVkLz5dkCh1q2dmLE6y1ABeZa1ZuMRA3iDqSUIUg47om"
        env = "production"

        if (client_id.startswith("test")):
            url = "https://test.instamojo.com/oauth2/token/"
            env = "test"

        payload = "grant_type=client_credentials&client_id=" + client_id + "&client_secret=" + client_secret
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        token = env + json.loads(response.text)["access_token"]
        return Response(token)
