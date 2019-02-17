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


class ListCreateBusinessView(BusinessMixin,
                             generics.OwnerListCreateAPIView):
    pass


class RetrieveUpdateBusinessView(BusinessMixin,
                                 generics.OwnerRetrieveUpdateAPIView):
    pass


class ListCreateBusinessDocumentView(generics.OwnerListCreateAPIView):
    from .models import BusinessDocument

    queryset = BusinessDocument.objects.all()

    def get_queryset(self):
        qs = super(ListCreateBusinessDocumentView, self).get_queryset()

