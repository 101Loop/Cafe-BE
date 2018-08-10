from django.urls import path
from . import views


app_name = 'drf_instamojo'

urlpatterns = [
    path('token/', views.TokenView.as_view(), name='Token View'),
    path('paymentrequest/', views.CreatePaymentRequestView.as_view(), name='Payment Request'),
    path('trackpayment/', views.PaymentTrackView.as_view(), name='Track Payment'),
    path('createpayment/', views.AndroidCreatePaymentView.as_view(), name='Android Create Payment'),
]
