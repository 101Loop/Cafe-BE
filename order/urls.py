from django.urls import path

from .views import ListCreateOrderView, RetrieveOrderView


app_name = "order"


urlpatterns = [
    path('order/', ListCreateOrderView.as_view(), name='order-list-add'),
    path('order/<int:pk>', RetrieveOrderView.as_view(),
         name='order-retrieve'),
]
