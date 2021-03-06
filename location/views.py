from rest_framework.generics import ListAPIView


class ListCountryView(ListAPIView):
    from rest_framework.permissions import AllowAny
    from rest_framework.filters import SearchFilter

    from .models import Country
    from .serializers import CountrySerializer

    permission_classes = (AllowAny, )
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    filter_backends = (SearchFilter, )
    search_fields = ('name', )


class ListStateView(ListAPIView):
    from rest_framework.permissions import AllowAny
    from rest_framework.filters import SearchFilter

    from django_filters.rest_framework.backends import DjangoFilterBackend

    from .models import State
    from .serializers import StateSerializer

    permission_classes = (AllowAny, )

    queryset = State.objects.all()
    serializer_class = StateSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('country__name', )
    search_fields = ('name', 'country__name')


class ListCityView(ListAPIView):
    from rest_framework.permissions import AllowAny
    from rest_framework.filters import SearchFilter

    from django_filters.rest_framework.backends import DjangoFilterBackend

    from .models import City
    from .serializers import CitySerializer

    permission_classes = (AllowAny, )
    queryset = City.objects.all()
    serializer_class = CitySerializer

    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('state__country__name', 'state__name')
    search_fields = ('name', 'state__country__name', 'state__name')


class ListAreaView(ListAPIView):
    from rest_framework.permissions import AllowAny
    from rest_framework.filters import SearchFilter

    from django_filters.rest_framework.backends import DjangoFilterBackend

    from .models import Area
    from .serializers import AreaSerializer

    permission_classes = (AllowAny, )
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('city', 'city__name', 'pincode')
    search_fields = ('name', 'pincode', 'city__name')


class ListBuildingComplexView(ListAPIView):
    from rest_framework.permissions import AllowAny
    from rest_framework.filters import SearchFilter

    from django_filters.rest_framework.backends import DjangoFilterBackend

    from .models import BuildingComplex
    from .serializers import BuildingComplexSerializer

    permission_classes = (AllowAny,)
    queryset = BuildingComplex.objects.all()
    serializer_class = BuildingComplexSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('area', 'area__name')
    search_fields = ('name', 'area', 'area__name', 'area__pincode')
