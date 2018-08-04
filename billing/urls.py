from django.urls import path
from . import views


app_name = 'billing'

urlpatterns = [
    # ex: api/billing/list/
    path('list/', views.ShowBillView.as_view(), name='Show-Bill-Item'),
    # ex: api/billing/add/
    path('add/', views.AddBillingHeaderView.as_view(), name='Add-Bill-Item'),
    # ex: api/billing/instamojo/
    path('instamojo/', views.InstamojoTokenView.as_view(), name='InstaMojo'),
    # ex: api/billing/payment/
    path('instamojo/request/', views.InstamojoRequestPaymentView.as_view(), name='Payment-Request'),
    # ex: api/billing/str/payment/
    path('instamojo/<str:payment_request_id>/payment/', views.InstamojoPaymentTrackView.as_view(), name='Payment-Request'),
]
