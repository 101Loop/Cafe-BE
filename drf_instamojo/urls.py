from django.urls import path
from . import views


app_name = 'drf_instamojo'

urlpatterns = [
    # ex: api/instamojo/token/
    path('token/', views.TokenView.as_view(), name='Token View'),
    # ex: api/instamojo/paymentrequest/
    path('paymentrequest/', views.CreatePaymentRequestView.as_view(), name='Payment Request'),
    # ex: api/instamojo/trackpayment/
    path('trackpayment/', views.PaymentTrackView.as_view(), name='Track Payment'),
    # ex: api/instamojo/androidpayment/
    path('androidpayment/', views.AndroidCreatePaymentView.as_view(), name='Android Create Payment'),
]
