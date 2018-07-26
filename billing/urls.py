from django.urls import path
from . import views


app_name = 'billing'

urlpatterns = [
    path('show/billitem/', views.ShowBillItemView.as_view(), name='Show-Bill-Item'),
    path('add/billitem/', views.AddBillItemview.as_view(), name='Add-Bill-Item'),
    path('show/header/', views.ShowBillingHeaderView.as_view(), name='Show-Billing-Header'),
    path('add/header/', views.AddBillingHeaderView.as_view(), name='Add-Billing-Header'),
]