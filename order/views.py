from drfaddons.generics import OwnerListCreateAPIView, OwnerRetrieveAPIView, OwnerUpdateAPIView


class ListCreateOrderView(OwnerListCreateAPIView):
    """
    Creates an order in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from .serializers import OrderSerializer
    from .models import Order

    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class RetrieveOrderView(OwnerRetrieveAPIView):
    """
    Creates an order in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from .serializers import OrderSerializer
    from .models import Order

    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class ListOutletOrderView(OwnerRetrieveAPIView):
    """
    get: Lists orders of an outlet.
    """
    from .serializers import OrderSerializer
    from .models import Order

    from django_filters.rest_framework.backends import DjangoFilterBackend

    from outlet.permissions import OwnerOrManager

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    filter_backends = (DjangoFilterBackend, )
    permission_classes = (OwnerOrManager, )

    def filter_queryset(self, queryset):
        from outlet.models import Outlet

        from rest_framework.exceptions import NotFound

        queryset = super(ListOutletOrderView, self).filter_queryset(queryset=queryset)
        outlet_id = self.kwargs.get('outlet__id')
        try:
            outlet = Outlet.objects.get(pk=outlet_id)
        except Outlet.DoesNotExist:
            raise NotFound("Invalid Outlet ID {} - object does not "
                           "exist.".format(outlet_id))
        else:
            return queryset.filter(outlet=outlet)


class UpdateOrderByManager(OwnerUpdateAPIView):

    from .models import Order
    from .serializers import OrderUpdateSerializer
    from outlet.permissions import OwnerOrManager

    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    permission_classes = (OwnerOrManager, )
