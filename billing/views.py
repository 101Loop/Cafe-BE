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

        obj = serializer.save(created_by=self.request.user)
        signals.order_placed.send(bh=obj, sender=None)
