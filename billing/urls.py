from django.urls import path
from . import views


app_name = 'billing'

urlpatterns = [
    path('list/', views.ShowBillView.as_view(), name='Show-Bill-Item'),
    path('add/', views.AddBillingHeaderView.as_view(), name='Add-Bill-Item'),
]
