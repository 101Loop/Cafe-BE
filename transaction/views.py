from django.utils.text import gettext_lazy as _

from rest_framework.views import APIView

from drfaddons.generics import OwnerListAPIView, OwnerListCreateAPIView


class TransactionStaticVariableView(APIView):
    """
    Transaction Static Variables

    Author: Himanshu Shankar (https://himanshus.com)
    """

    def get(self, request):
        from OfficeCafe.variables import PAYMENT_MODE_CHOICES
        from OfficeCafe.variables import PAYMENT_TYPE_CHOICES

        from drfaddons.utils import JsonResponse

        data = {'PAYMENT_TYPE': {}, 'PAYMENT_MODE': {}}
        for obj in PAYMENT_TYPE_CHOICES:
            data['PAYMENT_TYPE'][obj[1]] = obj[0]

        for obj in PAYMENT_MODE_CHOICES:
            data['PAYMENT_MODE'][obj[1]] = obj[0]

        return JsonResponse(content=data, status=200)


class ListTransactionView(OwnerListAPIView):
    from .serializers import OrderPaymentSerializer
    from .models import OrderPayment

    queryset = OrderPayment.objects.all()
    serializer_class = OrderPaymentSerializer

    filter_fields = ('order', 'payment_mode', 'payment_type', 'is_credit')


class AcceptTransactionView(OwnerListCreateAPIView):
    from django_filters.rest_framework.backends import DjangoFilterBackend

    from outlet.permissions import OwnerOrManager

    from .serializers import OrderPaymentSerializer
    from .models import OrderPayment

    permission_classes = (OwnerOrManager, )

    queryset = OrderPayment.objects.all()
    serializer_class = OrderPaymentSerializer

    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('order', 'payment_mode', 'payment_type', 'is_credit',
                     'accepted_by__manager', 'order__outlet')

    def filter_queryset(self, queryset):
        from outlet.permissions import is_manager, is_owner
        from outlet.models import Outlet

        qs = super(AcceptTransactionView, self).filter_queryset(
            queryset=queryset
        )

        if is_owner(self.request.user):
            outlet = Outlet.objects.filter(created_by=self.request.user)
        elif is_manager(self.request.user):
            outlet = Outlet.objects.filter(
                outletmanager__manager=self.request.user)
        else:
            return qs.none()

        return qs.filter(order__outlet__in=outlet)

    def perform_create(self, serializer):
        from outlet.permissions import is_manager
        from outlet.models import OutletManager

        from rest_framework.exceptions import PermissionDenied

        outlet = serializer.validated_data['order'].outlet

        if is_manager(self.request.user):
            try:
                manager = OutletManager.objects.get(
                    manager=self.request.user, is_active=True, outlet=outlet)
            except OutletManager.DoesNotExist:
                raise PermissionDenied(
                    _("User doesn't have permission on provided outlet."))

        else:
            manager = OutletManager.objects.filter(outlet=outlet).first()
            if not manager:
                manager = OutletManager.objects.create(
                    is_active=True,
                    manager=self.request.user,
                    outlet=outlet,
                    created_by=self.request.user
                )

        serializer.save(accepted_by=manager)
