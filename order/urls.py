from django.urls import path

from .views import ListCreateOrderView, RetrieveOrderView, ListManagerOrderView
from .views import RetrieveUpdateOrderView


app_name = "order"


urlpatterns = [
    # ex: api/order/order/
    path('order/', ListCreateOrderView.as_view(), name='order-list-add'),
    # ex: api/order/order/id/
    path('order/<int:pk>/', RetrieveOrderView.as_view(),
         name='order-retrieve'),
    # ex: api/order/order/id/update/
    path('manager/order/', ListManagerOrderView.as_view(), name='List Order'),
    path('manager/<int:pk>/', RetrieveUpdateOrderView.as_view(),
         name='Update Order'),
]
