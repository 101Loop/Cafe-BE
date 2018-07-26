from rest_framework.generics import ListAPIView, CreateAPIView


class ShowItemView(ListAPIView):
    from .models import Item
    from .serializers import ShowItemSerializer

    queryset = Item.objects.all().order_by('-create_date')
    serializer_class = ShowItemSerializer


class AddItemView(CreateAPIView):
    from .serializers import AddItemSerializer

    serializer_class = AddItemSerializer


class ShowLunchPackView(ListAPIView):
    from .models import LunchPack
    from .serializers import LunchPackSerializer

    queryset = LunchPack.objects.all().order_by('-create_date')
    serializer_class = LunchPackSerializer


class AddLunchPackView(CreateAPIView):
    from .serializers import LunchPackSerializer

    serializer_class = LunchPackSerializer


class ShowStoreView(ListAPIView):
    from .models import Store
    from .serializers import ShowStoreSerializer

    queryset = Store.objects.all().order_by('-create_date')
    serializer_class = ShowStoreSerializer


class AddStoreView(CreateAPIView):
    from .serializers import AddStoreSerializer

    serializer_class = AddStoreSerializer
