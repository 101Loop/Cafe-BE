from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
    # ex: api/users/login/
    path('login/', views.Login.as_view(), name='Login'),
    # ex: api/users/register/
    path('register/', views.Register.as_view(), name='Register'),
    # # ex: api/users/sendotp/
    # path('sendotp/', views.SendOTP.as_view(), name='Send OTP'),
    # # ex: api/users/verifyotp/
    # path('verifyotp/', views.VerifyOTP.as_view(), name='Verify OTP'),
    # ex: api/users/loginotp/
    path('loginotp/', views.LoginOTP.as_view(), name='Login OTP'),
    # ex: api/users/isunique/
    path('isunique/', views.CheckUnique.as_view(), name='Check Unique'),
    # ex: api/users/updateprofile/
    path('updateprofile/', views.UpdateProfileView.as_view(), name='Update-Profile'),
]
