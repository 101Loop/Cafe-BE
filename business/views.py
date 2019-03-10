from drfaddons import generics


class BusinessMixin:
    from django_filters.rest_framework.backends import DjangoFilterBackend
    from rest_framework.filters import SearchFilter

    from drfaddons.filters import IsOwnerOrSuperuser

    from .serializers import BusinessSerializer
    from .models import Business

    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

    filter_backends = (IsOwnerOrSuperuser, DjangoFilterBackend,
                       SearchFilter)
    filter_fields = ('business_type', 'state', 'is_active')
    search_fields = ('name', 'gst', 'pan')


class ListBusinessView(BusinessMixin, generics.OwnerListAPIView):
    from drfaddons.permissions import IsAuthenticatedWithPermission

    permission_classes = (IsAuthenticatedWithPermission, )
