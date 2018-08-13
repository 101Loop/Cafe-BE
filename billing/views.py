from drfaddons.generics import OwnerCreateAPIView, OwnerListAPIView

from rest_framework.generics import RetrieveAPIView


# TODO: Import this from drfaddons
def get_user(email: str, mobile: str, name: str=None):
    from django.contrib.auth import get_user_model

    User = get_user_model()

    try:
        user = User.objects.get(mobile=mobile)
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(username=mobile, email=email, mobile=mobile, name=name, is_active=True,
                                            password=User.objects.make_random_password())
    return user


class GetBillView(RetrieveAPIView):
    """
    This view will show the details of a particular bill using primary key of the bill.
    """
    from .models import BillingHeader
    from .serializers import ShowBillSerializer
    from rest_framework.permissions import AllowAny
    from django_filters.rest_framework import DjangoFilterBackend

    filter_backends = (DjangoFilterBackend ,)
    permission_classes = (AllowAny, )
    queryset = BillingHeader.objects.all().order_by('-create_date')
    serializer_class = ShowBillSerializer


class ShowBillView(OwnerListAPIView):
    """
    This view will show the details of all the bills.
    Only admin has access to it.
    """
    from .models import BillingHeader
    from .serializers import ShowBillSerializer
    from rest_framework.permissions import IsAdminUser
    from django_filters.rest_framework import DjangoFilterBackend
    from restaurant.paginations import CustomPageSizePagination

    pagination_class = CustomPageSizePagination
    permission_classes = (IsAdminUser, )
    filter_backends = (DjangoFilterBackend, )
    queryset = BillingHeader.objects.all().order_by('-create_date')
    serializer_class = ShowBillSerializer


class AddBillingHeaderView(OwnerCreateAPIView):
    """
    This view is to create a new bill.
    """
    from .serializers import AddBillingHeaderSerializer
    from rest_framework.permissions import AllowAny

    serializer_class = AddBillingHeaderSerializer
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        from .signals import signals

        name = serializer.validated_data['name']
        email = serializer.validated_data['email']
        mobile = serializer.validated_data['mobile']

        if self.request.user.is_authenticated:
            obj = serializer.save(created_by=self.request.user)
        else:
            obj = serializer.save(created_by=get_user(email, mobile, name))
        signals.order_placed.send(bh=obj, sender=None)
