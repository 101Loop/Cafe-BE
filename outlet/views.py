from rest_framework.generics import ListAPIView, RetrieveAPIView

from drfaddons import generics


class ListOutletView(ListAPIView):
    """
    List Outlets

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from rest_framework.permissions import AllowAny
    from rest_framework.filters import SearchFilter

    from django_filters.rest_framework.backends import DjangoFilterBackend

    from .models import Outlet
    from .serializers import OutletSerializer

    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('city__name', 'building', 'area', 'pincode',
                     'unit', 'business', 'business__name', 'city')
    search_fields = ('city__name', 'building', 'area', 'name', 'pincode',
                     'unit', 'business__name')

    queryset = Outlet.objects.filter(is_active=True)
    serializer_class = OutletSerializer


class RetrieveOutletView(RetrieveAPIView):
    from rest_framework.permissions import AllowAny

    from .models import Outlet
    from .serializers import OutletSerializer

    permission_classes = (AllowAny, )
    queryset = Outlet.objects.filter(is_active=True)
    serializer_class = OutletSerializer
    filter_backends = ()


class ListOutletServiceableAreaView(ListAPIView):
    """
    Outlet Serviceable Areas

    Author: Himanshu Shankar (https://himanshus.com)
    """
    from rest_framework.permissions import AllowAny
    from rest_framework.filters import SearchFilter

    from django_filters.rest_framework.backends import DjangoFilterBackend

    from location.serializers import AreaSerializer

    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)

    serializer_class = AreaSerializer

    def get_queryset(self):
        from rest_framework.exceptions import NotFound

        from .models import Outlet

        outlet_id = self.kwargs.get('outlet__id')
        try:
            outlet = Outlet.objects.get(pk=outlet_id, is_active=True)
        except Outlet.DoesNotExist:
            raise NotFound("Invalid Outlet ID {} - object does not "
                           "exist.".format(outlet_id))
        else:
            return outlet.serviceable_area.all()


class ListOutletProductView(ListAPIView):
    """
    get: Lists product available in a particular outlet

    Author: Himanshu Shankar (https://himanshus.com)
    """
    from rest_framework.permissions import AllowAny
    from rest_framework.filters import SearchFilter

    from django_filters.rest_framework.backends import DjangoFilterBackend

    from .models import OutletProduct
    from .serializers import OutletProductSerializer

    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('product__name', 'product__category',
                     'product__category__name')
    search_fields = ('product__name', 'product__category__name', )

    queryset = OutletProduct.objects.filter(stock__gt=0, outlet__is_active=True)
    serializer_class = OutletProductSerializer

    def filter_queryset(self, queryset):
        from rest_framework.exceptions import NotFound

        from .models import Outlet

        queryset = super(ListOutletProductView, self).filter_queryset(
            queryset=queryset)
        outlet_id = self.kwargs.get('outlet__id')
        try:
            outlet = Outlet.objects.get(pk=outlet_id, is_active=True)
        except Outlet.DoesNotExist:
            raise NotFound("Invalid Outlet ID {} - object does not "
                           "exist.".format(outlet_id))
        else:
            return queryset.filter(outlet=outlet)


class RetrieveProductView(RetrieveAPIView):
    """
    get: List details of a specific product.
    """
    from rest_framework.permissions import AllowAny
    from rest_framework.filters import SearchFilter

    from django_filters.rest_framework.backends import DjangoFilterBackend

    from .models import OutletProduct
    from .serializers import OutletProductSerializer

    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, SearchFilter)

    queryset = OutletProduct.objects.filter(stock__gt=0, outlet__is_active=True)
    serializer_class = OutletProductSerializer

    lookup_field = 'product_id'

    def filter_queryset(self, queryset):
        from rest_framework.exceptions import NotFound

        from .models import Outlet

        queryset = super(RetrieveProductView, self).filter_queryset(
            queryset=queryset)
        outlet_id = self.kwargs.get('outlet_id')
        try:
            outlet = Outlet.objects.get(pk=outlet_id, is_active=True)
        except Outlet.DoesNotExist:
            raise NotFound("Invalid Outlet ID {} - object does not "
                           "exist.".format(outlet_id))
        else:
            return queryset.filter(outlet=outlet)


class ListManagerOutletView(ListAPIView):
    """
    get: Lists all the managers of an outlet.
    """
    from .permissions import OwnerOrManager
    from .models import Outlet
    from .serializers import OutletSerializer

    from django_filters.rest_framework.backends import DjangoFilterBackend

    from rest_framework.filters import SearchFilter

    permission_classes = (OwnerOrManager, )

    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('business', 'city', 'pincode', 'is_active')
    search_fields = ('name', 'business__name', 'city__name', 'pincode',
                     'building', 'area')

    def filter_queryset(self, queryset):
        from django.db.models import Q

        queryset = super(ListManagerOutletView, self).filter_queryset(queryset)

        return queryset.filter(Q(outletmanager__manager=self.request.user)
                               | Q(created_by=self.request.user)).distinct()


class ListOwnerOutletView(generics.OwnerListAPIView):
    from .serializers import OutletSerializer
    from .models import Outlet

    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer
