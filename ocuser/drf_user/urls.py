from django.urls import path
from . import views


app_name = 'drf_user'

urlpatterns = [
    # ex: api/user/loginotp/
    path('loginotp/', views.LoginOTP.as_view(), name='Login OTP'),
    # ex: api/user/updateprofile/
    path('updateprofile/', views.UpdateProfileView.as_view(), name='Update-Profile'),
]
