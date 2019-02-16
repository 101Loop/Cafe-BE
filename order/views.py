from drfaddons.generics import OwnerCreateAPIView, OwnerRetrieveAPIView
from drfaddons.generics import OwnerListAPIView

from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView


class ListOrderView(OwnerListAPIView):
    """
    Creates an order in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from .serializers import OrderListSerializer
    from .models import Order

    serializer_class = OrderListSerializer
    queryset = Order.objects.all()


class CreateOrderView(OwnerCreateAPIView):
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

    from rest_framework.filters import SearchFilter

    from django_filters.rest_framework.backends import DjangoFilterBackend

    from outlet.permissions import OwnerOrManager

    permission_classes = (OwnerOrManager, )
    serializer_class = OrderUpdateSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name', 'mobile', 'email', 'status')
    queryset = Order.objects.all()


class CreateManagerOrderView(ManagerOwnerMixin, CreateOrderView):
    from .serializers import ManagerOrderSerializer

    serializer_class = ManagerOrderSerializer

    def perform_create(self, serializer):
        from outlet.models import OutletManager

        outlet_manager = OutletManager.objects.get(
            manager_id=self.request.user.id,
            outlet_id=serializer.validated_data['outlet'].id
        )
        if not serializer.validated_data['created_by']:
            serializer.save(
                created_by=self.request.user,
                managed_by=outlet_manager
            )
        else:
            serializer.save(managed_by=self.request.user)


class ListManagerOrderView(ManagerOwnerMixin, ListAPIView):
    """
    get: Lists orders for Manager
    """

    from .serializers import OrderListSerializer

    filter_fields = ('outlet', 'status')
    serializer_class = OrderListSerializer

    def filter_queryset(self, queryset):
        from django.db.models import Q

        queryset = super(ListManagerOrderView, self).filter_queryset(queryset=
                                                                     queryset)

        return queryset.filter(
            Q(outlet__outletmanager__manager=self.request.user) |
            Q(outlet__created_by=self.request.user)).distinct()


class RetrieveUpdateOrderView(ManagerOwnerMixin, RetrieveUpdateAPIView):
    def perform_update(self, serializer):
        from outlet.permissions import is_manager

        if is_manager(self.request.user):
            serializer.save(
                managed_by=serializer.instance.outlet.outletmanager_set.get(
                    manager=self.request.user, is_active=True
                ))
        else:
            serializer.save(
                managed_by=serializer.instance.outlet.outletmanager_set.filter(
                    is_active=True
                ).first()
            )
