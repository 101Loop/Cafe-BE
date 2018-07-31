from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from drfaddons.generics import OwnerCreateAPIView


class ShowItemView(ListAPIView):
    """
    This view will show all the details of the items.
    """
    from .models import HasItem, Store, Item
    from .serializers import ShowItemSerializer
    from django_filters.rest_framework import DjangoFilterBackend
    from rest_framework.filters import SearchFilter
    from .filters import RangeFiltering

    # TODO: After in_stock implementation, require to select store first then show item.

    permission_classes = (AllowAny, )
    queryset = Item.objects.all()#.filter(store_id=val).filter(in_stock=True).order_by('-create_date')
    serializer_class = ShowItemSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)

    filter_class = RangeFiltering
    search_fields = ('^name', '^tag', '^category' )


class ShowLunchPackView(ListAPIView):
    """
    This view will show all the details of the lunch pack.
    """
    from .models import LunchPack
    from .serializers import LunchPackSerializer
    from django_filters.rest_framework import DjangoFilterBackend

    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, )
    queryset = LunchPack.objects.all().order_by('-create_date')
    serializer_class = LunchPackSerializer


class ShowStoreView(ListAPIView):
    """
    This view will show all the stores.
    """
    from .models import Store
    from .serializers import ShowStoreSerializer
    from django_filters.rest_framework import DjangoFilterBackend
    from rest_framework.filters import SearchFilter

    permission_classes = (AllowAny, )
    queryset = Store.objects.all().order_by('-create_date')
    serializer_class = ShowStoreSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('^name', '^address')


class AddItemView(OwnerCreateAPIView):
    """
    This view will allow only the admin to add new items.
    """
    from .serializers import AddItemSerializer
    from rest_framework.permissions import IsAdminUser

    permission_classes = (IsAdminUser, )
    serializer_class = AddItemSerializer


class ShowOrderView(ListAPIView):
    """
    This view is to show the details of the order.
    Only admin has access to it.
    """
    from .models import Order
    from .serializers import ShowOrderSerializer
    from rest_framework.permissions import IsAdminUser

    permission_classes = (IsAdminUser, )
    queryset = Order.objects.all().order_by('-create_date')
    serializer_class = ShowOrderSerializer


class UpdateFeedbackView(UpdateAPIView):
    """
    This view is to get the feedback from the user.
    """
    from .models import Order
    from .serializers import UpdateFeedbackSerializer

    queryset = Order.objects.all()
    serializer_class = UpdateFeedbackSerializer
