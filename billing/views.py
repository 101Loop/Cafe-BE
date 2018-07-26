from rest_framework.generics import ListAPIView, CreateAPIView


class ShowBillItemView(ListAPIView):
    from .models import BillItem
    from .serializers import BillItemSerializer

    queryset = BillItem.objects.all().order_by('-billheader__create_date')
    serializer_class = BillItemSerializer


class AddBillItemview(CreateAPIView):
    from .serializers import BillItemSerializer

    serializer_class = BillItemSerializer


class ShowBillingHeaderView(ListAPIView):
    from .models import BillingHeader
    from .serializers import ShowBillingHeaderSerializer

    queryset = BillingHeader.objects.all().order_by('-create_date')
    serializer_class = ShowBillingHeaderSerializer


class AddBillingHeaderView(CreateAPIView):
    from .serializers import AddBillingHeaderSerializer

    serializer_class = AddBillingHeaderSerializer
