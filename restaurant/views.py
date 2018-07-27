from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny


class ShowItemView(ListAPIView):
    from .models import Item
    from .serializers import ShowItemSerializer
    from drfaddons.filters import IsOwnerFilterBackend
    from django_filters.rest_framework import DjangoFilterBackend
    from rest_framework.filters import SearchFilter
    from .filters import RangeFiltering

    # TODO: After in_stock implementation, require to select store first then show item.

    permission_classes = (AllowAny, )
    queryset = Item.objects.all().order_by('-create_date')
    serializer_class = ShowItemSerializer
    filter_backends = (IsOwnerFilterBackend, DjangoFilterBackend, SearchFilter)

    filter_class = RangeFiltering
    search_fields = ('^name', '^tag', '^category' )


class ShowLunchPackView(ListAPIView):
    from .models import LunchPack
    from .serializers import LunchPackSerializer

    permission_classes = (AllowAny, )
    queryset = LunchPack.objects.all().order_by('-create_date')
    serializer_class = LunchPackSerializer


class ShowStoreView(ListAPIView):
    from .models import Store
    from .serializers import ShowStoreSerializer
    from drfaddons.filters import IsOwnerFilterBackend
    from django_filters.rest_framework import DjangoFilterBackend
    from rest_framework.filters import SearchFilter

    permission_classes = (AllowAny, )
    queryset = Store.objects.all().order_by('-create_date')
    serializer_class = ShowStoreSerializer
    filter_backends = (IsOwnerFilterBackend, DjangoFilterBackend, SearchFilter)
    search_fields = ('^name', '^address')
