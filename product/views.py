from rest_framework.generics import ListAPIView


class ListCategoryView(ListAPIView):
    from .serializers import CategorySerializer
    from .models import Category

    from rest_framework.permissions import AllowAny
    from rest_framework.filters import SearchFilter

    from django_filters.rest_framework.backends import DjangoFilterBackend

    permission_classes = (AllowAny, )
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name', 'sku_prefix')
    filter_fields = ('name', 'hsn', 'sku_prefix')


class ListProductView(ListAPIView):
    from .serializers import ProductSerializer
    from .models import Product

    from rest_framework.permissions import AllowAny
    from rest_framework.filters import SearchFilter

    from django_filters.rest_framework.backends import DjangoFilterBackend

    permission_classes = (AllowAny, )
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name', 'category__name', 'sku')
    filter_fields = ('name', 'category', 'sku')
