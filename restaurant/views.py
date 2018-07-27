from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny


class ShowItemView(ListAPIView):
    from .models import Item
    from .serializers import ShowItemSerializer

    # TODO: Set pagination
    # TODO: Add filter by tags, category
    # TODO: Add search by name, tag, category
    # TODO: Add range filter for price
    # TODO: Sort by create_date in descending order

    # TODO: After in_stock implementation, require to select store first then show item.

    permission_classes = (AllowAny, )
    queryset = Item.objects.all().order_by('-create_date')
    serializer_class = ShowItemSerializer


class ShowLunchPackView(ListAPIView):
    from .models import LunchPack
    from .serializers import LunchPackSerializer

    permission_classes = (AllowAny, )
    queryset = LunchPack.objects.all().order_by('-create_date')
    serializer_class = LunchPackSerializer


class ShowStoreView(ListAPIView):
    from .models import Store
    from .serializers import ShowStoreSerializer

    # TODO: Pagination
    # TODO: Search by name, address

    permission_classes = (AllowAny, )
    queryset = Store.objects.all().order_by('-create_date')
    serializer_class = ShowStoreSerializer
