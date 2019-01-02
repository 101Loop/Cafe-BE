from django.urls import path

from .views import TransactionStaticVariableView, ListTransactionView
from .views import AcceptTransactionView

app_name = 'transaction'


urlpatterns = [
    path('', TransactionStaticVariableView.as_view(),
         name='get-static-transaction'),
    path('list/', ListTransactionView.as_view(), name='list-transactions'),
    path('manager/', AcceptTransactionView.as_view(),
         name='manager-transaction')
]
