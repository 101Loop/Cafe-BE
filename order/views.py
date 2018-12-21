from drfaddons.generics import OwnerListCreateAPIView, OwnerRetrieveAPIView


class ListCreateOrderView(OwnerListCreateAPIView):
    """
    Creates an order in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from .serializers import OrderSerializer
    from .models import Order

    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class RetrieveOrderView(OwnerRetrieveAPIView):
    """
    Creates an order in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from .serializers import OrderSerializer
    from .models import Order

    serializer_class = OrderSerializer
    queryset = Order.objects.all()
