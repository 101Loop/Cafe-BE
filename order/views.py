from drfaddons.generics import OwnerListCreateAPIView, OwnerRetrieveAPIView

from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView


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


class ManagerOwnerMixin:
    from .serializers import OrderUpdateSerializer
    from .models import Order

    from outlet.permissions import OwnerOrManager

    permission_classes = (OwnerOrManager, )
    serializer_class = OrderUpdateSerializer
    filter_backends = ()
    queryset = Order.objects.all()


class ListManagerOrderView(ManagerOwnerMixin, ListAPIView):
    """
    get: Lists orders for Manager
    """

    from django_filters.rest_framework.backends import DjangoFilterBackend

    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('outlet', 'status')

    def filter_queryset(self, queryset):
        from django.db.models import Q

        queryset = super(ListManagerOrderView, self).filter_queryset(queryset=
                                                                     queryset)

        return queryset.filter(
            Q(outlet__outletmanager__manager=self.request.user)
            | Q(outlet__created_by=self.request.user))


class RetrieveUpdateOrderView(ManagerOwnerMixin, RetrieveUpdateAPIView):
    def perform_update(self, serializer):
        serializer.save(
            managed_by=self.request.user.outletmanager_set.get(
                outlet=serializer.instance.outlet))
