from rest_framework.generics import ListAPIView


class ShowMenuView(ListAPIView):
    from .models import Menu
    from .serializers import ShowMenuSerializer

    queryset = Menu.objects.all()
    serializer_class = ShowMenuSerializer
