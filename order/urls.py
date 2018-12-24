from django.urls import path

from .views import ListCreateOrderView, RetrieveOrderView, ListOutletOrderView, UpdateOrderByManager


app_name = "order"


urlpatterns = [
    # ex: api/order/order/
    path('order/', ListCreateOrderView.as_view(), name='order-list-add'),
    # ex: api/order/order/id/
    path('order/<int:pk>/', RetrieveOrderView.as_view(),
         name='order-retrieve'),
    # ex: api/order/public/id/orders/
    path('public/<int:outlet__id>/orders/', ListOutletOrderView.as_view(), name='Outlet Orders'),
    # ex: api/order/order/id/update/
    path('order/<int:pk>/update/', UpdateOrderByManager.as_view(), name='Update Order'),
]
