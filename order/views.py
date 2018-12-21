from drfaddons.generics import OwnerCreateAPIView


class CreateOrderView(OwnerCreateAPIView):
    """
    Creates an order in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from .serializers import OrderSerializer
    from .models import Order

    serializer_class = OrderSerializer
    queryset = Order.objects.all()
