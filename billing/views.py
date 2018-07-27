from drfaddons.generics import OwnerCreateAPIView, OwnerListAPIView


class ShowBillView(OwnerListAPIView):
    from .models import BillingHeader
    from .serializers import ShowBillSerializer

    queryset = BillingHeader.objects.all().order_by('-create_date')
    serializer_class = ShowBillSerializer


class AddBillingHeaderView(OwnerCreateAPIView):
    from .serializers import AddBillingHeaderSerializer

    serializer_class = AddBillingHeaderSerializer
