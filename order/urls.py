from django.urls import path

from .views import CreateOrderView


app_name = "order"


urlpatterns = [
    path('order/', CreateOrderView.as_view(), name='order-add'),
]
