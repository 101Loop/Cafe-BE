from django.urls import path

from .views import ListOrderView, RetrieveOrderView, ListManagerOrderView
from .views import RetrieveUpdateOrderView, CreateOrderView
from .views import CreateManagerOrderView


app_name = "order"


urlpatterns = [
    # ex: api/order/order/
    path('list/', ListOrderView.as_view(), name='order-list'),
    path('create/', CreateOrderView.as_view(), name='order-add'),
    # ex: api/order/id/
    path('<int:pk>/', RetrieveOrderView.as_view(), name='order-retrieve'),
    # ex: api/order/order/id/update/
    path('manager/list/', ListManagerOrderView.as_view(), name='List Order'),
    path('manager/create/', CreateManagerOrderView.as_view(),
         name='order-add-manager'),
    path('manager/<int:pk>/', RetrieveUpdateOrderView.as_view(),
         name='order-update'),
]
